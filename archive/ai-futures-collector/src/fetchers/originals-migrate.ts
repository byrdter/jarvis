/**
 * Build the originals/ mirror tree for the wiki + record canonical artifact
 * paths in wiki-graph.db. One-time migration; safe to re-run (idempotent).
 *
 * What this does:
 *   1. Adds items.original_path TEXT and items.original_kind TEXT columns
 *      if they don't already exist.
 *   2. For each wiki/academic-library/<slug>.md, reads the frontmatter
 *      origin_file field, locates the sibling .pdf in EffectAI24-26/
 *      or EffectOnWork/, and copies it to originals/academic-library/<slug>.pdf
 *      (skip if destination already exists and is identical in size).
 *   3. Updates the DB row with original_path + original_kind='pdf'.
 *
 * Flags:
 *   --dry-run        Print actions, write nothing.
 *   --limit N        Only process the first N matching items.
 *   --category C     Restrict to a single category (default: academic-library).
 *
 * Usage:
 *   bun run src/fetchers/originals-migrate.ts --dry-run --limit 3
 *   bun run src/fetchers/originals-migrate.ts            # full migration
 */

import { Database } from 'bun:sqlite';
import { readFileSync, existsSync, mkdirSync, copyFileSync, statSync } from 'fs';
import { join, dirname } from 'path';

const WIKI_ROOT = '/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis-private/ai-futures-wiki';
const DB_PATH = join(WIKI_ROOT, 'wiki-graph.db');
const ORIGINALS_ROOT = join(WIKI_ROOT, 'originals');

interface Args {
  dryRun: boolean;
  limit: number | null;
  category: string;
}

function parseArgs(argv: string[]): Args {
  const a: Args = { dryRun: false, limit: null, category: 'academic-library' };
  for (let i = 0; i < argv.length; i++) {
    const v = argv[i];
    if (v === '--dry-run') a.dryRun = true;
    else if (v === '--limit') a.limit = parseInt(argv[++i] ?? '0', 10) || null;
    else if (v === '--category') a.category = argv[++i] ?? a.category;
  }
  return a;
}

function ensureSchema(db: Database, dryRun: boolean): void {
  const cols = db.query<{ name: string }, []>(`PRAGMA table_info(items)`).all();
  const have = new Set(cols.map((c) => c.name));
  const stmts: string[] = [];
  if (!have.has('original_path')) stmts.push(`ALTER TABLE items ADD COLUMN original_path TEXT`);
  if (!have.has('original_kind')) stmts.push(`ALTER TABLE items ADD COLUMN original_kind TEXT`);
  if (stmts.length === 0) {
    console.log('[schema] original_path/original_kind columns already present');
    return;
  }
  if (dryRun) {
    console.log('[schema] would run:');
    for (const s of stmts) console.log('  ' + s);
    return;
  }
  for (const s of stmts) {
    db.exec(s);
    console.log('[schema] applied: ' + s);
  }
}

// Parse YAML frontmatter (simple — just the fields we need).
function readFrontmatter(mdPath: string): Record<string, string> | null {
  if (!existsSync(mdPath)) return null;
  const text = readFileSync(mdPath, 'utf-8');
  if (!text.startsWith('---\n')) return null;
  const end = text.indexOf('\n---\n', 4);
  if (end === -1) return null;
  const block = text.slice(4, end);
  const out: Record<string, string> = {};
  for (const line of block.split('\n')) {
    const m = line.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$/);
    if (!m) continue;
    let v = m[2]!.trim();
    if (v.startsWith('"') && v.endsWith('"')) v = v.slice(1, -1);
    out[m[1]!] = v;
  }
  return out;
}

// Given a wiki .md page slug + an origin_file like
// "EffectAI24-26/AIAutomationAugmentationHBR2026.md", derive the canonical
// source PDF location. The original PDF lives as a sibling of the .md
// extraction (same basename, .pdf extension).
function resolvePdf(originFile: string): string | null {
  if (!originFile) return null;
  const candidate = join(WIKI_ROOT, originFile.replace(/\.md$/i, '.pdf'));
  return existsSync(candidate) ? candidate : null;
}

interface Plan {
  itemId: number;
  wikiPath: string;
  slug: string;
  src: string;        // absolute path to source PDF
  dst: string;        // absolute path to originals/<cat>/<slug>.pdf
  dstRel: string;     // relative-to-wiki-root path stored in DB
  action: 'copy' | 'skip-exists' | 'skip-no-pdf' | 'skip-no-origin';
}

function planFor(db: Database, category: string, limit: number | null): Plan[] {
  const rows = db
    .query<{ id: number; path: string }, [string]>(
      `SELECT id, path FROM items WHERE category = ? ORDER BY id`
    )
    .all(category);
  const plans: Plan[] = [];
  for (const r of rows) {
    if (limit !== null && plans.filter((p) => p.action === 'copy').length >= limit) break;
    const mdAbs = join(WIKI_ROOT, 'wiki', r.path);
    const fm = readFrontmatter(mdAbs) ?? {};
    const slug = r.path.split('/').pop()!.replace(/\.md$/i, '');
    const dstRel = join('originals', category, slug + '.pdf');
    const dstAbs = join(WIKI_ROOT, dstRel);

    const origin = fm.origin_file ?? '';
    if (!origin) {
      plans.push({ itemId: r.id, wikiPath: r.path, slug, src: '', dst: dstAbs, dstRel, action: 'skip-no-origin' });
      continue;
    }
    const src = resolvePdf(origin);
    if (!src) {
      plans.push({ itemId: r.id, wikiPath: r.path, slug, src: '', dst: dstAbs, dstRel, action: 'skip-no-pdf' });
      continue;
    }
    if (existsSync(dstAbs) && statSync(dstAbs).size === statSync(src).size) {
      plans.push({ itemId: r.id, wikiPath: r.path, slug, src, dst: dstAbs, dstRel, action: 'skip-exists' });
      continue;
    }
    plans.push({ itemId: r.id, wikiPath: r.path, slug, src, dst: dstAbs, dstRel, action: 'copy' });
  }
  return plans;
}

function execute(db: Database, plans: Plan[], dryRun: boolean): void {
  let copied = 0, recorded = 0;
  // Only prepare the UPDATE if the column exists (skipped in dry-run when the
  // ALTER hasn't actually run yet).
  const upd = dryRun
    ? null
    : db.prepare<unknown, [string, string, number]>(
        `UPDATE items SET original_path = ?, original_kind = ? WHERE id = ?`
      );
  for (const p of plans) {
    if (p.action === 'copy') {
      if (dryRun) {
        console.log(`[copy] ${p.src} -> ${p.dstRel}`);
      } else {
        mkdirSync(dirname(p.dst), { recursive: true });
        copyFileSync(p.src, p.dst);
        copied++;
      }
    }
    if (p.action === 'copy' || p.action === 'skip-exists') {
      if (dryRun) {
        console.log(`[db]   would set original_path=${p.dstRel} kind=pdf for item ${p.itemId} (${p.wikiPath})`);
      } else {
        upd!.run(p.dstRel, 'pdf', p.itemId);
        recorded++;
      }
    } else {
      console.log(`[${p.action}] ${p.wikiPath}`);
    }
  }
  console.log(`\nSummary: copied=${copied} recorded=${recorded} (dry-run=${dryRun})`);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  console.log(`[migrate] wiki=${WIKI_ROOT}`);
  console.log(`[migrate] originals=${ORIGINALS_ROOT}`);
  console.log(`[migrate] category=${args.category} dryRun=${args.dryRun} limit=${args.limit ?? 'all'}\n`);

  const db = new Database(DB_PATH);
  try {
    ensureSchema(db, args.dryRun);
    const plans = planFor(db, args.category, args.limit);
    const byAction = plans.reduce<Record<string, number>>((acc, p) => {
      acc[p.action] = (acc[p.action] ?? 0) + 1;
      return acc;
    }, {});
    console.log(`[plan] ${JSON.stringify(byAction)}\n`);
    execute(db, plans, args.dryRun);
  } finally {
    db.close();
  }
}

main();

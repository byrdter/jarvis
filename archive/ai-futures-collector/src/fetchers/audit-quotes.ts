/**
 * Audit every notable_quote against its source PDF.
 *
 * For each quote with a non-null original_path of kind 'pdf':
 *   1. Extract the PDF text once via pdftotext (cached per PDF).
 *   2. Aggressively normalize both quote and PDF text (smart quotes, dashes,
 *      ligatures, hyphenation across line breaks, all non-alphanumeric chars).
 *      The fingerprint comparison becomes formatting-blind.
 *   3. Fingerprint = middle ~60% of normalized quote, capped at 80 alphanumeric
 *      chars. Substring containment in normalized PDF text.
 *   4. Categorize: VERIFIED | NOT_FOUND | NO_PDF.
 *
 * Adds a `verified` TEXT column to notable_quotes ('yes' | 'no' | 'no-pdf').
 *
 * Flags:
 *   --dry-run        Don't write verdicts to the DB.
 *   --limit N        Only audit the first N quotes.
 *   --item-id N      Audit only quotes from item id N.
 *   --report         Print a per-paper summary instead of per-quote detail.
 *
 * Usage:
 *   bun run src/fetchers/audit-quotes.ts --report     # full audit
 */

import { Database } from 'bun:sqlite';
import { existsSync } from 'fs';
import { join } from 'path';
import { spawnSync } from 'child_process';

const WIKI_ROOT = '/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis-private/ai-futures-wiki';
const DB_PATH = join(WIKI_ROOT, 'wiki-graph.db');
const PDFTOTEXT = '/opt/homebrew/bin/pdftotext';

interface Args {
  dryRun: boolean;
  limit: number | null;
  itemId: number | null;
  report: boolean;
}

function parseArgs(argv: string[]): Args {
  const a: Args = { dryRun: false, limit: null, itemId: null, report: false };
  for (let i = 0; i < argv.length; i++) {
    const v = argv[i];
    if (v === '--dry-run') a.dryRun = true;
    else if (v === '--report') a.report = true;
    else if (v === '--limit') a.limit = parseInt(argv[++i] ?? '0', 10) || null;
    else if (v === '--item-id') a.itemId = parseInt(argv[++i] ?? '0', 10) || null;
  }
  return a;
}

function ensureVerifiedColumn(db: Database, dryRun: boolean): void {
  const cols = db.query<{ name: string }, []>('PRAGMA table_info(notable_quotes)').all();
  if (cols.some((c) => c.name === 'verified')) return;
  if (dryRun) { console.log('[schema] would add notable_quotes.verified column'); return; }
  db.exec('ALTER TABLE notable_quotes ADD COLUMN verified TEXT');
  console.log('[schema] added notable_quotes.verified column');
}

// Aggressive normalization. Drops ALL non-alphanumerics so smart quotes,
// dashes, line breaks, hyphenation, whitespace, and punctuation differences
// can't produce false negatives. The fingerprint substring becomes a pure
// lowercase alnum string that should appear identically in any text rendering.
function normalize(s: string): string {
  return s
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '');
}

function pdfText(absPath: string): string {
  const r = spawnSync(PDFTOTEXT, [absPath, '-'], { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 });
  if (r.status !== 0) return '';
  return r.stdout;
}

interface QuoteRow {
  id: number;
  item_id: number;
  quote: string;
  page: number | null;
  extractor_model: string | null;
  item_path: string;
  original_path: string | null;
  original_kind: string | null;
}

function quotes(db: Database, args: Args): QuoteRow[] {
  const where: string[] = [];
  const params: any[] = [];
  if (args.itemId !== null) { where.push('q.item_id = ?'); params.push(args.itemId); }
  const sql = `
    SELECT q.id, q.item_id, q.quote, q.page, q.extractor_model,
           i.path as item_path, i.original_path, i.original_kind
      FROM notable_quotes q
      JOIN items i ON i.id = q.item_id
      ${where.length ? 'WHERE ' + where.join(' AND ') : ''}
      ORDER BY q.item_id, q.id
  `;
  const rows = db.query<QuoteRow, any[]>(sql).all(...params);
  return args.limit ? rows.slice(0, args.limit) : rows;
}

interface Verdict {
  id: number;
  item_id: number;
  item_path: string;
  verdict: 'yes' | 'no' | 'no-pdf';
}

function audit(db: Database, args: Args): Verdict[] {
  const qs = quotes(db, args);
  const pdfCache = new Map<string, string>();
  const verdicts: Verdict[] = [];

  for (const q of qs) {
    if (!q.original_path || q.original_kind !== 'pdf') {
      verdicts.push({ id: q.id, item_id: q.item_id, item_path: q.item_path, verdict: 'no-pdf' });
      continue;
    }
    const abs = join(WIKI_ROOT, q.original_path);
    if (!existsSync(abs)) {
      verdicts.push({ id: q.id, item_id: q.item_id, item_path: q.item_path, verdict: 'no-pdf' });
      continue;
    }
    if (!pdfCache.has(q.original_path)) {
      pdfCache.set(q.original_path, normalize(pdfText(abs)));
    }
    const haystack = pdfCache.get(q.original_path)!;

    const normQuote = normalize(q.quote);
    // Middle 60% of the normalized alphanumeric quote, capped at 60 chars.
    // Middle-anchored avoids edge-trimming false negatives. 60 chars of
    // contiguous alphanumerics is highly specific.
    const len = normQuote.length;
    const start = Math.max(0, Math.floor(len * 0.2));
    const end = Math.min(len, Math.floor(len * 0.8));
    const fp = normQuote.slice(start, end).slice(0, 60);

    const hit = fp.length >= 20 && haystack.includes(fp);
    verdicts.push({
      id: q.id,
      item_id: q.item_id,
      item_path: q.item_path,
      verdict: hit ? 'yes' : 'no',
    });
  }

  if (!args.dryRun) {
    const upd = db.prepare<unknown, [string, number]>(`UPDATE notable_quotes SET verified = ? WHERE id = ?`);
    db.transaction(() => {
      for (const v of verdicts) upd.run(v.verdict, v.id);
    })();
  }
  return verdicts;
}

function reportSummary(verdicts: Verdict[]): void {
  const byItem = new Map<number, { path: string; yes: number; no: number; nopdf: number }>();
  for (const v of verdicts) {
    if (!byItem.has(v.item_id)) byItem.set(v.item_id, { path: v.item_path, yes: 0, no: 0, nopdf: 0 });
    const s = byItem.get(v.item_id)!;
    if (v.verdict === 'yes') s.yes++;
    else if (v.verdict === 'no') s.no++;
    else s.nopdf++;
  }
  const totalYes = verdicts.filter((v) => v.verdict === 'yes').length;
  const totalNo = verdicts.filter((v) => v.verdict === 'no').length;
  const totalNoPdf = verdicts.filter((v) => v.verdict === 'no-pdf').length;
  console.log(`\n=== Summary ===`);
  console.log(`Total: ${verdicts.length}`);
  console.log(`  VERIFIED  : ${totalYes}`);
  console.log(`  NOT FOUND : ${totalNo}  (residual hallucinations)`);
  console.log(`  NO PDF    : ${totalNoPdf}`);
  console.log('');

  const allBad = [...byItem.entries()]
    .filter(([_, s]) => s.no > 0)
    .sort((a, b) => b[1].no - a[1].no);
  console.log(`=== Papers with NOT_FOUND quotes (worst first) ===`);
  for (const [id, s] of allBad.slice(0, 30)) {
    const total = s.yes + s.no + s.nopdf;
    console.log(`  ${s.no}/${total}  item ${id}  ${s.path}`);
  }
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const db = new Database(DB_PATH);
  try {
    ensureVerifiedColumn(db, args.dryRun);
    console.log(`[audit] dryRun=${args.dryRun} limit=${args.limit ?? 'all'} itemId=${args.itemId ?? 'all'}`);
    const verdicts = audit(db, args);
    if (args.report) reportSummary(verdicts);
    else {
      const counts = verdicts.reduce<Record<string, number>>((acc, v) => {
        acc[v.verdict] = (acc[v.verdict] ?? 0) + 1; return acc;
      }, {});
      console.log(`[audit] verdicts: ${JSON.stringify(counts)}`);
    }
  } finally {
    db.close();
  }
}

main();

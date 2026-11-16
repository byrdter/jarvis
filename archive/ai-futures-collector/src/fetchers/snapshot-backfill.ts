/**
 * Backfill snapshots for existing wiki items that have a URL but no entry in
 * originals/<category>/<slug>.{pdf,png}. Skips items whose original_path is
 * already populated.
 *
 * Flags:
 *   --category C    Restrict to a single category (repeatable).
 *   --limit N       Only process the first N candidates.
 *   --concurrency K Snapshot K URLs in parallel (default 3).
 *   --dry-run       List what would be snapshotted, don't run Playwright.
 *
 * After running, rebuild the graph to pick up the new originals:
 *   bun run src/fetchers/graph.ts build
 *
 * Usage:
 *   bun run src/fetchers/snapshot-backfill.ts --category news --limit 5
 *   bun run src/fetchers/snapshot-backfill.ts                 # all categories
 */

import { Database } from 'bun:sqlite';
import { snapshot, closeBrowser } from './snapshot';
import { existsSync } from 'fs';
import { join } from 'path';

const WIKI_ROOT = '/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis-private/ai-futures-wiki';
const DB_PATH = join(WIKI_ROOT, 'wiki-graph.db');

// Categories with public URLs worth snapshotting. Excludes academic (already
// has PDFs), reddit (no canonical article), and youtube (anti-bot).
const DEFAULT_CATEGORIES = ['news', 'newsletters', 'thinktanks'];

interface Args {
  categories: string[];
  limit: number | null;
  concurrency: number;
  dryRun: boolean;
}

function parseArgs(argv: string[]): Args {
  const a: Args = { categories: [], limit: null, concurrency: 3, dryRun: false };
  for (let i = 0; i < argv.length; i++) {
    const v = argv[i];
    if (v === '--category') a.categories.push(argv[++i]!);
    else if (v === '--limit') a.limit = parseInt(argv[++i] ?? '0', 10) || null;
    else if (v === '--concurrency') a.concurrency = parseInt(argv[++i] ?? '3', 10) || 3;
    else if (v === '--dry-run') a.dryRun = true;
  }
  if (a.categories.length === 0) a.categories = DEFAULT_CATEGORIES;
  return a;
}

interface Candidate {
  id: number;
  path: string;        // wiki/<category>/<slug>.md
  category: string;
  slug: string;
  url: string;
}

function candidates(db: Database, categories: string[], limit: number | null): Candidate[] {
  const placeholders = categories.map(() => '?').join(',');
  const rows = db
    .query<{ id: number; path: string; category: string; url: string; original_path: string | null }, string[]>(
      `SELECT id, path, category, url, original_path
         FROM items
        WHERE category IN (${placeholders})
          AND url IS NOT NULL AND url <> ''
        ORDER BY id`
    )
    .all(...categories);

  const out: Candidate[] = [];
  for (const r of rows) {
    if (r.original_path) continue;
    const slug = r.path.split('/').pop()!.replace(/\.md$/i, '');
    // If the file already exists on disk (created by a prior run or by the
    // fetcher) skip — the next graph build will pick it up.
    const pdfAbs = join(WIKI_ROOT, 'originals', r.category, slug + '.pdf');
    if (existsSync(pdfAbs)) continue;
    out.push({ id: r.id, path: r.path, category: r.category, slug, url: r.url });
    if (limit !== null && out.length >= limit) break;
  }
  return out;
}

async function run(args: Args): Promise<void> {
  const db = new Database(DB_PATH);
  const cands = candidates(db, args.categories, args.limit);
  db.close();

  console.log(`[backfill] categories=${args.categories.join(',')} found=${cands.length} concurrency=${args.concurrency} dryRun=${args.dryRun}`);
  if (args.dryRun) {
    for (const c of cands) console.log(`  ${c.category}/${c.slug}  <-  ${c.url}`);
    return;
  }
  if (cands.length === 0) {
    console.log('[backfill] nothing to do');
    return;
  }

  let ok = 0, fail = 0, done = 0;
  const queue = cands.slice();
  const total = queue.length;

  const workers = Array.from({ length: args.concurrency }, async () => {
    while (queue.length > 0) {
      const job = queue.shift();
      if (!job) break;
      done++;
      const tag = `[${done}/${total}] ${job.category}/${job.slug}`;
      try {
        const r = await snapshot({ url: job.url, category: job.category, slug: job.slug });
        ok++;
        console.log(`${tag}  ✓ (${r.skipped ? 'cached' : 'snapped'})`);
      } catch (e: any) {
        fail++;
        console.log(`${tag}  ✗ ${e.message?.slice(0, 80) ?? e}`);
      }
    }
  });

  await Promise.all(workers);
  await closeBrowser();
  console.log(`\n[backfill] done: ok=${ok} fail=${fail}`);
  console.log(`[backfill] next: bun run src/fetchers/graph.ts build  (to populate original_path in DB)`);
}

run(parseArgs(process.argv.slice(2)))
  .catch((e) => { console.error(e); process.exit(1); });

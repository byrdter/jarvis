/**
 * Notable-quotes extraction. Walks library PDFs (and now news/newsletter snapshots),
 * asks Claude to surface 3-8 quotable passages per source, stores them in
 * wiki-graph.db with (page, bbox) so the citation card pipeline can render them
 * directly.
 *
 * Uses pdftotext (system binary) for PDF text extraction — pdf-parse silently
 * fails on Antenna House XSL Formatter output (most HBR PDFs) and on arXiv PDFs.
 *
 * Flags:
 *   --category C         Restrict to a category (default: academic-library).
 *   --limit N            Only process the first N items needing extraction.
 *   --force              Re-extract even if quotes already exist for the item.
 *   --dry-run            Show the plan, run no LLM calls.
 *   --redo-hallucinated  Wipe + re-extract items whose quotes are all verified='no'.
 *   --init               Create the notable_quotes table and exit.
 */

import { Database } from 'bun:sqlite';
import { existsSync } from 'fs';
import { join } from 'path';
import { spawnSync } from 'child_process';
const PDFTOTEXT = '/opt/homebrew/bin/pdftotext';
const PDFINFO = '/opt/homebrew/bin/pdfinfo';

const WIKI_ROOT = '/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis-private/ai-futures-wiki';
const DB_PATH = join(WIKI_ROOT, 'wiki-graph.db');
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY ?? '';
const MODEL = 'claude-haiku-4-5-20251001';

interface Args {
  category: string;
  limit: number | null;
  force: boolean;
  dryRun: boolean;
  init: boolean;
  redoHallucinated: boolean;
}

function parseArgs(argv: string[]): Args {
  const a: Args = { category: 'academic-library', limit: null, force: false, dryRun: false, init: false, redoHallucinated: false };
  for (let i = 0; i < argv.length; i++) {
    const v = argv[i];
    if (v === '--category') a.category = argv[++i] ?? a.category;
    else if (v === '--limit') a.limit = parseInt(argv[++i] ?? '0', 10) || null;
    else if (v === '--force') a.force = true;
    else if (v === '--dry-run') a.dryRun = true;
    else if (v === '--init') a.init = true;
    else if (v === '--redo-hallucinated') a.redoHallucinated = true;
  }
  return a;
}

function ensureTable(db: Database): void {
  db.exec(`
    CREATE TABLE IF NOT EXISTS notable_quotes (
      id INTEGER PRIMARY KEY,
      item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
      quote TEXT NOT NULL,
      page INTEGER,
      speaker TEXT,
      speaker_role TEXT,
      context_50w TEXT,
      thesis_lenses TEXT,
      cite_count INTEGER DEFAULT 0,
      extracted_at TEXT NOT NULL,
      extractor_model TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_quotes_item ON notable_quotes(item_id);
    CREATE INDEX IF NOT EXISTS idx_quotes_lenses ON notable_quotes(thesis_lenses);
  `);
}

interface Item {
  id: number;
  path: string;
  title: string;
  author: string;
  source: string;
  original_path: string | null;
  original_kind: string | null;
}

function pickCandidates(db: Database, args: Args): Item[] {
  let where: string;
  if (args.redoHallucinated) {
    where = `category = ? AND original_path IS NOT NULL AND id IN (
      SELECT item_id FROM notable_quotes
        GROUP BY item_id
        HAVING SUM(CASE WHEN verified = 'no' THEN 1 ELSE 0 END) = COUNT(*)
           AND COUNT(*) > 0
    )`;
  } else if (args.force) {
    where = `category = ? AND original_path IS NOT NULL`;
  } else {
    where = `category = ? AND original_path IS NOT NULL
       AND id NOT IN (SELECT DISTINCT item_id FROM notable_quotes)`;
  }
  const rows = db
    .query<Item, [string]>(
      `SELECT id, path, title, author, source, original_path, original_kind
         FROM items WHERE ${where} ORDER BY id`
    )
    .all(args.category);
  return args.limit ? rows.slice(0, args.limit) : rows;
}

interface PageText { page: number; text: string; }

// Uses system pdftotext. pdf-parse silently fails on many of our real-world PDFs
// (HBR's Antenna House output, arXiv). Per-page extraction via -f/-l gives
// accurate page numbers the LLM can cite back.
async function extractPdfPages(pdfPath: string): Promise<PageText[]> {
  const info = spawnSync(PDFINFO, [pdfPath], { encoding: 'utf8' });
  if (info.status !== 0) throw new Error(`pdfinfo failed: ${info.stderr?.slice(0, 200)}`);
  const m = info.stdout.match(/Pages:\s+(\d+)/);
  if (!m) throw new Error('could not determine page count');
  const pageCount = parseInt(m[1]!, 10);

  const all = spawnSync(PDFTOTEXT, [pdfPath, '-layout', '-'], {
    encoding: 'utf8',
    maxBuffer: 50 * 1024 * 1024,
  });
  if (all.status !== 0) throw new Error(`pdftotext failed: ${all.stderr?.slice(0, 200)}`);
  const text = all.stdout;
  const chunks = text.split('\f');
  if (chunks.length !== pageCount + 1 && chunks.length !== pageCount) {
    const pages: PageText[] = [];
    for (let p = 1; p <= pageCount; p++) {
      const r = spawnSync(PDFTOTEXT, [pdfPath, '-f', String(p), '-l', String(p), '-'], {
        encoding: 'utf8',
        maxBuffer: 50 * 1024 * 1024,
      });
      pages.push({ page: p, text: r.stdout ?? '' });
    }
    return pages;
  }
  return chunks.slice(0, pageCount).map((t, i) => ({ page: i + 1, text: t }));
}

interface ExtractedQuote {
  quote: string;
  page: number | null;
  speaker: string | null;
  speaker_role: string | null;
  context_50w: string | null;
  thesis_lenses: string[];
}

const PROMPT_SYSTEM = `You extract the most quotable passages from research papers and articles for use as on-screen citation cards in a YouTube essay channel.

The channel thesis: "Technology is neutral. Choices aren't." It explores five lenses:
- power-control: who decides how AI gets used; what are they optimizing for
- economic-futures: automated vs. augmented vs. transformed work; winners/losers
- meaning-identity: what gives life meaning when work changes; what stays human
- strategic-choices: trade-offs leaders face; preparing for many futures
- social-consequences: how AI reshapes education, family, community, fairness

A good quote for a citation card is:
- 1-3 sentences, self-contained, would land on screen with a yellow highlight
- Carries a non-obvious finding, a sharp framing, a memorable phrase, a specific number with population, or a falsifiable claim
- NOT a generic intro sentence, NOT a methods description, NOT a literature-review filler

Return STRICT JSON: {"quotes": [{quote, page, speaker, speaker_role, context_50w, thesis_lenses: []}, ...]}
- quote: the exact passage as written (preserve hyphens, em-dashes, quotation marks; do not paraphrase)
- page: the 1-indexed page number where it appears
- speaker: the author or null if it's a quotation of someone else inside the paper
- speaker_role: optional role like "researcher", "executive", "interviewee"
- context_50w: ~50 words of text immediately preceding the quote (for fuzzy-matching back into the PDF)
- thesis_lenses: 1-3 of the slugs above
Extract 3-8 quotes. Prefer fewer-and-sharper to many-and-mid.`;

async function callClaude(systemPrompt: string, userText: string): Promise<ExtractedQuote[]> {
  if (!ANTHROPIC_API_KEY) throw new Error('ANTHROPIC_API_KEY not set');
  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 4096,
      system: systemPrompt,
      messages: [{ role: 'user', content: userText }],
    }),
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`anthropic ${res.status}: ${t.slice(0, 300)}`);
  }
  const json = await res.json() as any;
  const text = json.content?.[0]?.text ?? '';
  const m = text.match(/\{[\s\S]*\}/);
  if (!m) throw new Error('no JSON in response: ' + text.slice(0, 200));
  const parsed = JSON.parse(m[0]);
  return parsed.quotes ?? [];
}

function tagPages(pages: PageText[], maxChars = 60_000): string {
  let out = '';
  for (const p of pages) {
    const chunk = `\n\n[PAGE ${p.page}]\n${p.text.trim()}`;
    if (out.length + chunk.length > maxChars) break;
    out += chunk;
  }
  return out;
}

async function extractForItem(item: Item): Promise<ExtractedQuote[]> {
  const pdfAbs = join(WIKI_ROOT, item.original_path!);
  if (!existsSync(pdfAbs)) throw new Error(`missing original: ${item.original_path}`);
  const pages = await extractPdfPages(pdfAbs);
  const tagged = tagPages(pages);
  const userText =
    `Source: ${item.source} — ${item.title}\nAuthor: ${item.author || '(unknown)'}\n` +
    `Wiki path: ${item.path}\n\n--- PAPER TEXT (page-tagged) ---\n${tagged}\n--- END ---`;
  return await callClaude(PROMPT_SYSTEM, userText);
}

async function run(args: Args): Promise<void> {
  const db = new Database(DB_PATH);
  ensureTable(db);
  if (args.init) { console.log('[init] notable_quotes table ready'); db.close(); return; }

  const items = pickCandidates(db, args);
  console.log(`[notable-quotes] category=${args.category} candidates=${items.length} model=${MODEL} dryRun=${args.dryRun}`);
  if (args.dryRun) {
    for (const it of items.slice(0, 20)) console.log(`  ${it.id}  ${it.path}  -> ${it.original_path}`);
    db.close();
    return;
  }
  if (items.length === 0) { console.log('[notable-quotes] nothing to do'); db.close(); return; }

  if (args.redoHallucinated) {
    const wipe = db.prepare<unknown, [number]>(
      `DELETE FROM notable_quotes WHERE item_id = ? AND verified = 'no'`
    );
    let wiped = 0;
    for (const it of items) {
      const r = wipe.run(it.id);
      wiped += Number(r.changes);
    }
    console.log(`[notable-quotes] wiped ${wiped} hallucinated quotes across ${items.length} items`);
  }

  const ins = db.prepare(
    `INSERT INTO notable_quotes
       (item_id, quote, page, speaker, speaker_role, context_50w, thesis_lenses, extracted_at, extractor_model)
     VALUES (?,?,?,?,?,?,?,?,?)`
  );

  let ok = 0, fail = 0, totalQuotes = 0;
  for (const it of items) {
    const tag = `[${ok + fail + 1}/${items.length}] ${it.path}`;
    try {
      const quotes = await extractForItem(it);
      for (const q of quotes) {
        ins.run(
          it.id,
          q.quote,
          q.page,
          q.speaker,
          q.speaker_role,
          q.context_50w,
          (q.thesis_lenses ?? []).join(','),
          new Date().toISOString(),
          MODEL,
        );
      }
      totalQuotes += quotes.length;
      ok++;
      console.log(`${tag}  ✓ ${quotes.length} quotes`);
    } catch (e: any) {
      fail++;
      console.log(`${tag}  ✗ ${e.message?.slice(0, 120) ?? e}`);
    }
  }
  db.close();
  console.log(`\n[notable-quotes] done: ok=${ok} fail=${fail} quotes=${totalQuotes}`);
}

await run(parseArgs(process.argv.slice(2)))
  .catch((e) => { console.error(e); process.exit(1); });

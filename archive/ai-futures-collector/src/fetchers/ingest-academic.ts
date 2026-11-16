/**
 * Academic library ingester.
 *
 * Turns the full-text papers you've already collected (PDF/MD/HTML) into
 * searchable wiki pages + embeddings. Watches the library folders; new drops
 * are auto-ingested on the next run. This is the landing zone for papers you
 * retrieve via institutional access after a digest alert.
 *
 * Library folders (under ai-futures-wiki/):
 *   EffectAI24-26/  EffectOnWork/   (+ any folder passed as an arg)
 *
 * Output: wiki/academic-library/<slug>.md  (FTS-indexed + embedded by reindex)
 *
 * Usage:
 *   bun run src/fetchers/ingest-academic.ts
 *   bun run src/fetchers/ingest-academic.ts SomeOtherFolder
 */

import { PDFParse } from 'pdf-parse';
import TurndownService from 'turndown';
import { readdirSync, statSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const WIKI_ROOT = '/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis-private/ai-futures-wiki';
const OUT_DIR = join(WIKI_ROOT, 'wiki', 'academic-library');
const STATE_PATH = join(import.meta.dir, '.academic-ingest-state.json');
const DEFAULT_LIBS = ['EffectAI24-26', 'EffectOnWork'];
const MAX_BODY = 80_000; // chars; full papers are fine for FTS

const td = new TurndownService({ headingStyle: 'atx' });

// filename token -> canonical journal/source
const JOURNALS: [RegExp, string][] = [
  [/HBR/i, 'Harvard Business Review'], [/SMR/i, 'MIT Sloan Management Review'],
  [/MISQE/i, 'MISQ Executive'], [/MISQ/i, 'MIS Quarterly'],
  [/\bISR\b/i, 'Information Systems Research'], [/JMIS/i, 'Journal of MIS'],
  [/\bMS\d|MnSc|ManagementScience/i, 'Management Science'], [/NBER/i, 'NBER'],
  [/arXiv/i, 'arXiv'], [/Microsoft/i, 'Microsoft Research'], [/Fortune/i, 'Fortune'],
  [/Time\d/i, 'Time'], [/\bWS\b|WSJ/i, 'Wall Street Journal'], [/Nature/i, 'Nature'],
];
const LENS_KW: Record<string, string[]> = {
  'power-control': ['power', 'control', 'govern', 'regulat', 'monopol', 'concentrat'],
  'economic-futures': ['job', 'labor', 'labour', 'work', 'automat', 'augment', 'productiv', 'wage', 'employ', 'economic', 'firm'],
  'meaning-identity': ['meaning', 'identity', 'creativ', 'human', 'expert', 'skill', 'learning', 'agency'],
  'strategic-choices': ['strateg', 'decision', 'adopt', 'manage', 'organiz', 'enterprise', 'leader'],
  'social-consequences': ['society', 'social', 'inequalit', 'ethic', 'bias', 'patient', 'customer', 'service'],
};

interface State { seen: Record<string, { size: number; ingested: string }>; }
const loadState = (): State => { try { return JSON.parse(readFileSync(STATE_PATH, 'utf-8')); } catch { return { seen: {} }; } };
const saveState = (s: State) => writeFileSync(STATE_PATH, JSON.stringify(s, null, 2));

const slug = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 80) || 'paper';
const humanize = (f: string) => f.replace(/\.[^.]+$/, '').replace(/([a-z])([A-Z])/g, '$1 $2').replace(/([A-Z]+)([A-Z][a-z])/g, '$1 $2').replace(/\d{4}$/, '').trim();
const DOI_RE = /\b10\.\d{4,9}\/[-._;()/:A-Za-z0-9]+/;

function journalOf(name: string): string { for (const [re, j] of JOURNALS) if (re.test(name)) return j; return 'Academic (uncategorized)'; }
function yearOf(name: string): string { const m = name.match(/(20\d\d)/); return m ? m[1]! : ''; }
function assignLenses(text: string): string[] {
  const low = text.slice(0, 8000).toLowerCase();
  const hits = Object.entries(LENS_KW).filter(([, kws]) => kws.some((k) => low.includes(k))).map(([l]) => l);
  return hits.length ? hits : ['economic-futures'];
}

async function extractText(abs: string): Promise<string> {
  if (abs.endsWith('.pdf')) {
    const buf = await Bun.file(abs).arrayBuffer();
    const r = await new PDFParse({ data: new Uint8Array(buf) }).getText();
    return r.text || '';
  }
  if (abs.endsWith('.md')) return readFileSync(abs, 'utf-8');
  if (abs.endsWith('.html') || abs.endsWith('.htm')) { try { return td.turndown(readFileSync(abs, 'utf-8')); } catch { return readFileSync(abs, 'utf-8').replace(/<[^>]+>/g, ' '); } }
  return '';
}

function walk(dir: string): string[] {
  const out: string[] = [];
  const rec = (d: string) => {
    let entries: string[] = [];
    try { entries = readdirSync(d); } catch { return; }
    for (const e of entries) {
      if (e.startsWith('.')) continue;
      const p = join(d, e);
      const s = statSync(p);
      if (s.isDirectory()) rec(p);
      else if (/\.(pdf|md|html?|)$/i.test(e) && /\.(pdf|md|html?)$/i.test(e)) out.push(p);
    }
  };
  rec(dir);
  return out;
}

export async function ingestAcademicLibrary(libs: string[] = []): Promise<{ ingested: number; skipped: number; failed: number }> {
  const dirs = (libs.length ? libs : DEFAULT_LIBS).map((d) => (d.startsWith('/') ? d : join(WIKI_ROOT, d)));
  mkdirSync(OUT_DIR, { recursive: true });
  const state = loadState();

  let ingested = 0, skipped = 0, failed = 0;
  for (const dir of dirs) {
    const files = walk(dir);
    console.log(`📂 ${dir.split('/').pop()}: ${files.length} candidate files`);
    for (const abs of files) {
      const rel = abs.replace(WIKI_ROOT + '/', '');
      const size = statSync(abs).size;
      if (state.seen[rel] && state.seen[rel].size === size) { skipped++; continue; }
      const name = abs.split('/').pop()!;
      try {
        const text = (await extractText(abs)).trim();
        if (text.length < 200) { console.log(`  ⚠️  ${name}: too little text (${text.length} chars)`); failed++; continue; }
        const journal = journalOf(name), year = yearOf(name);
        const title = humanize(name);
        const doi = text.slice(0, 4000).match(DOI_RE)?.[0]?.replace(/[.,)]+$/, '');
        const lenses = assignLenses(text);
        const body = text.length > MAX_BODY ? text.slice(0, MAX_BODY) + '\n\n…[truncated]' : text;
        const fm = [
          '---', `title: ${JSON.stringify(title)}`, `source: ${journal}`,
          `source_type: academic-fulltext`, `tier: "1.5"`, `access: have-fulltext`,
          year ? `year: ${year}` : 'year: ', doi ? `doi: ${doi}` : 'doi: ',
          `origin_file: ${rel}`, `indexed: ${new Date().toISOString()}`,
          `thesis_lens: [${lenses.join(', ')}]`, `tags: [academic-library, ${slug(journal)}]`, '---', '',
          `# ${title}`, '', `**Journal/Source:** ${journal}${year ? ` (${year})` : ''}`,
          doi ? `**DOI:** [${doi}](https://doi.org/${doi})` : '', `**Origin file:** \`${rel}\``,
          `**Lenses:** ${lenses.join(', ')}`, '', '## Full text', '', body, '',
        ].filter((l) => l !== '').join('\n');
        writeFileSync(join(OUT_DIR, `${slug(humanize(name)) || slug(name)}.md`), fm);
        state.seen[rel] = { size, ingested: new Date().toISOString() };
        ingested++;
        console.log(`  ✓ ${name} → ${journal}${year ? ` ${year}` : ''} [${lenses.join(',')}]`);
      } catch (e: any) { console.log(`  ✗ ${name}: ${String(e.message).slice(0, 80)}`); failed++; }
    }
  }
  saveState(state);
  console.log(`\n✅ Academic ingest: ${ingested} new, ${skipped} unchanged, ${failed} failed → ${OUT_DIR}`);
  return { ingested, skipped, failed };
}

if (import.meta.main) {
  const libs = process.argv.slice(2).filter((a) => !a.startsWith('-'));
  ingestAcademicLibrary(libs).catch((e) => { console.error(e); process.exit(1); });
}

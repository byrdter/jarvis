/**
 * Multi-cadence sweep engine for the Byrddynasty knowledge pipeline.
 *
 * Reads the unified registry (sources.ts) and pulls new items for every
 * RSS-reachable source on the requested cadence. Dedupes by URL/DOI, writes
 * wiki pages with rich frontmatter (tier, lens, access, doi, needs_fulltext),
 * and returns the new items so the digest builder can email/Telegram them.
 *
 * Academic + paywalled sources: capture title + authors + abstract + DOI only,
 * and flag needs_fulltext=true so YOU retrieve the PDF via institutional access.
 * Never scrapes behind a paywall.
 *
 * HTML-diff / alert / api sources are not yet swept here (tracked as follow-ups);
 * `runSweep` reports how many were skipped so nothing is silently dropped.
 *
 * Usage:
 *   bun run src/fetchers/sweep.ts daily      # daily-cadence RSS sources
 *   bun run src/fetchers/sweep.ts weekly
 *   bun run src/fetchers/sweep.ts all        # every RSS source regardless of cadence
 */

import { XMLParser } from 'fast-xml-parser';
import TurndownService from 'turndown';
import { mkdirSync, readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import { SOURCES, fineLenses, type Source, type Cadence } from './sources';

const WIKI_ROOT = '/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis-private/ai-futures-wiki';
const STATE_PATH = join(import.meta.dir, '.sweep-state.json');
const MAX_PER_SOURCE = 10;
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15';

const xml = new XMLParser({ ignoreAttributes: false, attributeNamePrefix: '@_', textNodeName: '#text' });
const td = new TurndownService({ headingStyle: 'atx' });

export interface NewItem {
  sourceId: string; sourceName: string; tier: string; category: string;
  title: string; author: string; url: string; published: string;
  lenses: string[]; access: string; doi?: string; abstract?: string;
  needs_fulltext: boolean;
}

interface State { seen: Record<string, string>; lastRun: Record<string, string>; }
const loadState = (): State => { try { return JSON.parse(readFileSync(STATE_PATH, 'utf-8')); } catch { return { seen: {}, lastRun: {} }; } };
const saveState = (s: State) => writeFileSync(STATE_PATH, JSON.stringify(s, null, 2));

// ── helpers ──
const asArray = <T>(x: T | T[] | undefined): T[] => (x == null ? [] : Array.isArray(x) ? x : [x]);
const txt = (n: any): string => (n == null ? '' : typeof n === 'string' ? n : typeof n === 'object' && '#text' in n ? String(n['#text']) : String(n));
const slug = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 70) || 'untitled';
const htmlToMd = (h: string) => { if (!h) return ''; try { return td.turndown(h); } catch { return h.replace(/<[^>]+>/g, ' ').trim(); } };
const DOI_RE = /\b10\.\d{4,9}\/[-._;()/:A-Za-z0-9]+/;

// Per-article lens classification (keyword-based, $0). Replaces the old source-level
// fineLenses(), which tagged every item from a source identically (e.g. every arXiv
// paper → "Economy · Society"). Now each item's lenses come from its own title/abstract.
const LENS_KEYWORDS: Record<string, RegExp> = {
  'power-control':      /\b(regulat|policy|governance|antitrust|monopol|lawsuit|legal|\blaw\b|compliance|oversight|\bban\b|censor|surveillance|military|weapon|national security|\bcontrol\b|safety|alignment|guardrail|\bEU\b|regulator|sanction|export control|copyright|licens|geopolit)/i,
  'economic-futures':  /\b(econom|\bjobs?\b|labor|labour|employ|wage|salary|\bmarket|\bGDP\b|revenue|profit|invest|funding|\bIPO\b|valuation|startup|productivity|\bcost|\bprice|\btrade\b|layoff|hiring|business model|billion|venture|capital|monetiz)/i,
  'meaning-identity':  /\b(identity|meaning|\bhuman\b|creativ|\bart\b|artist|culture|conscious|emotion|relationship|purpose|authentic|personhood|dignity|companion|loneli|belief)/i,
  'strategic-choices': /\b(strateg|decision|enterprise|adoption|deploy|competit|roadmap|corporate|leadership|management|transformation|\bagent|agentic|workflow|automat|orchestrat|\bscal(e|ing)\b|infrastructure|data cent|\bcompute\b)/i,
  'social-consequences':/\b(societ|\bsocial\b|misinformation|disinformation|\bbias\b|fairness|inequalit|education|student|\bhealth|medical|clinical|patient|communit|\bpublic\b|democra|discriminat|children|mental health|addict|wellbeing|\bharm)/i,
};
function classifyLenses(title: string, abstract: string, src: Source): string[] {
  const text = `${title}\n${abstract}`;
  const hits = Object.entries(LENS_KEYWORDS).filter(([, re]) => re.test(text)).map(([lens]) => lens);
  // fall back to the source's configured lenses if nothing matched, so every item has ≥1
  return hits.length ? hits : fineLenses(src);
}

async function getText(url: string): Promise<string> {
  const res = await fetch(url, { headers: { 'User-Agent': UA, Accept: 'application/xml,text/html,*/*' }, signal: AbortSignal.timeout(25000) });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.text();
}

function extractDoi(it: any, link: string, body: string): string | undefined {
  const cand = txt(it['prism:doi']) || txt(it['dc:identifier']) || '';
  const m = cand.match(DOI_RE) || link.match(DOI_RE) || body.match(DOI_RE) || txt(it.guid).match(DOI_RE);
  return m ? m[0].replace(/[.,)]+$/, '') : undefined;
}

function normalizeFeed(doc: any): { items: any[]; isAtom: boolean } {
  const rss = asArray(doc?.rss?.channel?.item);
  const atom = asArray(doc?.feed?.entry);
  const rdf = asArray(doc?.['rdf:RDF']?.item); // RSS 1.0 (some academic feeds)
  if (rss.length) return { items: rss, isAtom: false };
  if (atom.length) return { items: atom, isAtom: true };
  if (rdf.length) return { items: rdf, isAtom: false };
  return { items: [], isAtom: false };
}

function writeItem(it: NewItem) {
  const dir = join(WIKI_ROOT, 'wiki', it.category);
  mkdirSync(dir, { recursive: true });
  const file = join(dir, `${slug(it.sourceName)}--${slug(it.title)}.md`);
  const fm = [
    '---',
    `title: ${JSON.stringify(it.title)}`,
    `author: ${it.author || it.sourceName}`,
    `url: ${it.url}`,
    `source: ${it.sourceName}`,
    `source_type: tier-${it.tier}`,
    `tier: "${it.tier}"`,
    `access: ${it.access}`,
    it.doi ? `doi: ${it.doi}` : `doi: `,
    `needs_fulltext: ${it.needs_fulltext}`,
    `published: ${it.published || 'unknown'}`,
    `indexed: ${new Date().toISOString()}`,
    `thesis_lens: [${it.lenses.join(', ')}]`,
    `tags: [${it.sourceId}]`,
    '---',
    '',
    `# ${it.title}`,
    '',
    `**Source:** ${it.sourceName} (Tier ${it.tier}) · ${it.author || ''}`,
    `**Published:** ${it.published || 'unknown'} · [original](${it.url})`,
    it.doi ? `**DOI:** [${it.doi}](https://doi.org/${it.doi})` : '',
    it.needs_fulltext ? `**⚠️ Full text behind paywall — retrieve via institutional access.**` : '',
    `**Lenses:** ${it.lenses.join(', ')}`,
    '',
    it.abstract ? `## Abstract\n\n${it.abstract}` : '_(no abstract/summary in feed — see original)_',
    '',
  ].filter((l) => l !== '').join('\n');
  writeFileSync(file, fm);
}

async function sweepSource(src: Source, state: State): Promise<NewItem[]> {
  if (src.sweep !== 'rss' || !src.feed) return []; // html/alert/api handled elsewhere
  let raw: string;
  try { raw = await getText(src.feed); } catch (e: any) { console.log(`  ⚠️  ${src.name}: ${e.message}`); return []; }
  let doc: any; try { doc = xml.parse(raw); } catch { console.log(`  ⚠️  ${src.name}: parse error`); return []; }
  const { items, isAtom } = normalizeFeed(doc);
  if (!items.length) { console.log(`  ·  ${src.name}: feed empty/HTML — html-diff follow-up`); return []; }

  const out: NewItem[] = [];
  for (const it of items) {
    if (out.length >= MAX_PER_SOURCE) break;
    const title = txt(it.title).trim();
    let link = '';
    if (isAtom) {
      const links = asArray(it.link);
      link = (links.find((l: any) => l['@_rel'] === 'alternate') || links[0])?.['@_href'] || '';
    } else {
      link = txt(it.link).trim() || txt(it.guid) || it.guid?.['#text'] || '';
    }
    if (!title || !link) continue;
    const rawBody = txt(it['content:encoded']) || txt(it.summary) || txt(it.description) || txt(it['dc:description']) || '';
    const doi = src.academic ? extractDoi(it, link, rawBody) : undefined;
    const key = doi ? `doi:${doi}` : link;
    if (state.seen[key]) continue;

    const abstract = htmlToMd(rawBody).slice(0, 4000);
    const author = txt(it['dc:creator']) || txt(it.author?.name) || txt(it.author) || src.name;
    const item: NewItem = {
      sourceId: src.id, sourceName: src.name, tier: src.tier, category: src.category,
      title, author, url: link, published: txt(it.pubDate) || txt(it.published) || txt(it['dc:date']) || '',
      lenses: classifyLenses(title, abstract, src), access: src.access, doi, abstract,
      needs_fulltext: src.academic === true && src.access !== 'open',
    };
    out.push(item);
    state.seen[key] = new Date().toISOString();
    // Wiki markdown write is best-effort: Dropbox online-only eviction throws EDEADLK here.
    // The item is already in the digest + marked seen, so a failed write must NOT crash delivery.
    try { writeItem(item); } catch (e: any) { console.log(`  ⚠️  ${src.name}: wiki write skipped (${e?.code || e?.message}) — item still in digest`); }
  }
  console.log(`  ✓ ${src.name}: ${out.length} new${out.some(i => i.needs_fulltext) ? ' (paywalled — abstract+DOI captured)' : ''}`);
  return out;
}

export async function runSweep(cadence: Cadence | 'all'): Promise<NewItem[]> {
  const state = loadState();
  const selected = SOURCES.filter((s) => (cadence === 'all' ? true : s.cadence === cadence));
  const rss = selected.filter((s) => s.sweep === 'rss' && s.feed);
  const skipped = selected.filter((s) => s.sweep !== 'rss' || !s.feed);
  console.log(`🛰️  Sweep [${cadence}] — ${rss.length} RSS sources, ${skipped.length} non-RSS (html/alert/api) deferred`);

  const all: NewItem[] = [];
  for (const src of rss) all.push(...(await sweepSource(src, state)));

  state.lastRun[cadence] = new Date().toISOString();
  saveState(state);
  const paywalled = all.filter((i) => i.needs_fulltext).length;
  console.log(`\n✅ Sweep done: ${all.length} new items (${paywalled} paywalled academic flagged for full-text retrieval).`);
  if (skipped.length) console.log(`   ℹ️  ${skipped.length} non-RSS sources need html-diff/alert adapters (see bd backlog).`);
  return all;
}

if (import.meta.main) {
  const arg = (process.argv[2] as Cadence | 'all') || 'daily';
  runSweep(arg).catch((e) => { console.error(e); process.exit(1); });
}

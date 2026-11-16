/**
 * AI-Futures Wiki Fetchers (Byrddynasty "Understanding AI")
 *
 * Unified fetcher with 5 source adapters (top-5 FREE ranked sources from
 * source-registry.md). Each run pulls items since last run, dedupes by URL,
 * writes markdown with standard frontmatter into the ai-futures wiki, and
 * (for YouTube) mirrors transcripts/metadata into raw/transcripts/.
 *
 * Thesis: "Technology is neutral. Choices aren't."
 * Every item is tagged with one or more of 5 lenses (see source-registry.md).
 *
 * Usage:
 *   bun run src/fetchers/ai-futures.ts            # all classes
 *   bun run src/fetchers/ai-futures.ts news       # one class
 *   bun run src/fetchers/ai-futures.ts news reddit # several
 *
 * Cost: $0 (RSS / public JSON / channel RSS only).
 */

import { XMLParser } from 'fast-xml-parser';
import TurndownService from 'turndown';
import { mkdirSync, readFileSync, writeFileSync, existsSync } from 'fs';
import { snapshot, closeBrowser } from './snapshot';
import { join, dirname } from 'path';

const WIKI_ROOT =
  '/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis-private/ai-futures-wiki';
const STATE_PATH = join(import.meta.dir, '.ai-futures-state.json');

const xml = new XMLParser({
  ignoreAttributes: false,
  attributeNamePrefix: '@_',
  textNodeName: '#text',
});
const td = new TurndownService({ headingStyle: 'atx', codeBlockStyle: 'fenced' });

// ---------------------------------------------------------------------------
// Lens taxonomy (thesis_lens frontmatter)
// ---------------------------------------------------------------------------
type Lens =
  | 'power-control'
  | 'economic-futures'
  | 'meaning-identity'
  | 'strategic-choices'
  | 'social-consequences';

const LENS_KEYWORDS: Record<Lens, string[]> = {
  'power-control': ['power', 'control', 'monopoly', 'regulat', 'govern', 'antitrust', 'concentrat', 'who decides', 'lobby', 'policy', 'censor', 'surveillance'],
  'economic-futures': ['job', 'labor', 'labour', 'work', 'automat', 'augment', 'productivity', 'wage', 'economy', 'gdp', 'unemploy', 'inequality', 'wealth', 'market'],
  'meaning-identity': ['meaning', 'identity', 'purpose', 'human', 'creativity', 'consciousness', 'agency', 'dignity', 'craft', 'authentic'],
  'strategic-choices': ['strategy', 'strategic', 'decision', 'trade-off', 'tradeoff', 'scenario', 'invest', 'adopt', 'roadmap', 'leadership', 'enterprise', 'build vs buy', 'competit'],
  'social-consequences': ['society', 'social', 'education', 'school', 'community', 'family', 'inequality', 'fairness', 'bias', 'democracy', 'misinformation', 'children', 'public'],
};

function assignLenses(text: string, defaults: Lens[]): Lens[] {
  const lower = text.toLowerCase();
  const hits = new Set<Lens>(defaults);
  for (const [lens, kws] of Object.entries(LENS_KEYWORDS) as [Lens, string[]][]) {
    if (kws.some((k) => lower.includes(k))) hits.add(lens);
  }
  return [...hits];
}

// ---------------------------------------------------------------------------
// Source config — top 5 FREE ranked classes
// ---------------------------------------------------------------------------
interface RssSource { name: string; slug: string; url: string; author?: string; defaults: Lens[]; }

const NEWSLETTERS: RssSource[] = [
  { name: 'One Useful Thing', slug: 'one-useful-thing', url: 'https://www.oneusefulthing.org/feed', author: 'Ethan Mollick', defaults: ['strategic-choices', 'economic-futures'] },
  { name: 'Import AI', slug: 'import-ai', url: 'https://importai.substack.com/feed', author: 'Jack Clark', defaults: ['power-control', 'social-consequences'] },
  { name: 'AI Snake Oil', slug: 'ai-snake-oil', url: 'https://www.aisnakeoil.com/feed', author: 'Narayanan & Kapoor', defaults: ['social-consequences', 'power-control'] },
  { name: 'Exponential View', slug: 'exponential-view', url: 'https://www.exponentialview.co/feed', author: 'Azeem Azhar', defaults: ['economic-futures', 'power-control'] },
];

const NEWS: RssSource[] = [
  { name: 'MIT Technology Review', slug: 'mit-tech-review', url: 'https://www.technologyreview.com/feed/', defaults: ['power-control', 'social-consequences'] },
  { name: 'The Verge', slug: 'the-verge', url: 'https://www.theverge.com/rss/index.xml', defaults: ['power-control'] },
  { name: 'Ars Technica', slug: 'ars-technica', url: 'https://feeds.arstechnica.com/arstechnica/index', defaults: ['strategic-choices'] },
  { name: 'Platformer', slug: 'platformer', url: 'https://www.platformer.news/rss/', author: 'Casey Newton', defaults: ['power-control', 'social-consequences'] },
];

const THINKTANKS: RssSource[] = [
  { name: 'RAND — Artificial Intelligence', slug: 'rand', url: 'https://www.rand.org/topics/artificial-intelligence.xml', defaults: ['power-control', 'social-consequences'] },
  { name: 'AI Now Institute', slug: 'ai-now', url: 'https://ainowinstitute.org/feed', defaults: ['power-control', 'social-consequences'] },
  { name: 'Montreal AI Ethics Institute', slug: 'montreal-ai-ethics', url: 'https://montrealethics.ai/feed/', defaults: ['social-consequences', 'power-control'] },
];

const REDDIT_SUBS = [
  { sub: 'Futurology', defaults: ['social-consequences', 'economic-futures'] as Lens[] },
  { sub: 'artificial', defaults: ['social-consequences', 'power-control'] as Lens[] },
  { sub: 'singularity', defaults: ['meaning-identity', 'social-consequences'] as Lens[] },
];

const YOUTUBE_CHANNELS = [
  { handle: 'a16z', slug: 'a16z', defaults: ['power-control', 'economic-futures'] as Lens[] },
  { handle: 'lexfridman', slug: 'lex-fridman', defaults: ['meaning-identity', 'power-control'] as Lens[] },
  { handle: 'DwarkeshPatel', slug: 'dwarkesh', defaults: ['strategic-choices', 'economic-futures'] as Lens[] },
];

// Only the most-recent N items per source are written on a seed run.
const MAX_PER_SOURCE = 8;
const BROOKINGS_AI_ONLY = true; // Brookings is general; keep AI-relevant items only.

// ---------------------------------------------------------------------------
// State (dedupe by url)
// ---------------------------------------------------------------------------
interface State { seen: Record<string, string>; lastRun: Record<string, string>; }
function loadState(): State {
  try { return JSON.parse(readFileSync(STATE_PATH, 'utf-8')); }
  catch { return { seen: {}, lastRun: {} }; }
}
function saveState(s: State) { writeFileSync(STATE_PATH, JSON.stringify(s, null, 2)); }

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function slugify(s: string): string {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 70) || 'untitled';
}
function asArray<T>(x: T | T[] | undefined): T[] {
  if (x === undefined || x === null) return [];
  return Array.isArray(x) ? x : [x];
}
function txt(node: any): string {
  if (node == null) return '';
  if (typeof node === 'string') return node;
  if (typeof node === 'object' && '#text' in node) return String(node['#text']);
  return String(node);
}
function htmlToMd(html: string): string {
  if (!html) return '';
  try { return td.turndown(html); } catch { return html.replace(/<[^>]+>/g, ' ').trim(); }
}
// Browser-like UA — many publisher/think-tank feeds 403 a custom bot UA.
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36';
async function getText(url: string): Promise<string> {
  const res = await fetch(url, { headers: { 'User-Agent': UA, Accept: 'text/html,application/xml,application/json,*/*' } });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return res.text();
}

interface WriteOpts {
  category: string; title: string; author?: string; url: string;
  sourceType: string; published: string; lenses: Lens[]; tags?: string[];
  body: string; sourceName: string;
}
// Snapshot queue: collected during writes, drained at end of main(). Each
// entry produces originals/<category>/<slug>.{pdf,png} via Playwright.
// Categories with no public URL (e.g. raw-only content) are filtered out.
const SNAPSHOT_QUEUE: Array<{ url: string; category: string; slug: string }> = [];

function writeItem(o: WriteOpts): string {
  const dir = join(WIKI_ROOT, 'wiki', o.category);
  mkdirSync(dir, { recursive: true });
  const slugBase = `${slugify(o.sourceName)}--${slugify(o.title)}`;
  const file = join(dir, `${slugBase}.md`);
  const fm = [
    '---',
    `title: ${JSON.stringify(o.title)}`,
    `author: ${o.author || o.sourceName}`,
    `url: ${o.url}`,
    `source: ${o.sourceName}`,
    `source_type: ${o.sourceType}`,
    `published: ${o.published || 'unknown'}`,
    `indexed: ${new Date().toISOString()}`,
    `thesis_lens: [${o.lenses.join(', ')}]`,
    `tags: [${(o.tags || []).join(', ')}]`,
    '---',
    '',
    `# ${o.title}`,
    '',
    `**Source:** ${o.sourceName}${o.author ? ` · ${o.author}` : ''}`,
    `**Published:** ${o.published || 'unknown'} · [original](${o.url})`,
    `**Lenses:** ${o.lenses.join(', ')}`,
    '',
    o.body.trim(),
    '',
  ].join('\n');
  writeFileSync(file, fm);
  // Queue a snapshot if the item has a fetchable URL. youtube watch URLs
  // are skipped — Playwright against youtube.com hits anti-bot consistently;
  // transcripts already provide the text-side citation.
  if (o.url && !/youtube\.com|youtu\.be|reddit\.com/.test(o.url)) {
    SNAPSHOT_QUEUE.push({ url: o.url, category: o.category, slug: slugBase });
  }
  return file;
}

// Drain the snapshot queue with a small concurrency cap. Failures are logged
// and skipped — citation card pipeline can also fall back to URL re-fetch.
async function drainSnapshots(concurrency = 3): Promise<void> {
  if (SNAPSHOT_QUEUE.length === 0) return;
  console.log(`\n📸 Snapshotting ${SNAPSHOT_QUEUE.length} new items (concurrency=${concurrency})…`);
  let ok = 0, fail = 0;
  const queue = SNAPSHOT_QUEUE.slice();
  const workers = Array.from({ length: concurrency }, async () => {
    while (queue.length > 0) {
      const job = queue.shift();
      if (!job) break;
      try {
        const r = await snapshot(job);
        if (r.skipped) ok++; else ok++;
      } catch (e: any) {
        fail++;
        console.log(`  ⚠️  snapshot ${job.url}: ${e.message}`);
      }
    }
  });
  await Promise.all(workers);
  await closeBrowser();
  console.log(`  ✓ snapshots: ${ok} ok, ${fail} failed`);
}

// ---------------------------------------------------------------------------
// Adapter: generic RSS / Atom
// ---------------------------------------------------------------------------
async function fetchRss(category: string, src: RssSource, state: State): Promise<number> {
  let raw: string;
  try { raw = await getText(src.url); }
  catch (e: any) { console.log(`  ⚠️  ${src.name}: ${e.message}`); return 0; }

  let doc: any;
  try { doc = xml.parse(raw); } catch (e: any) { console.log(`  ⚠️  ${src.name}: parse error`); return 0; }

  const rssItems = asArray(doc?.rss?.channel?.item);
  const atomItems = asArray(doc?.feed?.entry);
  const items = rssItems.length ? rssItems : atomItems;
  const isAtom = !rssItems.length && atomItems.length > 0;

  let written = 0;
  for (const it of items) {
    if (written >= MAX_PER_SOURCE) break;
    const title = txt(it.title).trim();
    let link = '';
    if (isAtom) {
      const links = asArray(it.link);
      link = (links.find((l: any) => l['@_rel'] === 'alternate') || links[0])?.['@_href'] || '';
    } else {
      link = txt(it.link).trim() || it.link?.['@_href'] || it.guid?.['#text'] || txt(it.guid);
    }
    if (!title || !link) continue;
    if (state.seen[link]) continue;

    if (src.slug === 'brookings' && BROOKINGS_AI_ONLY) {
      const blob = `${title} ${txt(it.description)} ${txt(it['category'])}`.toLowerCase();
      if (!/(\bai\b|artificial intelligence|machine learning|automation|algorithm|chatbot|gpt|llm)/.test(blob)) continue;
    }

    const published = txt(it.pubDate) || txt(it.published) || txt(it.updated) || txt(it['dc:date']) || '';
    const author = src.author || txt(it['dc:creator']) || txt(it.author?.name) || txt(it.author);
    const rawBody = txt(it['content:encoded']) || txt(it.content) || txt(it.summary) || txt(it.description) || '';
    const body = htmlToMd(rawBody) || '_(no summary in feed — see original)_';

    const lenses = assignLenses(`${title} ${rawBody}`, src.defaults);
    writeItem({
      category, title, author, url: link, sourceType: category === 'newsletters' ? 'newsletter' : category === 'thinktanks' ? 'think-tank' : 'news',
      published, lenses, tags: [src.slug], body, sourceName: src.name,
    });
    state.seen[link] = new Date().toISOString();
    written++;
  }
  console.log(`  ✓ ${src.name}: ${written} new`);
  return written;
}

// ---------------------------------------------------------------------------
// Adapter: Reddit (public JSON)
// ---------------------------------------------------------------------------
async function fetchReddit(sub: string, defaults: Lens[], state: State): Promise<number> {
  const url = `https://www.reddit.com/r/${sub}/top.json?t=week&limit=25`;
  let json: any;
  try { json = JSON.parse(await getText(url)); }
  catch (e: any) { console.log(`  ⚠️  r/${sub}: ${e.message}`); return 0; }

  const posts = asArray(json?.data?.children);
  let written = 0;
  for (const p of posts) {
    if (written >= MAX_PER_SOURCE) break;
    const d = p.data;
    if (!d || d.stickied || d.score < 50) continue;        // filter low-signal
    const permalink = `https://www.reddit.com${d.permalink}`;
    if (state.seen[permalink]) continue;
    const title = String(d.title || '').trim();
    if (!title) continue;
    const selftext = String(d.selftext || '').trim();
    const linkOut = d.url && !d.url.includes('reddit.com') ? `\n\n**Links to:** ${d.url}` : '';
    const body = `**r/${sub}** · ${d.score} upvotes · ${d.num_comments} comments\n\n${selftext || '_(link post — discussion thread)_'}${linkOut}`;
    const lenses = assignLenses(`${title} ${selftext}`, defaults);
    writeItem({
      category: 'reddit', title, author: `u/${d.author}`, url: permalink,
      sourceType: 'reddit', published: new Date(d.created_utc * 1000).toISOString(),
      lenses, tags: [`r-${sub}`], body, sourceName: `r/${sub}`,
    });
    state.seen[permalink] = new Date().toISOString();
    written++;
  }
  console.log(`  ✓ r/${sub}: ${written} new`);
  return written;
}

// ---------------------------------------------------------------------------
// Adapter: YouTube (resolve channel_id from handle -> channel RSS)
// Transcript via youtube_transcript_api if available; else RSS metadata+description.
// ---------------------------------------------------------------------------
async function resolveChannelId(handle: string): Promise<string | null> {
  try {
    const html = await getText(`https://www.youtube.com/@${handle}`);
    const m = html.match(/"channelId":"(UC[\w-]+)"/) || html.match(/channel\/(UC[\w-]+)/);
    return m ? m[1]! : null;
  } catch { return null; }
}

function tryTranscript(videoId: string): string | null {
  try {
    const proc = Bun.spawnSync([
      'python3', '-c',
      `import sys,json\ntry:\n from youtube_transcript_api import YouTubeTranscriptApi as Y\n t=Y.get_transcript("${videoId}")\n print(" ".join(x["text"] for x in t))\nexcept Exception as e:\n sys.exit(2)`,
    ]);
    if (proc.exitCode === 0) {
      const out = proc.stdout.toString().trim();
      return out.length > 50 ? out : null;
    }
  } catch {}
  return null;
}

async function fetchYouTube(ch: { handle: string; slug: string; defaults: Lens[] }, state: State): Promise<number> {
  const cid = await resolveChannelId(ch.handle);
  if (!cid) { console.log(`  ⚠️  @${ch.handle}: could not resolve channel id`); return 0; }
  let raw: string;
  try { raw = await getText(`https://www.youtube.com/feeds/videos.xml?channel_id=${cid}`); }
  catch (e: any) { console.log(`  ⚠️  @${ch.handle}: ${e.message}`); return 0; }

  const doc = xml.parse(raw);
  const entries = asArray(doc?.feed?.entry);
  const channelName = txt(doc?.feed?.title) || ch.handle;
  let written = 0;
  for (const e of entries) {
    if (written >= MAX_PER_SOURCE) break;
    const videoId = txt(e['yt:videoId']);
    const title = txt(e.title).trim();
    const url = `https://www.youtube.com/watch?v=${videoId}`;
    if (!videoId || !title || state.seen[url]) continue;
    const published = txt(e.published);
    const desc = txt(e['media:group']?.['media:description']) || '';
    const transcript = tryTranscript(videoId);
    const lenses = assignLenses(`${title} ${desc} ${transcript || ''}`, ch.defaults);

    const body = transcript
      ? `**Transcript:**\n\n${transcript}`
      : `**Description:**\n\n${desc || '_(no description)_'}\n\n> ⚠️ Full transcript not ingested (youtube_transcript_api unavailable). See bd backlog.`;

    // Wiki page (FTS + embeddings)
    writeItem({
      category: 'youtube', title, author: channelName, url,
      sourceType: 'youtube', published, lenses, tags: [ch.slug, transcript ? 'transcript' : 'metadata'],
      body, sourceName: channelName,
    });
    // Mirror raw transcript/metadata into raw/transcripts/<channel>/ (counts as videos_ready)
    const rawDir = join(WIKI_ROOT, 'raw', 'transcripts', ch.slug);
    mkdirSync(rawDir, { recursive: true });
    const rawFm = [
      '---', `title: ${JSON.stringify(title)}`, `author: ${channelName}`, `url: ${url}`,
      `video_id: ${videoId}`, `channel: ${ch.slug}`, `published: ${published}`,
      `indexed: ${new Date().toISOString()}`, `thesis_lens: [${lenses.join(', ')}]`,
      `type: youtube`, `transcript: ${transcript ? 'yes' : 'no'}`, '---', '', `# ${title}`, '', body, '',
    ].join('\n');
    writeFileSync(join(rawDir, `${videoId}-${slugify(title)}.md`), rawFm);

    state.seen[url] = new Date().toISOString();
    written++;
  }
  console.log(`  ✓ @${ch.handle} (${channelName}): ${written} new`);
  return written;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
async function runClass(name: string, state: State): Promise<number> {
  let n = 0;
  console.log(`\n▶ ${name}`);
  switch (name) {
    case 'newsletters': for (const s of NEWSLETTERS) n += await fetchRss('newsletters', s, state); break;
    case 'news':        for (const s of NEWS) n += await fetchRss('news', s, state); break;
    case 'thinktanks':  for (const s of THINKTANKS) n += await fetchRss('thinktanks', s, state); break;
    case 'reddit':      for (const r of REDDIT_SUBS) n += await fetchReddit(r.sub, r.defaults, state); break;
    case 'youtube':     for (const c of YOUTUBE_CHANNELS) n += await fetchYouTube(c, state); break;
    default: console.log(`  (unknown class: ${name})`);
  }
  state.lastRun[name] = new Date().toISOString();
  return n;
}

async function main() {
  const ALL = ['newsletters', 'news', 'thinktanks', 'reddit', 'youtube'];
  const args = process.argv.slice(2).filter((a) => !a.startsWith('-'));
  const classes = args.length ? args : ALL;
  const state = loadState();
  let total = 0;
  console.log(`🛰️  AI-Futures fetch — classes: ${classes.join(', ')}`);
  for (const c of classes) total += await runClass(c, state);
  saveState(state);
  await drainSnapshots();
  console.log(`\n✅ Done. ${total} new items written. State: ${STATE_PATH}`);
}

if (import.meta.main) {
  main().catch((e) => { console.error(e); process.exit(1); });
}

export { main, runClass, assignLenses };

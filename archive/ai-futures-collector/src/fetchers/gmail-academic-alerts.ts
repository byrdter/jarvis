/**
 * Academic alert-email parser.
 *
 * Reads forwarded academic alert emails from the JARVIS Gmail inbox
 * (Google Scholar alerts, SSRN, journal eTOC alerts) and turns each referenced
 * paper into a captured item: title + link + (DOI/abstract when present),
 * flagged needs_fulltext so you retrieve the PDF via institutional access.
 *
 * This complements the RSS sweep ("Both" coverage): Scholar + SSRN only push
 * via email, never RSS. SETUP: in Google Scholar / SSRN / journal sites, set
 * alerts to email the JARVIS-connected Gmail (or forward them there). JARVIS
 * already has read access; this parser does the rest.
 *
 * Requires GOOGLE_* OAuth in .env. If absent, returns [] gracefully.
 *
 * Usage:  bun run src/fetchers/gmail-academic-alerts.ts [--dry]
 */

import { mkdirSync, readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import type { NewItem } from './sweep';

const WIKI_ROOT = '/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis-private/ai-futures-wiki';
const OUT_DIR = join(WIKI_ROOT, 'wiki', 'academic');
const STATE_PATH = join(import.meta.dir, '.academic-alerts-state.json');

// Senders / subjects that mark an academic alert email.
const ALERT_QUERY =
  '(from:scholaralerts-noreply@google.com OR from:scholarcitations-noreply@google.com OR ' +
  'from:noreply@ssrn.com OR from:ssrn@ssrn.com OR subject:"Table of Contents" OR ' +
  'subject:"new results" OR subject:"new citations" OR subject:"eTOC") newer_than:3d';

const DOI_RE = /\b10\.\d{4,9}\/[-._;()/:A-Za-z0-9]+/;
const slug = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 70) || 'paper';

interface State { seen: Record<string, string>; }
const loadState = (): State => { try { return JSON.parse(readFileSync(STATE_PATH, 'utf-8')); } catch { return { seen: {} }; } };
const saveState = (s: State) => writeFileSync(STATE_PATH, JSON.stringify(s, null, 2));

/** Extract (title, url) pairs from an alert email's HTML/text body. */
function extractEntries(body: string): Array<{ title: string; url: string }> {
  const out: Array<{ title: string; url: string }> = [];
  const seen = new Set<string>();
  // Google Scholar: <h3 ...><a href="URL">Title</a></h3>
  const h3 = /<h3[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)<\/a>/gis;
  let m: RegExpExecArray | null;
  while ((m = h3.exec(body))) push(m[1]!, strip(m[2]!));
  // Fallback / SSRN / eTOC: any anchor with a substantial title.
  if (out.length === 0) {
    const a = /<a[^>]*href="([^"]+)"[^>]*>(.*?)<\/a>/gis;
    while ((m = a.exec(body))) {
      const url = m[1]!, title = strip(m[2]!);
      if (title.length >= 25 && /^https?:/.test(url) && !/unsubscribe|scholar\.google|settings|preferences/i.test(url + title)) push(url, title);
    }
  }
  function push(url: string, title: string) {
    const key = title.toLowerCase();
    if (!title || seen.has(key)) return;
    seen.add(key); out.push({ title, url });
  }
  function strip(h: string) { return h.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, ' ').trim(); }
  return out;
}

function senderType(from: string): string {
  if (/scholar/i.test(from)) return 'Google Scholar alert';
  if (/ssrn/i.test(from)) return 'SSRN alert';
  return 'Journal eTOC alert';
}

function writeAlert(it: NewItem) {
  mkdirSync(OUT_DIR, { recursive: true });
  const file = join(OUT_DIR, `alert--${slug(it.title)}.md`);
  const fm = [
    '---', `title: ${JSON.stringify(it.title)}`, `source: ${it.sourceName}`,
    `source_type: academic-alert`, `tier: "1.5"`, `access: alert`,
    it.doi ? `doi: ${it.doi}` : 'doi: ', `needs_fulltext: true`,
    `url: ${it.url}`, `indexed: ${new Date().toISOString()}`,
    `thesis_lens: [${it.lenses.join(', ')}]`, `tags: [academic-alert]`, '---', '',
    `# ${it.title}`, '', `**Via:** ${it.sourceName} · [link](${it.url})`,
    it.doi ? `**DOI:** [${it.doi}](https://doi.org/${it.doi})` : '',
    `**⚠️ Retrieve full text via institutional access.**`, '',
    it.abstract || '_(alert entry — open link for abstract)_', '',
  ].filter((l) => l !== '').join('\n');
  writeFileSync(file, fm);
}

export async function parseAcademicAlerts(opts: { dry?: boolean } = {}): Promise<NewItem[]> {
  let gmail: any;
  try { ({ gmail } = await import('../../integrations/gmail.ts')); }
  catch { console.log('  (Gmail not configured — skipping academic alert parse)'); return []; }

  const state = loadState();
  let messages: any[] = [];
  try { messages = await gmail.searchEmails({ query: ALERT_QUERY, maxResults: 25, includeBody: true }); }
  catch (e: any) { console.log(`  ⚠️ Gmail search failed: ${String(e.message).slice(0, 120)}`); return []; }

  const items: NewItem[] = [];
  for (const msg of messages) {
    const body = msg.body || msg.snippet || '';
    const from = msg.from || '';
    const sourceName = senderType(from);
    for (const e of extractEntries(body)) {
      if (state.seen[e.url] || items.some((i) => i.title.toLowerCase() === e.title.toLowerCase())) continue;
      const doi = (e.url.match(DOI_RE) || body.match(DOI_RE))?.[0]?.replace(/[.,)]+$/, '');
      const item: NewItem = {
        sourceId: 'academic-alert', sourceName, tier: '1.5', category: 'academic',
        title: e.title, author: '', url: e.url, published: msg.date ? new Date(msg.date).toISOString() : '',
        lenses: ['economic-futures', 'strategic-choices'], access: 'alert', doi,
        abstract: undefined, needs_fulltext: true,
      };
      if (!opts.dry) { writeAlert(item); state.seen[e.url] = new Date().toISOString(); }
      items.push(item);
    }
  }
  if (!opts.dry) saveState(state);
  console.log(`  📧 Academic alerts: ${items.length} new paper(s) from ${messages.length} alert email(s)`);
  return items;
}

if (import.meta.main) {
  parseAcademicAlerts({ dry: process.argv.includes('--dry') }).catch((e) => { console.error(e); process.exit(1); });
}

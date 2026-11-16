/**
 * Daily digest builder + delivery for the Byrddynasty knowledge pipeline.
 *
 * Sweeps the requested cadences, collates new items (plus any academic-alert
 * items parsed from forwarded emails), formats an email (HTML) + Telegram
 * (markdown) digest grouped by tier, with paywalled academic items surfaced
 * FIRST as "retrieve full text" with DOI links — then delivers via notify.ts
 * (Gmail if configured, else Telegram).
 *
 * Usage:
 *   bun run src/fetchers/digest.ts            # daily cadence -> deliver
 *   bun run src/fetchers/digest.ts daily weekly
 *   bun run src/fetchers/digest.ts daily --dry   # build but don't send
 */

import { runSweep, type NewItem } from './sweep';
import { deliver, chosenChannel } from './notify';
import type { Cadence } from './sources';

const TIER_LABEL: Record<string, string> = {
  '1': '📊 Tier 1 — Data Anchors',
  '1.5': '🎓 Tier 1.5 — Academic Evidence',
  '2': '⚖️ Tier 2 — Power, Governance & Safety',
  '3': '📰 Tier 3 — Analysis & Story Ideas',
  '4': '📚 Tier 4 — History & Frameworks',
  '5': '🏢 Tier 5 — Primary & Company Sources',
};
const LENS_LABEL: Record<string, string> = {
  'power-control': 'Power', 'economic-futures': 'Economy', 'meaning-identity': 'Meaning',
  'strategic-choices': 'Strategy', 'social-consequences': 'Society',
};

function lensTags(it: NewItem) { return it.lenses.map((l) => LENS_LABEL[l] || l).join(' · '); }

export function buildDigest(items: NewItem[], cadences: string[]): { subject: string; html: string; text: string } {
  const date = new Date().toISOString().slice(0, 10);
  const paywalled = items.filter((i) => i.needs_fulltext);
  const rest = items.filter((i) => !i.needs_fulltext);

  const subject = `🛰️ AI-Futures Digest — ${date} (${items.length} new${paywalled.length ? `, ${paywalled.length} to retrieve` : ''})`;

  // ── HTML (email) ──
  const h: string[] = [];
  h.push(`<div style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:680px;margin:0 auto;color:#1a1a1a">`);
  h.push(`<h2 style="margin:0 0 4px">🛰️ AI-Futures Digest</h2>`);
  h.push(`<p style="color:#666;margin:0 0 16px">${date} · ${items.length} new items · cadence: ${cadences.join(', ')}</p>`);

  if (paywalled.length) {
    h.push(`<div style="background:#fff7e6;border:1px solid #ffd591;border-radius:8px;padding:12px 16px;margin-bottom:18px">`);
    h.push(`<h3 style="margin:0 0 8px">🎓 Retrieve full text (${paywalled.length}) — paywalled academic</h3>`);
    h.push(`<p style="color:#874d00;margin:0 0 10px;font-size:13px">Grab these via your institutional databases, then drop the PDF in <code>ai-futures-wiki/EffectAI24-26/</code> to auto-ingest.</p>`);
    for (const it of paywalled) {
      h.push(`<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #f0e0c0">`);
      h.push(`<b>${esc(it.title)}</b><br><span style="font-size:12px;color:#555">${esc(it.sourceName)} · ${esc(it.author)} · ${lensTags(it)}</span>`);
      if (it.doi) h.push(`<br><a href="https://doi.org/${it.doi}" style="font-size:12px">doi.org/${it.doi}</a>`);
      else h.push(`<br><a href="${it.url}" style="font-size:12px">${esc(it.url)}</a>`);
      if (it.abstract) h.push(`<div style="font-size:12px;color:#444;margin-top:4px">${esc(it.abstract.slice(0, 320))}…</div>`);
      h.push(`</div>`);
    }
    h.push(`</div>`);
  }

  for (const tier of ['1', '1.5', '2', '3', '4', '5']) {
    const group = rest.filter((i) => i.tier === tier);
    if (!group.length) continue;
    h.push(`<h3 style="margin:18px 0 8px;border-bottom:2px solid #eee;padding-bottom:4px">${TIER_LABEL[tier]} (${group.length})</h3>`);
    for (const it of group) {
      h.push(`<div style="margin-bottom:8px">`);
      h.push(`<a href="${it.url}" style="font-weight:600;text-decoration:none;color:#0b5fff">${esc(it.title)}</a>`);
      h.push(`<br><span style="font-size:12px;color:#777">${esc(it.sourceName)} · ${lensTags(it)}</span>`);
      h.push(`</div>`);
    }
  }
  h.push(`<p style="color:#999;font-size:11px;margin-top:24px">JARVIS · ${items.length} items swept from the unified source registry. Reply to tune sources.</p>`);
  h.push(`</div>`);

  // ── Telegram (markdown) ──
  const t: string[] = [];
  t.push(`${date} · ${items.length} new (${cadences.join(', ')})`);
  if (paywalled.length) {
    t.push(`\n🎓 *Retrieve full text (${paywalled.length})*`);
    for (const it of paywalled.slice(0, 15)) {
      const link = it.doi ? `https://doi.org/${it.doi}` : it.url;
      t.push(`• [${trunc(it.title, 90)}](${link}) — ${it.sourceName}`);
    }
  }
  for (const tier of ['1', '1.5', '2', '3', '4', '5']) {
    const group = rest.filter((i) => i.tier === tier);
    if (!group.length) continue;
    t.push(`\n${TIER_LABEL[tier]} (${group.length})`);
    for (const it of group.slice(0, 12)) t.push(`• [${trunc(it.title, 90)}](${it.url}) — ${it.sourceName}`);
  }
  return { subject, html: h.join('\n'), text: t.join('\n') };
}

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const trunc = (s: string, n: number) => (s.length > n ? s.slice(0, n - 1) + '…' : s).replace(/([[\]()])/g, '\\$1');

export async function runDigest(cadences: (Cadence | 'all')[], opts: { dry?: boolean } = {}) {
  const items: NewItem[] = [];
  for (const c of cadences) items.push(...(await runSweep(c)));

  if (!items.length) {
    console.log('No new items — skipping digest.');
    return { sent: false, count: 0 };
  }
  const digest = buildDigest(items, cadences);
  console.log(`\n📋 Digest: ${digest.subject}`);
  if (opts.dry) {
    console.log(`(dry run — not sending). Channel would be: ${chosenChannel()}`);
    return { sent: false, count: items.length, digest };
  }
  const res = await deliver(digest);
  console.log(res.ok ? `✅ Delivered via ${res.channel} (${res.detail})` : `❌ Delivery failed: ${res.detail}`);
  return { sent: res.ok, count: items.length, channel: res.channel };
}

if (import.meta.main) {
  const args = process.argv.slice(2);
  const dry = args.includes('--dry');
  const cadences = (args.filter((a) => !a.startsWith('--')) as (Cadence | 'all')[]);
  runDigest(cadences.length ? cadences : ['daily'], { dry }).catch((e) => { console.error(e); process.exit(1); });
}

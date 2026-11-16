/**
 * Snapshot a URL to originals/<category>/<slug>.{pdf,png}.
 *
 * Captures BOTH a print-PDF (preserves text, selectable, ~clean) AND a full-page
 * PNG (preserves visual layout exactly as the user would see it). The PDF is the
 * preferred citation-card source because page bounding boxes are deterministic;
 * the PNG is the fallback for pages whose print stylesheet drops too much.
 *
 * Used by:
 *   - daily news/yt/newsletter fetchers via snapshotOnIngest() at end of each item
 *   - snapshot-backfill.ts for existing items missing originals
 *
 * Usage as a library:
 *   import { snapshot } from './snapshot';
 *   const { pdfPath, pngPath } = await snapshot({ url, category: 'news', slug });
 *
 * Usage as a CLI (quick test):
 *   bun run src/fetchers/snapshot.ts <url> <category> <slug>
 */

import { chromium, type Browser } from 'playwright';
import { mkdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';

const WIKI_ROOT = '/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis-private/ai-futures-wiki';

// Common cookie-banner / dismiss selectors. We try each; failures are ignored.
const DISMISS_SELECTORS = [
  'button:has-text("Accept all")',
  'button:has-text("Accept All")',
  'button:has-text("I agree")',
  'button:has-text("I Agree")',
  'button:has-text("Got it")',
  'button:has-text("Continue")',
  '[aria-label="Accept all cookies"]',
  '[aria-label="Accept cookies"]',
  '#onetrust-accept-btn-handler',
  '.cc-allow',
];

export interface SnapshotInput {
  url: string;
  category: string;       // e.g. "news", "newsletters", "youtube"
  slug: string;           // wiki page slug without extension
  overwrite?: boolean;    // default false; skip if both files already exist
  extraDismiss?: string[];
  timeoutMs?: number;
}

export interface SnapshotResult {
  pdfPath: string;        // relative to wiki root, e.g. "originals/news/foo.pdf"
  pngPath: string;
  skipped: boolean;
}

async function dismissBanners(page: any, extras: string[] = []): Promise<void> {
  const all = [...extras, ...DISMISS_SELECTORS];
  for (const sel of all) {
    try {
      const el = await page.$(sel);
      if (el) {
        await el.click({ timeout: 500 }).catch(() => {});
        break;
      }
    } catch {
      // ignore
    }
  }
}

let _browser: Browser | null = null;
async function getBrowser(): Promise<Browser> {
  if (_browser && _browser.isConnected()) return _browser;
  _browser = await chromium.launch({ headless: true });
  return _browser;
}

export async function closeBrowser(): Promise<void> {
  if (_browser) {
    await _browser.close();
    _browser = null;
  }
}

export async function snapshot(input: SnapshotInput): Promise<SnapshotResult> {
  const dstDir = join(WIKI_ROOT, 'originals', input.category);
  const base = join(dstDir, input.slug);
  const pdfAbs = base + '.pdf';
  const pngAbs = base + '.png';
  const pdfRel = join('originals', input.category, input.slug + '.pdf');
  const pngRel = join('originals', input.category, input.slug + '.png');

  if (!input.overwrite && existsSync(pdfAbs) && existsSync(pngAbs)) {
    return { pdfPath: pdfRel, pngPath: pngRel, skipped: true };
  }

  mkdirSync(dirname(pdfAbs), { recursive: true });

  const browser = await getBrowser();
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    userAgent:
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' +
      '(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  });
  const page = await ctx.newPage();
  // Hard cap on the WHOLE per-page operation (nav + dismiss + screenshot + pdf).
  // Heavy ad pages can hang networkidle and freeze screenshot/pdf indefinitely;
  // we'd rather lose one snapshot than block the queue.
  const overallTimeoutMs = input.timeoutMs ?? 45_000;
  const overallDeadline = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error(`overall timeout ${overallTimeoutMs}ms`)), overallTimeoutMs)
  );
  const doCapture = async () => {
    try {
      // 'domcontentloaded' is far more reliable than 'networkidle' across the
      // newsletter/news landscape (ads, analytics, third-party widgets).
      await page.goto(input.url, { waitUntil: 'domcontentloaded', timeout: 20_000 });
    } catch {
      // Fallback: try a looser strategy. If even this fails we re-throw.
      await page.goto(input.url, { waitUntil: 'commit', timeout: 10_000 });
    }
    await dismissBanners(page, input.extraDismiss);
    await page.waitForTimeout(500);
    await page.screenshot({ path: pngAbs, fullPage: true, type: 'png', timeout: 15_000 });
    await page.emulateMedia({ media: 'screen' });
    await page.pdf({
      path: pdfAbs,
      format: 'Letter',
      printBackground: true,
      margin: { top: '0.4in', bottom: '0.4in', left: '0.4in', right: '0.4in' },
    });
  };
  try {
    await Promise.race([doCapture(), overallDeadline]);
  } finally {
    await ctx.close().catch(() => {});
  }

  return { pdfPath: pdfRel, pngPath: pngRel, skipped: false };
}

/**
 * Convenience wrapper for fetcher integration. Returns null on failure
 * (logged to stderr) so the caller can decide whether to abort the ingest
 * or just record the URL without a snapshot.
 */
export async function snapshotOnIngest(
  input: SnapshotInput
): Promise<SnapshotResult | null> {
  try {
    return await snapshot(input);
  } catch (err) {
    console.error(`[snapshot] failed for ${input.url}: ${(err as Error).message}`);
    return null;
  }
}

// CLI entry point.
if (import.meta.main) {
  const [url, category, slug] = process.argv.slice(2);
  if (!url || !category || !slug) {
    console.error('usage: bun run src/fetchers/snapshot.ts <url> <category> <slug>');
    process.exit(1);
  }
  snapshot({ url, category, slug })
    .then((r) => {
      console.log(JSON.stringify(r, null, 2));
    })
    .catch((e) => {
      console.error('snapshot failed:', e);
      process.exit(1);
    })
    .finally(() => closeBrowser());
}

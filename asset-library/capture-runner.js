#!/usr/bin/env node
// Playbook-driven asset capture for the asset library.
//
// Usage:
//   node capture-runner.js <product>       # run one playbook
//   node capture-runner.js --all           # run every playbook
//
// A playbook exports: { product, surfaces: [{ name, shots: [...] }] }
// where each shot is one of:
//   { type: 'screenshot',    name, url, fullPage?, selector?, wait? }
//   { type: 'scroll-video',  name, url, duration, viewport? }
//   { type: 'click-shot',    name, url, selector, wait? }

import { chromium } from 'playwright';
import { mkdir, writeFile, readdir, copyFile, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PLAYBOOKS_DIR = path.join(__dirname, 'playbooks');
const PRODUCTS_DIR  = path.join(__dirname, 'products');

const DEFAULT_VIEWPORT = { width: 1440, height: 900 };
const DEFAULT_WAIT = 1500;
const DEFAULT_WAIT_UNTIL = 'domcontentloaded';

async function ensureDir(p) { await mkdir(p, { recursive: true }); }

function outPath(product, surface, name, ext) {
  return path.join(PRODUCTS_DIR, product, 'surfaces', surface, `${name}.${ext}`);
}

async function runScreenshot(page, shot, dest) {
  await page.goto(shot.url, { waitUntil: shot.waitUntil ?? DEFAULT_WAIT_UNTIL });
  await page.waitForTimeout(shot.wait ?? DEFAULT_WAIT);
  if (shot.selector) {
    const el = await page.locator(shot.selector).first();
    await el.screenshot({ path: dest });
  } else {
    await page.screenshot({ path: dest, fullPage: shot.fullPage ?? false });
  }
  console.log(`  ✓ ${path.basename(dest)}`);
}

async function runClickShot(page, shot, dest) {
  await page.goto(shot.url, { waitUntil: shot.waitUntil ?? DEFAULT_WAIT_UNTIL });
  await page.waitForTimeout(shot.wait ?? DEFAULT_WAIT);
  await page.locator(shot.selector).first().click();
  await page.waitForTimeout(shot.wait ?? DEFAULT_WAIT);
  await page.screenshot({ path: dest });
  console.log(`  ✓ ${path.basename(dest)} (after click)`);
}

async function runScrollVideo(browser, shot, dest) {
  const viewport = shot.viewport ?? DEFAULT_VIEWPORT;
  const ctx = await browser.newContext({
    viewport,
    recordVideo: { dir: path.dirname(dest), size: viewport },
  });
  const page = await ctx.newPage();
  await page.goto(shot.url, { waitUntil: shot.waitUntil ?? DEFAULT_WAIT_UNTIL });
  await page.waitForTimeout(800);

  const steps = Math.max(2, Math.floor(shot.duration / 0.4));
  for (let i = 0; i < steps; i++) {
    await page.evaluate(() => window.scrollBy({ top: window.innerHeight * 0.6, behavior: 'smooth' }));
    await page.waitForTimeout(400);
  }
  await page.waitForTimeout(500);

  const video = page.video();
  await ctx.close();
  if (video) {
    const tmp = await video.path();
    await copyFile(tmp, dest);
    await rm(tmp, { force: true });
    console.log(`  ✓ ${path.basename(dest)} (${shot.duration}s scroll)`);
  } else {
    console.warn(`  ! no video produced for ${shot.name}`);
  }
}

async function runPlaybook(playbookPath) {
  const mod = await import(pathToFileURL(playbookPath).href);
  const pb = mod.default ?? mod;
  console.log(`\n▶ ${pb.product}`);

  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: DEFAULT_VIEWPORT });
  const page = await ctx.newPage();

  for (const surface of pb.surfaces) {
    const surfaceDir = path.join(PRODUCTS_DIR, pb.product, 'surfaces', surface.name);
    await ensureDir(surfaceDir);
    console.log(`  surface: ${surface.name}`);

    for (const shot of surface.shots) {
      try {
        if (shot.type === 'screenshot') {
          await runScreenshot(page, shot, outPath(pb.product, surface.name, shot.name, 'png'));
        } else if (shot.type === 'click-shot') {
          await runClickShot(page, shot, outPath(pb.product, surface.name, shot.name, 'png'));
        } else if (shot.type === 'scroll-video') {
          await runScrollVideo(browser, shot, outPath(pb.product, surface.name, shot.name, 'webm'));
        } else {
          console.warn(`  ! unknown shot type: ${shot.type}`);
        }
      } catch (err) {
        console.error(`  ✗ ${shot.name}: ${err.message}`);
      }
    }
  }

  await ctx.close();
  await browser.close();

  const metaPath = path.join(PRODUCTS_DIR, pb.product, 'meta.json');
  if (existsSync(metaPath)) {
    const { readFile } = await import('node:fs/promises');
    const meta = JSON.parse(await readFile(metaPath, 'utf8'));
    meta.last_captured = new Date().toISOString().slice(0, 10);
    await writeFile(metaPath, JSON.stringify(meta, null, 2) + '\n');
  }
}

async function main() {
  const arg = process.argv[2];
  if (!arg) {
    console.error('Usage: node capture-runner.js <product> | --all');
    process.exit(1);
  }
  if (arg === '--all') {
    const files = (await readdir(PLAYBOOKS_DIR)).filter(f => f.endsWith('.js'));
    for (const f of files) await runPlaybook(path.join(PLAYBOOKS_DIR, f));
  } else {
    await runPlaybook(path.join(PLAYBOOKS_DIR, `${arg}.js`));
  }
}

main().catch(err => { console.error(err); process.exit(1); });

/**
 * Phase 4 — Ingest & Index the ai-futures wiki.
 *
 * 1. Rebuild FTS5 index (ai_futures_fts) from wiki/ pages.
 * 2. Build local embeddings (all-MiniLM-L6-v2, $0) over wiki/ + raw/transcripts/.
 * 3. Update .manifest.json stats.
 * 4. Verify: print FTS stats + a sample semantic search.
 *
 * Run: bun run src/fetchers/reindex-ai-futures.ts
 */

import { WikiSearchIndex } from '../api/wiki-search';
import { EmbeddingService } from '../embeddings';
import { getWiki } from '../api/wikis-registry';
import { readdirSync, readFileSync, writeFileSync, statSync } from 'fs';
import { readFileSyncRetry, readdirSyncRetry } from './fs-retry';
import { join } from 'path';

const SLUG = 'ai-futures';
const wiki = getWiki(SLUG);
if (!wiki) throw new Error(`Wiki ${SLUG} not registered`);
const ROOT = wiki.rootPath;

function walk(dir: string): string[] {
  const out: string[] = [];
  const rec = (d: string) => {
    let entries: string[] = [];
    try { entries = readdirSyncRetry(d); } catch { return; }
    for (const e of entries) {
      const p = join(d, e);
      const s = statSync(p);
      if (s.isDirectory()) rec(p);
      else if (e.endsWith('.md')) out.push(p);
    }
  };
  rec(dir);
  return out;
}

async function main() {
  console.log(`📚 Indexing wiki: ${SLUG}\n`);

  // 1. FTS reindex (this wiki only)
  const index = new WikiSearchIndex();
  const { pageCount } = index.reindex(SLUG);
  console.log(`✓ FTS5 reindex: ${pageCount} pages -> ${wiki!.ftsTable}`);

  // 2. Embeddings over wiki/ + raw/transcripts/
  const wikiFiles = walk(join(ROOT, 'wiki')).filter(
    (f) => !/\/(hot|index|log)\.md$/.test(f)
  );
  const rawFiles = walk(join(ROOT, 'raw'));
  const allFiles = [...wikiFiles, ...rawFiles];
  const embDbPath = join(import.meta.dir, '../../data/knowledge-embeddings.db');
  const emb = new EmbeddingService(embDbPath, ROOT);
  const res = await emb.indexFiles(allFiles, true);
  console.log(`✓ Embeddings: ${res.indexed} indexed, ${res.skipped} unchanged, ${res.failed} failed`);

  // 3. Update manifest stats
  const manifestPath = join(ROOT, '.manifest.json');
  const manifest = JSON.parse(readFileSyncRetry(manifestPath, 'utf-8'));
  let totalWords = 0;
  for (const f of wikiFiles) totalWords += readFileSyncRetry(f, 'utf-8').split(/\s+/).length;
  let videosReady = 0;
  try {
    const tdir = join(ROOT, 'raw/transcripts');
    for (const ch of readdirSync(tdir)) {
      const cp = join(tdir, ch);
      if (statSync(cp).isDirectory()) videosReady += readdirSync(cp).filter((x) => x.endsWith('.md')).length;
    }
  } catch {}
  manifest.last_updated = new Date().toISOString();
  manifest.phase = '4-complete';
  manifest.stats = {
    ...manifest.stats,
    total_pages: wikiFiles.length,
    total_sources: allFiles.length,
    total_videos_ready: videosReady,
    total_words: totalWords,
    last_ingest: new Date().toISOString(),
  };
  writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
  console.log(`✓ Manifest: ${wikiFiles.length} pages, ${videosReady} videos, ${totalWords.toLocaleString()} words`);

  // 4. Verify — FTS sample
  console.log('\n🔍 FTS sample  (query: "power who decides"):');
  const fts = index.search(SLUG, 'power who decides', { limit: 3 });
  for (const r of fts.results) console.log(`   • [${r.category}] ${r.title}`);
  if (!fts.results.length) console.log('   (no FTS hits)');

  // 4b. Verify — semantic sample (ai-futures files only)
  console.log('\n🔍 Semantic sample  (query: "Will AI automate jobs or augment workers?"):');
  const sem = await emb.search('Will AI automate jobs or augment workers, and who benefits?', 25);
  const mine = sem.filter((s) => s.path.includes('/ai-futures-wiki/')).slice(0, 5);
  for (const s of mine) {
    const name = s.path.split('/').slice(-2).join('/');
    console.log(`   • ${s.score.toFixed(3)}  ${name}`);
  }
  if (!mine.length) console.log('   (no semantic hits for ai-futures)');

  emb.close();
  console.log('\n✅ Phase 4 complete.');
}

main().catch((e) => { console.error(e); process.exit(1); });

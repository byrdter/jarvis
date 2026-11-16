/**
 * Dropbox-safe synchronous filesystem reads.
 *
 * Files under ~/Library/CloudStorage/Dropbox (the ai-futures wiki lives there)
 * intermittently throw EDEADLK ("Resource deadlock avoided") / EBUSY / EAGAIN
 * when Dropbox is materializing an online-only placeholder or holds a transient
 * lock. This crashed the ai-futures digest (graph.ts buildGraph) and the
 * youtube aggregator. The lock clears in tens of milliseconds, so retry with a
 * short backoff instead of dying. Mirrors commit 5f180c2 (sqlite Dropbox retry).
 */
import { readFileSync as _readFileSync, readdirSync as _readdirSync } from 'fs';

const TRANSIENT = new Set(['EDEADLK', 'EBUSY', 'EAGAIN', 'EBADF', 'EIO']);

function withRetry<T>(fn: () => T, label: string, tries = 6): T {
  let lastErr: any;
  for (let i = 0; i < tries; i++) {
    try {
      return fn();
    } catch (e: any) {
      lastErr = e;
      if (!TRANSIENT.has(e?.code)) throw e;
      // 60,120,180,240,300ms backoff — Dropbox locks clear well within this.
      try { (globalThis as any).Bun?.sleepSync(60 * (i + 1)); } catch { /* no Bun */ }
    }
  }
  console.error(`  fs-retry: gave up on ${label} after ${tries} tries: ${lastErr?.code || lastErr}`);
  throw lastErr;
}

export function readFileSyncRetry(path: string, encoding: BufferEncoding = 'utf-8'): string {
  return withRetry(() => _readFileSync(path, encoding) as string, `read ${path}`);
}

export function readdirSyncRetry(path: string): string[] {
  return withRetry(() => _readdirSync(path) as string[], `readdir ${path}`);
}

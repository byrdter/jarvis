/**
 * Knowledge graph over the ai-futures wiki.
 *
 * Turns the 478+ pages into a queryable graph so you can ask:
 *   • "Show everything across all sources about the entry-level job squeeze."
 *   • "Which entities (Microsoft, Mollick, Anthropic…) recur, and where?"
 *   • "Per the show-bible rule, which items combine a number + a decision + a precedent?"
 *
 * Storage: bun:sqlite alongside wiki-search.db. No new deps.
 * Build:   bun run src/fetchers/graph.ts build
 * Query:   bun run src/fetchers/graph.ts entity Microsoft
 *          bun run src/fetchers/graph.ts topic "entry-level jobs"
 *          bun run src/fetchers/graph.ts lens power-control --tier 1.5
 *          bun run src/fetchers/graph.ts episodes        # show-bible "promote" candidates
 *          bun run src/fetchers/graph.ts stats
 */

import { Database } from 'bun:sqlite';
import { readdirSync, readFileSync, statSync, existsSync } from 'fs';
import { readFileSyncRetry, readdirSyncRetry } from './fs-retry';
import { join } from 'path';

const WIKI_ROOT = '/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis-private/ai-futures-wiki';
const DB_PATH = join(WIKI_ROOT, 'wiki-graph.db');
const META_SKIP = new Set(['hot.md', 'index.md', 'log.md']);

// ── Entities we want to recognize (precision over recall) ────────────────────
// Curated seed list — grows as the wiki grows. Each entry: regex (word-bounded
// and case-insensitive), canonical name, type, optional aliases handled by the
// regex's alternation.
const ENTITIES: Array<{ re: RegExp; name: string; type: 'person' | 'org' | 'product' | 'concept' }> = [
  // People
  { re: /\b(Ethan Mollick|Mollick)\b/i, name: 'Ethan Mollick', type: 'person' },
  { re: /\b(Jack Clark)\b/i, name: 'Jack Clark', type: 'person' },
  { re: /\b(Ezra Klein)\b/i, name: 'Ezra Klein', type: 'person' },
  { re: /\b(Ben Thompson)\b/i, name: 'Ben Thompson', type: 'person' },
  { re: /\b(Azeem Azhar)\b/i, name: 'Azeem Azhar', type: 'person' },
  { re: /\b(Lex Fridman)\b/i, name: 'Lex Fridman', type: 'person' },
  { re: /\b(Dwarkesh(?: Patel)?)\b/i, name: 'Dwarkesh Patel', type: 'person' },
  { re: /\b(Casey Newton)\b/i, name: 'Casey Newton', type: 'person' },
  { re: /\b(Daron Acemoglu|Acemoglu)\b/i, name: 'Daron Acemoglu', type: 'person' },
  { re: /\b(Erik Brynjolfsson|Brynjolfsson)\b/i, name: 'Erik Brynjolfsson', type: 'person' },
  { re: /\b(Carlota Perez)\b/i, name: 'Carlota Perez', type: 'person' },
  { re: /\b(Satya Nadella|Nadella)\b/i, name: 'Satya Nadella', type: 'person' },
  { re: /\b(Sam Altman|Altman)\b/i, name: 'Sam Altman', type: 'person' },
  { re: /\b(Dario Amodei|Amodei)\b/i, name: 'Dario Amodei', type: 'person' },
  { re: /\b(Sundar Pichai|Pichai)\b/i, name: 'Sundar Pichai', type: 'person' },
  { re: /\b(Mark Zuckerberg|Zuckerberg)\b/i, name: 'Mark Zuckerberg', type: 'person' },
  { re: /\b(Yoshua Bengio|Bengio)\b/i, name: 'Yoshua Bengio', type: 'person' },
  { re: /\b(Geoffrey Hinton|Hinton)\b/i, name: 'Geoffrey Hinton', type: 'person' },
  { re: /\b(Arvind Narayanan|Narayanan)\b/i, name: 'Arvind Narayanan', type: 'person' },
  { re: /\b(Sayash Kapoor|Kapoor)\b/i, name: 'Sayash Kapoor', type: 'person' },
  // Orgs
  { re: /\b(OpenAI)\b/i, name: 'OpenAI', type: 'org' },
  { re: /\b(Anthropic)\b/i, name: 'Anthropic', type: 'org' },
  { re: /\b(Google DeepMind|DeepMind)\b/i, name: 'Google DeepMind', type: 'org' },
  { re: /\b(Microsoft)\b/i, name: 'Microsoft', type: 'org' },
  { re: /\b(Meta(?: Platforms)?)\b/i, name: 'Meta', type: 'org' },
  { re: /\b(Apple)\b/i, name: 'Apple', type: 'org' },
  { re: /\b(Amazon)\b/i, name: 'Amazon', type: 'org' },
  { re: /\b(Nvidia|NVIDIA)\b/i, name: 'Nvidia', type: 'org' },
  { re: /\b(a16z|Andreessen Horowitz)\b/i, name: 'a16z', type: 'org' },
  { re: /\b(Stanford HAI|HAI)\b/i, name: 'Stanford HAI', type: 'org' },
  { re: /\b(Brookings)\b/i, name: 'Brookings', type: 'org' },
  { re: /\b(RAND)\b/i, name: 'RAND', type: 'org' },
  { re: /\b(McKinsey)\b/i, name: 'McKinsey', type: 'org' },
  { re: /\b(NBER)\b/i, name: 'NBER', type: 'org' },
  { re: /\b(AI Now(?: Institute)?)\b/i, name: 'AI Now Institute', type: 'org' },
  { re: /\b(European Union|EU AI Act|European Commission)\b/i, name: 'European Union', type: 'org' },
  { re: /\b(White House)\b/i, name: 'White House', type: 'org' },
  { re: /\b(SEC)\b/i, name: 'SEC', type: 'org' },
  { re: /\b(FTC)\b/i, name: 'FTC', type: 'org' },
  { re: /\b(NIST)\b/i, name: 'NIST', type: 'org' },
  { re: /\b(OECD)\b/i, name: 'OECD', type: 'org' },
  { re: /\b(IMF)\b/i, name: 'IMF', type: 'org' },
  { re: /\b(WEF|World Economic Forum)\b/i, name: 'World Economic Forum', type: 'org' },
  // Products / models
  { re: /\b(ChatGPT)\b/i, name: 'ChatGPT', type: 'product' },
  { re: /\b(GPT-?[345](?:\.\d)?)\b/i, name: 'GPT', type: 'product' },
  { re: /\b(Claude(?: \d(?:\.\d)?)?)\b/i, name: 'Claude', type: 'product' },
  { re: /\b(Gemini)\b/i, name: 'Gemini', type: 'product' },
  { re: /\b(Llama|LLaMA)\b/i, name: 'Llama', type: 'product' },
  { re: /\b(Copilot|GitHub Copilot)\b/i, name: 'Copilot', type: 'product' },
  { re: /\b(Cursor)\b/i, name: 'Cursor', type: 'product' },
  // Concepts (the channel's vocabulary)
  { re: /\b(AGI|artificial general intelligence)\b/i, name: 'AGI', type: 'concept' },
  { re: /\b(automation)\b/i, name: 'automation', type: 'concept' },
  { re: /\b(augmentation)\b/i, name: 'augmentation', type: 'concept' },
  { re: /\b(reskilling|upskilling)\b/i, name: 'reskilling', type: 'concept' },
  { re: /\b(alignment)\b/i, name: 'alignment', type: 'concept' },
  { re: /\b(governance)\b/i, name: 'governance', type: 'concept' },
  { re: /\b(regulation)\b/i, name: 'regulation', type: 'concept' },
  { re: /\b(open[- ]source)\b/i, name: 'open source', type: 'concept' },
  { re: /\b(safety)\b/i, name: 'AI safety', type: 'concept' },
  { re: /\b(scaling laws?)\b/i, name: 'scaling laws', type: 'concept' },
  { re: /\b(productivity)\b/i, name: 'productivity', type: 'concept' },
  { re: /\b(monopoly|monopolies|antitrust)\b/i, name: 'monopoly/antitrust', type: 'concept' },
  { re: /\b(inequality)\b/i, name: 'inequality', type: 'concept' },
  { re: /\b(layoff|layoffs|job displacement)\b/i, name: 'layoffs/displacement', type: 'concept' },
  { re: /\b(knowledge work(?:er)?s?)\b/i, name: 'knowledge work', type: 'concept' },
  { re: /\b(entry[- ]level)\b/i, name: 'entry-level jobs', type: 'concept' },
  { re: /\b(software engineer(?:s|ing)?)\b/i, name: 'software engineering', type: 'concept' },
  { re: /\b(creative industries|creators?)\b/i, name: 'creative work', type: 'concept' },
  { re: /\b(data center(?:s)?)\b/i, name: 'data centers', type: 'concept' },
  { re: /\b(compute)\b/i, name: 'compute', type: 'concept' },
  { re: /\b(brain[- ]computer interface|BCI)\b/i, name: 'BCI', type: 'concept' },
  { re: /\b(deepfake(?:s)?)\b/i, name: 'deepfakes', type: 'concept' },
  { re: /\b(election(?:s)?)\b/i, name: 'elections', type: 'concept' },
];

// Topic clusters — coarser than entities. Keyword bags scored against page text.
const TOPICS: Array<{ id: string; label: string; kws: string[] }> = [
  { id: 'entry-level-squeeze',   label: 'Entry-level job squeeze', kws: ['entry-level', 'junior', 'graduate', 'recent grad', 'first job', 'no longer hiring'] },
  { id: 'automation-vs-augment', label: 'Automation vs augmentation', kws: ['automate', 'augment', 'replace', 'task automation', 'human-in-the-loop'] },
  { id: 'power-concentration',   label: 'Power & market concentration', kws: ['concentrat', 'monopoly', 'antitrust', 'data center', 'compute moat', 'big tech'] },
  { id: 'governance-regulation', label: 'AI governance & regulation', kws: ['governance', 'regulat', 'policy', 'eu ai act', 'executive order', 'liability'] },
  { id: 'jobs-displacement',     label: 'Jobs & displacement', kws: ['layoff', 'displacement', 'unemploy', 'labor market', 'wage'] },
  { id: 'safety-risk',           label: 'AI safety & risk', kws: ['safety', 'alignment', 'existential', 'misuse', 'misinformation', 'biosecurity'] },
  { id: 'creative-work',         label: 'Creative work & copyright', kws: ['creative', 'artist', 'musician', 'copyright', 'training data'] },
  { id: 'productivity',          label: 'Productivity & enterprise adoption', kws: ['productivity', 'adoption', 'roi', 'workflow', 'enterprise'] },
  { id: 'education-future',      label: 'Education & learning', kws: ['education', 'classroom', 'student', 'teacher', 'curriculum'] },
  { id: 'meaning-work',          label: 'Meaning, identity & work', kws: ['meaning', 'identity', 'purpose', 'dignity', 'craft'] },
  { id: 'open-source-models',    label: 'Open-source models', kws: ['open source', 'open-weights', 'llama', 'mistral', 'huggingface'] },
  { id: 'agents',                label: 'AI agents & autonomy', kws: ['agentic', 'agent', 'autonomous', 'tool use', 'multi-agent'] },
];

const LENSES = ['power-control', 'economic-futures', 'meaning-identity', 'strategic-choices', 'social-consequences'] as const;

// ─────────────────────────── DB schema ───────────────────────────
function openDb(): Database {
  const db = new Database(DB_PATH);
  db.exec('PRAGMA journal_mode=WAL;');
  db.exec(`
    CREATE TABLE IF NOT EXISTS items (
      id INTEGER PRIMARY KEY,
      path TEXT UNIQUE NOT NULL,        -- relative to wiki/
      category TEXT NOT NULL,
      tier TEXT,
      title TEXT,
      author TEXT,
      source TEXT,
      url TEXT,
      doi TEXT,
      access TEXT,
      needs_fulltext INTEGER DEFAULT 0,
      published TEXT,
      indexed TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_items_tier ON items(tier);
    CREATE INDEX IF NOT EXISTS idx_items_category ON items(category);

    CREATE TABLE IF NOT EXISTS lenses_items (
      item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
      lens TEXT NOT NULL,
      PRIMARY KEY (item_id, lens)
    );
    CREATE INDEX IF NOT EXISTS idx_lenses ON lenses_items(lens);

    CREATE TABLE IF NOT EXISTS entities (
      id INTEGER PRIMARY KEY,
      name TEXT UNIQUE NOT NULL,
      type TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS entity_mentions (
      item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
      entity_id INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
      count INTEGER NOT NULL DEFAULT 1,
      PRIMARY KEY (item_id, entity_id)
    );
    CREATE INDEX IF NOT EXISTS idx_mentions_entity ON entity_mentions(entity_id);

    CREATE TABLE IF NOT EXISTS topics (
      id TEXT PRIMARY KEY,
      label TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS topic_items (
      topic_id TEXT NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
      item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
      score REAL NOT NULL,                -- normalized 0..1
      PRIMARY KEY (topic_id, item_id)
    );
    CREATE INDEX IF NOT EXISTS idx_topic_items_topic ON topic_items(topic_id, score DESC);

    CREATE TABLE IF NOT EXISTS coocc_entity (
      a INTEGER NOT NULL,
      b INTEGER NOT NULL,
      count INTEGER NOT NULL DEFAULT 1,
      PRIMARY KEY (a, b)
    );

    CREATE TABLE IF NOT EXISTS graph_meta (
      key TEXT PRIMARY KEY,
      value TEXT NOT NULL
    );
  `);
  return db;
}

// ─────────────────────────── helpers ───────────────────────────
function parseFrontmatter(content: string): { fm: Record<string, any>; body: string } {
  const m = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!m) return { fm: {}, body: content };
  const fm: Record<string, any> = {};
  for (const line of m[1]!.split('\n')) {
    const kv = line.match(/^(\w+):\s*(.*)$/);
    if (!kv) continue;
    const key = kv[1]!, val = kv[2]!.trim();
    if (val.startsWith('[') && val.endsWith(']')) fm[key] = val.slice(1, -1).split(',').map((s) => s.trim()).filter(Boolean);
    else if (/^".*"$/.test(val)) fm[key] = val.slice(1, -1);
    else fm[key] = val;
  }
  return { fm, body: m[2] || '' };
}
function walkMd(dir: string): string[] {
  const out: string[] = [];
  const rec = (d: string) => {
    let entries: string[] = [];
    try { entries = readdirSyncRetry(d); } catch { return; }
    for (const e of entries) {
      const p = join(d, e); const s = statSync(p);
      if (s.isDirectory()) rec(p);
      else if (e.endsWith('.md') && !META_SKIP.has(e)) out.push(p);
    }
  };
  rec(dir); return out;
}
function ensureEntity(db: Database, name: string, type: string): number {
  const row = db.query<{ id: number }, [string]>('SELECT id FROM entities WHERE name = ?').get(name);
  if (row) return row.id;
  const r = db.run('INSERT INTO entities (name, type) VALUES (?, ?)', [name, type]);
  return Number(r.lastInsertRowid);
}

// ─────────────────────────── BUILD ───────────────────────────
export function buildGraph() {
  const db = openDb();
  const wikiDir = join(WIKI_ROOT, 'wiki');
  const files = walkMd(wikiDir);
  console.log(`📚 Building graph over ${files.length} pages…`);

  // Seed topics
  const insTopic = db.prepare('INSERT OR REPLACE INTO topics (id, label) VALUES (?, ?)');
  for (const t of TOPICS) insTopic.run(t.id, t.label);

  // Ensure the originals columns exist (migration was additive and may not
  // have been applied on a fresh DB clone).
  const cols = db.query<{ name: string }, []>('PRAGMA table_info(items)').all();
  const colNames = new Set(cols.map((c) => c.name));
  if (!colNames.has('original_path')) db.exec('ALTER TABLE items ADD COLUMN original_path TEXT');
  if (!colNames.has('original_kind')) db.exec('ALTER TABLE items ADD COLUMN original_kind TEXT');

  // Preserve item ids across rebuilds so foreign keys from notable_quotes
  // (and any future quote-like tables) stay valid when new wiki pages are
  // added. Snapshot existing path -> id mapping; re-INSERT with the saved id
  // when a path persists; INSERT without id (auto-assign) for new paths.
  const idMap = new Map<string, number>();
  for (const r of db.query<{ id: number; path: string }, []>('SELECT id, path FROM items').all()) {
    idMap.set(r.path, r.id);
  }
  const maxId = db.query<{ m: number | null }, []>('SELECT MAX(id) AS m FROM items').get()?.m ?? 0;
  let nextNewId = (maxId ?? 0) + 1;

  // Reset link tables (idempotent build). NOTE: items is wiped LAST so the
  // idMap snapshot above is unaffected, and notable_quotes is intentionally
  // NOT touched here — its rows survive the rebuild via the preserved ids.
  for (const t of ['topic_items', 'entity_mentions', 'coocc_entity', 'lenses_items', 'items']) db.exec(`DELETE FROM ${t};`);

  const insItem = db.prepare(`INSERT INTO items
    (id, path, category, tier, title, author, source, url, doi, access, needs_fulltext, published, indexed, original_path, original_kind)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`);
  const insLens = db.prepare('INSERT OR IGNORE INTO lenses_items (item_id, lens) VALUES (?, ?)');
  const insMention = db.prepare('INSERT OR REPLACE INTO entity_mentions (item_id, entity_id, count) VALUES (?, ?, ?)');
  const insTopicItem = db.prepare('INSERT OR REPLACE INTO topic_items (topic_id, item_id, score) VALUES (?, ?, ?)');
  const insCo = db.prepare(`INSERT INTO coocc_entity (a, b, count) VALUES (?, ?, 1)
                            ON CONFLICT(a, b) DO UPDATE SET count = count + 1`);

  let scanned = 0;
  db.exec('BEGIN');
  for (const abs of files) {
    const rel = abs.replace(wikiDir + '/', '');
    const content = readFileSyncRetry(abs, 'utf-8');
    const { fm, body } = parseFrontmatter(content);
    const cat = rel.split('/')[0] || 'uncategorized';
    const needsFt = String(fm.needs_fulltext || '').toLowerCase() === 'true' ? 1 : 0;
    // Auto-discover canonical original artifact: originals/<rel-without-.md>.<ext>.
    // PDF preferred (selectable text, deterministic bboxes); PNG fallback.
    const wikiRoot = wikiDir.replace(/\/wiki$/, '');
    const stem = rel.replace(/\.md$/i, '');
    let origPath: string | null = null;
    let origKind: string | null = null;
    for (const ext of ['pdf', 'png'] as const) {
      const candidate = `originals/${stem}.${ext}`;
      if (existsSync(`${wikiRoot}/${candidate}`)) { origPath = candidate; origKind = ext; break; }
    }
    // Resolve a stable id for this path: reuse the prior id if we've seen it
    // before, otherwise allocate a fresh one above the previous max. This keeps
    // notable_quotes (and any future FK consumers) linked across rebuilds.
    const itemId = idMap.get(rel) ?? nextNewId++;
    const bindings: (string | number | null)[] = [
      itemId,
      rel, cat, fm.tier || '', fm.title || rel, fm.author || '', fm.source || '',
      fm.url || '', fm.doi || '', fm.access || '', needsFt, fm.published || '', fm.indexed || '',
      origPath, origKind,
    ];
    // Coerce any stray non-binding values (e.g. arrays from YAML lens fields
    // when the file lacks proper string quoting) to safe strings.
    for (let i = 0; i < bindings.length; i++) {
      const v = bindings[i];
      if (v !== null && typeof v !== 'string' && typeof v !== 'number') {
        bindings[i] = JSON.stringify(v);
      }
    }
    insItem.run(bindings);

    for (const l of (fm.thesis_lens || []) as string[]) if (LENSES.includes(l as any)) insLens.run(itemId, l);

    // Entities
    const text = `${fm.title || ''}\n${body}`;
    const hits: number[] = [];
    for (const ent of ENTITIES) {
      const matches = text.match(new RegExp(ent.re.source, 'gi'));
      if (matches && matches.length) {
        const eid = ensureEntity(db, ent.name, ent.type);
        insMention.run(itemId, eid, matches.length);
        hits.push(eid);
      }
    }
    // Co-occurrence (entity-entity within the same item, undirected, a<b)
    const u = [...new Set(hits)].sort((a, b) => a - b);
    for (let i = 0; i < u.length; i++) for (let j = i + 1; j < u.length; j++) insCo.run(u[i]!, u[j]!);

    // Topics — normalized score in [0,1]
    const lower = text.toLowerCase();
    for (const t of TOPICS) {
      let hits = 0;
      for (const kw of t.kws) {
        const m = lower.match(new RegExp(`\\b${kw.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&')}\\b`, 'gi'));
        if (m) hits += m.length;
      }
      if (hits > 0) insTopicItem.run(t.id, itemId, Math.min(hits / 6, 1));
    }
    scanned++;
  }
  db.exec('COMMIT');

  db.prepare('INSERT OR REPLACE INTO graph_meta (key, value) VALUES (?, ?)').run('built_at', new Date().toISOString());
  db.prepare('INSERT OR REPLACE INTO graph_meta (key, value) VALUES (?, ?)').run('item_count', String(scanned));

  console.log(`✓ items=${scanned}`);
  const stats = getStats(db);
  console.log(`✓ entities=${stats.entities} mentions=${stats.mentions} topics=${stats.topics} topic_items=${stats.topicItems} cooccs=${stats.cooccs}`);
  db.close();
}

// ─────────────────────────── QUERIES ───────────────────────────
function withDb<T>(fn: (db: Database) => T): T {
  const db = openDb(); try { return fn(db); } finally { db.close(); }
}

export function getStats(db?: Database) {
  const close = !db; const _db = db || openDb();
  const num = (sql: string) => (_db.query(sql).get() as any)?.n || 0;
  const out = {
    items: num('SELECT COUNT(*) AS n FROM items'),
    entities: num('SELECT COUNT(*) AS n FROM entities'),
    mentions: num('SELECT COUNT(*) AS n FROM entity_mentions'),
    topics: num('SELECT COUNT(*) AS n FROM topics'),
    topicItems: num('SELECT COUNT(*) AS n FROM topic_items'),
    cooccs: num('SELECT COUNT(*) AS n FROM coocc_entity'),
  };
  if (close) _db.close();
  return out;
}

export function topEntities(limit = 25) {
  return withDb((db) => db.query(`
    SELECT e.name, e.type, COUNT(DISTINCT em.item_id) AS docs, SUM(em.count) AS mentions
    FROM entities e JOIN entity_mentions em ON em.entity_id = e.id
    GROUP BY e.id ORDER BY docs DESC, mentions DESC LIMIT ?`).all(limit) as any[]);
}

export function byEntity(name: string, limit = 25) {
  return withDb((db) => db.query(`
    SELECT i.path, i.title, i.category, i.tier, i.url, i.doi, em.count AS mentions
    FROM items i JOIN entity_mentions em ON em.item_id = i.id
    JOIN entities e ON e.id = em.entity_id
    WHERE e.name LIKE ? COLLATE NOCASE
    ORDER BY i.tier ASC, em.count DESC LIMIT ?`).all(`%${name}%`, limit) as any[]);
}

export function byTopic(topic: string, opts: { tier?: string; limit?: number } = {}) {
  return withDb((db) => {
    const where = opts.tier ? 'AND i.tier = ?' : '';
    const params: any[] = [`%${topic}%`];
    if (opts.tier) params.push(opts.tier);
    params.push(opts.limit ?? 25);
    return db.query(`
      SELECT i.path, i.title, i.category, i.tier, i.url, i.doi, ti.score
      FROM items i JOIN topic_items ti ON ti.item_id = i.id
      JOIN topics t ON t.id = ti.topic_id
      WHERE (t.id LIKE ? OR t.label LIKE ?) ${where}
      ORDER BY ti.score DESC, i.tier ASC LIMIT ?`)
      .all(params[0], params[0], ...params.slice(1)) as any[];
  });
}

export function byLens(lens: string, opts: { tier?: string; limit?: number } = {}) {
  return withDb((db) => {
    const where = opts.tier ? 'AND i.tier = ?' : '';
    const params: any[] = [lens];
    if (opts.tier) params.push(opts.tier);
    params.push(opts.limit ?? 25);
    return db.query(`
      SELECT i.path, i.title, i.category, i.tier, i.url, i.doi
      FROM items i JOIN lenses_items li ON li.item_id = i.id
      WHERE li.lens = ? ${where} ORDER BY i.tier ASC LIMIT ?`).all(...params) as any[];
  });
}

export function relatedEntities(name: string, limit = 15) {
  return withDb((db) => db.query(`
    SELECT e2.name, e2.type, c.count
    FROM entities e1
    JOIN coocc_entity c ON (c.a = e1.id OR c.b = e1.id)
    JOIN entities e2 ON e2.id = CASE WHEN c.a = e1.id THEN c.b ELSE c.a END
    WHERE e1.name LIKE ? COLLATE NOCASE
    ORDER BY c.count DESC LIMIT ?`).all(`%${name}%`, limit) as any[]);
}

// Show-bible "promote to episode" rule: hard number (Tier 1) + decision/power
// angle (Tier 2 or 3) + trade-off/precedent (Tier 1.5 or 4) — all sharing a topic.
export function episodeCandidates(limit = 10) {
  return withDb((db) => db.query(`
    SELECT t.id AS topic, t.label,
           COUNT(DISTINCT CASE WHEN i.tier='1' THEN i.id END)   AS t1,
           COUNT(DISTINCT CASE WHEN i.tier IN ('2','3') THEN i.id END) AS t2_3,
           COUNT(DISTINCT CASE WHEN i.tier IN ('1.5','4') THEN i.id END) AS t15_4,
           COUNT(DISTINCT i.id) AS total
    FROM topics t
    JOIN topic_items ti ON ti.topic_id = t.id
    JOIN items i ON i.id = ti.item_id
    GROUP BY t.id
    HAVING t1 >= 1 AND t2_3 >= 1 AND t15_4 >= 1
    ORDER BY total DESC LIMIT ?`).all(limit) as any[]);
}

// ─────────────────────────── CLI ───────────────────────────
if (import.meta.main) {
  const [cmd, ...rest] = process.argv.slice(2);
  const argFlag = (k: string) => { const i = rest.indexOf(k); return i >= 0 ? rest[i + 1] : undefined; };
  const trunc = (s: any, n: number) => { const str = String(s ?? ''); return str.length > n ? str.slice(0, n - 1) + '…' : str.padEnd(n); };
  const out = (rows: any[]) => {
    if (!rows.length) return console.log('  (no results)');
    const cols = Object.keys(rows[0]);
    const widths = cols.map((c) => Math.min(Math.max(c.length, ...rows.map((r) => String(r[c] ?? '').length)), c === 'path' || c === 'url' || c === 'title' || c === 'label' ? 60 : 18));
    console.log('  ' + cols.map((c, i) => trunc(c, widths[i]!)).join(' │ '));
    console.log('  ' + widths.map((w) => '─'.repeat(w)).join('─┼─'));
    for (const r of rows) console.log('  ' + cols.map((c, i) => trunc(r[c], widths[i]!)).join(' │ '));
  };

  switch (cmd) {
    case 'build': buildGraph(); break;
    case 'stats': console.log(getStats()); break;
    case 'entity': out(byEntity(rest.filter((a) => !a.startsWith('-')).join(' ') || '')); break;
    case 'related': out(relatedEntities(rest.filter((a) => !a.startsWith('-')).join(' ') || '')); break;
    case 'topic': out(byTopic(rest.filter((a) => !a.startsWith('-')).join(' ') || '', { tier: argFlag('--tier') })); break;
    case 'lens': out(byLens(rest[0] || 'power-control', { tier: argFlag('--tier') })); break;
    case 'top': out(topEntities(Number(rest[0]) || 25)); break;
    case 'episodes': out(episodeCandidates(Number(rest[0]) || 10)); break;
    default:
      console.log(`Usage:
  bun run src/fetchers/graph.ts build
  bun run src/fetchers/graph.ts stats
  bun run src/fetchers/graph.ts top [N]
  bun run src/fetchers/graph.ts entity <name>
  bun run src/fetchers/graph.ts related <name>
  bun run src/fetchers/graph.ts topic <topic> [--tier 1.5]
  bun run src/fetchers/graph.ts lens <lens> [--tier 1.5]
  bun run src/fetchers/graph.ts episodes [N]`);
  }
}

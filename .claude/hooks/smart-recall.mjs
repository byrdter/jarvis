#!/usr/bin/env node
/**
 * smart-recall.mjs
 *
 * Minimal MCP stdio client that talks to claude-mem's mcp-search server and
 * runs query-aware memory recall using the documented 3-step workflow:
 *
 *   1. search(query)              → observation IDs + previews (fast, indexed)
 *   2. get_observations([top IDs]) → full text for the most relevant hits
 *
 * Note: this does NOT use claude-mem's `smart_search` tool — that one is a
 * tree-sitter codebase symbol search, not a memory search. The file is named
 * smart-recall.* (for "smart, query-aware recall") not because it calls
 * smart_search.
 *
 * Usage:
 *   node smart-recall.mjs "<query string>" [limit]
 *
 * Output: prints a formatted markdown block to stdout. Exits non-zero on error.
 *
 * Part of JARVIS Memory Fix #1 (beads: jarvis-yz9). See .claude/hooks/smart-recall.sh
 * for the orchestrating wrapper invoked by the UserPromptSubmit hook.
 */

import { spawn } from "node:child_process";
import { existsSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

const HOME = homedir();
const TIMEOUT_MS = Number(process.env.SMART_RECALL_TIMEOUT_MS) || 45_000;

function resolvePluginRoot() {
  if (process.env.CLAUDE_PLUGIN_ROOT) return process.env.CLAUDE_PLUGIN_ROOT;
  const cacheDir = join(HOME, ".claude/plugins/cache/thedotmack/claude-mem");
  if (!existsSync(cacheDir)) {
    throw new Error(`claude-mem cache not found at ${cacheDir}`);
  }
  // Pick the highest semver version subdirectory.
  const versions = readdirSync(cacheDir)
    .filter((v) => /^\d/.test(v))
    .sort((a, b) =>
      a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" })
    );
  if (versions.length === 0) {
    throw new Error(`No version directories under ${cacheDir}`);
  }
  return join(cacheDir, versions[versions.length - 1]);
}

function resolveBun() {
  if (process.env.BUN_PATH && existsSync(process.env.BUN_PATH)) {
    return process.env.BUN_PATH;
  }
  const candidates = [
    join(HOME, ".bun/bin/bun"),
    "/opt/homebrew/bin/bun",
    "/usr/local/bin/bun",
  ];
  for (const c of candidates) {
    if (existsSync(c)) return c;
  }
  return "bun"; // fall back to PATH
}

async function callMcp(query, limit) {
  const pluginRoot = resolvePluginRoot();
  const serverScript = join(pluginRoot, "scripts/mcp-server.cjs");
  if (!existsSync(serverScript)) {
    throw new Error(`mcp-server.cjs not found at ${serverScript}`);
  }
  const bun = resolveBun();

  const child = spawn(bun, [serverScript], {
    stdio: ["pipe", "pipe", "pipe"],
    env: { ...process.env, CLAUDE_PLUGIN_ROOT: pluginRoot },
  });

  let stderrBuf = "";
  child.stderr.on("data", (d) => {
    stderrBuf += d.toString();
  });

  // Line-delimited JSON-RPC 2.0 reader.
  let buffer = "";
  const pending = new Map(); // id -> {resolve, reject}
  child.stdout.on("data", (chunk) => {
    buffer += chunk.toString();
    let idx;
    while ((idx = buffer.indexOf("\n")) !== -1) {
      const line = buffer.slice(0, idx).trim();
      buffer = buffer.slice(idx + 1);
      if (!line) continue;
      let msg;
      try {
        msg = JSON.parse(line);
      } catch {
        continue;
      }
      if (msg.id !== undefined && pending.has(msg.id)) {
        const { resolve, reject } = pending.get(msg.id);
        pending.delete(msg.id);
        if (msg.error) reject(new Error(JSON.stringify(msg.error)));
        else resolve(msg.result);
      }
    }
  });

  child.on("error", (err) => {
    for (const { reject } of pending.values()) reject(err);
  });

  function send(payload) {
    child.stdin.write(JSON.stringify(payload) + "\n");
  }
  function request(id, method, params) {
    return new Promise((resolve, reject) => {
      pending.set(id, { resolve, reject });
      send({ jsonrpc: "2.0", id, method, params });
    });
  }
  function notify(method, params) {
    send({ jsonrpc: "2.0", method, params });
  }

  const watchdog = setTimeout(() => {
    child.kill("SIGKILL");
  }, TIMEOUT_MS);

  const dbg = (m) => {
    if (process.env.DEBUG_SMART_RECALL) process.stderr.write(`[smart-recall] ${m}\n`);
  };

  try {
    dbg("spawned server, sending initialize");
    // 1. initialize
    await request(1, "initialize", {
      protocolVersion: "2024-11-05",
      capabilities: {},
      clientInfo: { name: "jarvis-smart-recall", version: "0.1.0" },
    });
    dbg("initialize complete, sending initialized notification");
    notify("notifications/initialized", {});

    // ---- Step 1: search the observation index for relevant IDs ------------
    dbg(`calling search(query="${query.slice(0, 60)}...", limit=${limit})`);
    const searchRes = await request(2, "tools/call", {
      name: "search",
      arguments: { query, limit, orderBy: "relevance" },
    });
    const searchText = (searchRes?.content || [])
      .filter((b) => b.type === "text")
      .map((b) => b.text)
      .join("\n\n");
    dbg(`search returned ${searchText.length} chars`);

    if (!searchText) {
      return "(no observations matched the query)";
    }

    // Parse observation IDs. claude-mem's search emits IDs in a markdown
    // table as `| #21 |`, so the universal anchor is `#NNN` with a digit
    // boundary. Also accept `ID: NNN` and `"id": NNN` as fallbacks.
    const idSet = new Set();
    for (const m of searchText.matchAll(/#(\d{1,7})\b/g)) {
      idSet.add(Number(m[1]));
    }
    for (const m of searchText.matchAll(/\bID[:=\s]+(\d{1,7})\b/gi)) {
      idSet.add(Number(m[1]));
    }
    for (const m of searchText.matchAll(/"id"\s*:\s*(\d{1,7})/g)) {
      idSet.add(Number(m[1]));
    }
    // Preserve insertion order (which mirrors relevance ranking from search).
    const topIds = [...idSet].slice(0, Math.min(limit, 5));
    dbg(`extracted ${topIds.length} observation IDs: ${topIds.join(",")}`);

    let detailsBlock = "";
    if (topIds.length > 0) {
      // ---- Step 2: fetch full observations for the top IDs ----------------
      const detailsRes = await request(3, "tools/call", {
        name: "get_observations",
        arguments: { ids: topIds },
      });
      const rawText = (detailsRes?.content || [])
        .filter((b) => b.type === "text")
        .map((b) => b.text)
        .join("\n\n");
      dbg(`get_observations returned ${rawText.length} chars raw`);

      // Trim DB rows down to just useful fields. claude-mem returns a JSON
      // array; embedded JSON may be a string or have an explanatory preamble.
      const jsonStart = rawText.indexOf("[");
      const jsonEnd = rawText.lastIndexOf("]");
      let observations = [];
      if (jsonStart !== -1 && jsonEnd > jsonStart) {
        try {
          observations = JSON.parse(rawText.slice(jsonStart, jsonEnd + 1));
        } catch (e) {
          dbg(`failed to parse observation JSON: ${e.message}`);
        }
      }

      if (observations.length > 0) {
        const formatted = observations.map((o) => formatObservation(o)).join("\n\n---\n\n");
        detailsBlock = formatted;
      } else {
        // Fall back to raw text if parsing failed — better than nothing.
        detailsBlock = rawText.trim();
      }
      dbg(`formatted details: ${detailsBlock.length} chars`);
    }

    // Format the combined output.
    let out = `## Search index (relevance-ranked)\n\n${searchText.trim()}`;
    if (detailsBlock) {
      out += `\n\n## Top observation details\n\n${detailsBlock}`;
    }
    return out;
  } finally {
    clearTimeout(watchdog);
    try {
      child.stdin.end();
    } catch { /* noop */ }
    child.kill();
    if (process.env.DEBUG_SMART_RECALL && stderrBuf) {
      process.stderr.write(`[smart-recall mcp stderr]\n${stderrBuf}\n`);
    }
  }
}

/** Render one observation row as compact markdown. */
function formatObservation(o) {
  const date = o.created_at ? String(o.created_at).slice(0, 10) : "";
  const project = o.project || "";
  const type = o.type || "";
  const title = o.title || "(untitled)";
  const subtitle = o.subtitle || "";

  let facts = [];
  if (o.facts) {
    try {
      facts = typeof o.facts === "string" ? JSON.parse(o.facts) : o.facts;
    } catch { facts = []; }
  }
  let concepts = [];
  if (o.concepts) {
    try {
      concepts = typeof o.concepts === "string" ? JSON.parse(o.concepts) : o.concepts;
    } catch { concepts = []; }
  }
  let filesRead = [];
  if (o.files_read) {
    try {
      filesRead = typeof o.files_read === "string" ? JSON.parse(o.files_read) : o.files_read;
    } catch { filesRead = []; }
  }

  const header = `### #${o.id} — ${title}`;
  const metaParts = [date, project, type].filter(Boolean);
  const meta = metaParts.length ? `*${metaParts.join(" · ")}*` : "";
  const sub = subtitle ? subtitle : "";
  const factsBlock = facts.length
    ? "**Facts:**\n" + facts.map((f) => `- ${f}`).join("\n")
    : "";
  const narrative = o.narrative ? `**Narrative:** ${o.narrative}` : "";
  const conceptsLine = concepts.length ? `**Concepts:** ${concepts.join(", ")}` : "";
  const filesLine = filesRead.length
    ? `**Files referenced:** ${filesRead.slice(0, 5).join(", ")}`
    : "";

  return [header, meta, sub, factsBlock, narrative, conceptsLine, filesLine]
    .filter(Boolean)
    .join("\n\n");
}

async function main() {
  const query = process.argv[2];
  const limit = Number.parseInt(process.argv[3] || "7", 10);
  if (!query || query.length < 3) {
    process.stderr.write("smart-recall: query missing or too short, skipping\n");
    process.exit(2);
  }
  try {
    const out = await callMcp(query, limit);
    process.stdout.write(out);
  } catch (err) {
    process.stderr.write(`smart-recall error: ${err.message}\n`);
    process.exit(1);
  }
}

main();

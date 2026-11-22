# Brain Studio

The face of JARVIS: `jarvis-brain` drawn as a 3D galaxy you can talk to. Ask a question by voice or
text, JARVIS answers out loud from your notes only, and the camera flies to the note the answer came from.

```
python3 infra/laptop/brain-studio/server.py        # then open http://127.0.0.1:4700 in Chrome
```

(Or `preview_start brain-studio` from a Claude Code session; the config is in `.claude/launch.json`.)

## How it works

| Piece | File | What it does |
|---|---|---|
| Indexer | `build.py` | Types every brain note by folder (Core, People, Projects, Concepts, Tools, Models, Lab, Daily journal, Session memory, Sources…), links them through `[[wikilinks]]`, relative `.md` links and mentions of curated page titles, and adds one hub star per type. Writes `viewer/graph-data.js` (gitignored: it holds private excerpts). |
| Server | `server.py` | Serves only `viewer/` on 127.0.0.1. `POST /api/chat/stream` finds the closest notes with `brain-ask.py`'s hybrid search (Ollama embeddings, ~0.3 s; keywords if Ollama is off), then streams the answer from ONE long-lived `claude` session on your plan (stream-json in and out, Sonnet, low effort, no tools, no hooks, nothing saved), or from Ollama when the local brain is on. The model writes the spoken answer first and one `[[meta]]` line last (sources, about-notes, action), so the page speaks sentence by sentence while it is still being written. The persona is one block at the top of the file. |
| Viewer | `viewer/index.html` | 3d-force-graph + bloom + starfield; the brain grows star by star; click a star for the inspector (summary, excerpt, Read full note, connections); type filter; search; deep links `#n=Ray Fu`. |

**The rules that make the demo honest** (from Zubair's Fable 5.2 Workshop pack, Prompts 02–03):
- Small talk ("good morning") holds the galaxy still. The server decides `about_notes` before the viewer
  moves the camera.
- An answer from 1–3 notes flies to the top note and lights its neighbors and the other sources. Four or
  more light the whole cluster instead, because flying to one note out of six misrepresents the answer.
- Only `focusNode` / `lightCluster` / `clearFocus` move the camera or change what is lit.
- Only `speak()` makes sound, and it checks `?mute=1` itself, so a muted tab can never talk.

## The orb

Bottom right (top right on a phone), `viewer/orb.js`, plain canvas. The core is JARVIS gold; the aura is
the color of the brain answering (Claude `#d97757`, local `#4ade80`, from the brain palette). It
breathes when idle, ripples with the **real** mic level while listening, spins with orbiting satellites
while thinking, and pulses on every spoken word (word-boundary events; a soft beat if the voice sends
none). The caption under it says which engine and what it's doing ("Reading the brain · Claude",
"From 3 notes · 4.4 s"). Click it to talk.

**Switch brains out loud:** say it however you like ("can you switch over to the local brain", "go
local", "use Claude", "back to Claude"): a short request with a switch word and an engine name. Local
answers with `qwen3.5:9b` on Ollama (nothing leaves the Mac, ~2–4 s once warm). A *question* about the
engine ("which brain are you using?") goes to the model instead, and every prompt tells it where it is
running and on which engine (`where_you_are()` in `server.py`), with past answers labeled by engine.
Override with `BRAIN_STUDIO_ENGINE`, `BRAIN_STUDIO_LOCAL_MODEL` (e.g. `qwen3.8:27b`: smarter, slower).

## Voice

- **Speaking:** JARVIS's own voice, Kyutai Pocket TTS running on this Mac (`voice/voice.py`, free, nothing
  leaves the machine). One-time setup: `infra/laptop/brain-studio/voice/setup.sh` (it needs Python 3.12,
  so it gets its own environment in `~/.local/share/jarvis/brain-studio/voice-venv`). After that,
  `server.py` starts the voice by itself, restarts it if it dies, and the page plays each sentence as soon
  as it's written, fetching the next while one plays. The first chunk may end at a comma so a long
  opening sentence doesn't hold the first word back. Measured 2026-11-22: a sentence renders in ~0.25 s;
  first audio 1.1–2.3 s after a typed question. The orb follows the real loudness of the voice.
  - "use the Javert voice" (or Charles, Paul, Anna…) switches; "what voices do you have" lists them;
    `BRAIN_STUDIO_VOICE` sets the default (Marius). Licenses: Marius and Javert are CC0, the VCTK voices
    (Charles, Paul, Anna, Vera, Fantine, Eponine, Azelma) are CC-BY 4.0, Cosette is non-commercial only.
    A path to a 5–20 s WAV clip clones that voice; only use a voice you own or have permission to use.
  - "use the browser voice" / "use your local voice" switch between the two (remembered per browser). If
    the local voice isn't running, the page uses the browser's best American English voice instead.
- **Listening:** click the mic (Chrome). Recognition finalizes on every pause, so the page waits
  `FINISH_MS` (900 ms, top of the script) after the last words before sending; more speech restarts the
  clock. "Stop", "wait" or "quiet" cut JARVIS off instantly. While JARVIS speaks, everything else it
  hears is ignored, so it doesn't answer itself.
- **Remember:** "remember that…", "note to self…", "don't let me forget…", "log this…" or "make a
  note…" saves the rest as a new note in `jarvis-brain/captures/` (a new star is born next to its
  closest notes, pulses, and the camera flies to it) and adds one line to today's `daily/` log, which
  the nightly reflection promotes into MEMORY.md / USER.md. It's searchable in the very next question,
  and `brain-sync.sh` pushes it so Telegram and the server know it within a minute. The same fact twice
  in a day is kept once. A failed save is always said out loud. Server: `capture()`; viewer: `addNote()`.
- **Voice routes** (checked before the brain): "show me Ray Fu" / "go to Ollama" (flies there only if a
  note really matches), "zoom out" / "reset", "stop rotating" / "start rotating", "start over" (forget
  the conversation). Add routes to `ROUTES`, not to the core.

## Test plan

1. Open the page, click once: it says "Hi Terry." The count in the corner is read from the data.
2. Type "Who is Ray Fu?": the camera dives to Ray Fu, the inspector opens, the answer is spoken.
3. Type "Good morning": a warm reply, and the galaxy does not move.
4. Click the mic and say "what do we know about… [pause] …agent harnesses": the pause must not cut
   you off. If it does, raise `FINISH_MS`; tune it after a day of real use, not in one sitting.
5. While it answers, say "stop": it goes quiet at once.
6. Say "remember that the finish window should be 900 milliseconds": a new star is born, then ask "how
   long should the finish window be?" and it answers from that note.
7. Open `http://127.0.0.1:4700/?mute=1` in a second tab and ask something: the text appears, nothing is heard.

Measured 2026-11-22 on the M5 Pro: first spoken word 0.7–1.3 s after the question on Claude (was 5–6 s when every turn started a new `claude -p`), ~2 s on the local 9B once it is loaded. Why and what's next: `docs/jarvis-2.0/VOICE-CRITIQUE.md`.

Credit: the type-by-folder galaxy and the honesty rules follow Zubair Trabzada's free `brain-map`
(MIT) and his JARVIS prompt packs. This is our own code, written for our brain layout and the Claude plan.

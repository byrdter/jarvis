# Talking to JARVIS: critique of Zubair's build, and what we do instead

> **Summary:** Our Brain Studio is ahead of Zubair's on the brain and behind it on the voice, because we
> copied his *free* voice tier (browser speech both ways), which is his weakest part. Measured on Terry's
> M5 Pro on 2026-11-22: almost all of the ~6 s wait is starting a new `claude` process each turn. A
> persistent session answers in 0.4–0.7 s on the same plan. A local voice (Kyutai Pocket TTS) starts in
> 0.03 s, and local ears (Whisper turbo) transcribe in 0.3 s. Verdict: keep our architecture and replace
> the voice layer in four builds, speed first.

Sources: Zubair's packs in `jarvis-brain/raw/sources/zubair/` (Fable 5.2 Workshop, Run Jarvis Fully
Local, JARVIS prompt pack, Reflexes/Jev), a web survey of 2026 voice-agent tech (links below), and
benchmarks run on this Mac (scripts were in the session scratchpad; numbers below).

## 1. What Zubair actually does

His smoothness is not a secret trick. It is written down in his packs, mostly in the *paid-adjacent*
and *fully local* ones, not in the free workshop we started from:

| Layer | Free workshop (what we copied) | His smooth version |
|---|---|---|
| Brain | Claude through the **API**, streaming | Same, or Ollama `qwen3.5:9b` with `reasoning_effort: none` |
| Voice | Browser `speechSynthesis` | **Cloned voice**: ElevenLabs (paid) or VoiceStudio running CSM-1B on MLX (free); answer split into ~170-character sentence chunks, the next chunk fetched while one plays; kept warm with a "Standing by." render every 10 min |
| Ears | Chrome `webkitSpeechRecognition` (audio goes to Google) | **Whisper on the Mac** (`large-v3-turbo` for commands, `small` for the wake word), loaded once and warmed |
| Turn end | 900 ms finish window | Loudness, 700 ms silence + 900 ms finish window |
| Wake word | none | Transcribe with the small model; keep it only if it starts with "Jarvis" |
| Interrupt | "stop" / "wait" | Same, with a higher threshold while he speaks; headphones suggested |
| Prompt | answer only from notes | **Lean**: a persona of 300 words or fewer, a stable prefix so the model reuses its cache, "one witty sentence plus the facts" |
| Actions | none | **Control tags** the server executes (switch brain, etc.), tested five times for reliability |

His own lessons, in brief: *the slow part was the prompt, not the Mac*; *a local brain can think itself
to death*; *benchmark the voice engine first*; *hearing was the hidden cloud*; *fluency beats first-word
speed*.

## 2. Critique: where his design is weak

1. **The wake word is fake.** Transcribing everything and checking whether the text starts with "Jarvis"
   is exactly why we got "Thomas." A keyword model (openWakeWord ships a pre-trained `hey_jarvis`;
   not yet verified) never transcribes, so it can't mishear.
2. **Turn-taking is a stopwatch.** 700 + 900 ms of silence is both too slow (1.6 s of dead air every
   turn) and too dumb (a thinking pause still cuts you off). 2026 systems listen for *how* you stopped:
   Pipecat **Smart Turn v3.2** (open, 8 MB, ~10–65 ms per check, trained on cafe and office noise) ends
   a turn in ~200–400 ms and waits when you trail off. He uses a hosted model (Jev) only in the Reflexes
   pack.
3. **No real barge-in.** Only "stop" and "wait," plus headphones. Chrome's own echo cancellation
   (`getUserMedia({echoCancellation: true})`) makes "any speech stops him" workable on laptop speakers.
4. **Retrieval is keyword overlap** (top 6 by shared words). Ours is meaning-based (Ollama embeddings +
   rare words), and it already finds Ray Fu from "the ex-Meta guy."
5. **The fast cloud brain costs money.** Every reply goes through the paid API. We can match the speed
   on Terry's plan (section 3).
6. **"Fluency beats first-word speed" was true for his engine, not in general.** CSM renders barely
   faster than real time, so a short first chunk made him stall mid-sentence. Pocket TTS renders ~11×
   real time here, so speaking the first *clause* as soon as it exists doesn't stall.
7. **Memory is a side feature.** "Remember that…" writes a file. Ours also lands in the daily log, gets
   promoted nightly, and is known to Telegram and the server within the hour.

What he gets right that we should keep or adopt: the honesty rules (we have them); stable-prefix prompts
for local models; warm-keeping every model; sentence-safe chunking with prefetch; a preflight that tests
real chains end to end; the Wi-Fi-off drill; control tags (we just added the same idea as `action`).

## 3. Measured on Terry's Mac (M5 Pro, 64 GB), 2026-11-22

| Step | Today | Measured alternative |
|---|---|---|
| Turn end | Chrome finalizes, then 900 ms | Smart Turn: ~0.2–0.4 s (published, not yet measured here) |
| Ears | Chrome → Google, ~0.5–1 s | **mlx-whisper turbo 0.3 s**, small.en 0.17 s for 8 s of speech (warm) |
| Retrieval | 0.3 s | same |
| Brain, Claude | **new `claude -p` each turn: 5.5–6.0 s**, nothing spoken until done | **one persistent `claude` stream session: first words in 0.40–0.67 s**, same plan, no API key |
| Brain, local 9B | full reply 2–4 s, nothing spoken until done | streaming: first token ~1.5 s on a new question (it reads ~2,150 prompt tokens first), 57 tokens/s |
| Brain, local 27B | — | ~6 s just to read the prompt; too slow to talk to on this laptop |
| Voice | browser voice, robotic | **Kyutai Pocket TTS: first audio 0.03 s**, ~11× real time on CPU, Whisper transcribed it word-perfect |

**Voice-to-voice today: ~6–7 s. Reachable with these parts: ~1.2–1.8 s on Claude, ~2–2.5 s on local
9B.** The research consensus is 0.5–0.8 s great, under 1.5 s fine, above 1.5 s poor. One surprise:
**Claude in a persistent session starts talking faster than the local 9B**, because the 9B has to read
the notes first at ~1,400 tokens/s. A leaner local prompt (fewer, shorter notes) narrows that.

Kokoro (the other popular local voice) would not install cleanly here: its text processor fails on
Python 3.15 and on 3.12 its espeak data path. Pocket TTS needs Python ≤ 3.14 too, so the voice bay gets
its own Python 3.12 environment. Pocket TTS code is MIT; each built-in voice has its own license (check
before publishing anything with it), and it clones a voice from a ~5 s clip.

## 4. Verdict

**Keep our approach.** The galaxy, the honesty rules, meaning-based retrieval, one shared brain, and
answering on the Claude plan are all at least as good as his, and several are better. **Replace the
voice layer**, in this order (each is shippable alone):

1. **Speed (biggest win):** one persistent `claude` stream session; the model writes the spoken answer
   as plain text *first* and a short tag line after it (sources, about-notes, action), so the page can
   speak clause by clause while the rest is still arriving. Ollama streams the same way. Expected: first
   words ~1 s after you stop talking, down from ~6 s.
2. **Voice:** a local voice bay (Python 3.12 + Pocket TTS, kept warm) that streams audio to the page;
   the browser voice stays as the fallback. A JARVIS voice of our choosing (a built-in voice, or a clip
   Terry records). No paid service.
3. **Ears:** the page records with echo cancellation and Silero VAD, Smart Turn decides when you're
   done, and Whisper turbo on the Mac transcribes. openWakeWord "hey Jarvis" for hands-free. Fixes
   "Thomas," the cut-offs, and audio going to Google.
4. **Barge-in:** any speech while JARVIS talks stops him (echo cancellation makes this safe on
   speakers), and the brain is told it was interrupted.

**Considered and rejected for now:** OpenAI `gpt-realtime-2` speech-to-speech (fastest, ~$32/$64 per 1M
audio tokens, but it is not Claude and can't use our plan); Pipecat or LiveKit as the framework
(excellent and they include Smart Turn, but heavy, and they don't speak the `claude` CLI; we borrow their
models instead); Anthropic has no voice or realtime API as of November 2026.

## 5. Research links

- Smart Turn v3.2: https://github.com/pipecat-ai/smart-turn · https://www.daily.co/blog/smart-turn-v3-2-handling-noisy-environments-and-short-responses/
- LiveKit turn detector: https://livekit.com/blog/solving-end-of-turn-detection
- Silero VAD: https://pypi.org/project/silero-vad/
- Pocket TTS: https://github.com/kyutai-labs/pocket-tts
- mlx-audio (Kokoro, CSM, more): https://github.com/Blaizzy/mlx-audio
- Local Mac voice agent example (Pipecat, MLX Whisper, Kokoro): https://github.com/kwindla/macos-local-voice-agents
- Latency budgets: https://elevenlabs.io/blog/voice-agent-latency-optimization · https://soniox.com/wiki/voice-agent-latency-budget
- OpenAI realtime pricing: https://developers.openai.com/api/docs/models/gpt-realtime-2
- Claude models (no audio API): https://platform.claude.com/docs/en/about-claude/models/overview

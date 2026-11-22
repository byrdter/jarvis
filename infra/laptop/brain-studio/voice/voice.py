"""JARVIS's voice: Kyutai Pocket TTS on this Mac, served on 127.0.0.1 only.

Runs in its own Python 3.12 environment (Pocket TTS needs Python < 3.15; see setup.sh). server.py starts
it as a child process and proxies /api/tts to it, so the page never talks to this port directly.

  GET  /health          {"ready", "voice", "voices", "error"}
  POST /tts   {"text"}  -> audio/wav (16-bit mono), one sentence or a few
  POST /voice {"voice"} switch voice: a built-in name, or a path to a ~5-20 s WAV clip to clone

Measured 2026-11-22 on the M5 Pro: first audio 0.03 s, ~11x faster than real time, on the CPU.
Built-in voice licenses (huggingface.co/kyutai/tts-voices): marius, javert = CC0 (donated); anna, vera,
fantine, charles, paul, eponine, azelma = CC-BY 4.0 (credit VCTK); cosette = non-commercial only.
Only clone a voice you own or have permission to use.
"""
from __future__ import annotations

import io
import json
import os
import sys
import threading
import time
import wave
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

VOICES = {  # name -> license, so the choice is never a surprise
    "marius": "CC0", "javert": "CC0",
    "charles": "CC-BY 4.0", "paul": "CC-BY 4.0", "anna": "CC-BY 4.0", "vera": "CC-BY 4.0",
    "fantine": "CC-BY 4.0", "eponine": "CC-BY 4.0", "azelma": "CC-BY 4.0",
    "alba": "see kyutai/tts-voices", "jean": "see kyutai/tts-voices", "cosette": "non-commercial",
}
DEFAULT_VOICE = os.environ.get("BRAIN_STUDIO_VOICE", "marius")
MAX_CHARS = 600          # one request; the page sends a sentence at a time
CACHE_MAX = 300          # short lines ("Hi Terry.", "Back on Claude.") come back instantly

S = {"model": None, "state": None, "voice": None, "ready": False, "error": None}
_lock = threading.Lock()          # the model is not thread-safe: one render at a time
_states: dict[str, object] = {}
_cache: dict[tuple[str, str], bytes] = {}


def load(voice: str):
    try:
        from pocket_tts import TTSModel
        t = time.time()
        S["model"] = TTSModel.load_model()
        set_voice(voice)
        render("Standing by.")                       # warm every code path before the first real line
        S["ready"] = True
        print(f"voice ready: {S['voice']} in {time.time() - t:.1f}s", flush=True)
    except Exception as e:
        S["error"] = f"{type(e).__name__}: {e}"
        print(f"voice failed to load: {S['error']}", file=sys.stderr, flush=True)


def set_voice(voice: str):
    voice = voice.strip()
    if voice not in VOICES and not Path(voice).expanduser().is_file():
        raise ValueError(f"unknown voice {voice!r}; built-in: {', '.join(VOICES)}, or a path to a WAV clip")
    with _lock:
        if voice not in _states:
            src = str(Path(voice).expanduser()) if voice not in VOICES else voice
            _states[voice] = S["model"].get_state_for_audio_prompt(src)
        S["state"], S["voice"] = _states[voice], voice


def render(text: str) -> bytes:
    key = (S["voice"], text)
    if key in _cache:
        return _cache[key]
    with _lock:
        audio = S["model"].generate_audio(S["state"], text).numpy()
    pcm = (audio.clip(-1, 1) * 32767).astype("<i2").tobytes()
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(S["model"].sample_rate); w.writeframes(pcm)
    data = buf.getvalue()
    if len(text) <= 120:
        if len(_cache) >= CACHE_MAX:
            _cache.pop(next(iter(_cache)))
        _cache[key] = data
    return data


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def reply(self, code: int, body: bytes, ctype: str = "application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def j(self, code: int, obj: dict):
        self.reply(code, json.dumps(obj).encode())

    def do_GET(self):
        if self.path == "/health":
            return self.j(200, {"ready": S["ready"], "voice": S["voice"], "error": S["error"],
                                "voices": VOICES})
        self.j(404, {"error": "unknown route"})

    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        except ValueError:
            return self.j(400, {"error": "bad json"})
        if not S["ready"]:
            return self.j(503, {"error": S["error"] or "the voice is still loading"})
        try:
            if self.path == "/tts":
                text = str(body.get("text", "")).strip()[:MAX_CHARS]
                if not text:
                    return self.j(400, {"error": "no text"})
                t = time.time()
                data = render(text)
                self.send_response(200)
                self.send_header("Content-Type", "audio/wav")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("X-Render-Ms", str(int((time.time() - t) * 1000)))
                self.send_header("X-Jarvis-Voice", f"local:{S['voice']}")
                self.end_headers()
                return self.wfile.write(data)
            if self.path == "/voice":
                set_voice(str(body.get("voice", "")))
                return self.j(200, {"voice": S["voice"], "license": VOICES.get(S["voice"], "your own clip")})
        except ValueError as e:
            return self.j(400, {"error": str(e)})
        except Exception as e:
            return self.j(500, {"error": f"{type(e).__name__}: {e}"})
        self.j(404, {"error": "unknown route"})


def main(argv: list[str]) -> int:
    port = int(argv[argv.index("--port") + 1]) if "--port" in argv else 4701
    threading.Thread(target=load, args=(DEFAULT_VOICE,), daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"voice bay on http://127.0.0.1:{port} (loading {DEFAULT_VOICE})", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

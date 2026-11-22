#!/usr/bin/env bash
# One-time setup for JARVIS's local voice (Kyutai Pocket TTS). Pocket TTS needs Python < 3.15, and this
# Mac's default python3 is 3.15, so the voice gets its own 3.12 environment outside the repo.
# server.py finds it there and starts the voice automatically; without it, the page uses the browser voice.
set -euo pipefail
VENV="${BRAIN_STUDIO_VOICE_VENV:-$HOME/.local/share/jarvis/brain-studio/voice-venv}"
command -v uv >/dev/null || { echo "needs uv: brew install uv"; exit 1; }
uv venv -q -p 3.12 "$VENV"
VIRTUAL_ENV="$VENV" uv pip install -q "pocket-tts==4.0.1"
# Download the model and the default voice once, and prove it speaks.
"$VENV/bin/python" - <<'EOF'
import time
from pocket_tts import TTSModel
t = time.time(); m = TTSModel.load_model(); st = m.get_state_for_audio_prompt("marius")
a = m.generate_audio(st, "Voice check. JARVIS can talk.")
print(f"ok: {len(a) / m.sample_rate:.1f}s of speech, setup took {time.time() - t:.0f}s")
EOF
echo "voice ready in $VENV"

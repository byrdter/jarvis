#!/bin/bash
# Run ON THE SERVER, as the jarvis user. Installs Ollama without sudo (user-level, from the official
# GitHub release), runs it as a user service on 127.0.0.1:11434 only, and pulls nomic-embed-text,
# the small model that brain search (infra/laptop/brain-ask.py search) uses to match by meaning.
# Re-run to upgrade: set OLLAMA_VERSION=vX.Y.Z (default: the pinned version below).
set -euo pipefail
VER="${OLLAMA_VERSION:-v0.40.16}"
DEST="$HOME/.local/ollama"
command -v zstd >/dev/null || { echo "needs zstd (sudo apt-get install -y zstd)"; exit 1; }

if [[ ! -x "$DEST/bin/ollama" ]] || ! "$DEST/bin/ollama" --version 2>/dev/null | grep -q "${VER#v}"; then
  tmp=$(mktemp -d)
  curl -fL --retry 3 -o "$tmp/ollama.tar.zst" \
    "https://github.com/ollama/ollama/releases/download/$VER/ollama-linux-amd64.tar.zst"
  rm -rf "$DEST" && mkdir -p "$DEST"
  tar --use-compress-program=unzstd -xf "$tmp/ollama.tar.zst" -C "$DEST"
  rm -rf "$tmp"
  # CPU-only box: the GPU libraries are dead weight.
  rm -rf "$DEST"/lib/ollama/cuda_* "$DEST"/lib/ollama/rocm* 2>/dev/null || true
fi
mkdir -p "$HOME/.local/bin" "$HOME/.config/systemd/user"
ln -sf "$DEST/bin/ollama" "$HOME/.local/bin/ollama"

cat > "$HOME/.config/systemd/user/ollama.service" <<EOF
[Unit]
Description=Ollama (local embeddings for brain search), localhost only

[Service]
ExecStart=$DEST/bin/ollama serve
Environment=OLLAMA_HOST=127.0.0.1:11434
Environment=OLLAMA_KEEP_ALIVE=5m
Environment=OLLAMA_MAX_LOADED_MODELS=1
Restart=on-failure

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now ollama.service
for i in $(seq 1 30); do curl -sf http://127.0.0.1:11434/api/version >/dev/null && break; sleep 1; done
"$DEST/bin/ollama" pull nomic-embed-text
"$DEST/bin/ollama" --version
du -sh "$DEST"

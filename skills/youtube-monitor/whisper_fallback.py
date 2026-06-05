"""
Whisper fallback for videos whose YouTube captions are disabled/missing.

Pipeline:
  yt-dlp  ->  wav file (16kHz mono)  ->  whisper-cli  ->  text + segments

Audio archive lives on ORICO so we don't re-download. Failures are tolerated
silently (the video just stays at status='disabled' in the DB).
"""
from __future__ import annotations
import json
import os
import shutil
import subprocess
from pathlib import Path

# Tools — must be on PATH. Daily shell script sets PATH explicitly.
YT_DLP = shutil.which("yt-dlp") or "/opt/homebrew/bin/yt-dlp"
WHISPER_CLI = shutil.which("whisper-cli") or "/opt/homebrew/bin/whisper-cli"
WHISPER_MODEL = Path(os.path.expanduser("~/.whisper-models/ggml-base.en.bin"))

ORICO_ROOT = Path("/Volumes/ORICO/jarvis/youtube-transcripts")
AUDIO_ARCHIVE = ORICO_ROOT / "audio-archive"
TMP_DIR = Path(os.path.expanduser("~/.local/share/jarvis/youtube-transcripts/whisper-tmp"))


def _ensure_dirs():
    target = AUDIO_ARCHIVE if ORICO_ROOT.exists() else TMP_DIR
    target.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    return target


def whisper_available() -> bool:
    return Path(WHISPER_CLI).exists() and WHISPER_MODEL.exists() and Path(YT_DLP).exists()


def fetch_with_whisper(video_id: str, url: str, verbose: bool = False):
    """Return (text, segments, 'whisper') or (None, None, status).

    segments is a list of {text, start, duration} dicts so it matches the
    captions branch's storage shape.
    """
    if not whisper_available():
        return None, None, "whisper_unavailable"

    audio_root = _ensure_dirs()
    wav_path = audio_root / f"{video_id}.wav"
    json_path = TMP_DIR / f"{video_id}.json"

    # 1) Download audio if not already cached
    if not wav_path.exists():
        cmd = [
            YT_DLP, "-x",
            "--audio-format", "wav",
            "--audio-quality", "0",
            "--postprocessor-args", "ffmpeg:-ar 16000 -ac 1",
            "-o", str(wav_path.with_suffix("")) + ".%(ext)s",
            "--quiet", "--no-warnings",
            url,
        ]
        if verbose:
            print(f"    🎵 yt-dlp {video_id}")
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            if r.returncode != 0 or not wav_path.exists():
                return None, None, "yt_dlp_failed"
        except subprocess.TimeoutExpired:
            return None, None, "yt_dlp_timeout"
        except Exception as e:
            return None, None, f"yt_dlp_error:{type(e).__name__}"

    # 2) Whisper transcription with JSON output (gives us segments + text)
    if verbose:
        print(f"    🗣  whisper-cli {video_id}")
    cmd = [
        WHISPER_CLI,
        "-m", str(WHISPER_MODEL),
        "-f", str(wav_path),
        "-oj",
        "-of", str(json_path.with_suffix("")),
        "--no-prints",
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        if r.returncode != 0 or not json_path.exists():
            return None, None, f"whisper_failed:{r.returncode}"
    except subprocess.TimeoutExpired:
        return None, None, "whisper_timeout"
    except Exception as e:
        return None, None, f"whisper_error:{type(e).__name__}"

    # 3) Parse whisper.cpp JSON output
    try:
        data = json.loads(json_path.read_text())
        transcription = data.get("transcription", [])
        segments = []
        text_parts = []
        for seg in transcription:
            t = (seg.get("text") or "").strip()
            if not t:
                continue
            start_ms = (seg.get("offsets") or {}).get("from", 0)
            end_ms = (seg.get("offsets") or {}).get("to", start_ms)
            segments.append({
                "text": t,
                "start": start_ms / 1000.0,
                "duration": (end_ms - start_ms) / 1000.0,
            })
            text_parts.append(t)
        text = " ".join(text_parts).strip()
        if not text:
            return None, None, "whisper_empty"
        return text, segments, "whisper"
    except Exception as e:
        return None, None, f"whisper_parse_error:{type(e).__name__}"
    finally:
        # Keep WAV on ORICO archive; clean only the temp json
        if json_path.exists():
            try:
                json_path.unlink()
            except OSError:
                pass

#!/usr/bin/env python3
"""Generate per-scene Cartesia narration with word timestamps.

Credentials are loaded from the repository .env and never written to output.
The selected voice is passed explicitly because the shared .env contains several
historical CARTESIA_VOICE_ID entries.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import uuid
import wave
from pathlib import Path

from cartesia import Cartesia


SCENE_RE = re.compile(
    r"^(?:====\s*|##\s*)SCENE\s+(\d+)\s+—\s+(.+?)(?:\s*====)?$",
    re.MULTILINE,
)
CITATION_RE = re.compile(r"\s*\[CITE-[^\]]+\]")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def parse_scenes(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(SCENE_RE.finditer(text))
    scenes: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        transcript = text[start:end].strip()
        transcript = HTML_COMMENT_RE.sub("", transcript)
        transcript = CITATION_RE.sub("", transcript)
        transcript = re.sub(r"\n{3,}", "\n\n", transcript).strip()
        if not transcript:
            raise ValueError(f"Scene {match.group(1)} has no spoken text")
        scenes.append(
            {
                "number": match.group(1),
                "title": match.group(2).strip(),
                "transcript": transcript,
            }
        )
    if len(scenes) != 12:
        raise ValueError(f"Expected 12 scenes, found {len(scenes)}")
    return scenes


def ffprobe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return round(float(result.stdout.strip()), 3)


def synthesize_scene(
    client: Cartesia,
    scene: dict[str, str],
    output_dir: Path,
    model_id: str,
    voice_id: str,
    speed: float,
) -> dict:
    scene_id = f"s{int(scene['number']) - 1:02d}"
    wav_path = output_dir / f"{scene_id}-narration.wav"
    words_path = output_dir / f"{scene_id}-words.json"
    text_path = output_dir / f"{scene_id}-spoken.txt"
    context_id = str(uuid.uuid4())

    pcm = bytearray()
    words: list[dict] = []
    stream = client.tts.generate_sse(
        model_id=model_id,
        transcript=scene["transcript"],
        voice={"mode": "id", "id": voice_id},
        output_format={
            "container": "raw",
            "encoding": "pcm_s16le",
            "sample_rate": 44100,
        },
        language="en",
        context_id=context_id,
        add_timestamps=True,
        use_normalized_timestamps=True,
        generation_config={"speed": speed, "volume": 1.0},
        timeout=300.0,
    )

    for event in stream:
        if event.type == "chunk" and event.audio:
            pcm.extend(event.audio)
        elif event.type == "timestamps" and event.word_timestamps:
            timestamps = event.word_timestamps
            for token, start, end in zip(timestamps.words, timestamps.start, timestamps.end):
                words.append(
                    {
                        "id": f"w{len(words)}",
                        "text": token,
                        "start": round(float(start), 4),
                        "end": round(float(end), 4),
                    }
                )
        elif event.type == "error":
            raise RuntimeError(f"Cartesia returned an error for {scene_id}: {event.error}")

    if not pcm:
        raise RuntimeError(f"Cartesia returned no audio for {scene_id}")
    if not words:
        raise RuntimeError(f"Cartesia returned no word timestamps for {scene_id}")

    with wave.open(str(wav_path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        wav_file.writeframes(pcm)

    duration = ffprobe_duration(wav_path)
    if duration <= 0 or words[-1]["end"] > duration + 1.0:
        raise RuntimeError(
            f"Invalid timing for {scene_id}: audio={duration}s last_word={words[-1]['end']}s"
        )

    words_path.write_text(json.dumps(words, indent=2) + "\n", encoding="utf-8")
    text_path.write_text(scene["transcript"] + "\n", encoding="utf-8")
    return {
        "id": scene_id,
        "title": scene["title"],
        "path": str(wav_path),
        "words_path": str(words_path),
        "text_path": str(text_path),
        "duration_s": duration,
        "word_count": len(words),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=Path, required=True)
    parser.add_argument("--script", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--voice", required=True)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument(
        "--scene",
        type=int,
        action="append",
        help="Generate only the selected one-based scene number; may be repeated.",
    )
    args = parser.parse_args()

    env = load_env(args.env)
    api_key = env.get("CARTESIA_API_KEY")
    model_id = env.get("CARTESIA_MODEL_ID")
    if not api_key:
        raise SystemExit("CARTESIA_API_KEY is missing")
    if not model_id:
        raise SystemExit("CARTESIA_MODEL_ID is missing")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    scenes = parse_scenes(args.script)
    if args.scene:
        selected = {str(number).zfill(2) for number in args.scene}
        scenes = [scene for scene in scenes if scene["number"].zfill(2) in selected]
        missing = selected - {scene["number"].zfill(2) for scene in scenes}
        if missing:
            raise SystemExit(f"Requested scene(s) not found: {', '.join(sorted(missing))}")
    client = Cartesia(api_key=api_key)
    generated = []
    for scene in scenes:
        print(f"Generating scene {scene['number']}: {scene['title']}", flush=True)
        generated.append(
            synthesize_scene(client, scene, args.output_dir, model_id, args.voice, args.speed)
        )

    meta = {
        "tts_provider": "cartesia",
        "voice_id": args.voice,
        "model_id": model_id,
        "speed": args.speed,
        "sample_rate": 44100,
        "channels": 1,
        "source_script": str(args.script),
        "voices": generated,
        "total_duration_s": round(sum(item["duration_s"] for item in generated), 3),
    }
    meta_path = args.output_dir / "audio_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {meta_path}")


if __name__ == "__main__":
    main()

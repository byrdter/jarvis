#!/usr/bin/env python3
"""Offset scene-local Cartesia timestamps into the episode timeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_meta", type=Path)
    parser.add_argument("--gap", type=float, default=0.7)
    parser.add_argument("--transcript-out", type=Path, required=True)
    parser.add_argument("--timings-out", type=Path, required=True)
    args = parser.parse_args()

    meta = json.loads(args.audio_meta.read_text(encoding="utf-8"))
    global_words: list[dict] = []
    timings: list[dict] = []
    cursor = 0.0

    for index, voice in enumerate(meta["voices"]):
        scene_id = voice["id"]
        start = round(cursor, 3)
        duration = float(voice["duration_s"])
        end = round(start + duration, 3)
        timings.append(
            {"id": scene_id, "start_s": start, "end_s": end, "duration_s": duration}
        )
        local_words = json.loads(Path(voice["words_path"]).read_text(encoding="utf-8"))
        for word in local_words:
            global_words.append(
                {
                    "id": f"w{len(global_words)}",
                    "text": word["text"],
                    "start": round(start + float(word["start"]), 4),
                    "end": round(start + float(word["end"]), 4),
                    "scene": scene_id,
                }
            )
        cursor = end + (args.gap if index < len(meta["voices"]) - 1 else 0.0)

    master_duration = round(cursor, 3)
    by_id = {item["id"]: item for item in timings}
    timing_doc = {
        "source": str(args.audio_meta),
        "duration_authority": "ffprobe",
        "inter_scene_gap_s": args.gap,
        "master_duration_s": master_duration,
        "master_duration_display": f"{int(master_duration // 60):02d}:{master_duration % 60:06.3f}",
        "scenes": timings,
        "structural_positions": {
            "reversal_scene": "s05",
            "reversal_start_pct": round(by_id["s05"]["start_s"] / master_duration * 100, 2),
            "reversal_end_pct": round(by_id["s05"]["end_s"] / master_duration * 100, 2),
            "verdict_scene": "s10",
            "verdict_start_pct": round(by_id["s10"]["start_s"] / master_duration * 100, 2),
            "cta_scene": "s11",
        },
    }

    args.transcript_out.parent.mkdir(parents=True, exist_ok=True)
    args.timings_out.parent.mkdir(parents=True, exist_ok=True)
    args.transcript_out.write_text(json.dumps(global_words, indent=2) + "\n", encoding="utf-8")
    args.timings_out.write_text(json.dumps(timing_doc, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.transcript_out} ({len(global_words)} words)")
    print(f"Wrote {args.timings_out} ({master_duration}s)")


if __name__ == "__main__":
    main()

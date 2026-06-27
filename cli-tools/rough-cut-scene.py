#!/usr/bin/env python3
"""
Rough-cut scene assembler (V14 / Visuals Map style — L0 + L2).

Inputs:
  --scene-dir   Directory created by split-heygen.py (contains assets/audio.mp3,
                assets/avatar.mp4 if avatar=true, assets/transcript.json)
  --cues        L2 cue YAML (citation cards)
  --backdrop    Optional L0 cue YAML (asset-library backdrops). When omitted
                and no avatar.mp4 exists, the L0 falls back to a cream paper
                still — fine for testing, NOT fine for shipping.
  --cards-dir   Directory containing the rendered card PNGs
  --out         Output MP4 path

L2 cue YAML schema (unchanged):
  cues:
    - cue: "phrase to locate"
      card: c.<card-id>
      duration: 6.0
      offset: 0.0          # optional, shift start time
      fade: 0.3            # optional

L0 backdrop cue YAML schema (NEW):
  backdrop:
    # Either an explicit start_time in seconds, OR a cue phrase to anchor.
    - cue: "CEOs are facing a strategic fork"
      asset: /Users/.../fork-road-drone.mp4
      duration: 22.0       # how long this backdrop stays
      fade: 0.4            # crossfade into and out of (default 0.4)
      tint: 0.6            # 0.0=full original brightness, 1.0=fully dimmed
                           # default 0.0
    - start: 22.0
      asset: /Users/.../phase4-automation-leaving.mp4
      duration: 8.0
      tint: 0.4

The assembler:
  1. Loads audio + transcript.
  2. Builds the L0 backdrop layer (asset-library b-roll chain) OR uses
     avatar.mp4 if it exists OR falls back to cream-paper still.
  3. Resolves L2 cue start times via transcript word-timestamp lookup.
  4. Overlays each card at its window with fade-in / fade-out.
  5. Renders the audio with the scene's audio.mp3.

Video assets are looped via -stream_loop (so a 10-second clip can fill a
30-second backdrop window). Still images use -loop 1. Tint is applied via
the eq filter (brightness reduction) so the asset reads as backdrop, not
foreground.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml


def normalize_words(text: str) -> list[str]:
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).split()


def media_duration(path: Path) -> float:
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
        )
        .decode()
        .strip()
    )


def find_cue_time(cue: str, words: list[dict]) -> float | None:
    target = normalize_words(cue)
    if not target:
        return None
    tokens = []
    for i, w in enumerate(words):
        for t in normalize_words(w["text"]):
            tokens.append((t, i))
    n = len(tokens)
    for i in range(n - len(target) + 1):
        if [tok for tok, _ in tokens[i : i + len(target)]] == target:
            wi = tokens[i][1]
            return float(words[wi]["start"])
    return None


def asset_kind(path: Path) -> str:
    return "video" if path.suffix.lower() in {".mp4", ".mov", ".webm", ".m4v"} else "image"


def assemble(scene_dir: Path, cues_file: Path, backdrop_file: Path | None,
             cards_dir: Path, out: Path) -> None:
    assets = scene_dir / "assets"
    audio = assets / "audio.mp3"
    avatar = assets / "avatar.mp4"
    transcript = assets / "transcript.json"

    if not audio.exists():
        sys.exit(f"missing {audio}")
    if not transcript.exists():
        sys.exit(f"missing {transcript}")

    duration = media_duration(audio)
    words = json.loads(transcript.read_text())

    # ---- L2 cues (cards) -----------------------------------------------------
    cues = yaml.safe_load(cues_file.read_text()).get("cues", [])
    l2: list[tuple[float, Path, float, float]] = []
    for c in cues:
        start = c.get("start")
        if start is None:
            start = find_cue_time(c["cue"], words)
            if start is None:
                print(f"  ⚠️  L2 cue '{c['cue']}' not found — skipping", file=sys.stderr)
                continue
        start += float(c.get("offset", 0.0))
        card = cards_dir / f"{c['card']}.png"
        if not card.exists():
            print(f"  ⚠️  missing card: {card.name}", file=sys.stderr)
            continue
        l2.append((float(start), card, float(c.get("duration", 5.0)), float(c.get("fade", 0.3))))
    for i, (s, p, d, f) in enumerate(l2):
        if s + d > duration:
            l2[i] = (s, p, max(0.5, duration - s - 0.1), f)

    # ---- L0 backdrop cues ----------------------------------------------------
    # Each item is (start, asset_path, duration, fade, tint).
    l0: list[tuple[float, Path, float, float, float]] = []
    if backdrop_file and backdrop_file.exists():
        bd_spec = yaml.safe_load(backdrop_file.read_text()).get("backdrop", [])
        for b in bd_spec:
            start = b.get("start")
            if start is None and "cue" in b:
                start = find_cue_time(b["cue"], words)
                if start is None:
                    print(f"  ⚠️  L0 cue '{b['cue']}' not found — skipping", file=sys.stderr)
                    continue
            if start is None:
                print(f"  ⚠️  L0 entry missing 'start' or 'cue' — skipping", file=sys.stderr)
                continue
            asset = Path(b["asset"])
            if not asset.exists():
                print(f"  ⚠️  missing L0 asset: {asset}", file=sys.stderr)
                continue
            l0.append((float(start), asset, float(b.get("duration", 8.0)),
                       float(b.get("fade", 0.4)), float(b.get("tint", 0.0))))
        # Clamp last asset to scene duration.
        for i, (s, p, d, f, t) in enumerate(l0):
            if s + d > duration:
                l0[i] = (s, p, max(0.5, duration - s - 0.05), f, t)

    # ---- Decide base layer ---------------------------------------------------
    # Priority: avatar > L0 chain > cream paper.
    has_avatar = avatar.exists()
    has_l0 = bool(l0)
    if has_avatar and has_l0:
        # If both, prefer avatar for avatar-marked scenes (script intent).
        # Avatar scenes typically don't ship with a backdrop manifest anyway.
        has_l0 = False

    # ---- Build ffmpeg command ------------------------------------------------
    cmd: list[str] = ["ffmpeg", "-y", "-v", "error"]
    base_label = "[bg]"
    filters: list[str] = []
    # Always start with a cream paper canvas (visible only where nothing else covers).
    cmd += ["-f", "lavfi", "-i", f"color=c=#F4F1EA:s=1920x1080:r=30:d={duration}"]
    cream_input_idx = 0
    next_input = 1
    filters.append(
        f"[{cream_input_idx}:v]format=yuv420p,setsar=1[bg]"
    )

    if has_avatar:
        cmd += ["-i", str(avatar)]
        avatar_idx = next_input
        next_input += 1
        filters.append(
            f"[{avatar_idx}:v]scale=1920:1080:force_original_aspect_ratio=decrease,"
            f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#F4F1EA,setsar=1,format=yuv420p[av]"
        )
        filters.append(f"[bg][av]overlay=x=0:y=0[v_base]")
        prev_label = "[v_base]"
    elif has_l0:
        # Chain each L0 backdrop asset as an overlay with enable=between(start,end).
        # Each asset is scaled to 1920x1080 (preserve aspect) and tinted.
        prev_label = "[bg]"
        for i, (start, asset, dur, fade, tint) in enumerate(l0):
            end = start + dur
            if asset_kind(asset) == "video":
                # Loop the video stream for the full window.
                cmd += ["-stream_loop", "-1", "-t", f"{dur:.3f}", "-i", str(asset)]
            else:
                cmd += ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(asset)]
            asset_idx = next_input
            next_input += 1
            tint_amt = max(0.0, min(0.95, tint))
            brightness = -tint_amt * 0.4
            label = f"[a{i}]"
            filters.append(
                f"[{asset_idx}:v]scale=1920:1080:force_original_aspect_ratio=increase,"
                f"crop=1920:1080,setsar=1,eq=brightness={brightness:.3f},"
                f"setpts=PTS-STARTPTS+{start:.3f}/TB,"
                f"fade=t=in:st={start:.3f}:d={fade:.3f},"
                f"fade=t=out:st={max(start, end - fade):.3f}:d={fade:.3f},"
                f"format=yuva420p{label}"
            )
            out_label = f"[v_l0_{i}]"
            filters.append(
                f"{prev_label}{label}overlay=enable='between(t,{start:.3f},{end:.3f})':x=0:y=0:eof_action=pass{out_label}"
            )
            prev_label = out_label
    else:
        prev_label = "[bg]"

    # Audio input goes after all visual inputs.
    cmd += ["-i", str(audio)]
    audio_idx = next_input
    next_input += 1

    # ---- L2 cards overlay ----------------------------------------------------
    for i, (start, card_path, dur, fade) in enumerate(l2):
        end = start + dur
        cmd += ["-loop", "1", "-i", str(card_path)]
        card_idx = next_input
        next_input += 1
        card_label = f"[c{i}]"
        filters.append(
            f"[{card_idx}:v]format=rgba,fade=t=in:st={start:.3f}:d={fade:.3f}:alpha=1,"
            f"fade=t=out:st={max(start+fade, end - fade):.3f}:d={fade:.3f}:alpha=1{card_label}"
        )
        out_label = f"[v_c_{i}]"
        filters.append(
            f"{prev_label}{card_label}overlay=enable='between(t,{start:.3f},{end:.3f})':x=0:y=0{out_label}"
        )
        prev_label = out_label

    filter_complex = ";".join(filters)
    cmd += [
        "-filter_complex", filter_complex,
        "-map", prev_label,
        "-map", f"{audio_idx}:a:0",
        "-c:v", "libx264", "-preset", "faster", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-t", f"{duration:.3f}",
        str(out),
    ]

    src = "avatar" if has_avatar else ("L0" if has_l0 else "cream")
    print(f"  → {out.name}  ({src}, {len(l0)} backdrops, {len(l2)} cards, {duration:.1f}s)")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(res.stderr[-3000:])
        sys.exit(f"ffmpeg failed for {scene_dir.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene-dir", required=True)
    ap.add_argument("--cues", required=True)
    ap.add_argument("--backdrop", default=None)
    ap.add_argument("--cards-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    assemble(Path(args.scene_dir), Path(args.cues),
             Path(args.backdrop) if args.backdrop else None,
             Path(args.cards_dir), Path(args.out))


if __name__ == "__main__":
    main()

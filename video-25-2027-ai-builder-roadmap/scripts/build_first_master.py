#!/usr/bin/env python3
"""Build the first complete Video 25 master from HeyGen scene audio.

This is a pragmatic first-pass compositor:
- draws safe, sanitized 1920x1080 scene boards with Pillow
- embeds public web-roll/product assets into browser/device frames
- attaches the split HeyGen scene audio
- concatenates all scene MP4s into one master

Large generated media stays local and is ignored by Git.
"""

from __future__ import annotations

import json
import math
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[0]
ASSETS = REPO / "asset-library"
OUT = ROOT / "renders" / "first-master"
BOARDS = OUT / "boards"
SCENE_MP4 = OUT / "scenes"
MASTER = OUT / "video-25-first-master.mp4"
WIDTH, HEIGHT = 1920, 1080


INK = "#071014"
PANEL = "#0f2a31"
PANEL_2 = "#123842"
SIGNAL = "#18d6b3"
GOLD = "#f4c95d"
TEXT = "#e8f4f2"
MUTED = "#8fa8a3"
VIOLET = "#b75cff"
DANGER = "#ff6b6b"


def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    candidates = []
    if mono:
        candidates += [
            "/System/Library/Fonts/Monaco.ttf",
            "/System/Library/Fonts/Supplemental/Courier New.ttf",
        ]
    if bold:
        candidates += [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf",
        ]
    candidates += [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


F_TITLE = font(82, bold=True)
F_H2 = font(48, bold=True)
F_BODY = font(31)
F_SMALL = font(23)
F_MICRO = font(19, mono=True)
F_MONO = font(25, mono=True)


def draw_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str, fnt, max_width: int, line_gap: int = 10) -> int:
    x, y = xy
    words = text.split()
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width:
            line = test
        else:
            draw.text((x, y), line, fill=fill, font=fnt)
            y += draw.textbbox((0, 0), line, font=fnt)[3] + line_gap
            line = word
    if line:
        draw.text((x, y), line, fill=fill, font=fnt)
        y += draw.textbbox((0, 0), line, font=fnt)[3] + line_gap
    return y


def rounded(draw: ImageDraw.ImageDraw, box, fill, outline=None, width=1, radius=18):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def glow_line(draw: ImageDraw.ImageDraw, p1, p2, fill=SIGNAL, width=3):
    draw.line((p1, p2), fill=fill, width=width)


def base_canvas() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), INK)
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(0, HEIGHT, 48):
        od.line((0, y, WIDTH, y), fill=(232, 244, 242, 9), width=1)
    for x in range(0, WIDTH, 48):
        od.line((x, 0, x, HEIGHT), fill=(232, 244, 242, 7), width=1)
    for r, alpha in [(520, 42), (360, 36), (240, 28)]:
        od.ellipse((120 - r, 20 - r, 120 + r, 20 + r), fill=(24, 214, 179, alpha))
        od.ellipse((1650 - r, 130 - r, 1650 + r, 130 + r), fill=(183, 92, 255, alpha))
    overlay = overlay.filter(ImageFilter.GaussianBlur(28))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return img


def draw_header(draw: ImageDraw.ImageDraw, scene_no: int, label: str):
    draw.text((70, 52), f"VIDEO 25 / SCENE {scene_no:02d}", fill=SIGNAL, font=F_MICRO)
    draw.text((70, 83), label.upper(), fill=MUTED, font=F_MICRO)
    draw.line((70, 122, 1850, 122), fill=(24, 214, 179), width=1)


def draw_browser_slot(draw: ImageDraw.ImageDraw, slot, title: str, accent=SIGNAL):
    x, y, w, h = slot
    rounded(draw, (x - 16, y - 46, x + w + 16, y + h + 16), fill=(8, 22, 26), outline=(34, 74, 80), width=2, radius=22)
    draw.rounded_rectangle((x - 16, y - 46, x + w + 16, y - 4), radius=18, fill=(12, 31, 36))
    for i, c in enumerate([DANGER, GOLD, SIGNAL]):
        draw.ellipse((x + 14 + i * 28, y - 32, x + 26 + i * 28, y - 20), fill=c)
    draw.text((x + 110, y - 35), title, fill=TEXT, font=F_MICRO)
    rounded(draw, (x, y, x + w, y + h), fill=(4, 8, 10), outline=accent, width=2, radius=12)


def draw_bullets(draw: ImageDraw.ImageDraw, bullets: list[str], x: int, y: int, w: int):
    for bullet in bullets:
        rounded(draw, (x, y + 7, x + 18, y + 25), fill=GOLD, radius=5)
        y = draw_text(draw, (x + 34, y), bullet, TEXT, F_SMALL, w - 34, 7) + 4
    return y


def draw_terminal(draw: ImageDraw.ImageDraw, box, lines: list[str]):
    x, y, w, h = box
    rounded(draw, (x, y, x + w, y + h), fill=(3, 10, 12), outline=(24, 214, 179), width=2, radius=18)
    draw.rectangle((x, y, x + w, y + 48), fill=(12, 31, 36))
    for i, c in enumerate([DANGER, GOLD, SIGNAL]):
        draw.ellipse((x + 22 + i * 28, y + 17, x + 36 + i * 28, y + 31), fill=c)
    yy = y + 74
    for line in lines:
        draw.text((x + 28, yy), line, fill=SIGNAL if line.startswith("$") else TEXT, font=F_MONO)
        yy += 38


def draw_roadmap(draw: ImageDraw.ImageDraw, x: int, y: int, items: list[str], vertical: bool = True):
    if vertical:
        for i, item in enumerate(items):
            cy = y + i * 82
            draw.ellipse((x, cy, x + 42, cy + 42), fill=SIGNAL if i < 4 else PANEL_2, outline=GOLD, width=2)
            draw.text((x + 15, cy + 7), str(i + 1), fill=INK if i < 4 else TEXT, font=F_SMALL)
            if i < len(items) - 1:
                glow_line(draw, (x + 21, cy + 42), (x + 21, cy + 82), fill=(24, 214, 179), width=2)
            rounded(draw, (x + 70, cy - 8, x + 620, cy + 54), fill=(15, 42, 49), outline=(55, 93, 98), radius=12)
            draw.text((x + 92, cy + 8), item, fill=TEXT, font=F_SMALL)
    else:
        for i, item in enumerate(items):
            cx = x + i * 178
            draw.ellipse((cx, y, cx + 54, y + 54), fill=PANEL_2, outline=SIGNAL, width=2)
            draw.text((cx + 19, y + 13), str(i + 1), fill=TEXT, font=F_SMALL)
            if i < len(items) - 1:
                glow_line(draw, (cx + 54, y + 27), (cx + 178, y + 27), fill=(244, 201, 93), width=2)
            draw_text(draw, (cx - 34, y + 75), item, TEXT, F_MICRO, 132, 5)


@dataclass
class MediaSlot:
    path: str
    x: int
    y: int
    w: int
    h: int
    title: str


@dataclass
class Scene:
    no: int
    label: str
    title: str
    body: str
    bullets: list[str]
    media: list[MediaSlot]
    kind: str = "default"


def rel(path: str) -> str:
    return str((REPO / path).resolve())


SCENES = [
    Scene(
        1,
        "cold open",
        "Chat is only the entry point",
        "By 2027, useful AI builders understand the operating stack around the model.",
        ["Prompt box gives way to connected systems", "Models, tools, memory, evals, deployment", "Preparation plan, not prediction"],
        [
            MediaSlot("asset-library/products/chatgpt/surfaces/web/hero-full.png", 820, 230, 760, 430, "Chat baseline"),
            MediaSlot("asset-library/products/claude-code/surfaces/desktop/ClaudeCodeDesktop.png", 1140, 590, 560, 315, "Agent workspace"),
        ],
    ),
    Scene(
        2,
        "system shift",
        "From prompt writing to system building",
        "The builder gives the agent a goal, tools, memory, review loops, and a repeatable path to action.",
        ["Goal", "Tools", "Memory", "Review", "Reusable workflow"],
        [MediaSlot("asset-library/products/codex/desktop/CodexDesktop.png", 1040, 235, 590, 332, "Codex workspace")],
        "stack",
    ),
    Scene(
        3,
        "layer 1",
        "Model judgment",
        "The better question is not which model wins. It is which lane fits this job.",
        ["Fast lane", "Deep reasoning lane", "Coding lane", "Multimodal lane", "Private/local lane"],
        [
            MediaSlot("asset-library/products/openai/surfaces/web/hero-full.png", 900, 210, 500, 282, "OpenAI platform"),
            MediaSlot("asset-library/products/google-ai/surfaces/web/gemini-docs-scroll.webm", 1180, 540, 520, 292, "Gemini docs web-roll"),
        ],
        "dashboard",
    ),
    Scene(
        4,
        "layer 2",
        "Tools and APIs",
        "Tools are the bridge between language and action: tool names, schemas, permissions, errors, and logs.",
        ["API surface", "Tool registry", "Agent action", "Result for review"],
        [
            MediaSlot("asset-library/products/anthropic/surfaces/web/claude-code-docs-scroll.webm", 770, 210, 500, 282, "Anthropic docs web-roll"),
            MediaSlot("asset-library/products/mcp-registry/surfaces/web/mcp-docs-scroll.webm", 1260, 355, 500, 282, "MCP registry web-roll"),
            MediaSlot("asset-library/products/github/surfaces/web/pull-requests-scroll.webm", 920, 650, 500, 282, "GitHub PR web-roll"),
        ],
    ),
    Scene(
        5,
        "layer 3",
        "Memory and knowledge",
        "If every AI session starts from zero, the builder becomes the database. That does not scale.",
        ["Sources", "Segments", "Decisions", "Workflows", "Review notes"],
        [MediaSlot("asset-library/shared/JarvisOrb.png", 1270, 210, 310, 310, "JARVIS memory core")],
        "memory",
    ),
    Scene(
        6,
        "layer 4",
        "Workflows, hooks, and skills",
        "When a pattern repeats, it should become an operating procedure the agent can reuse.",
        ["Prompt becomes process", "Process becomes skill", "Skill becomes repeatable system"],
        [MediaSlot("asset-library/products/claude-code/surfaces/desktop/ClaudeCodeDesktop.png", 980, 220, 610, 344, "Mock coding-agent surface")],
        "terminal",
    ),
    Scene(
        7,
        "layer 5",
        "Evals and observability",
        "A serious agent system needs a flight recorder: traces, logs, screenshots, failures, and review loops.",
        ["What did it see?", "What tool did it call?", "What changed?", "Who reviewed it?"],
        [
            MediaSlot("asset-library/products/langchain/surfaces/web/langsmith-scroll.webm", 820, 205, 540, 304, "Trace dashboard web-roll"),
            MediaSlot("asset-library/products/ai-infra/surfaces/web/arize-phoenix-scroll.webm", 1170, 570, 540, 304, "Observability web-roll"),
        ],
    ),
    Scene(
        8,
        "layer 6",
        "Deployment and real systems",
        "AI leaves the demo through endpoints, queues, workers, schedulers, storage, permissions, and monitoring.",
        ["Where does the request enter?", "Where does the agent run?", "What happens if it fails?", "How do we stop it?"],
        [
            MediaSlot("asset-library/products/ai-infra/surfaces/web/runpod-scroll.webm", 760, 205, 480, 270, "RunPod web-roll"),
            MediaSlot("asset-library/products/ai-infra/surfaces/web/modal-scroll.webm", 1260, 205, 480, 270, "Modal web-roll"),
            MediaSlot("asset-library/products/ai-infra/surfaces/web/cloudflare-workers-ai-scroll.webm", 1010, 610, 560, 315, "Cloudflare Workers AI"),
        ],
    ),
    Scene(
        9,
        "roadmap",
        "What to learn in order",
        "Not a race to learn everything. A sequence where each layer makes the next one easier.",
        ["Prompting and judgment", "Git and terminal basics", "APIs and CLI tools", "MCP and tool calling", "Memory and retrieval", "Workflows and skills", "Evals and observability", "Deployment", "Product taste"],
        [],
        "roadmap",
    ),
    Scene(
        10,
        "close + cta",
        "Build the stack",
        "Subscribe, like, and ring the bell for practical AI builder breakdowns as this stack gets built piece by piece.",
        ["Agents", "Tools", "Memory", "Workflows", "Evals", "Deployment", "Judgment"],
        [MediaSlot("asset-library/shared/JarvisOrb.png", 1180, 245, 360, 360, "JARVIS signal")],
        "cta",
    ),
]


def draw_scene(scene: Scene, timing: dict) -> Path:
    img = base_canvas()
    d = ImageDraw.Draw(img, "RGBA")
    draw_header(d, scene.no, scene.label)
    title_bottom = draw_text(d, (70, 162), scene.title, TEXT, F_TITLE, 705, 8)
    y = draw_text(d, (76, title_bottom + 22), scene.body, "#b9cbc7", F_BODY, 690, 12)
    draw_bullets(d, scene.bullets, 82, y + 24, 690)
    rounded(d, (70, 900, 740, 986), fill=(8, 22, 26, 210), outline=(24, 214, 179, 150), width=2, radius=16)
    d.text((94, 922), f"VO {timing['segment_duration']:.1f}s  /  {timing['word_count']} words", fill=SIGNAL, font=F_MICRO)
    d.text((94, 952), "First complete master pass: safe mocks + public evidence rolls", fill=MUTED, font=F_MICRO)

    for slot in scene.media:
        draw_browser_slot(d, (slot.x, slot.y, slot.w, slot.h), slot.title)

    if scene.kind == "stack":
        items = ["Model", "Tools", "Memory", "Workflow", "Evals", "Deploy"]
        for i, item in enumerate(items):
            bx = 850 + i * 115
            by = 685 - i * 52
            rounded(d, (bx, by, bx + 510, by + 70), fill=(15, 42, 49, 220), outline=(24, 214, 179, 145), radius=14)
            d.text((bx + 28, by + 18), item, fill=TEXT, font=F_SMALL)
    elif scene.kind == "dashboard":
        lanes = [("FAST", SIGNAL), ("DEEP", VIOLET), ("CODE", GOLD), ("VISION", "#7bdcff"), ("PRIVATE", "#ff9f6e")]
        for i, (label, color) in enumerate(lanes):
            x = 780 + i * 170
            rounded(d, (x, 820, x + 140, 900), fill=(15, 42, 49, 230), outline=color, radius=14)
            d.text((x + 24, 846), label, fill=color, font=F_MICRO)
    elif scene.kind == "memory":
        rounded(d, (850, 615, 1660, 910), fill=(5, 14, 16, 220), outline=(24, 214, 179, 150), radius=22)
        nodes = [(970, 720, "Sources"), (1180, 660, "Segments"), (1390, 745, "Decisions"), (1120, 835, "Workflows"), (1480, 855, "Reviews")]
        for a in nodes:
            for b in nodes:
                if a != b:
                    d.line((a[0], a[1], b[0], b[1]), fill=(24, 214, 179, 45), width=2)
        for x, y2, label in nodes:
            d.ellipse((x - 42, y2 - 42, x + 42, y2 + 42), fill=(18, 56, 62), outline=GOLD, width=2)
            d.text((x - 45, y2 + 52), label, fill=TEXT, font=F_MICRO)
    elif scene.kind == "terminal":
        draw_terminal(d, (810, 635, 790, 300), [
            "$ agent run workflow-check",
            "read AGENT-TASK.md",
            "apply safe helper patch",
            "tests: pass",
            "status: ready for review",
        ])
    elif scene.kind == "roadmap":
        draw_roadmap(d, 820, 175, scene.bullets, vertical=True)
    elif scene.kind == "cta":
        d.text((840, 690), "SUBSCRIBE", fill=SIGNAL, font=F_H2)
        d.text((840, 760), "LIKE", fill=GOLD, font=F_H2)
        d.text((840, 830), "RING THE BELL", fill=VIOLET, font=F_H2)
        d.text((70, 1000), "Practical AI builder breakdowns. No hype clips.", fill=TEXT, font=F_SMALL)

    out = BOARDS / f"scene-{scene.no:02d}.png"
    img.save(out)
    return out


def media_is_video(path: Path) -> bool:
    return path.suffix.lower() in {".webm", ".mp4", ".mov", ".m4v"}


def run(cmd: list[str]):
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def render_scene(scene: Scene, board: Path, timing: dict) -> Path:
    duration = float(timing["segment_duration"])
    audio = ROOT / "heygen" / "scenes" / f"scene-{scene.no:02d}.wav"
    out = SCENE_MP4 / f"scene-{scene.no:02d}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", f"{duration:.3f}", "-i", str(board)]
    input_index = 1
    media_inputs = []
    for slot in scene.media:
        path = REPO / slot.path
        if media_is_video(path):
            cmd += ["-stream_loop", "-1", "-i", str(path)]
        else:
            cmd += ["-loop", "1", "-framerate", "30", "-t", f"{duration:.3f}", "-i", str(path)]
        media_inputs.append((input_index, slot))
        input_index += 1
    audio_index = input_index
    cmd += ["-i", str(audio)]

    filters = ["[0:v]scale=1920:1080,format=rgba[base]"]
    current = "base"
    for n, (idx, slot) in enumerate(media_inputs):
        label = f"m{n}"
        next_label = f"v{n}"
        filters.append(
            f"[{idx}:v]scale={slot.w}:{slot.h}:force_original_aspect_ratio=increase,"
            f"crop={slot.w}:{slot.h},setsar=1,format=rgba[{label}]"
        )
        filters.append(f"[{current}][{label}]overlay={slot.x}:{slot.y}:shortest=1[{next_label}]")
        current = next_label
    filters.append(f"[{current}]format=yuv420p[v]")
    cmd += [
        "-filter_complex",
        ";".join(filters),
        "-map",
        "[v]",
        "-map",
        f"{audio_index}:a",
        "-r",
        "30",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        str(out),
    ]
    run(cmd)
    return out


def concat(scenes: list[Path]):
    concat_file = OUT / "concat.txt"
    concat_file.write_text("".join(f"file '{p.resolve()}'\n" for p in scenes))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(MASTER)])


def main():
    BOARDS.mkdir(parents=True, exist_ok=True)
    SCENE_MP4.mkdir(parents=True, exist_ok=True)
    timing_data = json.loads((ROOT / "heygen" / "scene-timing.json").read_text())
    timing = {s["scene"]: s for s in timing_data["scenes"]}
    rendered = []
    for scene in SCENES:
        board = draw_scene(scene, timing[scene.no])
        rendered.append(render_scene(scene, board, timing[scene.no]))
    concat(rendered)
    manifest = {
        "master": str(MASTER.relative_to(ROOT)),
        "scene_count": len(rendered),
        "duration_seconds": timing_data["duration"],
        "method": "Pillow boards + FFmpeg overlays + HeyGen scene audio",
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Master written: {MASTER}")


if __name__ == "__main__":
    main()

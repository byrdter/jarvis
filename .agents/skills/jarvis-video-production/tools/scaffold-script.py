#!/usr/bin/env python3
"""scaffold-script.py — create a pipeline-ready 01-script/ folder for a new video.

Generates the script artifacts pre-filled with the topic, chosen lenses, and an N-scene
skeleton (with first-line ANCHOR placeholders that split-heygen.py will consume). You then
fill in the researched, voiced script. See SCRIPTING.md.

Usage:
  python3 scaffold-script.py --project <video-dir> --topic "..." \
    --lenses "power-control,economic-futures" --scenes 8 [--title "Episode Title"]
"""
import argparse, json, pathlib, datetime

LENSES = ["power-control","economic-futures","strategic-choices","meaning-identity","social-consequences"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, help="video project dir (01-script/ created inside)")
    ap.add_argument("--topic", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--lenses", default="power-control,economic-futures")
    ap.add_argument("--scenes", type=int, default=8)
    args = ap.parse_args()

    proj = pathlib.Path(args.project); sd = proj/"01-script"; sd.mkdir(parents=True, exist_ok=True)
    title = args.title or args.topic
    lenses = [l.strip() for l in args.lenses.split(",") if l.strip()]
    n = args.scenes
    today = datetime.date.today().isoformat()

    # Standard Byrddynasty structure: avatar intro · body · CTA (penultimate) · avatar close.
    # (intro, CTA, and close are all spoken/recorded by the avatar.)
    body_n = max(1, n - 3)
    roles = ["introduction"] + [f"beat-{i}" for i in range(1, body_n+1)] + ["cta", "closing"]
    avatar = {0: True, len(roles)-2: True, len(roles)-1: True}

    INTRO_VO = (f"I'm an avatar for Dr. Terry Byrd, and today I'll be telling you about "
                f"{args.topic}. <<Hook: a stop-you-in-your-tracks opening — you can lead with the hook "
                f"and weave the self-intro in, as long as the recorded first line matches the anchor.>>")
    CTA_VO = ("Before we land the final thought, a quick favor — and on a channel like this one it "
              "genuinely matters. If you've enjoyed exploring this with me and you'd like to see more "
              "videos that take AI seriously without the hype, subscribe to the channel. If this video "
              "was worth your time, give it a like — that tells YouTube to show it to other people who "
              "care about these questions. And ring the notification bell, so you'll know the moment the "
              "next video is published. Three small actions, one big help. Thank you.")
    DEF_ANCHOR = {"introduction": "I'm an avatar for Dr. Terry Byrd",
                  "cta": "Before we land the final thought",
                  "closing": "<<first ~6 words of the closing, verbatim>>"}
    DEF_VO = {"introduction": INTRO_VO, "cta": CTA_VO}
    DEF_TREAT = {"introduction": "avatar + hyperframes beside (lower-third; seed a recurring motif)",
                 "cta": "AVATAR + CTA hyperframes: SUBSCRIBE · LIKE · RING THE BELL",
                 "closing": "avatar + hyperframes; the closing question/idea on screen"}

    # SCRIPT-STRUCTURE.md
    struct = [f"# Script Structure — {title}\n",
              f"Topic: {args.topic}\nLenses: {', '.join(lenses)}\nTarget: 10–15 min (~1,500–2,200 words)\n",
              "| # | scene | avatar | lens | ~dur | first-line ANCHOR (verbatim, unique) | treatment idea |",
              "|---|-------|--------|------|------|--------------------------------------|----------------|"]
    scenes_spec = []
    for i, role in enumerate(roles):
        name = f"{i+1:02d}-{role}"
        av = avatar.get(i, False)
        anchor = DEF_ANCHOR.get(role, "<<write the exact opening line of this scene>>")
        treat = DEF_TREAT.get(role, "<<data-viz / diagram / B-roll / symbolic / breather>>")
        lens = "—" if role == "cta" else lenses[i%len(lenses)]
        struct.append(f"| {i+1} | {name} | {'yes' if av else ''} | {lens} | ~90s | `{anchor}` | {treat} |")
        scenes_spec.append({"name": name, **({"avatar": True} if av else {}), "anchor": anchor})
    struct.append("\nNOTE: anchors must be UNIQUE and match the recorded VO verbatim — split-heygen.py "
                  "locates them in the take to split scenes. Verify against the recording before splitting.")
    (sd/"SCRIPT-STRUCTURE.md").write_text("\n".join(struct)+"\n")

    # scenes.json (split-heygen spec skeleton)
    (sd/"scenes.json").write_text(json.dumps(scenes_spec, indent=2)+"\n")

    # COMPLETE-SCRIPT.md (script + scene markers + visual notes)
    comp = [f"# {title} — Complete Script\n",
            f"<!-- topic: {args.topic} · lenses: {', '.join(lenses)} · drafted: {today} -->",
            "<!-- Voice: Dr. Terry Byrd, explorer's tone. Explore, don't predict. Thesis: "
            "Technology is neutral. Choices aren't. (see SHOW-BIBLE.md) -->\n"]
    for i, role in enumerate(roles):
        lens = "—" if role == "cta" else lenses[i%len(lenses)]
        comp += [f"## [SCENE {i+1:02d}] {role}  ({'AVATAR' if avatar.get(i) else 'graphics'} · lens: {lens})",
                 f"**VO:** {DEF_VO.get(role, '<<spoken words — start with the verbatim first-line anchor>>')}\n",
                 f"**Visual:** {DEF_TREAT.get(role, '<<treatment — see VISUAL-SOURCING.md; not everything is HyperFrames>>')}\n"]
    (sd/"COMPLETE-SCRIPT.md").write_text("\n".join(comp)+"\n")

    # VO-ONLY.md (what gets recorded in HeyGen)
    vo = [f"# {title} — VO Only (record this in HeyGen)\n",
          "<!-- Spoken words only. Each scene begins with its verbatim anchor (see SCRIPT-STRUCTURE.md). "
          "Keep a beat of silence between scenes where natural. -->\n"]
    for i, role in enumerate(roles):
        tag = " (AVATAR)" if avatar.get(i) else ""
        vo += [f"<!-- SCENE {i+1:02d} {role}{tag} -->",
               DEF_VO.get(role, "<<spoken words for this scene>>")+"\n"]
    (sd/"VO-ONLY.md").write_text("\n".join(vo)+"\n")

    # claim-source-map.md
    (sd/"claim-source-map.md").write_text(
        f"# Claim → Source Map — {title}\n\nEvery meaningful claim needs a source or be framed as "
        "interpretation. Use research-topic.py URLs.\n\n"
        "| scene | claim | source | url | confidence | lens |\n"
        "|-------|-------|--------|-----|------------|------|\n"
        "|  |  |  |  | low/med/high |  |\n\n## Claims to soften\n| claim | why | safer wording |\n|--|--|--|\n|  |  |  |\n")

    print(f"✓ scaffolded {sd}")
    for f in ["COMPLETE-SCRIPT.md","VO-ONLY.md","SCRIPT-STRUCTURE.md","claim-source-map.md","scenes.json"]:
        print(f"   - {f}")
    print(f"\n{len(roles)} scenes: avatar intro · {body_n} body · CTA (pre-filled) · avatar close. "
          f"Next: research (research-topic.py) + write, "
          f"then fill anchors, record VO-ONLY.md, then split-heygen.py --spec 01-script/scenes.json")

if __name__ == "__main__":
    main()

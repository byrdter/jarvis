#!/usr/bin/env python3
"""scaffold-script.py — create a pipeline-ready 01-script/ folder for a new video.

Generates the script artifacts pre-filled with the topic, chosen lenses, and an N-scene
skeleton (with first-line ANCHOR placeholders that split-heygen.py will consume). You then
fill in the researched, voiced script. See SCRIPTING.md.

Structure it emits: cold-open (the QUESTION) · body beats (ESCALATION) · closing (the VERDICT)
· CTA last. FACELESS by default. Both of those are load-bearing, not cosmetic — see
knowledge/NARRATIVE-STRUCTURE.md §3 and §7.1.

Usage:
  python3 scaffold-script.py --project <video-dir> --topic "..." \
    --lenses "power-control,economic-futures" --scenes 8 [--title "Episode Title"] [--avatar]
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
    ap.add_argument("--avatar", action="store_true",
                    help="face-first mode (avatar on cold open + closing + CTA). Default is "
                         "FACELESS — see RETENTION-AND-HOOKS.md §2 for the stop condition.")
    args = ap.parse_args()

    proj = pathlib.Path(args.project); sd = proj/"01-script"; sd.mkdir(parents=True, exist_ok=True)
    title = args.title or args.topic
    lenses = [l.strip() for l in args.lenses.split(",") if l.strip()]
    n = args.scenes
    today = datetime.date.today().isoformat()

    # Standard Byrddynasty structure: intro · body · closing (the VERDICT) · CTA last.
    #
    # The CTA used to be generated PENULTIMATE. Measured 2026-08-02 across all 36 builds on
    # disk (`cta-sweep.py`): every one placed the CTA at 75.5–89.6% of runtime, and 28 of 30
    # had exactly one scene after it — the verdict. This line is why. See
    # knowledge/NARRATIVE-STRUCTURE.md §7: the ask goes AFTER the payoff, never between the
    # argument and the answer.
    body_n = max(1, n - 3)
    roles = ["cold-open"] + [f"beat-{i}" for i in range(1, body_n+1)] + ["closing", "cta"]
    # FACELESS is the current mode (since 2026-07-26; see RETENTION-AND-HOOKS.md §2). No avatar
    # anywhere unless --avatar is passed, which exists only for the documented stop condition:
    # if first-30s retention drops against the face-first videos, face-first returns.
    avatar = {0: True, len(roles)-2: True, len(roles)-1: True} if args.avatar else {}

    # INFORMATION-FIRST cold open (video-production-standard.md §2). The first frame carries
    # something concrete the viewer can READ, and the VO is about that thing. No self-ID, no
    # "today we'll explore", no bio — those are the DELETE FOREVER register, and this stub used
    # to pre-write them into every script. First-person PLURAL throughout.
    INTRO_VO = (f"<<0:00 — THE CONCRETE THING. Name the document / filing / number / headline "
                f"that is on screen right now, and say the sentence that makes it strange. "
                f"Topic: {args.topic}.>>\n"
                f"<<0:00–0:20 — THE HOOK. The most provocative concrete stake, as a PARADOX where "
                f"possible: two facts that cannot both be true. Reveal FACTS freely; withhold "
                f"MEANING. Consider the negation ladder: 'Not because X. Not because Y. Because—'>>\n"
                f"<<0:20–0:35 — RE-OPEN THE LOOP. End on a NAMED QUESTION the viewer cannot answer "
                f"alone — not the thesis, and not an agenda. This question must survive the whole "
                f"runtime (NARRATIVE-STRUCTURE.md §3①); its answer belongs in the closing scene, "
                f"NOT here.>>")
    # NOTE: this runs AFTER the verdict has landed. It must never defer the payoff — the old
    # stub opened "Before we land the final thought", which is the interrupt this channel was
    # measured doing in every build (NARRATIVE-STRUCTURE.md §7.1). Keep it short; the ask is
    # strongest when it names what the viewer just got.
    CTA_VO = ("<<One line naming what they just watched — e.g. 'You can't fix what you can't "
              "name.'>> If you want more of this — one hard question taken apart carefully, with "
              "no side to sell you — subscribe. If this one earned it, hit like; that's the signal "
              "that shows it to the next person asking the same question.")
    CLOSE_VO = ("<<THE VERDICT — the answer to the cold-open question, stated once, plainly, "
                "unhedged. This is the payoff the whole runtime withheld; nothing may preview it "
                "earlier (NARRATIVE-STRUCTURE.md §3④). Then the consequence, then out.>>")
    DEF_ANCHOR = {"cold-open": "<<first ~6 words of the cold open, verbatim>>",
                  "cta": "<<first ~6 words of the CTA, verbatim>>",
                  "closing": "<<first ~6 words of the closing, verbatim>>"}
    DEF_VO = {"cold-open": INTRO_VO, "closing": CLOSE_VO, "cta": CTA_VO}
    DEF_TREAT = {"cold-open": "CONCRETE ARTIFACT IN FRAME ONE — a named document / filing / real "
                              "number / labelled chart, over the darkened moving bed. Never a "
                              "gradient, particle field or kicker label alone: mood is not "
                              "information. Seed the spine motif here.",
                 "cta": "the spine device in its resolved/final state; no naked text",
                 "closing": "the verdict landing inside an artifact — the spine completing, the "
                            "row resolving, the ledger closing"}

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
            "<!-- Voice: first-person PLURAL throughout, no singular exception (FACELESS mode). "
            "Explore, don't predict. Thesis: Technology is neutral. Choices aren't. (SHOW-BIBLE.md) -->",
            "<!-- STRUCTURE: cold open = the QUESTION · beats = ESCALATION (each must raise the cost "
            "of not knowing, not just add support) · REVERSAL at 40-55% · closing = the VERDICT · "
            "CTA last. The answer may not appear before the closing. NARRATIVE-STRUCTURE.md -->\n"]
    for i, role in enumerate(roles):
        lens = "—" if role == "cta" else lenses[i%len(lenses)]
        comp += [f"## [SCENE {i+1:02d}] {role}  ({'AVATAR' if avatar.get(i) else 'graphics'} · lens: {lens})",
                 f"**VO:** {DEF_VO.get(role, '<<spoken words — start with the verbatim first-line anchor>>')}\n",
                 f"**Visual:** {DEF_TREAT.get(role, '<<treatment — see VISUAL-SOURCING.md; not everything is HyperFrames>>')}\n"]
    (sd/"COMPLETE-SCRIPT.md").write_text("\n".join(comp)+"\n")

    # VO-ONLY.md (what gets recorded in HeyGen)
    vo = [f"# {title} — VO Only (the recorded/synthesised script)\n",
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
    mode = "FACE-FIRST (avatar)" if args.avatar else "FACELESS"
    print(f"\n{len(roles)} scenes · {mode}: cold-open · {body_n} body · closing (THE VERDICT) · CTA last.")
    print("   Next: research-topic.py + write · fill anchors · record VO-ONLY.md")
    print("   THEN, before recording: python3 tools/narrative-measure.py on the draft transcript —")
    print("   first payoff >=40% of runtime, spine silent-gap <=90s (NARRATIVE-STRUCTURE.md §8).")
    print("   Then: split-heygen.py --spec 01-script/scenes.json")

if __name__ == "__main__":
    main()

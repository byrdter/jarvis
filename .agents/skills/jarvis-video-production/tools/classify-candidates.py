#!/usr/bin/env python3
"""
Classify pass — read what the ratchet surfaced and say what it actually IS.

    python3 classify-candidates.py                      # newest candidates-*.csv
    python3 classify-candidates.py --file path.csv
    python3 classify-candidates.py --watchlist          # backfill: classify the whole watchlist
    python3 classify-candidates.py --model claude-haiku-4-5-20251001 --batch 30

WHY THIS EXISTS
    outlier-ratchet.py deliberately does NOT classify topic, because the only cheap signal
    (word presence) cannot do it. On 2026-07-29 that limitation produced, in one session:
      * demand-probe scoring RESUME COACHING as 31.16x demand for an AI-and-jobs video
      * demand-probe scoring ANTI-WORK content as 41.29x for the same
      * the ratchet's own ai_hint tagging "Every Illegal Operating System EXPL-AI-NED" and
        "Peter Hitchens EXPL-AI-NS Why Britain Is Finished" as AI content, because a bare
        "ai" matches inside ordinary English words
    Word matching cannot read. This pass can. It is the step that turns a ranked list of
    outliers into a list we can act on.

WHAT IT DECIDES, PER VIDEO
    about_ai   ai | adjacent | no       "adjacent" = not about AI, but a SHAPE that could
                                        carry an AI payload. This is the valuable category:
                                        the anti-work lane (8-41x, vs 2-11x for AI-and-jobs)
                                        was found exactly here, as drift, on 2026-07-29.
    evergreen  yes | no                 no = pegged to a date, a news event, or a model
                                        version. A dated outlier still teaches the SHAPE.
    shape      the retention structure  (see SHAPES below -- from the competitor teardowns)
    adapt      one sentence: how WE would carry an AI payload in this shape, or "-"
    why        the classifier's own reasoning, so a human can overrule it

CALIBRATION HISTORY — the prompt is the product; read this before editing it
    v1 (2026-07-29) said "Do not inflate 'adjacent'; reserve it for structures genuinely worth
    stealing." That one sentence made the pass FAIL AT ITS ONE JOB. On the 54-channel
    watchlist it marked the entire anti-work lane "no" and binned it as churn -- including
    "How a 9 to 5 job takes over your life" at 232.35x, THE HIGHEST OUTLIER ON THE WHOLE
    WATCHLIST, and the exact lane this tooling was built to surface. It also over-fired on
    evergreen, marking Explainer Chris's proven model-roundup format and both data-centre
    explainers as DATED for naming ChatGPT.
    v2 flipped both: "adjacent" is now the generous default for any work/money/status/
    institution video, and evergreen asks "worth watching in twelve months?" rather than
    "mentions something current?". Result on the same input: BUILD 1 -> 26, ADAPT 0 -> 17,
    "no" 8 -> 3 (a personal investing vlog and two meme compilations -- correct).
    v2 IS DELIBERATELY GENEROUS ON "adjacent". Both errors are possible; they are not equally
    costly. A false "adjacent" costs two seconds of reading a printed `adapt` line. A false
    "no" silently deletes a 232x finding and nobody ever learns it existed. Err loud.

THIS IS A JUDGEMENT, NOT A MEASUREMENT
    The outlier score is measured. Everything this pass adds is a model reading a title.
    It prints `why` for exactly that reason. Titles are also thin evidence -- a title alone
    cannot always reveal a video's structure, so `shape` is the softest field here and should
    be treated as a guess until someone watches the video. Never auto-drop on this output;
    rank with it, then read.
"""
import os, sys, json, csv, glob, subprocess, argparse, datetime, re

HERE  = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(HERE, "ratchet")
MODEL = "claude-sonnet-5"
BATCH = 25
HIGH_SKIP = 15.0   # an outlier this big marked 'no' gets shouted, not truncated

# The structures the 2026-07-29 competitor teardowns found in EVERY proven long-form video.
SHAPES = {
 "mystery":      "a concrete unexplained thing held open across the runtime (High Yield: why did Meta raze $70M?)",
 "scale-ladder": "one quantity climbed rung by rung, each pinned to a physical twin (Big Data Factor)",
 "framework":    "a numbered set promised up front and worked through (Fractal Philosophy's '3 things')",
 "comparison":   "N things ranked or contrasted against each other (Explainer Chris: every AI model)",
 "verdict":      "a contestable claim argued to a conclusion",
 "list":         "enumerated items, little connective argument (weakest structure; often a churn format)",
 "explainer":    "how a thing works, start to finish, no withheld payoff",
 "clip":         "an excerpt of someone talking; the channel did not build it",
 "reaction":     "commentary riding on someone else's artifact",
}

PROMPT = """You are classifying YouTube videos that over-performed their channel's subscriber
count, for a faceless documentary channel called "Understanding AI".

## about_ai — "ai" | "adjacent" | "no"

"ai"        The video is about AI.

"adjacent"  NOT about AI, but its STRUCTURE or EMOTIONAL REGISTER could carry an AI subject.
            BE GENEROUS HERE. This category is the entire reason this pass exists.
            A high-performing video about work, money, status, education, institutions, or how
            systems treat ordinary people is almost always "adjacent" — those are the registers
            an AI story can be told in.
            Worked example: "Hard Work is a Scam" and "How a 9 to 5 job takes over your life"
            are BOTH "adjacent". They are grievance stories about the deal between people and
            employers — which is exactly how you frame a video about AI quietly expanding
            someone's job duties without changing their title or pay.

"no"         RESERVE THIS. Use it only when there is no transferable structure at all:
            relationship/dating advice, celebrity gossip, meme compilations, reaction clips,
            pure product tutorials. If you find yourself marking a video "no" purely because
            its topic is not AI, it is probably "adjacent" instead.

## evergreen — "yes" | "no"

The test is: WOULD THIS VIDEO STILL BE WORTH WATCHING IN TWELVE MONTHS?
It is NOT "does the title mention anything that exists today."

"yes"  Naming ChatGPT, a company, or a real ongoing phenomenon is FINE. Structural or
       explanatory subjects are evergreen: how data centres work, why models hallucinate,
       whether AI can be conscious, how AI changes job boundaries, what AI cannot do.
"no"   Reserve for genuine expiry: an explicit future date ("by 2030", "in 24 months"), a
       roundup of current model versions that a new release invalidates, a market call
       ("the bubble is about to burst"), or a specific news event.

Do not mark something "no" merely because it is topical or names a current company.

## shape

One of: {shapes}

## Output

For each video return an object with EXACTLY these keys:
  "n"         the video's number, as given
  "about_ai"  "ai" | "adjacent" | "no"
  "evergreen" "yes" | "no"
  "shape"     one of the shapes above
  "adapt"     ONE sentence on how this channel could carry an AI subject in this shape.
              Use "-" only if there is genuinely nothing to steal.
  "why"       ONE short sentence justifying about_ai and evergreen.

Return ONLY a JSON array. No prose, no markdown fences.

VIDEOS:
{videos}"""


def newest_candidates():
    fs = sorted(glob.glob(os.path.join(STORE, "candidates-*.csv")))
    if not fs:
        sys.exit("No candidates-*.csv in ratchet/. Run: outlier-ratchet.py --monitor")
    return fs[-1]


def load_rows(path, watchlist=False):
    if watchlist:
        w = json.load(open(os.path.join(STORE, "watchlist.json"), encoding="utf8"))
        return [{"title": m.get("found_title", ""), "channel": m.get("title", ""),
                 "outlier": m.get("found_score", 0), "subs": m.get("subs", 0),
                 "published": m.get("added", ""), "url": m.get("found_video", ""),
                 "found_via": m.get("lane", "")}
                for m in w.values() if m.get("found_title")]
    with open(path, encoding="utf8") as fh:
        return list(csv.DictReader(fh))


def ask(prompt, model):
    """One CLI subprocess. Uses the OAuth token, so no API charge (CLAUDE.md Phase 3A)."""
    p = subprocess.run(["claude", "-p", prompt, "--model", model],
                       capture_output=True, text=True, timeout=600)
    if p.returncode != 0:
        raise RuntimeError(f"claude exited {p.returncode}: {p.stderr[:300]}")
    return p.stdout.strip()


def parse_array(text):
    """LLMs fence JSON even when told not to. Strip, then find the outermost array."""
    t = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    i, j = t.find("["), t.rfind("]")
    if i == -1 or j == -1:
        raise ValueError("no JSON array in reply")
    return json.loads(t[i:j + 1])


def classify(rows, model, batch):
    shapes = " | ".join(SHAPES)
    out = {}
    for start in range(0, len(rows), batch):
        grp = rows[start:start + batch]
        listing = "\n".join(
            f'{start+k+1}. "{r["title"]}"  [channel: {r.get("channel","?")}]'
            for k, r in enumerate(grp))
        prompt = PROMPT.format(shapes=shapes, videos=listing)
        print(f"  classify {start+1}-{start+len(grp)} of {len(rows)} …", flush=True)

        got = None
        for attempt in (1, 2):
            try:
                reply = ask(prompt if attempt == 1 else
                            prompt + "\n\nYour previous reply was not valid JSON. "
                                     "Return ONLY the JSON array.", model)
                got = parse_array(reply)
                break
            except Exception as e:
                print(f"    attempt {attempt} failed: {str(e)[:90]}")
        if got is None:
            # Never silently drop. An unclassified row is a visible gap, not a "no".
            print(f"    !! batch {start+1}-{start+len(grp)} UNCLASSIFIED — left in output as such")
            continue
        for o in got:
            try:
                out[int(o["n"])] = o
            except (KeyError, ValueError, TypeError):
                pass

    for k, r in enumerate(rows, 1):
        c = out.get(k, {})
        r["about_ai"]  = c.get("about_ai", "UNCLASSIFIED")
        r["evergreen_llm"] = c.get("evergreen", "?")
        r["shape"]     = c.get("shape", "?")
        r["adapt"]     = c.get("adapt", "")
        r["why"]       = c.get("why", "")
    return rows


def report(rows, model, src):
    def score(r):
        try:    return float(r.get("outlier", 0) or 0)
        except (TypeError, ValueError): return 0.0

    build = [r for r in rows if r["about_ai"] == "ai"       and r["evergreen_llm"] == "yes"]
    adapt = [r for r in rows if r["about_ai"] == "adjacent" and r["evergreen_llm"] == "yes"]
    dated = [r for r in rows if r["about_ai"] in ("ai", "adjacent") and r["evergreen_llm"] != "yes"]
    skip  = [r for r in rows if r["about_ai"] == "no"]
    unk   = [r for r in rows if r["about_ai"] == "UNCLASSIFIED"]
    for g in (build, adapt, dated):
        g.sort(key=score, reverse=True)

    W = 100
    print(f"\n{'='*W}\nCLASSIFIED — {len(rows)} candidates · {model} · {os.path.basename(src)}\n"
          f"The outlier score is MEASURED. Everything below it is a model reading a title —\n"
          f"'why' is printed so you can overrule it. Shape is the softest field.\n{'='*W}")

    def block(title, rows_, show_adapt):
        print(f"\n{title}  ({len(rows_)})")
        if not rows_:
            print("   —")
        for r in rows_:
            print(f"  {score(r):7.2f}x  [{r['shape']}]  {r['title'][:72]}")
            print(f"           {r.get('channel','?')[:24]:24} {r.get('url','')}")
            if r.get("why"):
                print(f"           why:   {r['why'][:88]}")
            if show_adapt and r.get("adapt") and r["adapt"] != "-":
                print(f"           ADAPT: {r['adapt'][:88]}")

    block("BUILD — about AI, evergreen. Directly usable.", build, False)
    block("ADAPT — not about AI, but the SHAPE is worth stealing.", adapt, True)
    block("DATED — right subject, fails the evergreen constraint. The SHAPE may still teach.", dated, True)
    # SELF-CHECK. On 2026-07-29 the first version of this prompt binned "How a 9 to 5 job
    # takes over your life" (232x, the highest outlier on the whole watchlist) as SKIP —
    # the exact anti-work lane the tool was built to find. A big number in SKIP is the most
    # likely place this pass is WRONG, so it gets shouted rather than truncated away.
    loud = [r for r in skip if score(r) >= HIGH_SKIP]
    quiet = [r for r in skip if score(r) < HIGH_SKIP]
    if loud:
        loud.sort(key=score, reverse=True)
        print(f"\n!! HIGH-OUTLIER SKIPS ({len(loud)}) — {HIGH_SKIP}x+ and marked 'no'. "
              f"VERIFY THESE; it is where this pass most often errs.")
        for r in loud:
            print(f"  {score(r):7.2f}x  {r['title'][:74]}")
            print(f"           why: {r.get('why','')[:86]}")
    print(f"\nSKIP  ({len(quiet)}) — off-topic or churn")
    for r in quiet[:12]:
        print(f"  {score(r):7.2f}x  {r['title'][:76]}")
    if len(quiet) > 12:
        print(f"        … and {len(quiet)-12} more")
    if unk:
        print(f"\n!! UNCLASSIFIED ({len(unk)}) — the model failed on these; they were NOT dropped")
        for r in unk:
            print(f"  {score(r):7.2f}x  {r['title'][:76]}")


def markdown(rows, model, src, path, watched=None):
    """A digest for the morning email. Same content as the terminal report."""
    def score(r):
        try:    return float(r.get("outlier", 0) or 0)
        except (TypeError, ValueError): return 0.0
    groups = [
        ("BUILD — about AI, evergreen. Directly usable.",
         [r for r in rows if r["about_ai"] == "ai" and r["evergreen_llm"] == "yes"], False),
        ("ADAPT — not about AI, but the shape is worth stealing.",
         [r for r in rows if r["about_ai"] == "adjacent" and r["evergreen_llm"] == "yes"], True),
        ("DATED — right subject, fails the evergreen constraint. The shape may still teach.",
         [r for r in rows if r["about_ai"] in ("ai","adjacent") and r["evergreen_llm"] != "yes"], True),
    ]
    skip = [r for r in rows if r["about_ai"] == "no"]
    unk  = [r for r in rows if r["about_ai"] == "UNCLASSIFIED"]
    loud = sorted([r for r in skip if score(r) >= HIGH_SKIP], key=score, reverse=True)

    L = [f"# Outlier digest — {datetime.date.today().isoformat()}", ""]
    L.append(f"{len(rows)} candidates" + (f" from {watched} channels watched" if watched else "")
             + f" · classified by {model}")
    L.append("")
    L.append("`outlier` = views ÷ the **posting** channel's subscriber count. That number is measured. "
             "Everything else here is a model reading a title — `why` is shown so it can be overruled.")
    L.append("")
    for head, rs, show_adapt in groups:
        rs.sort(key=score, reverse=True)
        L += [f"## {head}  ({len(rs)})", ""]
        if not rs:
            L += ["_none_", ""]
        for r in rs:
            L.append(f"**{score(r):.2f}×** · `{r['shape']}` · [{r['title']}]({r.get('url','')})  ")
            L.append(f"{r.get('channel','?')} · {r.get('subs','?')} subs  ")
            if r.get("why"):
                L.append(f"*why:* {r['why']}  ")
            if show_adapt and r.get("adapt") and r["adapt"] != "-":
                L.append(f"**adapt:** {r['adapt']}  ")
            L.append("")
    if loud:
        L += [f"## ⚠ High-outlier skips ({len(loud)}) — verify these", "",
              "These scored well above the floor and were still marked off-topic. "
              "This is where the classifier most often errs.", ""]
        for r in loud:
            L.append(f"**{score(r):.2f}×** · [{r['title']}]({r.get('url','')}) — *{r.get('why','')}*  ")
        L.append("")
    L += [f"## Skipped ({len(skip)-len(loud)})", ""]
    for r in sorted([r for r in skip if score(r) < HIGH_SKIP], key=score, reverse=True)[:15]:
        L.append(f"- {score(r):.2f}× {r['title']}")
    if unk:
        L += ["", f"## Unclassified ({len(unk)}) — the model failed; NOT dropped", ""]
        for r in unk:
            L.append(f"- {score(r):.2f}× {r['title']}")
    open(path, "w", encoding="utf8").write("\n".join(L) + "\n")
    return path


def main():
    ap = argparse.ArgumentParser(description="Classify ratchet candidates with an LLM read.")
    ap.add_argument("--file")
    ap.add_argument("--watchlist", action="store_true", help="classify the whole watchlist instead")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--batch", type=int, default=BATCH)
    ap.add_argument("--out")
    ap.add_argument("--md", help="also write a markdown digest here (for the morning email)")
    a = ap.parse_args()

    src  = "watchlist.json" if a.watchlist else (a.file or newest_candidates())
    rows = load_rows(None if a.watchlist else src, a.watchlist)
    if not rows:
        sys.exit("Nothing to classify.")

    rows = classify(rows, a.model, a.batch)
    report(rows, a.model, src)

    stamp = datetime.date.today().isoformat()
    out = a.out or os.path.join(STORE, f"classified-{stamp}.csv")
    keys = list(dict.fromkeys(list(rows[0].keys())))
    with open(out, "w", newline="", encoding="utf8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    print(f"\n  -> {out}")
    if a.md:
        n = len(json.load(open(os.path.join(STORE, "watchlist.json"), encoding="utf8")))
        markdown(rows, a.model, src, a.md, watched=n)
        print(f"  -> {a.md}")


if __name__ == "__main__":
    main()

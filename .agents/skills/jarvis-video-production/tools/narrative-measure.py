#!/usr/bin/env python3
"""
narrative-measure — the SELF-teardown. Implements NARRATIVE-STRUCTURE.md §8.

`teardown.py` measures someone else's proven video from YouTube captions.
This measures OURS, from the word-level transcript of our own master, using the
same vocabulary so the two are directly comparable — plus the three devices
teardown.py cannot see because they need authorial intent declared:

  PAYOFF POSITION  where the video first states its own answer. The single
                   strongest predictor we have. Essay = early. Story = late.
  SPINE PERSISTENCE  the longest stretch with no spine token. A spine named
                   once and dropped is not a spine.
  CTA PLACEMENT    where the subscribe block sits relative to the payoff.

    python3 narrative-measure.py <transcript.json> [--dur SECONDS] [--spec narrative.json]
    python3 narrative-measure.py <scenes-dir>      # finds full-transcript.json

Transcript = a list of {"text","start","end"} — what transcribe.py / cue.py already use.

The spec is a small JSON file beside the script, all keys optional:
    {
      "payoff":  ["the wrong word", "is the exact opposite"],   # phrases that state the answer
      "spine":   ["trial","verdict","evidence","witness"],      # the carried device
      "cta":     ["subscribe","hit like","ring the bell"],
      "runtime": 935.182
    }

Without a spec you still get pacing, negation, loops and beat cadence. WITH a spec
you get the three that matter. Declaring the payoff phrase is the point of the
exercise — if you cannot name the sentence that gives the answer away, the script
is not finished.

This script reports. It does not pass or fail. The gate is prepublish-check.py.
"""
import json, os, re, sys
from collections import Counter

NEG = re.compile(
    r"^(but|not|never|isn't|aren't|don't|doesn't|didn't|can't|won't|wasn't|"
    r"nobody|nothing|no|wrong|failed|fails|instead|actually|however|yet)$")
LOOP_SOLO = {"why", "whether"}
LOOP_PAIR = {"happens", "should", "does", "do", "if", "a", "the", "it", "that", "makes"}


def ts(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def norm(t):
    return t.lower().strip(".,;:!?\"'“”‘’")


def load(path):
    if os.path.isdir(path):
        for c in ("full-transcript.json", "transcript.json"):
            if os.path.exists(os.path.join(path, c)):
                path = os.path.join(path, c)
                break
        else:
            sys.exit(f"no transcript json in {path}")
    return json.load(open(path)), path


def find(words, low, phrase):
    p = [norm(x) for x in phrase.split() if norm(x)]
    return [i for i in range(len(low) - len(p) + 1) if low[i:i + len(p)] == p]


def ctx(words, i, before=5, after=13):
    return " ".join(w["text"] for w in words[max(0, i - before):i + after])


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    words, src = load(args[0])
    low = [norm(w["text"]) for w in words]

    spec = {}
    if "--spec" in sys.argv:
        spec = json.load(open(sys.argv[sys.argv.index("--spec") + 1]))
    else:
        side = os.path.join(os.path.dirname(os.path.abspath(src)), "narrative.json")
        if os.path.exists(side):
            spec = json.load(open(side))

    dur = spec.get("runtime")
    if "--dur" in sys.argv:
        dur = float(sys.argv[sys.argv.index("--dur") + 1])
    if not dur:
        dur = words[-1]["end"]
    mins = dur / 60

    print(f"# narrative-measure — {os.path.basename(src)}")
    print(f"  runtime {ts(dur)} ({dur:.1f}s) · {len(words)} words · {len(words)/mins:.0f} wpm\n")

    # --- PAYOFF POSITION -----------------------------------------------------
    print("## PAYOFF POSITION — where the video answers itself")
    if spec.get("payoff"):
        best = None
        for ph in spec["payoff"]:
            for i in find(words, low, ph):
                pct = words[i]["start"] / dur * 100
                print(f"  [{ts(words[i]['start'])}] {pct:5.1f}%  \"{ph}\"")
                print(f"           ...{ctx(words, i)}")
                if best is None or words[i]["start"] < best[0]:
                    best = (words[i]["start"], ph, pct)
        if best:
            print(f"\n  FIRST PAYOFF at {ts(best[0])} = {best[2]:.1f}% of runtime")
            print("  §2: under 15% is an essay — the rest is support, and support does not hold.")
        else:
            print("  none of the declared payoff phrases were spoken (check wording)")
    else:
        print("  no payoff declared in spec — THIS IS THE MEASUREMENT THAT MATTERS. Declare it.")

    # --- SPINE PERSISTENCE ---------------------------------------------------
    print("\n## SPINE PERSISTENCE — is the device carried or abandoned?")
    if spec.get("spine"):
        terms = {t.lower() for t in spec["spine"]}
        hits = [(w["start"], low[i]) for i, w in enumerate(words) if low[i] in terms]
        if hits:
            for t, term in hits:
                print(f"  [{ts(t)}] {term}")
            marks = [0.0] + [h[0] for h in hits] + [dur]
            gaps = [(marks[i + 1] - marks[i], marks[i], marks[i + 1]) for i in range(len(marks) - 1)]
            g = max(gaps)
            print(f"\n  {len(hits)} mentions · {len(hits)/mins:.2f}/min")
            print(f"  LONGEST SILENT GAP {g[0]:.0f}s ({g[0]/dur*100:.0f}% of runtime) "
                  f"— {ts(g[1])} to {ts(g[2])}")
            print("  §5: a gap over ~90s means the viewer has no idea where they are.")
        else:
            print("  spine terms never spoken — the device does not exist in the VO")
    else:
        print("  no spine declared in spec")

    # --- CTA -----------------------------------------------------------------
    print("\n## CTA PLACEMENT")
    cta = spec.get("cta") or ["subscribe", "hit like", "ring the bell", "hit subscribe"]
    marks = sorted({words[i]["start"] for ph in cta for i in find(words, low, ph)})
    if marks:
        print(f"  block {ts(marks[0])}–{ts(marks[-1])} "
              f"({marks[0]/dur*100:.0f}%–{marks[-1]/dur*100:.0f}%) · {marks[-1]-marks[0]:.0f}s span")
        print("  §7: it belongs AFTER the payoff. Ahead of it, it interrupts the one "
              "thing the viewer stayed for.")
    else:
        print("  no CTA markers found")

    # --- COMPARABLE DEVICE METRICS ------------------------------------------
    neg = [w for i, w in enumerate(words) if NEG.match(low[i])]
    c = Counter(low[i] for i, w in enumerate(words) if NEG.match(low[i]))
    print(f"\n## NEGATION  {len(neg)} hits · {len(neg)/mins:.1f}/min "
          f"(Mackard 4.0 · Universal Resilience 3.1 · Agent Harness 1.3)")
    print("  " + " · ".join(f"{k}({v})" for k, v in c.most_common(10)))

    loops = []
    for i, t in enumerate(low):
        if t in LOOP_SOLO or (t in ("what", "how") and i + 1 < len(low) and low[i + 1] in LOOP_PAIR):
            loops.append(i)
    print(f"\n## LOOP-OPENERS  {len(loops)} · {len(loops)/mins:.2f}/min "
          f"(Mackard 0.6 · Universal Resilience 1.1)")
    for i in loops[:14]:
        print(f"  [{ts(words[i]['start'])}] ...{ctx(words, i, 4, 12)}")
    if len(loops) > 14:
        print(f"  (+{len(loops)-14} more)")

    print("\n## REVERSAL WINDOW (40–55%) — read it; is there a turn here?")
    lo, hi = dur * .40, dur * .55
    seg = " ".join(w["text"] for w in words if lo <= w["start"] < hi)
    print(f"  {ts(lo)}–{ts(hi)}")
    print("  " + seg[:900] + ("…" if len(seg) > 900 else ""))

    print("\n## PACING (words per minute)")
    m = 0
    while m * 60 < dur:
        n = len([w for w in words if m * 60 <= w["start"] < (m + 1) * 60])
        print(f"  {m:2d}:00  {n:3d}  " + "#" * int(n / 4))
        m += 1


if __name__ == "__main__":
    main()

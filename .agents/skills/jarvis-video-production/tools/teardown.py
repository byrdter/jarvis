#!/usr/bin/env python3
"""
Teardown — implements RETENTION-AND-HOOKS.md §7.6. The second half of the outlier scan.

`outlier-scan.py` finds WHICH videos out-travelled their own distribution. This finds
out WHY: it pulls a proven video apart into a structural spec — cold open verbatim,
beat map, pacing curve, where the loop is named, where the reversal lands — so the
shape can be fused (§7.2), not cloned.

    python3 teardown.py <url|video-id>          # one video
    python3 teardown.py --from-outliers 5       # top 5 candidates in outliers.csv
    python3 teardown.py <url> --refresh         # ignore cache

Writes teardowns/<id>.md: EVIDENCE (mechanical, from this script) followed by an
ANALYSIS template (judgment, filled in by the agent reading the file). The split is
deliberate — the script never guesses at intent, and the template keeps every teardown
comparable to every other one.

WHAT THIS IS NOT: it does not tell you to make the same video. Per §7.2 cloning a
single outlier puts us head-to-head with a winner on a bigger channel. The output is
raw material for a FUSION, and the §7.4 caveat applies — these are 15-27 min videos on
30K-900K-sub channels; borrow the shape, not the runtime.

Captions only (yt-dlp auto-subs, free). No download, no Whisper, no API keys.
Cache lives in raw/teardown/ beside this script.
"""
import subprocess, sys, os, re, csv, json, glob
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "raw", "teardown")
OUT = os.path.join(HERE, "teardowns")

COLD_OPEN = 45      # seconds of opening to quote verbatim -- §2 lives in the first 30-35s
REVERSAL = (0.40, 0.55)   # §4 mid-video reversal window, as a fraction of runtime

# §7.4: what breaks out is NEGATION, not news. These are the surface markers of a
# limit / correction / reversal. Hits are reported with timestamps, never scored --
# density is a place to LOOK, not a verdict.
NEGATION = r"""can't cannot couldn't doesn't don't didn't isn't aren't won't wouldn't
    never nobody no-one none fails failed failure wrong mistaken myth misconception
    limit limits ceiling wall barrier impossible breaks broken debunk actually
    turns-out but however except unless"""

# Loop-openers: the phrasings that NAME a question without answering it (§2 step 4, §3).
# Multi-word entries are matched as phrases.
LOOP = r"""why how what-if what-happens who-decides nobody-knows we-don't-know
    the-question the-problem here's-the-thing it-turns-out the-catch the-twist
    which-raises the-reason no-one-can what-nobody"""


def sh(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, check=False, **kw)


def fetch(vid, refresh=False):
    """Cache info-json + auto-captions for one video. Returns (info dict, vtt path)."""
    d = os.path.join(CACHE, vid)
    os.makedirs(d, exist_ok=True)
    info = os.path.join(d, f"{vid}.info.json")
    if refresh or not os.path.exists(info):
        print(f"  fetch   {vid} ...", flush=True)
        # `en.*` expands to en, en-US and en-orig -- THREE subtitle downloads for one video.
        # YouTube 429s the third, yt-dlp aborts, and the info-json is never written. The old
        # code then reported "private, removed, or bad id" for a perfectly public video, which
        # is how this cost an hour on 2026-08-11. One track is all parse_vtt ever reads.
        sh(["yt-dlp", "--no-update", "--skip-download", "--write-info-json",
            "--write-auto-subs", "--write-subs", "--sub-langs", "en-orig,en",
            "--ignore-errors",          # a subtitle 429 must not cost us the metadata
            "--sub-format", "vtt", "-o", os.path.join(d, "%(id)s"),
            f"https://www.youtube.com/watch?v={vid}"])
    if not os.path.exists(info):
        # FALLBACK: captions may have landed while the info-json did not. Metadata is one
        # cheap call and losing the whole teardown to a rate limit is absurd.
        got = sorted(glob.glob(os.path.join(d, f"{vid}*.vtt")))
        print(f"  retry   {vid} metadata only ({'captions present' if got else 'no captions'})",
              flush=True)
        r = sh(["yt-dlp", "--no-update", "--skip-download", "--dump-json",
                f"https://www.youtube.com/watch?v={vid}"])
        if r.returncode == 0 and r.stdout.strip():
            open(info, "w", encoding="utf8").write(r.stdout)
        else:
            print(f"  !! {vid}: metadata fetch failed. yt-dlp said:")
            print("     " + (r.stderr or "").strip().splitlines()[-1][:160] if r.stderr else
                  "     (no stderr)")
            return None, None
    vtts = sorted(glob.glob(os.path.join(d, f"{vid}*.vtt")))
    # prefer a manual track (no "-orig", shorter lang tag) over auto-generated
    vtts.sort(key=lambda p: ("auto" in p, len(p)))
    return json.load(open(info, encoding="utf8")), (vtts[0] if vtts else None)


def parse_vtt(path):
    """VTT -> [(seconds, word)], one timestamp per word (interpolated across each cue).

    YouTube auto-captions ROLL: each cue repeats the tail of the previous one. Dedupe at
    the word level -- find the longest overlap between the accumulated tail and the
    incoming cue, append only what is new."""
    if not path:
        return []
    ts = re.compile(r"(\d+):(\d\d):(\d\d)[.,](\d+)\s+-->\s+(\d+):(\d\d):(\d\d)[.,](\d+)")
    out = []
    for block in open(path, encoding="utf8").read().split("\n\n"):
        m = ts.search(block)
        if not m:
            continue
        g = [int(x.ljust(3, "0")[:3]) if i % 4 == 3 else int(x) for i, x in enumerate(m.groups())]
        t0 = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        t1 = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        body = re.sub(r"<[^>]+>", " ", block[m.end():])
        body = re.sub(r"align:\S+|position:\S+", " ", body)
        cue = [w for w in body.replace("\n", " ").split() if w]
        if not cue:
            continue
        tail = [w.lower() for w in [x[1] for x in out[-len(cue) * 2:]]]
        low = [w.lower() for w in cue]
        overlap = 0
        for k in range(min(len(tail), len(low)), 0, -1):
            if tail[-k:] == low[:k]:
                overlap = k
                break
        new = cue[overlap:]
        if not new:
            continue
        step = (t1 - t0) / max(len(new), 1)
        for i, w in enumerate(new):
            out.append((round(t0 + i * step, 2), w))
    return out


def hms(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def lines(words, lo, hi, per=13):
    """Render [(t,w)] between lo..hi as timestamped lines."""
    seg = [(t, w) for t, w in words if lo <= t < hi]
    out = []
    for i in range(0, len(seg), per):
        chunk = seg[i:i + per]
        out.append(f"[{hms(chunk[0][0])}] " + " ".join(w for _, w in chunk))
    return out


def hits(words, terms):
    """Timestamped matches for a term list -> [(t, term, index)]. Hyphenated entries
    match as phrases."""
    single = {t for t in terms if "-" not in t}
    phrases = [t.replace("-", " ").split() for t in terms if "-" in t]
    norm = [re.sub(r"[^a-z']", "", w.lower()) for _, w in words]
    found = []
    for i, n in enumerate(norm):
        if n in single:
            found.append((words[i][0], n, i))
    for pw in phrases:
        for i in range(len(norm) - len(pw)):
            if norm[i:i + len(pw)] == pw:
                found.append((words[i][0], " ".join(pw), i))
    return sorted(found)


def context(words, found, cap=24, span=7):
    """Render hits with surrounding words. A bare list of `how`/`why` is noise; the
    clause around it is the evidence -- you can only tell an opened loop from ordinary
    usage by reading it."""
    out, last = [], -99
    for t, term, i in found:
        if i - last < span:          # collapse hits inside the same clause
            continue
        last = i
        a, b = max(0, i - span), min(len(words), i + span + 1)
        txt = " ".join(w for _, w in words[a:i]) + f" «{words[i][1]}» " + \
              " ".join(w for _, w in words[i + 1:b])
        out.append(f"[{hms(t)}] ...{txt.strip()}...")
        if len(out) >= cap:
            out.append(f"(+{len(found) - cap} more)")
            break
    return out


def per_minute(words, dur):
    """Words-per-minute curve -- pacing. A flat curve is a monotone video."""
    buckets = Counter()
    for t, _ in words:
        buckets[int(t // 60)] += 1
    return [(m, buckets.get(m, 0)) for m in range(int(dur // 60) + 1)]


def teardown(vid, refresh=False):
    info, vtt = fetch(vid, refresh)
    if not info:
        print(f"  !! {vid}: no metadata after retry -- private, removed, or bad id")
        return None
    words = parse_vtt(vtt)
    dur = info.get("duration") or (words[-1][0] if words else 0)
    subs = info.get("channel_follower_count") or 0
    views = info.get("view_count") or 0
    score = views / subs if subs else 0

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{vid}.md")
    w = open(path, "w", encoding="utf8")
    P = lambda s="": print(s, file=w)

    P(f"# TEARDOWN — {info.get('title', '?')}")
    P()
    P(f"- **channel** {info.get('channel', '?')} · {subs:,} subs")
    P(f"- **views** {views:,} · **outlier** {score:.2f}x · **uploaded** {info.get('upload_date', '?')}")
    P(f"- **runtime** {hms(dur)} · **words** {len(words):,} · "
      f"**{(len(words) / (dur / 60)) if dur else 0:.0f} wpm** avg")
    P(f"- **url** https://www.youtube.com/watch?v={vid}")
    if not words:
        P()
        P("> **NO CAPTIONS AVAILABLE** — everything below is metadata only. The cold open is the")
        P("> whole point of this teardown, so either watch it with `/watch --end 45` or drop it.")
    P()
    P("---")
    P()
    P(f"## EVIDENCE 1 — COLD OPEN (0:00–{hms(COLD_OPEN)}) — verbatim")
    P()
    P("> §2 says the entire distribution outcome is decided here. Read it before anything else.")
    P()
    P("```")
    for l in lines(words, 0, COLD_OPEN) or ["(none)"]:
        P(l)
    P("```")
    P()

    P("## EVIDENCE 2 — BEAT MAP")
    P()
    ch = info.get("chapters") or []
    if ch:
        P("Author-declared chapters (the beat map they intended):")
        P()
        for c in ch:
            P(f"- `{hms(c['start_time'])}` — {c['title']}")
    else:
        P("No chapters declared. Transcript sampled every ~10% of runtime:")
        P()
        P("```")
        for i in range(10):
            t = dur * i / 10
            seg = lines(words, t, t + 12, per=13)
            P(f"[{hms(t)}] {(seg[0][7:] if seg else '(silence)')[:100]}")
        P("```")
    P()

    P(f"## EVIDENCE 3 — REVERSAL WINDOW ({int(REVERSAL[0]*100)}–{int(REVERSAL[1]*100)}% = "
      f"{hms(dur*REVERSAL[0])}–{hms(dur*REVERSAL[1])}) — verbatim")
    P()
    P("> §4 puts the turn here. If there is one, it is in this block.")
    P()
    P("```")
    for l in lines(words, dur * REVERSAL[0], dur * REVERSAL[0] + 75) or ["(none)"]:
        P(l)
    P("```")
    P()

    P("## EVIDENCE 4 — LOOP-OPENERS (timestamped)")
    P()
    P("> Where they NAME a question. §3: a loop named and left open holds; one answered on the")
    P("> spot spends the video. Check whether each of these is followed by an answer.")
    P()
    lh = hits(words, LOOP.split())
    P("```")
    for l in context(words, lh) or ["(none)"]:
        P(l)
    P("```")
    P(f"\n{len(lh)} hits · {len(lh)/(dur/60) if dur else 0:.1f} per minute")
    P()

    P("## EVIDENCE 5 — NEGATION MARKERS (§7.4: negation, not news)")
    P()
    P("> A limit / correction / reversal leaves lexical fingerprints. High density is a place")
    P("> to look, not a verdict — read the clauses.")
    P()
    nh = hits(words, NEGATION.split())
    P("```")
    for l in context(words, nh, cap=18) or ["(none)"]:
        P(l)
    P("```")
    P(f"\n{len(nh)} hits · {len(nh)/(dur/60) if dur else 0:.1f} per minute · "
      f"top terms: {', '.join(f'{k}({v})' for k, v in Counter(x[1] for x in nh).most_common(8))}")
    P()

    P("## EVIDENCE 6 — PACING (words per minute)")
    P()
    P("```")
    pm = per_minute(words, dur)
    peak = max((c for _, c in pm), default=1) or 1
    for m, c in pm:
        P(f"{hms(m*60):>6} {c:>4}  {'#' * int(40 * c / peak)}")
    P("```")
    P()

    P("## EVIDENCE 7 — PACKAGING")
    P()
    P(f"**Title:** {info.get('title','?')}")
    P()
    P("**Description (first 600 chars):**")
    P()
    P("```")
    P((info.get("description") or "")[:600])
    P("```")
    P()
    P("---")
    P()
    P(ANALYSIS)
    w.close()
    print(f"  -> {path}   [{score:.2f}x · {hms(dur)} · {len(words):,} words"
          f"{' · NO CAPTIONS' if not words else ''}]")
    return path


ANALYSIS = """## ANALYSIS — fill this in from the evidence above (do NOT skip; this is the deliverable)

Answer from the transcript, quoting timestamps. "Unclear" is a valid answer — a guess is not.

**1. Hook shape.** Which §7.4 shape is the title/open? *ceiling · mechanism · consensus-is-wrong ·
negation-of-assumed-truth · debunk · public-reversal · insider-defection · announcement (news).*
If it's an announcement, note that it broke out DESPITE the register, and say what carried it.

**2. Fact-vs-meaning sort (§3).** List what the cold open GIVES (events, numbers, situation) against
what it WITHHOLDS (mechanism, verdict, resolution). A hook that leaks meaning early is a
counter-example worth recording, not a template.

**3. Paradox test.** State the open loop as one sentence the viewer cannot resolve alone. If you
can't, the video held on something else — say what (authority? production? proof-by-demo?).

**4. Loop named at.** Timestamp where the question gets named, and whether it is answered within
30s (spent) or carried (held). Compare against §2's ~0:20–0:35.

**5. Reversal.** Timestamp + one line. Is there a real turn, or does the argument run monotone?

**6. Beat cadence.** Seconds between distinct beats, from the beat map and pacing curve. Note any
stretch >90s without a new beat and whether anything else carried it there.

**7. TRANSFERABLE STRUCTURE.** The point of the whole exercise: 3–5 bullets stating the structural
move — not the topic. "Opens on a number that contradicts the title" is transferable; "talks about
scaling laws" is not.

**8. FUSION CANDIDATES (§7.2).** 2–3 fusions of THIS concept with another *independently proven*
outlier from `outliers.csv`. Each must be statable as a contradiction (§3). Naming the second parent
and its score is mandatory — fusing with an unproven idea is how a dead concept gets built.

**9. DO NOT IMPORT.** What worked here only because of their channel size, runtime, or authority.
§7.4: these run 15–27 min on 30K–900K-sub channels; §1's 8-minute rule is not up for renegotiation
at our size.
"""


def from_outliers(n):
    f = os.path.join(HERE, "outliers.csv")
    if not os.path.exists(f):
        sys.exit(f"no {f} -- run outlier-scan.py first")
    rows = sorted(csv.DictReader(open(f, encoding="utf8")),
                  key=lambda r: -float(r["outlier"]))[:n]
    print(f"top {len(rows)} by outlier score:")
    for r in rows:
        print(f"  {float(r['outlier']):>6.2f}x  [{r['channel'][:18]}] {r['title'][:60]}")
    return [r["id"] for r in rows]


def as_id(s):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([\w-]{11})", s)
    return m.group(1) if m else (s if re.fullmatch(r"[\w-]{11}", s) else None)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    refresh = "--refresh" in sys.argv
    if "--from-outliers" in sys.argv:
        i = sys.argv.index("--from-outliers")
        ids = from_outliers(int(sys.argv[i + 1]) if len(sys.argv) > i + 1 else 5)
    elif args:
        ids = [as_id(a) for a in args]
    else:
        sys.exit(__doc__)
    if not all(ids):
        sys.exit("could not parse a video id from: " + ", ".join(a for a, i in zip(args, ids) if not i))
    print()
    for v in ids:
        teardown(v, refresh)
    print(f"\n{len(ids)} teardown(s) in {OUT}/ — now READ each one and fill in the ANALYSIS section.")

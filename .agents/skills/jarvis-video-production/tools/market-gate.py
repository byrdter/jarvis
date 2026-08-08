#!/usr/bin/env python3
"""market-gate.py — should the studio take on this market at all?

TOOL CONTRACT
  SUBSYSTEM  Q (Quality), gating P1a Market Selection
  STATE      reads: a scout CSV + market-decisions.json  ·  writes: decisions only, via --record
  GATE       exits 1 if any check BLOCKS. Missing evidence BLOCKS — it is never read as a
             pass, and never as a market failure either. See VERDICTS.
  MODULE     jarvis-video-production (tools tree), consumed by the studio umbrella.
  SCOPE      market-agnostic, format-agnostic, subject-agnostic

WHY THIS EXISTS
  ai-film-studio/docs/STUDIO-ROADMAP.md "SCOPE" says: "We will not take on a niche or video
  without a thorough and solid analysis." Doctrine also says a gate that is not a runnable
  script does not exist. This is that gate, made runnable.

  It answers P1a ("which market should the studio serve at all"), NOT P1b ("what video will
  get watched"). Those are different questions and this one is upstream. A market that passes
  here is cleared for concept work; nothing here says which video to make.

VERDICTS  (deliberately the same three as rights-check.py — same doctrine, same reflexes)
  SAFE    the check passed on measured evidence
  REVIEW  passed weakly, or rests on a human judgement that was recorded but is not a fact
  BLOCK   either the market failed a hard floor, or THE EVIDENCE IS NOT THERE

  BLOCK does not mean "bad market". It means "not cleared". Three of the P1a axes cannot be
  measured from any external source (incumbent craft, back-end product fit, slop risk); they
  are recorded human judgements, and an unrecorded one blocks. That is the entire point —
  a market waved through on vibes is exactly what SCOPE forbids.

CALIBRATION — every threshold below was measured, not chosen
  Against the 647-channel 2026-08-08 any-production survey:
      _per_video        p25   1.0x   med   3.2x   p75  10.0x   p90  23.8x
      _usd_per_video    p25  $5.9    med  $33.3   p75 $148.6   p90 $610.8
      _implied_rpm      p25  $0.04   med  $0.21   p75  $1.08   p90  $2.75
      subscriberCount   p25  6,490   med 25,500   p75 100,000  p90 218,000
  The floors sit at roughly the population p75: a market worth a studio's time should beat
  three quarters of what is already out there, not merely be typical.

    market-gate.py --list                          rank candidate markets in the CSV
    market-gate.py --country US --category Knowledge
    market-gate.py --niche "Personal Finance"
    market-gate.py --country US --category Knowledge --record \
        --incumbent-craft weak --backend-fit yes --slop-risk low --by terry
    market-gate.py --country US --category Knowledge --strict     REVIEW also fails
"""
import argparse
import csv
import datetime as dt
import json
import os
import shlex
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
RATCHET = TOOLS / "ratchet"
DECISIONS = RATCHET / "market-decisions.json"

SAFE, REVIEW, BLOCK = "SAFE", "REVIEW", "BLOCK"

# --- thresholds: see CALIBRATION above. Population p75 unless noted. ------------------
MIN_N            = 8        # matches scout-niches.py's --wide roll-up floor
MIN_RPM_COVERAGE = 0.20     # share of the slice with a computable implied RPM
MIN_PER_VIDEO    = 5.0      # avgViews/subs, slice median. Pop med 3.2, p75 10.0
MIN_IMPLIED_RPM  = 1.00     # slice median. Pop p75 1.08 — also ~the tier-1 geo boundary
MIN_USD_PER_VID  = 150.0    # slice median. Pop p75 148.6
MAX_MEDIAN_SUBS  = 300_000  # BAND_SUBS in scout-niches.py — "reachable from cold"
MAX_UPLOADS_MO   = 15       # above this it is an aggregation farm, not a studio
MIN_RUNTIME_MIN  = 3.0      # below this the lane is shorts; $/video collapses (measured 3.5x)

# Recorded-judgement vocabularies. Anything outside these is unrecognised, hence BLOCK.
CRAFT   = {"weak": SAFE, "mixed": REVIEW, "strong": BLOCK}
BACKEND = {"yes": SAFE, "maybe": REVIEW, "no": BLOCK}
SLOP    = {"low": SAFE, "medium": REVIEW, "high": BLOCK}


def newest_csv() -> Path:
    """Default to the most recent scout sweep. Prefer --production any: the faceless sweep
    is a deliberately narrowed population and gating a market on it would re-import a
    production-mode constraint the studio does not have."""
    cands = sorted(RATCHET.glob("scout-*.csv"))
    if not cands:
        sys.exit(f"FAIL: no scout CSV in {RATCHET} — run scout-niches.py first")
    anyprod = [p for p in cands if "-any" in p.name]
    return (anyprod or cands)[-1]


def fnum(row, key):
    """Blank means MISSING, and missing is not zero. _implied_rpm is blank for ~71% of rows;
    coalescing it to 0.0 would rank every poor-data channel as a poor market."""
    v = (row.get(key) or "").strip()
    if not v:
        return None
    try:
        f = float(v)
    except ValueError:
        return None
    return f


def med(vals):
    vals = [v for v in vals if v is not None]
    return st.median(vals) if vals else None


def backfill_derived(rows: list[dict]) -> int:
    """CSVs written before 2026-08-08 predate the P1a market columns. Rather than duplicate
    the formulas here — two copies of a threshold is how doctrine and build drift apart —
    import scout-niches.enrich() and run the real one. Costs no credits: every input field
    is already in the CSV. Returns how many rows gained an implied RPM.

    Copies back EVERY derived column, not just the three new ones. Found while testing: a CSV
    carrying the raw fields but no `_per_video`/`_usd_per_video` (any partial or hand-built
    export) blocked on demand and producibility with "no values" — a spurious BLOCK caused by
    our own missing backfill, which is precisely the failure this gate exists to not commit."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("scout", TOOLS / "scout-niches.py")
    scout = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scout)
    NUM = {"subscriberCount", "avgViews", "viewCount", "videoCount", "estimatedEarnings",
           "longAvgDuration30d", "longAvgDuration1y", "shortAvgDuration30d",
           "longVideoCount30d", "shortVideoCount30d", "longViewCount30d", "shortViewCount30d"}
    got = 0
    for r in rows:
        typed = dict(r)
        for k in NUM:
            v = (r.get(k) or "").strip()
            try:
                typed[k] = float(v) if v else 0
            except ValueError:
                typed[k] = 0
        e = scout.enrich(typed)
        for k, v in e.items():
            # Only fill derived columns, and only where the CSV is actually silent — a value
            # already written by the sweep wins over one recomputed from a stale row.
            if k.startswith("_") and not (r.get(k) or "").strip():
                r[k] = "" if v is None else str(v)
        if e.get("_implied_rpm") is not None:
            got += 1
    return got


def load(csv_path: Path) -> list[dict]:
    with open(csv_path, newline="", encoding="utf8") as f:
        rows = list(csv.DictReader(f))
    if rows and not (rows[0].get("_implied_rpm") or "").strip():
        n = backfill_derived(rows)
        print(f"  (CSV predates the P1a columns — derived implied RPM for {n}/{len(rows)} rows "
              f"via scout-niches.enrich)")
    return rows


def slice_key(a) -> str:
    """A market is a BRACKET, not a category. The key is whatever axes were pinned, in a
    stable order, so the same market always resolves to the same recorded decision."""
    parts = []
    for label, val in (("country", a.country), ("category", a.category), ("niche", a.niche)):
        if val:
            parts.append(f"{label}={val}")
    return " · ".join(parts)


def select(rows, a) -> list[dict]:
    out = rows
    if a.country:
        out = [r for r in out if (r.get("country") or "").upper() == a.country.upper()]
    if a.category:
        out = [r for r in out if (r.get("mainCategory") or "").lower() == a.category.lower()]
    if a.niche:
        n = a.niche.lower()
        out = [r for r in out
               if n in (r.get("niche") or "").lower() or n in (r.get("subNiches") or "").lower()]
    return out


def check(name, verdict, detail):
    return {"name": name, "verdict": verdict, "detail": detail}


def evaluate(rows, key, decision) -> list[dict]:
    """Every check returns exactly one verdict. Order is diagnostic: evidence first, because
    if the evidence is thin nothing below it means anything."""
    out = []
    n = len(rows)

    # 1. EVIDENCE SUFFICIENCY — the "thorough and solid analysis" clause, made literal.
    #    A thin slice BLOCKS. This is the check that distinguishes "we looked and it is bad"
    #    from "we did not really look", which are the two outcomes SCOPE refuses to conflate.
    if n >= MIN_N * 2:
        out.append(check("evidence", SAFE, f"{n} channels in slice"))
    elif n >= MIN_N:
        out.append(check("evidence", REVIEW, f"{n} channels — thin; widen the sweep to be sure"))
    else:
        out.append(check("evidence", BLOCK,
                         f"{n} channels — below n={MIN_N}. Not a verdict on the market; "
                         f"the sweep has not covered it. Re-run scout-niches.py --wide"))
        return out                      # everything downstream would be noise

    # 2. DEMAND — is anything here beating its own distribution?
    pv = med([fnum(r, "_per_video") for r in rows])
    top = sum(1 for r in rows if (fnum(r, "_per_video") or 0) >= 10.0)
    if pv is None:
        out.append(check("demand", BLOCK, "no _per_video values"))
    elif pv >= MIN_PER_VIDEO:
        out.append(check("demand", SAFE, f"median {pv:.1f}x views/sub · {top} channels >=10x"))
    elif top >= 3:
        out.append(check("demand", REVIEW,
                         f"median only {pv:.1f}x, but {top} channels clear 10x — winners exist, "
                         f"the lane average does not"))
    else:
        out.append(check("demand", BLOCK,
                         f"median {pv:.1f}x and only {top} channel{'' if top == 1 else 's'} "
                         f">=10x (floor {MIN_PER_VIDEO}x)"))

    # 3. REACHABILITY — can a cold start land here, or is it owned by incumbents?
    subs = med([fnum(r, "subscriberCount") for r in rows])
    small = sum(1 for r in rows if (fnum(r, "subscriberCount") or 0) <= 50_000)
    if subs is not None and subs <= MAX_MEDIAN_SUBS and small >= 3:
        out.append(check("reachability", SAFE,
                         f"median {subs:,.0f} subs · {small} winners under 50k"))
    elif small >= 1:
        out.append(check("reachability", REVIEW,
                         f"median {subs:,.0f} subs, only {small} under 50k — mostly large incumbents"))
    else:
        out.append(check("reachability", BLOCK,
                         f"median {subs:,.0f} subs, no reachable winners under 50k"))

    # 4. MONETIZATION DENSITY — the load-bearing money axis.
    #    Coverage is checked BEFORE the value: a median over 2 rows is not a median.
    rpms = [fnum(r, "_implied_rpm") for r in rows]
    have = [v for v in rpms if v is not None]
    cov = len(have) / n
    if cov < MIN_RPM_COVERAGE:
        out.append(check("monetization", BLOCK,
                         f"implied RPM computable for {len(have)}/{n} ({cov:.0%}) — under "
                         f"{MIN_RPM_COVERAGE:.0%}. Unknown, not poor. Widen the sweep"))
    else:
        mr = st.median(have)
        # ORDERING, never a forecast — vidIQ's earnings model runs conservative.
        if mr >= MIN_IMPLIED_RPM:
            out.append(check("monetization", SAFE,
                             f"median implied RPM ${mr:.2f} (n={len(have)}, {cov:.0%} coverage)"))
        elif mr >= MIN_IMPLIED_RPM / 2:
            out.append(check("monetization", REVIEW,
                             f"median implied RPM ${mr:.2f} — below the ${MIN_IMPLIED_RPM:.2f} floor "
                             f"but not cheap. Ordering only, not a real RPM"))
        else:
            out.append(check("monetization", BLOCK,
                             f"median implied RPM ${mr:.2f} — a low-bid audience "
                             f"(floor ${MIN_IMPLIED_RPM:.2f})"))

    # 5. PRODUCIBILITY — revenue per unit of production effort, the metric a studio optimises.
    upv = med([fnum(r, "_usd_per_video") for r in rows])
    if upv is None:
        out.append(check("producibility", BLOCK, "no _usd_per_video values"))
    elif upv >= MIN_USD_PER_VID:
        out.append(check("producibility", SAFE, f"median ${upv:,.0f} per video"))
    elif upv >= MIN_USD_PER_VID / 3:
        out.append(check("producibility", REVIEW,
                         f"median ${upv:,.0f} per video — viable only at low cost per video"))
    else:
        out.append(check("producibility", BLOCK,
                         f"median ${upv:,.0f} per video (floor ${MIN_USD_PER_VID:,.0f})"))

    # 6. SHAPE — runtime tolerance and cadence. Together these say what KIND of operation
    #    the lane rewards; a studio cannot win a lane that pays only at farm cadence.
    rt = med([fnum(r, "_runtime_min") for r in rows])
    vpm = med([fnum(r, "_vids_per_mo") for r in rows])
    if rt is not None and rt < MIN_RUNTIME_MIN:
        out.append(check("shape", BLOCK,
                         f"median runtime {rt:.1f} min — a shorts lane; $/video collapses (3.5x)"))
    elif vpm is not None and vpm > MAX_UPLOADS_MO:
        out.append(check("shape", BLOCK,
                         f"median {vpm:.0f} uploads/mo — aggregation cadence, not production"))
    else:
        out.append(check("shape", SAFE,
                         f"runtime {f'{rt:.1f} min' if rt else 'unknown'} · "
                         f"{f'{vpm:.1f}' if vpm else '?'} uploads/mo"))

    # 7-9. RECORDED JUDGEMENTS. Not measurable from any external source, so they are recorded
    #      or they block. Unknown is never a pass — same rule as rights-check.py.
    if not decision:
        out.append(check("judgement", BLOCK,
                         f'no recorded decision for "{key}". Record one with --record '
                         f"(--incumbent-craft / --backend-fit / --slop-risk)"))
        return out
    for label, field, vocab in (("incumbent craft", "incumbent_craft", CRAFT),
                                ("back-end fit", "backend_fit", BACKEND),
                                ("slop risk", "slop_risk", SLOP)):
        raw = (decision.get(field) or "").strip().lower()
        v = vocab.get(raw)
        if v is None:
            out.append(check(label, BLOCK,
                             f"{'not recorded' if not raw else f'unrecognised value {raw!r}'} "
                             f"— expected one of {'/'.join(vocab)}"))
        else:
            note = {"incumbent craft": {"weak": "the opening", "mixed": "contested",
                                        "strong": "already well served"},
                    "back-end fit": {"yes": "sellable audience", "maybe": "unproven",
                                     "no": "AdSense only"},
                    "slop risk": {"low": "", "medium": "watch it", "high": "not this studio"},
                    }[label].get(raw, "")
            out.append(check(label, v, f"{raw}{' — ' + note if note else ''}"))
    return out


def do_list(rows, a):
    """Rank candidate markets so you know what is worth gating. Rolled on country x category
    because the P1a axes cut ACROSS categories — category alone was refuted 2026-08-07."""
    agg = defaultdict(list)
    for r in rows:
        agg[((r.get("country") or "?").upper(), r.get("mainCategory") or "?")].append(r)
    cand = [(k, v) for k, v in agg.items() if len(v) >= MIN_N]
    if not cand:
        print(f"no country x category slice reached n={MIN_N}. Try --wide sweeps, or gate on "
              f"--category alone.")
        return 0
    print(f"{len(cand)} slices at n>={MIN_N} (of {len(agg)}); ranked by median implied RPM\n")
    print(f"{'country':>7} {'category':26} {'n':>4} {'RPM':>7} {'/sub':>7} {'$/vid':>8} {'subs':>9}")
    print("-" * 74)
    def keyf(kv):
        m = med([fnum(r, "_implied_rpm") for r in kv[1]])
        return -(m if m is not None else -1)
    for (cc, cat), v in sorted(cand, key=keyf):
        m = med([fnum(r, "_implied_rpm") for r in v])
        print(f"{cc:>7} {cat[:26]:26} {len(v):>4} "
              f"{('$%.2f' % m) if m is not None else '    ?':>7} "
              f"{(med([fnum(r,'_per_video') for r in v]) or 0):>6.1f}x "
              f"{(med([fnum(r,'_usd_per_video') for r in v]) or 0):>8,.0f} "
              f"{(med([fnum(r,'subscriberCount') for r in v]) or 0):>9,.0f}")
    print(f"\nGate one:  market-gate.py --country US --category '<name>'")
    return 0


def do_record(key, a):
    store = json.loads(DECISIONS.read_text()) if DECISIONS.exists() else {}
    prev = store.get(key, {})
    entry = {
        "incumbent_craft": a.incumbent_craft or prev.get("incumbent_craft", ""),
        "backend_fit":     a.backend_fit     or prev.get("backend_fit", ""),
        "slop_risk":       a.slop_risk       or prev.get("slop_risk", ""),
        "note":            a.note            or prev.get("note", ""),
        "reviewed_by":     a.by              or prev.get("reviewed_by", os.environ.get("USER", "?")),
        "reviewed_at":     dt.date.today().isoformat(),
    }
    store[key] = entry
    RATCHET.mkdir(parents=True, exist_ok=True)
    DECISIONS.write_text(json.dumps(store, indent=2, sort_keys=True) + "\n")
    print(f"recorded judgement for \"{key}\" in {DECISIONS.name}:")
    for k, v in entry.items():
        print(f"    {k:<16} {v or '(empty)'}")
    print()


def main() -> int:
    ap = argparse.ArgumentParser(description="P1a market-selection gate")
    ap.add_argument("--csv", type=Path, help="scout CSV (default: newest --production any)")
    ap.add_argument("--country")
    ap.add_argument("--category")
    ap.add_argument("--niche", help="substring match on niche/subNiches")
    ap.add_argument("--list", action="store_true", help="rank candidate markets and exit")
    ap.add_argument("--strict", action="store_true", help="REVIEW also fails (exit 1)")
    ap.add_argument("--record", action="store_true", help="write the human-judgement axes")
    ap.add_argument("--incumbent-craft", choices=sorted(CRAFT))
    ap.add_argument("--backend-fit", choices=sorted(BACKEND))
    ap.add_argument("--slop-risk", choices=sorted(SLOP))
    ap.add_argument("--note")
    ap.add_argument("--by")
    a = ap.parse_args()

    csv_path = a.csv or newest_csv()
    if not csv_path.exists():
        sys.exit(f"FAIL: no such CSV {csv_path}")
    rows = load(csv_path)
    print(f"market-gate · {csv_path.name} · {len(rows)} channels\n")

    if a.list:
        return do_list(rows, a)

    if not (a.country or a.category or a.niche):
        sys.exit("nothing to gate — pass --country / --category / --niche, or --list")

    key = slice_key(a)
    if a.record:
        do_record(key, a)

    sel = select(rows, a)
    store = json.loads(DECISIONS.read_text()) if DECISIONS.exists() else {}
    decision = store.get(key)

    print(f'MARKET  "{key}"  →  {len(sel)} of {len(rows)} channels\n')
    checks = evaluate(sel, key, decision)
    width = max(len(c["name"]) for c in checks)
    for c in checks:
        print(f"  {c['verdict']:<7} {c['name']:<{width}}  {c['detail']}")

    blocked = [c for c in checks if c["verdict"] == BLOCK]
    review = [c for c in checks if c["verdict"] == REVIEW]
    print()
    if blocked or (review and a.strict):
        failed = blocked + (review if a.strict else [])
        print(f"NOT CLEARED — {len(failed)} check(s) failed"
              f"{' (--strict: REVIEW counts as failure)' if a.strict else ''}.")
        if any(c["name"] in ("evidence", "monetization") and "widen" in c["detail"].lower()
               for c in blocked):
            print("  Evidence gap, not a market verdict:  scout-niches.py --wide --production any")
        if any(c["name"] in ("judgement", "incumbent craft", "back-end fit", "slop risk")
               for c in blocked):
            print(f"  Record the judgement axes:")
            # shlex.quote or the suggestion is unrunnable: most mainCategory values contain
            # spaces or parentheses ("Lifestyle (sociology)") and would be re-split by the shell.
            argv = " ".join(shlex.quote(x) for x in sys.argv[1:])
            print(f"    market-gate.py {argv} --record \\")
            print(f"        --incumbent-craft weak --backend-fit yes --slop-risk low --by terry")
        return 1
    print(f"CLEARED for concept work (P1b){' with ' + str(len(review)) + ' REVIEW' if review else ''}.")
    print("  This says the MARKET is worth serving. It does not say which video to make.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

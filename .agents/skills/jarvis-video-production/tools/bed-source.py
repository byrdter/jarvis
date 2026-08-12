#!/usr/bin/env python3
"""
bed-source.py — source the GENERIC-REAL BED: the ~75% of a documentary timeline that is
ordinary environment footage carrying the VO between evidence beats.

WHY THIS IS A SEPARATE TOOL FROM archival-search.py
`archival-search.py` finds the SPECIFIC-REAL layer — the filing, the hearing, the named
person, the exact moment. It queries Commons, EDGAR, NASA, press rooms, local news. That
layer is ~15% of a timeline and every row is irreplaceable.

This finds the other 75%: lecture halls, bookstore shelves, bursar windows, students at
desks. Any of a hundred assets will do for each slot. Different problem, different tool.

  Censused 2026-08-12: Modern MBA runs 14.0 shots/min. A 27-min video wants ~380 shots,
  of which ~285 are bed. Our own stills test scene ran SIX sources/min. This is the gap.

THE TWO SEARCH RULES, NEITHER OPTIONAL

1. **Search SPECIFIC ENVIRONMENTS, never abstract concepts.** "lecture hall" not "education".
   "college bookstore" not "learning". Concept keywords return the exact clips every other
   faceless channel is already using — that is how a video comes out looking generic even
   though every asset is real. (FOOTAGE-SOURCING.md §9.)

2. **KEEP QUERIES TO 1-3 WORDS.** Both providers AND-match every term. Measured 2026-08-13:

       "college bookstore textbook shelves"  -> openverse 4     commons 0
       "college bookstore"                   -> openverse 240   commons 5
       "students walking across campus quad" -> openverse 0     commons 0
       "campus quad"                         -> openverse 240   commons 5

   A descriptive phrase is the right query for a fuzzy stock engine (Pexels) and the WRONG
   query for a keyword archive. Rule 1 lives in the NOUN, not in the sentence length: "campus
   quad" is specific; "students walking across campus quad" is just zero results.

   This is the same artifact class as the recorded "0/24 beats have free video" false
   negative (multi-word terms). It cost two full runs here before anyone tested a control.
   `--strict-terms` refuses to run a plan containing >3-word queries; the default warns.

RIGHTS TIERS — narrower than archival-search's, on purpose
  CLEAR    CC0 / public domain / CC-BY. Usable in a monetised cut; BY needs attribution.
  FLAGGED  CC-BY-SA. Share-alike on a monetised video is UNRESOLVED and is a question for
           counsel, not for this script (FOOTAGE-SOURCING.md §5). Surfaced, never silently
           mixed into the CLEAR pool.
  EXCLUDED NC (non-commercial) and ND (no-derivatives) are dropped before you ever see them.
           Both are structurally incompatible with a monetised, edited video. Openverse
           returns them by DEFAULT — that is the trap this tool exists to close.

PROVIDERS
  PROVIDER ORDER IS THE --providers ORDER and it matters. For the bed, put openverse
  FIRST: it aggregates Flickr (ordinary contemporary life). Commons is the encyclopedic
  record and drifts badly on generic environments — measured ~25-30% usable.

  openverse  keyless, ~700M CC works, images. RATE-LIMITED HARD when anonymous —
             returns 401 once the quota is spent, so treat it as a bonus provider,
             not a dependency. Commons alone covers the bed (6,312 hits for
             "lecture hall"; ~23 of every 50 rows are CLEAR-tier).
  commons    keyless, Wikimedia. Stills-dominant (measured 702:1 stills:video).

  Pexels / Pixabay / Storyblocks would add MOTION cheaply but all need an API key and none
  is set. Not a blocker: FOOTAGE-SOURCING.md §7 measured a stills-only scene at 71
  change-events/min, beating our shipped masters (67.6-69.6). Stills + punch-ins clear the
  gate. Add keys to widen, not to unblock.

FAILURE POLICY (learned expensively, 2026-08-12; tightened 2026-08-13)
A provider that fails RAISES. It never returns []. A silent zero reads as evidence of
absence and that is how "0/24 beats have free video" got reported when it was a filter
artifact.

**Raising was not enough.** Pass 1 of the textbooks bed ran 54 environments at 1.0s spacing,
took 34 provider failures to rate-limiting, and printed 21 environments as `EMPTY` — including
"college bookstore textbook shelves", which returns three named college bookstores on Commons
the moment you ask it politely. The rows were correctly raised AND the summary still said
EMPTY, so the artifact survived all the way to the report.

Two fixes, both here:
  1. **Per-provider rate limiting** (`MIN_INTERVAL`) — spacing between calls to the SAME
     provider, independent of --pause, so adding providers cannot silently speed up the
     request rate to any one of them.
  2. **EMPTY and UNRESOLVED are different outcomes and are never merged.** EMPTY means the
     provider answered and had nothing. UNRESOLVED means we do not know. Only EMPTY is
     evidence. A run with any UNRESOLVED rows prints its coverage as a FLOOR, not a result.

    python3 bed-source.py --plan plan.json --out manifest.jsonl
    python3 bed-source.py --query "campus bookstore shelves" --need 6
    python3 bed-source.py --plan plan.json --out m.jsonl --report bed.md
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request

UA = {"User-Agent": "jarvis-video-research/1.0 (byrdter@auburn.edu)"}
G, R, Y, C, Z = "\033[32m", "\033[31m", "\033[33m", "\033[36m", "\033[0m"

CLEAR_LICENSES = {"cc0", "pdm", "by"}
FLAGGED_LICENSES = {"by-sa"}
# everything else (by-nc, by-nd, by-nc-sa, by-nc-nd) is dropped before display


class ProviderError(RuntimeError):
    pass


# Minimum seconds between calls to the SAME provider. Anonymous Openverse throttles hard;
# Commons is generous but asks for politeness. Independent of --pause so that adding a
# provider cannot silently raise the request rate to any single one.
MIN_INTERVAL = {"openverse": 4.0, "commons": 1.0}
_last_call = {}


def _throttle(provider):
    gap = MIN_INTERVAL.get(provider, 1.0)
    prev = _last_call.get(provider)
    if prev is not None:
        wait = gap - (time.monotonic() - prev)
        if wait > 0:
            time.sleep(wait)
    _last_call[provider] = time.monotonic()


def get(url, provider, tries=5, pause=3.0):
    last = None
    for i in range(tries):
        _throttle(provider)
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            last = e
            code = getattr(e, "code", None)
            if code in (429, 503) or code is None:
                time.sleep(pause * (2 ** i))
                continue
            break
    raise ProviderError(f"{provider} failed after {tries}: {last}")


def tier(lic):
    lic = (lic or "").lower()
    if lic in CLEAR_LICENSES:
        return "CLEAR"
    if lic in FLAGGED_LICENSES:
        return "FLAGGED"
    return None


CLEAR_ONLY = False  # set by --clear-only; drops by-sa at the REQUEST, not after


def openverse(q, need):
    lic = "cc0,pdm,by" if CLEAR_ONLY else "cc0,pdm,by,by-sa"
    url = ("https://api.openverse.org/v1/images/?"
           + urllib.parse.urlencode({"q": q, "page_size": min(need * 4, 40),
                                     "license": lic}))
    d = get(url, "openverse")
    out = []
    for r in d.get("results", []):
        t = tier(r.get("license"))
        if not t:
            continue
        out.append({"provider": "openverse", "kind": "still", "tier": t,
                    "title": (r.get("title") or "").strip()[:110],
                    "license": f"{r.get('license')} {r.get('license_version') or ''}".strip(),
                    "creator": r.get("creator"), "source": r.get("source"),
                    "url": r.get("foreign_landing_url"), "file": r.get("url")})
    return out, d.get("result_count", 0)


def commons(q, need):
    url = ("https://commons.wikimedia.org/w/api.php?"
           + urllib.parse.urlencode({
               "action": "query", "format": "json", "generator": "search",
               "gsrsearch": f"filetype:bitmap {q}", "gsrnamespace": "6",
               "gsrlimit": min(max(need * 8, 20), 50), "prop": "imageinfo",
               "iiprop": "url|extmetadata", "iiurlwidth": "1280"}))
    d = get(url, "commons")
    pages = (d.get("query") or {}).get("pages") or {}
    out = []
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata") or {}
        lic = (meta.get("LicenseShortName", {}).get("value") or "").lower()
        norm = ("cc0" if "cc0" in lic or "public domain" in lic
                else "by-sa" if "sa" in lic
                else "by" if "cc by" in lic or "cc-by" in lic else lic)
        t = tier(norm)
        if not t:
            continue
        out.append({"provider": "commons", "kind": "still", "tier": t,
                    "title": (p.get("title") or "").replace("File:", "")[:110],
                    "license": meta.get("LicenseShortName", {}).get("value"),
                    "creator": (meta.get("Artist", {}).get("value") or "")[:80],
                    "source": "wikimedia", "url": ii.get("descriptionurl"),
                    "file": ii.get("thumburl") or ii.get("url")})
    return out, len(pages)


PROVIDERS = {"openverse": openverse, "commons": commons}


def run_query(q, need, providers):
    rows, errs, failed = [], [], []
    for name in providers:
        try:
            got, total = PROVIDERS[name](q, need)
            rows += got
        except ProviderError as e:
            errs.append(str(e))
            failed.append(name)
            print(f"  {R}provider {name} FAILED{Z}: {e}", file=sys.stderr)
    seen, dedup = set(), []
    for r in rows:
        k = (r.get("url") or r.get("file") or "").lower()
        if k and k not in seen:
            seen.add(k)
            dedup.append(r)
    # Provider order matters for the BED specifically: Openverse/Flickr carries ordinary
    # contemporary life, Commons carries the encyclopedic record. Measured 2026-08-13, a
    # Commons-only bed ran ~25-30% usable against the pixels. Rank by provider first, then
    # tier, so Commons only fills what Openverse could not.
    rank = {p: i for i, p in enumerate(providers)}
    dedup.sort(key=lambda r: (rank.get(r["provider"], 9),
                              0 if r["tier"] == "CLEAR" else 1))
    return dedup, errs, failed


def main():
    ap = argparse.ArgumentParser(description="Source the generic-real bed.")
    ap.add_argument("--plan", help="JSON: [{section, env, need}] shot plan")
    ap.add_argument("--query", help="single environment query")
    ap.add_argument("--need", type=int, default=6, help="assets wanted per environment")
    ap.add_argument("--providers", default="openverse,commons")
    ap.add_argument("--out", help="JSONL manifest")
    ap.add_argument("--report", help="markdown coverage report")
    ap.add_argument("--pause", type=float, default=1.2, help="seconds between queries")
    ap.add_argument("--clear-only", action="store_true",
                    help="CC0/PD/BY only — exclude share-alike entirely, no counsel question")
    ap.add_argument("--strict-terms", action="store_true",
                    help="refuse to run if any query exceeds 3 words (see header rule 2)")
    a = ap.parse_args()

    global CLEAR_ONLY
    CLEAR_ONLY = a.clear_only
    provs = [p for p in a.providers.split(",") if p in PROVIDERS]
    if a.query:
        plan = [{"section": "-", "env": a.query, "need": a.need}]
    elif a.plan:
        plan = json.load(open(a.plan))
    else:
        ap.error("need --plan or --query")

    # Rule 2: long descriptive phrases return zero on AND-matching archives. Catch it
    # BEFORE burning a run, not after reading 21 false EMPTYs in a report.
    longq = [p["env"] for p in plan if len(p["env"].split()) > 3]
    if longq:
        print(f"{R}{len(longq)} quer{'y' if len(longq)==1 else 'ies'} exceed 3 words. "
              f"These providers AND-match; long phrases return ZERO and read as EMPTY.{Z}",
              file=sys.stderr)
        for q in longq[:8]:
            print(f"  {Y}{len(q.split())}w{Z}  {q}", file=sys.stderr)
        if len(longq) > 8:
            print(f"  … and {len(longq)-8} more", file=sys.stderr)
        if a.strict_terms:
            sys.exit("refusing to run (--strict-terms). Shorten to 1-3 word noun phrases.")
        print(f"{Y}  continuing anyway — treat any EMPTY below as UNPROVEN.{Z}\n",
              file=sys.stderr)

    manifest, cov, failures = [], [], []
    for i, item in enumerate(plan, 1):
        env, need = item["env"], item.get("need", a.need)
        rows, errs, failed = run_query(env, need, provs)
        failures += errs
        # rows already ranked by provider-then-tier in run_query
        clear = [r for r in rows if r["tier"] == "CLEAR"]
        flagged = [] if a.clear_only else [r for r in rows if r["tier"] == "FLAGGED"]
        keep = (clear + flagged)[:need] if a.clear_only else (clear + flagged)[:need]
        for r in keep:
            r["section"], r["env"] = item.get("section", "-"), env
        manifest += keep
        col = G if len(clear) >= need else (Y if keep else R)
        print(f"{col}{len(keep):>3}{Z}/{need}  [{len(clear)} clear · {len(flagged)} share-alike]"
              f"  {C}{item.get('section','-'):<10}{Z} {env}")
        cov.append({"section": item.get("section", "-"), "env": env, "need": need,
                    "clear": len(clear), "flagged": len(flagged), "kept": len(keep),
                    "failed": failed})
        if i < len(plan):
            time.sleep(a.pause)

    tot_need = sum(c["need"] for c in cov)
    tot_keep = sum(c["kept"] for c in cov)
    tot_clear = sum(min(c["clear"], c["need"]) for c in cov)
    # EMPTY (provider answered, had nothing) and UNRESOLVED (provider failed) are
    # DIFFERENT OUTCOMES and must never be merged. Only EMPTY is evidence of absence.
    unresolved = [c for c in cov if c["failed"] and c["kept"] < c["need"]]
    empty = [c for c in cov if c["kept"] == 0 and not c["failed"]]
    thin = [c for c in cov if 0 < c["kept"] < c["need"] and not c["failed"]]

    print(f"\n{'='*70}\n  environments {len(cov)}   assets {tot_keep}/{tot_need}"
          f"   fully-clear {tot_clear}")
    print(f"  EMPTY {len(empty)}   THIN {len(thin)}   {R}UNRESOLVED {len(unresolved)}{Z}")
    if unresolved:
        print(f"\n  {R}⚠  {len(unresolved)} environment(s) had a provider FAIL.{Z}")
        print(f"  {R}   Coverage above is a FLOOR, not a result. Re-run the deficit before")
        print(f"     concluding anything is unavailable.{Z}")
    for c in unresolved:
        print(f"  {R}UNRESOLVED{Z}  {c['env']}  (failed: {','.join(c['failed'])})")
    for c in empty:
        print(f"  {Y}EMPTY{Z}       {c['env']}")

    if a.out:
        with open(a.out, "w") as f:
            for r in manifest:
                f.write(json.dumps(r) + "\n")
        print(f"\n  manifest → {a.out}")
    if a.report:
        with open(a.report, "w") as f:
            f.write("# Generic-real bed — coverage\n\n")
            f.write(f"- environments queried: **{len(cov)}**\n")
            f.write(f"- assets kept: **{tot_keep} / {tot_need}**\n")
            f.write(f"- environments fully covered by CLEAR-tier alone: **{tot_clear}**\n")
            f.write(f"- EMPTY (asked, nothing there): **{len(empty)}** · "
                    f"THIN: **{len(thin)}** · **UNRESOLVED (provider failed): "
                    f"{len(unresolved)}**\n\n")
            if unresolved:
                f.write(f"> ⚠️ **{len(unresolved)} environment(s) had a provider fail. "
                        f"These numbers are a FLOOR, not a result.** UNRESOLVED is not "
                        f"evidence of absence — re-run the deficit before concluding "
                        f"anything is unavailable.\n\n")
            f.write("| section | environment | need | clear | share-alike | kept | state |\n")
            f.write("|---|---|---:|---:|---:|---:|---|\n")
            for c in cov:
                state = ("ok" if c["kept"] >= c["need"]
                         else "**UNRESOLVED**" if c["failed"]
                         else "EMPTY" if not c["kept"] else "thin")
                f.write(f"| {c['section']} | {c['env']} | {c['need']} | "
                        f"{c['clear']} | {c['flagged']} | {c['kept']} | {state} |\n")
        print(f"  report   → {a.report}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""verify-vo-sync — check that each visual cut matches the voice-over.

For every beat in a scene's timeline.json, the visual that anchors to a spoken claim
must appear right as (or just before) the VO says it — never while the VO is still on
the previous point. This is the check that catches "the document changed too early /
too late" misalignment in the new-format video pipeline.

timeline.json  : [{"start": s, "end": e, "label": "...", "cue": "exact VO phrase" | null}, ...]
transcript.json: Whisper word list [{"text","start","end"}, ...]

A beat with cue=null (avatar / self-synced HyperFrames / pure breather) is not checked.
For a cued beat, we find where the VO actually says the cue, then require:
    beat.start  ∈  [cue_word_start - MAXLEAD , cue_word_start + MAXLAG]
i.e. the visual leads the VO by at most MAXLEAD and never lags by more than MAXLAG.

Usage:
  verify-vo-sync.py <scene_dir>                 # expects timeline.json + assets/transcript.json
  verify-vo-sync.py --timeline t.json --transcript tr.json [--maxlead 0.8 --maxlag 0.4]
Exit code 0 = all aligned, 1 = misalignments found.
"""
import argparse, json, sys
from pathlib import Path

def load_words(p):
    d=json.load(open(p)); return d if isinstance(d,list) else d.get("words",d.get("segments",[]))

def find_cue(W, phrase, near=None):
    """Return (start,end) of the run of words matching the phrase. With `near` set, pick the
    occurrence whose start is closest to `near` (handles repeated phrases like 'Phase one')."""
    norm=lambda s: s.strip().lower().strip(".,%$?\"'—-")
    toks=[norm(x) for x in phrase.split() if norm(x)]
    if not toks: return None,None
    ww=[norm(w["text"]) for w in W]
    hits=[i for i in range(len(ww)-len(toks)+1) if ww[i:i+len(toks)]==toks]
    if not hits: return None,None
    i = min(hits, key=lambda i: abs(W[i]["start"]-near)) if near is not None else hits[0]
    return round(W[i]["start"],2), round(W[i+len(toks)-1]["end"],2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("scene_dir", nargs="?")
    ap.add_argument("--timeline"); ap.add_argument("--transcript")
    ap.add_argument("--maxlead", type=float, default=0.8, help="max seconds a visual may lead its VO cue")
    ap.add_argument("--maxlag",  type=float, default=0.4, help="max seconds a visual may lag its VO cue")
    a=ap.parse_args()
    if a.scene_dir:
        tl=Path(a.scene_dir)/"timeline.json"; tr=Path(a.scene_dir)/"assets"/"transcript.json"
    else:
        tl=Path(a.timeline); tr=Path(a.transcript)
    beats=json.load(open(tl)); W=load_words(tr)

    print(f"VO-sync check: {tl}")
    print(f"  tolerance: visual may lead VO by ≤{a.maxlead}s, lag by ≤{a.maxlag}s\n")
    print(f"  {'beat':28} {'start':>7} {'cue@VO':>8} {'Δ':>7}  status")
    fails=0; missing=0
    for b in beats:
        lbl=b.get("label","?")[:28]; st=round(float(b["start"]),2); cue=b.get("cue")
        if not cue:
            print(f"  {lbl:28} {st:7.2f} {'—':>8} {'—':>7}  (uncued: avatar/HF/breather)")
            continue
        cs,ce=find_cue(W,cue,near=st)
        if cs is None:
            print(f"  {lbl:28} {st:7.2f} {'NOTFND':>8} {'?':>7}  ⚠ cue text not found in transcript")
            missing+=1; continue
        delta=round(st-cs,2)               # negative = visual leads VO; positive = visual lags
        if delta < -a.maxlead:
            status=f"✗ TOO EARLY by {abs(delta+0):.2f}s (cuts off previous)"; fails+=1
        elif delta > a.maxlag:
            status=f"✗ TOO LATE by {delta:.2f}s (VO already moved on)"; fails+=1
        else:
            status="✓ ok"
        print(f"  {lbl:28} {st:7.2f} {cs:8.2f} {delta:+7.2f}  {status}")
    print()
    n=len([b for b in beats if b.get('cue')])
    if fails or missing:
        print(f"  RESULT: {fails} misaligned, {missing} cue(s) not found, of {n} cued beats — FAIL")
        sys.exit(1)
    print(f"  RESULT: all {n} cued beats aligned — PASS")

if __name__=="__main__": main()

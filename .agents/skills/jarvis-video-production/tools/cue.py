#!/usr/bin/env python3
"""Find exact word-start times for cue phrases in a shorts transcript.
Usage: python3 cue.py transcripts/v1-s1.json "phrase" "phrase" ..."""
import json,sys,re
toks=json.load(open(sys.argv[1])); phrases=sys.argv[2:]
def norm(s): return re.sub(r'[^a-z0-9]','',s.lower())
words=[(norm(t["text"]),t["start"]) for t in toks]; J=[w[0] for w in words]
for ph in phrases:
    pw=[norm(x) for x in ph.split() if norm(x)]; hit=None
    for i in range(len(J)-len(pw)+1):
        if J[i:i+len(pw)]==pw: hit=i; break
    if hit is None:
        for i in range(len(J)-2):
            if J[i:i+min(3,len(pw))]==pw[:min(3,len(pw))]: hit=i; break
    print(f"  {words[hit][1]:6.2f} | {ph}" if hit is not None else f"  ??.?? | NOTFOUND: {ph}")

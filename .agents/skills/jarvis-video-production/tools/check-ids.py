#!/usr/bin/env python3
"""Static check: every id referenced in a scene's JS must exist in its markup.
Usage: check-ids.py sceneDir [sceneDir...]  — prints MISSING lines; silent if clean."""
import re,sys
hexish=re.compile(r'^[0-9a-fA-F]{6}$')
bad=0
for d in sys.argv[1:]:
    try: html=open(f"{d}/index.html").read()
    except FileNotFoundError: continue
    defined=set(re.findall(r'id="([^"]+)"',html))
    script="".join(re.findall(r"<script>([\s\S]*?)</script>",html))
    refs=set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)",script))
    sels=set(re.findall(r"['\"]#([A-Za-z][A-Za-z0-9_-]*)['\"]",script))
    for r in sorted(refs|{s for s in sels if not hexish.match(s)}):
        if r not in defined:
            print(f"MISSING id '{r}' in {d}"); bad=1
sys.exit(bad)

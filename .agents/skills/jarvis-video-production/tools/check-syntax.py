#!/usr/bin/env python3
"""Extract each scene's <script> body and node --check it for syntax errors.
Usage: check-syntax.py sceneDir [sceneDir...]  — prints FAIL lines; exit 1 if any."""
import re,sys,subprocess,tempfile,os
bad=0
for d in sys.argv[1:]:
    f=os.path.join(d,"index.html")
    if not os.path.exists(f): continue
    html=open(f).read()
    scripts=re.findall(r"<script>([\s\S]*?)</script>",html)
    for i,sc in enumerate(scripts):
        if not sc.strip(): continue
        with tempfile.NamedTemporaryFile("w",suffix=".js",delete=False) as tmp:
            tmp.write(sc); path=tmp.name
        r=subprocess.run(["node","--check",path],capture_output=True,text=True)
        os.unlink(path)
        if r.returncode!=0:
            err=r.stderr.strip().split("\n")
            msg=[l for l in err if "SyntaxError" in l or ":" in l][:2]
            print(f"FAIL {'/'.join(d.split('/')[-2:])} script#{i}: {' | '.join(msg[-2:])}")
            bad=1
sys.exit(bad)

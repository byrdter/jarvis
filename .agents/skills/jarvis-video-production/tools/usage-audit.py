import json,os,glob,collections,datetime
ROOT=os.path.expanduser("~/.claude/projects")
tot=collections.Counter(); bymon=collections.defaultdict(collections.Counter)
byproj=collections.defaultdict(collections.Counter); bymodel=collections.defaultdict(collections.Counter)
sess=0; msgs=0; files=glob.glob(os.path.join(ROOT,"*","*.jsonl"))
for f in files:
    proj=os.path.basename(os.path.dirname(f)); sess+=1
    for line in open(f,encoding="utf8",errors="ignore"):
        if '"usage"' not in line: continue
        try: d=json.loads(line)
        except: continue
        m=d.get("message") or {}
        u=m.get("usage")
        if not isinstance(u,dict): continue
        model=m.get("model") or "unknown"
        ts=(d.get("timestamp") or "")[:7]
        msgs+=1
        for k in ("input_tokens","output_tokens","cache_creation_input_tokens","cache_read_input_tokens"):
            v=u.get(k) or 0
            tot[k]+=v; bymon[ts][k]+=v; byproj[proj][k]+=v; bymodel[model][k]+=v
        st=u.get("server_tool_use") or {}
        for k,v in st.items():
            tot[k]+=v or 0; bymon[ts][k]+=v or 0
print(f"sessions(files)={sess}  assistant msgs with usage={msgs:,}\n")
T=lambda c: c['input_tokens']+c['output_tokens']+c['cache_creation_input_tokens']+c['cache_read_input_tokens']
print("=== ALL-TIME TOKENS ===")
for k in ("input_tokens","cache_creation_input_tokens","cache_read_input_tokens","output_tokens"):
    print(f"  {k:<32} {tot[k]:>16,}  {100*tot[k]/T(tot):>5.1f}%")
print(f"  {'TOTAL':<32} {T(tot):>16,}")
print(f"  web_search={tot['web_search_requests']:,}  web_fetch={tot['web_fetch_requests']:,}")
print("\n=== BY MONTH (total tokens, and output tokens) ===")
for k in sorted(bymon):
    if not k: continue
    c=bymon[k]; print(f"  {k}  total {T(c):>15,}   output {c['output_tokens']:>12,}   cache_read {c['cache_read_input_tokens']:>15,}")
print("\n=== BY PROJECT ===")
for p,c in sorted(byproj.items(),key=lambda x:-T(x[1])):
    print(f"  {T(c):>16,}  out {c['output_tokens']:>11,}  {p[:74]}")
print("\n=== BY MODEL ===")
for m,c in sorted(bymodel.items(),key=lambda x:-T(x[1]))[:10]:
    print(f"  {T(c):>16,}  out {c['output_tokens']:>11,}  {m}")

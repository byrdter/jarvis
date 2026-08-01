import json,os,glob,collections,statistics
ROOT=os.path.expanduser("~/.claude/projects")
# public API list prices $/Mtok. OPUS tier vs SONNET tier. cache_read=0.1x in, cache_write=1.25x in
P={"opus":{"in":15.0,"out":75.0},"sonnet":{"in":3.0,"out":15.0},"haiku":{"in":1.0,"out":5.0}}
def tier(m):
    m=m.lower()
    if "opus" in m or "fable" in m: return "opus"
    if "sonnet" in m: return "sonnet"
    if "haiku" in m: return "haiku"
    return "opus"
cost=collections.Counter(); comp=collections.Counter(); persess={}
for f in glob.glob(os.path.join(ROOT,"*","*.jsonl")):
    s=collections.Counter()
    for line in open(f,encoding="utf8",errors="ignore"):
        if '"usage"' not in line: continue
        try: d=json.loads(line)
        except: continue
        m=d.get("message") or {}; u=m.get("usage")
        if not isinstance(u,dict): continue
        t=tier(m.get("model") or ""); p=P[t]
        i=u.get("input_tokens") or 0; o=u.get("output_tokens") or 0
        cw=u.get("cache_creation_input_tokens") or 0; cr=u.get("cache_read_input_tokens") or 0
        c=(i*p["in"] + o*p["out"] + cw*p["in"]*1.25 + cr*p["in"]*0.10)/1e6
        cost[t]+=c; comp["input"]+=i*p["in"]/1e6; comp["output"]+=o*p["out"]/1e6
        comp["cache_write"]+=cw*p["in"]*1.25/1e6; comp["cache_read"]+=cr*p["in"]*0.10/1e6
        s["tok"]+=i+o+cw+cr; s["cost"]+=c; s["cr"]+=cr; s["cw"]+=cw; s["out"]+=o
    if s["tok"]: persess[f]=s
T=sum(cost.values())
print(f"=== API-EQUIVALENT COST (list price) — you paid a flat subscription ===")
print(f"  TOTAL  ${T:,.0f}   across {len(persess)} sessions\n")
print("  by model tier:")
for k,v in cost.most_common(): print(f"    {k:<8} ${v:>11,.0f}  {100*v/T:>5.1f}%")
print("\n  BY COMPONENT — this is the reversal:")
tv=sum(comp.values())
for k,v in sorted(comp.items(),key=lambda x:-x[1]): print(f"    {k:<12} ${v:>11,.0f}  {100*v/tv:>5.1f}% of cost")
print("\n=== SESSION DISTRIBUTION ===")
cs=sorted((s['cost'] for s in persess.values()),reverse=True)
print(f"  median ${statistics.median(cs):,.2f} | mean ${statistics.mean(cs):,.2f} | max ${cs[0]:,.0f}")
top10=sum(cs[:max(1,len(cs)//10)]); print(f"  TOP 10% of sessions = ${top10:,.0f} = {100*top10/T:.1f}% of all cost")
top1=sum(cs[:max(1,len(cs)//100)]); print(f"  TOP  1% of sessions = ${top1:,.0f} = {100*top1/T:.1f}% of all cost")
print("\n  10 most expensive sessions:")
for f,s in sorted(persess.items(),key=lambda x:-x[1]['cost'])[:10]:
    ratio=s['cr']/max(s['cw'],1)
    print(f"    ${s['cost']:>8,.0f}  {s['tok']:>13,} tok  cache_read/write {ratio:>6.1f}x  out {s['out']:>9,}  {os.path.basename(f)[:12]}")

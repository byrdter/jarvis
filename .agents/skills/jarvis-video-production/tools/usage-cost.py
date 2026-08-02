import json,os,glob,collections,statistics
ROOT=os.path.expanduser("~/.claude/projects")
# Published API list prices, $/Mtok. VERIFIED 2026-08-02 against a 4K capture of
# platform.claude.com/docs/en/about-claude/pricing (capture C5, in the project assets).
# Multipliers read off that page and confirmed: 5m cache write = 1.25x base input,
# 1h cache write = 2.00x, "Cache Hits & Refreshes" (read) = 0.10x. The two write TTLs are
# priced separately below from usage.cache_creation, which carries both counts on every record.
#
# WAS WRONG until 2026-08-02: this table carried opus 15/75 — that is Opus 4 / 4.1 pricing
# (deprecated and retired respectively), not the current Opus tier — plus a flat 1.25x write.
# Together those inflated the total ~2.1x. Do not "restore" those numbers.
P={"opus":   {"in": 5.0,"out":25.0},  # Opus 5 / 4.8 / 4.7 / 4.6 / 4.5
   "fable":  {"in":10.0,"out":50.0},  # Fable 5 / Mythos 5
   "sonnet5":{"in": 2.0,"out":10.0},  # INTRODUCTORY, through 2026-08-31; $3/$15 from 2026-09-01
   "sonnet": {"in": 3.0,"out":15.0},  # Sonnet 4.6 / 4.5 / 4
   "haiku":  {"in": 1.0,"out": 5.0}}
CW_1H, CW_5M = 2.00, 1.25
def tier(m):
    m=m.lower()
    if "fable" in m or "mythos" in m: return "fable"
    if "opus" in m: return "opus"
    if "sonnet-5" in m: return "sonnet5"   # must precede the general sonnet test
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
        # split the cache write by TTL — 1h writes cost 2.00x input, 5m writes 1.25x
        cc=u.get("cache_creation")
        if isinstance(cc,dict):
            w1=cc.get("ephemeral_1h_input_tokens") or 0; w5=cc.get("ephemeral_5m_input_tokens") or 0
        else:
            w1,w5=0,cw            # no breakdown on this record: assume 5m (the cheaper rate)
        cwcost=(w1*CW_1H + w5*CW_5M)*p["in"]/1e6
        c=(i*p["in"] + o*p["out"] + cr*p["in"]*0.10)/1e6 + cwcost
        cost[t]+=c; comp["input"]+=i*p["in"]/1e6; comp["output"]+=o*p["out"]/1e6
        comp["cache_write"]+=cwcost; comp["cache_read"]+=cr*p["in"]*0.10/1e6
        s["tok"]+=i+o+cw+cr; s["cost"]+=c; s["cr"]+=cr; s["cw"]+=cw; s["out"]+=o
    if s["tok"]: persess[f]=s
T=sum(cost.values())
print(f"=== API-EQUIVALENT COST (list price) — you paid a flat subscription ===")
print(f"  ESTIMATE, not a bill. Published list rates $/Mtok, applied to measured counts:")
print(f"    opus  in $5  / out $25    sonnet 4.6 in $3 / out $15    haiku in $1 / out $5")
print(f"    fable in $10 / out $50    sonnet 5   in $2 / out $10 (intro, thru 2026-08-31)")
print(f"    cache read 0.10x input    cache write 1.25x (5m TTL) / 2.00x (1h TTL)")
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

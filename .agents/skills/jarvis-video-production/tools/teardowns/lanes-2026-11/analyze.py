import json,re,math,statistics as st,csv,sys
d=json.load(open('data.json'))
MODEL=r"(opus|sonnet|haiku|gpt|fable|gemini|kimi|glm|jev|mythos|deepseek|sakana|dots|muse|stealth|llm released|qwen|llama|codex's \$500|astra|sol\b)"
B={
 'a_built_app': r"(build mobile apps|\$1m/y saas|video game|same app|cloned calendly|built me a business|safer openclaw alternative|build & sell ai saas|build & sell software|build & sell \(2026\)|full course 4 hours: build & sell|make it better.. 100|build anything with it|build beautiful frontends|3d websites|\$15k animated sites|\$10k websites|designs websites|kills ai website slop|\$1 website)",
 'b_factory_autonomous': r"(factor(y|ies)|harness|ralph|\bprs\b|autonomous|nonstop|agent teams|archon|worktree|autoresearch|agent loops|ships its own|make it better|forced claude|adversarial|ai native|engineering team with subagents|on autopilot)",
 'c_second_brain_memory': r"(second brain|memory|knowledge base|llm wiki|obsidian|notion|ai os\b|ai operating system|code operating systems|karpathy.s llm)",
 'c2_rag_knowledge': r"(\brag\b|knowledge graph|lightrag|llm knowledge)",
 'd_local_open_cheap': r"(open model|open source|\blocal\b|for free|free forever|code free|deepseek|kimi|glm|chinese|qwen|replaces your .* subscription|killed notion|\$1(?![,\dMmKk])|1/5 the price|too cheap|stealth|sakana)",
 'e_model_news': MODEL+r"|just dropped|dropped|is here|is coming|just announced|ai news|announced|new model|released",
 'f_tutorial_setup': r"(how to|guide|tutorial|course|set up|setup|full workflow|step by step|explained|master \d|learn|blueprint|in \d+ min|here's how|use cases|template|tricks|tips)",
 'g_business_money': r"(\$\d|money|sell|agency|client|business|consult|millionaire|saas|offer|retainer|\bjob|career|leads|pricing|capitalism|solopreneur|economically|wealth|\d+k)",
 'h_team_org': r"(compan|enterprise|engineering org|corporation|multiplayer|stripe.s|goldman)",
 'j_open_agents': r"(hermes|openclaw|clawdbot|pi coding agent|paperclip)",
 'j2_personal_agent_bots': r"(hermes|openclaw|clawdbot|paperclip|grok bot|dispatch|claude channels|managed agents|routines)",
}
F={
 'i_built_made': r"^(i|i've)\b.*\b(built|cloned|turned|made|had .* build)\b|^i built",
 'i_tested_tried': r"^(i|i've)\b.*\b(tested|tried|battle tested|spent|benching|used)\b|hours testing|testing ",
 'i_experiment': r"^(i)\b.*\b(gave|told|asked|forced|uploaded|deleted)\b",
 'number_list': r"(?<![.\d])\b\d+\b\s+(\w+\s+)?(ways|tricks|tips|skills|repos|tools|use cases|techniques|lessons|components|fixes|concepts|methods|best|strategies|mcp|things|levels|steps|ai skills|boring|most|claude|github|unsettling|key|must)|^every |these \d|\d+ (are|is) the best",
 'question': r"\?",
 'stance_claim': r"(sucks|dead|is wrong|wrong about|scam|kills|killed|destroy|destroyed|isn't|won't|don't|doesn't|\bnot\b|never|changed|finally|insane|unfair|terrif|dangerous|game changer|unreal|blowing|cheating|nuts|beast|huge|it's not even close|wasn't even close|clearly won|scary|is p\*rn|warning|slop)",
 'how_to': r"(^how |how to|guide|tutorial|here's how|step by step|full workflow|blueprint)",
 'vs_compare': r"(\bvs\.?\b|same app|versus|better than|\bor\b.*\?)",
 'cost_in_title': r"(\$|\bfree\b|cost|price|cheap|token|subscription|limit|paid)",
 'full_course': None,
 'what_you_need_to_know': r"what you need to know",
}
def mw(x,y):
    n1,n2=len(x),len(y)
    if n1<3 or n2<3: return None
    allv=sorted([(v,0) for v in x]+[(v,1) for v in y])
    ranks=[0]*len(allv); i=0; ties=0
    while i<len(allv):
        j=i
        while j+1<len(allv) and allv[j+1][0]==allv[i][0]: j+=1
        r=(i+j)/2+1
        for k in range(i,j+1): ranks[k]=r
        t=j-i+1; ties+=t**3-t; i=j+1
    R1=sum(r for r,(v,g) in zip(ranks,allv) if g==0)
    U=R1-n1*(n1+1)/2; N=n1+n2
    sd=math.sqrt(n1*n2/12*((N+1)-ties/(N*(N-1))))
    z=(U-n1*n2/2)/sd
    p=math.erfc(abs(z)/math.sqrt(2))
    return p
rows_all=[]
for c,v in d.items():
    r=sorted(v['rows'],key=lambda x:x['date'])
    r=[x for x in r if x['dur']>=180]
    for i,x in enumerate(r):
        nb=[y['views'] for j,y in enumerate(r) if j!=i and abs(j-i)<=15]
        x['ratio']=x['views']/st.median(nb)
        x['ch']=c
        t=x['title'].lower()
        x['b']=[k for k,p in B.items() if re.search(p,t)]
        x['f']=[k for k,p in F.items() if p and re.search(p,t)]
        if x['dur']>=3600 or ('course' in t and x['dur']>=1800): x['f'].append('full_course')
        if not x['b']: x['b']=['i_other']
    r=[x for x in r if x['date']<='2026-11-01']
    v['kept']=r; rows_all+=r
json.dump(rows_all,open('coded.json','w'))
with open('coded.csv','w') as f:
    w=csv.writer(f); w.writerow(['ch','id','date','views','dur_min','ratio','buckets','forms','title'])
    for x in rows_all: w.writerow([x['ch'],x['id'],x['date'],x['views'],x['dur']//60,round(x['ratio'],2),'|'.join(x['b']),'|'.join(x['f']),x['title']])
def table(rows,key,names):
    out=[]
    for k in names:
        ins=[x['ratio'] for x in rows if k in x[key]]; outs=[x['ratio'] for x in rows if k not in x[key]]
        if not ins: out.append((k,0,None,None,None,'')); continue
        p=mw(ins,outs)
        top=sorted([x for x in rows if k in x[key]],key=lambda x:-x['ratio'])[:3]
        out.append((k,len(ins),st.median(ins),st.median(outs) if outs else None,p,' ; '.join(f"{x['title'][:55]} ({x['ratio']:.1f}x)" for x in top)))
    return out
bn=list(B)+['i_other']; fn=list(F)
mode=sys.argv[1] if len(sys.argv)>1 else 'all'
for c,v in d.items():
    r=v['kept']
    print(f"\n#### {c}  subs={v['subs']:,}  n={len(r)}  {r[0]['date']}..{r[-1]['date']}  median views={st.median([x['views'] for x in r]):,.0f}  last-30 median={st.median([x['views'] for x in r[-30:]]):,.0f}")
    for title,key,names in [('BUCKET','b',bn),('FORM','f',fn)]:
        print(f"-- {title}: name | n | med ratio in | med out | MW p | top")
        for k,n,mi,mo,p,top in table(r,key,names):
            if n==0: print(f"{k:24s} 0"); continue
            print(f"{k:24s} {n:3d} {mi:5.2f} {mo:5.2f} {('%.3f'%p) if p is not None else '  -  '}  {top if mode=='all' else ''}")
print("\n#### POOLED (ratios are within-channel, so poolable)")
for title,key,names in [('BUCKET','b',bn),('FORM','f',fn)]:
    for k,n,mi,mo,p,top in table(rows_all,key,names):
        if n: print(f"{k:24s} {n:3d} {mi:5.2f} {mo:5.2f} {('%.4f'%p) if p is not None else '-'}")

print("\n#### POOLED EXCLUDING full_course")
nc=[x for x in rows_all if 'full_course' not in x['f']]
for title,key,names in [('BUCKET','b',bn),('FORM','f',fn)]:
    for k,n,mi,mo,p,top in table(nc,key,names):
        if n: print(f"{k:24s} {n:3d} {mi:5.2f} {mo:5.2f} {('%.4f'%p) if p is not None else '-'}")
print("\n#### PER-CHANNEL share of uploads per bucket (%)")
for c,v in d.items():
    r=v['kept']; print(c, ' '.join(f"{k.split('_')[0]}:{100*sum(k in x['b'] for x in r)/len(r):.0f}" for k in bn))

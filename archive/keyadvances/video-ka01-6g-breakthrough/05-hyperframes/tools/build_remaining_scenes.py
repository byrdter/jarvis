#!/usr/bin/env python3
"""Build KA01 S01-S11 HyperFrames compositions and the full host timeline."""

from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]

SCENES = {
    "s01": dict(duration=40.64, start=34.62, mode="timeline", code="EXPECTATION RESET", title="WHAT 4G TAUGHT US", node="SPEED", state="CONSEQUENCE BEFORE CAPABILITY", beats=[
        (0.2,"4G","A network generation became visible through what people did."),(2.48,"APP STORES","Software distribution moved into every pocket."),(5.6,"STREAMING","Video stopped belonging to the living room."),(8.6,"RIDES · MAPS · COMMERCE","Daily behavior changed in ways people could name."),(12.7,"5G","Spectacular speed tests. No single behavior that obvious."),(19.0,"NOT FAILURE","Adoption happened before a defining consumer use."),(23.81,"2.9 BILLION","5G subscriptions expected by end of 2025."),(25.55,"FIXED WIRELESS","A serious broadband alternative."),(28.68,"PRIVATE NETWORKS","Business change, mostly outside public view."),(31.92,"THE LESSON","A headline capability is not its defining use."),(34.5,"CAPABILITY ≠ DEFINING USE","Society discovers the use later."),(37.62,"SPEED","Enters the map—never the center.")]),
    "s02": dict(duration=42.00, start=75.96, mode="spectrum", code="CANDIDATE 01", title="SPEED HAS A CASE", node="SPEED", state="DEMONSTRATED", beats=[
        (0.2,"THE CHIP","An integrated radio-photonic processor."),(2.92,"NATURE · 2025","Peer-reviewed evidence, not a launch promise."),(5.92,"11 × 1.7 mm","The measured processor footprint."),(9.96,"0.5 → 115 GHz","Signal generation across a wide span."),(13.16,"9 BANDS","Consecutive wireless bands supported."),(16.84,"100 Gb/s","Demonstrated on a single lane."),(21.2,"120 Gb/s","Tested near 97.5 GHz."),(26.76,"180 μs","A six-gigahertz frequency shift."),(31.0,"FLEXIBILITY > RECORD","Avoid interference. Escape a poor channel."),(36.0,"LIMITS REMAIN","Equipment and method define the result."),(40.01,"HOW FAR?","The missing measurement changes the story.")]),
    "s03": dict(duration=50.56, start=118.66, mode="route", code="CANDIDATE 02", title="REACH IS A SYSTEM", node="REACH", state="STANDARD DIRECTION", beats=[
        (0.2,"REACH","The second candidate enters."),(3.8,"HIGH FREQUENCY","More information. More fragile paths."),(6.6,"WALLS · RAIN · DISTANCE","Physics does not disappear under a 6G label."),(12.0,"ATMOSPHERIC LOSS","Some bands are especially costly."),(16.12,"50–75 GHz OMITTED","Absorption shaped the Nature wireless tests."),(22.84,"NO SINGLE BEAM","A practical network needs alternatives."),(27.33,"NICT · 2026","60 and 300 GHz worked together."),(33.0,"FALLBACK","When the fragile path degrades, another band carries on."),(38.36,"UBIQUITOUS","Remote communities · satellites · agriculture."),(44.0,"DISASTER RESPONSE","Coverage becomes a portfolio of routes."),(49.0,"WHY CENTIMETRES?","Reach opens the door to positioning.")]),
    "s04": dict(duration=46.48, start=169.92, mode="flow", code="CANDIDATE 03", title="COMPUTE MOVES INTO THE NETWORK", node="INTELLIGENCE", state="PLAUSIBLE APPLICATION", beats=[
        (0.2,"INTELLIGENCE","The third candidate changes where work happens."),(5.0,"ITU · AI + COMMUNICATION","AI is a usage scenario—not merely an app."),(9.5,"DEVICE","Capture the immediate signal."),(14.28,"EDGE","Distributed inference and model sharing."),(18.0,"NETWORK","Data processing and resource orchestration."),(21.64,"FIELD GLASSES","Offload a difficult visual task nearby."),(26.0,"LESS BATTERY","Wearable hardware carries less compute."),(29.32,"RENT INTENSITY","A small company uses local inference only when needed."),(33.96,"NOT A PRODUCT PROMISE","Plausible for 2030 is not available now."),(38.2,"THREE DEPENDENCIES","Cost · energy · orchestration."),(42.26,"THE UNEXPLAINED WORDS","Posture. Movement. Position.")]),
    "s05": dict(duration=59.76, start=217.10, mode="lab", code="MIDPOINT REVERSAL", title="PULL BACK FROM THE CHIP", node="SPEED", state="CORRECTED PICTURE", beats=[
        (0.2,"THE PICTURE CHANGES","The headline crop was too tight."),(3.8,"TINY CHIP","It looks like a base station on a fingernail."),(6.77,"PULL BACK","The system extends beyond the silicon."),(9.01,"LASERS · AMPLIFIERS","External optical and electrical equipment appears."),(13.2,"PHOTODETECTORS · FILTERS","The apparatus keeps expanding."),(16.8,"HORN ANTENNAS","A directional laboratory link."),(19.56,"1.3 METRES","The wireless path was about this long."),(24.0,"206.25 ≠ 2025 CHIP","Two stories were fused into one headline."),(27.02,"OFC · 2022","103.125 Gb/s net at 370 GHz."),(33.96,"THE DOUBLED NUMBER","Not stated in that peer-reviewed abstract."),(39.56,"NOT DEBUNKED","The achievement survives the correction."),(42.04,"RELOCATED","Broad, adaptable signal generation and processing."),(47.0,"NOT AN ENTIRE NETWORK","Nineteen square millimetres is only one component."),(50.52,"NEW QUESTION","What happens when radio, compute, position and measurement converge?"),(56.0,"SPEED MOVES OUTWARD","The map rotates around a different center.")]),
    "s06": dict(duration=51.92, start=277.56, mode="mesh", code="CANDIDATE 04", title="THE NETWORK CAN INFER", node="SENSING", state="STANDARD TARGET", beats=[
        (0.2,"SENSING","The thumbnail needs one correction."),(5.01,"IT DOESN'T SEE","Radio is not a camera."),(6.54,"IT CAN INFER","Changes in a signal describe a scene."),(7.69,"RADIO WAVES","Bodies, walls, rain and motion alter the path."),(13.0,"SAME INFRASTRUCTURE","Communication and measurement share a system."),(19.03,"NIST","Detect objects · track motion · estimate position."),(24.0,"A ROOM BECOMES DATA","Contours resolve without a visible lens."),(27.25,"GESTURE · FALL · VEHICLE","The ITU names concrete sensing uses."),(33.0,"MAPPING · MONITORING","Unconnected objects can still be measured."),(39.24,"1–10 cm","Current positioning target."),(41.24,"TARGET ≠ HOME PERFORMANCE","A standard is not a guarantee."),(46.0,"SENSING MOVES INWARD","The node approaches the person."),(49.31,"WHO DECIDES?","Measurement becomes information about us.")]),
    "s07": dict(duration=48.64, start=330.18, mode="grid", code="CANDIDATE 05", title="FROM DEVICES TO COORDINATION", node="COORDINATION", state="PLAUSIBLE SYSTEM", beats=[
        (0.2,"SENSING FEEDS ACTION","A measurement matters when another system responds."),(3.08,"ROAD","A hidden hazard crosses vehicle boundaries."),(8.84,"WAREHOUSE","Robots reroute around a worker."),(11.64,"PORT","Vehicles and cranes share one changing map."),(15.4,"HOSPITAL","Equipment, rooms and assistance devices coordinate."),(20.44,"NAMED, NOT PROMISED","The framework identifies the ingredients."),(24.0,"AUTOMATED DRIVING","One controlled coordination domain."),(27.0,"MEDICAL ASSISTANCE","Autonomous collaboration between devices."),(30.0,"DIGITAL TWINS","A shared model of physical space."),(33.08,"NOT A NERVOUS SYSTEM—YET","The pieces remain separate."),(37.4,"THE UNIT OF VALUE CHANGES","Many machines act on one model."),(42.0,"COORDINATION UNLOCKS","The fifth node joins the map."),(45.01,"WHO GOVERNS THE SPACE?","The phone is no longer the boundary.")]),
    "s08": dict(duration=50.00, start=379.52, mode="ladder", code="HUMAN USE", title="THE FIRST OPPORTUNITIES", node="WORK", state="EVIDENCE-BASED ADJACENCY", beats=[
        (0.2,"LESS GLAMOROUS THAN AN APP STORE","The work begins underneath the consumer layer."),(5.0,"INFRASTRUCTURE","Modelling · measurement · spectrum."),(10.0,"SYSTEMS","Edge AI · sensing · security."),(15.0,"SERVICES","Testing · integration · compliance."),(21.08,"CONNECT","Sensors to local intelligence."),(24.0,"ADAPT","Robots to shared spatial maps."),(27.0,"PROVE","Equipment safe and reliable."),(30.0,"GOVERN","Spatial data and access."),(32.3,"ADJACENCY, NOT FORECAST","The fields are real; the winners are unknown."),(38.68,"DON'T “BUILD WITH 6G”","Solve one expensive physical-world problem."),(43.0,"CONNECTIVITY + SENSING + COMPUTE","The convergence creates the opening."),(47.64,"CONTROL FOLLOWS MEASUREMENT","Value and power arrive together.")]),
    "s09": dict(duration=40.24, start=430.22, mode="split", code="GOVERNANCE TEST", title="ONE SIGNAL. TWO FUTURES.", node="CHOICE", state="DESIGN DECISION", beats=[
        (0.2,"ONE REFLECTION","The engineering is identical at the start."),(1.8,"FALL ALERT","A room notices danger without a camera."),(4.68,"WORKER TRACKING","Positioning exceeds what someone agreed to."),(9.64,"SHARED MAP","Public coordination—or a private tollbooth."),(14.0,"BENEFIT / CONTROL","The split is institutional, not technical."),(17.32,"ROADMAP REQUIREMENTS","Security · resilience · privacy · access."),(21.0,"CONNECT THE UNCONNECTED","Inclusion belongs beside performance."),(25.8,"BUILT IN BEFORE ARRIVAL","Sensing and consent become defaults."),(29.0,"RETENTION","How long do measurements survive?"),(32.0,"ACCESS","Who can buy the physical record?"),(35.0,"OPT OUT","Can an unconnected person refuse?"),(36.84,"FIVE CANDIDATES VISIBLE","Now we can put them in order.")]),
    "s10": dict(duration=65.12, start=471.16, mode="forecast", code="THE VERDICT", title="THE 6G IMPACT MAP", node="ORDERED", state="DEFENSIBLE FORECAST", beats=[
        (0.2,"THE MAP LANDS","Five capabilities, ordered by human consequence."),(3.64,"CHINA'S BREAKTHROUGH IS REAL","Broad, adaptable radio-photonic processing."),(8.0,"FASTER PHONES","The least consequential part."),(13.88,"THE DEFENSIBLE ORDER","Deployment follows value and constraint."),(15.47,"FIRST","Reliability · capacity · hybrid coverage."),(21.88,"NEXT","Sensing and machine coordination in controlled places."),(26.0,"FACTORIES · PORTS · ROADS","Value can justify equipment and governance."),(30.0,"CAMPUSES · HOSPITALS","Bounded spaces arrive before everywhere."),(33.85,"LATER","Broad consumer experiences—if dependencies align."),(37.0,"COST · ENERGY · STANDARDS · CONSENT","Four gates, not one date."),(40.28,"THE DEEPER SHIFT","Infrastructure becomes perception and coordination."),(45.32,"NOT EVERYWHERE · NOT AUTOMATIC","One chip does not make the future inevitable."),(51.0,"THE CLAIM TEST","Classify the next headline before believing it."),(56.2,"DEMONSTRATED","Did it happen under stated conditions?"),(58.1,"STANDARD TARGET","Is it a formal goal?"),(59.7,"PLAUSIBLE","Do the pieces support the application?"),(61.0,"IMAGINED","Is the product only being sold now?"),(61.66,"SEPARATE NEXT FROM NOISE","That is the useful way to watch 6G.")]),
    "s11": dict(duration=7.92, start=536.98, mode="cta", code="KEYADVANCES", title="WHAT'S REAL. WHAT'S NEXT.", node="SUBSCRIBE", state="NEAR-FUTURE, EXAMINED", beats=[
        (0.1,"REAL","Demonstrated."),(1.8,"TARGETED","Standards direction."),(3.3,"PLAUSIBLE","Human usefulness."),(4.8,"SPECULATIVE","Clearly labelled."),(6.1,"KEYADVANCES","Subscribe for the next important advance.")]),
}

MEDIA = {
    "s01":["s01-clip-headphones-phone-night.mp4","s01-office-vibrant.mp4","s01-manager-tablet-inventory.mp4"],
    "s02":["s02-s02-photonic-light-path.mp4","s02-GlowingDataPacket_CircuitBoard.mp4","s02-clip-two-researchers-whiteboard.mp4"],
    "s03":["s03-datacenter-revolt__br_02b_pylons-farmland.mp4","s03-clip-autonomous-car-highway-lidar.mp4","s03-fork-road-drone.mp4"],
    "s04":["s04-person-pointing-at-screen2.mp4","s04-clip-team-around-monitor-engaged.mp4","s04-celebrity-cac-subsidy__pov-phone-in-hand-notification.mp4"],
    "s05":["s05-s05-chip-to-optical-bench-pullback.mp4","s05-clip-nanolens-cleanroom-macro.mp4","s05-s05-horn-antenna-short-link.mp4"],
    "s06":["s06-hallucinations-v6__br-02a_corridor.mp4","s06-s06-person-radio-spatial-map.mp4","s06-hallucinations-v6__br-10a_hands-of-care.mp4"],
    "s07":["s07-athlete-syndicates-b2b__br-02_ai-in-the-clinic.mp4","s07-clip-warehouse-robots-fulfillment.mp4","s07-clip-smart-factory-robotic-arm.mp4"],
    "s08":["s08-clip-young-old-worker-desk.mp4","s08-datacenter-revolt__br-02c_construction-crew.mp4","s08-datacenter-revolt__br-05a_electrician-hands.mp4"],
    "s09":["s09-hallucinations-v6__br-07a_iv-drip.mp4","s09-s09-ordinary-room-radio-sensing.mp4","s09-superhuman-ban__br-08a_voting-booths.mp4"],
    "s10":["s10-out-window-city-night-view.mp4","s10-hallucinations-v6__br-10b_dawn-hospital.mp4","s10-fear-economy__br-09a_dawn-break.mp4"],
    "s11":["s11-fable-ban__br-02a_lattice.mp4","s11-fable-ban__br-07b_network.mp4","s11-superhuman-ban__br-06a_race-globe.mp4"],
}

CLIP_LOCAL = {
    "s01":[4.2,14.5,27.2], "s02":[4.8,15.5,29.0], "s03":[3.8,24.0,39.5],
    "s04":[3.0,18.2,31.0], "s05":[6.7,14.0,18.8], "s06":[8.0,21.0,34.0],
    "s07":[3.4,9.0,25.0], "s08":[3.0,16.0,29.0], "s09":[1.7,11.0,26.0],
    "s10":[4.0,22.0,36.0], "s11":[0.0,2.65,5.3],
}

MODE_ART = {
 "timeline":"<div class='rail'></div><div class='marks'><i></i><i></i><i></i><i></i><i></i></div>",
 "spectrum":"<div class='bands'>"+"".join(f"<i style='--i:{i}'></i>" for i in range(9))+"</div><div class='sweep'></div>",
 "route":"<div class='mapline a'></div><div class='mapline b'></div><div class='tower'>⌁</div><div class='sat'>◒</div>",
 "flow":"<div class='flow-nodes'><b>DEVICE</b><span>→</span><b>EDGE</b><span>→</span><b>CLOUD</b></div><div class='flowpulse'></div>",
 "lab":"<div class='chip'>11 × 1.7 mm</div><div class='apparatus'><i>LASER</i><i>AMP</i><i>DETECTOR</i><i>HORN</i></div><div class='ruler'>↔ 1.3 m ↔</div>",
 "mesh":"<div class='person'>●<br>┃<br>╱ ╲</div><div class='ring r1'></div><div class='ring r2'></div><div class='ring r3'></div><div class='scan'></div>",
 "grid":"<div class='coord-grid'><i>ROAD</i><i>WAREHOUSE</i><i>PORT</i><i>HOSPITAL</i></div><div class='crosshair'></div>",
 "ladder":"<div class='ladder'><i>INFRASTRUCTURE</i><i>SYSTEMS</i><i>SERVICES</i><i>GOVERNANCE</i></div>",
 "split":"<div class='split good'>BENEFIT</div><div class='split bad'>CONTROL</div><div class='choice-line'></div>",
 "forecast":"<div class='forecast'><i>FIRST</i><span></span><i>NEXT</i><span></span><i>LATER</i></div>",
 "cta":"<div class='ka-mark'>KA</div><div class='signal-rings'></div>",
}

CSS = r"""
*{box-sizing:border-box}#root{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden;color:#f4f1e8;font-family:Montserrat,sans-serif;background:transparent}.wash{position:absolute;inset:0;background:linear-gradient(90deg,rgba(7,19,31,.95) 0%,rgba(7,19,31,.82) 52%,rgba(7,19,31,.4) 100%)}.grain{position:absolute;inset:0;opacity:.11;background-image:repeating-radial-gradient(circle at 15% 20%,rgba(244,241,232,.22) 0 1px,transparent 1px 6px)}.rule{position:absolute;left:104px;right:104px;top:76px;height:3px;background:#d6a84b;transform-origin:left}.code{position:absolute;left:106px;top:98px;color:#d6a84b;font:700 21px/1 'IBM Plex Mono',monospace;letter-spacing:.13em}.state{position:absolute;right:106px;top:96px;border:2px solid #d6a84b;border-radius:999px;padding:9px 15px;color:#d6a84b;font:700 18px/1 'IBM Plex Mono',monospace}.title{position:absolute;left:104px;top:154px;width:1180px;font-size:68px;line-height:.96;font-weight:900;letter-spacing:-.045em}.art{position:absolute;left:104px;right:104px;top:294px;height:404px;border-top:1px solid rgba(155,174,184,.45);border-bottom:1px solid rgba(155,174,184,.45)}.beat{position:absolute;left:104px;bottom:82px;width:1090px;min-height:214px;padding:28px 34px 26px;border-left:8px solid #42b8ad;background:rgba(7,19,31,.91);box-shadow:0 18px 55px rgba(0,0,0,.32)}.beat.paper{background:#eee8da;color:#20282b;border-left-color:#d6a84b}.beat .datum{font-size:60px;line-height:.96;font-weight:900;letter-spacing:-.035em}.beat .sub{margin-top:12px;max-width:1000px;color:#9baeb8;font-size:28px;line-height:1.2}.beat.paper .sub{color:#4f5a5d}.node{position:absolute;right:104px;bottom:92px;width:440px;text-align:right;color:#42b8ad;font:700 24px/1.15 'IBM Plex Mono',monospace}.node b{display:inline-block;margin-top:11px;padding:10px 16px;border:2px solid #42b8ad;border-radius:999px;color:#f4f1e8}.rail{position:absolute;left:40px;right:40px;top:198px;height:5px;background:#42b8ad}.marks{position:absolute;left:80px;right:80px;top:170px;display:flex;justify-content:space-between}.marks i{width:58px;height:58px;border-radius:50%;border:5px solid #d6a84b;background:#07131f}.bands{position:absolute;left:26px;right:26px;top:70px;height:250px;display:flex;gap:14px;align-items:flex-end}.bands i{flex:1;height:calc(44px + var(--i)*22px);background:linear-gradient(#42b8ad,#173c4c);border-top:4px solid #d6a84b}.sweep{position:absolute;top:42px;bottom:42px;width:8px;background:#f4f1e8;box-shadow:0 0 32px #42b8ad}.mapline{position:absolute;height:7px;background:#42b8ad;transform-origin:left}.mapline.a{left:100px;top:265px;width:690px;transform:rotate(-12deg)}.mapline.b{left:755px;top:120px;width:710px;transform:rotate(10deg);background:#d6a84b}.tower,.sat{position:absolute;font-size:100px}.tower{left:40px;top:185px}.sat{right:70px;top:38px;color:#d6a84b}.flow-nodes{position:absolute;left:60px;right:60px;top:130px;display:flex;align-items:center;justify-content:space-between}.flow-nodes b{padding:30px;border:3px solid #42b8ad;font:900 34px/1 'IBM Plex Mono',monospace}.flow-nodes span{font-size:70px;color:#d6a84b}.flowpulse{position:absolute;left:90px;top:246px;width:40px;height:40px;border-radius:50%;background:#d6a84b;box-shadow:0 0 35px #d6a84b}.chip{position:absolute;left:60px;top:130px;padding:28px 34px;border:4px solid #d6a84b;font:900 42px/1 'IBM Plex Mono',monospace}.apparatus{position:absolute;left:510px;right:40px;top:92px;display:flex;gap:18px}.apparatus i{padding:28px 18px;border:3px solid #42b8ad;font:700 24px/1 'IBM Plex Mono',monospace}.ruler{position:absolute;left:760px;top:250px;color:#d6a84b;font:900 42px/1 'IBM Plex Mono',monospace}.person{position:absolute;left:790px;top:95px;text-align:center;font:900 48px/1.25 'IBM Plex Mono',monospace}.ring{position:absolute;left:640px;top:-20px;border:3px solid rgba(66,184,173,.6);border-radius:50%}.r1{width:330px;height:330px}.r2{left:550px;top:-110px;width:510px;height:510px}.r3{left:455px;top:-205px;width:700px;height:700px}.scan{position:absolute;left:150px;top:190px;width:1180px;height:4px;background:#d6a84b;box-shadow:0 0 28px #d6a84b}.coord-grid{position:absolute;inset:28px;display:grid;grid-template-columns:1fr 1fr;gap:14px}.coord-grid i{display:grid;place-items:center;border:3px solid #42b8ad;background:rgba(7,19,31,.65);font:900 35px/1 'IBM Plex Mono',monospace}.crosshair{position:absolute;left:50%;top:50%;width:50px;height:50px;border:5px solid #d6a84b;border-radius:50%;transform:translate(-50%,-50%)}.ladder{position:absolute;left:220px;top:20px;width:1020px;display:flex;flex-direction:column-reverse;gap:12px}.ladder i{height:78px;padding:23px 28px;background:linear-gradient(90deg,#173c4c,rgba(23,60,76,.1));border-left:8px solid #d6a84b;font:900 30px/1 'IBM Plex Mono',monospace}.split{position:absolute;top:25px;bottom:25px;width:48%;display:grid;place-items:center;font:900 50px/1 'IBM Plex Mono',monospace}.split.good{left:0;background:rgba(66,184,173,.22)}.split.bad{right:0;background:rgba(214,92,89,.2)}.choice-line{position:absolute;left:50%;top:0;bottom:0;width:5px;background:#d6a84b}.forecast{position:absolute;left:80px;right:80px;top:150px;display:flex;align-items:center}.forecast i{padding:30px;border:4px solid #42b8ad;font:900 38px/1 'IBM Plex Mono',monospace}.forecast span{flex:1;height:5px;background:#d6a84b}.ka-mark{position:absolute;left:590px;top:55px;width:330px;height:280px;display:grid;place-items:center;border:10px solid #d6a84b;font-size:145px;font-weight:900}.signal-rings{position:absolute;left:470px;top:-70px;width:570px;height:570px;border:4px solid #42b8ad;border-radius:50%}.mode-cta .title{font-size:86px}.mode-cta .beat{width:1180px}.mode-cta .art{border:0}.mode-cta .state{border-color:#42b8ad;color:#42b8ad}
"""

def scene_html(sid, cfg):
    beats=[]
    for i,(t,datum,sub) in enumerate(cfg["beats"]):
        paper=" paper" if i % 4 == 1 else ""
        beats.append(f'<div id="{sid}-b{i}" class="beat{paper}"><div class="datum">{escape(datum)}</div><div class="sub">{escape(sub)}</div></div>')
    anim=[]
    for i,(t,_,__) in enumerate(cfg["beats"]):
        anim.append(f'tl.fromTo("#{sid}-b{i}",{{x:-90,opacity:0,scale:.96}},{{x:0,opacity:1,scale:1,duration:.42,ease:"power3.out"}},{t});')
        if i:
            anim.append(f'tl.to("#{sid}-b{i-1}",{{x:38,opacity:0,duration:.14,ease:"power2.in"}},{max(t-.18,0):.2f});')
    mode=cfg['mode']
    special = {
      "timeline":f'tl.fromTo(".rail",{{scaleX:0}},{{scaleX:1,duration:{cfg["duration"]-1:.2f},ease:"none"}},.3);',
      "spectrum":f'tl.fromTo(".sweep",{{x:0}},{{x:1410,duration:{cfg["duration"]-1:.2f},ease:"none"}},.2);',
      "route":'tl.fromTo(".mapline",{scaleX:0},{scaleX:1,duration:2.2,stagger:.5,ease:"power2.out"},1.0);',
      "flow":f'tl.fromTo(".flowpulse",{{x:0}},{{x:1190,duration:{cfg["duration"]-1:.2f},ease:"none"}},.4);',
      "lab":'tl.fromTo(".apparatus i",{y:-50,opacity:0},{y:0,opacity:1,duration:.4,stagger:.22,ease:"back.out(1.3)"},6.77);tl.fromTo(".ruler",{scaleX:0,opacity:0},{scaleX:1,opacity:1,duration:.7,ease:"power3.out"},19.56);',
      "mesh":f'tl.fromTo(".ring",{{scale:.7,opacity:.15}},{{scale:1.12,opacity:.78,duration:{cfg["duration"]-1:.2f},stagger:.2,ease:"sine.inOut"}},.2);tl.fromTo(".scan",{{y:-150}},{{y:170,duration:{cfg["duration"]-1:.2f},ease:"none"}},.3);',
      "grid":'tl.fromTo(".coord-grid i",{scale:.7,opacity:0},{scale:1,opacity:1,duration:.45,stagger:.5,ease:"back.out(1.2)"},2.8);',
      "ladder":'tl.fromTo(".ladder i",{scaleX:0,opacity:0},{scaleX:1,opacity:1,duration:.55,stagger:2.2,ease:"power3.out",transformOrigin:"left"},4.5);',
      "split":f'tl.fromTo(".choice-line",{{scaleY:0}},{{scaleY:1,duration:.6,ease:"power3.out"}},8.8);tl.fromTo(".good",{{x:-80,opacity:0}},{{x:0,opacity:1,duration:.5}},1.8);tl.fromTo(".bad",{{x:80,opacity:0}},{{x:0,opacity:1,duration:.5}},4.68);',
      "forecast":'tl.fromTo(".forecast i",{y:50,opacity:0},{y:0,opacity:1,duration:.5,stagger:6.4,ease:"power3.out"},15.2);tl.fromTo(".forecast span",{scaleX:0},{scaleX:1,duration:4.5,stagger:6.4,ease:"none"},15.7);',
      "cta":f'tl.fromTo(".ka-mark",{{scale:.72,rotation:-5,opacity:0}},{{scale:1,rotation:0,opacity:1,duration:.65,ease:"back.out(1.3)"}},3.0);tl.fromTo(".signal-rings",{{scale:.65,opacity:.1}},{{scale:1.25,opacity:.7,duration:{cfg["duration"]-1:.2f},ease:"sine.inOut"}},.1);',
    }[mode]
    return f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"></head><body><template><style>{CSS}</style>
<div id="root" data-composition-id="ka01-{sid}" data-width="1920" data-height="1080" data-duration="{cfg['duration']}">
<div class="mode-{mode}" style="position:absolute;inset:0"><div class="wash"></div><div class="grain" data-layout-ignore></div><div id="{sid}-rule" class="rule"></div><div class="code">KA01 / {escape(cfg['code'])}</div><div class="state">{escape(cfg['state'])}</div><div class="title">{escape(cfg['title'])}</div><div class="art">{MODE_ART[mode]}</div>{''.join(beats)}<div class="node">IMPACT MAP<br><b>{escape(cfg['node'])}</b></div></div></div>
<script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});tl.fromTo("#{sid}-rule",{{scaleX:0}},{{scaleX:1,duration:.55,ease:"power3.out"}},.05);tl.fromTo(".title",{{y:35,opacity:0}},{{y:0,opacity:1,duration:.55,ease:"power3.out"}},.15);{special}{''.join(anim)}window.__timelines["ka01-{sid}"]=tl;</script></template></body></html>'''

def build_index():
    s00='''<div id="el-s00" class="clip" data-composition-id="ka01-s00" data-composition-src="compositions/s00-three-numbers.html" data-start="0" data-duration="33.92" data-track-index="1" data-width="1920" data-height="1080"></div>
<video id="s00-data-flow" class="clip host-media" src="assets/video/s00-data-flow.mp4" data-start="0" data-duration="5.04" data-track-index="2" muted playsinline></video>
<video id="s00-network" class="clip host-media" src="assets/video/s00-network.mp4" data-start="10.8" data-duration="5.04" data-track-index="3" muted playsinline></video>
<video id="s00-wafer" class="clip host-media" src="assets/video/s00-wafer-fab.mp4" data-start="15.7" data-duration="5.0" data-track-index="4" muted playsinline></video>
<audio id="s00-voice" class="clip" src="assets/audio/s00-narration.wav" data-start="0" data-duration="33.92" data-track-index="20" data-volume="1"></audio>'''
    blocks=[s00]
    for sid,cfg in SCENES.items():
        st=cfg['start']; dur=cfg['duration']
        scene_media=[f'<img id="{sid}-bg" class="clip host-bg" src="assets/images/{sid}-background.jpg" data-start="{st}" data-duration="{dur}" data-track-index="0">']
        scene_media.append(f'''<div id="el-{sid}" class="clip" data-composition-id="ka01-{sid}" data-composition-src="compositions/{sid}-{cfg['mode']}.html" data-start="{st}" data-duration="{dur}" data-track-index="1" data-width="1920" data-height="1080"></div>''')
        for i,(name,local) in enumerate(zip(MEDIA[sid],CLIP_LOCAL[sid])):
            cd=4.0 if sid == 's05' and i == 2 else (5.0 if sid != 's11' else 2.62)
            scene_media.append(f'<video id="{sid}-v{i}" class="clip host-inset inset-{i}" src="assets/video/{name}" data-start="{st+local:.2f}" data-duration="{cd}" data-track-index="{2+i}" muted playsinline></video>')
        scene_media.append(f'<audio id="{sid}-voice" class="clip" src="assets/audio/{sid}-narration.wav" data-start="{st}" data-duration="{dur}" data-track-index="{20+int(sid[1:])}" data-volume="1"></audio>')
        blocks.extend(scene_media)
    host_anim=[]
    for sid,cfg in SCENES.items():
        st=cfg['start']; dur=cfg['duration']
        camera_times=[0.08]
        previous=0.08
        for cue,_,__ in cfg['beats'][1:]:
            while cue-previous > 3.8:
                previous += 3.5
                camera_times.append(previous)
            camera_times.append(cue)
            previous=cue
        while dur-previous > 3.8:
            previous += 3.5
            camera_times.append(previous)
        poses=[(-28,-12,1.12),(18,8,1.14),(-12,16,1.13),(30,-6,1.15),(0,0,1.12)]
        x0,y0,z0=poses[0]
        host_anim.append(f'tl.set("#{sid}-bg",{{scale:{z0},x:{x0},y:{y0}}},{st});')
        for j,local in enumerate(camera_times[1:],1):
            x,y,z=poses[j%len(poses)]
            host_anim.append(f'tl.to("#{sid}-bg",{{scale:{z},x:{x},y:{y},duration:.56,ease:"power2.inOut"}},{st+local:.2f});')
        for i,local in enumerate(CLIP_LOCAL[sid]):
            at=st+local
            host_anim.append(f'tl.fromTo("#{sid}-v{i}",{{x:{110 if i%2==0 else -110},opacity:0,scale:1.08}},{{x:0,opacity:.82,scale:1,duration:.45,ease:"power3.out"}},{at:.2f});')
    return f'''<!doctype html><html lang="en" data-resolution="landscape"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080"><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>*{{box-sizing:border-box}}html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#07131f}}body{{font-family:Montserrat,sans-serif}}#root{{position:relative;width:1920px;height:1080px;overflow:hidden;background:#07131f}}#root>div[data-composition-src]{{position:absolute;inset:0;z-index:1}}.host-media,.host-bg,.host-inset{{position:absolute;object-fit:cover;overflow:hidden}}.host-bg{{inset:0;width:1920px;height:1080px;z-index:0;filter:saturate(.66) contrast(1.18) brightness(.48)}}.host-media,.host-inset{{z-index:2}}.host-inset{{width:610px;height:344px;right:100px;top:322px;border:3px solid rgba(244,241,232,.72);box-shadow:0 22px 70px rgba(0,0,0,.5);filter:saturate(.78) contrast(1.1) brightness(.8)}}.inset-1{{top:285px;right:145px}}.inset-2{{top:360px;right:78px}}#s00-data-flow{{inset:0;width:1920px;height:1080px;opacity:.5}}#s00-network{{left:1090px;top:168px;width:690px;height:500px;border-radius:12px;opacity:.56}}#s00-wafer{{left:1032px;top:154px;width:746px;height:560px;border-radius:12px;opacity:.62}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="544.9">{''.join(blocks)}</div><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});tl.fromTo("#s00-data-flow",{{scale:1.16,opacity:.18}},{{scale:1,opacity:.5,duration:4.8,ease:"power2.out"}},0);tl.fromTo("#s00-network",{{x:130,scale:1.12,opacity:0}},{{x:0,scale:1,opacity:.56,duration:.55,ease:"power3.out"}},10.8);tl.fromTo("#s00-wafer",{{x:150,scale:1.18,opacity:0}},{{x:0,scale:1,opacity:.62,duration:.65,ease:"expo.out"}},15.7);{''.join(host_anim)}window.__timelines["main"]=tl;</script></body></html>'''

def main():
    comp=ROOT/'compositions'; comp.mkdir(exist_ok=True)
    for sid,cfg in SCENES.items():
        (comp/f"{sid}-{cfg['mode']}.html").write_text(scene_html(sid,cfg))
    (ROOT/'index.html').write_text(build_index())

if __name__ == '__main__': main()

import cv2, numpy as np, glob, os, re, base64
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
prof = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")

def sheets(path):
    """Pull every JPEG out of an mhtml by byte-scanning + base64 blocks."""
    raw = open(path,'rb').read()
    out=[]
    # base64-encoded parts
    for m in re.finditer(rb'Content-Transfer-Encoding: base64\r?\n\r?\n(.*?)\r?\n--', raw, re.S):
        try:
            d=base64.b64decode(re.sub(rb'\s',b'',m.group(1)))
            if d[:2]==b'\xff\xd8': out.append(d)
        except Exception: pass
    if out: return out
    i=0
    while True:
        s=raw.find(b'\xff\xd8\xff', i)
        if s<0: break
        e=raw.find(b'\xff\xd9', s)
        if e<0: break
        out.append(raw[s:e+2]); i=e+2
    return out

rows=[]
for f in sorted(glob.glob('frames2/*.mhtml')):
    name=os.path.basename(f)[:-6]
    if name.startswith('iob_'): continue
    tiles_total=0; tiles_face=0
    for blob in sheets(f):
        img=cv2.imdecode(np.frombuffer(blob,np.uint8), cv2.IMREAD_COLOR)
        if img is None: continue
        h,w=img.shape[:2]
        tw,th=320,180
        cols,rowsn=max(1,w//tw),max(1,h//th)
        for r in range(rowsn):
            for c in range(cols):
                t=img[r*th:(r+1)*th, c*tw:(c+1)*tw]
                if t.shape[0]<100: continue
                t=cv2.resize(t,(640,360))
                g=cv2.cvtColor(t,cv2.COLOR_BGR2GRAY); g=cv2.equalizeHist(g)
                tiles_total+=1
                d=casc.detectMultiScale(g,1.1,6,minSize=(60,60))
                if len(d)==0: d=prof.detectMultiScale(g,1.1,6,minSize=(60,60))
                if len(d)>0: tiles_face+=1
    if tiles_total:
        rows.append((100*tiles_face/tiles_total, name, tiles_face, tiles_total))
rows.sort(reverse=True)
print(f"{'channel':<30}{'% frames w/ face':>18}{'   n':>8}")
for p,n,fc,tt in rows: print(f"{n:<30}{p:>17.1f}%{tt:>8}")

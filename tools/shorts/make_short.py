import json, sys, math, subprocess, numpy as np, soundfile as sf, re, random
from PIL import Image, ImageDraw, ImageFont
from kokoro_onnx import Kokoro
spec=json.load(open(sys.argv[1])); slug=spec['slug']
W,H,FPS=1080,1920,30
SL=(31,58,77); SL2=(38,70,92); OW=(245,241,232); OR=(242,140,40); MU=(150,170,182)
FB='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; FM='/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
F_CAP=ImageFont.truetype(FB,92); F_BIG=ImageFont.truetype(FB,230); F_MED=ImageFont.truetype(FB,64); F_SM=ImageFont.truetype(FM,40); F_BADGE=ImageFont.truetype(FB,52)
# ---------- voice ----------
import os
MD=os.environ.get('KOKORO_DIR','/home/claude/podcast/models')
k=Kokoro(MD+'/kokoro-v1.0.onnx',MD+'/voices-v1.0.bin')
SR=24000; GAP=0.22; LEAD=0.7
segs=[]; t=LEAD; voice=[]
for s in spec['segments']:
    a,sr=k.create(s['text'],voice='am_michael',speed=1.08,lang='en-us'); assert sr==SR
    d=len(a)/SR; segs.append({**s,'t0':t,'t1':t+d}); voice.append((t,a)); t+=d+GAP
TOTAL=t+0.6
N=int(TOTAL*SR)
vo=np.zeros(N,dtype=np.float32)
for t0,a in voice: i=int(t0*SR); vo[i:i+len(a)]+=a
# ---------- sound design (original, synthesized) ----------
tt=np.arange(N)/SR; sfx=np.zeros(N,dtype=np.float32)
def put(sig,at,gain=1.0):
    i=int(at*SR); j=min(N,i+len(sig)); sfx[i:j]+=sig[:j-i]*gain
# signature: tool click + low warm tone
n=int(0.05*SR); click=np.random.RandomState(1).randn(n)*np.exp(-np.arange(n)/(0.006*SR)); put(click,0.05,0.5)
n=int(0.9*SR); x=np.arange(n)/SR; tone=(np.sin(2*np.pi*110*x)+.4*np.sin(2*np.pi*220*x)+.15*np.sin(2*np.pi*330*x))*np.exp(-x*4)*np.minimum(1,x*60); put(tone,0.08,0.22)
# whoosh on scene changes
def whoosh():
    n=int(0.35*SR); w=np.random.RandomState(2).randn(n); 
    # simple moving-average lowpass sweep
    out=np.zeros(n); acc=0
    for i in range(n):
        a=0.02+0.3*(i/n); acc+=a*(w[i]-acc); out[i]=acc
    env=np.sin(np.pi*np.arange(n)/n)**2; return (out*env).astype(np.float32)
wh=whoosh()
for s in segs[1:]: put(wh,max(0,s['t0']-0.25),0.35)
# soft pad bed: Am F C G
chords=[(220,261.6,329.6),(174.6,220,261.6),(130.8,164.8,196),(196,246.9,293.7)]
bed=np.zeros(N,dtype=np.float32); L=2.4
for ci in range(int(TOTAL/L)+1):
    f=chords[ci%4]; i0=int(ci*L*SR); n=min(int(L*SR),N-i0)
    if n<=0: break
    x=np.arange(n)/SR; env=np.minimum(1,x/0.4)*np.minimum(1,(L-x)/0.4)
    bed[i0:i0+n]+=sum(np.sin(2*np.pi*fr*x)+.3*np.sin(2*np.pi*fr*2*x) for fr in f)*env/6
mix=vo*1.0+sfx+bed*0.05
mix=mix/np.max(np.abs(mix))*0.89
sf.write(f'{slug}.wav',mix,SR)
# ---------- captions ----------
caps=[]
for s in segs:
    words=s['text'].split(); chunks=[]; cur=[]
    for w_ in words:
        cur.append(w_)
        if len(cur)>=3 or re.search(r'[.,?!]$',w_): chunks.append(' '.join(cur)); cur=[]
    if cur: chunks.append(' '.join(cur))
    tot=sum(len(c)+3 for c in chunks); tt0=s['t0']
    for c in chunks:
        d=(s['t1']-s['t0'])*(len(c)+3)/tot; caps.append((tt0,tt0+d,c)); tt0+=d
KEY=set(spec.get('keys','').split()) or set('freeze trickle warm drain 55 fifty-five flame torch plumber landlord moving hose heat four one two three crack gallons follow'.split())
# ---------- drawing ----------
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def text_c(d,xy,s,f,fill): w=d.textlength(s,font=f); d.text((xy[0]-w/2,xy[1]),s,font=f,fill=fill)
def drop(d,cx,cy,r,col):
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=col); d.polygon([(cx-r*.92,cy-r*.35),(cx,cy-r*2.3),(cx+r*.92,cy-r*.35)],fill=col)
def wrench_icon(d,cx,cy,s,col):
    ang=math.radians(-45); ca,sa=math.cos(ang),math.sin(ang)
    def R(x,y): return (cx+x*ca-y*sa, cy+x*sa+y*ca)
    hw=s*.09; d.polygon([R(-hw,-s*.1),R(hw,-s*.1),R(hw,s*.55),R(-hw,s*.55)],fill=col)
    hx,hy=R(0,-s*.32); r=s*.22; d.ellipse((hx-r,hy-r,hx+r,hy+r),fill=col)
    jx,jy=R(0,-s*.45); j=s*.1; d.ellipse((jx-j,jy-j,jx+j,jy+j),fill=SL)
    d.polygon([R(-j,-s*.45),R(j,-s*.45),R(j,-s*.62),R(-j,-s*.62)],fill=SL)
def scene(d,sc,lt,t):
    cx,cy=W/2,820; p=ease(lt/0.45)
    if sc=='hook':
        n=int(250*ease(lt/1.6)); text_c(d,(cx,560),str(n),F_BIG,OR); text_c(d,(cx,820),'GALLONS / DAY',F_MED,OW)
        text_c(d,(cx,910),'from one small crack',F_SM,MU)
        for i in range(5):
            ph=(t*1.1+i/5)%1; drop(d,cx-260+i*130,380+ph*80,16,(120,170,200) if i%2 else OW)
        # pipe with crack
        d.rounded_rectangle((180,1010,900,1080),radius=35,fill=SL2,outline=OW,width=6)
        d.line([(540,1010),(525,1035),(550,1050),(535,1080)],fill=OR,width=7)
    elif sc=='faucet':
        d.rounded_rectangle((260,560,620,640),radius=40,fill=OW); d.rounded_rectangle((540,560,640,760),radius=40,fill=OW)
        d.rounded_rectangle((380,500,500,560),radius=18,fill=MU)
        for i in range(3):
            ph=((t*1.4)+i/3)%1; drop(d,590,790+ph*330,18,(140,190,220))
        d.rounded_rectangle((420,1150,760,1175),radius=12,fill=SL2)
    elif sc=='cabinet':
        d.rectangle((250,520,830,1080),fill=SL2,outline=OW,width=8)
        # U-trap
        d.line([(540,520),(540,800)],fill=MU,width=40); d.arc((440,720,640,920),0,180,fill=MU,width=40); d.line([(640,820),(830,820)],fill=MU,width=40)
        o=ease((lt-0.3)/0.9); dw=int(290*(1-0.82*o))
        d.rectangle((250,520,250+dw,1080),fill=OW,outline=SL,width=6); d.rectangle((830-dw,520,830,1080),fill=OW,outline=SL,width=6)
        if o>0.6:
            for i in range(3):
                y=620+i*120; sh=int(25*math.sin(t*6+i)); d.line([(380+sh,y),(430-sh,y+40),(380+sh,y+80)],fill=OR,width=8)
    elif sc=='hose':
        for i in range(4): r=110+i*42; d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(120,190,120) if i%2 else (90,160,95),width=26)
        off=ease((lt-0.4)/0.8)*150
        d.rectangle((W-170,cy-60,W-100,cy+60),fill=OW); d.rectangle((W-230,cy-28,W-170,cy+28),fill=OW)
        d.line([(cx+250,cy),(cx+300-off,cy)],fill=(90,160,95),width=26)
        d.rounded_rectangle((W-360-off,cy-30,W-230-off,cy+30),radius=14,fill=MU)
        if lt>1.0:
            for i in range(3): ph=((t*1.3)+i/3)%1; drop(d,W-300-off,cy+70+ph*200,14,(140,190,220))
    elif sc=='thermo':
        d.rounded_rectangle((300,520,780,1060),radius=60,fill=OW)
        v=int(45+10*ease((lt-0.2)/1.2)); text_c(d,(cx,640),f'{v}°',F_BIG,SL); text_c(d,(cx,900),'OR HIGHER',F_MED,OR)
    elif sc=='warn':
        if lt<2.6:
            fx,fy=cx,820; fl=1+0.08*math.sin(t*14)
            d.polygon([(fx,fy-200*fl),(fx+120,fy+40),(fx,fy+130),(fx-120,fy+40)],fill=OR); d.polygon([(fx,fy-60*fl),(fx+55,fy+60),(fx,fy+110),(fx-55,fy+60)],fill=(255,205,120))
            d.ellipse((fx-260,fy-260,fx+260,fy+260),outline=(230,80,70),width=30); d.line([(fx-185,fy-185),(fx+185,fy+185)],fill=(230,80,70),width=30)
            text_c(d,(cx,1110),'NO OPEN FLAME',F_MED,OW)
        else:
            d.rounded_rectangle((290,640,700,860),radius=100,fill=OW); d.rounded_rectangle((470,820,580,1080),radius=30,fill=OW); d.ellipse((600,660,780,840),fill=MU)
            for i in range(3):
                y=700+i*60; ph=(t*2+i/3)%1; d.line([(800+ph*120,y),(860+ph*120,y)],fill=OR,width=10)
            text_c(d,(cx,1110),'hair dryer = safer',F_MED,OW)
    elif sc=='stat':
        st=SCN_CUR
        big=st['big']; 
        if big.isdigit():
            big=str(int(int(big)*ease(lt/1.4)))
        text_c(d,(cx,560),big+st.get('unit',''),F_BIG,OR); text_c(d,(cx,830),st.get('label',''),F_MED,OW); text_c(d,(cx,920),st.get('note',''),F_SM,MU)
    elif sc=='vs':
        st=SCN_CUR; o2=ease((lt-1.2)/0.5)
        for i,(tmp,lab,col) in enumerate(st["rows"]):
            col=tuple(int(v) for v in col.strip("()").split(","))
            if i==1 and o2<=0: continue
            y=560+i*300
            d.rounded_rectangle((170,y,910,y+240),radius=40,fill=OW if i==1 else SL2,outline=col,width=8)
            d.text((220,y+30),tmp,font=ImageFont.truetype(FB,140),fill=col if i==0 else SL)
            d.text((560,y+50),lab,font=F_MED,fill=OW if i==0 else SL); 
    elif sc=='heater':
        d.rounded_rectangle((360,480,720,1120),radius=70,fill=OW); d.rectangle((360,600,720,612),fill=MU)
        d.ellipse((470,860,610,1000),fill=SL2,outline=OR,width=8)
        v=int(140-20*ease((lt-0.8)/1.4)); text_c(d,(540,890),f'{v}',F_MED,OW)
        d.rounded_rectangle((420,1120,460,1170),radius=8,fill=MU); d.rounded_rectangle((620,1120,660,1170),radius=8,fill=MU)
        text_c(d,(cx,1040+120*0),'',F_SM,MU)
    elif sc=='sediment':
        d.rounded_rectangle((330,480,690,1120),radius=70,fill=OW)
        rr=random.Random(5)
        for i in range(60):
            x=rr.randint(370,650); y=1090-int(rr.random()**2*110); d.ellipse((x-6,y-6,x+6,y+6),fill=MU)
        # quart jar
        jx=800; d.rounded_rectangle((jx-70,860,jx+70,1100),radius=20,outline=OW,width=8)
        lvl=int(220*ease((lt-0.5)/1.5)); d.rectangle((jx-62,1092-lvl,jx+62,1092),fill=(140,190,220))
        d.line([(690,1060),(jx-80,1060)],fill=MU,width=18)
        text_c(d,(jx,1120),'1 qt / 3 mo',F_SM,OW)
    elif sc=='hair':
        d.ellipse((240,560,840,1080),fill=OW); d.ellipse((440,760,640,880),fill=SL2)
        rr=random.Random(3)
        for i in range(14):
            pts=[(540+rr.randint(-60,60),820+rr.randint(-30,30))]
            for j in range(4): pts.append((pts[-1][0]+rr.randint(-50,50),pts[-1][1]+rr.randint(-40,40)))
            d.line(pts,fill=(60,50,45),width=5)
        # slow water level
        d.text((cx-150,1100),'slow...',font=F_MED,fill=MU)
    elif sc=='stopper':
        up=ease((lt-0.3)/1.0)*260
        d.rectangle((300,980,780,1010),fill=OW)
        d.rounded_rectangle((470,980-up-40,610,980-up+10),radius=20,fill=MU); d.rectangle((530,980-up,550,1150-up),fill=MU)
        rr=random.Random(8)
        for i in range(10):
            y=1000-up+i*14; d.line([(540,y),(540+rr.randint(-70,70),y+rr.randint(10,40))],fill=(60,50,45),width=5)
        d.text((610,560),'twist +\nlift',font=F_MED,fill=OR)
    elif sc=='snake':
        yy=int(120*math.sin(min(lt,3)*2.2)) if lt>0.4 else 0
        d.rectangle((300,1000,780,1030),fill=OW); d.rectangle((300,1030,780,1180),fill=SL2)
        x0=525; d.rectangle((x0,520-yy,x0+30,1150-yy),fill=(70,190,120))
        for i in range(14):
            y=620+i*38-yy; d.polygon([(x0,y),(x0-28,y+16),(x0,y+18)],fill=(70,190,120)); d.polygon([(x0+30,y+10),(x0+58,y+26),(x0+30,y+28)],fill=(70,190,120))
        d.rounded_rectangle((x0-40,480-yy,x0+70,540-yy),radius=20,fill=(50,160,100))
    elif sc=='chem':
        d.rounded_rectangle((420,600,660,1060),radius=40,fill=OW); d.rectangle((480,520,600,600),fill=MU); d.rectangle((440,740,640,900),fill=OR)
        text_c(d,(540,780),'LYE',F_MED,SL)
        d.ellipse((290,560,790,1100),outline=(230,80,70),width=28); d.line([(375,645),(705,1015)],fill=(230,80,70),width=28)
    elif sc=='grease':
        d.ellipse((180,700,560,900),fill=MU); d.rectangle((540,780,690,820),fill=MU); d.ellipse((220,730,520,870),fill=(205,180,90))
        o=ease((lt-1.0)/0.8)
        jx=820; d.rounded_rectangle((jx-80,820-int(40*o),jx+80,1060),radius=24,outline=OW,width=8); d.rectangle((jx-72,980,jx+72,1052),fill=(205,180,90))
        if o>0.5: d.rectangle((jx-90,800-int(40*o),jx+90,830-int(40*o)),fill=OW)
        text_c(d,(cx,1110),'cool · seal · trash',F_MED,OW)
    elif sc=='cta':
        wrench_icon(d,cx,780,420,OW); d.ellipse((cx+120,560,cx+200,640),fill=OR)
        text_c(d,(cx,1040),'@renterfix',F_MED,OR)
SCN_CUR=None
def frame(t):
    im=Image.new('RGB',(W,H),SL); d=ImageDraw.Draw(im)
    for x in range(0,W,72): d.line((x,0,x,H),fill=(35,64,84),width=2)
    # brand
    wrench_icon(d,110,170,90,OW); d.text((165,138),'RenterFix',font=F_MED,fill=OW)
    s=next((s for s in segs if s['t0']-GAP<=t<s['t1']+GAP), segs[-1] if t>=segs[-1]['t0'] else segs[0])
    lt=t-s['t0']+0.25
    if s.get('badge'):
        bw=d.textlength(s['badge'],font=F_BADGE)+56; d.rounded_rectangle((W-90-bw,130,W-90,212),radius=40,fill=OR); d.text((W-90-bw+28,138),s['badge'],font=F_BADGE,fill=SL)
    # scene slide-in
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); ld=ImageDraw.Draw(lay)
    global SCN_CUR; SCN_CUR=s; scene(ld,s['scene'],lt,t)
    off=int((1-ease(lt/0.35))*120); im.paste(lay,(0,off),lay)
    # caption
    c=next((c for c in caps if c[0]<=t<c[1]),None)
    if c:
        words=c[2].split(); y=1270
        line=' '.join(words); wtot=d.textlength(line,font=F_CAP); x=W/2-wtot/2
        if wtot>W-120:
            x=60
        for w_ in words:
            col=OR if re.sub(r'[^a-z0-9-]','',w_.lower()) in KEY else OW
            ww=d.textlength(w_+' ',font=F_CAP)
            for dx,dy in ((4,4),): d.text((x+dx,y+dy),w_,font=F_CAP,fill=(15,30,40))
            d.text((x,y),w_,font=F_CAP,fill=col); x+=ww
    # progress
    d.rectangle((0,H-12,int(W*t/TOTAL),H),fill=OR)
    return im
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',f'{slug}.wav',
  '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-af','loudnorm=I=-14:TP=-1.5','-shortest',f'{slug}.mp4'],stdin=subprocess.PIPE)
for i in range(int(TOTAL*FPS)): p.stdin.write(frame(i/FPS).tobytes())
p.stdin.close(); p.wait()
json.dump({'total':TOTAL,'segs':[(s['scene'],round(s['t0'],2),round(s['t1'],2)) for s in segs]},open(f'{slug}.timing.json','w'))
print('done',round(TOTAL,1))

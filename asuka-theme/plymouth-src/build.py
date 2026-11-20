#!/usr/bin/env python3
"""Plymouth theme asuka-nerv: проверенный скрипт nyarch-logo + свои картинки."""
import os, shutil, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps
SRC="/usr/share/plymouth/themes/nyarch-logo"
A=os.path.expanduser("~/.local/share/asuka-theme")
OUT=A+"/plymouth/asuka-nerv"; shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
F=os.path.expanduser("~/.local/share/fonts/nerv")
SER=F+"/ShipporiMinchoB1-ExtraBold.ttf"; OSW=F+"/Oswald[wght].ttf"; JP=F+"/NotoSansJP[wght].ttf"
RED=(220,38,48,255); ORG=(255,106,19,255); DIM=(150,110,100,255)
W,H=1063,360
def font(p,s,var=None):
    f=ImageFont.truetype(p,s)
    if var:
        try: f.set_variation_by_axes([var])
        except Exception: pass
    return f
def hexmask(size):
    m=Image.new("L",(size,size),0); d=ImageDraw.Draw(m); c=size/2; r=size/2
    d.polygon([(c+r*math.cos(math.radians(60*k+30)),c+r*math.sin(math.radians(60*k+30))) for k in range(6)],fill=255); return m
def base():
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    s=300; x0,y0=30,30
    hx=Image.new("RGBA",(s+16,s+16),(0,0,0,0)); m=hexmask(s+16); hx.paste(Image.new("RGBA",(s+16,s+16),RED),(0,0),m)
    im.alpha_composite(hx,(x0-8,y0-8))
    av=ImageOps.fit(Image.open(A+"/img/avatar.png").convert("RGBA"),(s,s)); im.paste(av,(x0,y0),hexmask(s))
    d.text((370,20),"NERV",font=font(SER,150),fill=RED)
    d.text((862,58),"GOD'S IN HIS HEAVEN.\nALL'S RIGHT WITH\nTHE WORLD.",font=font(OSW,17,300),fill=DIM,spacing=6)
    d.text((372,190),"EVA-02  //  PRODUCTION MODEL",font=font(OSW,34,500),fill=ORG)
    d.text((372,252),"惣流・アスカ・ラングレー",font=font(JP,36,800),fill=(245,226,214,255))
    d.line([(372,246),(1040,246)],fill=RED,width=3)
    return im
def face(txt,col):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((372,306),"▌ "+txt,font=font(JP,34,700),fill=col); return im
imgs={"no-face-nyarch-logo":base(),
 "nyarch-logo-face-gt-w-lt":face("STANDBY — 待機中",DIM),
 "nyarch-logo-face-OwO":face("SYNCHRONIZING… シンクロ開始",ORG),
 "nyarch-logo-face-caret-w-caret":face("SYNC OK — 起動！",(0,230,118,255)),
 "nyarch-logo-face-gt-dash-lt":face("あんたバカぁ？！ FALSCHES PASSWORT",RED),
 "nyarch-logo-face-UwU":face("SYNC OK",(0,230,118,255))}
tiers={"720p":0.5,"1080p":0.75,"1440p":1.0,"4k":1.5}
for t,k in tiers.items():
    for n,im in imgs.items():
        im.resize((round(W*k),round(H*k)),Image.LANCZOS).save(f"{OUT}/{n}-{t}.png")
    # прогресс-бар и маски: перекрасить градиент в красно-оранжевый
    g=Image.open(f"{SRC}/loading-gradient-{t}.png").convert("RGBA"); a=g.getchannel("A")
    grad=Image.new("RGBA",g.size); gd=ImageDraw.Draw(grad)
    for x in range(g.width):
        u=x/max(1,g.width-1); c=tuple(int(RED[i]+(ORG[i]-RED[i])*u) for i in range(3))
        gd.line([(x,0),(x,g.height)],fill=c+(255,))
    grad.putalpha(a); grad.save(f"{OUT}/loading-gradient-{t}.png")
    for n in ("mask-left","mask-right","password-box"): shutil.copy(f"{SRC}/{n}-{t}.png",OUT)
    for n,col in (("paw-pink",RED),("paw-hotpink",ORG),("paw-lightblue",(86,182,245,255)),("paw-darkblue",(255,176,46,255))):
        p=Image.open(f"{SRC}/{n}-{t}.png").convert("RGBA"); c=Image.new("RGBA",p.size,col); c.putalpha(p.getchannel("A")); c.save(f"{OUT}/{n}-{t}.png")
shutil.copy(f"{SRC}/nyarch-logo.script",f"{OUT}/asuka-nerv.script")
open(f"{OUT}/asuka-nerv.plymouth","w").write("[Plymouth Theme]\nName=asuka-nerv\nDescription=NERV // Asuka boot splash (based on nyarch-logo)\nModuleName=script\n\n[script]\nImageDir=/usr/share/plymouth/themes/asuka-nerv\nScriptFile=/usr/share/plymouth/themes/asuka-nerv/asuka-nerv.script\n")
# проверка: все Image("...") из скрипта существуют
import re
s=open(f"{OUT}/asuka-nerv.script").read()
names=set(re.findall(r'Image\("([a-z0-9-]+)-"\s*\+\s*tier',s))
missing=[f"{n}-{t}.png" for n in names for t in tiers if not os.path.exists(f"{OUT}/{n}-{t}.png")]
print("images referenced:",sorted(names)); print("MISSING:",missing if missing else "none")

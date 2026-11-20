#!/usr/bin/env python3
"""Генератор курсора NERV-Asuka: SVG -> PNG (rsvg-convert) -> xcursor (xcursorgen)."""
import os, subprocess, math, shutil
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.expanduser("~/.local/share/icons/NERV-Asuka")
TMP=os.path.join(HERE,"build"); shutil.rmtree(TMP,ignore_errors=True); os.makedirs(TMP)
SIZES=[24,32,48,64,96]
RED="#c81c26"; ORG="#ff6a13"; BLK="#120406"; GRN="#00e676"; WHT="#fff1e6"
def svg(body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">{body}</svg>'
ARROW_P="M4 2 L4 25 L9.5 19.8 L13.2 28.2 L17 26.6 L13.4 18.4 L21 18.4 Z"
arrow=svg(f'<path d="{ARROW_P}" fill="{RED}" stroke="{BLK}" stroke-width="2.2" stroke-linejoin="round"/>'
          f'<path d="{ARROW_P}" fill="none" stroke="{ORG}" stroke-width="0.9" stroke-linejoin="round"/>'
          f'<path d="M6 8 L6 15 L9 12.4 Z" fill="{GRN}" opacity=".9"/>')
hand=svg(f'<path d="M11 3.5c0-1.4 2.6-1.4 2.6 0V14l.2-2.2c0-1.4 2.5-1.4 2.5 0V14.4l.2-1.6c0-1.4 2.5-1.4 2.5 0v2.6l.2-1c0-1.3 2.3-1.3 2.3 0v6.8c0 4-2.6 7.2-6.7 7.2h-1.6c-2.5 0-4-1-5.3-3L4.3 19c-.8-1.3 1-2.7 2.2-1.6L11 21Z" fill="{RED}" stroke="{BLK}" stroke-width="1.8" stroke-linejoin="round"/>'
         f'<path d="M12.3 4v13" stroke="{ORG}" stroke-width="0.9"/>')
text=svg(f'<path d="M11 4h10M11 28h10M16 4v24" stroke="{BLK}" stroke-width="4" stroke-linecap="round"/><path d="M11 4h10M11 28h10M16 4v24" stroke="{ORG}" stroke-width="2" stroke-linecap="round"/>')
cross=svg(f'<g stroke="{BLK}" stroke-width="3.6"><path d="M16 2v10M16 20v10M2 16h10M20 16h10"/></g><g stroke="{RED}" stroke-width="1.8"><path d="M16 2v10M16 20v10M2 16h10M20 16h10"/></g><circle cx="16" cy="16" r="2" fill="{ORG}" stroke="{BLK}"/>')
def dbl(angle):
    p="M16 2 L22 9 H18.2 V23 H22 L16 30 L10 23 H13.8 V9 H10 Z"
    return svg(f'<g transform="rotate({angle} 16 16)"><path d="{p}" fill="{RED}" stroke="{BLK}" stroke-width="1.8" stroke-linejoin="round"/><path d="M16 6v20" stroke="{ORG}" stroke-width="1"/></g>')
move=svg(''.join(f'<g transform="rotate({a} 16 16)"><path d="M16 2 L21 8 H11 Z" fill="{RED}" stroke="{BLK}" stroke-width="1.6" stroke-linejoin="round"/></g>' for a in (0,90,180,270))+f'<circle cx="16" cy="16" r="3.5" fill="{ORG}" stroke="{BLK}" stroke-width="1.6"/>')
noway=svg(f'<circle cx="16" cy="16" r="11" fill="none" stroke="{BLK}" stroke-width="6"/><circle cx="16" cy="16" r="11" fill="none" stroke="{RED}" stroke-width="3.6"/><path d="M8.2 23.8 23.8 8.2" stroke="{BLK}" stroke-width="6"/><path d="M8.2 23.8 23.8 8.2" stroke="{RED}" stroke-width="3.6"/>')
help_=svg(f'<path d="{ARROW_P}" fill="{RED}" stroke="{BLK}" stroke-width="2.2" stroke-linejoin="round"/><circle cx="24" cy="24" r="7" fill="{ORG}" stroke="{BLK}" stroke-width="1.6"/><text x="24" y="28" font-family="Oswald" font-weight="bold" font-size="11" text-anchor="middle" fill="{BLK}">?</text>')
def hexframe(i,n,small):
    a=360*i/n; pts=" ".join(f"{16+11*math.cos(math.radians(60*k+a)):.2f},{16+11*math.sin(math.radians(60*k+a)):.2f}" for k in range(6))
    inner=" ".join(f"{16+6*math.cos(math.radians(60*k-a*2)):.2f},{16+6*math.sin(math.radians(60*k-a*2)):.2f}" for k in range(6))
    body=f'<polygon points="{pts}" fill="none" stroke="{BLK}" stroke-width="4.4"/><polygon points="{pts}" fill="none" stroke="{RED}" stroke-width="2.4"/><polygon points="{inner}" fill="{ORG}" stroke="{BLK}" stroke-width="1.2"/>'
    if small:  # progress: arrow + small hex
        return svg(f'<path d="{ARROW_P}" fill="{RED}" stroke="{BLK}" stroke-width="2.2" stroke-linejoin="round"/><g transform="translate(14 14) scale(.55)">{body}</g>')
    return svg(body)
# name: (frames, hotspot in 32-grid)
shapes={"default":([arrow],(4,2)),"pointer":([hand],(12,4)),"text":([text],(16,16)),"crosshair":([cross],(16,16)),
 "ns-resize":([dbl(0)],(16,16)),"ew-resize":([dbl(90)],(16,16)),"nesw-resize":([dbl(45)],(16,16)),"nwse-resize":([dbl(-45)],(16,16)),
 "move":([move],(16,16)),"not-allowed":([noway],(16,16)),"help":([help_],(4,2)),
 "wait":([hexframe(i,12,False) for i in range(12)],(16,16)),"progress":([hexframe(i,12,True) for i in range(12)],(4,2))}
aliases={"default":["left_ptr","arrow","top_left_arrow","context-menu","alias","copy","default","center_ptr","right_ptr","vertical-text","cell","dnd-none","dnd-move","dnd-copy","dnd-link","x-cursor","X_cursor","pirate"],
 "pointer":["hand1","hand2","pointing_hand","grab","grabbing","openhand","closedhand","dnd-ask","9d800788f1b08800ae810202380a0822","e29285e634086352946a0e7090d73106","5aca4d189052212118709018842178c0","208530c400c041818281048008011002"],
 "text":["xterm","ibeam","text"],"crosshair":["cross","tcross","crosshair","cross_reverse","diamond_cross","color-picker","zoom-in","zoom-out","target"],
 "ns-resize":["sb_v_double_arrow","n-resize","s-resize","row-resize","size_ver","v_double_arrow","top_side","bottom_side","00008160000006810000408080010102","split_v","double_arrow"],
 "ew-resize":["sb_h_double_arrow","e-resize","w-resize","col-resize","size_hor","h_double_arrow","left_side","right_side","028006030e0e7ebffc7f7070c0600140","split_h"],
 "nesw-resize":["ne-resize","sw-resize","size_bdiag","fd_double_arrow","top_right_corner","bottom_left_corner","fcf1c3c7cd4491d801f1e1c78f100000"],
 "nwse-resize":["nw-resize","se-resize","size_fdiag","bd_double_arrow","top_left_corner","bottom_right_corner","c7088f0f3e6c8088236ef8e1e3e70000"],
 "move":["fleur","all-scroll","size_all","4498f0e0c1937ffe01fd06f973665830","9081237383d90e509aa00f00170e968f"],
 "not-allowed":["crossed_circle","forbidden","no-drop","circle","03b6e0fcb3499374a867c041f52298f0"],
 "help":["question_arrow","whats_this","left_ptr_help","5c6cd98b3f3ebcb1f9c7f1c204630408","d9ce0ab605698f320427677b8d6a4e98"],
 "wait":["watch","clock"],"progress":["left_ptr_watch","half-busy","00000000000000020006000e7e9ffc3f","08e8e1c95fe2fc01f976f1e063a24ccd","3ecb610c1bf2410f44200f48c40d3599"]}
os.makedirs(OUT+"/cursors",exist_ok=True)
for name,(frames,(hx,hy)) in shapes.items():
    cfg=[]
    for fi,s in enumerate(frames):
        sp=f"{TMP}/{name}_{fi}.svg"; open(sp,"w").write(s)
        for sz in SIZES:
            png=f"{TMP}/{name}_{fi}_{sz}.png"
            subprocess.run(["rsvg-convert","-w",str(sz),"-h",str(sz),sp,"-o",png],check=True)
            cfg.append(f"{sz} {round(hx*sz/32)} {round(hy*sz/32)} {png}"+(" 50" if len(frames)>1 else ""))
    cp=f"{TMP}/{name}.cfg"; open(cp,"w").write("\n".join(cfg)+"\n")
    subprocess.run(["xcursorgen",cp,f"{OUT}/cursors/{name}"],check=True)
    for al in aliases.get(name,[]):
        if al==name: continue
        d=f"{OUT}/cursors/{al}"
        if os.path.lexists(d): os.remove(d)
        os.symlink(name,d)
open(OUT+"/index.theme","w").write("[Icon Theme]\nName=NERV-Asuka\nComment=Eva-02 red cursor // NERV\nInherits=breeze_cursors\n")
open(OUT+"/cursor.theme","w").write("[Icon Theme]\nInherits=NERV-Asuka\n")
subprocess.run(["rsvg-convert","-w","256",f"{TMP}/default_0.svg","-o",f"{HERE}/preview_default.png"])
print("ok", len(os.listdir(OUT+"/cursors")), "cursors")

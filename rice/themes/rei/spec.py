#!/usr/bin/env python3
"""Rei // 1995 — Аянами Рей в стиле аниме 90-х: VHS-кассета, ЭЛТ-сканлайны, ледяной голубой и красный."""
import os, sys, math, random, shutil
import numpy as np
sys.path.insert(0, os.path.expanduser("~/.local/share/rice/build"))
from lib import *

D = os.path.dirname(os.path.abspath(__file__)); SRC = D + "/src"
FR = HOME + "/.local/share/fonts/rice"; FN = HOME + "/.local/share/fonts/nerv"
VT = FR + "/VT323-Regular.ttf"; DOT = FR + "/DotGothic16-Regular.ttf"
SHIP = FN + "/ShipporiMinchoB1-ExtraBold.ttf"; OSW = FN + "/Oswald[wght].ttf"

ICE, RED, CREAM, NAVY = "#9cc8ff", "#e03a3e", "#f2ead8", "#0a1018"
S = {
    "id": "rei", "dir": D, "name": "Rei // 1995",
    "desc": "Аянами Рей в духе аниме 90-х: VHS-кассета, ЭЛТ-сканлайны, ледяной голубой и красный, логи «с плёнки».",
    "pal": {"bg": NAVY, "bg2": "#0f1824", "surface": "#1a2635", "fg": "#e8f0f8", "dim": "#6f8296",
            "accent": ICE, "accent2": RED, "neg": "#ff4d4d", "pos": "#7fe0a8", "neu": "#f0c060",
            "link": ICE, "visited": "#c49cff", "sel_fg": "#08101a", "term_bg": "#070c12"},
    "ansi": ["#16202c", "#e03a3e", "#7fe0a8", "#f0c060", "#6fa8ff", "#c49cff", "#7fd6e0", "#d8e2ec",
             "#3a4a5c", "#ff6b6b", "#a8f0c4", "#ffd88a", "#9cc8ff", "#dcbcff", "#a8eef4", "#ffffff"],
    "fonts": {"title": (SHIP, None), "ui": (OSW, 400), "ui_bold": (OSW, 600), "jp": (DOT, None)},
    "kde_colors": "Rei1995", "konsole_scheme": "Rei1995", "konsole_profile": "Rei 1995",
    "term_font": "VT323,16,-1,5,400,0,0,0,0,0,0,0,0,0,0,1", "cursor_shape": 0, "term_opacity": 0.95,
    "cursor": "Rei-1995", "sounds": "rei-1995",
    "prompt": {"line1": [("▌00 ", RED, True), ("{USER}", ICE, False), ("@", "#6f8296", False), ("UNIT-00 ", ICE, False),
                         (":: ", "#6f8296", False), ("{WD} ", "#e8f0f8", False), ("[", "#6f8296", False)],
               "arrow": [("▶", RED, True), ("▶", ICE, False)], "tail": ("]", "#6f8296")},
    "prompt_status": (("…", "#7fe0a8"), ("わからない", "#ff4d4d")),
    "fastfetch": {"key_color": "94", "title_color": "91",
                  "header": ["{#1;91}▌綾波レイ{#0;94}  FIRST CHILD // UNIT-00 {#90}[TAPE 01 · SEP 1995]",
                             "{#34}─────────────────────────────────────────",
                             "{#94}PILOT     {#97}綾波レイ  {#90}(Ayanami Rei)",
                             "{#94}UNIT      {#97}EVA-00 {#90}// Prototype"],
                  "keys": [("title", "OPERATOR "), ("os", "OS       "), ("kernel", "KERNEL   "), ("packages", "PACKAGES "),
                           ("shell", "SHELL    "), ("terminal", "TERMINAL "), ("wm", "WM       "), ("cpu", "UNIT-00  "),
                           ("gpu", "AT FIELD "), ("memory", "LCL      "), ("uptime", "TAPE     ")]},
    "splash": {"id": "rei.1995", "title": "綾波レイ", "title_font": "Shippori Mincho B1", "font": "VT323",
               "subtitle": "PLAY ▶  TAPE 01 — SEP. 1995", "radius": 0,
               "messages": ["TRACKING...", "UNIT-00: REACTIVATION TEST", "SYNCHRO START", "A10 NERVE: CONNECTED",
                            "私は、あなたを守るもの", "PLAY ▶"]},
    "plymouth": {"name": "rei-log", "title": "零号機", "head1": "AYANAMI REI // FIRST CHILD", "head2": "TAPE 01 - SEP. 1995 - SP - HI-FI STEREO",
                 "tab": "VHS BOOT LOG", "tab_right": "PLAY  >  CH 03", "bar": "SYNC", "radius": 0, "seg_radius": 0,
                 "footer": "I am not a doll.", "font_family": "Oswald", "mono_family": "VT323", "fsize_div": 48,
                 "names": ["UNIT-00", "LCL", "AT-FLD"], "tags": {"ok": "[ PLAY ]", "amb": "[ NERV ]", "warn": "[ ERR  ]"},
                 "c_ok": "#7fe0a8", "c_amb": ICE, "c_name": RED, "c_text": CREAM, "seg": (RED, ICE, "#7fe0a8"),
                 "stop": "STOP / EJECT ... sayonara",
                 "sub": {"boot": ("▌ 再生 — PLAY TAPE 01", CREAM), "shutdown": ("▌ 停止 — STOP / EJECT", RED),
                         "reboot": ("▌ 巻き戻し — REWIND", ICE)},
                 "ask": "パスワードを。…命令なら、そうする",
                 "ambient": ["TRACKING ..... auto", "Pilot: Ayanami Rei // First Child", "Unit-00 ..... reactivation test",
                             "Synchro ratio ..... stable", "Positron rifle ..... charging", "Shield ..... ready",
                             "Room 402 ..... quiet", "Moon ..... visible", "Tape counter ..... 00:19:95",
                             "Commander Ikari ..... watching", "Pattern blue ..... negative", "I don't know what to say..."]},
    "grub": {"name": "Rei-1995", "title": "REI // 1995", "item": "#9cc8ff", "item_sel": "#ffffff", "radius": 0,
             "fonts": {"title": SHIP, "ui": VT, "menu": VT},
             "labels": [{"left": "8%+6", "top": "8%+122", "color": RED, "text": "UNIT-00 // FIRST CHILD // SELECT TAPE"},
                        {"left": "8%+6", "top": "8%+152", "color": "#6f8296", "text": "PLAY  >  TAPE 01  -  SEP. 1995  -  SP"},
                        {"left": "8%", "top": "100%-136", "color": ICE, "text": " UP/DOWN - SELECT TAPE", "font": "menu"},
                        {"left": "8%", "top": "100%-110", "color": ICE, "text": " ENTER - PLAY", "font": "menu"},
                        {"left": "8%", "top": "100%-84", "color": "#6f8296", "text": " E - EDIT  //  C - CONSOLE"}]},
    "refind": {"name": "rei-1995", "font": VT, "shape": "square"},
    "sddm": {"name": "rei-1995", "font": "Oswald", "position": "left",
             "message": "FIRST CHILD AUTHENTICATION // 綾波レイ // …命令なら、そうする", "spinner": "SYNCHRONIZING... PLAY ▶"},
}
P = S["pal"]
for d_ in ("out", "system", "build-tmp", "wallpapers"): mkdir(T(S, d_))
random.seed(1995)

face = Image.open(SRC + "/wallhaven-gpdm3e.png").convert("RGBA")
glitch = Image.open(SRC + "/wallhaven-x1ppyv.jpg").convert("RGBA")
poster = Image.open(SRC + "/wallhaven-ogdzd5.png").convert("RGBA")
city = Image.open(SRC + "/wallhaven-pk98lm.jpg").convert("RGBA")
moon = Image.open(SRC + "/wallhaven-8xk6oo.png").convert("RGBA")
pix = Image.open(SRC + "/wallhaven-1jgvwv.jpg").convert("RGBA")


# ── ЭЛТ/VHS-обработка ────────────────────────────────────────────────────────
def scanlines(size, step=4, a=70):
    lay = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for y in range(0, size[1], step): d.line([(0, y), (size[0], y)], fill=(0, 0, 0, a))
    return lay

def crt(im, shift=4, lines=True, vignette=.55):
    r, g, b, a = im.split()
    r = ImageChops.offset(r, shift, 0); b = ImageChops.offset(b, -shift, 0)
    im = Image.merge("RGBA", (r, g, b, a))
    if lines: im.alpha_composite(scanlines(im.size))
    if vignette:
        w, h = im.size; v = Image.new("L", (w // 8, h // 8), 0); vd = ImageDraw.Draw(v)
        for k in range(30):
            q = k / 30; vd.ellipse([-w // 8 * .25 * (1 - q), -h // 8 * .25 * (1 - q), w // 8 * (1 + .25 * (1 - q)), h // 8 * (1 + .25 * (1 - q))],
                                  fill=int(255 * q))
        v = v.resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(40))
        dark = Image.new("RGBA", (w, h), (4, 8, 14, 255)); im = Image.composite(im, dark, v.point(lambda x: int(255 - (255 - x) * vignette)))
    return im
from PIL import ImageChops

def osd(d, size, counter):
    w, h = size; f = font(VT, round(h * .05)); m = round(h * .045)
    d.text((m * 1.6, m), "PLAY", font=f, fill=(242, 234, 216, 235))
    x = m * 1.6 + d.textlength("PLAY ", font=f); y = m + h * .012; s_ = h * .03
    d.polygon([(x, y), (x, y + s_), (x + s_ * .9, y + s_ / 2)], fill=(242, 234, 216, 235))
    d.text((w - m * 1.6 - d.textlength("SP", font=f), m), "SP", font=f, fill=(242, 234, 216, 235))
    d.text((m * 1.6, h - m - h * .06), "SEP. 13 1995", font=f, fill=(242, 234, 216, 220))
    d.text((w - m * 1.6 - d.textlength(counter, font=f), h - m - h * .06), counter, font=f, fill=(242, 234, 216, 220))

# ── обои: главный монитор — живая «кассета» ──────────────────────────────────
WP = T(S, "wallpapers")
base = ImageOps.fit(face, (W, H), Image.LANCZOS)
base = ImageEnhance.Color(base).enhance(1.12)
base = crt(base, shift=5)
rng = np.random.default_rng(95)
def vhs(fr, t, i):
    a = np.asarray(fr.convert("RGB")).astype(np.int16)
    # полоса трекинга, проползающая сверху вниз
    y0 = int(((t * 1.0) % 1) * (H + 160)) - 80; hgt = 70
    for y in range(max(0, y0), min(H, y0 + hgt)):
        a[y] = np.roll(a[y], int(rng.integers(-28, 28)), axis=0); a[y] += 18
    # редкие «срывы» строк
    for _ in range(3):
        y = int(rng.integers(0, H - 3)); a[y:y + 2] = np.roll(a[y:y + 2], int(rng.integers(-60, 60)), axis=1)
    a += rng.integers(-9, 10, size=a.shape, dtype=np.int16)          # зерно
    a = (a * (1 + 0.025 * math.sin(2 * math.pi * t * 6))).astype(np.int16)  # мерцание
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    secs = 19 * 60 + 95 % 60 + int(t * 12); osd(ImageDraw.Draw(im), (W, H), f"0:{secs // 60:02d}:{secs % 60:02d}")
    return im
main_mp4, splash_gif = live_wallpaper(S, base, WP + "/main-live.mp4", lambda d, t, l: None, seconds=12, fps=24,
                                      poster=WP + "/main-poster.jpg", post=vhs, crf=24)

side = crt(ImageOps.fit(glitch, (1920, 1080), Image.LANCZOS), shift=3)
side.convert("RGB").save(WP + "/side-1080p.png")
lock = crt(ImageOps.fit(city, (W, H), Image.LANCZOS, centering=(0.62, 0.5)), shift=3)
od = ImageDraw.Draw(lock); osd(od, (W, H), "0:00:00"); lock.convert("RGB").save(WP + "/lock.png")

# ── аватар, лого, кнопка меню ────────────────────────────────────────────────
AVB = (690, 150, 1230, 690)
av = face.crop(AVB).resize((512, 512), Image.LANCZOS); av.convert("RGB").save(T(S, "system", "avatar.png"))
lg = crt(av.copy(), shift=3, vignette=0); fr_ = Image.new("RGBA", (540, 540), rgba(RED)); fr_.alpha_composite(lg, (14, 14))
fastfetch(S, fr_.resize((256, 256), Image.LANCZOS))
def kick(s):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.rectangle([0, 0, s - 1, s - 1], fill=rgba(NAVY), outline=rgba(ICE), width=s // 14)
    f = font(SHIP, round(s * .62)); tw = dd.textlength("零", font=f)
    dd.text(((s - tw) / 2, s * .08), "零", font=f, fill=rgba(RED)); return im
ss(kick, 256).save(T(S, "kickoff.png"))

kde_colors(S); terminal(S); prompts(S)

# ── курсор: пиксельная стрелка 90-х, ожидание — вращающееся «AT-поле» ───────
OUTL, FILL, HL = "#08101a", ICE, "#ffffff"
def svg(b): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" shape-rendering="crispEdges">{b}</svg>'
AR = "M4 2 V24 H6 V22 H8 V20 H10 V24 H12 V28 H16 V24 H14 V20 H19 V18 H17 V16 H15 V14 H13 V12 H11 V10 H9 V8 H7 V6 H6 V4 H5 V2 Z"
AR2 = "M4 2 L4 24 L9 19 L12.5 27 L15.5 25.8 L12.2 18 L19 18 Z"
arrow = svg(f'<path d="{AR2}" fill="{FILL}" stroke="{OUTL}" stroke-width="2.2" stroke-linejoin="miter"/><path d="M6 7 V16" stroke="{HL}" stroke-width="1.4"/>')
hand = svg(f'<path d="M11 3.5c0-1.4 2.6-1.4 2.6 0V14l.2-2.2c0-1.4 2.5-1.4 2.5 0V14.4l.2-1.6c0-1.4 2.5-1.4 2.5 0v2.6l.2-1c0-1.3 2.3-1.3 2.3 0v6.8c0 4-2.6 7.2-6.7 7.2h-1.6c-2.5 0-4-1-5.3-3L4.3 19c-.8-1.3 1-2.7 2.2-1.6L11 21Z" fill="{FILL}" stroke="{OUTL}" stroke-width="1.8" stroke-linejoin="round"/><path d="M12.3 4v13" stroke="{HL}" stroke-width=".9"/>')
text = svg(f'<path d="M11 4h10M11 28h10M16 4v24" stroke="{OUTL}" stroke-width="4"/><path d="M11 4h10M11 28h10M16 4v24" stroke="{ICE}" stroke-width="2"/>')
cross = svg(f'<g stroke="{OUTL}" stroke-width="3.6"><path d="M16 2v10M16 20v10M2 16h10M20 16h10"/></g><g stroke="{RED}" stroke-width="1.8"><path d="M16 2v10M16 20v10M2 16h10M20 16h10"/></g>')
def dbl(a):
    p = "M16 2 L22 9 H18.2 V23 H22 L16 30 L10 23 H13.8 V9 H10 Z"
    return svg(f'<g transform="rotate({a} 16 16)"><path d="{p}" fill="{ICE}" stroke="{OUTL}" stroke-width="1.8"/></g>')
move = svg(''.join(f'<g transform="rotate({a} 16 16)"><path d="M16 2 L21 8 H11 Z" fill="{ICE}" stroke="{OUTL}" stroke-width="1.6"/></g>' for a in (0, 90, 180, 270)) + f'<rect x="13" y="13" width="6" height="6" fill="{RED}" stroke="{OUTL}"/>')
noway = svg(f'<circle cx="16" cy="16" r="11" fill="none" stroke="{OUTL}" stroke-width="6"/><circle cx="16" cy="16" r="11" fill="none" stroke="{RED}" stroke-width="3.6"/><path d="M8.2 23.8 23.8 8.2" stroke="{OUTL}" stroke-width="6"/><path d="M8.2 23.8 23.8 8.2" stroke="{RED}" stroke-width="3.6"/>')
help_ = svg(f'<path d="{AR2}" fill="{FILL}" stroke="{OUTL}" stroke-width="2.2"/><rect x="18" y="18" width="12" height="12" fill="{RED}" stroke="{OUTL}" stroke-width="1.4"/><text x="24" y="28" font-family="VT323" font-size="13" text-anchor="middle" fill="#fff">?</text>')
def atf(i, n, small):
    a = 360 * i / n; body = ""
    for k, (r, col) in enumerate(((11, "#f0a040"), (7.5, "#f0c060"), (4, RED))):
        pts = " ".join(f"{16 + r * math.cos(math.radians(45 * j + a * (1 if k % 2 == 0 else -1) + 22.5)):.2f},"
                       f"{16 + r * math.sin(math.radians(45 * j + a * (1 if k % 2 == 0 else -1) + 22.5)):.2f}" for j in range(8))
        body += f'<polygon points="{pts}" fill="none" stroke="{OUTL}" stroke-width="3"/><polygon points="{pts}" fill="none" stroke="{col}" stroke-width="1.4"/>'
    if small: return svg(f'<path d="{AR2}" fill="{FILL}" stroke="{OUTL}" stroke-width="2.2"/><g transform="translate(13 13) scale(.6)">{body}</g>')
    return svg(body)
cursor(S, {"default": ([arrow], (4, 2)), "pointer": ([hand], (12, 4)), "text": ([text], (16, 16)), "crosshair": ([cross], (16, 16)),
           "ns-resize": ([dbl(0)], (16, 16)), "ew-resize": ([dbl(90)], (16, 16)), "nesw-resize": ([dbl(45)], (16, 16)),
           "nwse-resize": ([dbl(-45)], (16, 16)), "move": ([move], (16, 16)), "not-allowed": ([noway], (16, 16)),
           "help": ([help_], (4, 2)), "wait": ([atf(i, 12, False) for i in range(12)], (16, 16)),
           "progress": ([atf(i, 12, True) for i in range(12)], (4, 2))})

# ── звуки: чиптюн-писки 90-х ─────────────────────────────────────────────────
A4, C5, E5, G5, A5, C6, E6 = 440, 523.3, 659.3, 784.0, 880.0, 1046.5, 1318.5
pip = [(1000, .06, "square", .5, None)]
sounds(S, {
    "desktop-login": [(A4, .12, "square", .5, None), (C5, .12, "square", .5, None), (E5, .12, "square", .5, None),
                      (A5, .12, "square", .5, None), (E6, .45, "tri", .7, None)],
    "message-new-instant": [(E6, .07, "square", .45, None), (0, .04, "rest", 0, None), (E6, .1, "square", .45, None)],
    "message": pip, "message-new-email": pip, "message-attention": [(A5, .08, "square", .5, None), (E6, .12, "square", .5, None)],
    "dialog-information": [(C6, .08, "tri", .6, None), (G5, .2, "tri", .6, None)],
    "dialog-question": [(G5, .1, "tri", .6, None), (C6, .2, "tri", .6, None)],
    "dialog-warning": [(A5, .12, "square", .5, None), (A5, .12, "square", .5, None)],
    "dialog-warning-auth": [(A5, .12, "square", .5, None), (A5, .12, "square", .5, None)],
    "dialog-error": [(300, .3, "square", .55, 150)], "dialog-error-critical": [(300, .2, "square", .55, None), (200, .4, "square", .55, 120)],
    "outcome-success": [(C6, .08, "square", .5, None), (E6, .25, "square", .5, None)],
    "outcome-failure": [(E5, .12, "square", .5, None), (C5, .3, "square", .5, None)],
    "complete": [(G5, .08, "tri", .6, None), (C6, .25, "tri", .6, None)],
    "audio-volume-change": [(1200, .04, "square", .4, None)], "bell": [(2000, .08, "square", .4, None)],
    "bell-window-system": [(2000, .08, "square", .4, None)],
    "device-added": [(G5, .08, "square", .5, None), (C6, .15, "square", .5, None)],
    "device-removed": [(C6, .08, "square", .5, None), (G5, .15, "square", .5, None)],
    "power-plug": [(C5, .1, "tri", .6, None), (G5, .2, "tri", .6, None)],
    "power-unplug": [(G5, .1, "tri", .6, None), (C5, .2, "tri", .6, None)],
    "battery-low": [(A4, .2, "square", .5, None)], "battery-caution": [(A4, .3, "square", .5, 300)],
    "trash-empty": [(3000, .3, "square", .25, 200)],
})

splash(S, splash_gif)

# ── Plymouth: постер Рей справа, логи кассеты слева ──────────────────────────
pb = Image.new("RGBA", (W, H), (0, 0, 0, 255))
pst = ImageOps.fit(poster, (W, H), Image.LANCZOS)
pb.alpha_composite(pst.transform((W, H), Image.AFFINE, (1, 0, -0.30 * W, 0, 1, 0), fillcolor=(0, 0, 0, 255)))
pb = crt(pb, shift=3, vignette=0)
plymouth_log(S, pb)

# ── GRUB: силуэт на фоне луны, меню слева ────────────────────────────────────
gb = crt(ImageOps.fit(moon, (W, H), Image.LANCZOS), shift=2, vignette=.3)
grub(S, gb)

# ── rEFInd: пиксель-арт, тёмный ──────────────────────────────────────────────
rb = ImageEnhance.Brightness(ImageOps.fit(pix, (W, H), Image.NEAREST)).enhance(.55)
rb = crt(rb, shift=2, vignette=.5); rd = ImageDraw.Draw(rb)
rd.text((140, 150), "REI // 1995", font=font(SHIP, 120), fill=rgba(ICE))
rd.text((146, 310), "SELECT TAPE  —  テープを選んでください", font=font(DOT, 44), fill=rgba(RED))
rd.text((146, H - 140), "LEFT / RIGHT  SELECT     ENTER  PLAY     F2  OPTIONS", font=font(VT, 40), fill=rgba(ICE))
osd(rd, (W, H), "0:00:00")
refind(S, rb, {"os_main": (face.crop(AVB), "LINUX", ICE, False),
               "os_fallback": (face.crop(AVB), "FALLBACK", "#6f8296", True),
               "os_grub": (moon.crop((900, 0, 1980, 1080)), "GRUB", RED, False),
               "os_unknown": (None, "???", ICE, False)})

# ── SDDM: Рей у окна ─────────────────────────────────────────────────────────
sddm(S, WP + "/lock.png", WP + "/lock.png")

# ── клавиатура: голубая с красными «глазами» и полосой 00 ────────────────────
rgb_art(S, {"B": (40, 120, 255), "I": (120, 190, 255), "R": (255, 0, 10), "W": (200, 220, 255), "K": (0, 0, 20)},
        ["I" * 23, "B" * 6 + "R" * 2 + "B" * 7 + "R" * 2 + "B" * 6, "B" * 23, "W" * 23, "B" * 23, "I" * 23])

pv = Image.open(WP + "/main-poster.jpg").convert("RGBA").resize((960, 540), Image.LANCZOS); pd = ImageDraw.Draw(pv)
pd.rectangle([24, 400, 600, 516], fill=(7, 12, 18, 220))
pd.text((44, 404), S["name"], font=font(SHIP, 46), fill=rgba(ICE))
pd.text((46, 466), "VHS · CRT · Unit-00 · ice blue & red", font=font(VT, 30), fill=rgba(RED))
pv.convert("RGB").save(T(S, "preview.png"))

manifest(S, wallpapers={"main": {"type": "video", "path": WP + "/main-live.mp4", "poster": WP + "/main-poster.jpg"},
                        "side": {"type": "image", "path": WP + "/side-1080p.png"}},
         lockscreen={"type": "image", "path": WP + "/lock.png"},
         kickoff_icon=T(S, "kickoff.png"))
shutil.rmtree(T(S, "build-tmp", "frames"), ignore_errors=True)
print("rei: ok")

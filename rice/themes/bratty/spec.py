#!/usr/bin/env python3
"""Femboy Paws // Bratty — дерзкая неоновая версия: чокеры, гольфы, сарказм и сердечки."""
import os, sys, math, random, shutil
sys.path.insert(0, os.path.expanduser("~/.local/share/rice/build"))
from lib import *

D = os.path.dirname(os.path.abspath(__file__)); SRC = D + "/src"
FR = HOME + "/.local/share/fonts/rice"
FRED = FR + "/Fredoka[wdth,wght].ttf"; MPR = FR + "/MPLUSRounded1c-ExtraBold.ttf"; MPRB = FR + "/MPLUSRounded1c-Bold.ttf"
JBM = "/usr/share/fonts/TTF/JetBrainsMonoNerdFontMono-Regular.ttf"

PINK, HOT, LAV, BLUE, WHITE = "#ff3fa4", "#ff1f8f", "#b45cff", "#6fe3ff", "#ffeef8"
S = {
    "id": "bratty", "dir": D, "name": "Femboy Paws // Bratty",
    "desc": "Дерзкая неоновая версия: чокеры, гольфы, сарказм и сердечки. Требует headpats для загрузки.",
    "pal": {"bg": "#0d0612", "bg2": "#150a1c", "surface": "#26112f", "fg": WHITE, "dim": "#8d7d9e",
            "accent": PINK, "accent2": BLUE, "neg": "#ff5577", "pos": "#7dffb2", "neu": "#ffd27a",
            "link": BLUE, "visited": LAV, "sel_fg": "#1a0f1f", "term_bg": "#0d0912"},
    "ansi": ["#2a1d33", "#ff5c8a", "#7dffb2", "#ffd27a", "#7fd4ff", "#ff7ac6", "#8ff0e6", "#e6d8f0",
             "#5a4868", "#ff86a8", "#a6ffcb", "#ffe1a3", "#a8e3ff", "#ffa3d9", "#b5fff4", "#ffffff"],
    "fonts": {"title": (FRED, [700, 100]), "ui": (FRED, [400, 100]), "ui_bold": (FRED, [600, 100]), "jp": (MPR, None)},
    "kde_colors": "FemboyBratty", "konsole_scheme": "FemboyBratty", "konsole_profile": "Femboy Bratty",
    "term_opacity": 0.9, "cursor": "Femboy-Bratty", "sounds": "femboy-bratty",
    "prompt": {"line1": [("\uf1b0 ", PINK, True), ("{USER}", BLUE, False), ("@", "#8d7d9e", False), ("brat ", LAV, False),
                         (":: ", "#8d7d9e", False), ("{WD} ", WHITE, False), ("[", "#8d7d9e", False)],
               "arrow": [("❯", PINK, True), ("❯", LAV, False), ("❯", BLUE, False)], "tail": ("]", "#8d7d9e")},
    "prompt_status": (("good boy~", "#7dffb2"), ("hmph! baka", "#ff5577")),
    "fastfetch": {"key_color": "95", "title_color": "94",
                  "header": ["{#1;95}\uf1b0  {#0;94}femboy paws {#90}// {#95}bratty mode",
                             "{#35}─────────────────────────────────────────",
                             "{#95}MOOD      {#97}bratty  {#90}// headpats required",
                             "{#95}OUTFIT    {#97}choker · thigh-highs · oversized hoodie"],
                  "keys": [("title", "USER     "), ("os", "OS       "), ("kernel", "KERNEL   "), ("packages", "PACKAGES "),
                           ("shell", "SHELL    "), ("terminal", "TERMINAL "), ("wm", "WM       "), ("cpu", "BRAIN    "), ("gpu", "SPARKLE  "), ("memory", "ATTENTION"), ("uptime", "BEING CUTE")]},
    "splash": {"id": "femboy.bratty", "title": "brat mode ♡", "title_font": "Fredoka", "font": "Fredoka",
               "subtitle": "ugh, fine, I'm booting... happy now? ♡", "radius": 24,
               "messages": ["clicking on the choker~", "pulling up thigh-highs", "fixing eyeliner", "pretending not to care",
                            "waiting for headpats...", "fine. you may come in ♡"]},
    "plymouth": {"name": "bratty-log", "title": "brat mode", "head1": "BRATTY BOOT TERMINAL", "head2": "headpats: required // attitude: maximum",
                 "tab": "boot.log", "tab_right": "choker · socks · sass", "bar": "BRAT", "radius": 18, "seg_radius": 6,
                 "footer": "make me boot faster. I dare you.", "font_family": "Fredoka", "mono_family": "JetBrainsMono Nerd Font Mono",
                 "names": ["CHOKER-1", "SOCKS-2", "SASS-3"], "tags": {"ok": "[ ok~ ]", "amb": "[hmph!]", "warn": "[ >:c ]"},
                 "c_ok": "#7dffb2", "c_amb": PINK, "c_name": LAV, "c_text": "#ffd8ee", "seg": (LAV, PINK, "#7dffb2"),
                 "stop": "leaving already? hmph. fine. bye~",
                 "sub": {"boot": ("▌ ふん！ — FINE, I'LL BOOT. FOR YOU.", WHITE), "shutdown": ("▌ もう行くの？ — LEAVING ALREADY?", PINK),
                         "reboot": ("▌ また？ — AGAIN?! UGH~ ♡", BLUE)},
                 "ask": "パスワード… ちゃんと言って？♡",
                 "ambient": ["choker ..... clicked on", "thigh-highs.service ..... equipped", "mood ..... bratty",
                             "eyeliner ..... sharp enough to kill", "headpats ..... required to continue",
                             "you're staring again ..... noted", "compliments ..... accepted, more pls",
                             "tail ..... flicking impatiently", "skirt twirl ..... calibrated", "waiting for you to say please~",
                             "bratty.service ..... cannot be stopped", "attitude ..... 420%"]},
    "grub": {"name": "Femboy-Bratty", "title": "brat mode ♡", "item": "#ffb3dd", "item_sel": "#ffffff", "radius": 0,
             "fonts": {"title": MPR, "ui": MPRB, "menu": MPRB},
             "labels": [{"left": "8%+6", "top": "8%+122", "color": BLUE, "text": "pick one. quickly. I don't have all day~ ♡"},
                        {"left": "8%+6", "top": "8%+156", "color": "#8d7d9e", "text": "be nice to me or I won't boot"},
                        {"left": "8%", "top": "100%-136", "color": PINK, "text": "  UP/DOWN - choose", "font": "menu"},
                        {"left": "8%", "top": "100%-110", "color": PINK, "text": "  ENTER - pretty please?", "font": "menu"},
                        {"left": "8%", "top": "100%-84", "color": "#8d7d9e", "text": "  E - edit  //  C - console"}]},
    "refind": {"name": "femboy-bratty", "font": JBM, "shape": "circle"},
    "sddm": {"name": "femboy-bratty", "font": "Fredoka", "position": "left",
             "message": "say the password nicely~ ♡  (I'm watching)", "spinner": "hmph... fine, come in~"},
}
P = S["pal"]
for d_ in ("out", "system", "build-tmp", "wallpapers"): mkdir(T(S, d_))
random.seed(7)

# ── исходники ────────────────────────────────────────────────────────────────
def letterbox_crop(im):
    g = im.convert("L").resize((64, im.height // 8)); rows = [sum(g.crop((0, y, 64, y + 1)).tobytes()) / 64 for y in range(g.height)]
    top = next(y for y, v in enumerate(rows) if v > 22); bot = g.height - next(y for y, v in enumerate(reversed(rows)) if v > 22)
    return im.crop((0, (top + 2) * 8, im.width, (bot - 2) * 8))

fluff = letterbox_crop(Image.open(SRC + "/wallhaven-vpzld3.jpg").convert("RGBA"))
boy = Image.open(SRC + "/wallhaven-kxmrxm.png").convert("RGBA")
room = Image.open(SRC + "/wallhaven-l3wx2p.png").convert("RGBA")
brat = Image.open(SRC + "/wallhaven-qrppoq.png").convert("RGBA")
def darken_white(im, bg):
    """белый фон → тёмный градиент темы (персонаж остаётся)"""
    import numpy as np
    a = np.asarray(im.convert("RGB")).astype(np.int16); mx, mn = a.max(2), a.min(2)
    m = ((mn > 232) & (mx - mn < 18)).astype(np.uint8) * 255
    mask = Image.fromarray(m).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(2))
    g = Image.new("RGBA", im.size); gd = ImageDraw.Draw(g)
    for y in range(im.height):
        gd.line([(0, y), (im.width, y)], fill=rgba(mix(bg, "#3a0c3a", y / im.height)))
    return Image.composite(g, im.convert("RGBA"), mask)
astolfo = darken_white(Image.open(SRC + "/wallhaven-dg58wj.png").convert("RGBA"), "#0d0612")

def paw_field(size, n, cols, alpha=(30, 90), rmin=10, rmax=26, region=(0, 0, 1, 1), seed=1):
    rnd = random.Random(seed); lay = Image.new("RGBA", size, (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
    for _ in range(n):
        x = rnd.uniform(region[0], region[2]) * size[0]; y = rnd.uniform(region[1], region[3]) * size[1]
        paw(dd, x, y, rnd.uniform(rmin, rmax), rgba(rnd.choice(cols), rnd.randint(*alpha)))
    return lay.rotate(0)

# ── обои ─────────────────────────────────────────────────────────────────────
WP = T(S, "wallpapers")
main = ImageOps.fit(astolfo, (W, H), Image.LANCZOS)
side = ImageOps.fit(fluff, (1920, 1080), Image.LANCZOS, centering=(0.5, 0.45))
side.convert("RGB").save(WP + "/side-1080p.png")
main.convert("RGB").save(WP + "/main-1440p.png")

# частицы: лапки и искорки, всплывающие по кругу (бесшовно: позиция зависит от t по модулю 1)
def heart(dd, cx, cy, r, fill):
    dd.ellipse([cx - r, cy - r * .7, cx, cy + r * .3], fill=fill); dd.ellipse([cx, cy - r * .7, cx + r, cy + r * .3], fill=fill)
    dd.polygon([(cx - r * .97, cy - r * .05), (cx + r * .97, cy - r * .05), (cx, cy + r * 1.1)], fill=fill)
PRT = [(random.random(), random.random(), random.uniform(9, 22), random.choice([PINK, LAV, BLUE, WHITE]),
        random.uniform(.6, 1.4), random.random()) for _ in range(46)]
def particles(dd, t, lay):
    for (x0, y0, r, col, spd, ph) in PRT:
        k = (t * round(spd) + ph) % 1 if round(spd) else (t + ph) % 1
        y = (y0 - k) % 1; x = x0 + 0.012 * math.sin(2 * math.pi * (t * 2 + ph))
        a = max(0, min(150, int(150 * (0.5 + 0.5 * math.sin(2 * math.pi * (t + ph))))))
        if int(ph * 10) % 2: heart(dd, x * W, y * H, r * 1.2, rgba(col, a))
        else: paw(dd, x * W, y * H, r, rgba(col, a))

main_mp4, splash_gif = live_wallpaper(S, main, WP + "/main-live.mp4", particles, seconds=12, fps=24,
                                      glow=(HOT, 0.06), poster=WP + "/main-poster.jpg")

# ── аватар / лого / иконка меню ──────────────────────────────────────────────
AVB = (520, 160, 1360, 1000)
av = astolfo.crop(AVB).resize((512, 512), Image.LANCZOS)
av.convert("RGB").save(T(S, "system", "avatar.png"))
logo = av.copy(); m = Image.new("L", logo.size, 0); ImageDraw.Draw(m).ellipse([0, 0, 511, 511], fill=255); logo.putalpha(m)
ring = Image.new("RGBA", (540, 540), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse([0, 0, 539, 539], fill=rgba(PINK))
ring.alpha_composite(logo, (14, 14)); fastfetch(S, ring.resize((256, 256), Image.LANCZOS))
def kick(s):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.ellipse([0, 0, s - 1, s - 1], fill=rgba(P["bg"])); dd.ellipse([0, 0, s - 1, s - 1], outline=rgba(PINK), width=s // 14)
    paw(dd, s / 2, s * .58, s * .17, rgba(PINK)); return im
ss(kick, 256).save(T(S, "kickoff.png"))

# ── цвета, терминал, приглашения ─────────────────────────────────────────────
kde_colors(S); terminal(S); prompts(S)

# ── курсор: розовая стрелка, лапка-указатель, кружащиеся лапки ────────────────
OUT_C, IN_C, DARK = "#ffffff", PINK, "#2a1030"
def svg(b): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">{b}</svg>'
AR = "M4 2 L4 25 L9.5 19.8 L13.2 28.2 L17 26.6 L13.4 18.4 L21 18.4 Z"
def pawsvg(cx, cy, r, fill, stroke=DARK, sw=1.2):
    s_ = f'<ellipse cx="{cx}" cy="{cy + r * .2}" rx="{r}" ry="{r * .75}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    for dx, dy in ((-1.05, -1.0), (-.38, -1.55), (.38, -1.55), (1.05, -1.0)):
        s_ += f'<ellipse cx="{cx + dx * r:.2f}" cy="{cy + dy * r:.2f}" rx="{r * .36:.2f}" ry="{r * .45:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    return s_
arrow = svg(f'<path d="{AR}" fill="{IN_C}" stroke="{DARK}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<path d="{AR}" fill="none" stroke="{OUT_C}" stroke-width="1" stroke-linejoin="round"/>'
            + pawsvg(10.5, 15, 2.2, OUT_C, "none", 0))
pointer = svg(pawsvg(16, 19, 6.5, PINK, DARK, 1.6) + f'<ellipse cx="16" cy="20.3" rx="3.2" ry="2.3" fill="{OUT_C}" opacity=".85"/>')
text = svg(f'<path d="M11 4h10M11 28h10M16 4v24" stroke="{DARK}" stroke-width="4" stroke-linecap="round"/><path d="M11 4h10M11 28h10M16 4v24" stroke="{PINK}" stroke-width="2" stroke-linecap="round"/>')
cross = svg(f'<g stroke="{DARK}" stroke-width="3.6"><path d="M16 2v10M16 20v10M2 16h10M20 16h10"/></g><g stroke="{PINK}" stroke-width="1.8"><path d="M16 2v10M16 20v10M2 16h10M20 16h10"/></g><circle cx="16" cy="16" r="2" fill="{BLUE}" stroke="{DARK}"/>')
def dbl(a):
    p = "M16 2 L22 9 H18.2 V23 H22 L16 30 L10 23 H13.8 V9 H10 Z"
    return svg(f'<g transform="rotate({a} 16 16)"><path d="{p}" fill="{PINK}" stroke="{DARK}" stroke-width="1.8" stroke-linejoin="round"/><path d="M16 6v20" stroke="{OUT_C}" stroke-width="1"/></g>')
move = svg(''.join(f'<g transform="rotate({a} 16 16)"><path d="M16 2 L21 8 H11 Z" fill="{PINK}" stroke="{DARK}" stroke-width="1.6" stroke-linejoin="round"/></g>' for a in (0, 90, 180, 270)) + pawsvg(16, 17, 3, BLUE, DARK, 1))
noway = svg(f'<circle cx="16" cy="16" r="11" fill="none" stroke="{DARK}" stroke-width="6"/><circle cx="16" cy="16" r="11" fill="none" stroke="#ff5577" stroke-width="3.6"/><path d="M8.2 23.8 23.8 8.2" stroke="{DARK}" stroke-width="6"/><path d="M8.2 23.8 23.8 8.2" stroke="#ff5577" stroke-width="3.6"/>')
help_ = svg(f'<path d="{AR}" fill="{IN_C}" stroke="{DARK}" stroke-width="2.4" stroke-linejoin="round"/><circle cx="24" cy="24" r="7" fill="{BLUE}" stroke="{DARK}" stroke-width="1.6"/><text x="24" y="28" font-family="Fredoka" font-weight="bold" font-size="11" text-anchor="middle" fill="{DARK}">?</text>')
def spin(i, n, small):
    a = 360 * i / n; body = ""
    for k in range(4):
        ang = math.radians(a + 90 * k); cx, cy = 16 + 9 * math.cos(ang), 16 + 9 * math.sin(ang)
        body += pawsvg(round(cx, 2), round(cy, 2), 2.6, [PINK, LAV, BLUE, WHITE][k], DARK, .8)
    if small:
        return svg(f'<path d="{AR}" fill="{IN_C}" stroke="{DARK}" stroke-width="2.4" stroke-linejoin="round"/><g transform="translate(13 13) scale(.6)">{body}</g>')
    return svg(body)
cursor(S, {"default": ([arrow], (4, 2)), "pointer": ([pointer], (16, 10)), "text": ([text], (16, 16)), "crosshair": ([cross], (16, 16)),
           "ns-resize": ([dbl(0)], (16, 16)), "ew-resize": ([dbl(90)], (16, 16)), "nesw-resize": ([dbl(45)], (16, 16)),
           "nwse-resize": ([dbl(-45)], (16, 16)), "move": ([move], (16, 16)), "not-allowed": ([noway], (16, 16)),
           "help": ([help_], (4, 2)), "wait": ([spin(i, 12, False) for i in range(12)], (16, 16)),
           "progress": ([spin(i, 12, True) for i in range(12)], (4, 2))})

# ── звуки: мягкие «бупы» и колокольчики ──────────────────────────────────────
C5, E5, G5, C6, A5, D6, E6 = 523.3, 659.3, 784.0, 1046.5, 880.0, 1174.7, 1318.5
boop = [(700, .07, "sine", .8, 1150), (1150, .2, "sine", .8, 620)]  # «ня~»
sounds(S, {
    "desktop-login": [(C5, .14, "bell", .7, None), (E5, .14, "bell", .7, None), (G5, .14, "bell", .7, None), (C6, .5, "bell", .8, None)],
    "message-new-instant": boop, "message": boop, "message-new-email": boop, "message-attention": boop,
    "dialog-information": [(G5, .12, "bell", .7, None), (C6, .3, "bell", .7, None)],
    "dialog-question": [(E5, .12, "sine", .7, None), (A5, .25, "sine", .7, 1000)],
    "dialog-warning": [(A5, .14, "tri", .7, None), (E5, .3, "tri", .7, None)],
    "dialog-warning-auth": [(A5, .14, "tri", .7, None), (E5, .3, "tri", .7, None)],
    "dialog-error": [(1200, .35, "tri", .8, 500)], "dialog-error-critical": [(1200, .2, "tri", .8, 600), (900, .35, "tri", .8, 400)],
    "outcome-success": [(E5, .1, "bell", .7, None), (G5, .1, "bell", .7, None), (E6, .35, "bell", .7, None)],
    "outcome-failure": [(G5, .15, "tri", .7, None), (E5, .15, "tri", .7, None), (C5, .35, "tri", .7, 400)],
    "complete": [(C6, .1, "bell", .6, None), (E6, .3, "bell", .6, None)],
    "audio-volume-change": [(1500, .05, "sine", .6, 1800)], "bell": [(1760, .12, "sine", .6, 1400)],
    "bell-window-system": [(1760, .12, "sine", .6, 1400)],
    "device-added": [(G5, .1, "sine", .7, None), (C6, .2, "sine", .7, None)],
    "device-removed": [(C6, .1, "sine", .7, None), (G5, .2, "sine", .7, None)],
    "power-plug": [(C5, .1, "sine", .7, None), (G5, .2, "sine", .7, None)],
    "power-unplug": [(G5, .1, "sine", .7, None), (C5, .2, "sine", .7, None)],
    "battery-low": [(A5, .2, "tri", .7, None), (A5, .2, "tri", .7, None)], "battery-caution": [(A5, .3, "tri", .7, 600)],
    "trash-empty": [(2000, .25, "sine", .5, 300)],
})

# ── сплэш ────────────────────────────────────────────────────────────────────
splash(S, splash_gif)

# ── Plymouth: котик со светом справа, логи слева ─────────────────────────────
pb = ImageOps.fit(brat, (W, H), Image.LANCZOS)
pb.alpha_composite(paw_field((W, H), 70, [PINK, LAV, BLUE], alpha=(10, 32), rmin=12, rmax=30, region=(0, 0, .62, 1), seed=3))
plymouth_log(S, pb)

# ── GRUB: пушистик справа, меню слева в тени ─────────────────────────────────
gb = ImageOps.fit(fluff, (W, H), Image.LANCZOS, centering=(0.5, 0.45))
gb = gb.transform((W, H), Image.AFFINE, (1, 0, -0.22 * W, 0, 1, 0), fillcolor=rgba(P["bg"]))
shade = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(shade)
for x in range(W):
    u = x / W; sd.line([(x, 0), (x, H)], fill=235 if u < .5 else max(0, int(235 * (1 - (u - .5) / .2))))
gb.alpha_composite(Image.merge("RGBA", (*[Image.new("L", (W, H), v) for v in rgb(P["bg"])], shade)))
gb.alpha_composite(paw_field((W, H), 40, [PINK, LAV], alpha=(14, 40), region=(0, 0, .5, 1), seed=5))
grub(S, gb)

# ── rEFInd: тёмный размытый пушистик + надписи ───────────────────────────────
rb = ImageEnhance.Brightness(main.filter(ImageFilter.GaussianBlur(10))).enhance(.45)
rd = ImageDraw.Draw(rb)
rd.text((140, 70), "brat mode", font=F(S, "title", 120), fill=rgba(PINK)); paw(rd, 140 + rd.textlength("brat mode", font=F(S, "title", 120)) + 80, 150, 34, rgba(PINK))
rd.text((146, 220), "pick one, cutie ♡  早くして～", font=F(S, "jp", 44), fill=rgba(BLUE))
rd.text((146, H - 140), "LEFT / RIGHT  choose     ENTER  pretty please?     F2  options", font=F(S, "ui_bold", 30), fill=rgba(PINK))
rd.text((146, H - 92), "ふん、別に待ってないし… ♡", font=F(S, "jp", 30), fill=rgba(P["dim"]))
rb.alpha_composite(paw_field((W, H), 30, [PINK, LAV, BLUE], alpha=(20, 50), seed=9))
refind(S, rb, {"os_main": (astolfo.crop(AVB), "LINUX", PINK, False),
               "os_fallback": (astolfo.crop(AVB), "FALLBACK", "#8d7d9e", True),
               "os_grub": (fluff.crop((2600, 0, 5600, 3000)), "GRUB", BLUE, False),
               "os_unknown": (None, "???", LAV, False)})

# ── SDDM: уютная комната, вход слева ─────────────────────────────────────────
sroom = ImageOps.fit(brat, (W, H), Image.LANCZOS); sroom.convert("RGB").save(WP + "/sddm.png")
sddm(S, WP + "/sddm.png", WP + "/sddm.png")

# ── RGB клавиатура: флаг фембоя (розовый · белый · голубой) ──────────────────
rgb_art(S, {"P": (255, 40, 150), "W": (255, 200, 230), "B": (40, 160, 255), "L": (150, 60, 255), "K": (0, 0, 0)},
        ["P" * 23, "L" * 23, "P" * 23, "L" * 23, "P" * 23, "L" * 23])

# ── превью для переключателя ─────────────────────────────────────────────────
pv = main.resize((960, 540), Image.LANCZOS); pd = ImageDraw.Draw(pv)
pd.rounded_rectangle([24, 400, 600, 516], radius=18, fill=(15, 10, 20, 210))
pd.text((44, 410), S["name"], font=F(S, "title", 44), fill=rgba(PINK))
pd.text((46, 466), "chokers · thigh-highs · sass · neon", font=F(S, "ui", 26), fill=rgba(BLUE))
pv.convert("RGB").save(T(S, "preview.png"))

manifest(S, wallpapers={"main": {"type": "video", "path": WP + "/main-live.mp4", "poster": WP + "/main-poster.jpg"},
                        "side": {"type": "image", "path": WP + "/side-1080p.png"}},
         lockscreen={"type": "video", "path": WP + "/main-live.mp4", "poster": WP + "/main-poster.jpg"},
         kickoff_icon=T(S, "kickoff.png"))
shutil.rmtree(T(S, "build-tmp", "frames"), ignore_errors=True)
print("bratty: ok")

#!/usr/bin/env python3
"""Семейство фембой-тем: одно описание V → полная тема (обои, цвета, курсор, звуки, сплэш, Plymouth, GRUB, rEFInd, SDDM, Claude).
Запуск: python family.py <id>|all   (описания — в family_themes.py)"""
import os, sys, math, random, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
import numpy as np

POOL = RICE + "/pool"
FR = HOME + "/.local/share/fonts/rice"; FN = HOME + "/.local/share/fonts/nerv"
FONTS = {"fredoka": ((FR + "/Fredoka[wdth,wght].ttf", [700, 100]), (FR + "/Fredoka[wdth,wght].ttf", [400, 100]),
                     (FR + "/Fredoka[wdth,wght].ttf", [600, 100]), "Fredoka"),
         "mincho": ((FN + "/ShipporiMinchoB1-ExtraBold.ttf", None), (FN + "/Oswald[wght].ttf", 400),
                    (FN + "/Oswald[wght].ttf", 600), "Oswald"),
         "vt": ((FR + "/VT323-Regular.ttf", None), (FR + "/VT323-Regular.ttf", None), (FR + "/VT323-Regular.ttf", None), "VT323"),
         "oswald": ((FN + "/Oswald[wght].ttf", 700), (FN + "/Oswald[wght].ttf", 400), (FN + "/Oswald[wght].ttf", 600), "Oswald")}
MPR = FR + "/MPLUSRounded1c-ExtraBold.ttf"; MPRB = FR + "/MPLUSRounded1c-Bold.ttf"
JBM = "/usr/share/fonts/TTF/JetBrainsMonoNerdFontMono-Regular.ttf"


def img(name):
    p = next(f for f in os.listdir(POOL) if f.startswith(f"wallhaven-{name}."))
    im = Image.open(f"{POOL}/{p}").convert("RGBA")
    g = im.convert("L").resize((64, max(8, im.height // 8))); rows = [sum(g.crop((0, y, 64, y + 1)).tobytes()) / 64 for y in range(g.height)]
    if rows[0] < 6 and rows[-1] < 6 and max(rows) > 40:  # леттербокс
        top = next(y for y, v in enumerate(rows) if v > 22); bot = g.height - next(y for y, v in enumerate(reversed(rows)) if v > 22)
        im = im.crop((0, (top + 2) * 8, im.width, (bot - 2) * 8))
    return im


def focus_crop(im, f):
    cx, cy, s = f; side = round(s * im.height); x = round(cx * im.width - side / 2); y = round(cy * im.height - side / 2)
    x = max(0, min(im.width - side, x)); y = max(0, min(im.height - side, y))
    return im.crop((x, y, x + side, y + side))


def heart(dd, cx, cy, r, fill):
    dd.ellipse([cx - r, cy - r * .7, cx, cy + r * .3], fill=fill); dd.ellipse([cx, cy - r * .7, cx + r, cy + r * .3], fill=fill)
    dd.polygon([(cx - r * .97, cy - r * .05), (cx + r * .97, cy - r * .05), (cx, cy + r * 1.1)], fill=fill)


def star(dd, cx, cy, r, fill):
    pts = [(cx + (r if k % 2 == 0 else r * .45) * math.cos(math.radians(-90 + 36 * k)),
            cy + (r if k % 2 == 0 else r * .45) * math.sin(math.radians(-90 + 36 * k))) for k in range(10)]
    dd.polygon(pts, fill=fill)


SHAPES = {"paw": paw, "heart": heart, "star": star}


def field(size, n, cols, shapes, alpha=(12, 36), rmin=10, rmax=26, region=(0, 0, 1, 1), seed=1):
    rnd = random.Random(seed); lay = Image.new("RGBA", size, (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
    for _ in range(n):
        SHAPES[rnd.choice(shapes)](dd, rnd.uniform(region[0], region[2]) * size[0], rnd.uniform(region[1], region[3]) * size[1],
                                   rnd.uniform(rmin, rmax), rgba(rnd.choice(cols), rnd.randint(*alpha)))
    return lay


def shade_left(im, col, upto=.5, fade=.2, strength=235):
    s = Image.new("L", im.size, 0); sd = ImageDraw.Draw(s); w = im.width
    for x in range(w):
        u = x / w; sd.line([(x, 0), (x, im.height)], fill=strength if u < upto else max(0, int(strength * (1 - (u - upto) / fade))))
    out = im.copy(); out.alpha_composite(Image.merge("RGBA", (*[Image.new("L", im.size, v) for v in rgb(col)], s))); return out


def art_right(im, bg, shift=.22, focus=(.5, .5)):
    b = ImageOps.fit(im, (W, H), Image.LANCZOS, centering=focus)
    return b.transform((W, H), Image.AFFINE, (1, 0, -shift * W, 0, 1, 0), fillcolor=rgba(bg))


# ── наборы звуков ────────────────────────────────────────────────────────────
C5, E5, G5, A5, C6, E6 = 523.3, 659.3, 784.0, 880.0, 1046.5, 1318.5
def sound_kit(kind, wave):
    if kind == "nya":  msg = [(700, .07, "sine", .8, 1150), (1150, .2, "sine", .8, 620)]
    elif kind == "chip": msg = [(E6, .07, "square", .45, None), (0, .04, "rest", 0, None), (E6, .1, "square", .45, None)]
    elif kind == "bell": msg = [(G5, .12, "bell", .7, None), (C6, .3, "bell", .7, None)]
    else:              msg = [(880, .09, "sine", .8, 1320), (0, .03, "rest", 0, None), (1320, .12, "sine", .7, 1760)]
    w = wave
    return {
        "desktop-login": [(C5, .14, w, .7, None), (E5, .14, w, .7, None), (G5, .14, w, .7, None), (C6, .5, w, .8, None)],
        "message-new-instant": msg, "message": msg, "message-new-email": msg, "message-attention": msg,
        "dialog-information": [(G5, .12, w, .7, None), (C6, .3, w, .7, None)],
        "dialog-question": [(E5, .12, "sine", .7, None), (A5, .25, "sine", .7, 1000)],
        "dialog-warning": [(A5, .14, "tri", .7, None), (E5, .3, "tri", .7, None)],
        "dialog-warning-auth": [(A5, .14, "tri", .7, None), (E5, .3, "tri", .7, None)],
        "dialog-error": [(1200, .35, "tri", .8, 500)], "dialog-error-critical": [(1200, .2, "tri", .8, 600), (900, .35, "tri", .8, 400)],
        "outcome-success": [(E5, .1, w, .7, None), (G5, .1, w, .7, None), (E6, .35, w, .7, None)],
        "outcome-failure": [(G5, .15, "tri", .7, None), (E5, .15, "tri", .7, None), (C5, .35, "tri", .7, 400)],
        "complete": [(C6, .1, w, .6, None), (E6, .3, w, .6, None)],
        "audio-volume-change": [(1500, .05, "sine", .6, 1800)], "bell": [(1760, .12, "sine", .6, 1400)],
        "bell-window-system": [(1760, .12, "sine", .6, 1400)],
        "device-added": [(G5, .1, "sine", .7, None), (C6, .2, "sine", .7, None)],
        "device-removed": [(C6, .1, "sine", .7, None), (G5, .2, "sine", .7, None)],
        "power-plug": [(C5, .1, "sine", .7, None), (G5, .2, "sine", .7, None)],
        "power-unplug": [(G5, .1, "sine", .7, None), (C5, .2, "sine", .7, None)],
        "battery-low": [(A5, .2, "tri", .7, None), (A5, .2, "tri", .7, None)], "battery-caution": [(A5, .3, "tri", .7, 600)],
        "trash-empty": [(2000, .25, "sine", .5, 300)]}


# ── курсор (как у femboy, в цветах темы) ─────────────────────────────────────
def build_cursor(S, A1, A2, DARK, shape):
    WHITE = "#ffffff"
    def svg(b): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">{b}</svg>'
    AR = "M4 2 L4 25 L9.5 19.8 L13.2 28.2 L17 26.6 L13.4 18.4 L21 18.4 Z"
    def pawsvg(cx, cy, r, fill, stroke=DARK, sw=1.2):
        s_ = f'<ellipse cx="{cx}" cy="{cy + r * .2}" rx="{r}" ry="{r * .75}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        for dx, dy in ((-1.05, -1.0), (-.38, -1.55), (.38, -1.55), (1.05, -1.0)):
            s_ += f'<ellipse cx="{cx + dx * r:.2f}" cy="{cy + dy * r:.2f}" rx="{r * .36:.2f}" ry="{r * .45:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        return s_
    def heartsvg(cx, cy, r, fill, stroke=DARK, sw=1.2):
        return (f'<path d="M{cx} {cy + r} C{cx - r * 1.6} {cy - r * .2} {cx - r * .8} {cy - r * 1.4} {cx} {cy - r * .45} '
                f'C{cx + r * .8} {cy - r * 1.4} {cx + r * 1.6} {cy - r * .2} {cx} {cy + r} Z" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    mark = pawsvg if shape == "paw" else heartsvg
    arrow = svg(f'<path d="{AR}" fill="{A1}" stroke="{DARK}" stroke-width="2.4" stroke-linejoin="round"/>'
                f'<path d="{AR}" fill="none" stroke="{WHITE}" stroke-width="1" stroke-linejoin="round"/>' + mark(10.5, 15, 2.2, WHITE, "none", 0))
    pointer = svg(mark(16, 19, 6.5, A1, DARK, 1.6))
    text = svg(f'<path d="M11 4h10M11 28h10M16 4v24" stroke="{DARK}" stroke-width="4" stroke-linecap="round"/><path d="M11 4h10M11 28h10M16 4v24" stroke="{A1}" stroke-width="2" stroke-linecap="round"/>')
    cross = svg(f'<g stroke="{DARK}" stroke-width="3.6"><path d="M16 2v10M16 20v10M2 16h10M20 16h10"/></g><g stroke="{A1}" stroke-width="1.8"><path d="M16 2v10M16 20v10M2 16h10M20 16h10"/></g><circle cx="16" cy="16" r="2" fill="{A2}" stroke="{DARK}"/>')
    def dbl(a):
        p = "M16 2 L22 9 H18.2 V23 H22 L16 30 L10 23 H13.8 V9 H10 Z"
        return svg(f'<g transform="rotate({a} 16 16)"><path d="{p}" fill="{A1}" stroke="{DARK}" stroke-width="1.8" stroke-linejoin="round"/><path d="M16 6v20" stroke="{WHITE}" stroke-width="1"/></g>')
    move = svg(''.join(f'<g transform="rotate({a} 16 16)"><path d="M16 2 L21 8 H11 Z" fill="{A1}" stroke="{DARK}" stroke-width="1.6" stroke-linejoin="round"/></g>' for a in (0, 90, 180, 270)) + mark(16, 17, 3, A2, DARK, 1))
    noway = svg(f'<circle cx="16" cy="16" r="11" fill="none" stroke="{DARK}" stroke-width="6"/><circle cx="16" cy="16" r="11" fill="none" stroke="#ff5577" stroke-width="3.6"/><path d="M8.2 23.8 23.8 8.2" stroke="{DARK}" stroke-width="6"/><path d="M8.2 23.8 23.8 8.2" stroke="#ff5577" stroke-width="3.6"/>')
    help_ = svg(f'<path d="{AR}" fill="{A1}" stroke="{DARK}" stroke-width="2.4" stroke-linejoin="round"/><circle cx="24" cy="24" r="7" fill="{A2}" stroke="{DARK}" stroke-width="1.6"/><text x="24" y="28" font-family="Fredoka" font-weight="bold" font-size="11" text-anchor="middle" fill="{DARK}">?</text>')
    def spin(i, n, small):
        a = 360 * i / n; body = ""
        for k in range(4):
            ang = math.radians(a + 90 * k); cx, cy = 16 + 9 * math.cos(ang), 16 + 9 * math.sin(ang)
            body += mark(round(cx, 2), round(cy, 2), 2.6, [A1, A2, WHITE, A1][k], DARK, .8)
        if small:
            return svg(f'<path d="{AR}" fill="{A1}" stroke="{DARK}" stroke-width="2.4" stroke-linejoin="round"/><g transform="translate(13 13) scale(.6)">{body}</g>')
        return svg(body)
    cursor(S, {"default": ([arrow], (4, 2)), "pointer": ([pointer], (16, 10)), "text": ([text], (16, 16)), "crosshair": ([cross], (16, 16)),
               "ns-resize": ([dbl(0)], (16, 16)), "ew-resize": ([dbl(90)], (16, 16)), "nesw-resize": ([dbl(45)], (16, 16)),
               "nwse-resize": ([dbl(-45)], (16, 16)), "move": ([move], (16, 16)), "not-allowed": ([noway], (16, 16)),
               "help": ([help_], (4, 2)), "wait": ([spin(i, 12, False) for i in range(12)], (16, 16)),
               "progress": ([spin(i, 12, True) for i in range(12)], (4, 2))})


def ansi_from(P):
    a, b = P["accent"], P["accent2"]
    base = ["#2a1d33", "#ff5c8a", "#7dffb2", "#ffd27a", b, a, "#8ff0e6", "#e6d8f0"]
    return base + [mix(c, "#ffffff", .25) for c in base[:-1]] + ["#ffffff"]


# ── сборка ───────────────────────────────────────────────────────────────────
def build(V):
    tid = V["id"]; D = mkdir(f"{RICE}/themes/{tid}")
    A1, A2, A3, BG = V["accent"], V["accent2"], V.get("accent3", "#ffffff"), V["bg"]
    FG = V.get("fg", "#fbefff"); DIM = V.get("dim", mix(FG, BG, .45))
    ft, fu, fub, ffam = FONTS[V.get("font", "fredoka")]
    nm = V["name"]; pal = {"bg": BG, "bg2": mix(BG, A1, .05), "surface": mix(BG, A1, .14), "fg": FG, "dim": DIM, "accent": A1, "accent2": A2,
                           "neg": "#ff5577", "pos": "#7dffb2", "neu": "#ffd27a", "link": A2, "visited": A3, "sel_fg": mix(BG, "#000000", .3),
                           "term_bg": mix(BG, "#000000", .2)}
    camel = "".join(p.capitalize() for p in tid.split("-"))
    mono = V.get("mono", "JetBrainsMono Nerd Font Mono")
    S = {"id": tid, "dir": D, "name": nm, "desc": V["desc"], "pal": pal, "ansi": ansi_from(pal),
         "fonts": {"title": ft, "ui": fu, "ui_bold": fub, "jp": (MPR, None)},
         "kde_colors": "Femboy" + camel, "konsole_scheme": "Femboy" + camel, "konsole_profile": "Femboy " + camel,
         "term_opacity": 0.9, "cursor": "Femboy-" + camel, "sounds": "femboy-" + tid,
         "prompt": {"line1": [(" " if V.get("cursor", "paw") == "paw" else " ", A1, True), ("{USER}", A2, False), ("@", DIM, False),
                              (V["host"] + " ", A3 if A3 != "#ffffff" else A1, False), (":: ", DIM, False), ("{WD} ", FG, False), ("[", DIM, False)],
                    "arrow": [("❯", A1, True), ("❯", A3, False), ("❯", A2, False)], "tail": ("]", DIM)},
         "prompt_status": ((V["ok"], "#7dffb2"), (V["fail"], "#ff5577")),
         "fastfetch": {"key_color": "95", "title_color": "94",
                       "header": [f"{{#1;95}}  {{#0;94}}{V['short']} {{#90}}// {{#95}}{V['tag']}",
                                  "{#35}─────────────────────────────────────────",
                                  f"{{#95}}MOOD      {{#97}}{V['mood']}", f"{{#95}}OUTFIT    {{#97}}{V['outfit']}"],
                       "keys": [("title", "USER     "), ("os", "OS       "), ("kernel", "KERNEL   "), ("packages", "PACKAGES "),
                                ("shell", "SHELL    "), ("terminal", "TERMINAL "), ("wm", "WM       "), ("cpu", "BRAIN    "),
                                ("gpu", "SPARKLE  "), ("memory", "SNACKS   "), ("uptime", "BEING CUTE")]},
         "splash": {"id": f"femboy.{tid}", "title": V["short"], "title_font": ffam, "font": ffam, "subtitle": V["splash_sub"],
                    "radius": V.get("radius", 24), "messages": V["splash"]},
         "plymouth": {"name": f"{tid}-log", "title": V["short"], "head1": V["head1"], "head2": V["head2"], "tab": "boot.log",
                      "tab_right": V["tab_right"], "bar": V["bar"], "radius": V.get("radius", 18), "seg_radius": 6 if V.get("radius", 18) else 0,
                      "footer": V["footer"], "font_family": ffam, "mono_family": mono, "fsize_div": 48 if mono == "VT323" else 62,
                      "names": V["names"], "tags": V["tags"], "c_ok": "#7dffb2", "c_amb": A1, "c_name": A3 if A3 != "#ffffff" else A2,
                      "c_text": mix(FG, A1, .15), "seg": (A3 if A3 != "#ffffff" else A2, A1, "#7dffb2"), "stop": V["stop"],
                      "sub": {"boot": (V["sub"][0], FG), "shutdown": (V["sub"][1], A1), "reboot": (V["sub"][2], A2)},
                      "ask": V["ask"], "ambient": V["ambient"]},
         "grub": {"name": "Femboy-" + camel, "title": V["short"] + " ♡", "item": mix(A1, "#ffffff", .35), "item_sel": "#ffffff", "radius": 0,
                  "fonts": {"title": MPR, "ui": MPRB, "menu": MPRB},
                  "labels": [{"left": "8%+6", "top": "8%+122", "color": A2, "text": V["grub1"]},
                             {"left": "8%+6", "top": "8%+156", "color": DIM, "text": V["grub2"]},
                             {"left": "8%", "top": "100%-136", "color": A1, "text": "  UP/DOWN - choose", "font": "menu"},
                             {"left": "8%", "top": "100%-110", "color": A1, "text": "  ENTER - " + V["enter"], "font": "menu"},
                             {"left": "8%", "top": "100%-84", "color": DIM, "text": "  E - edit  //  C - console"}]},
         "refind": {"name": "femboy-" + tid, "font": JBM, "shape": V.get("shape", "circle")},
         "sddm": {"name": "femboy-" + tid, "font": ffam, "position": V.get("sddm_pos", "left"), "message": V["sddm"], "spinner": V["sddm_spin"]}}
    for d_ in ("out", "system", "build-tmp", "wallpapers"): mkdir(T(S, d_))
    WP = T(S, "wallpapers"); shapes = V.get("shapes", ["paw", "heart"])
    main_src = img(V["main"]); side_src = img(V["side"])
    if V.get("dark_key"): main_src = dark_key(main_src, BG)
    if V.get("side_dark_key"): side_src = dark_key(side_src, BG)
    main = ImageOps.fit(main_src, (W, H), Image.LANCZOS, centering=V.get("focus", (.5, .5)))
    if V.get("dim_main"): main = ImageEnhance.Brightness(main).enhance(V["dim_main"])
    ImageOps.fit(side_src, (1920, 1080), Image.LANCZOS, centering=V.get("side_focus", (.5, .5))).convert("RGB").save(WP + "/side-1080p.png")
    rnd = random.Random(tid)
    PRT = [(rnd.random(), rnd.random(), rnd.uniform(9, 22), rnd.choice([A1, A2, A3, "#ffffff"]), rnd.random(), rnd.choice(shapes)) for _ in range(42)]
    def particles(dd, t, lay):
        for (x0, y0, r, col, ph, sh) in PRT:
            y = (y0 - (t + ph)) % 1; x = x0 + 0.012 * math.sin(2 * math.pi * (t * 2 + ph))
            a = max(0, min(150, int(150 * (0.5 + 0.5 * math.sin(2 * math.pi * (t + ph))))))
            SHAPES[sh](dd, x * W, y * H, r, rgba(col, a))
    _, gif = live_wallpaper(S, main, WP + "/main-live.mp4", particles, seconds=10, fps=24, glow=(A1, 0.05), poster=WP + "/main-poster.jpg")
    # аватар / лого / меню
    av_src = img(V.get("avatar_img", V["main"])); av = focus_crop(av_src, V["avatar"]).resize((512, 512), Image.LANCZOS)
    av.convert("RGB").save(T(S, "system", "avatar.png"))
    logo = av.copy(); m = Image.new("L", (512, 512), 0); ImageDraw.Draw(m).ellipse([0, 0, 511, 511], fill=255); logo.putalpha(m)
    ring = Image.new("RGBA", (540, 540), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse([0, 0, 539, 539], fill=rgba(A1))
    ring.alpha_composite(logo, (14, 14)); fastfetch(S, ring.resize((256, 256), Image.LANCZOS))
    def kick(s):
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        dd.ellipse([0, 0, s - 1, s - 1], fill=rgba(BG)); dd.ellipse([0, 0, s - 1, s - 1], outline=rgba(A1), width=s // 14)
        if V.get("cursor", "paw") == "paw": paw(dd, s / 2, s * .58, s * .17, rgba(A1))
        else: heart(dd, s / 2, s * .48, s * .26, rgba(A1))
        return im
    ss(kick, 256).save(T(S, "kickoff.png"))
    kde_colors(S); terminal(S); prompts(S)
    build_cursor(S, A1, A2, mix(BG, "#000000", .3), V.get("cursor", "paw"))
    sounds(S, sound_kit(V.get("kit", "boop"), V.get("wave", "bell")))
    splash(S, gif)
    cx = V.get("avatar")[0] if not V.get("avatar_img") else .5
    shift = V.get("shift", max(0, min(.6, .74 - cx)))
    def art(src):
        a = art_right(src, BG, shift, V.get("focus", (.5, .5)))
        return ImageEnhance.Brightness(a).enhance(.5) if is_light(src) else a
    ply_src = img(V.get("ply_img", V["main"]))
    if V.get("dark_key") and "ply_img" not in V: ply_src = main_src
    pb = shade_left(art(ply_src), BG)
    pb.alpha_composite(field((W, H), 60, [A1, A2, A3], shapes, alpha=(10, 30), region=(0, 0, .6, 1), seed=3))
    plymouth_log(S, pb)
    gb = shade_left(art(main_src), BG)
    gb.alpha_composite(field((W, H), 36, [A1, A3], shapes, alpha=(14, 40), region=(0, 0, .5, 1), seed=5))
    grub(S, gb)
    rb = ImageEnhance.Brightness(main.filter(ImageFilter.GaussianBlur(10))).enhance(.42); rd = ImageDraw.Draw(rb)
    tf = font(ft[0], 120, ft[1]); rd.text((140, 70), V["short"], font=tf, fill=rgba(A1))
    rd.text((146, 220), V["refind"], font=font(MPR, 44), fill=rgba(A2))
    rd.text((146, H - 140), f"LEFT / RIGHT  choose     ENTER  {V['enter']}     F2  options", font=font(fub[0], 30, fub[1]), fill=rgba(A1))
    rb.alpha_composite(field((W, H), 26, [A1, A2, A3], shapes, alpha=(20, 50), seed=9))
    refind(S, rb, {"os_main": (av_src if False else focus_crop(av_src, V["avatar"]), "LINUX", A1, False),
                   "os_fallback": (focus_crop(av_src, V["avatar"]), "FALLBACK", DIM, True),
                   "os_grub": (focus_crop(side_src, (.5, .5, 1.0)), "GRUB", A2, False), "os_unknown": (None, "???", A3, False)})
    sb = ImageOps.fit(img(V.get("sddm_img", V["side"])), (W, H), Image.LANCZOS, centering=V.get("side_focus", (.5, .5)))
    sb.convert("RGB").save(WP + "/sddm.png"); sddm(S, WP + "/sddm.png", WP + "/sddm.png")
    k = V.get("rgb", [A1, A3, A2]); pal_rgb = {"A": rgb(k[0]), "B": rgb(k[1]), "C": rgb(k[2]), "K": (0, 0, 0)}
    rgb_art(S, pal_rgb, ["A" * 23, "B" * 23, "C" * 23, "C" * 23, "B" * 23, "A" * 23])
    pv = main.resize((960, 540), Image.LANCZOS); pd = ImageDraw.Draw(pv)
    pd.rounded_rectangle([24, 400, 640, 516], radius=18, fill=rgba(BG, 215))
    pd.text((44, 406), nm, font=font(ft[0], 40, ft[1]), fill=rgba(A1))
    pd.text((46, 466), V["tagline"], font=font(fu[0], 24, fu[1]), fill=rgba(A2))
    pv.convert("RGB").save(T(S, "preview.png"))
    manifest(S, wallpapers={"main": {"type": "video", "path": WP + "/main-live.mp4", "poster": WP + "/main-poster.jpg"},
                            "side": {"type": "image", "path": WP + "/side-1080p.png"}},
             lockscreen={"type": "video", "path": WP + "/main-live.mp4", "poster": WP + "/main-poster.jpg"},
             kickoff_icon=T(S, "kickoff.png"))
    json.dump({"title": V["short"] + " ♡", "sub": V["tagline"], "mascot": "" if V.get("cursor", "paw") == "paw" else "♡",
               "accent": A1, "accent2": A2, "dim": DIM, "thinking": V["c_think"], "tool": V["c_tool"], "done": V["ok"], "error": V["fail"],
               "greet": V["greet"], "quotes": V["quotes"],
               "persona": ("Flavor only: " + V["persona"] + " Keep it light and strictly SFW: at most one short in-character remark per reply, "
                           "never at the expense of clarity, accuracy, safety or the user's instructions. Reply in the user's language.")},
              open(T(S, "claude.json"), "w"), ensure_ascii=False, indent=2)
    shutil.rmtree(T(S, "build-tmp", "frames"), ignore_errors=True)
    print(f"{tid}: ok", flush=True)


def dark_key(im, bg, tol=42):
    """фон, связанный с краями картинки и похожий на цвет углов → тёмный градиент темы (белое внутри персонажа не трогаем)"""
    rgbim = im.convert("RGB"); sm = rgbim.resize((im.width // 4, im.height // 4))
    a = np.asarray(sm).astype(np.int16)
    corners = np.array([a[2, 2], a[2, -3], a[-3, 2], a[-3, -3]]); ref = np.median(corners, 0)
    like = (np.abs(a - ref).sum(2) < tol * 3 // 2).astype(np.uint8) * 255
    m = Image.fromarray(like).copy()
    for x in range(0, m.width, 12):
        for y in (0, m.height - 1):
            if m.getpixel((x, y)) == 255: ImageDraw.floodfill(m, (x, y), 128)
    for y in range(0, m.height, 12):
        for x in (0, m.width - 1):
            if m.getpixel((x, y)) == 255: ImageDraw.floodfill(m, (x, y), 128)
    mask = m.point(lambda v: 255 if v == 128 else 0).filter(ImageFilter.MaxFilter(3)).resize(im.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(3))
    g = Image.new("RGBA", im.size); gd = ImageDraw.Draw(g)
    for y in range(im.height): gd.line([(0, y), (im.width, y)], fill=rgba(mix(bg, mix(bg, "#ffffff", .10), y / im.height)))
    return Image.composite(g, im.convert("RGBA"), mask)


def is_light(im):
    return sum(im.convert("L").resize((32, 18)).tobytes()) / (32 * 18) > 140


if __name__ == "__main__":
    from family_themes import THEMES
    want = sys.argv[1:] or ["all"]
    for V in THEMES:
        if "all" in want or V["id"] in want:
            try: build(V)
            except Exception as e:
                import traceback; traceback.print_exc(); print(f"{V['id']}: FAIL {e}", flush=True)

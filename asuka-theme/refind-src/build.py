#!/usr/bin/env python3
"""rEFInd theme nerv-asuka: баннер, гекс-иконки, выделение, моно-шрифт. + preview.png (макет экрана)."""
import os, shutil, math
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance

A = os.path.expanduser("~/.local/share/asuka-theme")
OUT = A + "/refind/nerv-asuka"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT + "/icons")
F = os.path.expanduser("~/.local/share/fonts/nerv")
SER = F + "/ShipporiMinchoB1-ExtraBold.ttf"; OSW = F + "/Oswald[wght].ttf"
JP = F + "/NotoSansJP[wght].ttf"; MONO = F + "/ShareTechMono-Regular.ttf"
RED = (220, 38, 48, 255); ORG = (255, 106, 19, 255); DIM = (150, 110, 100, 255); CRM = (245, 226, 214, 255)
W, H = 2560, 1440
BIG, SMALL = 256, 96


def font(p, s, wght=None):
    f = ImageFont.truetype(p, s)
    if wght:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f


def hexpts(cx, cy, r, rot=30):
    return [(cx + r * math.cos(math.radians(60 * k + rot)), cy + r * math.sin(math.radians(60 * k + rot))) for k in range(6)]


def hexmask(size, r=None):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).polygon(hexpts(size / 2, size / 2, r or size / 2), fill=255); return m


def ss(fn, size, k=4):
    """рисуем в k раз крупнее и сжимаем — гладкие края"""
    im = fn(size * k); return im.resize((size, size), Image.LANCZOS)


# ── баннер ───────────────────────────────────────────────────────────────────
bg = Image.open(A + "/img/wallhaven/wallhaven-vp2718.png").convert("RGBA").resize((W, H), Image.LANCZOS)
bg = bg.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, 0), fillcolor=(0, 0, 0, 255))
d = ImageDraw.Draw(bg)
for row in range(0, 30):
    for col in range(0, 44):
        cx = col * 66 + (33 if row % 2 else 0); cy = row * 57
        d.polygon(hexpts(cx, cy, 30), outline=(40, 6, 9, 255))
for y in range(0, H, 4): d.line([(0, y), (W, y)], fill=(0, 0, 0, 70))

d.text((140, 70), "NERV", font=font(SER, 130), fill=RED)
nx = 140 + round(d.textlength("NERV", font=font(SER, 130))) + 40
d.text((nx, 92), "MAGI SYSTEM // UNIT SELECT", font=font(OSW, 50, 600), fill=ORG)
d.text((nx, 160), "機体選択 — CHOOSE YOUR EVA", font=font(JP, 32, 700), fill=CRM)
d.line([(140, 250), (1500, 250)], fill=RED, width=3)
d.text((140, 262), "EVA-02 // PILOT: SORYU ASUKA LANGLEY   ·   SYNC STANDBY", font=font(OSW, 26, 300), fill=DIM)

# низ: подсказки + полосы
d.line([(140, H - 150), (1500, H - 150)], fill=RED, width=2)
d.text((140, H - 138), "LEFT / RIGHT  SELECT UNIT     ENTER  LAUNCH     F2 / INS  OPTIONS     ESC  RESCAN",
       font=font(OSW, 28, 500), fill=ORG)
d.text((140, H - 92), "あんたバカぁ？ 早く選びなさいよ！", font=font(JP, 30, 700), fill=DIM)
hz = Image.new("RGBA", (560, 50), (0, 0, 0, 0)); hd = ImageDraw.Draw(hz)
for i in range(-2, 20): hd.polygon([(i * 40, 50), (i * 40 + 20, 50), (i * 40 + 70, 0), (i * 40 + 50, 0)], fill=ORG)
bg.alpha_composite(hz, (W - 640, H - 110))
bg.convert("RGB").save(OUT + "/banner.png", optimize=True)

# ── большие иконки ───────────────────────────────────────────────────────────
av = Image.open(A + "/img/avatar.png").convert("RGBA")


def os_icon(photo, tag, col, gray=False):
    def draw(s):
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        dd.polygon(hexpts(s / 2, s / 2, s / 2), fill=col)
        inner = round(s * 0.88); off = (s - inner) // 2
        if photo is not None:
            p = ImageOps.fit(photo, (inner, inner))
            if gray: p = ImageOps.grayscale(p).convert("RGBA"); p = ImageEnhance.Brightness(p).enhance(0.7)
            im.paste(p, (off, off), hexmask(inner))
        else:
            dd.polygon(hexpts(s / 2, s / 2, inner / 2), fill=(12, 3, 4, 255))
        # плашка с подписью снизу
        bh = round(s * 0.16); by = round(s * 0.66)
        dd.rectangle([round(s * 0.14), by, round(s * 0.86), by + bh], fill=(0, 0, 0, 215))
        f = font(OSW, round(bh * 0.72), 600); tw = dd.textlength(tag, font=f)
        dd.text(((s - tw) / 2, by + bh * 0.06), tag, font=f, fill=col)
        return im
    return ss(draw, BIG)


def nerv_mark(s):
    """листок NERV, нарисованный примитивами: полулист + надпись"""
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.pieslice([s * 0.18, s * 0.08, s * 0.82, s * 0.72], 200, 340, fill=RED)
    dd.pieslice([s * 0.18, s * 0.08, s * 0.82, s * 0.72], 20, 160, fill=(120, 14, 20, 255))
    f = font(SER, round(s * 0.2)); tw = dd.textlength("NERV", font=f)
    dd.text(((s - tw) / 2, s * 0.30), "NERV", font=f, fill=CRM)
    return im


os_icon(av, "ASUKA", RED).save(OUT + "/icons/os_asuka.png")
os_icon(av, "FALLBACK", (150, 110, 100, 255), gray=True).save(OUT + "/icons/os_fallback.png")
g = os_icon(None, "GRUB", ORG); g.alpha_composite(nerv_mark(BIG).resize((round(BIG * 0.7),) * 2, Image.LANCZOS), (round(BIG * 0.15), round(BIG * 0.06)))
g.save(OUT + "/icons/os_grub.png")
os_icon(av, "UNKNOWN", DIM, gray=True).save(OUT + "/icons/os_unknown.png")


# ── маленькие иконки (инструменты) ───────────────────────────────────────────
def tool_icon(kind):
    def draw(s):
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        dd.polygon(hexpts(s / 2, s / 2, s / 2), fill=(12, 3, 4, 235), outline=ORG, width=round(s * 0.05))
        c = s / 2; r = s * 0.22; w = round(s * 0.07)
        if kind == "shutdown":
            dd.arc([c - r, c - r, c + r, c + r], -60, 240, fill=RED, width=w)
            dd.line([(c, c - r * 1.25), (c, c)], fill=RED, width=w)
        elif kind == "reset":
            dd.arc([c - r, c - r, c + r, c + r], 30, 330, fill=ORG, width=w)
            ax, ay = c + r * math.cos(math.radians(330)), c + r * math.sin(math.radians(330))
            dd.polygon([(ax - s * .09, ay - s * .02), (ax + s * .09, ay - s * .02), (ax, ay + s * .1)], fill=ORG)
        elif kind == "firmware":
            f = font(OSW, round(s * 0.22), 700); t = "BIOS"; tw = dd.textlength(t, font=f)
            dd.text((c - tw / 2, c - s * 0.16), t, font=f, fill=CRM)
        elif kind == "about":
            f = font(JP, round(s * 0.34), 800); t = "弐"; tw = dd.textlength(t, font=f)
            dd.text((c - tw / 2, c - s * 0.26), t, font=f, fill=RED)
        return im
    return ss(draw, SMALL)


for k in ("shutdown", "reset", "firmware", "about"): tool_icon(k).save(OUT + f"/icons/func_{k}.png")


# стрелки прокрутки
def arrow(left):
    def draw(s):
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        pts = [(s * .7, s * .2), (s * .3, s * .5), (s * .7, s * .8)] if left else [(s * .3, s * .2), (s * .7, s * .5), (s * .3, s * .8)]
        dd.polygon(pts, fill=ORG); return im
    return ss(draw, 48)


arrow(True).save(OUT + "/icons/arrow_left.png"); arrow(False).save(OUT + "/icons/arrow_right.png")


# ── выделение ────────────────────────────────────────────────────────────────
def selection(s):
    def draw(S):
        im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        dd.polygon(hexpts(S / 2, S / 2, S / 2 * 0.98), fill=(255, 106, 19, 70), outline=(255, 106, 19, 255), width=round(S * 0.022))
        dd.polygon(hexpts(S / 2, S / 2, S / 2 * 0.88), outline=(220, 38, 48, 200), width=round(S * 0.01))
        return im
    im = ss(draw, s)
    glow = im.filter(ImageFilter.GaussianBlur(s * 0.02))
    return Image.alpha_composite(glow, im)


selection(288).save(OUT + "/selection_big.png"); selection(120).save(OUT + "/selection_small.png")

# ── шрифт: 96 глифов ASCII 32..126 + «?» для неизвестных, чёрный LA (rEFInd сам инвертирует на тёмном фоне)
fs = 30; f = font(MONO, fs)
cw = round(f.getlength("M")); ch = fs + 8
fim = Image.new("LA", (cw * 96, ch), (0, 0))
fd = ImageDraw.Draw(fim)
for i, code in enumerate(list(range(32, 127)) + [ord("?")]):
    fd.text((i * cw, 2), chr(code), font=f, fill=(0, 255))
fim.save(OUT + "/font.png")

# ── theme.conf ───────────────────────────────────────────────────────────────
open(OUT + "/theme.conf", "w").write("""# NERV // Asuka theme for rEFInd
icons_dir themes/nerv-asuka/icons
banner themes/nerv-asuka/banner.png
banner_scale fillscreen
selection_big themes/nerv-asuka/selection_big.png
selection_small themes/nerv-asuka/selection_small.png
font themes/nerv-asuka/font.png
big_icon_size 256
small_icon_size 96
hideui hints,badges
""")

# ── превью (примерная раскладка rEFInd, для глаз) ────────────────────────────
pv = Image.open(OUT + "/banner.png").convert("RGBA")
icons = ["os_asuka", "os_fallback", "os_grub"]; gap = 288 + 40
x0 = (W - (len(icons) * gap - 40)) // 2; y0 = round(H * 0.42)
pv.alpha_composite(Image.open(OUT + "/selection_big.png"), (x0, y0))
for i, n in enumerate(icons): pv.alpha_composite(Image.open(OUT + f"/icons/{n}.png"), (x0 + i * gap + 16, y0 + 16))
tools = ["func_reset", "func_shutdown", "func_firmware"]; tg = 120 + 24
tx0 = (W - (len(tools) * tg - 24)) // 2; ty = y0 + 288 + 110
for i, n in enumerate(tools): pv.alpha_composite(Image.open(OUT + f"/icons/{n}.png"), (tx0 + i * tg + 12, ty + 12))
lab = Image.eval(fim.getchannel("A"), lambda v: v)
txt = "Boot NERV // Asuka from boot"
row = Image.new("RGBA", (cw * len(txt), ch), (0, 0, 0, 0))
for i, c in enumerate(txt):
    gi = ord(c) - 32 if 32 <= ord(c) <= 126 else 95
    glyph = Image.new("RGBA", (cw, ch), (255, 255, 255, 255)); glyph.putalpha(lab.crop((gi * cw, 0, gi * cw + cw, ch)))
    row.alpha_composite(glyph, (i * cw, 0))
pv.alpha_composite(row, ((W - row.width) // 2, y0 + 288 + 40))
pv.convert("RGB").save(A + "/refind/preview.png")
print("ok", sorted(os.listdir(OUT)), sorted(os.listdir(OUT + "/icons")))

#!/usr/bin/env python3
"""Plymouth theme asuka-log: NERV/MAGI терминал с живыми логами systemd вместо полоски."""
import os, shutil, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

A = os.path.expanduser("~/.local/share/asuka-theme")
OUT = A + "/plymouth/asuka-log"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
F = os.path.expanduser("~/.local/share/fonts/nerv")
SER = F + "/ShipporiMinchoB1-ExtraBold.ttf"; OSW = F + "/Oswald[wght].ttf"
JP = F + "/NotoSansJP[wght].ttf"; MONO = F + "/ShareTechMono-Regular.ttf"
RED = (220, 38, 48, 255); ORG = (255, 106, 19, 255); DIM = (150, 110, 100, 255); CRM = (245, 226, 214, 255)
W, H = 2560, 1440

# общие с .script координаты (доли экрана)
PANEL = (0.055, 0.255, 0.545, 0.865)       # x0, y0, x1, y1 окна логов
BAR_X, BAR_Y, SEG_W, SEG_G, SEG_H, SEGS = 0.175, 0.905, 0.0125, 0.0035, 0.024, 20


def font(p, s, wght=None):
    f = ImageFont.truetype(p, s)
    if wght:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f


def px(fx, fy): return (round(fx * W), round(fy * H))


# ── фон ──────────────────────────────────────────────────────────────────────
bg = Image.open(A + "/img/wallhaven/wallhaven-jeyj5p.png").convert("RGBA").resize((W, H), Image.LANCZOS)
bg = bg.transform((W, H), Image.AFFINE, (1, 0, -0.06 * W, 0, 1, 0), fillcolor=(0, 0, 0, 255))  # Аску чуть правее
shade = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(shade)
for x in range(W):  # слева почти чёрное, к правому краю прозрачное
    u = x / W; a = 235 if u < 0.5 else max(0, int(235 * (1 - (u - 0.5) / 0.18)))
    sd.line([(x, 0), (x, H)], fill=a)
bg.alpha_composite(Image.merge("RGBA", (*[Image.new("L", (W, H), 0)] * 3, shade)))
d = ImageDraw.Draw(bg)

# гекс-сетка еле заметная
for row in range(0, 30):
    for col in range(0, 40):
        cx = col * 66 + (33 if row % 2 else 0); cy = row * 57
        if cx > W * 0.6: continue
        pts = [(cx + 30 * math.cos(math.radians(60 * k + 30)), cy + 30 * math.sin(math.radians(60 * k + 30))) for k in range(6)]
        d.polygon(pts, outline=(60, 10, 14, 255))

# сканлайны
for y in range(0, H, 4): d.line([(0, y), (W, y)], fill=(0, 0, 0, 60))

# шапка
d.text(px(0.055, 0.035), "NERV", font=font(SER, 120), fill=RED)
NX = px(0.055, 0)[0] + round(d.textlength("NERV", font=font(SER, 120))) + 36
d.text((NX, px(0, 0.052)[1]), "MAGI SYSTEM", font=font(OSW, 46, 600), fill=ORG)
d.text((NX, px(0, 0.052)[1] + 62), "EVA-02 // PILOT: SORYU ASUKA LANGLEY", font=font(OSW, 28, 400), fill=DIM)
d.line([px(0.055, 0.155), px(0.545, 0.155)], fill=RED, width=3)

# окно терминала
x0, y0 = px(PANEL[0], PANEL[1]); x1, y1 = px(PANEL[2], PANEL[3])
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
od.rectangle([x0, y0, x1, y1], fill=(8, 2, 3, 200))
bg.alpha_composite(ov)
d.rectangle([x0, y0, x1, y1], outline=RED, width=2)
for (cx, cy, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):  # уголки
    d.line([(cx, cy), (cx + 40 * sx, cy)], fill=ORG, width=6); d.line([(cx, cy), (cx, cy + 40 * sy)], fill=ORG, width=6)
d.rectangle([x0, y0 - 44, x0 + 420, y0], fill=RED)
d.text((x0 + 14, y0 - 42), "TERMINAL // BOOT LOG", font=font(OSW, 30, 600), fill=(0, 0, 0, 255))
d.text((x1 - 260, y0 - 44), "CASPER · BALTHASAR · MELCHIOR", font=font(OSW, 20, 300), fill=DIM)

# полоса синхронизации: пустые сегменты
d.text(px(0.055, BAR_Y - 0.004), "SYNC RATIO", font=font(OSW, 34, 600), fill=ORG)
for k in range(SEGS):
    sx = round((BAR_X + k * (SEG_W + SEG_G)) * W); sy = round(BAR_Y * H)
    d.rectangle([sx, sy, sx + round(SEG_W * W), sy + round(SEG_H * H)], outline=(110, 24, 28, 255), width=2)
d.text(px(0.055, 0.95), "GOD'S IN HIS HEAVEN. ALL'S RIGHT WITH THE WORLD.", font=font(OSW, 22, 300), fill=DIM)

# справа внизу — предупреждающие полосы и подпись
hz = Image.new("RGBA", (520, 56), (0, 0, 0, 0)); hd = ImageDraw.Draw(hz)
for i in range(-2, 20): hd.polygon([(i * 40, 56), (i * 40 + 20, 56), (i * 40 + 76, 0), (i * 40 + 56, 0)], fill=ORG)
bg.alpha_composite(hz, (W - 600, H - 120))
d.text((W - 600, H - 190), "EVA-02 // 弐号機", font=font(JP, 46, 800), fill=CRM)
bg.convert("RGB").save(OUT + "/background.png", optimize=True)

# ── мелкие спрайты ───────────────────────────────────────────────────────────
def seg(col):
    im = Image.new("RGBA", (32, 32), col); return im
seg(RED).save(OUT + "/seg-red.png"); seg(ORG).save(OUT + "/seg-orange.png"); seg((0, 230, 118, 255)).save(OUT + "/seg-green.png")


def label(txt, f, col, pad=6):
    b = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), txt, font=f)
    im = Image.new("RGBA", (b[2] + pad * 2, b[3] + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad, pad), txt, font=f, fill=col); return im


label("▌ 起動シーケンス — BOOT SEQUENCE", font(JP, 34, 700), CRM).save(OUT + "/sub-boot.png")
label("▌ 活動停止 — SHUTDOWN SEQUENCE", font(JP, 34, 700), RED).save(OUT + "/sub-shutdown.png")
label("▌ 再起動 — REBOOT SEQUENCE", font(JP, 34, 700), ORG).save(OUT + "/sub-reboot.png")
label("あんたバカぁ？ パスワードは？", font(JP, 30, 700), RED).save(OUT + "/ask-pass.png")

# ── .plymouth ────────────────────────────────────────────────────────────────
open(OUT + "/asuka-log.plymouth", "w").write(
    "[Plymouth Theme]\nName=asuka-log\nDescription=NERV // Asuka MAGI boot log\nModuleName=script\n"
    "Font=Oswald 20\nMonospaceFont=Share Tech Mono 20\n\n"
    "[script]\nImageDir=/usr/share/plymouth/themes/asuka-log\nScriptFile=/usr/share/plymouth/themes/asuka-log/asuka-log.script\n")
shutil.copy(A + "/plymouth-src/asuka-log.script", OUT + "/asuka-log.script")
print("ok:", sorted(os.listdir(OUT)), os.path.getsize(OUT + "/background.png") // 1024, "KiB bg")

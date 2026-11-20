"""rice/build/lib.py — генераторы частей темы из одного описания SPEC (см. themes/*/spec.py).

Каждая функция пишет в каталог темы:
  out/   — пользовательские файлы (color-schemes, konsole, icons, sounds, look-and-feel, ...)
  system/— то, что ставит root-хелпер (plymouth, grub, refind, sddm, avatar)
"""
import os, re, json, math, shutil, subprocess, colorsys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance

HOME = os.path.expanduser("~")
RICE = HOME + "/.local/share/rice"
BUILD = RICE + "/build"
ASUKA = HOME + "/.local/share/asuka-theme"
W, H = 2560, 1440


# ── мелочи ───────────────────────────────────────────────────────────────────
def rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def rgba(h, a=255): return rgb(h) + (a,)
def csv(h): return ",".join(map(str, rgb(h)))
def flt(h): return ", ".join(f"{c / 255:.3f}" for c in rgb(h))
def mix(a, b, t): A, B = rgb(a), rgb(b); return "#%02x%02x%02x" % tuple(round(A[i] + (B[i] - A[i]) * t) for i in range(3))


def font(path, size, wght=None):
    f = ImageFont.truetype(path, size)
    if wght:
        try: f.set_variation_by_axes([wght] if not isinstance(wght, list) else wght)
        except Exception: pass
    return f


def F(S, key, size):
    """шрифт темы: S['fonts'][key] = (path, weight|None)"""
    p, w = S["fonts"][key]; return font(p, size, w)


def mkdir(p): os.makedirs(p, exist_ok=True); return p
def fresh(p): shutil.rmtree(p, ignore_errors=True); os.makedirs(p); return p
def T(S, *a): return os.path.join(S["dir"], *a)


def cover(path, size, focus=(0.5, 0.5), crop=None):
    """открыть картинку, обрезать (crop=(l,t,r,b) в долях) и заполнить size с точкой фокуса"""
    im = Image.open(path).convert("RGBA")
    if crop:
        l, t, r, b = crop; im = im.crop((round(l * im.width), round(t * im.height), round(r * im.width), round(b * im.height)))
    return ImageOps.fit(im, size, Image.LANCZOS, centering=focus)


def hexpts(cx, cy, r, rot=30):
    return [(cx + r * math.cos(math.radians(60 * k + rot)), cy + r * math.sin(math.radians(60 * k + rot))) for k in range(6)]


def paw(d, cx, cy, r, fill):
    """кошачья лапка: подушечка + 4 пальчика"""
    d.ellipse([cx - r, cy - r * .55, cx + r, cy + r * .95], fill=fill)
    for dx, dy, s in ((-1.05, -1.0, .42), (-.38, -1.55, .42), (.38, -1.55, .42), (1.05, -1.0, .42)):
        x, y = cx + dx * r, cy + dy * r; q = s * r * 1.15
        d.ellipse([x - q * .85, y - q, x + q * .85, y + q], fill=fill)


def label(txt, f, col, pad=6):
    b = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), txt, font=f)
    im = Image.new("RGBA", (b[2] + pad * 2, b[3] + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad, pad), txt, font=f, fill=col); return im


def ss(fn, size, k=4):
    return fn(size * k).resize((size, size), Image.LANCZOS)


# ── KDE color scheme / Konsole / kitty ───────────────────────────────────────
def kde_colors(S):
    P = S["pal"]; name = S["kde_colors"]
    def grp(bg, alt, fg=P["fg"]):
        return (f"BackgroundAlternate={csv(alt)}\nBackgroundNormal={csv(bg)}\nDecorationFocus={csv(P['accent'])}\n"
                f"DecorationHover={csv(P['accent2'])}\nForegroundActive={csv(P['accent'])}\nForegroundInactive={csv(P['dim'])}\n"
                f"ForegroundLink={csv(P['link'])}\nForegroundNegative={csv(P['neg'])}\nForegroundNeutral={csv(P['neu'])}\n"
                f"ForegroundNormal={csv(fg)}\nForegroundPositive={csv(P['pos'])}\nForegroundVisited={csv(P['visited'])}\n")
    bg, bg2, sf = P["bg"], P["bg2"], P["surface"]
    sel = P["accent"]
    out = f"""[General]
ColorScheme={name}
Name={S['name']}
shadeSortColumn=true

[KDE]
contrast=6

[ColorEffects:Disabled]
Color={csv(bg)}
ColorAmount=0
ColorEffect=0
ContrastAmount=0.65
ContrastEffect=1
IntensityAmount=0.1
IntensityEffect=2

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color={csv(bg)}
ColorAmount=0.025
ColorEffect=2
ContrastAmount=0.1
ContrastEffect=2
Enable=false
IntensityAmount=0
IntensityEffect=0

[Colors:Button]
{grp(sf, mix(sf, sel, .25))}
[Colors:Complementary]
{grp(bg, bg2)}
[Colors:Header]
{grp(bg2, bg2)}
[Colors:Header][Inactive]
{grp(bg, bg)}
[Colors:Selection]
{grp(sel, mix(sel, bg, .3), P['sel_fg'])}
[Colors:Tooltip]
{grp(bg2, bg)}
[Colors:View]
{grp(bg, bg2)}
[Colors:Window]
{grp(bg2, sf)}
[WM]
activeBackground={csv(bg2)}
activeBlend={csv(P['accent'])}
activeForeground={csv(P['fg'])}
inactiveBackground={csv(bg)}
inactiveBlend={csv(P['dim'])}
inactiveForeground={csv(P['dim'])}
"""
    p = mkdir(T(S, "out", "color-schemes")) + f"/{name}.colors"; open(p, "w").write(out); return p


def terminal(S):
    P = S["pal"]; A = S["ansi"]  # 16 цветов
    d = mkdir(T(S, "out", "konsole"))
    cs = S["konsole_scheme"]
    lines = [f"[Background]\nColor={csv(P['term_bg'])}\n", f"[BackgroundIntense]\nColor={csv(mix(P['term_bg'], P['fg'], .06))}\n",
             f"[BackgroundFaint]\nColor={csv(P['term_bg'])}\n", f"[Foreground]\nColor={csv(P['fg'])}\n",
             f"[ForegroundIntense]\nColor={csv(P['accent'])}\n", f"[ForegroundFaint]\nColor={csv(P['dim'])}\n"]
    for i in range(8):
        lines.append(f"[Color{i}]\nColor={csv(A[i])}\n"); lines.append(f"[Color{i}Intense]\nColor={csv(A[i + 8])}\n")
        lines.append(f"[Color{i}Faint]\nColor={csv(mix(A[i], P['term_bg'], .35))}\n")
    lines.append(f"[General]\nAnchor=0.5,0.5\nBlur=true\nColorRandomization=false\nDescription={S['name']}\nFillStyle=Tile\nOpacity={S.get('term_opacity', 0.92)}\nWallpaper=\n")
    open(f"{d}/{cs}.colorscheme", "w").write("\n".join(lines))
    prof = S["konsole_profile"]
    open(f"{d}/{prof}.profile", "w").write(f"""[Appearance]
ColorScheme={cs}
Font={S.get('term_font', 'JetBrainsMono Nerd Font,11,-1,5,500,0,0,0,0,0,0,0,0,0,0,1')}

[Cursor Options]
CursorShape={S.get('cursor_shape', 1)}
CustomCursorColor={csv(P['accent'])}
UseCustomCursorColor=true

[General]
Name={prof}
Parent=FALLBACK/
TerminalMargin=8

[Scrolling]
HistorySize=999999
""")
    k = [f"# {S['name']}", f"background {P['term_bg']}", f"foreground {P['fg']}", f"cursor {P['accent']}",
         f"cursor_text_color {P['term_bg']}", f"selection_background {P['accent']}", f"selection_foreground {P['sel_fg']}",
         f"url_color {P['link']}", f"active_border_color {P['accent']}", f"inactive_border_color {P['surface']}",
         f"active_tab_background {P['accent']}", f"active_tab_foreground {P['sel_fg']}",
         f"inactive_tab_background {P['bg2']}", f"inactive_tab_foreground {P['dim']}", f"tab_bar_background {P['term_bg']}"]
    k += [f"color{i} {A[i]}" for i in range(16)]
    open(T(S, "out", "kitty.conf"), "w").write("\n".join(k) + "\n")


def prompts(S):
    """bash/fish приглашения + приветствие fastfetch. S['prompt'] = список (текст, hex|None, bold)"""
    pr = S["prompt"]
    def bash_seg(t, c, b):
        if c is None: return t
        r, g, bl = rgb(c); return f"\\[\\e[{'1;' if b else ''}38;2;{r};{g};{bl}m\\]{t}"
    def fish_seg(t, c, b):
        if c is None: return t
        return f"(set_color {'-o ' if b else ''}{c.lstrip('#')})\"{t}\""
    ok, bad = S["prompt_status"]
    line1 = "".join(bash_seg(*x) for x in pr["line1"])
    arrow = "".join(bash_seg(*x) for x in pr["arrow"])
    bash = f"""# {S['name']} — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && {{ export RICE_GREETED=1; fastfetch; }}
__rice_ps1() {{
  local s=$? r='\\[\\e[0m\\]'
  local st="{bash_seg(ok[0], ok[1], False)}"; (( s != 0 )) && st="{bash_seg(bad[0] + ' [$s]', bad[1], True)}"
  local wd='\\w'
  PS1="\\n{line1}${{st}}{bash_seg(pr['tail'][0], pr['tail'][1], False)}${{r}}\\n{arrow}${{r}} "
}}
PROMPT_COMMAND=__rice_ps1
"""
    open(T(S, "prompt.bash"), "w").write(bash.replace("{WD}", "${wd}").replace("{USER}", "\\u"))
    l1 = "".join(fish_seg(*x) for x in pr["line1"]).replace("{WD}", "\"(prompt_pwd)\"").replace("{USER}", "\"$USER\"")
    l1 = l1.replace('""', '')
    fish = f"""# {S['name']} — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st {fish_seg(ok[0], ok[1], False)}
    test $s -ne 0; and set st {fish_seg(bad[0] + ' [$s]', bad[1], True)}
    echo
    echo {l1}$st{fish_seg(pr['tail'][0], pr['tail'][1], False)}
    echo -n {''.join(fish_seg(*x) for x in pr['arrow'])}" "(set_color normal)
end
"""
    open(T(S, "prompt.fish"), "w").write(fish)


def fastfetch(S, logo_img):
    P = S["pal"]; ff = S["fastfetch"]
    logo_img.save(T(S, "fastfetch-logo.png"))
    mods = ["break"] + [{"type": "custom", "format": f} for f in ff["header"]]
    for typ, key in ff["keys"]: mods.append({"type": typ, "key": key})
    mods += ["break", {"type": "colors", "symbol": "circle"}]
    cfg = {"$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
           "logo": {"source": T(S, "fastfetch-logo.png"), "type": "kitty", "height": 16, "padding": {"top": 1, "right": 3}},
           "display": {"separator": "  ", "color": {"keys": ff["key_color"], "title": ff["title_color"]}},
           "modules": mods}
    open(T(S, "fastfetch.jsonc"), "w").write(f"// {S['name']} — fastfetch (rice)\n" + json.dumps(cfg, ensure_ascii=False, indent=2))


# ── курсор ───────────────────────────────────────────────────────────────────
CUR_ALIASES = None
def cursor(S, shapes):
    """shapes: {name: ([svg frames], (hx,hy))}; алиасы — как у NERV-Asuka"""
    global CUR_ALIASES
    if CUR_ALIASES is None:
        src = open(ASUKA + "/cursor-src/build.py").read()
        ns = {}; exec(src[src.index("aliases={"):src.index("os.makedirs(OUT")], ns); CUR_ALIASES = ns["aliases"]
    name = S["cursor"]; out = fresh(T(S, "out", "icons", name)); cdir = mkdir(out + "/cursors")
    tmp = fresh(T(S, "build-tmp", "cursor"))
    for cname, (frames, (hx, hy)) in shapes.items():
        cfg = []
        for fi, s in enumerate(frames):
            sp = f"{tmp}/{cname}_{fi}.svg"; open(sp, "w").write(s)
            for sz in (24, 32, 48, 64, 96):
                png = f"{tmp}/{cname}_{fi}_{sz}.png"
                subprocess.run(["rsvg-convert", "-w", str(sz), "-h", str(sz), sp, "-o", png], check=True)
                cfg.append(f"{sz} {round(hx * sz / 32)} {round(hy * sz / 32)} {png}" + (" 60" if len(frames) > 1 else ""))
        open(f"{tmp}/{cname}.cfg", "w").write("\n".join(cfg) + "\n")
        subprocess.run(["xcursorgen", f"{tmp}/{cname}.cfg", f"{cdir}/{cname}"], check=True)
        for al in CUR_ALIASES.get(cname, []):
            if al != cname and not os.path.lexists(f"{cdir}/{al}"): os.symlink(cname, f"{cdir}/{al}")
    open(out + "/index.theme", "w").write(f"[Icon Theme]\nName={name}\nComment={S['name']} cursor\nInherits=breeze_cursors\n")
    open(out + "/cursor.theme", "w").write(f"[Icon Theme]\nInherits={name}\n")
    subprocess.run(["rsvg-convert", "-w", "128", f"{tmp}/default_0.svg", "-o", T(S, "build-tmp", "cursor-preview.png")])


# ── звуки (синтез) ───────────────────────────────────────────────────────────
def sounds(S, recipes):
    """recipes: {event: [(freq_hz, dur_s, wave, vol, glide_to_hz|None), ...]} — ноты подряд"""
    import numpy as np
    sid = S["sounds"]; d = fresh(T(S, "out", "sounds", sid)); st = mkdir(d + "/stereo")
    sr = 48000; tmp = mkdir(T(S, "build-tmp", "snd"))
    for ev, notes in recipes.items():
        chunks = []
        for f0, dur, wave, vol, f1 in notes:
            n = int(sr * dur); t = np.arange(n) / sr
            f = np.full(n, float(f0)) if not f1 else np.geomspace(f0, f1, n)
            ph = 2 * np.pi * np.cumsum(f) / sr
            if wave == "sine": y = np.sin(ph)
            elif wave == "tri": y = 2 / np.pi * np.arcsin(np.sin(ph))
            elif wave == "square": y = np.sign(np.sin(ph)) * .5
            elif wave == "bell": y = np.sin(ph) + .35 * np.sin(2.76 * ph) + .2 * np.sin(5.4 * ph)
            elif wave == "rest": y = np.zeros(n)
            else: y = np.sin(ph)
            env = np.minimum(1, t / 0.006) * np.exp(-t * (3.2 / dur))
            chunks.append(y * env * vol)
        y = np.concatenate(chunks + [np.zeros(int(sr * .05))])
        # лёгкое эхо
        e = np.zeros(len(y) + int(sr * .12)); e[:len(y)] += y; e[int(sr * .12):] += y * .25
        e = np.clip(e / max(1e-9, np.abs(e).max()) * .8, -1, 1)
        raw = f"{tmp}/{ev}.f32"; (np.stack([e, e], 1).astype("float32")).tofile(raw)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", raw,
                        "-c:a", "libvorbis", "-q:a", "5", f"{st}/{ev}.oga"], check=True)
    open(d + "/index.theme", "w").write(f"[Sound Theme]\nName={S['name']}\nComment={S['name']} sounds (rice)\n"
                                         "Inherits=ocean,freedesktop\nDirectories=stereo\n\n[stereo]\nOutputProfile=stereo\n")


# ── сплэш (ksplash) ──────────────────────────────────────────────────────────
def splash(S, media, kind="gif"):
    """media — путь к gif/png для рамки по центру"""
    P = S["pal"]; sp = S["splash"]; sid = sp["id"]
    d = fresh(T(S, "out", "look-and-feel", sid)); c = mkdir(d + "/contents/splash/images")
    ext = os.path.splitext(media)[1]; shutil.copy(media, f"{c}/media{ext}")
    json.dump({"KPackageStructure": "Plasma/LookAndFeel/Splash",
               "KPlugin": {"Authors": [{"Name": "femboychik"}], "Category": "", "Description": f"{S['name']} splash",
                           "Id": sid, "License": "GPLv3", "Name": S["name"]},
               "Keywords": "Desktop;Workspace;Appearance;Look and Feel;Splash;", "X-Plasma-APIVersion": "2"},
              open(d + "/metadata.json", "w"), ensure_ascii=False, indent=4)
    msgs = json.dumps(sp["messages"], ensure_ascii=False)
    elem = "AnimatedImage" if ext == ".gif" else "Image"
    qml = f"""import QtQuick
import QtQuick.Window

Rectangle {{
    id: root
    color: "{P['bg']}"
    property int stage
    onStageChanged: if (stage == 1) introAnimation.running = true
    readonly property var messages: {msgs}

    Item {{
        id: content
        anchors.fill: parent
        opacity: 0

        Text {{
            id: title
            text: "{sp['title']}"
            font.family: "{sp['title_font']}"
            font.weight: Font.Bold
            font.pixelSize: Math.round(root.height * 0.075)
            color: "{P['accent']}"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: frame.top
            anchors.bottomMargin: root.height * 0.02
        }}
        Rectangle {{
            id: frame
            width: Math.min(root.width * 0.5, 900)
            height: width * 9 / 16
            anchors.centerIn: parent
            color: "transparent"
            border.color: "{P['accent2']}"
            border.width: 3
            radius: {sp.get('radius', 0)}
            clip: true
            {elem} {{
                anchors.fill: parent
                anchors.margins: 3
                source: "images/media{ext}"
                fillMode: Image.PreserveAspectCrop
                smooth: true
                {'playing: true' if ext == '.gif' else ''}
            }}
        }}
        Text {{
            id: sub
            text: "{sp['subtitle']}"
            font.family: "{sp['font']}"
            font.pixelSize: Math.round(root.height * 0.022)
            color: "{P['accent2']}"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: frame.bottom
            anchors.topMargin: root.height * 0.025
        }}
        Rectangle {{
            id: barBg
            width: frame.width
            height: 6
            radius: 3
            color: "{P['surface']}"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: sub.bottom
            anchors.topMargin: root.height * 0.02
            Rectangle {{
                height: parent.height
                radius: 3
                width: parent.width * Math.min(1, root.stage / 6)
                gradient: Gradient {{
                    orientation: Gradient.Horizontal
                    GradientStop {{ position: 0; color: "{P['accent']}" }}
                    GradientStop {{ position: 1; color: "{P['accent2']}" }}
                }}
                Behavior on width {{ NumberAnimation {{ duration: 400; easing.type: Easing.OutQuad }} }}
            }}
        }}
        Text {{
            text: root.messages[Math.max(0, Math.min(root.messages.length - 1, root.stage - 1))]
            font.family: "{sp['font']}"
            font.pixelSize: Math.round(root.height * 0.018)
            color: "{P['dim']}"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: barBg.bottom
            anchors.topMargin: root.height * 0.012
        }}
    }}
    OpacityAnimator {{
        id: introAnimation
        running: false
        target: content
        from: 0; to: 1
        duration: 600
        easing.type: Easing.InOutQuad
    }}
}}
"""
    open(d + "/contents/splash/Splash.qml", "w").write(qml)


# ── Plymouth: терминал с логами ──────────────────────────────────────────────
PANEL = (0.055, 0.255, 0.545, 0.865)
BAR_X, BAR_Y, SEG_W, SEG_G, SEG_H, SEGS = 0.175, 0.905, 0.0125, 0.0035, 0.024, 20


def plymouth_log(S, bg):
    """bg — готовый фон W×H (RGBA) с артом справа; тут дорисовываем шапку/окно/полосу."""
    P = S["pal"]; pl = S["plymouth"]; name = pl["name"]
    out = fresh(T(S, "system", "plymouth", name))
    bg = bg.copy(); d = ImageDraw.Draw(bg)
    px = lambda fx, fy: (round(fx * W), round(fy * H))
    # шапка
    tf = F(S, "title", pl.get("title_size", 120))
    d.text(px(0.055, 0.035), pl["title"], font=tf, fill=rgba(P["accent"]))
    nx = px(0.055, 0)[0] + round(d.textlength(pl["title"], font=tf)) + 36
    d.text((nx, px(0, 0.052)[1]), pl["head1"], font=F(S, "ui_bold", 46), fill=rgba(P["accent2"]))
    d.text((nx, px(0, 0.052)[1] + 62), pl["head2"], font=F(S, "ui", 28), fill=rgba(P["dim"]))
    d.line([px(0.055, 0.155), px(0.545, 0.155)], fill=rgba(P["accent"]), width=3)
    # окно
    x0, y0 = px(PANEL[0], PANEL[1]); x1, y1 = px(PANEL[2], PANEL[3])
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    rad = pl.get("radius", 0)
    od.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=rgba(P["term_bg"], 205)); bg.alpha_composite(ov)
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad, outline=rgba(P["accent"]), width=2)
    if not rad:
        for (cx, cy, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
            d.line([(cx, cy), (cx + 40 * sx, cy)], fill=rgba(P["accent2"]), width=6)
            d.line([(cx, cy), (cx, cy + 40 * sy)], fill=rgba(P["accent2"]), width=6)
    tabf = F(S, "ui_bold", 30); tw = round(d.textlength(pl["tab"], font=tabf)) + 28
    d.rounded_rectangle([x0, y0 - 44, x0 + tw, y0 + (rad and 2)], radius=min(rad, 10), fill=rgba(P["accent"]))
    d.text((x0 + 14, y0 - 42), pl["tab"], font=tabf, fill=rgba(P["term_bg"]))
    sf = F(S, "ui", 20); d.text((x1 - d.textlength(pl["tab_right"], font=sf), y0 - 34), pl["tab_right"], font=sf, fill=rgba(P["dim"]))
    # полоса
    d.text(px(0.055, BAR_Y - 0.004), pl["bar"], font=F(S, "ui_bold", 34), fill=rgba(P["accent2"]))
    for k in range(SEGS):
        sx = round((BAR_X + k * (SEG_W + SEG_G)) * W); sy = round(BAR_Y * H)
        box = [sx, sy, sx + round(SEG_W * W), sy + round(SEG_H * H)]
        d.rounded_rectangle(box, radius=pl.get("seg_radius", 0), outline=rgba(mix(P["accent"], P["bg"], .45)), width=2)
    d.text(px(0.055, 0.95), pl["footer"], font=F(S, "ui", 22), fill=rgba(P["dim"]))
    bg.convert("RGB").save(out + "/background.png", optimize=True)
    for fn, col in (("seg-red", pl["seg"][0]), ("seg-orange", pl["seg"][1]), ("seg-green", pl["seg"][2])):
        Image.new("RGBA", (32, 32), rgba(col)).save(f"{out}/{fn}.png")
    jf = F(S, "jp", 34)
    for mode, (txt, col) in pl["sub"].items():
        label(txt, jf, rgba(col)).save(f"{out}/sub-{mode}.png")
    label(pl["ask"], F(S, "jp", 30), rgba(P["accent"])).save(out + "/ask-pass.png")
    # скрипт из шаблона
    s = open(BUILD + "/plymouth_log.script.tmpl").read()
    names = pl["names"]; tags = pl["tags"]
    rep = {"ID": name, "TAG_W": max(tags.values(), key=len), "NAME_W": max(names, key=len),
           "NAME0": names[0], "NAME1": names[1], "NAME2": names[2],
           "TAG_OK": tags["ok"], "TAG_AMB": tags["amb"], "TAG_WARN": tags["warn"],
           "C_DIM": flt(P["dim"]), "C_OK": flt(pl["c_ok"]), "C_AMB": flt(pl["c_amb"]), "C_WARN": flt(P["neg"]),
           "C_NAME": flt(pl["c_name"]), "C_TEXT": flt(pl["c_text"]), "C_ACCENT": flt(P["accent"]),
           "STOP_LINE": pl["stop"], "FSIZE_DIV": str(pl.get("fsize_div", 62)),
           "AMBIENT": "\n".join(f'amb[{i}] = "{a}";' for i, a in enumerate(pl["ambient"])) + f"\nnamb = {len(pl['ambient'])};"}
    for k_, v in rep.items(): s = s.replace("{{" + k_ + "}}", v)
    assert "{{" not in s
    open(f"{out}/{name}.script", "w").write(s)
    open(f"{out}/{name}.plymouth", "w").write(
        f"[Plymouth Theme]\nName={name}\nDescription={S['name']} boot log\nModuleName=script\n"
        f"Font={pl['font_family']} 20\nMonospaceFont={pl['mono_family']} 20\n\n"
        f"[script]\nImageDir=/usr/share/plymouth/themes/{name}\nScriptFile=/usr/share/plymouth/themes/{name}/{name}.script\n")
    return out


# ── GRUB ─────────────────────────────────────────────────────────────────────
def grub(S, bg):
    """bg — фон W×H; меню слева (как у NERV-Asuka). Шрифты .pf2 генерируются grub-mkfont."""
    P = S["pal"]; g = S["grub"]; name = g["name"]
    out = fresh(T(S, "system", "grub", name))
    if os.path.isdir(ASUKA + "/grub/NERV-Asuka/icons"): shutil.copytree(ASUKA + "/grub/NERV-Asuka/icons", out + "/icons")
    shutil.copy(ASUKA + "/grub/NERV-Asuka/terminus-ttf-16.pf2", out)
    fonts = {}
    for key, size in (("title", 96), ("ui", 22), ("menu", 24)):
        path = g["fonts"][key]; fam = f"Rice{key.capitalize()}"
        fn = f"{out}/{fam}_{size}.pf2"
        used = set(g["title"] + "".join(l["text"] for l in g["labels"]))
        extra = ",".join(f"0x{ord(c):x}-0x{ord(c):x}" for c in sorted(used) if ord(c) > 0x4ff and not 0x2010 <= ord(c) <= 0x2027)
        rng = "0x20-0x7e,0xa0-0xff,0x400-0x4ff,0x2010-0x2027,0x2190-0x21ff,0x25a0-0x25ff" + ("," + extra if extra else "")
        subprocess.run(["grub-mkfont", "-s", str(size), "-n", fam, "-r", rng, "-o", fn, path], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        fonts[key] = f"{fam} Regular {size}"
    bg.convert("RGB").save(out + "/background.png", optimize=True)
    # подсветка пункта
    hl = Image.new("RGBA", (900, 50), (0, 0, 0, 0)); hd = ImageDraw.Draw(hl)
    hd.rounded_rectangle([0, 0, 899, 49], radius=g.get("radius", 0), fill=rgba(P["accent"], 90), outline=rgba(P["accent"]), width=2)
    hl.save(out + "/highlight_c.png")
    Image.new("RGBA", (400, 31), rgba(P["accent"])).save(out + "/progress_c.png")
    labels = "".join(f"""
+ label {{
  font = "{fonts[l.get('font', 'ui')]}"
  left = {l['left']}
  top = {l['top']}
  width = 60%
  color = "{l['color']}"
  text = "{l['text']}"
}}
""" for l in g["labels"])
    open(out + "/theme.txt", "w").write(f"""# {S['name']} GRUB theme (rice)
title-text: ""
desktop-image: "background.png"
desktop-color: "{P['bg']}"
terminal-font: "Terminus (TTF) Regular 16"
terminal-left: "0"
terminal-top: "0"
terminal-width: "100%"
terminal-height: "100%"
terminal-border: "0"

+ boot_menu {{
  left = 8%
  width = 42%
  top = 32%
  height = 42%
  item_font = "{fonts['menu']}"
  item_color = "{g['item']}"
  selected_item_font = "{fonts['menu']}"
  selected_item_color = "{g['item_sel']}"
  icon_width = 24
  icon_height = 24
  item_height = 38
  item_padding = 20
  item_icon_space = 16
  item_spacing = 6
  menu_pixmap_style = "no_*.png"
  selected_item_pixmap_style = "highlight_*.png"
}}

+ progress_bar {{
  left = 0%
  top = 100%-30
  width = 100%
  height = 30
  id = "__timeout__"
  text = "@TIMEOUT_NOTIFICATION_LONG@"
  font = "{fonts['menu']}"
  text_color = "{P['fg']}"
  fg_color = "{P['accent']}"
  bg_color = "{P['bg2']}"
  highlight_style = "progress_*.png"
}}

+ label {{
  font = "{fonts['title']}"
  left = 8%
  top = 8%
  width = 60%
  color = "{P['accent']}"
  text = "{g['title']}"
}}
{labels}""")
    return out


# ── rEFInd ───────────────────────────────────────────────────────────────────
def refind(S, banner, entries):
    """entries: {icon_name: (photo RGBA|None, tag, color_hex, gray)}"""
    P = S["pal"]; r = S["refind"]; name = r["name"]
    out = fresh(T(S, "system", "refind", name)); mkdir(out + "/icons")
    banner.convert("RGB").save(out + "/banner.png", optimize=True)
    shape = r.get("shape", "hex")
    def mask(s):
        m = Image.new("L", (s, s), 0); dd = ImageDraw.Draw(m)
        if shape == "hex": dd.polygon(hexpts(s / 2, s / 2, s / 2), fill=255)
        elif shape == "square": dd.rectangle([0, 0, s - 1, s - 1], fill=255)
        else: dd.ellipse([0, 0, s - 1, s - 1], fill=255)
        return m
    def outline(dd, s, r_, **kw):
        if shape == "hex": dd.polygon(hexpts(s / 2, s / 2, r_), **kw)
        elif shape == "square": dd.rectangle([s / 2 - r_, s / 2 - r_, s / 2 + r_, s / 2 + r_], **kw)
        else: dd.ellipse([s / 2 - r_, s / 2 - r_, s / 2 + r_, s / 2 + r_], **kw)
    def os_icon(photo, tag, col, gray):
        def draw(s):
            im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
            outline(dd, s, s / 2, fill=rgba(col))
            inner = round(s * 0.88); off = (s - inner) // 2
            if photo is not None:
                p = ImageOps.fit(photo, (inner, inner))
                if gray: p = ImageEnhance.Brightness(ImageOps.grayscale(p).convert("RGBA")).enhance(.7)
                im.paste(p, (off, off), mask(inner))
            else:
                ii = Image.new("RGBA", (inner, inner), rgba(P["bg"])); im.paste(ii, (off, off), mask(inner))
            bh = round(s * .16); by = round(s * .66)
            dd.rounded_rectangle([round(s * .14), by, round(s * .86), by + bh], radius=bh // 3 if shape != "hex" else 0, fill=(0, 0, 0, 215))
            f = F(S, "ui_bold", round(bh * .72)); tw = dd.textlength(tag, font=f)
            dd.text(((s - tw) / 2, by + bh * .04), tag, font=f, fill=rgba(col))
            return im
        return ss(draw, 256)
    for fn, (photo, tag, col, gray) in entries.items():
        os_icon(photo, tag, col, gray).save(f"{out}/icons/{fn}.png")
    def tool(kind):
        def draw(s):
            im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
            outline(dd, s, s / 2, fill=rgba(P["bg"], 235), outline=rgba(P["accent2"]), width=round(s * .05))
            c = s / 2; rr = s * .22; w = round(s * .07)
            if kind == "shutdown":
                dd.arc([c - rr, c - rr, c + rr, c + rr], -60, 240, fill=rgba(P["accent"]), width=w)
                dd.line([(c, c - rr * 1.25), (c, c)], fill=rgba(P["accent"]), width=w)
            elif kind == "reset":
                dd.arc([c - rr, c - rr, c + rr, c + rr], 30, 330, fill=rgba(P["accent2"]), width=w)
                ax, ay = c + rr * math.cos(math.radians(330)), c + rr * math.sin(math.radians(330))
                dd.polygon([(ax - s * .09, ay - s * .02), (ax + s * .09, ay - s * .02), (ax, ay + s * .1)], fill=rgba(P["accent2"]))
            elif kind == "firmware":
                f = F(S, "ui_bold", round(s * .22)); tw = dd.textlength("BIOS", font=f)
                dd.text((c - tw / 2, c - s * .16), "BIOS", font=f, fill=rgba(P["fg"]))
            elif kind == "about":
                paw(dd, c, c + s * .06, s * .14, rgba(P["accent"]))
            return im
        return ss(draw, 96)
    for k_ in ("shutdown", "reset", "firmware", "about"): tool(k_).save(f"{out}/icons/func_{k_}.png")
    for left in (True, False):
        def draw(s, left=left):
            im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
            pts = [(s * .7, s * .2), (s * .3, s * .5), (s * .7, s * .8)] if left else [(s * .3, s * .2), (s * .7, s * .5), (s * .3, s * .8)]
            dd.polygon(pts, fill=rgba(P["accent2"])); return im
        ss(draw, 48).save(f"{out}/icons/arrow_{'left' if left else 'right'}.png")
    def sel(sz):
        def draw(Sz):
            im = Image.new("RGBA", (Sz, Sz), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
            outline(dd, Sz, Sz / 2 * .98, fill=rgba(P["accent"], 70), outline=rgba(P["accent"]), width=round(Sz * .022))
            outline(dd, Sz, Sz / 2 * .88, outline=rgba(P["accent2"], 200), width=round(Sz * .01))
            return im
        im = ss(draw, sz); return Image.alpha_composite(im.filter(ImageFilter.GaussianBlur(sz * .02)), im)
    sel(288).save(out + "/selection_big.png"); sel(120).save(out + "/selection_small.png")
    mf = font(r["font"], 30); cw = round(mf.getlength("M")); ch = 38
    fim = Image.new("LA", (cw * 96, ch), (0, 0)); fd = ImageDraw.Draw(fim)
    for i, code in enumerate(list(range(32, 127)) + [ord("?")]): fd.text((i * cw, 2), chr(code), font=mf, fill=(0, 255))
    fim.save(out + "/font.png")
    open(out + "/theme.conf", "w").write(f"""# {S['name']} theme for rEFInd (rice)
icons_dir themes/{name}/icons
banner themes/{name}/banner.png
banner_scale fillscreen
selection_big themes/{name}/selection_big.png
selection_small themes/{name}/selection_small.png
font themes/{name}/font.png
big_icon_size 256
small_icon_size 96
hideui hints,badges
""")
    # превью
    pv = banner.convert("RGBA").copy(); icons = list(entries)[:3]; gap = 328
    x0 = (W - (len(icons) * gap - 40)) // 2; y0 = round(H * .42)
    pv.alpha_composite(Image.open(out + "/selection_big.png"), (x0, y0))
    for i, n in enumerate(icons): pv.alpha_composite(Image.open(f"{out}/icons/{n}.png"), (x0 + i * gap + 16, y0 + 16))
    tx0 = (W - (3 * 144 - 24)) // 2
    for i, n in enumerate(("func_reset", "func_shutdown", "func_firmware")):
        pv.alpha_composite(Image.open(f"{out}/icons/{n}.png"), (tx0 + i * 144 + 12, y0 + 288 + 122))
    pv.convert("RGB").save(T(S, "build-tmp", "refind-preview.png"))
    return out


# ── SDDM (SilentSDDM, конфиг на базе nerv-asuka) ─────────────────────────────
def sddm(S, bg_media, placeholder):
    P = S["pal"]; sd = S["sddm"]; name = sd["name"]
    out = T(S, "system", "sddm", name); shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(ASUKA + "/sddm/nerv-asuka", out, ignore=shutil.ignore_patterns("backgrounds", "docs", "*.nix", "flake.lock"))
    mkdir(out + "/backgrounds")
    ext = os.path.splitext(bg_media)[1]
    shutil.copy(bg_media, f"{out}/backgrounds/bg{ext}"); shutil.copy(placeholder, f"{out}/backgrounds/bg.png") if ext != ".png" else None
    os.remove(f"{out}/configs/nerv-asuka.conf") if os.path.exists(f"{out}/configs/nerv-asuka.conf") else None
    conf = open(ASUKA + "/sddm/nerv-asuka/configs/nerv-asuka.conf").read()
    conf = conf.replace('animated-background-placeholder = asuka.png', 'animated-background-placeholder = bg.png')
    conf = conf.replace('background = "asuka.mp4"', f'background = "bg{ext}"')
    conf = re.sub(r'text = "PILOT AUTHENTICATION REQUIRED[^"]*"', f'text = "{sd["message"]}"', conf)
    conf = re.sub(r'text = "SYNCHRONIZING[^"]*"', f'text = "{sd["spinner"]}"', conf)
    conf = conf.replace('font-family = "RedHatDisplay"', f'font-family = "{sd.get("font", "RedHatDisplay")}"')
    conf = conf.replace('position = "right"\nmargin = 50', f'position = "{sd.get("position", "right")}"\nmargin = 50')
    # белые элементы → цвет темы
    conf = conf.replace('content-color = "#FFFFFF"', f'content-color = "{P["fg"]}"')
    conf = conf.replace('background-color = "#FFFFFF"\nbackground-opacity = 0.15', f'background-color = "{P["accent"]}"\nbackground-opacity = 0.22')
    conf = conf.replace('active-background-color = "#FFFFFF"', f'active-background-color = "{P["accent"]}"')
    conf = conf.replace('font-size = 70\nfont-weight = 900\ncolor = "#FFFFFF"', f'font-size = 70\nfont-weight = 900\ncolor = "{P["accent"]}"')
    open(f"{out}/configs/{name}.conf", "w").write(conf)
    md = open(ASUKA + "/sddm/nerv-asuka/metadata.desktop").read()
    md = md.replace("Name=NERV // Asuka", f"Name={S['name']}").replace("ConfigFile=configs/nerv-asuka.conf", f"ConfigFile=configs/{name}.conf")
    open(out + "/metadata.desktop", "w").write(md)
    return out


# ── живые обои: картинка + частицы/свечение → бесшовный mp4 ──────────────────
def live_wallpaper(S, base, out_mp4, particles, seconds=12, fps=24, size=(W, H), glow=None, poster=None, post=None, crf=20):
    """base — RGBA size; particles(draw, t01, frame_img) рисует слой; glow=(hex, amp) пульсирующее свечение"""
    import numpy as np
    tmp = fresh(T(S, "build-tmp", "frames"))
    n = seconds * fps
    for i in range(n):
        t = i / n
        fr = base.copy()
        if glow:
            col, amp = glow
            a = int(255 * amp * (0.5 + 0.5 * math.sin(2 * math.pi * t)))
            g = Image.new("RGBA", size, rgba(col, 0)); g.putalpha(Image.new("L", size, a))
            fr = Image.blend(fr, Image.alpha_composite(fr, g), 1)
        lay = Image.new("RGBA", size, (0, 0, 0, 0)); particles(ImageDraw.Draw(lay), t, lay)
        fr.alpha_composite(lay)
        if post: fr = post(fr, t, i)
        fr.convert("RGB").save(f"{tmp}/{i:04d}.jpg", quality=92)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(fps), "-i", f"{tmp}/%04d.jpg",
                    "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart", out_mp4], check=True)
    if poster: Image.open(f"{tmp}/0000.jpg").save(poster)
    gif = os.path.splitext(out_mp4)[0] + "-splash.gif"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", out_mp4, "-vf",
                    "fps=12,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer",
                    gif], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    return out_mp4, gif


# ── RGB-клавиатура ───────────────────────────────────────────────────────────
def rgb_art(S, palette, rows):
    assert len(rows) == 6 and all(len(r) == 23 for r in rows), "6 рядов × 23 клавиши"
    json.dump({"palette": {k: list(rgb(v) if isinstance(v, str) else v) for k, v in palette.items()}, "rows": rows,
               "bg": rows[0][0]}, open(T(S, "rgb.json"), "w"), indent=1)


# ── theme.json ───────────────────────────────────────────────────────────────
def manifest(S, **kw):
    m = {"id": S["id"], "name": S["name"], "description": S["desc"], "preview": "preview.png",
         "colorscheme": S["kde_colors"], "cursor": S["cursor"], "cursor_size": S.get("cursor_size", 32),
         "icons": S.get("icons", "Papirus-Dark"), "sounds": S["sounds"], "splash": S["splash"]["id"],
         "konsole_profile": S["konsole_profile"] + ".profile", "kitty": "out/kitty.conf",
         "prompt_bash": "prompt.bash", "prompt_fish": "prompt.fish", "fastfetch": "fastfetch.jsonc",
         "rgb": "rgb.json", "accent": S["pal"]["accent"], "accent2": S["pal"]["accent2"], "bg": S["pal"]["bg"],
         "system": {"sddm": S["sddm"]["name"], "grub": S["grub"]["name"], "plymouth": S["plymouth"]["name"],
                    "refind": S["refind"]["name"], "avatar": "system/avatar.png"}}
    m.update(kw)
    json.dump(m, open(T(S, "theme.json"), "w"), ensure_ascii=False, indent=2)
    return m

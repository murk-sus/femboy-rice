#!/usr/bin/env python3
"""rice — переключатель тем рабочего стола целиком.

  rice list                    список тем
  rice current                 активная тема
  rice apply <id>              обои, цвета, курсор, звуки, сплэш, терминалы, приглашения, fastfetch, клавиатура
  rice apply <id> --system     + загрузка/вход: GRUB, Plymouth, SDDM, rEFInd, аватар (через pkexec, спросит пароль)
  rice system <id>             только системная часть
  rice rgb                     применить подсветку клавиатуры текущей темы (для автозапуска)

Ничего не перезапускает (plasmashell/kwin/sddm не трогаются) — всё применяется на лету.
"""
import json, os, sys, shutil, subprocess, time

HOME = os.path.expanduser("~")
RICE = HOME + "/.local/share/rice"
THEMES = RICE + "/themes"
CUR = RICE + "/current"
LOG = RICE + "/rice.log"
SHARE = HOME + "/.local/share"
CFG = HOME + "/.config"
VIDEO_PLUGIN = "luisbocanegra.smart.video.wallpaper.reborn"
HELPER = "/usr/local/bin/rice-system"


def log(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(msg, flush=True)
    with open(LOG, "a") as f: f.write(line + "\n")


def run(cmd, **kw):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=kw.pop("timeout", 120), **kw)
        if r.returncode != 0: log(f"   ! {' '.join(cmd[:3])}… → {r.returncode}: {(r.stderr or r.stdout).strip()[:200]}")
        return r
    except Exception as e:
        log(f"   ! {cmd[0]}: {e}"); return None


def themes():
    out = []
    for d in sorted(os.listdir(THEMES)):
        p = f"{THEMES}/{d}/theme.json"
        if os.path.isfile(p):
            t = json.load(open(p)); t["_dir"] = f"{THEMES}/{d}"; out.append(t)
    return out


def load(tid):
    for t in themes():
        if t["id"] == tid: return t
    sys.exit(f"нет темы «{tid}». Есть: {', '.join(t['id'] for t in themes())}")


def current():
    try: return os.path.basename(os.readlink(CUR))
    except OSError: return None


def P(t, p):
    if not p: return None
    p = os.path.expanduser(p)
    return p if os.path.isabs(p) else os.path.join(t["_dir"], p)


def kw(file, groups, key, val):
    cmd = ["kwriteconfig6", "--notify", "--file", file]
    for g in groups: cmd += ["--group", g]
    run(cmd + ["--key", key, str(val)])


def plasma_js(js):
    return run(["qdbus6", "org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", js])


def link(src, dst):
    """симлинк dst → src (заменяя только наши симлинки/отсутствующие файлы)"""
    if os.path.islink(dst): os.remove(dst)
    elif os.path.exists(dst): return  # чужой настоящий файл не трогаем
    os.makedirs(os.path.dirname(dst), exist_ok=True); os.symlink(src, dst)


# ── шаги ─────────────────────────────────────────────────────────────────────
def install_assets(t):
    out = t["_dir"] + "/out"
    if not os.path.isdir(out): return
    m = {"color-schemes": SHARE + "/color-schemes", "konsole": SHARE + "/konsole", "icons": SHARE + "/icons",
         "sounds": SHARE + "/sounds", "look-and-feel": SHARE + "/plasma/look-and-feel"}
    for sub, dst in m.items():
        if os.path.isdir(f"{out}/{sub}"):
            for n in os.listdir(f"{out}/{sub}"): link(f"{out}/{sub}/{n}", f"{dst}/{n}")


def step_look(t):
    log("● цвета, курсор, иконки, звуки, сплэш")
    run(["plasma-apply-colorscheme", t["colorscheme"]])
    kw("kcminputrc", ["Mouse"], "cursorSize", t.get("cursor_size", 32))
    run(["plasma-apply-cursortheme", "--size", str(t.get("cursor_size", 32)), t["cursor"]])
    if t.get("icons"):
        kw("kdeglobals", ["Icons"], "Theme", t["icons"])
        if os.path.exists("/usr/lib/plasma-changeicons"): run(["/usr/lib/plasma-changeicons", t["icons"]])
    kw("kdeglobals", ["Sounds"], "Theme", t["sounds"]); kw("kdeglobals", ["Sounds"], "Enable", "true")
    kw("ksplashrc", ["KSplash"], "Engine", "KSplashQML"); kw("ksplashrc", ["KSplash"], "Theme", t["splash"])


def _wp_obj(t, w):
    return {"type": w["type"], "path": P(t, w["path"]), "poster": P(t, w.get("poster")) or ""}


def step_wallpapers(t):
    log("● обои (оба монитора) и меню")
    wp = t["wallpapers"]; cfg = {"main": _wp_obj(t, wp["main"]), "side": _wp_obj(t, wp.get("side", wp["main"]))}
    js = """
var cfg = %s;
var ds = desktops(), maxw = 0;
for (var i = 0; i < ds.length; i++) { var g = screenGeometry(ds[i].screen); if (g.width > maxw) maxw = g.width; }
for (var i = 0; i < ds.length; i++) {
  var d = ds[i], g = screenGeometry(d.screen), w = (g.width == maxw) ? cfg.main : cfg.side;
  if (w.type == "video") {
    d.wallpaperPlugin = "%s";
    d.currentConfigGroup = ["Wallpaper", "%s", "General"];
    d.writeConfig("VideoUrls", JSON.stringify([{filename: "file://" + w.path, enabled: true, duration: 0, customDuration: 0,
                  playbackRate: 0, alternativePlaybackRate: 0, loop: true, dayNightPhase: 4}]));
  } else {
    d.wallpaperPlugin = "org.kde.image";
    d.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
    d.writeConfig("Image", "file://" + w.path);
    d.writeConfig("FillMode", 2);
  }
}
var icon = %s;
if (icon) { var ps = panels(); for (var j = 0; j < ps.length; j++) { var ws = ps[j].widgets("org.kde.plasma.kickoff");
  for (var k = 0; k < ws.length; k++) { ws[k].currentConfigGroup = ["General"]; ws[k].writeConfig("icon", icon); } } }
""" % (json.dumps(cfg), VIDEO_PLUGIN, VIDEO_PLUGIN, json.dumps(P(t, t.get("kickoff_icon")) or ""))
    plasma_js(js)


def step_lockscreen(t):
    log("● экран блокировки")
    w = t.get("lockscreen")
    if not w: return
    p = P(t, w["path"]); g = ["Greeter", "Wallpaper"]
    if w["type"] == "video":
        kw("kscreenlockerrc", ["Greeter"], "WallpaperPlugin", VIDEO_PLUGIN)
        kw("kscreenlockerrc", g + [VIDEO_PLUGIN, "General"], "VideoUrls", json.dumps(
            [{"filename": "file://" + p, "enabled": True, "duration": 0, "customDuration": 0, "playbackRate": 0,
              "alternativePlaybackRate": 0, "loop": True, "dayNightPhase": 4}], separators=(",", ":")))
        if w.get("poster"): kw("kscreenlockerrc", g + ["org.kde.image", "General"], "Image", "file://" + P(t, w["poster"]))
    else:
        kw("kscreenlockerrc", ["Greeter"], "WallpaperPlugin", "org.kde.image")
        kw("kscreenlockerrc", g + ["org.kde.image", "General"], "Image", "file://" + p)


def step_terminals(t):
    log("● Konsole, kitty, bash/fish, fastfetch")
    prof = t["konsole_profile"]
    kw("konsolerc", ["Desktop Entry"], "DefaultProfile", prof)
    # открытые вкладки Konsole не трогаем (их D-Bus API закрыт настройкой безопасности) — профиль подхватят новые окна
    # kitty
    kc = CFG + "/kitty/kitty.conf"
    if os.path.exists(kc) and t.get("kitty"):
        shutil.copy(P(t, t["kitty"]), CFG + "/kitty/rice-current.conf")
        s = open(kc).read(); lines = s.splitlines()
        new = [("include rice-current.conf" if l.strip().startswith("include themes/") or l.strip() == "include rice-current.conf" else l) for l in lines]
        if "include rice-current.conf" not in new: new.append("include rice-current.conf")
        if new != lines: open(kc, "w").write("\n".join(new) + "\n")
        subprocess.run(["pkill", "-USR1", "-x", "kitty"], capture_output=True)
    # fastfetch
    if t.get("fastfetch"):
        os.makedirs(CFG + "/fastfetch", exist_ok=True); shutil.copy(P(t, t["fastfetch"]), CFG + "/fastfetch/config.jsonc")


def step_rgb_async(t):
    if os.path.exists(P(t, t.get("rgb") or "") or "/nonexistent"):
        log("● подсветка клавиатуры (в фоне)")
        subprocess.Popen([sys.executable, os.path.abspath(__file__), "rgb"], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, start_new_session=True)


def step_avatar(t):
    av = P(t, t.get("system", {}).get("avatar"))
    if av and os.path.exists(av): shutil.copy(av, HOME + "/.face.icon")


def apply_user(tid):
    t = load(tid)
    log(f"══ тема: {t['name']} ══")
    if os.path.islink(CUR) or not os.path.exists(CUR):
        if os.path.islink(CUR): os.remove(CUR)
        os.symlink(t["_dir"], CUR)
    install_assets(t)
    run(["kbuildsycoca6"], timeout=60)
    for step in (step_look, step_wallpapers, step_lockscreen, step_terminals, step_avatar, step_rgb_async):
        try: step(t)
        except Exception as e: log(f"   ! {step.__name__}: {e}")
    log("✓ рабочий стол готов (новые окна терминала подхватят приглашение)")


def apply_system(tid):
    load(tid)
    if not os.path.exists(HELPER):
        log("✗ системный помощник не установлен. Один раз выполни:  sudo bash ~/rice-install-system.sh"); return 1
    log("● загрузка и вход: GRUB, Plymouth, SDDM, rEFInd (спросит пароль; initramfs пересобирается ~1 мин)")
    p = subprocess.Popen(["pkexec", HELPER, tid], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in p.stdout: log("   " + line.rstrip())
    rc = p.wait()
    log("✓ системная часть применена" if rc == 0 else f"✗ системная часть: код {rc}")
    return rc


def rgb():
    t = load(current() or "asuka"); spec = P(t, t.get("rgb"))
    if not spec or not os.path.exists(spec): return
    py = HOME + "/.local/share/asuka-theme/rgb/venv/bin/python"
    appimg = HOME + "/Applications/OpenRGB.AppImage"
    if not (os.path.exists(py) and os.path.exists(appimg)): return
    import socket
    def up():
        try: socket.create_connection(("127.0.0.1", 6742), 1).close(); return True
        except OSError: return False
    srv = None
    if not up():
        srv = subprocess.Popen([appimg, "--server", "--noautoconnect"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(30):
            if up(): break
            time.sleep(1)
    subprocess.run([py, RICE + "/rgb/kbd.py", spec])
    if srv: srv.terminate()


def main(a):
    if not a or a[0] in ("-h", "--help", "help"): print(__doc__); return
    cmd = a[0]
    if cmd == "list":
        cur = current()
        for t in themes(): print(("* " if t["id"] == cur else "  ") + f"{t['id']:10} {t['name']}")
    elif cmd == "current": print(current() or "")
    elif cmd == "apply" and len(a) > 1:
        if "--system-only" not in a: apply_user(a[1])
        if "--system" in a or "--system-only" in a: sys.exit(apply_system(a[1]))
    elif cmd == "system" and len(a) > 1: sys.exit(apply_system(a[1]))
    elif cmd == "rgb": rgb()
    else: print(__doc__); sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])

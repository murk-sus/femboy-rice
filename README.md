# femboy-rice ฅ^•ﻌ•^ฅ

Полная смена темы KDE Plasma 6 одной кнопкой: обои на оба монитора (живые), цвета, курсор, звуки,
сплэш, Konsole/kitty, приглашение bash/fish, fastfetch, RGB-клавиатура, а также **GRUB, rEFInd,
Plymouth (логи загрузки вместо полоски) и SDDM**. Плюс мод для Claude Code, который подстраивает
интерфейс и характер под активную тему.

19 тем: NERV // Asuka, Femboy Paws (Dark / Bratty), Rei // 1995 (в работе) и 15 фембой-тем —
Catboy Maid, Pink Rider, Protogen Lab, Fox Cottage, Arctic Wolf, Synthwave Boy, Night Fox, Cozy Lamp,
Rainbow Chaos, Space Bunny, Lightbulb Kitten, Goth Boy, Forest Spirit, Laundry Day, Samurai Cat.

> Сделано под конкретную машину (Arch/Nyarch, Plasma 6 Wayland, GRUB на `/efi`, пользователь
> `femboychik`). Пути, UUID разделов и имя пользователя захардкожены в скриптах — поправь под себя.

## Что внутри

| Путь | Что |
|---|---|
| `rice/rice.py` | CLI: `rice list`, `rice apply <id> [--system]`, `rice rgb` |
| `rice/rice_gui.py` | окно «Темы райса» (PyQt6), встраивается в Параметры → Внешний вид |
| `rice/build/lib.py` | генераторы: цвета KDE, Konsole/kitty, приглашения, курсор, звуки (синтез), сплэш, Plymouth, GRUB, rEFInd, SDDM, живые обои |
| `rice/build/family.py`, `family_themes.py` | 15 фембой-тем из описаний |
| `rice/themes/<id>/` | описание темы (`spec.py` или запись в `family_themes.py`), `claude.json` — характер для Claude |
| `rice/system/rice-system` | root-помощник (через pkexec): SDDM, GRUB, Plymouth, rEFInd, аватар |
| `scripts/rice-install-system.sh` | разовая установка системной части (`sudo`) |
| `scripts/fetch-art.sh` | скачивает арты с wallhaven (в репозитории их нет) |
| `claude-mod/rice-mood` | мод Claude Code: шапка, статус, звуки, характер, `/rice` |
| `rice/rclaude` | запуск Claude Code в окне Konsole с профилем темы |
| `asuka-theme/` | исходники темы NERV // Asuka |
| `fonts/` | шрифты (OFL) |

## Установка

```bash
# зависимости: python-pyqt6 python-pillow python-numpy python-fonttools ffmpeg librsvg xorg-xcursorgen
#              plymouth grub efibootmgr, плагин обоев luisbocanegra.smart.video.wallpaper.reborn
mkdir -p ~/.local/share/fonts/rice && cp fonts/* ~/.local/share/fonts/rice/ && fc-cache -f
cp -r rice ~/.local/share/rice
bash scripts/fetch-art.sh
cd ~/.local/share/rice/build && python family.py all        # 15 тем
python ../themes/femboy/spec.py; python ../themes/bratty/spec.py
ln -s ~/.local/share/rice/rice.py ~/.local/bin/rice
sudo bash scripts/rice-install-system.sh                     # GRUB/Plymouth/SDDM/rEFInd
rice apply femboy --system
```

Своя тема — один блок в `rice/build/family_themes.py`, затем `python family.py <id>`.

Арты в темах — SFW-работы с wallhaven.cc, права принадлежат их авторам.
Видео, звуки и картинки темы Asuka в репозиторий не входят.

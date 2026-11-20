#!/usr/bin/env bash
# Rice — разовая установка системной части переключателя тем.
# Запуск:  sudo bash ~/rice-install-system.sh
# Перезапускать после добавления/пересборки тем (копирует их GRUB/Plymouth/SDDM/rEFInd в систему).
# Что делает:
#   • /usr/local/bin/rice-system (root) + правило polkit — смена темы загрузки из GUI по паролю
#   • шрифты тем → /usr/share/fonts/rice (нужны Plymouth/SDDM)
#   • темы → /usr/share/{plymouth,grub,sddm}/themes, /efi/EFI/refind/themes
#   • rEFInd: ставит, если ещё нет (в прошлый раз помешала блокировка pacman), + пункт в NVRAM
#     и запасной пункт «rEFInd» в меню GRUB (если прошивка потеряет запись NVRAM)
# Ничего не перезагружает и не переключает текущую тему.
set -uo pipefail
U=femboychik
H=/home/$U
R=$H/.local/share/rice
ESP=/efi
ESP_PARTUUID=8dce05cb-1300-485a-bcbc-54475b3809ed
BOOT_PARTUUID=81c02714-fcb8-4491-a445-5ff7c83564e2
BK=/var/backups/rice-install-$(date +%Y%m%d-%H%M%S)
O=$'\e[38;2;255;122;198m'; G=$'\e[1;92m'; X=$'\e[1;91m'; N=$'\e[0m'
say()  { echo "${O}▌rice${N} $*"; }
ok()   { echo "  ${G}✓${N} $*"; }
fail() { echo "  ${X}✗ $*${N}"; }

[[ $EUID -eq 0 ]] || { echo "Нужен root: sudo bash $0"; exit 1; }
[[ -f $R/system/rice-system && -d $R/themes ]] || { echo "Нет $R — нечего ставить"; exit 1; }
mkdir -p "$BK"

say "Помощник и polkit"
install -m755 -o root -g root "$R/system/rice-system" /usr/local/bin/rice-system
cat > /usr/share/polkit-1/actions/org.femboychik.rice.policy <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE policyconfig PUBLIC "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd">
<policyconfig>
  <action id="org.femboychik.rice.system">
    <description>Change boot and login theme</description>
    <description xml:lang="ru">Сменить тему загрузки и входа (GRUB, Plymouth, SDDM, rEFInd)</description>
    <message xml:lang="ru">Смена темы загрузки требует пароль</message>
    <message>Changing the boot theme requires authentication</message>
    <defaults><allow_any>auth_admin</allow_any><allow_inactive>auth_admin</allow_inactive><allow_active>auth_admin_keep</allow_active></defaults>
    <annotate key="org.freedesktop.policykit.exec.path">/usr/local/bin/rice-system</annotate>
  </action>
</policyconfig>
EOF
ok "/usr/local/bin/rice-system, polkit"

say "Шрифты тем"
mkdir -p /usr/share/fonts/rice
for f in "$H"/.local/share/fonts/rice/*.ttf "$H"/.local/share/fonts/nerv/*.ttf; do [[ -f $f ]] && install -m644 "$f" /usr/share/fonts/rice/; done
fc-cache -f /usr/share/fonts/rice >/dev/null 2>&1; ok "$(ls /usr/share/fonts/rice | wc -l) шрифтов"

# ── rEFInd (если ещё не стоит) ───────────────────────────────────────────────
say "rEFInd"
RD=$ESP/EFI/refind
ESP_DEV=$(findmnt -no SOURCE "$ESP" 2>/dev/null)
if [[ $(findmnt -no FSTYPE "$ESP" 2>/dev/null) != vfat || $(blkid -s PARTUUID -o value "$ESP_DEV") != "$ESP_PARTUUID" ]]; then
  fail "$ESP — не ожидаемый EFI-раздел, rEFInd пропущен"
else
  if [[ ! -f /usr/share/refind/refind_x64.efi ]]; then
    for _ in $(seq 1 60); do [[ -e /var/lib/pacman/db.lck ]] || break; echo "  … жду, пока освободится pacman"; sleep 5; done
    pacman -S --needed --noconfirm refind > "$BK/pacman-refind.log" 2>&1 || fail "pacman refind (лог $BK/pacman-refind.log)"
  fi
  if [[ -f /usr/share/refind/refind_x64.efi ]]; then
    [[ -d $RD ]] && cp -a "$RD" "$BK/refind-esp-before"
    mkdir -p "$RD/drivers_x64" "$RD/themes"
    install -m644 /usr/share/refind/refind_x64.efi "$RD/refind_x64.efi"
    install -m644 /usr/share/refind/drivers_x64/ext4_x64.efi "$RD/drivers_x64/ext4_x64.efi"
    if [[ ! -f $RD/refind.conf ]] || ! grep -q '(rice)' "$RD/refind.conf"; then
      OPTS=$(tr ' ' '\n' < /proc/cmdline | grep -v -E '^(BOOT_IMAGE=|initrd=)' | grep -v '^$' | tr '\n' ' ' | sed 's/ $//')
      grep -q 'root=' <<<"$OPTS" || OPTS="root=UUID=$(findmnt -no UUID /) rw quiet splash loglevel=3"
      UC=""; for m in amd-ucode.img intel-ucode.img; do [[ -f /boot/$m ]] && UC+="initrd=\\$m "; done
      CURT=$(basename "$(readlink "$R/current" 2>/dev/null)" 2>/dev/null)
      RT=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['system']['refind'])" "$R/themes/${CURT:-asuka}/theme.json" 2>/dev/null || echo nerv-asuka)
      cat > "$RD/refind.conf" <<EOF
# rEFInd (rice) — тема переключается командой rice / «Темы райса» в Параметрах
timeout 8
use_nvram false
resolution max
scanfor manual
showtools reboot, shutdown, firmware
default_selection "LINUX"

include themes/$RT/theme.conf

menuentry "LINUX" {
    icon     /EFI/refind/themes/$RT/icons/os_main.png
    volume   $BOOT_PARTUUID
    loader   /vmlinuz-linux
    options  "$OPTS ${UC}initrd=\\initramfs-linux.img"
}

menuentry "FALLBACK" {
    icon     /EFI/refind/themes/$RT/icons/os_fallback.png
    volume   $BOOT_PARTUUID
    loader   /vmlinuz-linux
    options  "$(sed 's/ *quiet//; s/ *splash//; s/ *loglevel=[0-9]//' <<<"$OPTS") ${UC}initrd=\\initramfs-linux-fallback.img"
}

menuentry "GRUB" {
    icon     /EFI/refind/themes/$RT/icons/os_grub.png
    volume   $ESP_PARTUUID
    loader   \\EFI\\BOOT\\BOOTX64.EFI
}
EOF
    fi
    ok "файлы rEFInd на ESP"
    NUM=$(efibootmgr | sed -n 's/^Boot\([0-9A-F]\{4\}\)\* NERV rEFInd.*/\1/p' | head -1)
    if [[ -z $NUM ]]; then
      DISK=/dev/$(lsblk -no PKNAME "$ESP_DEV"); PART=$(cat /sys/class/block/$(basename "$ESP_DEV")/partition)
      efibootmgr --create --disk "$DISK" --part "$PART" --label "NERV rEFInd" --loader '\EFI\refind\refind_x64.efi' > "$BK/efibootmgr.log" 2>&1
      NUM=$(efibootmgr | sed -n 's/^Boot\([0-9A-F]\{4\}\)\* NERV rEFInd.*/\1/p' | head -1)
    fi
    if [[ -n $NUM ]]; then
      ORDER=$(efibootmgr | sed -n 's/^BootOrder: //p' | tr ',' '\n' | grep -v "^$NUM$" | paste -sd,)
      efibootmgr -o "$NUM${ORDER:+,$ORDER}" >/dev/null 2>&1; echo "$NUM" > /var/backups/asuka-refind-bootnum
      ok "NVRAM: Boot$NUM «NERV rEFInd» первым, GRUB («UEFI OS») — следующим"
    else fail "запись NVRAM не создана — rEFInd будет доступен из меню GRUB"; fi
    ESPUUID=$(blkid -s UUID -o value "$ESP_DEV")
    cat > /etc/grub.d/41_rice_refind <<EOF
#!/bin/sh
exec tail -n +3 \$0
menuentry "rEFInd (rice)" --class efi {
    insmod part_gpt
    insmod fat
    search --no-floppy --fs-uuid --set=root $ESPUUID
    chainloader /EFI/refind/refind_x64.efi
}
EOF
    chmod 755 /etc/grub.d/41_rice_refind; ok "пункт «rEFInd (rice)» в GRUB (появится при следующей смене темы)"
  fi
fi

# ── темы ─────────────────────────────────────────────────────────────────────
say "Темы"
for TD in "$R"/themes/*/; do
  TJ=$TD/theme.json; [[ -f $TJ ]] || continue
  read -r ID SDDM GRUB PLY REF AV < <(python3 - "$TJ" <<'EOF'
import json, os, sys
t = json.load(open(sys.argv[1])); s = t["system"]; d = os.path.dirname(sys.argv[1])
av = os.path.expanduser(s.get("avatar", "")); av = av if os.path.isabs(av) else os.path.join(d, av)
print(t["id"], s["sddm"], s["grub"], s["plymouth"], s["refind"], av)
EOF
)
  [[ $ID =~ ^[a-z0-9_-]+$ ]] || { fail "плохой id в $TJ"; continue; }
  SRCS=("$TD/system" "$H/.local/share/asuka-theme")   # asuka хранит системные части в asuka-theme
  inst() {  # inst <тип> <имя> <куда>
    local typ=$1 name=$2 dst=$3 src=""
    for b in "${SRCS[@]}"; do
      [[ -d $b/$typ/$name ]] && { src=$b/$typ/$name; break; }
    done
    if [[ -n $src ]]; then rm -rf "$dst/$name"; command cp -r "$src" "$dst/$name"; chown -R root:root "$dst/$name"; chmod -R a+rX "$dst/$name"; return 0
    elif [[ -d $dst/$name ]]; then return 0; else return 1; fi
  }
  M=()
  inst plymouth "$PLY" /usr/share/plymouth/themes && M+=(plymouth) || fail "$ID: нет plymouth/$PLY"
  inst grub "$GRUB" /usr/share/grub/themes && M+=(grub) || fail "$ID: нет grub/$GRUB"
  inst sddm "$SDDM" /usr/share/sddm/themes && M+=(sddm) || fail "$ID: нет sddm/$SDDM"
  if [[ -d $RD/themes ]]; then
    inst refind "$REF" "$RD/themes" && M+=(refind) || fail "$ID: нет refind/$REF"
    T_I=$RD/themes/$REF/icons
    [[ -f $T_I/os_asuka.png && ! -f $T_I/os_main.png ]] && command cp "$T_I/os_asuka.png" "$T_I/os_main.png"
  fi
  mkdir -p "/usr/local/share/rice/themes/$ID"
  printf 'SDDM=%s\nGRUB=%s\nPLYMOUTH=%s\nREFIND=%s\n' "$SDDM" "$GRUB" "$PLY" "$REF" > "/usr/local/share/rice/themes/$ID/system.conf"
  [[ -f $AV ]] && install -m644 "$AV" "/usr/local/share/rice/themes/$ID/avatar.png"
  chown -R root:root "/usr/local/share/rice/themes/$ID"
  ok "$ID: ${M[*]}"
done
sync
echo
say "Готово. Теперь тему загрузки можно менять в «Параметры → Внешний вид → Темы райса» (или: rice apply <id> --system)."
say "Бэкап: $BK"

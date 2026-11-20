#!/usr/bin/env bash
# NERV // Asuka — загрузка: Plymouth с живыми логами (asuka-log) + загрузчик rEFInd (nerv-asuka).
# Запуск:  sudo bash ~/asuka-apply-boot.sh            (всё)
#          sudo bash ~/asuka-apply-boot.sh --plymouth (только экран логов)
#          sudo bash ~/asuka-apply-boot.sh --refind   (только rEFInd)
# Перезагрузка НЕ выполняется. GRUB не удаляется: остаётся пунктом в rEFInd и запасным вариантом в BIOS.
# Откат:   sudo bash ~/asuka-rollback-boot.sh
set -uo pipefail

U=femboychik
H=/home/$U
A=$H/.local/share/asuka-theme
ESP=/efi
ESP_PARTUUID=8dce05cb-1300-485a-bcbc-54475b3809ed    # sda1, EFI
BOOT_PARTUUID=81c02714-fcb8-4491-a445-5ff7c83564e2   # sda2, /boot (ext4)
BK=/var/backups/asuka-boot-$(date +%Y%m%d-%H%M%S)
R=$'\e[1;91m'; O=$'\e[38;2;255;106;19m'; G=$'\e[1;92m'; N=$'\e[0m'
say()  { echo "${O}▌NERV${N} $*"; }
ok()   { echo "  ${G}✓${N} $*"; }
fail() { echo "  ${R}✗ $*${N}"; }

DO_PLY=1; DO_REF=1
case "${1:-}" in --plymouth) DO_REF=0;; --refind) DO_PLY=0;; "") ;; *) echo "Неизвестный флаг $1"; exit 1;; esac

[[ $EUID -eq 0 ]] || { echo "Нужен root: sudo bash $0"; exit 1; }
for p in "$A/plymouth/asuka-log/asuka-log.plymouth" "$A/plymouth/asuka-log/asuka-log.script" \
         "$A/plymouth/asuka-log/background.png" "$A/refind/nerv-asuka/theme.conf" \
         "$A/refind/nerv-asuka/banner.png" "$H/.local/share/fonts/nerv/ShareTechMono-Regular.ttf"; do
  [[ -e $p ]] || { echo "Нет файла $p — прерываю, ничего не изменено."; exit 1; }
done

mkdir -p "$BK"; echo "$BK" > /var/backups/asuka-boot-last
cp -a /etc/plymouth/plymouthd.conf "$BK"/
cp -a /boot/initramfs-linux.img /boot/initramfs-linux-fallback.img "$BK"/
efibootmgr -v > "$BK/efibootmgr-before.txt" 2>&1
plymouth-set-default-theme > "$BK/plymouth-theme-before" 2>/dev/null
say "Бэкап: $BK"
RESULT=()

# ── 1. Plymouth: терминал MAGI с логами systemd ──────────────────────────────
if (( DO_PLY )); then
  say "Plymouth: тема asuka-log (логи вместо полоски)"
  # шрифты для initramfs: plymouth-font-file ищет их через fc-match от root
  install -Dm644 "$H/.local/share/fonts/nerv/ShareTechMono-Regular.ttf" /usr/share/fonts/nerv/ShareTechMono-Regular.ttf
  install -Dm644 "$H/.local/share/fonts/nerv/Oswald[wght].ttf" "/usr/share/fonts/nerv/Oswald[wght].ttf"
  fc-cache -f /usr/share/fonts/nerv >/dev/null 2>&1
  rm -rf /usr/share/plymouth/themes/asuka-log
  cp -r "$A/plymouth/asuka-log" /usr/share/plymouth/themes/asuka-log
  chown -R root:root /usr/share/plymouth/themes/asuka-log; chmod -R a+rX /usr/share/plymouth/themes/asuka-log
  if plymouth-set-default-theme asuka-log \
     && [[ $(plymouth-set-default-theme) == asuka-log ]] \
     && mkinitcpio -p linux > "$BK/mkinitcpio.log" 2>&1 \
     && [[ -s /boot/initramfs-linux.img && -s /boot/initramfs-linux-fallback.img ]] \
     && lsinitcpio /boot/initramfs-linux.img | grep -q 'plymouth/themes/asuka-log/asuka-log.script'; then
    sync
    if lsinitcpio /boot/initramfs-linux.img | grep -q 'Plymouth-monospace.ttf' \
       && fc-match -f '%{family}' 'Share Tech Mono' | grep -q 'Share Tech Mono'; then
      ok "initramfs пересобран, тема и моно-шрифт внутри"
    else
      ok "initramfs пересобран (шрифт логов — системный моноширинный)"
    fi
    RESULT+=("Plymouth: OK (asuka-log)")
  else
    fail "Plymouth/mkinitcpio ошибка — откатываю"
    cp -a "$BK/plymouthd.conf" /etc/plymouth/plymouthd.conf
    cp -a "$BK/initramfs-linux.img" "$BK/initramfs-linux-fallback.img" /boot/; sync
    RESULT+=("Plymouth: ОТКАТ (старый initramfs возвращён). Лог: $BK/mkinitcpio.log")
  fi
fi

# ── 2. rEFInd: загрузчик в стиле NERV ────────────────────────────────────────
if (( DO_REF )); then
  say "rEFInd: тема nerv-asuka"
  ESP_DEV=$(findmnt -no SOURCE "$ESP" 2>/dev/null)
  ESP_FS=$(findmnt -no FSTYPE "$ESP" 2>/dev/null)
  if [[ $ESP_FS != vfat || $(blkid -s PARTUUID -o value "$ESP_DEV") != "$ESP_PARTUUID" ]]; then
    fail "$ESP не смонтирован как ожидаемый EFI-раздел ($ESP_DEV, $ESP_FS) — rEFInd пропущен"
    RESULT+=("rEFInd: пропущен (ESP не найден)")
  elif ! pacman -S --needed --noconfirm refind > "$BK/pacman-refind.log" 2>&1 || [[ ! -f /usr/share/refind/refind_x64.efi ]]; then
    fail "Не удалось поставить пакет refind (лог: $BK/pacman-refind.log)"; RESULT+=("rEFInd: пропущен (pacman)")
  else
    RD=$ESP/EFI/refind
    [[ -d $RD ]] && cp -a "$RD" "$BK/refind-esp-before"
    mkdir -p "$RD/drivers_x64" "$RD/themes"
    install -m644 /usr/share/refind/refind_x64.efi "$RD/refind_x64.efi"
    install -m644 /usr/share/refind/drivers_x64/ext4_x64.efi "$RD/drivers_x64/ext4_x64.efi"
    rm -rf "$RD/themes/nerv-asuka"; cp -r "$A/refind/nerv-asuka" "$RD/themes/nerv-asuka"

    # параметры ядра — ровно те, с которыми система загружена сейчас (без BOOT_IMAGE/initrd)
    OPTS=$(tr ' ' '\n' < /proc/cmdline | grep -v -E '^(BOOT_IMAGE=|initrd=)' | grep -v '^$' | tr '\n' ' ' | sed 's/ $//')
    grep -q 'root=' <<<"$OPTS" || OPTS="root=UUID=$(findmnt -no UUID /) rw quiet splash loglevel=3"
    UC=""; for m in amd-ucode.img intel-ucode.img; do [[ -f /boot/$m ]] && UC+="initrd=\\$m "; done
    GRUB_EFI=""
    [[ -f $ESP/EFI/BOOT/BOOTX64.EFI ]] && GRUB_EFI='\EFI\BOOT\BOOTX64.EFI'
    [[ -z $GRUB_EFI ]] && GRUB_EFI=$(cd "$ESP" && find EFI -maxdepth 2 -iname 'grubx64.efi' | head -1 | sed 's|^|\\|; s|/|\\|g')

    cat > "$RD/refind.conf" <<EOF
# NERV // Asuka — rEFInd (сгенерировано asuka-apply-boot.sh)
timeout 8
use_nvram false
resolution max
scanfor manual
showtools reboot, shutdown, firmware
default_selection "ASUKA"

include themes/nerv-asuka/theme.conf

menuentry "ASUKA" {
    icon     /EFI/refind/themes/nerv-asuka/icons/os_asuka.png
    volume   $BOOT_PARTUUID
    loader   /vmlinuz-linux
    options  "$OPTS ${UC}initrd=\\initramfs-linux.img"
}

menuentry "FALLBACK" {
    icon     /EFI/refind/themes/nerv-asuka/icons/os_fallback.png
    volume   $BOOT_PARTUUID
    loader   /vmlinuz-linux
    options  "$(sed 's/ *quiet//; s/ *splash//; s/ *loglevel=[0-9]//' <<<"$OPTS") ${UC}initrd=\\initramfs-linux-fallback.img"
}
EOF
    if [[ -n $GRUB_EFI ]]; then
      cat >> "$RD/refind.conf" <<EOF

menuentry "GRUB" {
    icon     /EFI/refind/themes/nerv-asuka/icons/os_grub.png
    volume   $ESP_PARTUUID
    loader   $GRUB_EFI
}
EOF
    fi
    sync

    if [[ -s $RD/refind_x64.efi && -s $RD/drivers_x64/ext4_x64.efi && -s $RD/themes/nerv-asuka/banner.png ]] \
       && grep -q 'root=' "$RD/refind.conf"; then
      ok "Файлы на ESP: $RD (GRUB в меню: ${GRUB_EFI:-нет})"
      # пункт в NVRAM — первым; GRUB (UEFI OS) остаётся следующим в BootOrder
      NUM=$(efibootmgr | sed -n 's/^Boot\([0-9A-F]\{4\}\)\* NERV rEFInd.*/\1/p' | head -1)
      if [[ -z $NUM ]]; then
        DISK=/dev/$(lsblk -no PKNAME "$ESP_DEV"); PART=$(cat /sys/class/block/$(basename "$ESP_DEV")/partition)
        efibootmgr --create --disk "$DISK" --part "$PART" --label "NERV rEFInd" --loader '\EFI\refind\refind_x64.efi' > "$BK/efibootmgr-create.log" 2>&1
        NUM=$(efibootmgr | sed -n 's/^Boot\([0-9A-F]\{4\}\)\* NERV rEFInd.*/\1/p' | head -1)
      fi
      if [[ -n $NUM ]]; then
        echo "$NUM" > /var/backups/asuka-refind-bootnum
        ORDER=$(efibootmgr | sed -n 's/^BootOrder: //p' | tr ',' '\n' | grep -v "^$NUM$" | paste -sd,)
        efibootmgr -o "$NUM${ORDER:+,$ORDER}" > /dev/null 2>&1
        ok "NVRAM: Boot$NUM «NERV rEFInd» первым; дальше: $ORDER"
        RESULT+=("rEFInd: OK (Boot$NUM первым, GRUB запасной)")
      else
        fail "efibootmgr не создал запись — rEFInd лежит на ESP, но не в меню BIOS (лог: $BK/efibootmgr-create.log)"
        RESULT+=("rEFInd: файлы есть, запись в NVRAM не создана")
      fi
    else
      fail "Файлы rEFInd на ESP не проверились — удаляю"
      rm -rf "$RD"; [[ -d $BK/refind-esp-before ]] && cp -a "$BK/refind-esp-before" "$RD"
      RESULT+=("rEFInd: ОТКАТ")
    fi
  fi
fi

efibootmgr -v > "$BK/efibootmgr-after.txt" 2>&1
echo; say "ИТОГ:"; for r in "${RESULT[@]}"; do echo "   $r"; done
echo "   Бэкап: $BK   |   откат: sudo bash $H/asuka-rollback-boot.sh"
echo "   ${R}Перезагрузка не требуется сейчас${N} — увидишь при следующем включении."
echo "   Если rEFInd вдруг не стартует: в меню BIOS (F8/F11/F12) выбери «UEFI OS» — это GRUB."

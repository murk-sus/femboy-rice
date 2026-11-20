#!/usr/bin/env bash
# NERV // Asuka — системная часть (GRUB, Plymouth, SDDM, аватар).
# Запуск:  sudo bash ~/asuka-apply-system.sh
# Перезагрузка НЕ нужна и НЕ выполняется — всё увидишь при следующем включении.
# Откат:   sudo bash ~/asuka-rollback-system.sh
set -uo pipefail

U=femboychik
H=/home/$U
A=$H/.local/share/asuka-theme
BK=/var/backups/asuka-$(date +%Y%m%d-%H%M%S)
R=$'\e[1;91m'; O=$'\e[38;2;255;106;19m'; G=$'\e[1;92m'; N=$'\e[0m'
say()  { echo "${O}▌NERV${N} $*"; }
ok()   { echo "  ${G}✓${N} $*"; }
fail() { echo "  ${R}✗ $*${N}"; }

[[ $EUID -eq 0 ]] || { echo "Нужен root: sudo bash $0"; exit 1; }
for p in "$A/sddm/nerv-asuka/Main.qml" "$A/sddm/nerv-asuka/backgrounds/asuka.mp4" \
         "$A/grub/NERV-Asuka/theme.txt" "$A/plymouth/asuka-nerv/asuka-nerv.plymouth" "$A/img/avatar.png"; do
  [[ -e $p ]] || { echo "Нет файла $p — прерываю, ничего не изменено."; exit 1; }
done

mkdir -p "$BK"
cp -a /etc/default/grub /etc/sddm.conf.d /etc/plymouth/plymouthd.conf "$BK"/ 2>/dev/null
cp -a /boot/grub/grub.cfg "$BK/grub.cfg"
cp -a /boot/initramfs-linux.img /boot/initramfs-linux-fallback.img "$BK"/
echo "$BK" > /var/backups/asuka-last
say "Бэкап: $BK"
RESULT=()

# ── 1. SDDM: экран входа (вместо ДжоДжо) ──────────────────────────────────────
say "SDDM: тема nerv-asuka"
rm -rf /usr/share/sddm/themes/nerv-asuka
cp -r "$A/sddm/nerv-asuka" /usr/share/sddm/themes/nerv-asuka
chown -R root:root /usr/share/sddm/themes/nerv-asuka; chmod -R a+rX /usr/share/sddm/themes/nerv-asuka
F=/etc/sddm.conf.d/kde_settings.conf
if grep -q '^Current=' "$F"; then
  sed -i 's/^Current=.*/Current=nerv-asuka/' "$F"
  grep -q '^Current=nerv-asuka' "$F" && { ok "SDDM → nerv-asuka"; RESULT+=("SDDM: OK"); } \
    || { cp -a "$BK/sddm.conf.d/kde_settings.conf" "$F"; fail "SDDM откатан"; RESULT+=("SDDM: ОТКАТ"); }
else
  fail "В $F нет строки Current= — SDDM не трогаю"; RESULT+=("SDDM: пропущен")
fi

# ── 2. Аватар пользователя (SDDM / меню) ─────────────────────────────────────
mkdir -p /var/lib/AccountsService/icons /var/lib/AccountsService/users
install -m 644 "$A/img/avatar.png" /var/lib/AccountsService/icons/$U
UF=/var/lib/AccountsService/users/$U
[[ -f $UF ]] && cp -a "$UF" "$BK/accountsservice-user"
if [[ -f $UF ]] && grep -q '^\[User\]' "$UF"; then
  grep -q '^Icon=' "$UF" && sed -i "s|^Icon=.*|Icon=/var/lib/AccountsService/icons/$U|" "$UF" \
                         || sed -i "/^\[User\]/a Icon=/var/lib/AccountsService/icons/$U" "$UF"
else
  printf '[User]\nIcon=/var/lib/AccountsService/icons/%s\nSystemAccount=false\n' "$U" > "$UF"
fi
ok "Аватар Аски"; RESULT+=("Аватар: OK")

# ── 3. GRUB: тема меню выбора ОС ─────────────────────────────────────────────
say "GRUB: тема NERV-Asuka"
rm -rf /usr/share/grub/themes/NERV-Asuka
cp -r "$A/grub/NERV-Asuka" /usr/share/grub/themes/NERV-Asuka
chown -R root:root /usr/share/grub/themes/NERV-Asuka
if grep -q '^GRUB_THEME=' /etc/default/grub; then
  sed -i 's|^GRUB_THEME=.*|GRUB_THEME="/usr/share/grub/themes/NERV-Asuka/theme.txt"|' /etc/default/grub
else
  echo 'GRUB_THEME="/usr/share/grub/themes/NERV-Asuka/theme.txt"' >> /etc/default/grub
fi
NEW=/boot/grub/grub.cfg.asuka-new
if grub-mkconfig -o "$NEW" > "$BK/grub-mkconfig.log" 2>&1 \
   && grub-script-check "$NEW" \
   && grep -q 'NERV-Asuka/theme.txt' "$NEW" \
   && [[ $(grep -c '^menuentry\|^submenu' "$NEW") -ge $(grep -c '^menuentry\|^submenu' "$BK/grub.cfg") ]] \
   && grep -q 'vmlinuz-linux' "$NEW"; then
  mv "$NEW" /boot/grub/grub.cfg; sync
  ok "grub.cfg пересобран и проверен (grub-script-check OK, все пункты меню на месте)"; RESULT+=("GRUB: OK")
else
  rm -f "$NEW"; cp -a "$BK/grub" /etc/default/grub
  fail "Проверка grub.cfg не прошла — старый grub.cfg и /etc/default/grub не тронуты. Лог: $BK/grub-mkconfig.log"
  RESULT+=("GRUB: ОТКАТ (ничего не изменено)")
fi

# ── 4. Plymouth: логотип загрузки ────────────────────────────────────────────
say "Plymouth: тема asuka-nerv"
rm -rf /usr/share/plymouth/themes/asuka-nerv
cp -r "$A/plymouth/asuka-nerv" /usr/share/plymouth/themes/asuka-nerv
chown -R root:root /usr/share/plymouth/themes/asuka-nerv
if plymouth-set-default-theme asuka-nerv \
   && [[ $(plymouth-set-default-theme) == asuka-nerv ]] \
   && mkinitcpio -p linux > "$BK/mkinitcpio.log" 2>&1 \
   && [[ -s /boot/initramfs-linux.img && -s /boot/initramfs-linux-fallback.img ]]; then
  sync; ok "initramfs пересобран (mkinitcpio -p linux)"; RESULT+=("Plymouth: OK")
else
  fail "Plymouth/mkinitcpio ошибка — откатываю"
  cp -a "$BK/plymouthd.conf" /etc/plymouth/plymouthd.conf
  cp -a "$BK/initramfs-linux.img" "$BK/initramfs-linux-fallback.img" /boot/; sync
  RESULT+=("Plymouth: ОТКАТ (старый initramfs возвращён). Лог: $BK/mkinitcpio.log")
fi

echo; say "ИТОГ:"; for r in "${RESULT[@]}"; do echo "   $r"; done
echo "   Бэкап: $BK   |   откат: sudo bash $H/asuka-rollback-system.sh"
echo "   ${R}Перезагрузка не требуется сейчас${N} — изменения появятся при следующем включении."

#!/usr/bin/env bash
# Откат системной части NERV // Asuka к состоянию до asuka-apply-system.sh
# Запуск: sudo bash ~/asuka-rollback-system.sh [папка-бэкапа]
set -uo pipefail
[[ $EUID -eq 0 ]] || { echo "Нужен root: sudo bash $0"; exit 1; }
BK=${1:-$(cat /var/backups/asuka-last 2>/dev/null)}
[[ -d $BK ]] || { echo "Бэкап не найден: '$BK'"; exit 1; }
echo "Откат из $BK"
cp -a "$BK/grub" /etc/default/grub
cp -a "$BK/grub.cfg" /boot/grub/grub.cfg
cp -a "$BK/sddm.conf.d/." /etc/sddm.conf.d/
cp -a "$BK/plymouthd.conf" /etc/plymouth/plymouthd.conf
cp -a "$BK/initramfs-linux.img" "$BK/initramfs-linux-fallback.img" /boot/
[[ -f $BK/accountsservice-user ]] && cp -a "$BK/accountsservice-user" /var/lib/AccountsService/users/femboychik
sync
echo "Готово: GRUB, SDDM, Plymouth и initramfs возвращены как было. Темы в /usr/share оставлены (не мешают)."

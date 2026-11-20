#!/usr/bin/env bash
# Откат asuka-apply-boot.sh: Plymouth → прежняя тема, rEFInd убирается из NVRAM и с ESP. GRUB не трогается.
# Запуск: sudo bash ~/asuka-rollback-boot.sh
set -uo pipefail
[[ $EUID -eq 0 ]] || { echo "Нужен root: sudo bash $0"; exit 1; }
BK=$(cat /var/backups/asuka-boot-last 2>/dev/null)
[[ -d $BK ]] || { echo "Бэкап не найден (/var/backups/asuka-boot-last)"; exit 1; }
echo "Бэкап: $BK"

PREV=$(cat "$BK/plymouth-theme-before" 2>/dev/null); PREV=${PREV:-asuka-nerv}
if [[ $(plymouth-set-default-theme) == asuka-log ]]; then
  plymouth-set-default-theme "$PREV" && mkinitcpio -p linux > "$BK/rollback-mkinitcpio.log" 2>&1 \
    && echo "✓ Plymouth → $PREV, initramfs пересобран" \
    || { cp -a "$BK/plymouthd.conf" /etc/plymouth/; cp -a "$BK"/initramfs-linux*.img /boot/; echo "✓ Plymouth: возвращены файлы из бэкапа"; }
fi

NUM=$(cat /var/backups/asuka-refind-bootnum 2>/dev/null)
if [[ -n $NUM ]] && efibootmgr | grep -q "^Boot$NUM\* NERV rEFInd"; then
  efibootmgr -b "$NUM" -B > /dev/null && echo "✓ Запись Boot$NUM (NERV rEFInd) удалена из NVRAM"
fi
rm -f /var/backups/asuka-refind-bootnum
if [[ -d /efi/EFI/refind ]]; then
  if [[ -d $BK/refind-esp-before ]]; then rm -rf /efi/EFI/refind; cp -a "$BK/refind-esp-before" /efi/EFI/refind; echo "✓ /efi/EFI/refind возвращён как было"
  else rm -rf /efi/EFI/refind; echo "✓ /efi/EFI/refind удалён"; fi
fi
sync; echo "Готово. Загрузка снова через GRUB."

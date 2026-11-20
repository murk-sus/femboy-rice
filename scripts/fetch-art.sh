#!/usr/bin/env bash
# Скачивает арты тем с wallhaven.cc (SFW) — в репозитории их нет: это работы других авторов.
set -euo pipefail
R=$HOME/.local/share/rice
get() {  # get <id> <dir>
  mkdir -p "$2"; ls "$2"/wallhaven-"$1".* >/dev/null 2>&1 && return
  p=$(curl -s "https://wallhaven.cc/api/v1/w/$1" | python3 -c "import json,sys;print(json.load(sys.stdin)['data']['path'])")
  echo "↓ $1"; curl -fsSL -o "$2/$(basename "$p")" "$p"
}
for id in rq3me7 kxmrxm dg58wj 73wo7o l3wx2p v9y2vm gpm77q 8x76jk 0qvdgl e7y78w 45kqz9 xl7d3o 1qk68w dgp9pl 2eykl6 qrppoq vpzld3 wq6jdr o5dg9p 3z5j2v; do get $id "$R/pool"; done
for id in vpzld3 kxmrxm 2eykl6 l3wx2p dgp9pl; do get $id "$R/themes/femboy/src"; done
for id in dg58wj qrppoq vpzld3 kxmrxm l3wx2p; do get $id "$R/themes/bratty/src"; done
for id in gpdm3e x1ppyv ogdzd5 pk98lm 8xk6oo lyykvy 1jgvwv; do get $id "$R/themes/rei/src"; done
echo "готово"

# Space Bunny — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]landed~"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]houston, nya! [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;168;200;255m\] \[\e[38;2;255;154;213m\]\u\[\e[38;2;141;136;149m\]@\[\e[38;2;168;200;255m\]moonbase \[\e[38;2;141;136;149m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;141;136;149m\][${st}\[\e[38;2;141;136;149m\]]${r}\n\[\e[1;38;2;168;200;255m\]❯\[\e[38;2;255;255;255m\]❯\[\e[38;2;255;154;213m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

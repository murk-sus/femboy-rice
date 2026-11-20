# Protogen Lab — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]beep! ok"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]ERR >_< [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;79;240;255m\] \[\e[38;2;255;111;216m\]\u\[\e[38;2;141;139;150m\]@\[\e[38;2;125;255;178m\]visor \[\e[38;2;141;139;150m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;141;139;150m\][${st}\[\e[38;2;141;139;150m\]]${r}\n\[\e[1;38;2;79;240;255m\]❯\[\e[38;2;125;255;178m\]❯\[\e[38;2;255;111;216m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

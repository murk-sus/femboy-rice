# Goth Boy — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]...acceptable."; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]how tragic. [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;255;59;92m\] \[\e[38;2;232;232;240m\]\u\[\e[38;2;142;134;145m\]@\[\e[38;2;154;107;255m\]crypt \[\e[38;2;142;134;145m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;142;134;145m\][${st}\[\e[38;2;142;134;145m\]]${r}\n\[\e[1;38;2;255;59;92m\]❯\[\e[38;2;154;107;255m\]❯\[\e[38;2;232;232;240m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

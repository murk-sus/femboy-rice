# Night Fox — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]hehe~"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]*fox screech* [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;255;122;107m\] \[\e[38;2;211;154;255m\]\u\[\e[38;2;147;136;147m\]@\[\e[38;2;255;208;160m\]foxden \[\e[38;2;147;136;147m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;147;136;147m\][${st}\[\e[38;2;147;136;147m\]]${r}\n\[\e[1;38;2;255;122;107m\]❯\[\e[38;2;255;208;160m\]❯\[\e[38;2;211;154;255m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

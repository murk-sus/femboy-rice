# Samurai Cat — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]honor~"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]dishonor! [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;255;79;107m\] \[\e[38;2;255;179;200m\]\u\[\e[38;2;145;135;144m\]@\[\e[38;2;255;211;107m\]dojo \[\e[38;2;145;135;144m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;145;135;144m\][${st}\[\e[38;2;145;135;144m\]]${r}\n\[\e[1;38;2;255;79;107m\]❯\[\e[38;2;255;211;107m\]❯\[\e[38;2;255;179;200m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

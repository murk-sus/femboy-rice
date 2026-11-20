# Rainbow Chaos — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]WOOO!"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]AAAAA! [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;255;79;154m\] \[\e[38;2;79;216;255m\]\u\[\e[38;2;144;135;149m\]@\[\e[38;2;255;224;79m\]prism \[\e[38;2;144;135;149m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;144;135;149m\][${st}\[\e[38;2;144;135;149m\]]${r}\n\[\e[1;38;2;255;79;154m\]❯\[\e[38;2;255;224;79m\]❯\[\e[38;2;79;216;255m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

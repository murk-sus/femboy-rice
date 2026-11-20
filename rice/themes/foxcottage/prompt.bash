# Fox Cottage — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]all cozy~"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]spilled the tea! [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;255;160;74m\] \[\e[38;2;168;224;122m\]\u\[\e[38;2;147;137;144m\]@\[\e[38;2;255;226;168m\]cottage \[\e[38;2;147;137;144m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;147;137;144m\][${st}\[\e[38;2;147;137;144m\]]${r}\n\[\e[1;38;2;255;160;74m\]❯\[\e[38;2;255;226;168m\]❯\[\e[38;2;168;224;122m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

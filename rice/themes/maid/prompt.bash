# Catboy Maid — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]as you wish~"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]oh no, the tea! [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;255;143;199m\] \[\e[38;2;255;255;255m\]\u\[\e[38;2;146;137;148m\]@\[\e[38;2;201;160;255m\]maidcafe \[\e[38;2;146;137;148m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;146;137;148m\][${st}\[\e[38;2;146;137;148m\]]${r}\n\[\e[1;38;2;255;143;199m\]❯\[\e[38;2;201;160;255m\]❯\[\e[38;2;255;255;255m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

# Pink Rider — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]yay~!"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]oopsie daisy! [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;255;111;177m\] \[\e[38;2;255;211;107m\]\u\[\e[38;2;147;136;148m\]@\[\e[38;2;255;111;177m\]hippogriff \[\e[38;2;147;136;148m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;147;136;148m\][${st}\[\e[38;2;147;136;148m\]]${r}\n\[\e[1;38;2;255;111;177m\]❯\[\e[38;2;255;255;255m\]❯\[\e[38;2;255;211;107m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

# Forest Spirit — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]the grove approves~"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]the leaves rustle... [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;155;227;107m\] \[\e[38;2;255;211;107m\]\u\[\e[38;2;143;140;145m\]@\[\e[38;2;127;214;200m\]grove \[\e[38;2;143;140;145m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;143;140;145m\][${st}\[\e[38;2;143;140;145m\]]${r}\n\[\e[1;38;2;155;227;107m\]❯\[\e[38;2;127;214;200m\]❯\[\e[38;2;255;211;107m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

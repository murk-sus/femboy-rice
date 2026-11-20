# Arctic Wolf — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]awoo~"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]*sad howl* [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;185;200;255m\] \[\e[38;2;215;168;255m\]\u\[\e[38;2;143;138;151m\]@\[\e[38;2;127;232;255m\]tundra \[\e[38;2;143;138;151m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;143;138;151m\][${st}\[\e[38;2;143;138;151m\]]${r}\n\[\e[1;38;2;185;200;255m\]❯\[\e[38;2;127;232;255m\]❯\[\e[38;2;215;168;255m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

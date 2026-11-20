# Lightbulb Kitten — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]light on~"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]the light flickered... [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;255;210;79m\] \[\e[38;2;154;123;255m\]\u\[\e[38;2;144;135;155m\]@\[\e[38;2;255;210;79m\]nightboat \[\e[38;2;144;135;155m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;144;135;155m\][${st}\[\e[38;2;144;135;155m\]]${r}\n\[\e[1;38;2;255;210;79m\]❯\[\e[38;2;255;255;255m\]❯\[\e[38;2;154;123;255m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

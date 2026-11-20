# Laundry Day — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]squeaky clean~"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]lost a sock! [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;143;227;208m\] \[\e[38;2;255;168;207m\]\u\[\e[38;2;143;140;149m\]@\[\e[38;2;143;227;208m\]laundromat \[\e[38;2;143;140;149m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;143;140;149m\][${st}\[\e[38;2;143;140;149m\]]${r}\n\[\e[1;38;2;143;227;208m\]❯\[\e[38;2;255;255;255m\]❯\[\e[38;2;255;168;207m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

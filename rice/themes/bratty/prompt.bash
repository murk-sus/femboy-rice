# Femboy Paws // Bratty — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]good boy~"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]hmph! baka [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;255;63;164m\] \[\e[38;2;111;227;255m\]\u\[\e[38;2;141;125;158m\]@\[\e[38;2;180;92;255m\]brat \[\e[38;2;141;125;158m\]:: \[\e[38;2;255;238;248m\]${wd} \[\e[38;2;141;125;158m\][${st}\[\e[38;2;141;125;158m\]]${r}\n\[\e[1;38;2;255;63;164m\]❯\[\e[38;2;180;92;255m\]❯\[\e[38;2;111;227;255m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

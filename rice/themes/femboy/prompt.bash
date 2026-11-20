# Femboy Paws // Dark — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]uwu"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]>w< oopsie [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;255;122;198m\] \[\e[38;2;127;212;255m\]\u\[\e[38;2;141;125;158m\]@\[\e[38;2;184;146;255m\]fluffy \[\e[38;2;141;125;158m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;141;125;158m\][${st}\[\e[38;2;141;125;158m\]]${r}\n\[\e[1;38;2;255;122;198m\]❯\[\e[38;2;184;146;255m\]❯\[\e[38;2;127;212;255m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

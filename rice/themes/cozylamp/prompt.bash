# Cozy Lamp — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__rice_ps1() {
  local s=$? r='\[\e[0m\]'
  local st="\[\e[38;2;125;255;178m\]comfy~"; (( s != 0 )) && st="\[\e[1;38;2;255;85;119m\]*knocks over mug* [$s]"
  local wd='\w'
  PS1="\n\[\e[1;38;2;255;179;71m\] \[\e[38;2;255;143;177m\]\u\[\e[38;2;146;136;143m\]@\[\e[38;2;255;231;168m\]blanketfort \[\e[38;2;146;136;143m\]:: \[\e[38;2;251;239;255m\]${wd} \[\e[38;2;146;136;143m\][${st}\[\e[38;2;146;136;143m\]]${r}\n\[\e[1;38;2;255;179;71m\]❯\[\e[38;2;255;231;168m\]❯\[\e[38;2;255;143;177m\]❯${r} "
}
PROMPT_COMMAND=__rice_ps1

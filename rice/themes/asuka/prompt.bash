# NERV // Asuka — приглашение bash (rice)
[[ -z "$RICE_GREETED" && -t 1 ]] && command -v fastfetch >/dev/null && { export RICE_GREETED=1; fastfetch; }
__nerv_ps1() {
  local s=$? r='\[\e[0m\]' red='\[\e[1;91m\]' org='\[\e[38;2;255;106;19m\]' dim='\[\e[90m\]' wh='\[\e[97m\]'
  local st="${org}SYNC OK"; (( s != 0 )) && st="${red}あんたバカ? [$s]"
  PS1="\n${red}▌NERV ${dim}// ${org}\u${dim}@${org}EVA-02 ${dim}:: ${wh}\w ${dim}[${st}${dim}]${r}\n${red}❯${org}❯${r} "
}
PROMPT_COMMAND=__nerv_ps1

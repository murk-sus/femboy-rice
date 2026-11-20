# Goth Boy — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"...acceptable."
    test $s -ne 0; and set st (set_color -o ff5577)"how tragic. [$s]"
    echo
    echo (set_color -o ff3b5c)" "(set_color e8e8f0)$USER(set_color 8e8691)"@"(set_color 9a6bff)"crypt "(set_color 8e8691)":: "(set_color fbefff)(prompt_pwd)" "(set_color 8e8691)"["$st(set_color 8e8691)"]"
    echo -n (set_color -o ff3b5c)"❯"(set_color 9a6bff)"❯"(set_color e8e8f0)"❯"" "(set_color normal)
end

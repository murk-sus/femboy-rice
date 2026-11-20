# Catboy Maid — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"as you wish~"
    test $s -ne 0; and set st (set_color -o ff5577)"oh no, the tea! [$s]"
    echo
    echo (set_color -o ff8fc7)" "(set_color ffffff)$USER(set_color 928994)"@"(set_color c9a0ff)"maidcafe "(set_color 928994)":: "(set_color fbefff)(prompt_pwd)" "(set_color 928994)"["$st(set_color 928994)"]"
    echo -n (set_color -o ff8fc7)"❯"(set_color c9a0ff)"❯"(set_color ffffff)"❯"" "(set_color normal)
end

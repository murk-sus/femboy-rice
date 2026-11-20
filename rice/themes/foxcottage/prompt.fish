# Fox Cottage — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"all cozy~"
    test $s -ne 0; and set st (set_color -o ff5577)"spilled the tea! [$s]"
    echo
    echo (set_color -o ffa04a)" "(set_color a8e07a)$USER(set_color 938990)"@"(set_color ffe2a8)"cottage "(set_color 938990)":: "(set_color fbefff)(prompt_pwd)" "(set_color 938990)"["$st(set_color 938990)"]"
    echo -n (set_color -o ffa04a)"❯"(set_color ffe2a8)"❯"(set_color a8e07a)"❯"" "(set_color normal)
end

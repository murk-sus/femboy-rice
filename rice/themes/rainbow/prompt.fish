# Rainbow Chaos — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"WOOO!"
    test $s -ne 0; and set st (set_color -o ff5577)"AAAAA! [$s]"
    echo
    echo (set_color -o ff4f9a)" "(set_color 4fd8ff)$USER(set_color 908795)"@"(set_color ffe04f)"prism "(set_color 908795)":: "(set_color fbefff)(prompt_pwd)" "(set_color 908795)"["$st(set_color 908795)"]"
    echo -n (set_color -o ff4f9a)"❯"(set_color ffe04f)"❯"(set_color 4fd8ff)"❯"" "(set_color normal)
end

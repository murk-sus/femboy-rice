# Forest Spirit — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"the grove approves~"
    test $s -ne 0; and set st (set_color -o ff5577)"the leaves rustle... [$s]"
    echo
    echo (set_color -o 9be36b)" "(set_color ffd36b)$USER(set_color 8f8c91)"@"(set_color 7fd6c8)"grove "(set_color 8f8c91)":: "(set_color fbefff)(prompt_pwd)" "(set_color 8f8c91)"["$st(set_color 8f8c91)"]"
    echo -n (set_color -o 9be36b)"❯"(set_color 7fd6c8)"❯"(set_color ffd36b)"❯"" "(set_color normal)
end

# Protogen Lab — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"beep! ok"
    test $s -ne 0; and set st (set_color -o ff5577)"ERR >_< [$s]"
    echo
    echo (set_color -o 4ff0ff)" "(set_color ff6fd8)$USER(set_color 8d8b96)"@"(set_color 7dffb2)"visor "(set_color 8d8b96)":: "(set_color fbefff)(prompt_pwd)" "(set_color 8d8b96)"["$st(set_color 8d8b96)"]"
    echo -n (set_color -o 4ff0ff)"❯"(set_color 7dffb2)"❯"(set_color ff6fd8)"❯"" "(set_color normal)
end

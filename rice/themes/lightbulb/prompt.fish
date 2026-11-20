# Lightbulb Kitten — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"light on~"
    test $s -ne 0; and set st (set_color -o ff5577)"the light flickered... [$s]"
    echo
    echo (set_color -o ffd24f)" "(set_color 9a7bff)$USER(set_color 90879b)"@"(set_color ffd24f)"nightboat "(set_color 90879b)":: "(set_color fbefff)(prompt_pwd)" "(set_color 90879b)"["$st(set_color 90879b)"]"
    echo -n (set_color -o ffd24f)"❯"(set_color ffffff)"❯"(set_color 9a7bff)"❯"" "(set_color normal)
end

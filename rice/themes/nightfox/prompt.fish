# Night Fox — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"hehe~"
    test $s -ne 0; and set st (set_color -o ff5577)"*fox screech* [$s]"
    echo
    echo (set_color -o ff7a6b)" "(set_color d39aff)$USER(set_color 938893)"@"(set_color ffd0a0)"foxden "(set_color 938893)":: "(set_color fbefff)(prompt_pwd)" "(set_color 938893)"["$st(set_color 938893)"]"
    echo -n (set_color -o ff7a6b)"❯"(set_color ffd0a0)"❯"(set_color d39aff)"❯"" "(set_color normal)
end

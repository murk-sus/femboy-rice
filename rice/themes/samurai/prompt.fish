# Samurai Cat — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"honor~"
    test $s -ne 0; and set st (set_color -o ff5577)"dishonor! [$s]"
    echo
    echo (set_color -o ff4f6b)" "(set_color ffb3c8)$USER(set_color 918790)"@"(set_color ffd36b)"dojo "(set_color 918790)":: "(set_color fbefff)(prompt_pwd)" "(set_color 918790)"["$st(set_color 918790)"]"
    echo -n (set_color -o ff4f6b)"❯"(set_color ffd36b)"❯"(set_color ffb3c8)"❯"" "(set_color normal)
end

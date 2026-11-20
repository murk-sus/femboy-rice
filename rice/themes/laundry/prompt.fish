# Laundry Day — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"squeaky clean~"
    test $s -ne 0; and set st (set_color -o ff5577)"lost a sock! [$s]"
    echo
    echo (set_color -o 8fe3d0)" "(set_color ffa8cf)$USER(set_color 8f8c95)"@"(set_color 8fe3d0)"laundromat "(set_color 8f8c95)":: "(set_color fbefff)(prompt_pwd)" "(set_color 8f8c95)"["$st(set_color 8f8c95)"]"
    echo -n (set_color -o 8fe3d0)"❯"(set_color ffffff)"❯"(set_color ffa8cf)"❯"" "(set_color normal)
end

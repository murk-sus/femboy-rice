# Pink Rider — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"yay~!"
    test $s -ne 0; and set st (set_color -o ff5577)"oopsie daisy! [$s]"
    echo
    echo (set_color -o ff6fb1)" "(set_color ffd36b)$USER(set_color 938894)"@"(set_color ff6fb1)"hippogriff "(set_color 938894)":: "(set_color fbefff)(prompt_pwd)" "(set_color 938894)"["$st(set_color 938894)"]"
    echo -n (set_color -o ff6fb1)"❯"(set_color ffffff)"❯"(set_color ffd36b)"❯"" "(set_color normal)
end

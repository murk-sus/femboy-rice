# Femboy Paws // Bratty — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"good boy~"
    test $s -ne 0; and set st (set_color -o ff5577)"hmph! baka [$s]"
    echo
    echo (set_color -o ff3fa4)" "(set_color 6fe3ff)$USER(set_color 8d7d9e)"@"(set_color b45cff)"brat "(set_color 8d7d9e)":: "(set_color ffeef8)(prompt_pwd)" "(set_color 8d7d9e)"["$st(set_color 8d7d9e)"]"
    echo -n (set_color -o ff3fa4)"❯"(set_color b45cff)"❯"(set_color 6fe3ff)"❯"" "(set_color normal)
end

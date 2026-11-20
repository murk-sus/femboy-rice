# Space Bunny — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"landed~"
    test $s -ne 0; and set st (set_color -o ff5577)"houston, nya! [$s]"
    echo
    echo (set_color -o a8c8ff)" "(set_color ff9ad5)$USER(set_color 8d8895)"@"(set_color a8c8ff)"moonbase "(set_color 8d8895)":: "(set_color fbefff)(prompt_pwd)" "(set_color 8d8895)"["$st(set_color 8d8895)"]"
    echo -n (set_color -o a8c8ff)"❯"(set_color ffffff)"❯"(set_color ff9ad5)"❯"" "(set_color normal)
end

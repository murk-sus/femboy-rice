# Femboy Paws // Dark — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"uwu"
    test $s -ne 0; and set st (set_color -o ff5577)">w< oopsie [$s]"
    echo
    echo (set_color -o ff7ac6)" "(set_color 7fd4ff)$USER(set_color 8d7d9e)"@"(set_color b892ff)"fluffy "(set_color 8d7d9e)":: "(set_color fbefff)(prompt_pwd)" "(set_color 8d7d9e)"["$st(set_color 8d7d9e)"]"
    echo -n (set_color -o ff7ac6)"❯"(set_color b892ff)"❯"(set_color 7fd4ff)"❯"" "(set_color normal)
end

# Arctic Wolf — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"awoo~"
    test $s -ne 0; and set st (set_color -o ff5577)"*sad howl* [$s]"
    echo
    echo (set_color -o b9c8ff)" "(set_color d7a8ff)$USER(set_color 8f8a97)"@"(set_color 7fe8ff)"tundra "(set_color 8f8a97)":: "(set_color fbefff)(prompt_pwd)" "(set_color 8f8a97)"["$st(set_color 8f8a97)"]"
    echo -n (set_color -o b9c8ff)"❯"(set_color 7fe8ff)"❯"(set_color d7a8ff)"❯"" "(set_color normal)
end

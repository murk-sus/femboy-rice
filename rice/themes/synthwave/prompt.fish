# Synthwave Boy — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"RAD!"
    test $s -ne 0; and set st (set_color -o ff5577)"BOGUS! [$s]"
    echo
    echo (set_color -o ff4fd8)" "(set_color 4ff0ff)$USER(set_color 8f8797)"@"(set_color ffcf4f)"outrun "(set_color 8f8797)":: "(set_color fbefff)(prompt_pwd)" "(set_color 8f8797)"["$st(set_color 8f8797)"]"
    echo -n (set_color -o ff4fd8)"❯"(set_color ffcf4f)"❯"(set_color 4ff0ff)"❯"" "(set_color normal)
end

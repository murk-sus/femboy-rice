# Cozy Lamp — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7dffb2)"comfy~"
    test $s -ne 0; and set st (set_color -o ff5577)"*knocks over mug* [$s]"
    echo
    echo (set_color -o ffb347)" "(set_color ff8fb1)$USER(set_color 92888f)"@"(set_color ffe7a8)"blanketfort "(set_color 92888f)":: "(set_color fbefff)(prompt_pwd)" "(set_color 92888f)"["$st(set_color 92888f)"]"
    echo -n (set_color -o ffb347)"❯"(set_color ffe7a8)"❯"(set_color ff8fb1)"❯"" "(set_color normal)
end

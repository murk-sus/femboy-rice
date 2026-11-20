# Rei // 1995 — приглашение fish (rice)
function fish_prompt
    set -l s $status
    set -l st (set_color 7fe0a8)"…"
    test $s -ne 0; and set st (set_color -o ff4d4d)"わからない [$s]"
    echo
    echo (set_color -o e03a3e)"▌00 "(set_color 9cc8ff)$USER(set_color 6f8296)"@"(set_color 9cc8ff)"UNIT-00 "(set_color 6f8296)":: "(set_color e8f0f8)(prompt_pwd)" "(set_color 6f8296)"["$st(set_color 6f8296)"]"
    echo -n (set_color -o e03a3e)"▶"(set_color 9cc8ff)"▶"" "(set_color normal)
end

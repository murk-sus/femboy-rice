# NERV // Asuka prompt
function fish_prompt
    set -l s $status
    set -l st (set_color ff6a13)"SYNC OK"
    test $s -ne 0; and set st (set_color -o ff3b30)"あんたバカ? [$s]"
    echo
    echo (set_color -o ff3b30)"▌NERV "(set_color 777)"// "(set_color ff6a13)$USER(set_color 777)"@"(set_color ff6a13)"EVA-02 "(set_color 777)":: "(set_color fff)(prompt_pwd)" "(set_color 777)"["$st(set_color 777)"]"
    echo -n (set_color -o ff3b30)"❯"(set_color ff6a13)"❯ "(set_color normal)
end

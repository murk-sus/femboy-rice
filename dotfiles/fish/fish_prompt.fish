# Тема оформления (rice): приглашение берётся из активной темы
if test -f ~/.local/share/rice/current/prompt.fish
    source ~/.local/share/rice/current/prompt.fish
else
    function fish_prompt
        echo -n (prompt_pwd)' > '
    end
end

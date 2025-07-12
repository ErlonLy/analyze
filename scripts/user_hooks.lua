-- scripts/user_hooks.lua
-- Pode ser estendido para novos heurísticos Lua
function custom_heuristic(file)
    if string.match(file, "%.pak$") then
        return "Possível Unreal Engine PAK"
    end
    return nil
end

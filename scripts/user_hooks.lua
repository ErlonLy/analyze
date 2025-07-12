-- scripts/user_hooks.lua
function custom_heuristic(file)
    if string.match(file, "%.dll$") and string.match(file:lower(), "guard") then
        return "Possível DLL relacionada a proteção ou anti-cheat"
    end
    return nil
end

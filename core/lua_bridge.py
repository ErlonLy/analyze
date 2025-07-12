from lupa import LuaRuntime
import os

lua = LuaRuntime(unpack_returned_tuples=True)

# Função heurística principal
lua.execute("""
function analyze_files(files)
    local results = {}
    for i = 1, #files do
        local f = files[i]:lower()
        if string.find(f, "x3.xem") then
            table.insert(results, "Possível XignCode3 detectado")
        elseif string.find(f, "eac") then
            table.insert(results, "Possível EasyAntiCheat detectado")
        elseif string.find(f, "%.pak$") then
            table.insert(results, "Possível Unreal Engine (PAK)")
        end
    end
    return results
end
""")
lua_func = lua.globals().analyze_files

def pylist_to_luatable(pylist):
    tbl = lua.table()
    for i, v in enumerate(pylist):
        tbl[i+1] = v  # Lua é 1-based!
    return tbl

def load_user_lua_hooks():
    scripts_dir = os.path.join(os.path.dirname(__file__), "../scripts")
    hooks = []
    if not os.path.exists(scripts_dir):
        return hooks
    for fname in os.listdir(scripts_dir):
        if fname.endswith(".lua"):
            with open(os.path.join(scripts_dir, fname), "r", encoding="utf-8") as f:
                hooks.append(f.read())
    return hooks

def run_lua_heuristics(file_list):
    lua_files = pylist_to_luatable(file_list)
    results = list(lua_func(lua_files))
    # Executa scripts customizados do usuário:
    for code in load_user_lua_hooks():
        try:
            lua.execute(code)
            if 'custom_heuristic' in lua.globals():
                for f in file_list:
                    custom = lua.globals().custom_heuristic(f)
                    if custom:
                        results.append(str(custom))
        except Exception:
            continue
    return results

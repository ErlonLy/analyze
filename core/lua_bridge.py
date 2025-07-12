# core/lua_bridge.py
from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)

lua.execute("""
function analyze_files(files)
    local results = {}
    for i = 1, #files do
        local f = files[i]:lower()
        if string.find(f, "x3.xem") then
            table.insert(results, "Possível XignCode3 detectado")
        elseif string.find(f, "eac") then
            table.insert(results, "Possível EasyAntiCheat detectado")
        end
    end
    return results
end
""")

lua_func = lua.globals().analyze_files

def pylist_to_luatable(pylist):
    # Cria uma table do tipo Lua para o Lupa
    tbl = lua.table()
    for i, v in enumerate(pylist):
        tbl[i+1] = v  # Lua é 1-based!
    return tbl

def run_lua_heuristics(file_list):
    lua_files = pylist_to_luatable(file_list)
    return lua_func(lua_files)

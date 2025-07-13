import pefile
import os
from core.utils import read_file_strings
import math

LANG_KEYWORDS = [
    ("c++", ["msvcp", "msvcr", ".rdata", ".pdata", ".cpp", ".cxx"]),
    ("c", [".c", ".h", "msvcrt", "ucrtbase"]),
    ("c#", ["mscoree.dll", "clr", ".cs", "csharp"]),
    ("java", ["java", ".jar", ".class"]),
    ("lua", ["lua", ".lua", "luajit"]),
    ("python", ["python", ".py", ".pyc", "cpython", "python3"]),
    ("javascript", [".js", "node.js", "v8", "spidermonkey"]),
    ("typescript", [".ts", "typescript"]),
    ("rust", [".rs", "rust"]),
    ("gdscript", [".gd", "gdscript"]),
    ("hlsl", [".hlsl", ".fx"]),
    ("glsl", [".glsl", ".vert", ".frag"]),
]

ENGINE_KEYWORDS = [
    ("unreal engine", ["unrealengine", ".pak", "ue4", "ue5", "epicgames", "unreal"]),
    ("unity", ["unity", "globalgamemanagers", "unityplayer", "il2cpp", "mono", "unityengine"]),
    ("godot", ["godot", ".pck", "godotengine"]),
    ("cryengine", ["cryengine", "crytek"]),
    ("amazon lumberyard", ["lumberyard"]),
    ("source engine", ["sourceengine", "vpk", "valve", "source"]),
    ("frostbite", ["frostbite", "dice.se"]),
    ("id tech", ["idtech", "quake", "doom", "wolfenstein"]),
    ("construct", ["construct"]),
    ("gamemaker", ["gamemaker", "gml"]),
    ("rpg maker", ["rpg_rt.exe", "rpgmaker"]),
    ("phaser", ["phaser"]),
    ("three.js", ["three.js"]),
]

MIDDLEWARE_KEYWORDS = [
    ("directx", ["d3d", "dxgi", "direct3d", "dinput", "d3dx"]),
    ("opengl", ["opengl", "glew", "glfw"]),
    ("vulkan", ["vulkan"]),
    ("sdl", ["sdl"]),
    ("havok", ["havok"]),
    ("fmod", ["fmod"]),
    ("wwise", ["wwise"]),
    ("binkvideo", ["bink"]),
    ("miles sound", ["mss32"]),
    ("speedtree", ["speedtree"]),
    ("bullet physics", ["bullet"]),
    ("physx", ["physx"]),
    ("openal", ["openal"]),
]

MAGIC_BYTES = [
    ("elf", b"\x7fELF"),
    ("pe", b"MZ"),
    ("mach-o", b"\xcf\xfa\xed\xfe"),
]

def calculate_entropy(path):
    try:
        with open(path, 'rb') as f:
            data = f.read()
        if not data:
            return 0
        occurences = [0] * 256
        for b in data:
            occurences[b] += 1
        entropy = 0
        for occ in occurences:
            if occ:
                p = occ / len(data)
                entropy -= p * math.log2(p)
        return round(entropy, 2)
    except Exception:
        return 0

def detect_magic(path):
    try:
        with open(path, 'rb') as f:
            header = f.read(8)
        for name, magic in MAGIC_BYTES:
            if header.startswith(magic):
                return name
    except Exception:
        pass
    return None

def detect_languages(files, progress_callback=None):
    langs = set()
    engines = set()
    middlewares = set()
    lang_map, engine_map, mid_map = {}, {}, {}
    entropy_map = {}
    magic_map = {}

    for path in files:
        print(f"Analisando arquivo: {path}")
        base = os.path.basename(path).lower()
        ext = os.path.splitext(path)[1].lower()
        try:
            all_strings = set(read_file_strings(path))
        except Exception:
            all_strings = set()
        # Linguagens
        file_langs = set()
        for lang, terms in LANG_KEYWORDS:
            for term in terms:
                if term in base or term in ext or any(term in s.lower() for s in all_strings):
                    langs.add(lang)
                    file_langs.add(lang)
        if file_langs:
            lang_map[path] = list(file_langs)
        # Engines
        file_engines = set()
        for eng, terms in ENGINE_KEYWORDS:
            for term in terms:
                if term in base or term in ext or any(term in s.lower() for s in all_strings):
                    engines.add(eng)
                    file_engines.add(eng)
        if file_engines:
            engine_map[path] = list(file_engines)
        # Middlewares
        file_mids = set()
        for mid, terms in MIDDLEWARE_KEYWORDS:
            for term in terms:
                if term in base or term in ext or any(term in s.lower() for s in all_strings):
                    middlewares.add(mid)
                    file_mids.add(mid)
        if file_mids:
            mid_map[path] = list(file_mids)
        # Entropia
        entropy_map[path] = calculate_entropy(path)
        # Magic bytes
        magic_map[path] = detect_magic(path)
        # Progresso
        if progress_callback:
            progress_callback()
            print(f"Arquivo processado: {path}")

    return sorted(langs), lang_map, engine_map, mid_map, entropy_map, magic_map

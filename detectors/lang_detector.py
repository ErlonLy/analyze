import pefile
import os

LANG_KEYWORDS = [
    ("c++", ["msvcp", "msvcr", "rdata", "pdata"]),
    ("c#", ["mscoree.dll", "clr"]),
    ("java", ["java", ".jar", ".class"]),
    ("lua", ["lua", ".lua"]),
    ("python", ["python", ".py", ".pyc"]),
    ("javascript", [".js"]),
    ("typescript", [".ts"]),
    ("rust", ["rust"]),
    ("gdscript", [".gd"]),
    ("hlsl", [".hlsl"]),
    ("glsl", [".glsl"]),
]

ENGINE_KEYWORDS = [
    ("unreal engine", ["unrealengine", ".pak", "ue4", "ue5"]),
    ("unity", ["unity", "globalgamemanagers", "unityplayer"]),
    ("godot", ["godot", ".pck"]),
    ("cryengine", ["cryengine"]),
    ("amazon lumberyard", ["lumberyard"]),
    ("source engine", ["sourceengine", "vpk"]),
    ("frostbite", ["frostbite"]),
    ("id tech", ["idtech"]),
    ("construct", ["construct"]),
    ("gamemaker", ["gamemaker"]),
    ("rpg maker", ["rpg_rt.exe"]),
    ("phaser", ["phaser"]),
    ("three.js", ["three.js"]),
]

def detect_languages(files):
    langs = set()
    engines = set()
    lang_map = {}
    engine_map = {}
    for path in files:
        file_langs = set()
        file_engines = set()
        base = os.path.basename(path).lower()
        ext = os.path.splitext(path)[1].lower()
        for lang, terms in LANG_KEYWORDS:
            if any(term in base or term in ext for term in terms):
                langs.add(lang)
                file_langs.add(lang)
        for eng, terms in ENGINE_KEYWORDS:
            if any(term in base or term in ext for term in terms):
                engines.add(eng)
                file_engines.add(eng)
        if ext in [".exe", ".dll"]:
            try:
                pe = pefile.PE(path)
                if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                    for entry in pe.DIRECTORY_ENTRY_IMPORT:
                        dll = entry.dll.decode(errors="ignore").lower()
                        for lang, terms in LANG_KEYWORDS:
                            if any(t in dll for t in terms):
                                langs.add(lang)
                                file_langs.add(lang)
                        for eng, terms in ENGINE_KEYWORDS:
                            if any(t in dll for t in terms):
                                engines.add(eng)
                                file_engines.add(eng)
                section_names = [s.Name.strip(b"\x00") for s in pe.sections]
                if b".rdata" in section_names or b".pdata" in section_names:
                    langs.add("c++")
                    file_langs.add("c++")
            except Exception:
                pass
        if file_langs:
            lang_map[path] = sorted(file_langs)
        if file_engines:
            engine_map[path] = sorted(file_engines)
    all_tags = list(sorted(langs | engines))
    return list(sorted(langs)), lang_map, engine_map

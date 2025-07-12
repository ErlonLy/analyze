import pefile
import os

def detect_languages(files):
    langs = set()
    for path in files:
        ext = os.path.splitext(path)[1].lower()
        if ext in [".py", ".pyc"]:
            langs.add("Python")
        if ext == ".lua":
            langs.add("Lua")
        if ext in [".jar", ".class"]:
            langs.add("Java")
        if ext == ".pak":
            langs.add("Provável Unreal Engine (PAK)")
        if "unity" in path.lower() or "globalgamemanagers" in path.lower():
            langs.add("Provável Unity Engine")
        try:
            if ext in [".exe", ".dll"]:
                pe = pefile.PE(path)
                if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                    for entry in pe.DIRECTORY_ENTRY_IMPORT:
                        dll = entry.dll.decode(errors="ignore").lower()
                        if "mscoree.dll" in dll or "clr" in dll:
                            langs.add(".NET / C#")
                        if "lua" in dll:
                            langs.add("Lua (embutido)")
                        if "python" in dll:
                            langs.add("Python (embutido)")
                        if "java" in dll:
                            langs.add("Java (embutido)")
                # C++ (heurística bruta)
                section_names = [s.Name.strip(b"\x00") for s in pe.sections]
                if b".rdata" in section_names or b".pdata" in section_names:
                    langs.add("C++")
        except Exception:
            continue
    return list(langs)

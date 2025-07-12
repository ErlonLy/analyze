# detectors/lang_detector.py
import pefile

def detect_languages(files):
    langs = set()
    for path in files:
        try:
            pe = pefile.PE(path)
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    dll = entry.dll.decode().lower()
                    if "mscoree.dll" in dll or "clr" in dll:
                        langs.add(".NET / C#")
                    if "lua" in dll:
                        langs.add("Lua")
                    if "python" in dll:
                        langs.add("Python")
            if b".rdata" in pe.sections[0].Name:
                langs.add("C++")
        except Exception:
            continue
    return list(langs)

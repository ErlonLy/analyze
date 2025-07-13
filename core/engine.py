import json
from detectors.lang_detector import detect_languages
from detectors.protection import detect_protection
from detectors.crypto import detect_crypto
from core.lua_bridge import run_lua_heuristics
from core.scanner import list_all_files

def analyze_folder(folder_path, progress_callback=None):
    files = list_all_files(folder_path)
    exe_files = [f for f in files if f.lower().endswith((".exe", ".dll"))]
    steps = 5

    # Recebe listas + mapas de agrupamento
    languages_detected, lang_map, engine_map = detect_languages(files)
    protections, prot_map = detect_protection(exe_files)
    crypto_signals, crypto_map = detect_crypto(files)
    heuristics = run_lua_heuristics(files)

    result = {
        "game_path": folder_path,
        "executables": exe_files,
        "languages_detected": languages_detected,
        "protections": protections,
        "crypto_signals": crypto_signals,
        "lua_heuristics": list(heuristics) if heuristics else [],
        # Novos agrupamentos:
        "lang_map": lang_map,
        "engine_map": engine_map,
        "prot_map": prot_map,
        "crypto_map": crypto_map,
        "analyzed_files": len(files),
    }

    if progress_callback:
        progress_callback(100)
    return json.dumps(result, indent=2)

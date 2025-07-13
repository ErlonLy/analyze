import json
from detectors.lang_detector import detect_languages
from detectors.protection import detect_protection
from detectors.crypto import detect_crypto
from core.lua_bridge import run_lua_heuristics
from core.scanner import list_all_files

def analyze_folder(folder_path, progress_callback=None):
    files = list_all_files(folder_path)
    total_steps = len(files) * 3 + 2  # linguagens, proteções, cripto, heurística, finalização
    progress = 0

    def step():
        nonlocal progress
        progress += 1
        if progress_callback:
            percent = int(progress / total_steps * 100)
            progress_callback(percent)

    languages_detected, lang_map, engine_map, mid_map, entropy_map, magic_map = detect_languages(files, step)
    protections, prot_map = detect_protection(files, step)
    crypto_signals, crypto_map = detect_crypto(files, step)
    heuristics = run_lua_heuristics(files)
    result = {
        "game_path": folder_path,
        "executables": [f for f in files if f.lower().endswith((".exe", ".dll"))],
        "languages_detected": languages_detected,
        "protections": protections,
        "crypto_signals": crypto_signals,
        "lua_heuristics": list(heuristics) if heuristics else [],
        "lang_map": lang_map,
        "engine_map": engine_map,
        "middleware_map": mid_map,
        "entropy_map": entropy_map,
        "magic_map": magic_map,
        "prot_map": prot_map,
        "crypto_map": crypto_map,
        "analyzed_files": len(files),
    }
    if progress_callback:
        progress_callback(100)
    return json.dumps(result, indent=2)

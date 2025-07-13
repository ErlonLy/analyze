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
    result = {
        "game_path": folder_path,
        "executables": exe_files,
        "languages_detected": [],
        "protections": [],
        "crypto_signals": [],
        "lua_heuristics": []
    }
    if progress_callback:
        progress_callback(int(100 * 1 / steps))
    result["languages_detected"] = detect_languages(files)

    if progress_callback:
        progress_callback(int(100 * 2 / steps))
    result["protections"] = detect_protection(exe_files)

    if progress_callback:
        progress_callback(int(100 * 3 / steps))
    result["crypto_signals"] = detect_crypto(files)

    if progress_callback:
        progress_callback(int(100 * 4 / steps))
    heuristics = run_lua_heuristics(files)
    result["lua_heuristics"] = list(heuristics) if heuristics else []

    if progress_callback:
        progress_callback(100)
    return json.dumps(result, indent=2)

# core/engine.py
import os
import json
from core.scanner import list_all_files
from detectors.lang_detector import detect_languages
from detectors.protection import detect_protection
from detectors.crypto import detect_crypto
from core.lua_bridge import run_lua_heuristics

def analyze_folder(folder_path):
    files = list_all_files(folder_path)
    exe_files = [f for f in files if f.endswith((".exe", ".dll"))]

    result = {
        "game_path": folder_path,
        "executables": exe_files,
        "languages_detected": [],
        "protections": [],
        "crypto_signals": [],
        "lua_heuristics": []
    }

    result["languages_detected"] = detect_languages(exe_files)
    result["protections"] = detect_protection(exe_files)
    result["crypto_signals"] = detect_crypto(files)
    # Convertendo a tabela Lua para lista Python:
    heuristics = run_lua_heuristics(files)
    result["lua_heuristics"] = list(heuristics)  # <--- aqui!

    return json.dumps(result, indent=2)
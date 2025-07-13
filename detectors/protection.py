import yara
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

OBFUSCATION_KEYWORDS = [
    ("renomear_variaveis", ["obfuscat", "rename", "var_", "sym_"]),
    ("codigo_morto", ["deadcode", "dead_code"]),
    ("strings_codificadas", ["str_enc", "strdec", "decode", "encode", "xor", "base64"]),
    ("virtualizacao_codigo", ["vmprotect", "themida", "virtual", ".vmp"]),
    ("packing", ["upx", "asprotect", "pack", ".packed"]),
    ("alocacao_dinamica", ["malloc", "calloc", "alloc", "heap"]),
    ("pointer_swizzling", ["swizzle", "ptr_swap", "ptr_obf"]),
    ("anti_debug", ["isdebuggerpresent", "checkremotedebuggerpresent", "debug", "dbg"]),
    ("self_modifying_code", ["selfmod", "self_mod", "modify_code"]),
]

ANTI_CHEAT_KEYWORDS = [
    ("easy anti-cheat", ["eac", "easyanticheat"]),
    ("battleye", ["battleye", "beclient", "beservice"]),
    ("valve anti-cheat", ["vac", "valve anti-cheat"]),
    ("denuvo anti-cheat", ["denuvo"]),
    ("xigncode3", ["xigncode", "x3.xem"]),
]

EXTRA_TOOLS = [
    ("denuvo (drm)", ["denuvo"]),
    ("vmprotect", ["vmprotect", ".vmp"]),
    ("themida", ["themida"]),
    ("arxan", ["arxan"]),
]

def detect_protection(files, progress_callback=None):
    protections = set()
    prot_map = {}
    try:
        rules_path = resource_path("yara_rules/themida.yara")
        rules = yara.compile(filepath=rules_path)
        for f in files:
            try:
                matches = rules.match(f)
                for m in matches:
                    protections.add(m.rule)
                    prot_map.setdefault(f, []).append(m.rule)
            except Exception:
                continue
    except Exception:
        protections.add("Erro ao carregar regras YARA")
    for path in files:
        print(f"Analisando arquivo: {path}")
        base = os.path.basename(path).lower()
        found = set()
        for name, terms in OBFUSCATION_KEYWORDS:
            if any(term in base for term in terms):
                protections.add(name)
                found.add(name)
        for name, terms in ANTI_CHEAT_KEYWORDS:
            if any(term in base for term in terms):
                protections.add(name)
                found.add(name)
        for name, terms in EXTRA_TOOLS:
            if any(term in base for term in terms):
                protections.add(name)
                found.add(name)
        if found:
            existing = set(prot_map.get(path, []))
            prot_map[path] = list(existing | found)
        if progress_callback:
            progress_callback()
            print(f"Arquivo processado: {path}")
    return sorted(protections), prot_map

# detectors/protection.py
import yara

def detect_protection(files):
    protections = set()

    try:
        rules = yara.compile(filepath="yara_rules/themida.yara")
    except Exception:
        return ["Erro ao carregar regras YARA"]

    for f in files:
        try:
            matches = rules.match(f)
            for m in matches:
                protections.add(m.rule)
        except Exception:
            continue

    return list(protections)

# detectors/crypto.py
from core.utils import read_file_strings

def detect_crypto(files):
    signals = set()
    keywords = ["AES", "RSA", "SHA256", "blowfish", "xor", "encrypt", "decrypt"]

    for path in files:
        for s in read_file_strings(path):
            for k in keywords:
                if k.lower() in s.lower():
                    signals.add(k.upper())
    return list(signals)

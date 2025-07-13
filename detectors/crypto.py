from core.utils import read_file_strings

CRYPTO_KEYWORDS = [
    "aes", "des", "3des", "blowfish", "rc4", "rsa", "ecc", "md5",
    "sha1", "sha256", "crc32"
]

def detect_crypto(files):
    signals = set()
    crypto_map = {}
    for path in files:
        found = set()
        for s in read_file_strings(path):
            s_lower = s.lower()
            for k in CRYPTO_KEYWORDS:
                if k in s_lower:
                    signals.add(k.upper())
                    found.add(k.upper())
        if found:
            crypto_map[path] = list(found)
    return sorted(signals), crypto_map

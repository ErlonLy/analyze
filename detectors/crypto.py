from core.utils import read_file_strings

CRYPTO_KEYWORDS = [
    "aes", "des", "3des", "blowfish", "rc4", "rsa", "ecc", "md5",
    "sha1", "sha256", "crc32"
]

def detect_crypto(files):
    signals = set()
    for path in files:
        for s in read_file_strings(path):
            s_lower = s.lower()
            for k in CRYPTO_KEYWORDS:
                if k in s_lower:
                    signals.add(k.upper())
    return sorted(signals)

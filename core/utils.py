import re

def read_file_strings(file_path, limit=4096):
    try:
        with open(file_path, 'rb') as f:
            data = f.read(limit)
        # Strings ASCII e UTF-8
        found = set()
        for match in re.findall(rb'[\x20-\x7E]{4,}', data):
            found.add(match.decode('utf-8', 'ignore'))
        return list(found)
    except Exception:
        return []

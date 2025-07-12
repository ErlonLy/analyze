# core/utils.py
def read_file_strings(file_path, limit=2048):
    try:
        with open(file_path, 'rb') as f:
            data = f.read(limit)
            return [s.decode('utf-8', 'ignore') for s in data.split(b'\x00') if len(s) > 3]
    except Exception:
        return []

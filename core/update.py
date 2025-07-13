import requests
import os
import sys
import shutil

def download_new_version(url, dest_path, progress_callback=None):
    try:
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            with open(dest_path, 'wb') as f:
                downloaded = 0
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total:
                            progress_callback(downloaded, total)
        return True
    except Exception as e:
        return str(e)

def do_update(new_exe_path):
    current_exe = sys.executable
    backup_path = current_exe + ".bak"
    try:
        # Renomeia o .exe atual para backup
        os.rename(current_exe, backup_path)
        # Copia novo .exe no lugar do antigo
        shutil.copy2(new_exe_path, current_exe)
        # Remove o arquivo baixado
        os.remove(new_exe_path)
        # (Opcional) Remove o backup antigo
        # os.remove(backup_path)
        return True
    except Exception as e:
        return str(e)

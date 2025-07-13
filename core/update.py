import requests
import os
import sys

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

def run_batch_update(update_exe_path):
    current_exe = sys.executable
    batch_path = os.path.join(os.path.dirname(current_exe), "update_helper.bat")
    # Batch para esperar, mover update, relançar, deletar-se
    with open(batch_path, "w") as f:
        f.write(f"""@echo off
timeout /t 2 > nul
move /y "{update_exe_path}" "{current_exe}"
start "" "{current_exe}"
del "%~f0"
""")
    os.startfile(batch_path)

import subprocess
import json
import os

def run_cpp_scanner(file_path):
    exe_path = os.path.join(os.path.dirname(__file__), '../scanner/scanner.exe')
    process = subprocess.run(
        [exe_path, file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if process.returncode != 0:
        raise Exception(f"Erro: {process.stderr}")
    return json.loads(process.stdout)

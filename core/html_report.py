import os
import shutil
import json
import hashlib

def sha256sum(filename):
    h = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def export_html_report(data, export_dir="Relatorio_Loki", html_name="relatorio.html"):
    os.makedirs(export_dir, exist_ok=True)

    # Gera hashes
    file_hashes = {}
    for f in data.get("executables", []):
        try:
            file_hashes[os.path.basename(f)] = sha256sum(f)
        except Exception:
            file_hashes[os.path.basename(f)] = None
    data["file_hashes"] = file_hashes

    # Salva data.json
    with open(os.path.join(export_dir, "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Copia todos os assets para a pasta exportada
    src_assets = "./src"  # exemplo: "./src/assets" ou "./src"
    files_to_copy = [
    (os.path.join("html", "report_template.html"), html_name),
    (os.path.join("js", "chart.min.js"), "chart.min.js"),
    (os.path.join("js", "anime.min.js"), "anime.min.js"),
    (os.path.join("js", "loki_charts.js"), "loki_charts.js"),
    (os.path.join("css", "style.css"), "style.css"),
]
    for src, dst in files_to_copy:
        shutil.copy(os.path.join(src_assets, src), os.path.join(export_dir, dst))

    print(f"Relatório exportado em: {os.path.abspath(export_dir)}\\{html_name}")

import json
import hashlib
import os

def sha256sum(filename):
    if not os.path.exists(filename):
        print(f"Arquivo não encontrado: {filename}")
        return None
    try:
        h = hashlib.sha256()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        print(f"Erro ao gerar hash de {filename}: {e}")
        return None

def export_html_singlefile(data, output_html="relatorio.html"):
    if isinstance(data, str):
        data = json.loads(data)

    # Caminho absoluto para src (robusto)
    BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))

    # Leia os arquivos de assets das subpastas corretas
    with open(os.path.join(BASE, "css", "style.css"), "r", encoding="utf-8") as f:
        css = f.read()
    with open(os.path.join(BASE, "js", "chart.min.js"), "r", encoding="utf-8") as f:
        chartjs = f.read()
    with open(os.path.join(BASE, "js", "anime.min.js"), "r", encoding="utf-8") as f:
        animejs = f.read()

    # Seu JS de lógica pode estar em src/js/loki_charts.js
    with open(os.path.join(BASE, "js", "loki_charts.js"), "r", encoding="utf-8") as f:
        lokijs = f.read()

    # Gera hashes dos executáveis
    file_hashes = {}
    for filepath in data.get("executables", []):
        file_hashes[filepath] = sha256sum(filepath)
    data["file_hashes"] = file_hashes

    data_js = json.dumps(data, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Loki Analyzer - Relatório Detalhado</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
{css}
  </style>
</head>
<body>
  <div id="main-content">
    <h1>Loki Analyzer - Relatório Detalhado</h1>
    <div id="summary" class="summary-box"></div>
    <div class="chart-row">
      <div class="chartbox"><canvas id="pieLang"></canvas><div>Linguagens</div></div>
      <div class="chartbox"><canvas id="pieEngine"></canvas><div>Engines</div></div>
      <div class="chartbox"><canvas id="pieMid"></canvas><div>Middlewares</div></div>
      <div class="chartbox"><canvas id="pieProt"></canvas><div>Proteções</div></div>
      <div class="chartbox"><canvas id="pieCrypto"></canvas><div>Criptografia</div></div>
    </div>
    <div id="details"></div>
    <div id="hashes"></div>
    <footer>
      <span>Loki Analyzer &copy; 2025 Lyrien</span>
    </footer>
  </div>
  <script>
    // ---- Dados ----
    window.LOKI_DATA = {data_js};
  </script>
  <script>
{chartjs}
  </script>
  <script>
{animejs}
  </script>
  <script>
{lokijs}
  </script>
</body>
</html>
"""
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Relatório gerado: {output_html}")

# Exemplo de uso:
# export_html_singlefile(seu_resultado, "relatorio.html")

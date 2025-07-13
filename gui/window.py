import sys
import os
import json
import requests
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QTextEdit, QMessageBox, QTabWidget, QLabel
)
from core.engine import analyze_folder
from core.update import download_new_version, run_batch_update

GITHUB_VERSION_URL = "https://raw.githubusercontent.com/ErlonLy/analyze/main/latest_version.json"  # Troque para o seu repositório!

def get_local_version():
    try:
        with open("version.txt") as f:
            return f.read().strip()
    except Exception:
        return "0.0.0"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GameAnalyzer")
        self.resize(800, 600)
        self.tabs = QTabWidget()

        # Aba Principal
        self.tab_main = QWidget()
        self.layout_main = QVBoxLayout()
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.btn_select = QPushButton("Selecionar pasta do jogo")
        self.btn_select.clicked.connect(self.select_folder)
        self.btn_export = QPushButton("Exportar resultado")
        self.btn_export.clicked.connect(self.export_result)
        self.btn_export.setEnabled(False)
        self.layout_main.addWidget(self.btn_select)
        self.layout_main.addWidget(self.btn_export)
        self.layout_main.addWidget(self.result_area)
        self.tab_main.setLayout(self.layout_main)

        # Aba Sobre
        self.tab_about = QWidget()
        self.layout_about = QVBoxLayout()
        self.lbl_author = QLabel(f"Autor: <b>Lyrien</b><br>Versão atual: <b>{get_local_version()}</b>")
        self.btn_update = QPushButton("Verificar atualização")
        self.lbl_update = QLabel("")
        self.btn_update.clicked.connect(self.check_update)
        self.layout_about.addWidget(self.lbl_author)
        self.layout_about.addWidget(self.btn_update)
        self.layout_about.addWidget(self.lbl_update)
        self.layout_about.addStretch()
        self.tab_about.setLayout(self.layout_about)

        # Tabs
        self.tabs.addTab(self.tab_main, "Análise")
        self.tabs.addTab(self.tab_about, "Sobre")
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.last_json = ""

    def pretty_result(self, result_json):
        try:
            result = json.loads(result_json)
        except Exception:
            return result_json
        txt = f"""
<span style="color:#f5b042; font-weight:bold; font-size:13pt;">Caminho do Jogo:</span><br>
<span style="font-family:Consolas,monospace;">{result['game_path']}</span><br><br>
<span style="color:#5fcfff; font-weight:bold;">Executáveis/DLLs:</span><br>
<span style="font-family:Consolas,monospace;">{"<br>".join(str(x) for x in result["executables"])}</span><br><br>
<span style="color:#90ee90; font-weight:bold;">Linguagens/Engines Detectadas:</span><br>
{", ".join(str(x) for x in result["languages_detected"])}<br><br>
<span style="color:#ff8c8c; font-weight:bold;">Proteções e Ofuscação:</span><br>
{", ".join(str(x) for x in result["protections"])}<br><br>
<span style="color:#bb86fc; font-weight:bold;">Criptografia (sinais):</span><br>
{", ".join(str(x) for x in result["crypto_signals"])}<br><br>
<span style="color:#ffd700; font-weight:bold;">Heurísticas Lua:</span><br>
{", ".join(str(x) for x in result["lua_heuristics"])}<br>
"""
        return txt

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecione a pasta do jogo")
        if folder:
            result = analyze_folder(folder)
            self.last_json = result
            self.result_area.setHtml(self.pretty_result(result))  # <-- Troca para setHtml aqui!
            self.btn_export.setEnabled(True)

    def export_result(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(self, "Salvar resultado", "", "JSON (*.json);;TXT (*.txt)", options=options)
        if file:
            try:
                if file.endswith(".json"):
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(self.last_json)
                else:
                    # Exporta sem HTML se for TXT
                    import re
                    plain = re.sub(r'<[^>]+>', '', self.result_area.toHtml())
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(plain)
                QMessageBox.information(self, "Sucesso", "Arquivo salvo com sucesso!")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Não foi possível salvar: {e}")

    def check_update(self):
        self.lbl_update.setText("Verificando atualização...")
        def verif():
            try:
                resp = requests.get(GITHUB_VERSION_URL, timeout=10)
                if resp.status_code == 200:
                    latest = resp.json()
                    local = get_local_version()
                    if latest["version"] > local:
                        msg = f"<b>Nova versão disponível:</b> {latest['version']}<br>"
                        msg += f"<small>Atual:</small> {local}<br>"
                        self.lbl_update.setText(msg + "Baixando e atualizando...")
                        self.btn_update.setEnabled(False)
                        self.do_update(latest["url"], latest["version"])
                    else:
                        self.lbl_update.setText("Você já está na versão mais recente.")
                else:
                    self.lbl_update.setText("Não foi possível acessar o servidor.")
            except Exception as e:
                self.lbl_update.setText(f"Erro ao verificar atualização: {e}")
        threading.Thread(target=verif, daemon=True).start()

    def do_update(self, url, version):
        tmp_path = os.path.join(os.path.dirname(sys.executable), f"update_{version}.exe")
        def progress(done, total):
            pct = int((done/total)*100)
            self.lbl_update.setText(f"Baixando atualização: {pct}%")
        def finish():
            self.lbl_update.setText("Atualização baixada! Fechando para atualizar...")
            run_batch_update(tmp_path)
            QApplication.quit()
        def download_and_update():
            res = download_new_version(url, tmp_path, progress_callback=progress)
            if res is True:
                finish()
            else:
                self.lbl_update.setText(f"Erro ao baixar: {res}")
                self.btn_update.setEnabled(True)
        threading.Thread(target=download_and_update, daemon=True).start()

def set_dark_theme(app):
    dark_qss = """
    QWidget {
        background-color: #232629;
        color: #e0e0e0;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 12pt;
    }
    QTabWidget::pane {
        border: 1px solid #444;
        background: #181a1b;
    }
    QTabBar::tab {
        background: #32353a;
        color: #e0e0e0;
        border: 1px solid #181a1b;
        border-bottom: none;
        padding: 8px 20px;
        min-width: 110px;
        font-size: 11pt;
    }
    QTabBar::tab:selected {
        background: #1f2326;
        color: #f5b042;
        font-weight: bold;
        border-bottom: 2px solid #f5b042;
    }
    QTextEdit, QLineEdit {
        background: #2b2d31;
        color: #e0e0e0;
        border: 1px solid #3a3d41;
        border-radius: 6px;
        font-size: 11pt;
    }
    QPushButton {
        background-color: #31363b;
        color: #e0e0e0;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 7px 18px;
        font-size: 11pt;
    }
    QPushButton:hover {
        background-color: #474c50;
        color: #f5b042;
    }
    QPushButton:pressed {
        background-color: #1f2326;
    }
    QLabel {
        font-size: 11pt;
    }
    """
    app.setStyleSheet(dark_qss)

def start_gui():
    app = QApplication(sys.argv)
    set_dark_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

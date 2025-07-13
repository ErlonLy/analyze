import sys
import json
import requests
import threading
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QTextEdit,
    QMessageBox, QTabWidget, QLabel
)
from core.engine import analyze_folder
from core.update import download_new_version, run_batch_update

GITHUB_VERSION_URL = "https://raw.githubusercontent.com/ErlonLy/analyze/main/latest_version.json" # altere aqui!

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

    # ... (métodos pretty_result, select_folder, export_result) ...

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

def start_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

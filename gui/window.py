import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QTextEdit, QMessageBox, QTabWidget, QLabel, QProgressBar
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QPixmap
from core.engine import analyze_folder
from core.html_report import export_html_report

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_local_version():
    try:
        with open(resource_path("version.txt")) as f:
            return f.read().strip()
    except Exception:
        return "0.0.0"

class AnalyzeWorker(QThread):
    progress_changed = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, folder):
        super().__init__()
        self.folder = folder

    def run(self):
        result = analyze_folder(self.folder, progress_callback=self.update_progress)
        self.finished.emit(result)

    def update_progress(self, value):
        self.progress_changed.emit(value)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loki Analyzer")
        self.resize(800, 600)
        self.tabs = QTabWidget()

        # Aba Principal
        self.tab_main = QWidget()
        self.layout_main = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.layout_main.addWidget(self.progress_bar)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.btn_select = QPushButton("Selecionar pasta do jogo")
        self.btn_select.clicked.connect(self.select_folder)
        self.btn_export = QPushButton("Exportar resultado")
        self.btn_export.clicked.connect(self.export_result)
        self.btn_export.setEnabled(False)

        self.btn_export_html = QPushButton("Exportar HTML")
        self.btn_export_html.clicked.connect(self.export_html)
        self.btn_export_html.setEnabled(False)
        self.layout_main.addWidget(self.btn_export_html)


        self.layout_main.addWidget(self.btn_select)
        self.layout_main.addWidget(self.btn_export)
        self.layout_main.addWidget(self.btn_export_html)
        self.layout_main.addWidget(self.result_area)
        self.tab_main.setLayout(self.layout_main)

        # Aba Sobre (centralizado, com ícone)
        self.tab_about = QWidget()
        self.layout_about = QVBoxLayout()

        self.logo = QLabel()
        pixmap = QPixmap(resource_path("icon.ico"))
        if not pixmap.isNull():
            self.logo.setPixmap(pixmap.scaledToWidth(64, Qt.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)
        self.layout_about.addWidget(self.logo)

        self.lbl_author = QLabel(f"""
            <div style='text-align:center; margin-top:18px;'>
                <span style='font-size:15pt;'><b>Autor:</b> Lyrien</span><br>
                <span style='font-size:13pt;'><b>Versão atual:</b> {get_local_version()}</span><br><br>
                <span style='color:#f5b042; font-style:italic; font-size:11.5pt;'>
                    Esta ferramenta é para análise superficial de games e programas.<br>
                    Não me responsabilizo por seu uso.
                </span><br><br>
                <span style='color:#aaaaaa; font-size:10pt;'>Copyright (c) 2025 Lyrien</span>
            </div>
        """)
        self.lbl_author.setWordWrap(True)
        self.layout_about.addWidget(self.lbl_author)
        self.layout_about.addStretch()
        self.tab_about.setLayout(self.layout_about)

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
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.result_area.clear()
            self.btn_export.setEnabled(False)
            self.btn_export_html.setEnabled(False)
            self.worker = AnalyzeWorker(folder)
            self.worker.progress_changed.connect(self.progress_bar.setValue)
            def on_finished(result):
                self.last_json = result
                self.result_area.setHtml(self.pretty_result(result))
                self.progress_bar.setVisible(False)
                self.btn_export.setEnabled(True)
                self.btn_export_html.setEnabled(True)
            self.worker.finished.connect(on_finished)
            self.worker.start()

    def export_result(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(self, "Salvar resultado", "", "JSON (*.json);;TXT (*.txt)", options=options)
        if file:
            try:
                if file.endswith(".json"):
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(self.last_json)
                else:
                    import re
                    plain = re.sub(r'<[^>]+>', '', self.result_area.toHtml())
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(plain)
                QMessageBox.information(self, "Sucesso", "Arquivo salvo com sucesso!")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Não foi possível salvar: {e}")

    def export_html(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(self, "Salvar relatório HTML", "", "HTML (*.html)", options=options)
        if file:
            try:
                from core.html_report import export_html_report
                export_html_report(self.last_json, file)
                QMessageBox.information(self, "Sucesso", "Relatório HTML salvo com sucesso!")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Falha ao exportar HTML: {e}")


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
    QProgressBar {
        border: 1px solid #444;
        border-radius: 7px;
        background: #35383c;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #f5b042;
        width: 10px;
        margin: 0.5px;
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
    app.setWindowIcon(QIcon(resource_path("ico.ico")))
    window = MainWindow()
    window.setWindowIcon(QIcon(resource_path("ico.ico")))
    window.show()
    sys.exit(app.exec_())

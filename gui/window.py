import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QTextEdit, QMessageBox
from core.engine import analyze_folder
import json

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GameAnalyzer")
        self.resize(750, 500)

        self.layout = QVBoxLayout()
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        self.btn_select = QPushButton("Selecionar pasta do jogo")
        self.btn_select.clicked.connect(self.select_folder)

        self.btn_export = QPushButton("Exportar resultado")
        self.btn_export.clicked.connect(self.export_result)
        self.btn_export.setEnabled(False)

        self.layout.addWidget(self.btn_select)
        self.layout.addWidget(self.btn_export)
        self.layout.addWidget(self.result_area)
        self.setLayout(self.layout)
        self.last_json = ""

    def pretty_result(self, result_json):
        try:
            result = json.loads(result_json)
        except Exception:
            return result_json
        txt = f"Caminho do Jogo:\n{result['game_path']}\n\n"
        txt += f"Executáveis/DLLs:\n" + "\n".join(result["executables"]) + "\n\n"
        txt += f"Linguagens/Engines Detectadas:\n" + ", ".join(result["languages_detected"]) + "\n\n"
        txt += f"Proteções:\n" + ", ".join(result["protections"]) + "\n\n"
        txt += f"Criptografia (sinais):\n" + ", ".join(result["crypto_signals"]) + "\n\n"
        txt += f"Heurísticas Lua:\n" + ", ".join(str(x) for x in result["lua_heuristics"]) + "\n"
        return txt

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecione a pasta do jogo")
        if folder:
            result = analyze_folder(folder)
            self.last_json = result
            self.result_area.setPlainText(self.pretty_result(result))
            self.btn_export.setEnabled(True)

    def export_result(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(self, "Salvar resultado", "", "JSON (*.json);;TXT (*.txt)", options=options)
        if file:
            try:
                # Exporta o resultado "bonito" para txt, JSON para json
                if file.endswith(".json"):
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(self.last_json)
                else:
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(self.result_area.toPlainText())
                QMessageBox.information(self, "Sucesso", "Arquivo salvo com sucesso!")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Não foi possível salvar: {e}")

def start_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

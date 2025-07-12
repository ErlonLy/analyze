# gui/window.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QTextEdit
from core.engine import analyze_folder

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GameAnalyzer")
        self.resize(600, 400)

        self.layout = QVBoxLayout()
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        self.btn_select = QPushButton("Selecionar pasta do jogo")
        self.btn_select.clicked.connect(self.select_folder)

        self.layout.addWidget(self.btn_select)
        self.layout.addWidget(self.result_area)
        self.setLayout(self.layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecione a pasta do jogo")
        if folder:
            result = analyze_folder(folder)
            self.result_area.setPlainText(result)

def start_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

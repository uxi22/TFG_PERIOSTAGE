import sys

from PyQt6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QValidator, QIntValidator
from PySide6.QtWidgets import QLabel, QApplication, QWidget, QGridLayout, QLineEdit





class Tabla(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # Números de dientes
        for i in range(18, 10, -1):
            grid.addWidget(QLabel(str(i)), 0, 18 - i)
        # Movilidad
        movilidadInputs = []
        for i in range(18, 10, -1):
            validator = QRegularExpressionValidator(QRegularExpression(r"[0-3]"))
            val: QValidator = validator
            grid.addWidget(QLineEdit().setValidator(val), 1, 18 - i)

        # Establecer diferentes anchos para cada columna
        for i in range(18, 10, -1):
            grid.setColumnStretch(18-i, i*500)  # Columna 0 con ancho 1
        self.setWindowTitle('Tabla con Anchos de Columna Diferentes')
        self.show()


app = QApplication(sys.argv)
window = Tabla()
window.show()
app.exec()

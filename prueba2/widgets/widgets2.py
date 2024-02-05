import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow
)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        self.setFixedSize(550, 430)
        #widgets
        label = QLabel("Hola!")
        label.setText("Adios!")
        font = label.font() #coge la fuente predeterminada
        font.setPointSize(20)  #le cambia el tamaño
        label.setFont(font) #cambiamos la fuente del label a la nueva con el tam cambiado
        label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter) #lo situamos centrado
        #alignVcenter es verticalmente, alignHcenter, horizontalmente, alignCenter, ambos
        label.setPixmap(QPixmap('../otje.jpg')) #añadir una foto en el label
        label.setScaledContents(True)
        label.setFixedSize(300, 300)

        self.setCentralWidget(label)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
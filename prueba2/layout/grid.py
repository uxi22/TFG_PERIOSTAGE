import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout
from PySide6.QtGui import QPalette, QColor

#creamos un widget nuevo
class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        #rellena el fondo del widget
        self.setAutoFillBackground(True)

        #cogemos la paleta de colores del sistema por defecto
        palette = self.palette()
        #y la cambiamos
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layout = QGridLayout()

        layout.addWidget(Color('red'), 0, 3)
        layout.addWidget(Color('green'), 1, 1)
        layout.addWidget(Color('blue'), 2, 2)
        layout.addWidget(Color('purple'), 3, 0)
        layout.setSpacing(0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
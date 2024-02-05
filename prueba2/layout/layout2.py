import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPalette, QColor

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
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()

        layout2.addWidget(Color('red'))
        layout2.addWidget(Color('yellow'))
        layout2.addWidget(Color('purple'))
        layout2.setContentsMargins(0, 0, 0, 0)  # margenes del layout, left top right bottom
        layout2.setSpacing(0)  # espacio entre los elementos del layout

        layout1.addLayout(layout2)

        layout1.addWidget(Color('green'))

        layout3.addWidget(Color('red'))
        layout3.addWidget(Color('purple'))

        layout1.addLayout(layout3)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

"""
h = QApplication.instance().
if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()
    """
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

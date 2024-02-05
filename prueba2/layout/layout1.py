import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
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

        layout = QVBoxLayout() #tb QHBoxLayout o QGridLayout
        widgets = [Color("red"), Color("green"), Color("orange"), Color("blue")]
        for widget in widgets:
            layout.addWidget(widget)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
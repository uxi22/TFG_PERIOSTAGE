import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    #evento que se lanza al pulsar el botón derecho
    def contextMenuEvent(self, e):
        context = QMenu(self)
        #opciones que aparecen en el context menu
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos()) #le pasamos la posición inicial al exec -> lugar en el que tiene que desplegarse el menu

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
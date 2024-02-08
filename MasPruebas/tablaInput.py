import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QFrame, QWidget, QHBoxLayout
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Creamos un widget contenedor
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Creamos un layout vertical para el widget contenedor
        layout = QVBoxLayout(central_widget)

        # Creamos un layout horizontal para las imágenes
        layout_imagenes = QHBoxLayout()

        # Creamos widgets para las imágenes y los agregamos al layout horizontal
        for i in range(5):
            imagen_label = QLabel()
            pixmap = QPixmap(100, 100)
            pixmap.fill(QColor(Qt.red))  # Simulamos una imagen roja
            imagen_label.setPixmap(pixmap)
            layout_imagenes.addWidget(imagen_label)

        # Agregamos el layout de imágenes al layout vertical
        layout.addLayout(layout_imagenes)

        # Creamos una línea horizontal
        linea = QFrame(frameShape=QFrame.HLine)
        linea.setStyleSheet("QFrame { background-color: rgba(0, 0, 0, 0.5); }")  # Establecemos el color de la línea con opacidad reducida
        layout.addWidget(linea)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

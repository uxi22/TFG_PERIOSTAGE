from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PySide6.QtCore import QSize, Qt

# Only needed for access to command line arguments
import sys

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        # Para permitir q Qt configure el objeto
        super().__init__()

        #variable para guardar el estado del botón
        self.button_is_checked = True

        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.boton_toggled)

        self.button.released.connect(self.the_button_was_released)

        self.button.setChecked(self.button_is_checked)

        #tamaño fijado
        #self.setFixedSize(QSize(400, 300))
        #tamaños minimos o maximos
        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(700, 500))

        # Set the central widget of the Window.
        # por defecto ocupa toda la pantalla
        self.setCentralWidget(self.button)

    #estado del botón, va cambiando con cada click
    """def boton_toggled(self, checked):
        self.button_is_checked = checked
        print("checked", self.button_is_checked)
        """

    def the_button_was_released(self):
        self.button_is_checked = self.button.isChecked()
        print("released", self.button_is_checked)


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

#window = QWidget()
window = MainWindow()
window.show()

# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.

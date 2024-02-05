import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLabel, QVBoxLayout, QDialogButtonBox


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")

        #se añaden con or todos los botones que queremos que aparezcan en la pantalla de dialogo
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        #creamos una box que contenga a los botones
        self.buttonBox = QDialogButtonBox(QBtn)
        #conectamos las señales adecuadas con las acciones a realizar
        self.buttonBox.accepted.connect(self.accept)  #accept y reject están en QDialog
        self.buttonBox.rejected.connect(self.reject)

        #añadimos los botones a un layout
        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        print("click", s)
        #aqui ponemos la acción que se tiene que ejecutar al pulsar el boton
        #en este caso la creación del dialogo
        dlg = CustomDialog(self) # se establece la pantalla ppal como padre
        #esto bloquea la interacción con la otra ventana
        dlg.setWindowTitle("HELLO!")

        #crea un nuevo event loop para esta nueva ventana
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
import sys

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget, QListWidget,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        layout = QVBoxLayout()
        widgets = [
            QCheckBox,
            QDateEdit,
            QDateTimeEdit,
            QDial,
            QDoubleSpinBox,
            QFontComboBox, #tipo de letra
            QLCDNumber, #no se
            QLabel,
            QLineEdit,
            QProgressBar,
            QPushButton,
            QRadioButton,
            QSlider, # cuando no es necesaria la precisión
            QSpinBox,
            QTimeEdit,
        ]

        for widget in widgets:
            layout.addWidget(widget())

        # desplegable
        combobox = QComboBox()
        combobox.addItems(["uno", "dos", "tres"])

        #para que el usuario pueda introducir una opción no proporcionada
        combobox.setEditable(True)
        combobox.setInsertPolicy(QComboBox.InsertAlphabetically)
        combobox.setMaxCount(5)
        #hay mas opciones de configuración

        layout.addWidget(combobox)

        listwidget = QListWidget()
        listwidget.addItems(["One", "Two", "Three"])

        layout.addWidget(listwidget)


        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
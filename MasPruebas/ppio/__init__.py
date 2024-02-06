import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import (
    QApplication,
    QDateEdit,
    QLabel,
    QLineEdit,
    QMainWindow,
    QRadioButton,
    QVBoxLayout,
    QWidget, QHBoxLayout, QSpacerItem,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Periostage")
        self.screen = QScreen().geometry()

        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(self.screen.width(), self.screen.height()))
        # self.setFixedSize(QSize(1200, 600))
        self.resize(QSize(1000, 600))

        self.info1()

    def info1(self):
        # TITULO
        tit = QHBoxLayout()
        titu = QLabel('PERIODONTOGRAMA')
        tit.addWidget(titu)

        # PREVIO
        fecha1 = QHBoxLayout()
        fecha1.addWidget(QLabel('Fecha: '))
        fecha1.addWidget(QDateEdit())
        fecha1.setSpacing(0)

        self.examenIni = QRadioButton('Examen Inicial')
        self.reev = QRadioButton('Reevaluación')
        layExamen = QHBoxLayout()
        layExamen.addWidget(self.examenIni)
        layExamen.addWidget(self.reev)
        layExamen.setSpacing(10)

        layout1 = QHBoxLayout()
        layout1.addLayout(fecha1)
        layout1.addItem(QSpacerItem(float(self.frameSize().width())/3.0, 20))
        layout1.addLayout(layExamen)
        layout1.setContentsMargins(80, 20, 50, 20)

        # ODONTOLOGO

        layout2 = QHBoxLayout()
        layout2.addWidget(QLabel('Odontólogo:'))
        self.inputOdontologo = QLineEdit()
        self.inputOdontologo.setPlaceholderText("Nombre Apellido1 Apellido2")
        layout2.addWidget(self.inputOdontologo)
        layout2.setContentsMargins(80, 0, 50, 10)


        ### PACIENTE

        layoutPaciente = QVBoxLayout()
        layoutPaciente.addWidget(QLabel("Paciente: "))

        layout3 = QHBoxLayout()

        nombrePaciente = QHBoxLayout()
        nombrePaciente.addWidget(QLabel('Nombre:'))
        self.inputPaciente = QLineEdit()
        self.inputPaciente.setPlaceholderText("Nombre Apellido1 Apellido2")
        layout3.addWidget(self.inputPaciente)

        nacimientoPaciente = QHBoxLayout()
        nacimientoPaciente.addWidget(QLabel('Fecha: '))
        nacimientoPaciente.addWidget(QDateEdit())
        layout3.addLayout(nacimientoPaciente)
        layout3.setSpacing(20)
        layoutPaciente.addLayout(layout3)

        layout4 = QHBoxLayout()

        self.tratSi = QRadioButton('Sí')
        self.tratNo = QRadioButton('No')
        tratamientoPrevio = QHBoxLayout()
        tratamientoPrevio.addWidget(QLabel('Tratamiento previo'))
        tratamientoPrevio.addWidget(self.tratSi)
        tratamientoPrevio.addWidget(self.tratNo)
        tratamientoPrevio.setSpacing(10)
        layout4.addLayout(tratamientoPrevio)

        layout4.addSpacerItem(QSpacerItem(150, 20))

        self.colapsoSi = QRadioButton('Sí')
        self.colapsoNo = QRadioButton('No')
        colapsoMordida = QHBoxLayout()
        colapsoMordida.addWidget(QLabel('Colapso de mordida'))
        colapsoMordida.addWidget(self.colapsoSi)
        colapsoMordida.addWidget(self.colapsoNo)
        layout4.addLayout(colapsoMordida)
        layoutPaciente.addLayout(layout4)

        layout5 = QHBoxLayout()
        self.fumadorNo = QRadioButton('Sí')
        self.fumadorSi = QRadioButton('No')
        self.fumadorEx = QRadioButton('Ex')
        layout5.addWidget(QLabel('Fumador'))
        layout5.addWidget(self.fumadorSi)
        layout5.addWidget(self.fumadorNo)
        layout5.addWidget(self.fumadorEx)
        layoutPaciente.addLayout(layout5)

        layoutPaciente.setContentsMargins(80, 0, 50, 10)

        total = QVBoxLayout()
        total.addLayout(tit)
        tit.setAlignment(Qt.AlignCenter)
        total.addLayout(layout1)
        total.addLayout(layout2)
        total.addLayout(layoutPaciente)

        widget = QWidget()
        widget.setLayout(total)
        total.setAlignment(Qt.AlignTop)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

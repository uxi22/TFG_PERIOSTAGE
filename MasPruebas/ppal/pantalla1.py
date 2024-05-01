import os
import sys

from PySide6 import QtGui
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtWidgets import (
    QApplication,
    QDateEdit,
    QLabel,
    QLineEdit,
    QMainWindow,
    QRadioButton,
    QVBoxLayout,
    QFrame,
    QWidget, QHBoxLayout, QSpacerItem,
    QPushButton
)

style = "margin: 0.5px; border: 1px solid grey; border-radius: 3px;"

basedir = os.path.dirname(__file__)
basedir = os.path.join(basedir, os.pardir)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Periostage")
        self.setStyleSheet("background-color: #ECECEC ")
        self.setMinimumSize(QSize(1000, 500))
        self.resizeEvent = self.actualizar_tam

        # TITULO
        self.frameTitulo = QFrame(self)
        self.frameTitulo.setStyleSheet("text-align: center;")
        self.frameTitulo.setGeometry(0, 40, self.width(), 80)

        self.titu = QLabel(self.frameTitulo)
        self.titu.setText("Periodontograma")
        self.titu.setStyleSheet("font-family: Alata; font-size: 26px; font-weight: 400; color: black;")
        self.titu.adjustSize()
        self.titu.setGeometry(QRect((self.width() - self.titu.width()) // 2, 10, self.titu.width(), self.titu.height()))
        self.frameTitulo.show()

        self.info1()

    def info1(self):
        self.framePpal = QFrame(self)
        self.framePpal.setGeometry(180, 100, self.width() - 180*2, self.height() - 80)
        self.framePpal.setStyleSheet("font-family: Alata; background-color: pink; border-radius: 12px;"
                                     "justify-content: center; align-items: center; display: inline-flex")

        self.framePpal.show()

        self.frameFecha = QFrame(self.framePpal)
        self.frameFecha.setGeometry(0, 0, 350, 50)
        self.frameFecha.setStyleSheet(
            "font-size: 16px; font-weight: 300; color: black; background-color: #DBDBDB;")

        # FECHA
        layfecha = QHBoxLayout(self.frameFecha)
        layfecha.setAlignment(Qt.AlignLeft)
        layfecha.setSpacing(20)
        fecha1 = QLabel("Fecha: ")
        fecha1.setStyleSheet("margin-left: 20px; font-size: 20px;")
        fecha2 = QDateEdit()
        fecha2.setGeometry(0, 0, 200, 40)
        fecha2.setDate(fecha2.date().currentDate())
        fecha2.setCalendarPopup(True)
        fecha2.setStyleSheet("background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 14px;")
        layfecha.addWidget(fecha1)
        layfecha.addWidget(fecha2)

        # PREVIO
        self.frameExIni = QFrame(self.framePpal)
        self.frameExIni.setGeometry(self.framePpal.width() - 500, 0, 500, 50)
        self.frameExIni.setStyleSheet("background-color: #DBDBDB;")

        self.examen_inicial = True
        self.examenIni = QRadioButton("Examen inicial")
        self.examenIni.setStyleSheet("margin-left: 20px; font-size: 20px;")
        self.reev = QRadioButton("Reevaluación")
        self.reev.setStyleSheet("margin-right: 20px; font-size: 20px;")

        layExamen = QHBoxLayout(self.frameExIni)
        layExamen.setAlignment(Qt.AlignCenter)
        layExamen.addWidget(self.examenIni)
        layExamen.addWidget(self.reev)
        layExamen.setSpacing(40)
        self.examenIni.setChecked(True)
        self.examenIni.clicked.connect(lambda: self.click_examenini(1))

        # ODONTOLOGO
        self.frameOdont = QFrame(self.framePpal)
        self.frameOdont.setGeometry(0, 60, self.framePpal.width(), 50)
        self.frameOdont.setStyleSheet("background-color: #DBDBDB;")

        layodont = QHBoxLayout(self.frameOdont)
        layodont.setAlignment(Qt.AlignLeft)
        layodont.setSpacing(20)
        label = QLabel("Odontólogo: ")
        label.setStyleSheet("font-size: 20px; margin-left: 20px;")
        layodont.addWidget(label)
        inputOdont = QLineEdit()
        inputOdont.setPlaceholderText("Nombre Apellido1 Apellido2")
        inputOdont.setStyleSheet("background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 17px; margin-right: 30px;")
        inputOdont.setGeometry(0, 0, 220, 40)
        layodont.addWidget(inputOdont)

        # PACIENTE
        labpaciente = QLabel("Paciente: ", self.framePpal)
        labpaciente.setGeometry(20, 120, 400, 40)
        labpaciente.setStyleSheet("font-size: 20px; font-weight: 300;")

        self.framePacienteTodo = QFrame(self.framePpal)
        self.framePacienteTodo.setGeometry(0, 160, self.framePpal.width(), 50)

        self.framePaciente = QFrame(self.framePacienteTodo)
        self.framePaciente.setGeometry(0, 0, 550, 50)
        self.framePaciente.setStyleSheet("background-color: #DBDBDB;")

        laypaciente = QHBoxLayout(self.framePaciente)
        laypaciente.setAlignment(Qt.AlignLeft)
        laypaciente.setSpacing(20)
        labelpaciente = QLabel("Nombre: ")
        labelpaciente.setStyleSheet("font-size: 20px; margin-left: 20px;")
        laypaciente.addWidget(labelpaciente)
        inputPaciente = QLineEdit()
        inputPaciente.setPlaceholderText("Nombre Apellido1 Apellido2")
        inputPaciente.setStyleSheet("background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 17px; margin-right: 30px;")
        laypaciente.addWidget(inputPaciente)

        self.frameNacimiento = QFrame(self.framePacienteTodo)
        self.frameNacimiento.setGeometry(self.framePacienteTodo.width() - 300, 0, 300, 50)
        self.frameNacimiento.setStyleSheet("background-color: #DBDBDB;")
        laynacimiento = QHBoxLayout(self.frameNacimiento)
        laynacimiento.setAlignment(Qt.AlignLeft)
        laynacimiento.setSpacing(20)
        labelnacimiento = QLabel("Nacimiento: ")
        labelnacimiento.setStyleSheet("font-size: 20px; margin-left: 20px;")
        laynacimiento.addWidget(labelnacimiento)
        inputNacimiento = QDateEdit()
        inputNacimiento.setGeometry(0, 0, 200, 40)
        inputNacimiento.setStyleSheet("background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 17px; margin-right: 30px;")
        laynacimiento.addWidget(inputNacimiento)

        # PREGUNTAS RÁPIDAS


        """
    
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

        botonSiguiente = QPushButton("Siguiente")
        layoutBoton = QHBoxLayout()
        layoutBoton.addWidget(botonSiguiente)
        layoutBoton.setAlignment(Qt.AlignRight)
        layoutBoton.setContentsMargins(0, 0, 50, 0)

        total = QVBoxLayout()
        total.addLayout(layout1)
        total.addLayout(layout2)
        total.addLayout(layoutPaciente)
        total.addLayout(layoutBoton)

        widget = QWidget()
        widget.setLayout(total)
        total.setAlignment(Qt.AlignTop)
        self.setCentralWidget(widget)
        """

    def actualizar_tam(self, event):
        self.titu.setGeometry(QRect((self.width() - self.titu.width()) // 2, 10, self.titu.width(), self.titu.height()))
        self.frameTitulo.setGeometry(0, 40, self.width(), 80)
        self.framePpal.setGeometry(220, 100, self.width() - 220*2, self.height() - 80)
        self.frameExIni.setGeometry(self.framePpal.width() - 500, 0, 500, 50)
        self.frameOdont.setGeometry(0, 60, self.framePpal.width(), 50)
        self.framePacienteTodo.setGeometry(0, 160, self.framePpal.width(), 50)
        self.frameNacimiento.setGeometry(self.framePacienteTodo.width() - 350, 0, 350, 50)







    def click_examenini(self, tipo):
        if tipo == 1:
            self.examen_inicial = True
        else:
            self.examen_inicial = False


app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'diente.ico')))
window = None
window = MainWindow()
window.showMaximized()
window.show()
app.exec()

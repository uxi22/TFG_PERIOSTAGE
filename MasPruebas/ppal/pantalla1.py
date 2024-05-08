import os
import sys

from PyQt6.QtGui import QFontMetrics, QFont
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

class Fumador(QFrame):
    def __init__(self, parent, coordenadas, wtotal):
        super().__init__(parent)
        self.setGeometry(coordenadas[0], coordenadas[1], coordenadas[2], coordenadas[3])
        # self.setStyleSheet("background-color: #DBDBDB; font-size: 18px;")

        self.wtotal = wtotal

        self.coordenadas = coordenadas

        self.framePreguntaPpal = RecuadroPreguntaRadio(self, [0, 0, coordenadas[2], 50], "Fumador", ["Sí", "No", "Ex"], 20)
        self.botones = self.framePreguntaPpal.getOpciones()

        self.frameSubpreguntaSi = QFrame(self)
        self.frameSubpreguntaSi.setGeometry(0, 50, wtotal, 50)
        self.frameMesesFum = PreguntaInput(self.frameSubpreguntaSi, "Meses fumando:", [0, 0, int((wtotal - 10) / 3), 50], 60, 10, "0")
        self.frameSesDia = PreguntaInput(self.frameSubpreguntaSi, "Cigarros o sesiones/día:", [int((wtotal - 10) / 3) + 5, 0, int((wtotal - 10) / 3), 50], 60, 10, "0")
        self.frameDuracionSesion = PreguntaInput(self.frameSubpreguntaSi, "Minutos/sesión:", [int(2 * (wtotal - 10) / 3) + 10, 0, int((wtotal - 10) / 3), 50], 60, 10, "0")

        self.frameSubpreguntaSi.hide()

        self.frameSubpreguntaEx = QFrame(self)
        self.frameSubpreguntaEx.setGeometry(0, 50, wtotal, 50)
        self.frameMesesSinFum = PreguntaInput(self.frameSubpreguntaEx, "Meses sin fumar:", [0, 0, 300, 50], 60, 10, "0")
        self.frameSubpreguntaEx.hide()

        self.botones[0].toggled.connect(self.subpregunta)
        self.botones[-1].toggled.connect(self.subpregunta)
        self.botones[1].setChecked(True)

    def subpregunta(self):
        if self.botones[0].isChecked():  # Sí
            self.setGeometry(self.coordenadas[0], self.coordenadas[1], self.wtotal, 100)
            self.frameSubpreguntaEx.hide()
            self.frameSubpreguntaSi.show()
        elif self.botones[-1].isChecked():  # Ex
            self.setGeometry(self.coordenadas[0], self.coordenadas[1], self.wtotal, 100)
            self.frameSubpreguntaSi.hide()
            self.frameSubpreguntaEx.show()
        else:
            self.setGeometry(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], 50)
            self.frameSubpreguntaSi.hide()
            self.frameSubpreguntaEx.hide()

    def actualizarw(self, width, wtotal):
        self.coordenadas[2] = width
        self.wtotal = wtotal
        self.setGeometry(self.coordenadas[0], self.coordenadas[1], width, 50)
        self.framePreguntaPpal.setGeometry(0, 0, width, 50)
        self.framePreguntaPpal.widthOpciones(width)
        self.frameSubpreguntaSi.setGeometry(0, 50, wtotal, 50)
        self.frameMesesFum.actualizarGeometry([0, 0, int((wtotal - 10) / 3), 50])
        self.frameSesDia.actualizarGeometry([int((wtotal - 10) / 3) + 5, 0, int((wtotal - 10)/ 3), 50])
        self.frameDuracionSesion.actualizarGeometry([int(2 * (wtotal - 10) / 3) + 10, 0, int((wtotal - 10) / 3), 50])

    def actualizarh(self, height):
        self.coordenadas[1] += height
        self.setGeometry(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], 50)

class PreguntaInput(QFrame):
    def __init__(self, parent, pregunta, geometry, widthinput, spacing=20, placeholder=""):
        super().__init__(parent)
        self.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
        self.setStyleSheet("background-color: #DBDBDB; font-size: 18px;")
        layinput = QHBoxLayout(self)
        layinput.setAlignment(Qt.AlignLeft)
        layinput.setSpacing(spacing)
        label = QLabel(pregunta)
        label.setStyleSheet("margin-left: 20px;")
        layinput.addWidget(label)
        input = QLineEdit()
        input.setPlaceholderText(placeholder)
        input.setStyleSheet(
            "background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 17px; margin-right: 16px;"
        )
        input.setGeometry(0, 0, widthinput, 40)
        layinput.addWidget(input)

    def actualizarGeometry(self, geometry):
        self.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])


class TratPrevio(QFrame):
    def __init__(self, parent, w):
        super().__init__(parent)
        self.setGeometry(0, 0, w, 50)
        self.setStyleSheet("background-color: #DBDBDB;")

        self.w = w

        self.framePreguntaPpal = RecuadroPreguntaRadio(self, [0, 0, w, 50], "Tratamiento previo", ["Sí", "No"], 20)
        self.botones = self.framePreguntaPpal.getOpciones()

        """self.frameSubpregunta = QFrame(self)
        self.frameSubpregunta.setGeometry(0, 45, w, 35)
        self.frameSubpregunta.setStyleSheet("font-size: 14px;")
        layoutSubpregunta = QHBoxLayout(self.frameSubpregunta)
        layoutSubpregunta.setAlignment(Qt.AlignCenter)
        opciones = ["Básico", "Quirúrgico", "Ambas"]
        for i in range(len(opciones)):
            b = QRadioButton(opciones.pop(0))
            layoutSubpregunta.addWidget(b)
        self.frameSubpregunta.hide()  # no lo hacemos visible y no ocupa espacio en la pantalla"""

        self.frameSubpregunta = RecuadroPreguntaRadio(self, [0, 40, w, 40], "", ["Básico", "Quirúrgico", "Ambas"], 10, 14)
        self.frameSubpregunta.hide()

        # Acciones de los botones
        self.botones[0].toggled.connect(self.subpregunta)
        self.botones[-1].setChecked(True)

    def actw(self, w):
        self.w = w
        self.setGeometry(0, 0, w, 50)
        self.framePreguntaPpal.setGeometry(0, 0, w, 50)
        self.framePreguntaPpal.widthOpciones(w)
        self.frameSubpregunta.setGeometry(0, 45, w, 35)
        self.frameSubpregunta.widthOpciones(w)

    def subpregunta(self):
        if window:
            window.desplazarFrames(self.botones[0].isChecked())
        if self.botones[0].isChecked():
            self.setGeometry(0, 0, self.w, 80)
            self.frameSubpregunta.show()
        else:
            self.setGeometry(0, 0, self.w, 50)
            self.frameSubpregunta.hide()


class RecuadroPreguntaRadio(QFrame):
    def __init__(self, parent, coordenadas, pregunta, opciones, spacing=20, fs=18):
        super().__init__(parent)
        self.setGeometry(coordenadas[0], coordenadas[1], coordenadas[2], coordenadas[3])
        self.setStyleSheet("background-color: #DBDBDB; font-size: " + str(fs) + "px; border-radius: 7px; justify-content: center")
        self.layouttotal = QHBoxLayout(self)
        self.layouttotal.setAlignment(Qt.AlignLeft)

        self.pregunta = QLabel(pregunta)
        self.pregunta.setStyleSheet("margin-left: 20px;")
        self.layouttotal.addWidget(self.pregunta)

        self.wp = QFontMetrics(QFont("Alata", fs)).horizontalAdvance(pregunta)
        if self.wp > 0:
            self.wp += 20

        self.frameOpciones = QFrame(self)
        self.frameOpciones.setGeometry(self.wp, 0, self.width() - self.wp, 50)
        layOpciones = QHBoxLayout(self.frameOpciones)
        layOpciones.setAlignment(Qt.AlignCenter)
        layOpciones.setSpacing(spacing)

        self.opciones = []
        for i in range(len(opciones)):
            b = QRadioButton(opciones[i])
            layOpciones.addWidget(b)
            self.opciones.append(b)
        self.opciones[0].setChecked(True)

    def getOpciones(self):
        return self.opciones

    def widthOpciones(self, w):
        self.frameOpciones.setGeometry(self.wp, 0, w - self.wp, 50)


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
        self.frameTitulo.setGeometry(0, 40, self.width(), 60)

        self.titu = QLabel(self.frameTitulo)
        self.titu.setText("Periodontograma")
        self.titu.setStyleSheet("font-family: Alata; font-size: 26px; font-weight: 400; color: black;")
        self.titu.adjustSize()
        self.titu.setGeometry(QRect((self.width() - self.titu.width()) // 2, 10, self.titu.width(), self.titu.height()))
        self.frameTitulo.show()

        self.info1()

    def info1(self):
        self.framePpal = QFrame(self)
        self.framePpal.setGeometry(220, 100, self.width() - 220 * 2, self.height() - 80)
        self.framePpal.setStyleSheet("font-family: Alata; border-radius: 12px;"
                                     "justify-content: center; align-items: center; display: inline-flex")

        self.framePpal.show()

        # FECHA EXAMEN
        self.frameFecha = QFrame(self.framePpal)
        self.frameFecha.setGeometry(0, 0, 350, 50)
        self.frameFecha.setStyleSheet(
            "font-size: 16px; font-weight: 300; color: black; background-color: #DBDBDB;")

        layfecha = QHBoxLayout(self.frameFecha)
        layfecha.setAlignment(Qt.AlignLeft)
        layfecha.setSpacing(20)
        fecha1 = QLabel("Fecha: ")
        fecha1.setStyleSheet("margin-left: 20px; font-size: 18px;")
        fecha2 = QDateEdit()
        fecha2.setGeometry(0, 0, 200, 40)
        fecha2.setDate(fecha2.date().currentDate())
        fecha2.setCalendarPopup(True)
        fecha2.setStyleSheet("background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 14px;")
        layfecha.addWidget(fecha1)
        layfecha.addWidget(fecha2)

        # EXAMEN PREVIO
        self.frameExIni = RecuadroPreguntaRadio(self.framePpal, [self.framePpal.width() - 500, 0, 500, 50], "",
                                                ["Examen inicial", "Reevaluación"], 40)

        # ODONTOLOGO
        self.frameOdont = QFrame(self.framePpal)
        self.frameOdont.setGeometry(0, 60, self.framePpal.width(), 50)
        self.frameOdont.setStyleSheet("background-color: #DBDBDB;")

        layodont = QHBoxLayout(self.frameOdont)
        layodont.setAlignment(Qt.AlignLeft)
        layodont.setSpacing(20)
        label = QLabel("Odontólogo: ")
        label.setStyleSheet("font-size: 18px; margin-left: 20px;")
        layodont.addWidget(label)
        inputOdont = QLineEdit()
        inputOdont.setPlaceholderText("Nombre Apellido1 Apellido2")
        inputOdont.setStyleSheet(
            "background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 17px; margin-right: 30px;")
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
        labelpaciente.setStyleSheet("font-size: 18px; margin-left: 20px;")
        laypaciente.addWidget(labelpaciente)
        inputPaciente = QLineEdit()
        inputPaciente.setPlaceholderText("Nombre Apellido1 Apellido2")
        inputPaciente.setStyleSheet(
            "background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 17px; margin-right: 30px;")
        laypaciente.addWidget(inputPaciente)

        self.frameNacimiento = QFrame(self.framePacienteTodo)
        self.frameNacimiento.setGeometry(self.framePacienteTodo.width() - 300, 0, 300, 50)
        self.frameNacimiento.setStyleSheet("background-color: #DBDBDB;")
        laynacimiento = QHBoxLayout(self.frameNacimiento)
        laynacimiento.setAlignment(Qt.AlignLeft)
        laynacimiento.setSpacing(20)
        labelnacimiento = QLabel("Nacimiento: ")
        labelnacimiento.setStyleSheet("font-size: 18px; margin-left: 20px;")
        laynacimiento.addWidget(labelnacimiento)
        inputNacimiento = QDateEdit()
        inputNacimiento.setGeometry(0, 0, 200, 40)
        inputNacimiento.setStyleSheet(
            "background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 14px; margin-right: 30px;")
        laynacimiento.addWidget(inputNacimiento)

        # PREGUNTAS RÁPIDAS
        labpreguntas = QLabel("Preguntas rápidas: ", self.framePpal)
        labpreguntas.setGeometry(20, 220, 400, 40)
        labpreguntas.setStyleSheet("font-size: 20px; font-weight: 300;")

        self.framePreguntas = QFrame(self.framePpal)
        self.framePreguntas.setGeometry(0, 260, self.framePpal.width(), 500)

        # TRATAMIENTO PREVIO
        self.tratprevio = TratPrevio(self.framePreguntas, self.framePreguntas.width() / 2 - 10)

        # COLAPSO DE MORDIDA
        self.colapso = RecuadroPreguntaRadio(self.framePreguntas, [self.framePreguntas.width() - 400, 0, 400, 50],
                                             "Colapso de mordida:", ["Sí", "No"], 30)

        self.abierto = False
        # DIENTES PERDIDOS
        self.dientesperdidos = RecuadroPreguntaRadio(self.framePreguntas, [0, 60, self.framePreguntas.width(), 50],
                                                     "Dientes perdidos por periodontitis:",
                                                     ["0", "1-4", ">=5", "Desconocido"], 30)

        # FUMADOR
        self.fumador = Fumador(self.framePreguntas, [0, 120, self.framePreguntas.width() / 2, 50], self.framePreguntas.width())

        self.botonSiguiente = QPushButton("Siguiente", self)
        self.botonSiguiente.setGeometry(self.width() - 205, self.height() - 125, 100, 40)
        self.botonSiguiente.setStyleSheet("QPushButton { background-color: #9747FF; border-radius: 7px; font-size: 18px; font-family: Alata;} QPushButton:hover { background-color: #7A2ECC; } QPushButton:pressed { background-color: #5F1E9A; }")
        self.botonSiguiente.clicked.connect(self.siguientePag)

    def siguientePag(self):
        print("Siguiente")

    def desplazarFrames(self, abierto):
        if abierto:
            self.abierto = True
            self.dientesperdidos.setGeometry(0, 90, self.framePreguntas.width(), 50)
            self.fumador.actualizarh(35)
        else:
            self.abierto = False
            self.dientesperdidos.setGeometry(0, 60, self.framePreguntas.width(), 50)
            self.fumador.actualizarh(-35)

    def actualizar_tam(self, event):
        self.titu.setGeometry(QRect((self.width() - self.titu.width()) // 2, 10, self.titu.width(), self.titu.height()))
        self.frameTitulo.setGeometry(0, 40, self.width(), 80)
        self.framePpal.setGeometry(220, 100, self.width() - 220 * 2, self.height() - 80)
        self.frameExIni.setGeometry(self.framePpal.width() - 500, 0, 500, 50)
        self.frameOdont.setGeometry(0, 60, self.framePpal.width(), 50)
        self.framePacienteTodo.setGeometry(0, 160, self.framePpal.width(), 50)
        self.frameNacimiento.setGeometry(self.framePacienteTodo.width() - 350, 0, 350, 50)
        self.framePreguntas.setGeometry(0, 260, self.framePpal.width(), 300)
        self.tratprevio.actw(self.framePreguntas.width() / 2 - 10)
        self.colapso.setGeometry(int(self.framePreguntas.width() / 2 + 10), 0,
                                 int(self.framePreguntas.width() / 2 - 10), 50)
        self.colapso.widthOpciones(int(self.framePreguntas.width() / 2 - 10))
        self.dientesperdidos.setGeometry(0, 60, self.framePreguntas.width(), 50)
        self.dientesperdidos.widthOpciones(self.framePreguntas.width())
        self.fumador.setGeometry(0, 120, self.framePreguntas.width() / 2, 50)
        self.fumador.actualizarw(self.framePreguntas.width() / 2, self.framePreguntas.width())
        self.botonSiguiente.setGeometry(self.width() - 205, self.height() - 125, 100, 40)


app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'diente.ico')))
window = None
window = MainWindow()
window.showMaximized()
window.show()
app.exec()

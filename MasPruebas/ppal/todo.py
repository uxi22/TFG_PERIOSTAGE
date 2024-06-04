import datetime
import sys
import os
from collections import defaultdict

import pandas as pd
from PIL import Image
from ctypes import windll

from PySide6.QtCore import (Qt, QRegularExpression, QRect, QSize, QPoint, QDate)
from PySide6.QtGui import (QRegularExpressionValidator, QImage, QPolygon, QBrush, QColor,
                           QPainter, QPen, QFontMetrics, QFont, QIcon)
from PySide6.QtWidgets import (QApplication, QLabel, QDateEdit, QRadioButton, QMainWindow,
                               QWidget, QHBoxLayout, QLineEdit, QPushButton, QPointList, QFrame,
                               QFileDialog, QCheckBox, QScrollArea)

try:
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

# Obtenemos la ruta al directorio del script
basedir = os.path.dirname(__file__)
basedir = os.path.join(basedir, os.pardir)

# Datos de la aplicación
separaciones = [8, 6, 9, 11, 10, 12, 10, 29, 9, 8, 13, 7, 4, 7, 5, 3]
dientes = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28,
           48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38]
furcas = [18, 17, 16, 26, 27, 28, 48, 47, 46, 36, 37, 38]
furcas_abajo = [18, 17, 16, 14, 24, 26, 27, 28, 48, 47, 46, 36, 37, 38]

# Datos de estilo
colorBoton = "background-color: #BEBEBE;"
colorClasificacion = "lightgreen"
style = "margin: 0.5px; border: 1px solid grey; border-radius: 3px;"


class Fumador(QFrame):
    def __init__(self, parent, coordenadas, wtotal):
        super().__init__(parent)
        self.setGeometry(coordenadas[0], coordenadas[1], coordenadas[2], coordenadas[3])

        self.wtotal = wtotal

        self.coordenadas = coordenadas

        self.framePreguntaPpal = RecuadroPreguntaRadio(self, [0, 0, coordenadas[2], 50], "Fumador:", ["Sí", "No", "Ex"],
                                                       20)
        self.botones = self.framePreguntaPpal.getOpciones()

        self.frameSubpreguntaSi = QFrame(self)
        self.frameSubpreguntaSi.setGeometry(0, 55, wtotal, 50)
        self.frameMesesFum = PreguntaInput(self.frameSubpreguntaSi, "Meses fumando:",
                                           [0, 0, int((wtotal - 10) / 3) - 20, 50], 60, 10, "0", 16)
        self.frameMesesFum.input.editingFinished.connect(lambda: datos.set_meses_fum(self.frameMesesFum.input.text()))
        if datos.meses_fumando != "0":
            self.frameMesesFum.input.setText(datos.meses_fumando)

        self.frameSesDia = PreguntaInput(self.frameSubpreguntaSi, "Cigarros o sesiones/día:",
                                         [int((wtotal - 10) / 3) - 15, 0, int((wtotal - 10) / 3) + 30, 50], 60, 10, "0",
                                         16)
        self.frameSesDia.input.editingFinished.connect(lambda: datos.set_cigarrillos(self.frameSesDia.input.text()))
        if datos.cigarrillos_dia != "0":
            self.frameSesDia.input.setText(datos.cigarrillos_dia)

        self.frameDuracionSesion = PreguntaInput(self.frameSubpreguntaSi, "Minutos/sesión:",
                                                 [int(2 * (wtotal - 10) / 3) - 5, 0, int((wtotal - 10) / 3) - 15, 50],
                                                 60,
                                                 10, "0", 16)
        self.frameDuracionSesion.input.editingFinished.connect(
            lambda: datos.set_duracion_ses(self.frameDuracionSesion.input.text()))
        if datos.duracion_ses != "0":
            self.frameDuracionSesion.input.setText(datos.duracion_ses)
        self.frameSubpreguntaSi.hide()

        self.frameSubpreguntaEx = QFrame(self)
        self.frameSubpreguntaEx.setGeometry(0, 55, wtotal, 50)
        self.frameMesesSinFum = PreguntaInput(self.frameSubpreguntaEx, "Meses sin fumar:", [0, 0, 300, 50], 60, 10, "0")
        self.frameMesesSinFum.input.editingFinished.connect(
            lambda: datos.set_meses_sin_f(self.frameMesesSinFum.input.text()))
        if datos.meses_sin_f != "0":
            self.frameMesesSinFum.input.setText(datos.meses_sin_f)
        self.frameSubpreguntaEx.hide()

        for boton in self.botones:
            boton.clicked.connect(self.subpregunta)
            if boton.text() == datos.tabaquismo:
                boton.setChecked(True)

    def subpregunta(self):
        if self.botones[0].isChecked():  # Sí
            datos.set_tabaquismo("Sí")
            self.setGeometry(self.coordenadas[0], self.coordenadas[1], self.wtotal, 105)
            datos.set_meses_sin_f("0")
            self.frameSubpreguntaEx.hide()
            self.frameSubpreguntaSi.show()
            self.frameMesesSinFum.input.setText("0")
        elif self.botones[-1].isChecked():  # Ex
            datos.set_tabaquismo("Ex")
            self.setGeometry(self.coordenadas[0], self.coordenadas[1], self.wtotal, 105)
            datos.set_meses_fum("0")
            datos.set_cigarrillos("0")
            datos.set_duracion_ses("0")
            self.frameSubpreguntaSi.hide()
            self.frameSubpreguntaEx.show()
            self.frameSesDia.input.setText("0")
            self.frameMesesFum.input.setText("0")
            self.frameDuracionSesion.input.setText("0")
        else:
            datos.set_tabaquismo("No")
            self.setGeometry(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], 50)
            self.frameSubpreguntaSi.hide()
            self.frameSubpreguntaEx.hide()

    def actualizarw(self, width, wtotal):
        self.coordenadas[2] = width
        self.wtotal = wtotal
        self.setGeometry(self.coordenadas[0], self.coordenadas[1], width, 50)
        self.framePreguntaPpal.setGeometry(0, 0, width, 50)
        self.framePreguntaPpal.widthOpciones(width)
        self.frameSubpreguntaSi.setGeometry(0, 55, wtotal, 50)
        self.frameMesesFum.actualizarGeometry([0, 0, int((wtotal - 10) / 3), 50])
        self.frameSesDia.actualizarGeometry([int((wtotal - 10) / 3) + 5, 0, int((wtotal - 10) / 3), 50])
        self.frameDuracionSesion.actualizarGeometry([int(2 * (wtotal - 10) / 3) + 10, 0, int((wtotal - 10) / 3), 50])

    def actualizarh(self, height):
        self.coordenadas[1] += height
        self.subpregunta()  # para establecer las dimensiones del desplegable como corresponda


class PreguntaInput(QFrame):
    def __init__(self, parent, pregunta, geometry, widthinput, spacing=20, placeholder="", fs=18):
        super().__init__(parent)
        self.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
        self.setStyleSheet("background-color: #DBDBDB; font-size:" + str(fs) + "px;")
        layinput = QHBoxLayout(self)
        layinput.setAlignment(Qt.AlignLeft)
        layinput.setSpacing(spacing)
        label = QLabel(pregunta)
        label.setStyleSheet("margin-left: 20px;")
        layinput.addWidget(label)
        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setStyleSheet(
            "background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 17px; margin-right: 16px;"
        )
        self.input.setGeometry(0, 0, widthinput, 40)
        layinput.addWidget(self.input)

    def actualizarGeometry(self, geometry):
        self.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])


class TratPrevio(QFrame):
    def __init__(self, parent, w):
        super().__init__(parent)
        self.setGeometry(0, 0, w, 50)

        self.w = w

        self.framePreguntaPpal = RecuadroPreguntaRadio(self, [0, 0, w, 50], "Tratamiento previo:", ["Sí", "No"], 20)
        self.botones = self.framePreguntaPpal.getOpciones()

        self.frameSubpregunta = RecuadroPreguntaRadio(self, [0, 55, w, 40], "", ["Básico", "Quirúrgico", "Ambas"], 10,
                                                      16)
        self.frameSubpregunta.hide()

        # Acciones de los botones
        for boton in self.botones:
            boton.clicked.connect(self.subpregunta)
            if boton.text() == datos.tratamiento_prev:
                boton.setChecked(True)

        self.botonessub = self.frameSubpregunta.getOpciones()
        for boton in self.botonessub:
            boton.clicked.connect(self.crear_conexion(boton))
            if boton.text() == datos.tipo_trat:
                boton.setChecked(True)

    def actw(self, w):
        self.w = w
        self.setGeometry(0, 0, w, 50)
        self.framePreguntaPpal.setGeometry(0, 0, w, 50)
        self.framePreguntaPpal.widthOpciones(w)
        self.frameSubpregunta.setGeometry(0, 55, w, 40)
        self.frameSubpregunta.widthOpciones(w, 40)

    def subpregunta(self):
        if window:
            window.desplazarFrames(self.botones[0].isChecked())
        if self.botones[0].isChecked():  # Sí
            datos.set_tratamiento_prev("Sí")
            self.setGeometry(0, 0, self.w, 95)
            self.frameSubpregunta.show()
        else:  # No
            datos.set_tratamiento_prev("No")
            self.setGeometry(0, 0, self.w, 50)
            self.frameSubpregunta.hide()

    def crear_conexion(self, boton):
        return lambda: datos.set_tipo_trat(boton.text())


class RecuadroPreguntaRadio(QFrame):
    def __init__(self, parent, coordenadas, pregunta, opciones, spacing=20, fs=18):
        super().__init__(parent)
        self.setGeometry(coordenadas[0], coordenadas[1], coordenadas[2], coordenadas[3])
        self.setStyleSheet(
            "background-color: #DBDBDB; font-size: " + str(fs) + "px; border-radius: 7px; justify-content: center")
        self.layouttotal = QHBoxLayout(self)
        self.layouttotal.setAlignment(Qt.AlignLeft)

        self.pregunta = QLabel(pregunta)
        self.pregunta.setStyleSheet("margin-left: 20px;")
        self.layouttotal.addWidget(self.pregunta)

        self.wp = QFontMetrics(QFont("Alata", fs)).horizontalAdvance(pregunta)
        if self.wp > 0:
            self.wp += 20

        self.frameOpciones = QFrame(self)
        self.frameOpciones.setGeometry(self.wp, 0, self.width() - self.wp, coordenadas[3])
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

    def widthOpciones(self, w, h=50):
        self.frameOpciones.setGeometry(self.wp, 0, w - self.wp, h)


class windowIni(QMainWindow):
    def __init__(self):
        super().__init__()

        self.fumador = None

        self.setWindowTitle("Periostage")
        self.setStyleSheet("background-color: #ECECEC;")
        self.setMinimumSize(QSize(300, 300))
        self.resizeEvent = self.actualizar_tam

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.frameTodo = QFrame()

        # TITULO
        self.frameTitulo = QFrame(self.frameTodo)
        self.frameTitulo.setStyleSheet("text-align: center;")

        self.titu = QLabel(self.frameTitulo)
        self.titu.setText("Periodontograma")
        self.titu.setStyleSheet("font-family: Alata; font-size: 26px; font-weight: 400; color: black;")
        self.titu.adjustSize()
        self.frameTitulo.show()
        self.siguiente = BotonSiguiente(self.frameTitulo, "Arcada superior")
        self.elementos()

        self.scroll_area.setStyleSheet("border: None;")
        self.scroll_area.setWidget(self.frameTodo)
        # self.scroll_area.setMinimumSize(QSize(self.frameTodo.width(), 200))
        self.scroll_area.setWidgetResizable(False)

    def elementos(self):
        self.framePpal = QFrame(self.frameTodo)
        self.framePpal.setGeometry(0, 80, 920, self.height() - 80)
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
        fecha1 = QLabel("Fecha:")
        fecha1.setStyleSheet("margin-left: 20px; font-size: 18px;")
        fecha2 = QDateEdit()
        fecha2.setGeometry(0, 0, 200, 40)
        fecha2.setDate(datos.fecha)
        fecha2.setCalendarPopup(True)
        fecha2.setStyleSheet("background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 14px;")
        fecha2.dateChanged.connect(lambda: datos.set_fecha(fecha2.date()))
        layfecha.addWidget(fecha1)
        layfecha.addWidget(fecha2)

        # EXAMEN PREVIO
        self.frameExIni = RecuadroPreguntaRadio(self.framePpal, [self.framePpal.width() - 500, 0, 500, 50], "",
                                                ["Examen inicial", "Reevaluación"], 40)
        exini = self.frameExIni.getOpciones()
        for boton in exini:
            if boton.text() == datos.examen_inicial:
                boton.setChecked(True)
        exini[0].clicked.connect(lambda: datos.set_examen_inicial("Examen inicial"))
        exini[1].clicked.connect(lambda: datos.set_examen_inicial("Reevaluación"))

        # ODONTOLOGA
        self.frameOdont = QFrame(self.framePpal)
        self.frameOdont.setGeometry(0, 60, self.framePpal.width(), 50)
        self.frameOdont.setStyleSheet("background-color: #DBDBDB;")

        layodont = QHBoxLayout(self.frameOdont)
        layodont.setAlignment(Qt.AlignLeft)
        layodont.setSpacing(20)
        label = QLabel("Odontóloga/o: ")
        label.setStyleSheet("font-size: 18px; margin-left: 20px;")
        layodont.addWidget(label)
        inputOdont = QLineEdit()
        if datos.odontologa != "":
            inputOdont.setText(datos.odontologa)
        inputOdont.setPlaceholderText("Nombre Apellido1 Apellido2")
        inputOdont.setStyleSheet(
            "background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 17px; margin-right: 30px;")
        inputOdont.setGeometry(0, 0, 220, 40)
        inputOdont.editingFinished.connect(lambda: datos.set_odontologa(inputOdont.text()))

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
        labelpaciente = QLabel("Nombre:")
        labelpaciente.setStyleSheet("font-size: 18px; margin-left: 20px;")
        laypaciente.addWidget(labelpaciente)
        inputPaciente = QLineEdit()
        if datos.paciente != "":
            inputPaciente.setText(datos.paciente)
        inputPaciente.setPlaceholderText("Nombre Apellido1 Apellido2")
        inputPaciente.setStyleSheet(
            "background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 17px; margin-right: 30px;")
        inputPaciente.editingFinished.connect(lambda: datos.set_paciente(inputPaciente.text()))

        laypaciente.addWidget(inputPaciente)

        self.frameNacimiento = QFrame(self.framePacienteTodo)
        self.frameNacimiento.setGeometry(self.framePacienteTodo.width() - 300, 0, 300, 50)
        self.frameNacimiento.setStyleSheet("background-color: #DBDBDB;")
        laynacimiento = QHBoxLayout(self.frameNacimiento)
        laynacimiento.setAlignment(Qt.AlignLeft)
        laynacimiento.setSpacing(20)
        labelnacimiento = QLabel("Nacimiento:")
        labelnacimiento.setStyleSheet("font-size: 18px; margin-left: 20px;")
        laynacimiento.addWidget(labelnacimiento)
        inputNacimiento = QDateEdit()
        inputNacimiento.setGeometry(0, 0, 200, 40)
        inputNacimiento.setDate(datos.nacimiento)
        inputNacimiento.setCalendarPopup(True)
        inputNacimiento.setStyleSheet(
            "background-color: #BDBDBD; padding: 8px; border-radius: 7px; font-size: 14px;")
        inputNacimiento.dateChanged.connect(lambda: datos.set_nacimiento(inputNacimiento.date()))
        laynacimiento.addWidget(inputNacimiento)

        # PREGUNTAS RÁPIDAS
        labpreguntas = QLabel("Preguntas rápidas:", self.framePpal)
        labpreguntas.setGeometry(20, 220, 400, 40)
        labpreguntas.setStyleSheet("font-size: 20px; font-weight: 300;")

        self.framePreguntas = QFrame(self.framePpal)
        self.framePreguntas.setGeometry(0, 260, self.framePpal.width(), 500)

        # TRATAMIENTO PREVIO
        self.tratprevio = TratPrevio(self.framePreguntas, self.framePreguntas.width() / 2 - 10)

        # COLAPSO DE MORDIDA
        self.colapso = RecuadroPreguntaRadio(self.framePreguntas, [self.framePreguntas.width() - 400, 0, 400, 50],
                                             "Colapso de mordida:", ["Sí", "No"], 30)
        colaps = self.colapso.getOpciones()
        for boton in colaps:
            if boton.text() == datos.colapso_mordida:
                boton.setChecked(True)
        colaps[0].clicked.connect(lambda: datos.set_colapso("Sí"))
        colaps[1].clicked.connect(lambda: datos.set_colapso("No"))

        self.abierto = False
        # DIENTES PERDIDOS
        opc_dientes = ["0", "1-4", ">=5", "Desconocido"]
        self.dientesperdidos = RecuadroPreguntaRadio(self.framePreguntas, [0, 60, self.framePreguntas.width(), 50],
                                                     "Dientes perdidos por periodontitis:",
                                                     opc_dientes, 30)
        dientsperdidos = self.dientesperdidos.getOpciones()
        for boton in dientsperdidos:
            boton.clicked.connect(self.crear_conexion(boton))
            if boton.text() == datos.dientes_perdidos:
                boton.setChecked(True)

        # FUMADOR
        self.fumador = Fumador(self.framePreguntas, [0, 120, self.framePreguntas.width() / 2 - 10, 50],
                               self.framePreguntas.width())

    def crear_conexion(self, boton):
        return lambda: datos.set_dientes_perdidos(boton.text())

    def desplazarFrames(self, abierto):
        if abierto:
            self.abierto = True
            self.dientesperdidos.setGeometry(0, 110, self.framePreguntas.width(), 50)
            self.fumador.actualizarh(60)
        else:
            self.abierto = False
            self.dientesperdidos.setGeometry(0, 60, self.framePreguntas.width(), 50)
            self.fumador.actualizarh(-60)

    def actualizar_tam(self, event):
        self.frameTodo.setGeometry(0, 0, max(self.width(), 950), 675)
        self.titu.setGeometry(
            QRect((max(self.width(), 950) - self.titu.width()) // 2, 10, self.titu.width(), self.titu.height()))
        self.frameTitulo.setGeometry(0, 40, max(self.width(), 950), 80)
        if self.width() >= 960:
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.framePpal.setGeometry((self.width() - 920) / 2, 100, 920, 625)
            self.siguiente.setGeometry(
                QRect(self.framePpal.width() + int((self.width() - 920) / 2) - 125, 15, 125, 30))
        else:
            self.framePpal.setGeometry(15, 100, 920, 625)
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.siguiente.setGeometry(QRect(self.framePpal.width() + 15 - 125, 15, 125, 30))
        self.scroll_area.setGeometry(0, 0, self.width(), self.height())


def cambiar_color(boton, color):
    if boton.isChecked():
        boton.setStyleSheet(style + f"background-color: {color}")
    else:
        boton.setStyleSheet(style + colorBoton)


def es_numero(texto):
    if len(texto) == 0:
        return False
    if texto[0] in ('-', '+'):
        return texto[1:].isdigit()
    return texto.isdigit()


def calcular_cal(i, t):
    if i not in datos.desactivadosInferior + datos.desactivadosSuperior:
        mg = datos.margenes[i][t]
        ppd = datos.profundidades[i][t]
        if mg >= 0:
            mg = 0
            if ppd < 4:
                return 0
            elif ppd >= 4:
                return ppd + mg - 2
        else:
            mg = abs(mg)
            return ppd + mg
    else:
        return -1


def aplanar_lista(lista):
    salida = []
    for i in lista:
        if isinstance(i, list):
            salida.extend(i)
        else:
            salida.append(i)
    return salida


class ImagenDiente(QImage):
    def __init__(self, abajo=""):
        super().__init__()

        width = 0
        # Añadir imagen de los dientes
        self.dientes = []
        for i in range(0, 16):
            if datos.implantes[i + 16 * pantallaAct]:
                im = Image.open(
                    os.path.join(basedir, "DIENTES", f"periodontograma-i{dientes[i + 16 * pantallaAct]}{abajo}.png"))
                im = im.resize((int(im.width * 0.88), int(im.height * 0.88)))
                self.dientes.append(im)
                self.dientes[-1] = self.dientes[-1].convert("RGBA")
            else:
                im = Image.open(
                    os.path.join(basedir, "DIENTES", f"periodontograma-{dientes[i + 16 * pantallaAct]}{abajo}.png"))
                im = im.resize((int(im.width * 0.88), int(im.height * 0.88)))
                self.dientes.append(im)
                self.dientes[-1] = self.dientes[-1].convert("RGBA")

            width += self.dientes[-1].width + separaciones[i]

        imagen = Image.new('RGBA', (width, 137), (0, 0, 0, 0))

        position = 0
        for i in range(len(self.dientes)):
            imagen.paste(self.dientes[i], (position, 0))
            position += self.dientes[i].width + separaciones[i]
        self.swap(imagen.toqimage())


class LineasSobreDientesAbajo(QWidget):
    def __init__(self, parent):
        self.pantalla = pantallaAct
        super().__init__(parent)
        self.imagen = ImagenDiente("b")
        self.setGeometry(QRect(0, 0, self.width(), self.height()))
        # Inicializamos las listas de los puntos de las líneas
        self.points = QPointList()
        self.points2 = QPointList()

        self.puntos_furca = QPointList()

        # Puntos medios de la línea superior de los puntos de furca
        # 2 puntos por diente
        triangulos_abajo = [[70, 8], [74, 30], [72, 10], [75, 32], [71, 9], [73, 33], [71, 7], [69, 25],
                            [67, 6], [70, 23], [69, 10], [72, 34], [77, 12], [78, 26], [75, 10], [73, 31]]

        # Puntos de inicio y fin de la imagen del diente en la parte superior (no en el límite con la encía)
        # 2 valores por diente
        # En píxeles sobre el eje x
        puntos_arriba = [[1, 5], [5, 6], [4, 8], [9, 8], [9, 8], [7, 7], [6, 8], [10, 6], [7, 11], [6, 6], [7, 8],
                         [8, 9], [8, 10], [7, 5], [5, 5], [2, 1]]

        dist = 0
        self.altura = 57
        # Valores iniciales de los puntos de los dientes
        for i, diente_imagen in enumerate(self.imagen.dientes):
            if dientes[i + 16 * pantallaAct] in furcas_abajo:
                # Hay 2 puntos de furca en la cara que aparece abajo
                self.puntos_furca.append(QPoint(dist + triangulos_abajo[furcas_abajo.index(dientes[i]) * 2][1],
                                                triangulos_abajo[furcas_abajo.index(dientes[i]) * 2][0]))
                self.puntos_furca.append(QPoint(dist + triangulos_abajo[furcas_abajo.index(dientes[i]) * 2 + 1][1],
                                                triangulos_abajo[furcas_abajo.index(dientes[i]) * 2 + 1][0]))
            dist += puntos_arriba[i][0]
            self.points.append(QPoint(dist, int(self.altura)))
            self.points2.append(QPoint(dist, int(self.altura)))
            wdiente = diente_imagen.width - puntos_arriba[i][0] - puntos_arriba[i][1]
            self.points.append(QPoint(dist + wdiente // 2, int(self.altura)))
            self.points2.append(QPoint(dist + wdiente // 2, int(self.altura)))
            dist += wdiente
            self.points.append(QPoint(dist, int(self.altura)))
            self.points2.append(QPoint(dist, int(self.altura)))
            dist += puntos_arriba[i][1] + separaciones[i]

    def paintEvent(self, event):
        qp = QPainter(self)

        # Imagen de los dientes
        imagen = QImage(self.imagen)

        tam = QRect(0, 0, imagen.width(), imagen.height())
        self.setMinimumSize(imagen.width(), imagen.height())
        qp.drawImage(tam, imagen)

        pen = qp.pen()
        pen.setWidth(1.5)
        qp.setPen(pen)
        altura_ini = 52

        # Líneas negra horizontales
        for i in range(1, 18):
            altura_ini += 5
            qp.drawLine(0, altura_ini, tam.width(), altura_ini)

        qp.setRenderHint(QPainter.Antialiasing, True)

        poligono = QPolygon()
        # Pincel semitransparente
        brush = QBrush(QColor(50, 0, 100, 100))
        qp.setBrush(brush)

        auxpuntos = []

        # Dibujamos líneas y polígonos sobre los dientes
        for i in range(16):
            if (i + 16 * self.pantalla) not in datos.desactivadosInferior and (
                    i + 16 * self.pantalla) not in datos.desactivadosSuperior:
                qp.setBrush(brush)
                qp.setPen(QPen(Qt.blue, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
                auxpuntos.append(self.points2[i * 3])
                auxpuntos.append(self.points2[i * 3 + 1])
                auxpuntos.append(self.points2[i * 3 + 2])
                qp.drawPolyline(auxpuntos)  # línea azul
                poligono.append(auxpuntos)
                qp.setPen(QPen(Qt.red, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
                auxpuntos.clear()
                auxpuntos.append(self.points[i * 3])
                auxpuntos.append(self.points[i * 3 + 1])
                auxpuntos.append(self.points[i * 3 + 2])
                qp.drawPolyline(auxpuntos)  # línea roja
                poligono.append(list(reversed(auxpuntos)))
                qp.setPen(QPen(Qt.NoPen))
                qp.drawPolygon(poligono)
                if ((i + 16 * self.pantalla) + 1 not in datos.desactivadosInferior and (
                        i + 16 * self.pantalla) + 1 not in datos.desactivadosSuperior) and i != 7 and i != 15:
                    poligono.clear()
                    auxpuntos.clear()
                    qp.setPen(QPen(Qt.blue, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
                    auxpuntos.append(self.points2[i * 3 + 2])
                    auxpuntos.append(self.points2[i * 3 + 3])
                    qp.drawPolyline(auxpuntos)  # línea azul
                    poligono.append(auxpuntos)
                    qp.setPen(QPen(Qt.red, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
                    auxpuntos.clear()
                    auxpuntos.append(self.points[i * 3 + 2])
                    auxpuntos.append(self.points[i * 3 + 3])
                    qp.drawPolyline(auxpuntos)  # línea roja
                    poligono.append(list(reversed(auxpuntos)))
                    qp.setPen(QPen(Qt.NoPen))
                    qp.drawPolygon(poligono)
                qp.setBrush(Qt.NoBrush)
                poligono.clear()
                auxpuntos.clear()

                # defectos de furca
                for w in range(1, 3):
                    if not datos.implantes[i + 16 * self.pantalla] and dientes[
                        i + 16 * self.pantalla] in furcas_abajo and \
                            datos.defectosfurca[dientes[i + 16 * self.pantalla]][w] > 0:
                        auxindice = furcas_abajo.index(dientes[i])
                        valor = datos.defectosfurca[dientes[i + 16 * self.pantalla]][w]
                        qp.setPen(QPen(QColor(165, 10, 135, 210), 1.5, Qt.SolidLine, Qt.SquareCap))
                        auxpuntos = [self.puntos_furca[auxindice * 2 + w - 1].x(),
                                     self.puntos_furca[auxindice * 2 + w - 1].y()]
                        (poligono << QPoint(auxpuntos[0] - 8, auxpuntos[1]) <<
                         QPoint(auxpuntos[0], auxpuntos[1] + 11) << QPoint(auxpuntos[0] + 8, auxpuntos[1]))
                        if valor == 1:
                            qp.drawPolyline(poligono)  # triángulo sin cerrar y sin rellenar
                        else:
                            if valor == 3:
                                qp.setBrush(QBrush(QColor(165, 10, 135, 120), Qt.SolidPattern))
                            qp.drawPolygon(poligono)
                        poligono.clear()
                        auxpuntos.clear()
            else:
                # Dibujar línea para tachar diente
                punto_ini = QPoint(self.points[i * 3 + 2].x(), 0)
                punto_fin = QPoint(self.points[i * 3].x(), self.height())
                qp.setPen(QPen(Qt.black, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
                qp.drawLine(punto_ini, punto_fin)

    def minimumSizeHint(self):
        return QSize(1, 1)

    def actualizar_imagen(self):
        self.imagen = ImagenDiente("b")
        self.update()

    def actualizar_todas_alturas(self):
        for i in range(16):
            for j in range(3):
                self.actualizar_alturas(i, 1, j)
                self.actualizar_alturas(i, 2, j)
        self.update()

    def actualizar_alturas(self, numeroDiente, tipo, indice):
        if tipo == 1:  # Margen gingival
            aux = self.points[numeroDiente * 3 + indice]
            aux.setY(int(self.altura - 5 * datos.margenes[numeroDiente + 16 * pantallaAct][indice + 3]))
            self.points[numeroDiente * 3 + indice] = aux
            aux.setY(
                int(self.points[numeroDiente * 3 + indice].y() + 5 *
                    datos.profundidades[numeroDiente + 16 * pantallaAct][indice + 3]))
            self.points2[numeroDiente * 3 + indice] = aux
        elif tipo == 2:  # Profundidad de sondaje
            aux = self.points[numeroDiente * 3 + indice]
            aux.setY(int(self.altura + 5 * (abs(datos.margenes[numeroDiente + 16 * pantallaAct][indice + 3]) + abs(
                datos.profundidades[numeroDiente + 16 * pantallaAct][indice + 3]))))
            self.points2[numeroDiente * 3 + indice] = aux
        self.update()

    def def_furca(self):
        self.update()


class LineasSobreDientes(QWidget):
    def __init__(self, parent):
        self.pantalla = pantallaAct
        super().__init__(parent)
        self.imagen = ImagenDiente("")
        self.setGeometry(QRect(0, 0, self.width(), self.height()))

        # Inicializamos las listas de los puntos de las líneas
        self.points = QPointList()
        self.points2 = QPointList()
        self.puntos_furca = QPointList()

        triangulos_arriba = [[55, 23], [58, 21], [61, 19], [60, 25], [58, 24], [54, 23]]
        puntos_arriba = [[1, 5], [5, 6], [4, 8], [9, 8], [9, 8], [7, 7], [6, 8], [10, 6], [7, 11], [6, 6], [7, 8],
                         [8, 9], [8, 10], [7, 5], [5, 5], [2, 1]]
        dist = 0
        self.altura = 80
        # Valores iniciales de los puntos de los dientes
        for i, diente_imagen in enumerate(self.imagen.dientes):
            if dientes[i + 16 * pantallaAct] in furcas:
                self.puntos_furca.append(QPoint(dist + triangulos_arriba[furcas.index(dientes[i])][1],
                                                triangulos_arriba[furcas.index(dientes[i])][0]))
            dist += puntos_arriba[i][0]
            self.points.append(QPoint(dist, int(self.altura)))  # inicio diente
            self.points2.append(QPoint(dist, int(self.altura)))
            wdiente = diente_imagen.width - puntos_arriba[i][0] - puntos_arriba[i][1]
            self.points.append(QPoint(dist + wdiente // 2, int(self.altura)))
            self.points2.append(QPoint(dist + wdiente // 2, int(self.altura)))
            dist += wdiente
            self.points.append(QPoint(dist, int(self.altura)))  # fin diente, ppio siguiente
            self.points2.append(QPoint(dist, int(self.altura)))
            dist += puntos_arriba[i][1] + separaciones[i]

    def paintEvent(self, event):
        qp = QPainter(self)

        # Imagen de los dientes
        imagen = QImage(self.imagen)

        tam = QRect(0, 0, imagen.width(), imagen.height())
        self.setMinimumSize(imagen.width(), imagen.height())
        qp.drawImage(tam, imagen)

        pen = qp.pen()
        pen.setWidth(1.5)
        qp.setPen(pen)
        altura_ini = -5

        # Dibujamos las líneas negras horizontales
        for i in range(1, 18):
            altura_ini += 5
            qp.drawLine(0, altura_ini, tam.width(), altura_ini)

        qp.setRenderHint(QPainter.Antialiasing, True)

        poligono = QPolygon()
        brush = QBrush(QColor(50, 0, 100, 100))
        qp.setBrush(brush)

        auxpuntos = []

        for i in range(16):
            if (i + 16 * self.pantalla) not in datos.desactivadosInferior and (
                    i + 16 * self.pantalla) not in datos.desactivadosSuperior:
                qp.setBrush(brush)
                qp.setPen(QPen(Qt.blue, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
                auxpuntos.append(self.points2[i * 3])
                auxpuntos.append(self.points2[i * 3 + 1])
                auxpuntos.append(self.points2[i * 3 + 2])
                qp.drawPolyline(auxpuntos)  # línea azul
                poligono.append(auxpuntos)
                qp.setPen(QPen(Qt.red, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
                auxpuntos.clear()
                auxpuntos.append(self.points[i * 3])
                auxpuntos.append(self.points[i * 3 + 1])
                auxpuntos.append(self.points[i * 3 + 2])
                qp.drawPolyline(auxpuntos)  # línea roja
                poligono.append(list(reversed(auxpuntos)))
                qp.setPen(QPen(Qt.NoPen))
                qp.drawPolygon(poligono)
                if (i + 16 * self.pantalla + 1 not in datos.desactivadosSuperior and (
                        i + 16 * self.pantalla) + 1 not in datos.desactivadosInferior) and i != 7 and i != 15:
                    poligono.clear()
                    auxpuntos.clear()
                    qp.setPen(QPen(Qt.blue, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
                    auxpuntos.append(self.points2[i * 3 + 2])
                    auxpuntos.append(self.points2[i * 3 + 3])
                    qp.drawPolyline(auxpuntos)  # línea azul
                    poligono.append(auxpuntos)
                    qp.setPen(QPen(Qt.red, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
                    auxpuntos.clear()
                    auxpuntos.append(self.points[i * 3 + 2])
                    auxpuntos.append(self.points[i * 3 + 3])
                    qp.drawPolyline(auxpuntos)  # línea roja
                    poligono.append(list(reversed(auxpuntos)))
                    qp.setPen(QPen(Qt.NoPen))
                    qp.drawPolygon(poligono)
                qp.setBrush(Qt.NoBrush)
                poligono.clear()
                auxpuntos.clear()

                # defectos de furca
                if not datos.implantes[i + 16 * self.pantalla] and dientes[i + 16 * self.pantalla] in furcas and \
                        datos.defectosfurca[dientes[i + 16 * self.pantalla]][0] > 0:
                    auxindice = furcas.index(dientes[i])
                    valor = datos.defectosfurca[dientes[i + 16 * self.pantalla]][0]
                    qp.setPen(QPen(QColor(165, 10, 135, 210), 1.5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
                    auxpuntos = [self.puntos_furca[auxindice].x(),
                                 self.puntos_furca[auxindice].y()]
                    (poligono << QPoint(auxpuntos[0] - 8, auxpuntos[1]) <<
                     QPoint(auxpuntos[0], auxpuntos[1] + 11) << QPoint(auxpuntos[0] + 8, auxpuntos[1]))
                    if valor == 1:
                        qp.drawPolyline(poligono)  # triángulo sin cerrar y sin rellenar
                    else:
                        if valor == 3:
                            qp.setBrush(QBrush(QColor(165, 10, 135, 120), Qt.SolidPattern))
                        qp.drawPolygon(poligono)
                    poligono.clear()
                    auxpuntos.clear()
            else:
                # dibujar una línea para tachar el diente
                punto_ini = QPoint(self.points[i * 3 + 2].x(), 0)
                punto_fin = QPoint(self.points[i * 3].x(), self.height())
                qp.setPen(QPen(Qt.black, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
                qp.drawLine(punto_ini, punto_fin)

    def minimumSizeHint(self):
        return QSize(1, 1)

    def actualizar_imagen(self):
        self.imagen = ImagenDiente()
        self.update()

    def actualizar_todas_alturas(self):
        for i in range(16):
            for j in range(3):
                self.actualizar_alturas(i, 1, j)
                self.actualizar_alturas(i, 2, j)
        self.update()

    def actualizar_alturas(self, numeroDiente, tipo, indice):
        if tipo == 1:  # Margen gingival
            aux = self.points[numeroDiente * 3 + indice]
            aux.setY(int(self.altura + 5 * datos.margenes[numeroDiente + 16 * pantallaAct][indice]))
            self.points[numeroDiente * 3 + indice] = aux
            aux.setY(int(
                self.points[numeroDiente * 3 + indice].y() - 5 * datos.profundidades[numeroDiente + 16 * pantallaAct][
                    indice]))
            self.points2[numeroDiente * 3 + indice] = aux
        elif tipo == 2:  # Profundidad de sondaje
            aux = self.points[numeroDiente * 3 + indice]
            aux.setY(int(self.altura + 5 * (
                    datos.margenes[numeroDiente + 16 * pantallaAct][indice] -
                    datos.profundidades[numeroDiente + 16 * pantallaAct][indice])))
            self.points2[numeroDiente * 3 + indice] = aux
        self.update()

    def def_furca(self):
        self.update()


class Input03(QLineEdit):
    def __init__(self, height, furca=False, numDiente=0, parent=None, w=45, left=0, ind=0):
        super().__init__(parent)

        regex = QRegularExpression("[0-3]")
        self.setValidator(QRegularExpressionValidator(regex))
        self.setAlignment(Qt.AlignCenter)
        self.setPlaceholderText("0")
        self.editingFinished.connect(lambda: self.guardar_texto(numDiente, furca, ind))
        self.setStyleSheet("QLineEdit { " + style + "font-size: 10px;} QLineEdit:focus { border: 1px solid #C3C3C3; }")
        self.setGeometry(QRect(left, height, w, 18))

    def guardar_texto(self, numDiente, furca, ind):
        if furca:
            # actualizar datos
            datos.actualizar_defecto_furca(numDiente + 16 * pantallaAct, self.text(), ind)
            # Actualizar dibujo dientes
            window.widgetDientes.update()
            window.widgetDientesAbajo.update()
        else:
            # actualizar datos
            datos.actualizar_movilidad(numDiente + 16 * pantallaAct, self.text())


class Input2Furcas(QFrame):
    def __init__(self, parent, height, numDiente):
        super().__init__(parent)
        self.setGeometry(QRect(0, height, 45, 18))
        self.inputs = []
        self.inputs.append(Input03(0, True, numDiente, self, 22, 0, 1))
        self.inputs.append(Input03(0, True, numDiente, self, 22, 23, 2))


class InputSiNo3(QFrame):
    def __init__(self, numDiente, tipo, parent, height, abajo=False):
        super().__init__(parent)
        self.setGeometry(QRect(0, height, 45, 18))
        self.botones = []
        left = 0
        for n in range(1, 4):
            boton = QPushButton("", self)
            boton.setCheckable(True)
            boton.setStyleSheet("QPushButton { " + style + colorBoton + "}" +
                                "QPushButton:hover { background-color: #AAAAAA; }")
            boton.setDefault(True)
            boton.setGeometry(QRect(left, 0, 15, 18))
            left += 15
            boton.clicked.connect(lambda *args, ind=n - 1, t=tipo: self.pulsar_boton(ind, numDiente, t, abajo))
            self.botones.append(boton)

    def pulsar_boton(self, ind, numDiente, tipo, abajo):
        boton = self.botones[ind]
        if abajo:
            ind = ind + 3

        if tipo == 1:
            cambiar_color(boton, "#FF2B32")
            window.sangrado.actualizarDatos(numDiente * 6 + ind, boton.isChecked())
            datos.actualizar_sangrado(int(numDiente + 16 * pantallaAct), ind, boton.isChecked())
        elif tipo == 2:
            cambiar_color(boton, "#5860FF")
            window.placa.actualizarDatos(int(numDiente) * 6 + ind, boton.isChecked())
            datos.actualizar_placa(int(numDiente + 16 * pantallaAct), ind, boton.isChecked())
        elif tipo == 3:
            cambiar_color(boton, "#7CEBA0")
            # window.supuracion.actualizarDatos(int(numDiente) * 6 + ind, boton.isChecked())
            datos.actualizar_supuracion(int(numDiente + 16 * pantallaAct), ind, boton.isChecked())


class Input3(QFrame):
    def __init__(self, ndiente, tipo, height, parent, arriba=True):
        super().__init__(parent)
        self.setGeometry(QRect(0, height, 45, 18))
        self.validator = QRegularExpressionValidator(QRegularExpression(r"^[+-]?\d{1,2}$"))

        self.inpts = []
        left = 0
        for i in range(1, 4):
            inpt = QLineEdit()
            inpt.setParent(self)
            inpt.setValidator(self.validator)
            inpt.setStyleSheet(
                "QLineEdit { " + style + "font-size: 10px; } QLineEdit:focus { border: 1px solid #C3C3C3; }")
            inpt.setPlaceholderText("0")
            inpt.setGeometry(QRect(left, 0, 15, 18))
            left += 15
            inpt.editingFinished.connect(lambda ind=i - 1: self.guardar_texto(ndiente, tipo, ind, arriba))
            self.inpts.append(inpt)

    def guardar_texto(self, ndiente, tipo, num, arriba):
        inpt = self.inpts[num]
        if tipo == 1 and es_numero(inpt.text()):  # Margen gingival
            if -21 < int(inpt.text()) < 21:
                if arriba:
                    datos.actualizar_margen(int(ndiente + 16 * pantallaAct), num, int(inpt.text()))
                    window.widgetDientes.actualizar_alturas(int(ndiente), tipo, num)
                    window.cal.actualizarDatos(int(ndiente) * 6 + num,
                                               calcular_cal(int(ndiente + 16 * pantallaAct), num))
                else:
                    datos.actualizar_margen(int(ndiente + 16 * pantallaAct), num + 3, int(inpt.text()))
                    window.widgetDientesAbajo.actualizar_alturas(int(ndiente), tipo, num)
                    window.cal.actualizarDatos(int(ndiente) * 6 + num + 3,
                                               calcular_cal(int(ndiente + 16 * pantallaAct), num + 3))
            else:
                inpt.setText("0")
        elif tipo == 2 and es_numero(inpt.text()):  # Profundidad de sondaje
            if 0 < int(inpt.text()) < 21:
                if int(inpt.text()) >= 4:
                    self.inpts[num].setStyleSheet("QLineEdit { " + style + "color: crimson; font-size: 12px; }")
                else:
                    self.inpts[num].setStyleSheet("QLineEdit { " + style + "color: black; font-size: 12px; }")
                if arriba:
                    datos.actualizar_profundidad(int(ndiente + 16 * pantallaAct), num, int(inpt.text()))
                    window.widgetDientes.actualizar_alturas(int(ndiente), tipo, num)
                    window.ppd.actualizarDatos(int(ndiente) * 6 + num, int(inpt.text()))
                    window.cal.actualizarDatos(int(ndiente) * 6 + num,
                                               calcular_cal(int(ndiente + 16 * pantallaAct), num))
                else:
                    datos.actualizar_profundidad(int(ndiente + 16 * pantallaAct), num + 3, int(inpt.text()))
                    window.widgetDientesAbajo.actualizar_alturas(int(ndiente), tipo, num)
                    window.ppd.actualizarDatos(int(ndiente) * 6 + num + 3, int(inpt.text()))
                    window.cal.actualizarDatos(int(ndiente) * 6 + num + 3,
                                               calcular_cal(int(ndiente + 16 * pantallaAct), num + 3))
            else:
                inpt.setText("0")


class Columna(QFrame):
    def __init__(self, numDiente, left, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(left, 0, 45, parent.height()))

        self.incrementoHeight = 0

        botonNumeroDiente = QPushButton(str(dientes[numDiente + 16 * pantallaAct]), self)
        botonNumeroDiente.setCheckable(True)
        botonNumeroDiente.setDefault(True)
        botonNumeroDiente.setStyleSheet(style + colorBoton + "font-weight: bold; font-size: 12px;")
        botonNumeroDiente.clicked.connect(lambda: self.desactivar_activar_diente(numDiente))
        botonNumeroDiente.setGeometry(QRect(0, self.incrementoHeight, 45, 18))
        self.incrementoHeight += 18

        self.hijos = [botonNumeroDiente]

        if (numDiente + 16 * pantallaAct) not in datos.desactivadosInferior and (
                numDiente + 16 * pantallaAct) not in datos.desactivadosSuperior:
            self.anhadir_elementos(numDiente)
        else:
            self.eliminar_elementos()

    def newsize(self, height):
        self.setGeometry(self.geometry().left(), 0, 45, height)

    def anhadir_elementos(self, numDiente):
        self.incrementoHeight = 18

        # MOVILIDAD
        movilidad = Input03(self.incrementoHeight, False, numDiente, self)
        movilidad.show()
        self.incrementoHeight += 18
        self.hijos.append(movilidad)

        # DEFECTO DE FURCA
        if dientes[numDiente] in furcas and not datos.implantes[numDiente + 16 * pantallaAct]:
            furca = Input03(self.incrementoHeight, True, numDiente, self, ind=0)
        else:
            furca = QLabel("", self)
            furca.setGeometry(QRect(0, self.incrementoHeight, 45, 18))
        furca.show()
        self.incrementoHeight += 18
        self.hijos.append(furca)

        # IMPLANTE
        implante = QPushButton("", self)
        implante.setCheckable(True)
        implante.setStyleSheet(
            "QPushButton { " + style + colorBoton + "} QPushButton:hover { background-color: #AAAAAA; }")
        implante.setDefault(True)
        implante.clicked.connect(lambda: self.diente_implante(numDiente))
        implante.setGeometry(QRect(0, self.incrementoHeight, 45, 18))
        implante.show()
        self.incrementoHeight += 18
        self.hijos.append(implante)

        # SANGRADO AL SONDAJE
        sangrado = InputSiNo3(numDiente, 1, self, self.incrementoHeight)
        sangrado.show()
        self.incrementoHeight += 18
        self.hijos.append(sangrado)

        # PLACA
        placa = InputSiNo3(numDiente, 2, self, self.incrementoHeight)
        placa.show()
        self.incrementoHeight += 18
        self.hijos.append(placa)

        # SUPURACIÓN
        supuracion = InputSiNo3(numDiente, 3, self, self.incrementoHeight)
        supuracion.show()
        self.incrementoHeight += 18
        self.hijos.append(supuracion)

        # MARGEN GINGIVAL
        margenGingival = Input3(numDiente, 1, self.incrementoHeight, self, arriba=True)
        margenGingival.show()
        self.incrementoHeight += 18
        self.hijos.append(margenGingival)

        # PROFUNDIDAD DE SONDAJE
        profSondaje = Input3(numDiente, 2, self.incrementoHeight, self, arriba=True)
        profSondaje.show()
        self.incrementoHeight += 18
        self.hijos.append(profSondaje)

        self.incrementoHeight += 137 + 85 + 137

        # COLUMNAS INFERIORES
        # SANGRADO
        sangrado2 = InputSiNo3(numDiente, 1, self, self.incrementoHeight, abajo=True)
        sangrado2.show()
        self.incrementoHeight += 18
        self.hijos.append(sangrado2)

        # PLACA
        placa2 = InputSiNo3(numDiente, 2, self, self.incrementoHeight, abajo=True)
        placa2.show()
        self.incrementoHeight += 18
        self.hijos.append(placa2)

        # SUPURACIÓN
        supuracion2 = InputSiNo3(numDiente, 3, self, self.incrementoHeight, abajo=True)
        supuracion2.show()
        self.incrementoHeight += 18
        self.hijos.append(supuracion2)

        # MARGEN GINGIVAL
        margenGingival2 = Input3(numDiente, 1, self.incrementoHeight, self, arriba=False)
        margenGingival2.show()
        self.incrementoHeight += 18
        self.hijos.append(margenGingival2)

        # PROFUNDIDAD DE SONDAJE
        profSondaje2 = Input3(numDiente, 2, self.incrementoHeight, self, arriba=False)
        profSondaje2.show()
        self.incrementoHeight += 18
        self.hijos.append(profSondaje2)

        # FURCAS
        if (dientes[numDiente] in furcas or dientes[numDiente + 16*pantallaAct] in [14, 24]) and not datos.implantes[numDiente + 16 * pantallaAct]:
            furca2 = Input2Furcas(self, self.incrementoHeight, numDiente)
        else:
            furca2 = QLabel("", self)
            furca2.setGeometry(QRect(0, self.incrementoHeight, 45, 18))
        furca2.show()
        self.incrementoHeight += 18
        self.hijos.append(furca2)

        if window and (numDiente + 16 * pantallaAct) in datos.inicializados:
            movilidad.setText(str(datos.movilidad[numDiente + 16 * pantallaAct]))
            if datos.implantes[numDiente + 16 * pantallaAct]:
                implante.setChecked(True)
                cambiar_color(implante, "#333333")
            # Si el diente actual tiene furca y no implante, buscamos el dato a introducir
            if dientes[numDiente + 16 * pantallaAct] in furcas and not datos.implantes[numDiente + 16 * pantallaAct]:
                furca.setText(str(datos.defectosfurca[dientes[numDiente + 16 * pantallaAct]][0]))
                furca2.inputs[0].setText(str(datos.defectosfurca[dientes[numDiente + 16 * pantallaAct]][1]))
                furca2.inputs[1].setText(str(datos.defectosfurca[dientes[numDiente + 16 * pantallaAct]][2]))
            for i in range(0, 3):
                if datos.sangrados[numDiente + 16 * pantallaAct][i]:
                    sangrado.botones[i].setChecked(True)
                    cambiar_color(sangrado.botones[i], "#FF2B32")
                if datos.placas[numDiente + 16 * pantallaAct][i]:
                    placa.botones[i].setChecked(True)
                    cambiar_color(placa.botones[i], "#5860FF")
                if datos.supuraciones[numDiente + 16 * pantallaAct][i]:
                    supuracion.botones[i].setChecked(True)
                    cambiar_color(supuracion.botones[i], "#7CEBA0")
                margenGingival.inpts[i].setText(str(datos.margenes[numDiente + 16 * pantallaAct][i]))
                profSondaje.inpts[i].setText(str(datos.profundidades[numDiente + 16 * pantallaAct][i]))
            for i in range(0, 3):
                if datos.sangrados[numDiente + 16 * pantallaAct][i + 3]:
                    sangrado2.botones[i].setChecked(True)
                    cambiar_color(sangrado2.botones[i], "#FF2B32")
                if datos.placas[numDiente + 16 * pantallaAct][i + 3]:
                    placa2.botones[i].setChecked(True)
                    cambiar_color(placa2.botones[i], "#5860FF")
                if datos.supuraciones[numDiente + 16 * pantallaAct][i + 3]:
                    supuracion2.botones[i].setChecked(True)
                    cambiar_color(supuracion2.botones[i], "#7CEBA0")
                margenGingival2.inpts[i].setText(str(datos.margenes[numDiente + 16 * pantallaAct][i + 3]))
                profSondaje2.inpts[i].setText(str(datos.profundidades[numDiente + 16 * pantallaAct][i + 3]))

    def diente_implante(self, numDiente):
        boton = self.hijos[3]
        cambiar_color(boton, "#333333")
        # Actualizamos los datos
        datos.actualizar_implante(numDiente + 16 * pantallaAct, boton.isChecked())

        # Actualizamos la imagen
        window.widgetDientes.actualizar_imagen()
        window.widgetDientesAbajo.actualizar_imagen()
        # Cambiamos el input de la furca si corresponde
        if dientes[numDiente + 16 * pantallaAct] in furcas:
            inptfurca = self.hijos[2]
            self.hijos[2] = None
            inptfurca.deleteLater()
            inptfurcaabajo = self.hijos[14]
            self.hijos[14] = None
            inptfurcaabajo.deleteLater()
            if boton.isChecked():
                newArriba = QLabel("")
                newArriba.setParent(self)
                newArriba.setGeometry(QRect(0, 18 * 2, 45, 18))
                newAbajo = QLabel("")
                newAbajo.setParent(self)
                newAbajo.setGeometry(QRect(0, 611, 45, 18))
            else:
                newArriba = Input03(18 * 2, True, numDiente, self)
                # Añadimos el dato anterior a desactivar la furca por activar implante
                newArriba.setText(str(datos.defectosfurca[dientes[numDiente + 16 * pantallaAct]][0]))
                newAbajo = Input2Furcas(self, 611, numDiente)
                newAbajo.inputs[0].setText(str(datos.defectosfurca[dientes[numDiente + 16 * pantallaAct]][1]))
                newAbajo.inputs[1].setText(str(datos.defectosfurca[dientes[numDiente + 16 * pantallaAct]][2]))
            newArriba.show()
            newAbajo.show()
            self.hijos[2] = newArriba
            self.hijos[14] = newAbajo

    def eliminar_elementos(self):
        while len(self.hijos) > 1:
            hijo = self.hijos.pop()
            if isinstance(hijo, QHBoxLayout):
                self.vaciar_layout(hijo)
            else:
                hijo.deleteLater()

    def vaciar_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.vaciar_layout(child.layout())
        del layout

    def desactivar_activar_diente(self, numDiente):
        # Actualizamos el objeto datos para desactivar o volver a activar el diente
        datos.actualizar_desactivados(int(numDiente + 16 * pantallaAct))
        # Actualizamos los dibujos para que aparezca tachado el diente
        window.widgetDientes.update()
        window.widgetDientesAbajo.update()

        if self.hijos[0].isChecked():
            # Label para la columna superior
            self.eliminar_elementos()
            label = QLabel("", self)
            label.setGeometry(QRect(0, 20, 45, 160))
            self.hijos.append(label)
            label.show()

            # Label para la columna inferior
            label2 = QLabel("", self)
            label2.setGeometry(QRect(0, 500, 45, 100))
            self.hijos.append(label2)
            label2.show()

            # Quitamos los datos del diente de los datos medios
            window.cal.quitarDiente(numDiente)
            window.ppd.quitarDiente(numDiente)
            window.sangrado.quitarDiente(numDiente)
            window.placa.quitarDiente(numDiente)

        else:
            # Volver a introducir los elementos, con los datos anteriores si estaban inicializados
            while len(self.hijos) > 1:
                # Quita el label que ocupaba el espacio mientras el diente estaba desactivado
                hijo = self.hijos.pop()
                if isinstance(hijo, QWidget):
                    hijo.deleteLater()
            self.anhadir_elementos(numDiente)
            window.cal.anhadirDiente(numDiente)
            window.ppd.anhadirDiente(numDiente)
            for i in range(6):
                window.sangrado.actualizarDatos(numDiente * 6 + i,
                                                datos.sangrados[numDiente + 16 * pantallaAct][i])
                window.placa.actualizarDatos(numDiente * 6 + i, datos.placas[numDiente + 16 * pantallaAct][i])


class CuadroColores(QWidget):
    def __init__(self, profundidades, margenes, n, parent=None):
        super().__init__(parent)
        self.n = n
        if margenes is not None:
            # Para los cuadrados de CAL
            # Un site por cada medida del diente (6 por diente, 192 con todos los dientes en la final, 96 con una arcada)
            self.margenes = margenes
            self.profundidades = profundidades
            # Se inicializa
            self.listadatos = [0] * len(margenes) * 6
            self.p = pantallaAct if pantallaAct <= 1 else 0
            for i in range(len(margenes)):
                for j in range(6):
                    self.listadatos[i * 6 + j] = calcular_cal(i + 16*self.p, j)
        else:
            self.listadatos = aplanar_lista(profundidades)
        self.datoscolores = defaultdict(int)
        # Para cada valor que hay en la lista de los datos, contamos el número de veces que aparece
        for i in self.listadatos:
            self.datoscolores[int(i)] += 1

    def minimumSizeHint(self):
        return QSize(1, 1)

    def quitarDiente(self, indice):
        # Restamos las apariciones de los valores de los inputs que tenía diente desactivado
        for i in range(6):
            self.datoscolores[self.listadatos[indice * 6 + i]] -= 1
        self.update()

    def anhadirDiente(self, indice):
        for i in range(6):
            self.datoscolores[self.listadatos[indice * 6 + i]] += 1
        self.update()

    def actualizarDatos(self, indice, nuevo):
        self.datoscolores[self.listadatos[indice]] -= 1
        self.datoscolores[nuevo] += 1
        self.listadatos[indice] = nuevo
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)

        if self.n == 4:
            self.setMinimumSize(191, 87)
            text = "CAL"
            d = ["0", "1-2", "3-4", "≥5"]
            nsites = [str(self.datoscolores[0]), str(self.datoscolores[1] + self.datoscolores[2]),
                      str(self.datoscolores[3] + self.datoscolores[4]),
                      str(sum(self.datoscolores.values()) - sum([self.datoscolores[i] for i in range(0, 5)]))]
        else:
            self.setMinimumSize(228, 87)
            text = "PPD"
            d = ["0-3", "4", "5", "6-8", "≥9"]
            nsites = [str(self.datoscolores[0] + self.datoscolores[1] + self.datoscolores[2] + self.datoscolores[3]),
                      str(self.datoscolores[4]),
                      str(self.datoscolores[5]),
                      str(self.datoscolores[6] + self.datoscolores[7] + self.datoscolores[8]),
                      str(sum(self.datoscolores.values()) - sum([self.datoscolores[i] for i in range(0, 9)]))]

        # Título del cuadro
        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        # CAMBIAR
        qp.drawText(QPoint((self.width() - qp.fontMetrics().horizontalAdvance(text)) / 2, 14), text)

        etiqs = ["mm", "Nº sites", "%"]

        # Ponemos las etiquetas de las filas
        first_h = 32
        total_h = first_h
        ancho_etq = qp.fontMetrics().horizontalAdvance("Nº sites")
        for t in etiqs:
            qp.drawText((ancho_etq - qp.fontMetrics().horizontalAdvance(t)) / 2, total_h, t)
            total_h += qp.fontMetrics().height() + 3

        colores = [Qt.green, Qt.yellow, QColor(255, 136, 30), Qt.red, QColor(200, 0, 0)]
        # Columnas de los datos
        total = sum(self.datoscolores.values()) - self.datoscolores[-1]
        total_w = ancho_etq + 3
        widthcuadro = 37
        for i in range(self.n):
            total_h = first_h
            # Dibujamos los rectángulos de colores
            qp.setPen(QPen(Qt.transparent, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            qp.setBrush(QBrush(colores[i], Qt.SolidPattern))
            qp.drawRect(total_w, 20, widthcuadro, 17)
            # Las etiquetas de las colummnas
            qp.setPen(QPen(Qt.black, 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            qp.drawText(total_w + widthcuadro / 2 - qp.fontMetrics().horizontalAdvance(d[i]) / 2, total_h, d[i])
            total_h += qp.fontMetrics().height() + 4
            # Cantidades
            qp.drawText(total_w + widthcuadro / 2 - qp.fontMetrics().horizontalAdvance(nsites[i]) / 2, total_h,
                        nsites[i])
            total_h += qp.fontMetrics().height() + 3
            # Porcentajes
            if total != 0:
                pct = str(round(int(nsites[i]) / total * 100, 1))
            else:
                pct = "0.0"
            qp.drawText(total_w + widthcuadro / 2 - qp.fontMetrics().horizontalAdvance(pct) / 2, total_h, pct)
            total_w += widthcuadro


class BarraPorcentajes(QWidget):
    def __init__(self, datos_porcent, n, parent=None):
        super().__init__(parent)
        self.porcentaje = 0
        self.datosbarras = aplanar_lista(datos_porcent)
        self.tipo = n

    def minimumSizeHint(self):
        return QSize(1, 1)

    def quitarDiente(self, indice):
        for i in range(6):
            self.datosbarras[indice * 6 + i] = 0
        self.actualizarPorcentajes()

    def actualizarPorcentajes(self):
        if pantallaAct == 0:
            if len(datos.desactivadosSuperior) == 16:
                self.porcentaje = 0
            else:
                self.porcentaje = (sum(self.datosbarras)) / (
                        len(self.datosbarras) - (len(datos.desactivadosSuperior) * 6))
        elif pantallaAct == 1:
            if len(datos.desactivadosInferior) == 16:
                self.porcentaje = 0
            else:
                self.porcentaje = (sum(self.datosbarras)) / (
                        len(self.datosbarras) - (len(datos.desactivadosInferior) * 6))
        else:  # en la pantalla final
            if len(datos.desactivadosSuperior) + len(datos.desactivadosInferior) == 32:
                self.porcentaje = 0
            else:
                self.porcentaje = (sum(self.datosbarras)) / (
                        len(self.datosbarras) - (len(datos.desactivadosSuperior) * 6) - (
                        len(datos.desactivadosInferior) * 6))

    def actualizarDatos(self, indice, nuevo):
        self.datosbarras[indice] = nuevo
        self.actualizarPorcentajes()
        self.update()

    def paintEvent(self, event):
        self.setMinimumSize(150, 80)
        # Pintamos un rectángulo con un % pintado
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        width = 150
        w_coloreado = int(width * self.porcentaje)

        qp.setBrush(QBrush(QColor(220, 220, 220), Qt.SolidPattern))
        if self.tipo == 1:
            # Sangrado
            tit = "BOP"
            color = Qt.red
        elif self.tipo == 2:
            # Placa
            tit = "BPL"
            color = QColor(88, 96, 255)
        else:  # tipo = 3
            # Supuración
            tit = "SUP"
            color = QColor(124, 235, 160)

        qp.setPen(QPen(color, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        # Rectángulo vacío
        qp.drawRect(0, 20, width, 17)
        qp.setBrush(QBrush(color, Qt.SolidPattern))

        # Rectángulo coloreado
        if w_coloreado > 0:
            qp.drawRect(0, 20, w_coloreado, 17)

        # Porcentajes
        txt = "Nº sites = " + str(sum(aplanar_lista(self.datosbarras))) + "; % = " + str(
            round(self.porcentaje * 100, 2)) + "%"

        # Título y porcentajes
        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        qp.drawText(QPoint((width - qp.fontMetrics().horizontalAdvance(tit)) / 2, 14), tit)
        qp.drawText(
            QPoint((width - qp.fontMetrics().horizontalAdvance(txt)) / 2, qp.fontMetrics().height() + 45), txt)


class Datos:
    def __init__(self):
        self.fecha = QDate.currentDate()
        self.examen_inicial = "Examen inicial"
        self.odontologa = ""
        self.paciente = ""
        self.nacimiento = QDate.currentDate()
        self.dientes_perdidos = "0"
        self.tratamiento_prev = "No"
        self.tipo_trat = ""
        self.colapso_mordida = "No"
        self.tabaquismo = "No"
        self.meses_fumando = "0"
        self.cigarrillos_dia = "0"
        self.duracion_ses = "0"
        self.meses_sin_f = "0"

        self.sangrados = [[False, False, False, False, False, False] for _ in range(32)]
        self.placas = [[False, False, False, False, False, False] for _ in range(32)]
        self.supuraciones = [[False, False, False, False, False, False] for _ in range(32)]
        self.margenes = [[0, 0, 0, 0, 0, 0] for _ in range(32)]
        self.profundidades = [[0, 0, 0, 0, 0, 0] for _ in range(32)]
        self.defectosfurca = {}
        for i in furcas_abajo:
            self.defectosfurca[i] = [0, 0, 0]
        self.implantes = [False] * 32
        self.movilidad = [0] * 32
        self.desactivadosSuperior = []
        self.desactivadosInferior = []
        self.inicializados = []

        self.puntosMuestreo = dientes[1:-1]
        self.puntosMuestreo.remove(28)
        self.puntosMuestreo.remove(48)

    def extraerDatos(self):
        dir = os.path.join(basedir, "./excel/datos" + datetime.datetime.now().strftime(
            "%y%m%d%H%M%S") + ".xlsx")
        ruta, _ = QFileDialog.getSaveFileName(window, "Guardar como", dir, "Libro de excel (*.xlsx)")
        if ruta != "":
            dfs = []
            # DATOS DE LOS DIENTES
            for i in range(len(dientes)):
                diente = dientes[i]
                if i not in self.desactivadosInferior and i not in self.desactivadosSuperior and diente in self.puntosMuestreo:
                    # Primera columna con el número del diente
                    data = [self.movilidad[i], self.implantes[i]]
                    if diente in furcas:
                        data.append(self.defectosfurca[diente][0])
                    else:
                        data.append("")
                    data.extend([self.sangrados[i][0], self.placas[i][0], self.supuraciones[i][0], self.margenes[i][0],
                                 self.profundidades[i][0], self.sangrados[i][3], self.placas[i][3],
                                 self.supuraciones[i][3],
                                 self.margenes[i][3], self.profundidades[i][3]])
                    data = [1 if (x == True and isinstance(x, bool)) else 0 if isinstance(x, bool) else x for x in data]
                    dfs.append(pd.DataFrame(data=data, columns=[diente]))
                    data.clear()
                    # Columnas sin número de diente
                    for j in range(1, 3):
                        data = ["", ""]
                        if diente in furcas_abajo:
                            data.append(self.defectosfurca[diente][j])
                        else:
                            data.append("")
                        data.extend(
                            [self.sangrados[i][j], self.placas[i][j], self.supuraciones[i][j], self.margenes[i][j],
                             self.profundidades[i][j], self.sangrados[i][j + 3], self.placas[i][j + 3],
                             self.supuraciones[i][j + 3], self.margenes[i][j + 3], self.profundidades[i][j + 3]])
                        data = [1 if (x == True and isinstance(x, bool)) else 0 if isinstance(x, bool) else x for x in
                                data]
                        dfs.append(pd.DataFrame(data=data, columns=[""]))
            df = pd.concat(dfs, axis=1)
            # Ext para parte externa (vestibular/bucal)
            # Int para parte interna (palatino/lingual)
            df.index = ["Movilidad", "Implante", "Defectos de furca", "Ext.Sangrado al sondaje", "Ext.Placa",
                        "Ext.Supuración",
                        "Ext.Margen gingival", "Ext.Profundidad de sondaje", "Int.Sangrado al sondaje", "Int.Placa",
                        "Int.Supuración",
                        "Int.Margen gingival",
                        "Int.Profundidad de sondaje"]

            # DATOS DEL PACIENTE
            df2 = pd.DataFrame(
                data=[self.fecha.toString("dd/MM/yyyy"), self.odontologa, self.paciente,
                      self.nacimiento.toString("dd/MM/yyyy")])
            df2.index = ["Fecha", "Odontóloga/o", "Paciente", "Fecha de nacimiento"]

            # DATOS CALCULADOS
            datadf3 = []
            # Cuantitativos:
            nimplantes = sum(self.implantes)
            # Media de PPD para los sitios de muestreo
            ppd_suma = sum([sum(self.profundidades[dientes.index(i)]) for i in self.puntosMuestreo])
            ppdmedia = ppd_suma / (len(self.puntosMuestreo) * 6)
            cal_suma = sum([sum([calcular_cal(dientes.index(i), t) for t in range(6)]) for i in self.puntosMuestreo])
            calmedia = cal_suma / (len(self.puntosMuestreo) * 6)
            movilidadmedia = sum([self.movilidad[dientes.index(i)] for i in self.puntosMuestreo]) / len(self.puntosMuestreo)
            datadf3 += [nimplantes, 32 - len(self.desactivadosSuperior) - len(self.desactivadosInferior) - nimplantes,
                        ppdmedia, calmedia, movilidadmedia]
            datadf3 += [sum(1 for ind, i in enumerate(self.movilidad) if i == 0 and dientes[ind] in self.puntosMuestreo),
                        sum(1 for ind, i in enumerate(self.movilidad) if i == 1 and dientes[ind] in self.puntosMuestreo),
                        sum(1 for ind, i in enumerate(self.movilidad) if i == 2 and dientes[ind] in self.puntosMuestreo),
                        sum(1 for ind, i in enumerate(self.movilidad) if i == 3 and dientes[ind] in self.puntosMuestreo)]
            furcas_no_desact = []
            for i in furcas_abajo:
                if i in self.puntosMuestreo:
                    furcas_no_desact.append(i)
            # Media de valores de furca con los dientes con furcas no desactivados
            # Le restamos las dos posiciones de furca superior de 14 y 24
            furcas_suma = sum([sum(self.defectosfurca[i]) for i in furcas_no_desact])
            datadf3 += [furcas_suma / (len(furcas_no_desact) * 3 - 2)]
            valores_furcas = [0, 0, 0, 0]  # 0, 1, 2 o 3
            # recorremos las listas con los 3 valores de furca de cada diente
            # para el 14 y 24, el primer valor va a ser siempre 0
            for i in furcas_no_desact:
                valores_furcas[max(self.defectosfurca[i])] += 1
            datadf3 += valores_furcas
            # Cualitativos
            bop = sum([sum(self.sangrados[dientes.index(i)]) for i in self.puntosMuestreo]) / (
                    len(self.puntosMuestreo) * 6)
            placa = sum([sum(self.placas[dientes.index(i)]) for i in self.puntosMuestreo]) / (
                    len(self.puntosMuestreo) * 6)
            supuracion = sum([sum(self.supuraciones[dientes.index(i)]) for i in self.puntosMuestreo]) / (
                    len(self.puntosMuestreo) * 6)
            datadf3 += [bop, placa, supuracion]
            datadf3 += [self.tratamiento_prev, self.tipo_trat, self.dientes_perdidos, self.colapso_mordida,
                        self.tabaquismo,
                        self.meses_fumando, self.cigarrillos_dia, self.duracion_ses, self.meses_sin_f]

            df3 = pd.DataFrame(data=datadf3)
            df3.index = ["Número total implantes", "Número dientes naturales", "PPD media", "CAL media",
                         "Movilidad media", "Dientes movilidad 0", "Dientes movilidad 1",
                         "Dientes movilidad 2", "Dientes movilidad 3", "Afectación de furca media",
                         "Dientes afectación furca 0", "Dientes afectación furca 1", "Dientes afectación furca 2",
                         "Dientes afectación furca 3", "BOP %", "Placa %", "Supuración %",
                         "Tratamiento previo",
                         "Tipo de tratamiento previo", "Dientes hipermóviles en extracción",
                                                       "Colapso de mordida", "Tabaquismo/vapeo", "Meses fumando",
                         "Cigarrillos/sesiones por día",
                         "Duración sesiones", "Meses sin fumar"]
            try:
                with pd.ExcelWriter(ruta) as writer:
                    df2.to_excel(writer, sheet_name="Datos paciente")
                    df.to_excel(writer, sheet_name="Datos periodontograma")
                    df3.to_excel(writer, sheet_name="Datos calculados")
            except PermissionError:
                print("No se ha podido guardar el archivo")
        else:
            print("Acción cancelada")

    def set_fecha(self, fecha):
        self.fecha = fecha

    def set_examen_inicial(self, examen):
        self.examen_inicial = examen

    def set_odontologa(self, nombre):
        self.odontologa = nombre

    def set_paciente(self, nombre):
        self.paciente = nombre

    def set_nacimiento(self, fecha):
        self.nacimiento = fecha

    def set_dientes_perdidos(self, dientes):
        self.dientes_perdidos = dientes

    def set_tratamiento_prev(self, t):
        self.tratamiento_prev = t

    def set_tipo_trat(self, t):
        self.tipo_trat = t

    def set_colapso(self, t):
        self.colapso_mordida = t

    def set_tabaquismo(self, t):
        self.tabaquismo = t

    def set_meses_fum(self, m):
        self.meses_fumando = m

    def set_cigarrillos(self, c):
        self.cigarrillos_dia = c

    def set_duracion_ses(self, d):
        self.duracion_ses = d

    def set_meses_sin_f(self, m):
        self.meses_sin_f = m

    def actualizar_movilidad(self, diente, valor):
        self.movilidad[int(diente)] = abs(int(valor))
        if int(diente) not in self.inicializados:
            self.inicializados.append(int(diente))

    def actualizar_implante(self, diente, valor):
        self.implantes[int(diente)] = valor
        if int(diente) not in self.inicializados:
            self.inicializados.append(int(diente))

    def actualizar_defecto_furca(self, diente, valor, ind):
        self.defectosfurca[dientes[int(diente)]][int(ind)] = int(valor)
        if int(diente) not in self.inicializados:
            self.inicializados.append(int(diente))

    def actualizar_sangrado(self, diente, i, valor):
        self.sangrados[int(diente)][i] = valor
        if int(diente) not in self.inicializados:
            self.inicializados.append(int(diente))

    def actualizar_placa(self, diente, i, valor):
        self.placas[int(diente)][i] = valor
        if int(diente) not in self.inicializados:
            self.inicializados.append(int(diente))

    def actualizar_supuracion(self, diente, i, valor):
        self.supuraciones[int(diente)][i] = valor
        if int(diente) not in self.inicializados:
            self.inicializados.append(int(diente))

    def actualizar_margen(self, diente, i, valor):
        self.margenes[int(diente)][i] = int(valor)
        if int(diente) not in self.inicializados:
            self.inicializados.append(int(diente))

    def actualizar_profundidad(self, diente, i, valor):
        self.profundidades[int(diente)][i] = abs(int(valor))
        if int(diente) not in self.inicializados:
            self.inicializados.append(int(diente))

    def actualizar_desactivados(self, diente):
        if diente in self.desactivadosSuperior:
            self.desactivadosSuperior.remove(diente)
        elif diente in self.desactivadosInferior:
            self.desactivadosInferior.remove(diente)
        else:
            if diente < 16:
                self.desactivadosSuperior.append(diente)
            else:
                self.desactivadosInferior.append(diente)

    def actualizar_muestreo(self, diente, valor):
        if valor and diente not in self.puntosMuestreo:
            self.puntosMuestreo.append(diente)
        elif not valor:
            if diente in self.puntosMuestreo:
                self.puntosMuestreo.remove(diente)


def clasificacion_inicial():
    interdental = [0, 2, 3, 5]
    ultimo_d_caso1 = -2
    ultimo_d_caso2 = -2
    cal_interd_maximo = 0
    cal_max_todo = 0
    maxppd = 0
    respuesta = []
    for diente in dientes:
        # No se tienen en cuenta los 8s ni los dientes desactivados (no hay diente)
        if diente not in datos.desactivadosSuperior and diente not in datos.desactivadosInferior and diente % 10 != 8:
            if diente % 10 != 7:
                puntos = range(6)
            else:
                # no se tienen en cuenta los puntos distales de los 7s
                # quitamos 0 y 3 para 17 y 47
                # 2 y 5 para 27 y 37
                if diente in [17, 47]:
                    puntos = [1, 2, 4, 5]
                else:  # diente in [27, 37]:
                    puntos = [0, 1, 3, 4]
            for punto in puntos:
                maxppd = max(maxppd, datos.profundidades[dientes.index(diente)][punto])
                cal = calcular_cal(dientes.index(diente), punto)
                cal_max_todo = max(cal, cal_max_todo)
                if punto in interdental and cal >= 1:  # Puntos interdentales
                    if ultimo_d_caso1 != -2 and diente != dientes[ultimo_d_caso1] and diente != dientes[ultimo_d_caso1 + 1]:  # En dos dientes no adyacentes
                        # PERIODONTITIS
                        respuesta = ["Periodontitis: "]
                        respuesta.extend(clasificacion_periodontitis(cal, maxppd))
                    cal_interd_maximo = max(cal, cal_interd_maximo)
                    ultimo_d_caso1 = dientes.index(diente)
                elif punto not in interdental and cal >= 3:  # Puntos mediales
                    if ultimo_d_caso2 != -2 and diente == dientes[ultimo_d_caso2 + 1]:  # En dos dientes adyacentes
                        # PERIODONTITIS
                        respuesta = ["Periodontitis: "]
                        respuesta.extend(clasificacion_periodontitis(cal, maxppd))
                    ultimo_d_caso2 = dientes.index(diente)
    # Si no se cumplió ninguno de esos dos casos
    # Salud o gingivitis
    if not respuesta:
        return [clasificacion_salud_gingivitis(maxppd, cal_max_todo)]
    else:
        return respuesta


def clasificacion_salud_gingivitis(maxppd, calmaxtodo):
    global colorClasificacion
    bop = sum(aplanar_lista(datos.sangrados)) / (
            len(aplanar_lista(datos.sangrados)) - (len(datos.desactivadosSuperior) * 6))
    if bop < 0.1:
        if maxppd <= 3:
            if calmaxtodo >= 1 and datos.tratamiento_prev == "No":
                colorClasificacion = "yellow"
                return "Sano con periodonto reducido"
            else:
                colorClasificacion = "lightgreen"
                return "Sano"
        if maxppd <= 4:
            if calmaxtodo >= 1 and datos.tratamiento_prev == "Si":
                colorClasificacion = "lightgreen"
                return "Salud con periodontitis estable tratado con éxito"
        if maxppd > 3:
            if calmaxtodo == 0:
                colorClasificacion = "lightgreen"
                return "Sano"
    else:
        if maxppd <= 3:
            if calmaxtodo == 0:
                colorClasificacion = "light orange"
                return "Gingivitis"
            elif calmaxtodo >= 1:
                if datos.tratamiento_prev == "No":
                    colorClasificacion = "orange"
                    return "Gingivitis con periodonto reducido"
                else:
                    colorClasificacion = "orange"
                    return "Gingivitis con periodonto reducido y periodontitis estable tratado con éxito"
        else:  # maxppd > 3
            if calmaxtodo == 0:
                colorClasificacion = "light orange"
                return "Gingivitis "
    return "Desconocido"


def clasificacion_periodontitis(cal, maxppd):
    global colorClasificacion
    estadios = []
    dientes_naturales = 32 - len(datos.desactivadosSuperior) - len(datos.desactivadosInferior) - sum(datos.implantes)
    if 1 <= cal <= 2:
        if maxppd <= 4:
            colorClasificacion = "yellow"
            estadios.append("Estadío I ")  # Stage I
        if datos.dientes_perdidos == "1-4":
            colorClasificacion = "red"
            estadios.append("Estadío III ")  # Stage III
    elif 3 <= cal <= 4:
        if maxppd <= 5 and (not 2 in datos.defectosfurca or not 3 in datos.defectosfurca):
            colorClasificacion = "orange"
            estadios.append("Estadío II ")
        if (datos.dientes_perdidos in ["0", "1-4", "Desconocido"] and (maxppd >= 6 or 2 in datos.defectosfurca
                                                                       or 3 in datos.defectosfurca or dientes_naturales >= 20)):
            colorClasificacion = "red"
            estadios.append("Estadío III ")
        if datos.dientes_perdidos == "1-4" and dientes_naturales < 20:
            colorClasificacion = "dark red"
            estadios.append("Estadío IV ")
        if datos.dientes_perdidos == ">=5":
            colorClasificacion = "dark red"
            estadios.append("Estadío IV ")
    elif cal >= 5:
        if datos.dientes_perdidos in ["0", "1-4", "Desconocido"]:
            movilidad = contar_movilidad()
            if movilidad < 2 or datos.colapso_mordida == "No" or dientes_naturales >= 20:
                colorClasificacion = "red"
                estadios.append("Estadío III ")
            if movilidad >= 2 or datos.colapso_mordida == "Sí" or dientes_naturales < 20:
                colorClasificacion = "dark red"
                estadios.append("Estadío IV ")
        else:  # dientes perdidos >= 5
            colorClasificacion = "dark red"
            estadios.append("Estadío IV ")
    if not estadios:
        return ["Estadío no determinado"]
    return estadios


def contar_movilidad():
    return datos.movilidad.count(2) + datos.movilidad.count(3)


class Clasificacion(QLabel):
    def __init__(self, parent):
        global colorClasificacion
        super().__init__(parent)
        self.setStyleSheet("font-weight: bold; font-size: 16px; margin: 5px;" "text-color: " + colorClasificacion + "; padding: 3px; border: 1px solid grey;")
        self.setText("SANO")

    def actualizar(self):
        global colorClasificacion
        clasf = "Diagnóstico: "
        res = clasificacion_inicial()
        for t in res:
            clasf += t
        self.setText(clasf)
        self.setStyleSheet("background-color: " + colorClasificacion + "; font-weight: bold; font-size: 16px; margin: 5px; color: black; padding: 3px; border: 1px solid " + colorClasificacion + "; border-radius: 5px")
        self.adjustSize()


class BotonAnterior(QPushButton):
    def __init__(self, parent, texto):
        super().__init__(parent)
        self.setText(texto)
        self.setStyleSheet(
            "QPushButton { background-color: #DCB5FF; border-radius: 7px; font-size: 15px; font-family: Alata;}"
            "QPushButton:hover { background-color: #BF98E2; }"
            "QPushButton:pressed { background-color: #AC92C4; }")
        self.setCheckable(True)
        self.clicked.connect(self.funcion_clickado)

    def funcion_clickado(self):
        if window:
            anteriorPantalla()


class BotonSiguiente(QPushButton):
    def __init__(self, parent, texto):
        super().__init__(parent)
        self.setText(texto)
        self.setStyleSheet(
            "QPushButton { background-color: #DCB5FF; border-radius: 7px; font-size: 15px; font-family: Alata;}"
            "QPushButton:hover { background-color: #BF98E2; }"
            "QPushButton:pressed { background-color: #AC92C4; }")
        self.setCheckable(True)
        self.clicked.connect(self.funcion_clickado)

    def funcion_clickado(self):
        if window:
            siguientePantalla()


class WindowDientes(QMainWindow):
    def __init__(self, arc):
        super().__init__()
        self.setWindowTitle("Periostage")
        self.setStyleSheet("background-color: #ECECEC;")
        self.setMinimumSize(QSize(300, 300))
        self.resizeEvent = self.actualizar_tam

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.frameTodoTodo = QFrame()
        self.frameTodoTodo.setGeometry(0, 0, self.width() - 10, 675)

        self.frameTitulo = QFrame(self.frameTodoTodo)
        self.frameTitulo.setGeometry(QRect(0, 0, self.width(), 50))

        arcadas = ["Arcada superior", "Arcada inferior", "Pantalla final", "Datos paciente"]

        self.titulo = QLabel(self.frameTitulo)
        self.titulo.setText(arcadas[arc])
        self.titulo.setStyleSheet("font-size: 16pt; font-weight: 350; color: black;")
        self.titulo.adjustSize()
        self.titulo.setGeometry(
            QRect((self.width() - self.titulo.width()) // 2, 10, self.titulo.width(), self.titulo.height()))

        self.anterior = BotonAnterior(self.frameTitulo, arcadas[arc - 1])
        self.anterior.setGeometry(QRect(((self.width() - self.titulo.width()) // 2) - 145, 10, 125, 25))

        self.siguiente = BotonSiguiente(self.frameTitulo, arcadas[arc + 1])
        self.siguiente.setGeometry(
            QRect((((self.width() - self.titulo.width()) // 2) + self.titulo.width() + 20), 10, 125, 25))

        self.frameTodo = QFrame(self.frameTodoTodo)

        self.frameColumnas = QFrame(self.frameTodo)
        self.frameColumnas.setGeometry(QRect(0, 0, self.width(), self.height()))

        self.frameEtiquetas = QFrame(self.frameColumnas)
        tam = QRect(25, 18, 125, self.height())
        self.frameEtiquetas.setGeometry(tam)

        etiquetas = ["Movilidad", "Defecto de furca", "Implante", "Sangrado al sondaje", "Placa", "Supuración",
                     "Margen Gingival", "Profundidad de sondaje"]

        incrementoHeight = 0
        for n in etiquetas:
            label = QLabel(n, self.frameEtiquetas)
            label.setAlignment(Qt.AlignRight)
            label.setGeometry(QRect(0, incrementoHeight, 125, 18))
            incrementoHeight += 18
        self.frameDibujoDientes = QFrame(self.frameTodo)
        self.frameDibujoDientes.setGeometry(QRect(170, 170, self.width() - 176, 137))
        self.widgetDientes = LineasSobreDientes(self.frameDibujoDientes)
        self.widgetDientes.actualizar_todas_alturas()
        etq1 = ["Bucal", "Lingual"]
        labelBucal = QLabel(etq1[pantallaAct], self.frameEtiquetas)
        labelBucal.setStyleSheet("font-weight: bold; font-size: 16px;")
        labelBucal.setGeometry(QRect(70, 205, 125, 18))

        incrementoLeft = 170
        for n in range(0, 8):
            Columna(n, incrementoLeft, parent=self.frameColumnas)
            incrementoLeft += 45 + 4

        incrementoLeft += 16

        for n in range(8, 16):
            Columna(n, incrementoLeft, parent=self.frameColumnas)
            incrementoLeft += 45 + 4

        self.frameDatosMedios = QFrame(self.frameTodo)
        self.frameDatosMedios.setGeometry(200, 297, 970, 90)
        layoutDatosMedios = QHBoxLayout(self.frameDatosMedios)
        self.frameDatosMedios.setStyleSheet("background: none;")
        layoutDatosMedios.setSpacing(20)

        self.ppd = CuadroColores(datos.profundidades[16 * pantallaAct:16 + 16 * pantallaAct], None, 5,
                                 self.frameDatosMedios)
        self.cal = CuadroColores(datos.profundidades[16 * pantallaAct:16 + 16 * pantallaAct],
                                 datos.margenes[16 * pantallaAct:16 + 16 * pantallaAct], 4, self.frameDatosMedios)
        self.sangrado = BarraPorcentajes(datos.sangrados[16 * pantallaAct:16 + 16 * pantallaAct], 1,
                                         self.frameDatosMedios)
        self.placa = BarraPorcentajes(datos.placas[16 * pantallaAct:16 + 16 * pantallaAct], 2, self.frameDatosMedios)

        layoutDatosMedios.addWidget(self.ppd)
        layoutDatosMedios.addWidget(self.cal)
        layoutDatosMedios.addWidget(self.sangrado)
        layoutDatosMedios.addWidget(self.placa)

        self.frameDatosMedios.setLayout(layoutDatosMedios)

        etiquetas2 = ["Sangrado al sondaje", "Placa", "Supuración",
                      "Margen Gingival", "Profundidad de sondaje", "Defectos de furca"]

        incrementoHeight = 505
        for n in etiquetas2:
            label = QLabel(n, self.frameEtiquetas)
            label.setAlignment(Qt.AlignRight)
            label.setGeometry(QRect(0, incrementoHeight, 125, 18))
            incrementoHeight += 18

        self.frameDibujoDientesAbajo = QFrame(self.frameTodo)
        self.frameDibujoDientesAbajo.setGeometry(QRect(170, 385, self.width() - 176, 137))
        etq2 = ["Palatal", "Bucal"]
        labelPalatal = QLabel(etq2[pantallaAct], self.frameEtiquetas)
        labelPalatal.setStyleSheet("font-weight: bold; font-size: 16px;")
        labelPalatal.setGeometry(QRect(70, 420, 125, 18))

        self.widgetDientesAbajo = LineasSobreDientesAbajo(self.frameDibujoDientesAbajo)
        self.widgetDientesAbajo.actualizar_todas_alturas()
        self.frameTodo.adjustSize()
        self.frameTodo.setGeometry(QRect(150, 50, self.frameTodo.width(), self.frameTodo.height()))

        self.scroll_area.setStyleSheet("border: None;")
        self.scroll_area.setWidget(self.frameTodoTodo)
        self.scroll_area.setWidgetResizable(False)

    def actualizar_tam(self, event):
        self.frameTodoTodo.setGeometry(0, 0, self.width(), self.height())
        self.frameTitulo.setGeometry(QRect(0, 0, self.width(), 60))
        self.titulo.setGeometry(
            QRect((self.width() - self.titulo.width()) // 2, 10, self.titulo.width(), self.titulo.height()))
        self.frameColumnas.setGeometry(QRect(0, 0, self.width(), self.height()))
        self.frameEtiquetas.setGeometry(QRect(25, 18, 125, self.height()))
        self.frameDibujoDientes.setGeometry(QRect(170, 170, self.width() - 176, 137))
        self.frameDatosMedios.setGeometry(QRect(150, 297, 820, 90))
        self.frameDibujoDientesAbajo.setGeometry(QRect(170, 380, self.width() - 176, 137))
        self.frameTodo.setGeometry(QRect(150, 50, self.frameTodo.width(), self.height()))

        for columna in self.frameColumnas.findChildren(Columna):
            columna.newsize(self.height())
        self.anterior.setGeometry(QRect(((self.width() - self.titulo.width()) // 2) - 145, 10, 125, 25))
        self.siguiente.setGeometry(
            QRect((((self.width() - self.titulo.width()) // 2) + self.titulo.width() + 20), 10, 125, 25))
        self.scroll_area.setGeometry(0, 0, self.width(), self.height())


class ColumnaFinal(QFrame):
    def __init__(self, numDiente, left, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(left, 0, 45, parent.height()))

        self.ndiente = numDiente

        # Columna arriba
        botonNumeroDiente = QPushButton(str(dientes[numDiente]), self)
        botonNumeroDiente.setCheckable(False)
        botonNumeroDiente.setStyleSheet(style + colorBoton + "font-weight: bold; font-size: 12px;")
        botonNumeroDiente.setGeometry(QRect(0, 0, 45, 18))

        # Sitio de muestreo
        if numDiente not in datos.desactivadosSuperior:
            self.muestreo = QCheckBox(self)
            self.muestreo.setCheckable(True)
            self.muestreo.clicked.connect(self.actmuestreo1)
            if dientes[numDiente] % 10 == 8:
                self.muestreo.setChecked(False)
            else:
                self.muestreo.setChecked(True)
        else:
            self.muestreo = QLabel(self)
        self.muestreo.setGeometry(QRect(15, 18, 15, 18))

        # Columna abajo
        if numDiente + 16 not in datos.desactivadosInferior:
            self.muestreo2 = QCheckBox(self)
            self.muestreo2.setCheckable(True)
            self.muestreo2.clicked.connect(self.actmuestreo2)
            if dientes[numDiente + 16] % 10 == 8:
                self.muestreo2.setChecked(False)
            else:
                self.muestreo2.setChecked(True)
        else:
            self.muestreo2 = QLabel(self)
        self.muestreo2.setGeometry(QRect(15, 650, 15, 18))

        botonNumeroDienteAbajo = QPushButton(str(dientes[numDiente + 16]), self)
        botonNumeroDienteAbajo.setCheckable(False)
        botonNumeroDienteAbajo.setStyleSheet(style + colorBoton + "font-weight: bold; font-size: 12px;")
        botonNumeroDienteAbajo.setGeometry(QRect(0, 668, 45, 18))

    def actmuestreo1(self):
        datos.actualizar_muestreo(dientes[self.ndiente], self.muestreo.isChecked())

    def actmuestreo2(self):
        datos.actualizar_muestreo(dientes[self.ndiente + 16], self.muestreo2.isChecked())


class WindowFinal(QMainWindow):
    def __init__(self):
        global pantallaAct
        super().__init__()
        self.setWindowTitle("Periostage")
        self.setStyleSheet("background-color: #ECECEC ")
        self.setMinimumSize(QSize(300, 300))
        self.resizeEvent = self.actualizar_tam

        self.frameTodo = QFrame()

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # Siempre va a haber scroll vertical

        self.frameTitulo = QFrame(self.frameTodo)
        self.frameTitulo.setGeometry(QRect(0, 0, self.width(), 50))

        self.titulo = QLabel("Vista general", self.frameTitulo)
        self.titulo.setStyleSheet("font-size: 16pt; font-weight: 350; color: black;")
        self.titulo.adjustSize()
        self.titulo.setGeometry(
            QRect((self.width() - self.titulo.width()) // 2, 10, self.titulo.width(), self.titulo.height())
        )

        self.anterior = BotonAnterior(self.frameTitulo, "Arcada inferior")
        self.anterior.setGeometry(QRect(((self.width() - self.titulo.width()) // 2) - 145, 10, 125, 25))

        self.exportar = QPushButton("Exportar", self.frameTitulo)
        self.exportar.setGeometry(
            QRect(((self.width() - self.titulo.width()) // 2) + self.titulo.width() + 20, 10, 125, 25))
        self.exportar.setCheckable(True)
        self.exportar.setStyleSheet(
            "QPushButton { background-color: #9747FF; border-radius: 7px; font-size: 15px; font-family: Alata;}"
            "QPushButton:hover { background-color: #623897; }"
            "QPushButton:pressed { background-color: #4D2A7A; }")
        self.exportar.clicked.connect(lambda: datos.extraerDatos())

        self.frameClasificacion = QFrame(self.frameTodo)
        self.frameClasificacion.setGeometry(QRect(0, 50, self.width(), 50))

        self.clasificacion = Clasificacion(self.frameClasificacion)
        self.clasificacion.actualizar()
        self.clasificacion.setGeometry(
            QRect((self.width() - self.clasificacion.width()) // 2, 0, self.clasificacion.width(),
                  self.clasificacion.height()))

        self.frameCosas = QFrame(self.frameTodo)

        self.frameColumnas = QFrame(self.frameCosas)
        self.frameColumnas.setGeometry(QRect(0, 0, self.width() - 250, 800))

        self.frameEtiquetas = QFrame(self.frameColumnas)
        horizontalAdvanceEt = QFontMetrics(QFont("Alata", 16)).horizontalAdvance("Sitio de muestreo")

        self.frameEtiquetas.setGeometry(QRect(0, 18, horizontalAdvanceEt + 10, 1000))
        labEt = QLabel("Sitios de muestreo", self.frameEtiquetas)
        labEt.setAlignment(Qt.AlignRight)
        labEt.setGeometry(QRect(0, 0, horizontalAdvanceEt, 18))

        lBuc = QLabel("Vestibular", self.frameEtiquetas)
        lBuc.setAlignment(Qt.AlignRight)
        lBuc.setGeometry(QRect(0, 75, horizontalAdvanceEt, 18))
        lBuc.setStyleSheet("font-family: Alata; font-size: 20; font-weight: bold;")

        lPal = QLabel("Palatal", self.frameEtiquetas)
        lPal.setAlignment(Qt.AlignRight)
        lPal.setGeometry(QRect(0, 220, horizontalAdvanceEt, 18))
        lPal.setStyleSheet("font-family: Alata; font-size: 20; font-weight: bold;")

        self.frameDibujosDientesSuperior = QFrame(self.frameCosas)
        self.frameDibujosDientesSuperior.setGeometry(QRect(horizontalAdvanceEt + 35, 42, self.width() - 150 * 2, 270))
        pantallaAct = 0
        self.widgetDientesSuperiorArriba = LineasSobreDientes(self.frameDibujosDientesSuperior)
        self.widgetDientesSuperiorAbajo = LineasSobreDientesAbajo(self.frameDibujosDientesSuperior)
        self.widgetDientesSuperiorArriba.actualizar_todas_alturas()
        self.widgetDientesSuperiorAbajo.actualizar_todas_alturas()
        pantallaAct = 1
        self.widgetDientesSuperiorAbajo.setGeometry(
            QRect(0, 134, self.widgetDientesSuperiorAbajo.width(), self.widgetDientesSuperiorAbajo.height()))

        self.frameDibujosDientesInferior = QFrame(self.frameCosas)
        self.frameDibujosDientesInferior.setGeometry(QRect(horizontalAdvanceEt + 35, 390, self.width() - 150 * 2, 260))
        self.wDInferiorArriba = LineasSobreDientes(self.frameDibujosDientesInferior)
        self.wDInferiorAbajo = LineasSobreDientesAbajo(self.frameDibujosDientesInferior)
        self.wDInferiorArriba.actualizar_todas_alturas()
        self.wDInferiorAbajo.actualizar_todas_alturas()
        pantallaAct = 2
        self.wDInferiorAbajo.setGeometry(0, 120, self.wDInferiorAbajo.width(), self.wDInferiorAbajo.height())

        # Labels bucal y palatal
        incrementoLeft = horizontalAdvanceEt + 30
        for n in range(0, 8):
            ColumnaFinal(n, incrementoLeft, parent=self.frameColumnas)
            incrementoLeft += 45 + 4

        incrementoLeft += 16

        for n in range(8, 16):
            ColumnaFinal(n, incrementoLeft, parent=self.frameColumnas)
            incrementoLeft += 45 + 4

        self.frameDatosMedios = QFrame(self.frameCosas)
        self.frameDatosMedios.setGeometry(180, 300, 850, 90)
        layoutDatosMedios = QHBoxLayout(self.frameDatosMedios)
        self.frameDatosMedios.setStyleSheet("background: none;")
        layoutDatosMedios.setSpacing(20)

        self.ppd = CuadroColores(datos.profundidades, None, 5, self.frameDatosMedios)
        self.cal = CuadroColores(datos.profundidades, datos.margenes, 4, self.frameDatosMedios)
        self.sangrado = BarraPorcentajes(datos.sangrados, 1,
                                         self.frameDatosMedios)
        self.placa = BarraPorcentajes(datos.placas, 2, self.frameDatosMedios)

        layoutDatosMedios.addWidget(self.ppd)
        layoutDatosMedios.addWidget(self.cal)
        layoutDatosMedios.addWidget(self.sangrado)
        layoutDatosMedios.addWidget(self.placa)
        self.frameDatosMedios.setLayout(layoutDatosMedios)

        labEt2 = QLabel("Sitios de muestreo", self.frameEtiquetas)
        labEt2.setAlignment(Qt.AlignRight)
        labEt2.setGeometry(QRect(0, 632, horizontalAdvanceEt, 18))

        lBuc = QLabel("Lingual", self.frameEtiquetas)
        lBuc.setAlignment(Qt.AlignRight)
        lBuc.setGeometry(QRect(0, 425, horizontalAdvanceEt, 18))
        lBuc.setStyleSheet("font-family: Alata; font-size: 20; font-weight: bold;")

        lPal = QLabel("Vestibular", self.frameEtiquetas)
        lPal.setAlignment(Qt.AlignRight)
        lPal.setGeometry(QRect(0, 555, horizontalAdvanceEt, 18))
        lPal.setStyleSheet("font-family: Alata; font-size: 20; font-weight: bold;")

        self.frameCosas.adjustSize()
        self.frameCosas.setGeometry(QRect(125, 100, self.frameCosas.width(), 705))

        self.scroll_area.setStyleSheet("border: None;")
        self.scroll_area.setWidget(self.frameTodo)
        self.scroll_area.setWidgetResizable(False)

    def actualizar_tam(self, event):
        self.frameTodo.setGeometry(0, 0, self.width() - 18, 815)
        self.frameTitulo.setGeometry(QRect(0, 0, self.width(), 50))
        self.titulo.setGeometry(
            QRect((self.width() - self.titulo.width()) // 2, 10, self.titulo.width(), self.titulo.height())
        )
        self.frameClasificacion.setGeometry(QRect(0, 50, self.width(), 50))
        self.clasificacion.setGeometry(
            QRect((self.width() - self.clasificacion.width()) // 2, 10, self.clasificacion.width(),
                  self.clasificacion.height()))
        self.frameColumnas.setGeometry(QRect(0, 0, self.width() - 250, 705))
        horizontalAdvanceEt = QFontMetrics(QFont("Alata", 16)).horizontalAdvance("Sitio de muestreo")
        self.frameDibujosDientesSuperior.setGeometry(QRect(horizontalAdvanceEt + 35, 42, self.width() - 150 * 2, 270))
        self.frameDibujosDientesInferior.setGeometry(QRect(horizontalAdvanceEt + 35, 390, self.width() - 150 * 2, 260))
        self.frameCosas.setGeometry(QRect(125, 100, self.frameColumnas.width(), 705))
        self.scroll_area.setGeometry(0, 0, self.width(), self.height())
        self.scroll_area.setFixedSize(self.width(), self.height())
        self.anterior.setGeometry(QRect(((self.width() - self.titulo.width()) // 2) - 145, 10, 125, 25))
        self.exportar.setGeometry(
            QRect(((self.width() - self.titulo.width()) // 2) + self.titulo.width() + 20, 10, 125, 25))


window = None

pantallaAct = -1


def siguientePantalla():
    global pantallaAct
    global window
    window.deleteLater()
    pantallaAct += 1
    if pantallaAct < 2:
        window = WindowDientes(pantallaAct)
    elif pantallaAct == 2:
        window = WindowFinal()
    window.showMaximized()


def anteriorPantalla():
    global pantallaAct
    global window
    window.deleteLater()
    pantallaAct -= 1
    if pantallaAct >= 0:
        window = WindowDientes(pantallaAct)
    else:
        window = windowIni()
    window.showMaximized()


app = QApplication(sys.argv)
app.setWindowIcon(QIcon(os.path.join(basedir, 'diente.ico')))
datos = Datos()
window = windowIni()
# window = WindowFinal()
# window = WindowDientes(pantallaAct)
window.showMaximized()
app.exec()

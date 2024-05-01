import datetime
import sys
import os
from collections import defaultdict

import pandas as pd
from PIL import Image
from PySide6 import QtGui
from PySide6.QtCore import Qt, QRegularExpression, QRect, QSize, QPoint
from PySide6.QtGui import QRegularExpressionValidator, QImage, QPolygon, QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QWidget, QHBoxLayout, QLineEdit, QPushButton, QPointList, QFrame, QFileDialog
)
from ctypes import windll

try:
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass
# Obtenemos la ruta al directorio del script
basedir = os.path.dirname(__file__)
basedir = os.path.join(basedir, os.pardir)


arriba = [[1, 5], [5, 6], [4, 8], [9, 8], [9, 8], [7, 7], [6, 8], [10, 6], [7, 11], [6, 6], [7, 8], [8, 9], [8, 10],
          [7, 5], [5, 5], [2, 1]]
separaciones = [8, 6, 9, 11, 10, 12, 10, 29, 9, 8, 13, 7, 4, 7, 5, 3]

dientes = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]
furcas = [18, 17, 16, 26, 27, 28]


style = "margin: 0.5px; border: 1px solid grey; border-radius: 3px;"
colorBoton = "background-color: #BEBEBE;"
colorClasificacion = "black"


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
    if i not in window.datos.desactivados:
        return (window.datos.profundidades[i][t] + window.datos.margenes[i][t]) - 2
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


def aplanar_abs_lista(lista):
    salida = []
    for i in lista:
        if isinstance(i, list):
            salida.extend(aplanar_abs_lista(i))
        else:
            salida.append(abs(i))
    return salida


class ImagenDiente(QImage):
    def __init__(self, datos, abajo=""):
        super().__init__()

        width = 0
        # Añadir imagen de los dientes
        self.dientes = []
        for i in range(0, 16):
            if datos.implantes[i]:
                im = Image.open(os.path.join(basedir, "DIENTES", f"periodontograma-i{dientes[i]}{abajo}.png"))
                im = im.resize((int(im.width * 0.88), int(im.height * 0.88)))
                self.dientes.append(im)
                self.dientes[-1] = self.dientes[-1].convert("RGBA")
            else:
                im = Image.open(os.path.join(basedir, "DIENTES", f"periodontograma-{dientes[i]}{abajo}.png"))
                im = im.resize((int(im.width * 0.88), int(im.height * 0.88)))
                # print(im.height)
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
    def __init__(self, datos, parent):
        super().__init__(parent)
        self.imagen = ImagenDiente(datos, "b")
        self.setGeometry(QRect(0, 0, self.width(), self.height()))

        # Inicializamos las listas de los puntos de las líneas
        self.points = QPointList()
        self.points2 = QPointList()
        # De 32 elementos en lugar de 16
        self.puntos_furca = QPointList()

        # Puntos medios de la línea superior de los puntso de furca
        # 2 puntos por diente
        triangulos_abajo = [[0, 0], [0, 0], [72, 10], [75, 32], [71, 9], [73, 33],
                            [69, 10], [72, 34], [77, 12], [78, 26], [0, 0], [0, 0]]

        dist = 0
        self.altura = 57
        # Valores iniciales de los puntos de los dientes
        for i, diente_imagen in enumerate(self.imagen.dientes):
            if dientes[i] in furcas:
                # Hay 2 puntos de furca en la cara que aparece abajo
                self.puntos_furca.append(QPoint(dist + triangulos_abajo[furcas.index(dientes[i]) * 2][1],
                                                triangulos_abajo[furcas.index(dientes[i]) * 2][0]))
                self.puntos_furca.append(QPoint(dist + triangulos_abajo[furcas.index(dientes[i]) * 2 + 1][1],
                                                triangulos_abajo[furcas.index(dientes[i]) * 2 + 1][0]))

            dist += arriba[i][0]
            self.points.append(QPoint(dist, int(self.altura)))
            self.points2.append(QPoint(dist, int(self.altura)))
            wdiente = diente_imagen.width - arriba[i][0] - arriba[i][1]
            self.points.append(QPoint(dist + wdiente // 2, int(self.altura)))
            self.points2.append(QPoint(dist + wdiente // 2, int(self.altura)))
            dist += wdiente
            self.points.append(QPoint(dist, int(self.altura)))
            self.points2.append(QPoint(dist, int(self.altura)))
            dist += arriba[i][1] + separaciones[i]

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
            if i not in window.datos.desactivados:
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
                if (i + 1 not in window.datos.desactivados) and i != 7 and i != 15:
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
                # en la cara inferior hay dos puntos en lugar de uno
                if not window.datos.implantes[i] and dientes[i] in furcas and window.datos.defectosfurca[i] > 0:
                    auxindice = furcas.index(dientes[i])
                    valor = window.datos.defectosfurca[i]
                    qp.setPen(QPen(QColor(165, 10, 135, 210), 1.5, Qt.SolidLine, Qt.SquareCap))
                    for j in range(2):
                        auxpuntos = [self.puntos_furca[auxindice * 2 + j].x(),
                                     self.puntos_furca[auxindice * 2 + j].y()]
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
        self.imagen = ImagenDiente(window.datos, "b")
        self.update()

    def actualizar_alturas(self, numeroDiente, tipo, indice):
        if tipo == 1:  # Margen gingival
            aux = self.points[numeroDiente * 3 + indice]
            aux.setY(int(self.altura - 5 * window.datos.margenes[numeroDiente][indice + 3]))
            self.points[numeroDiente * 3 + indice] = aux
            aux.setY(int(self.points[numeroDiente * 3 + indice].y() + 5 * window.datos.profundidades[numeroDiente][indice + 3]))
            self.points2[numeroDiente * 3 + indice] = aux
        elif tipo == 2:  # Profundidad de sondaje
            aux = self.points[numeroDiente * 3 + indice]
            aux.setY(int(self.altura + 5 * (abs(window.datos.margenes[numeroDiente][indice + 3]) + abs(window.datos.profundidades[numeroDiente][indice + 3]))))
            self.points2[numeroDiente * 3 + indice] = aux
        self.update()

    def def_furca(self):
        self.update()


class LineasSobreDientes(QWidget):
    def __init__(self, datos, parent):
        super().__init__(parent)
        self.imagen = ImagenDiente(datos, "")
        self.setGeometry(QRect(0, 0, self.width(), self.height()))

        # Inicializamos las listas de los puntos de las líneas
        self.points = QPointList()
        self.points2 = QPointList()
        self.puntos_furca = QPointList()

        triangulos_arriba = [[55, 23], [58, 21], [61, 19], [60, 25], [58, 24], [54, 23]]

        dist = 0
        self.altura = 80
        # Valores iniciales de los puntos de los dientes
        for i, diente_imagen in enumerate(self.imagen.dientes):
            if dientes[i] in furcas:
                self.puntos_furca.append(QPoint(dist + triangulos_arriba[furcas.index(dientes[i])][1],
                                                triangulos_arriba[furcas.index(dientes[i])][0]))
            dist += arriba[i][0]
            self.points.append(QPoint(dist, int(self.altura)))  # inicio diente
            self.points2.append(QPoint(dist, int(self.altura)))
            wdiente = diente_imagen.width - arriba[i][0] - arriba[i][1]
            self.points.append(QPoint(dist + wdiente // 2, int(self.altura)))
            self.points2.append(QPoint(dist + wdiente // 2, int(self.altura)))
            dist += wdiente
            self.points.append(QPoint(dist, int(self.altura)))  # fin diente, ppio siguiente
            self.points2.append(QPoint(dist, int(self.altura)))
            dist += arriba[i][1] + separaciones[i]

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
            if i not in window.datos.desactivados:
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
                if (i + 1 not in window.datos.desactivados) and i != 7 and i != 15:
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
                if not window.datos.implantes[i] and dientes[i] in furcas and window.datos.defectosfurca[i] > 0:
                    auxindice = furcas.index(dientes[i])
                    valor = window.datos.defectosfurca[i]
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
        self.imagen = ImagenDiente(window.datos)
        self.update()

    def actualizar_alturas(self, numeroDiente, tipo, indice):
        if tipo == 1:  # Margen gingival
            aux = self.points[numeroDiente * 3 + indice]
            aux.setY(int(self.altura + 5 * window.datos.margenes[numeroDiente][indice]))
            self.points[numeroDiente * 3 + indice] = aux
            aux.setY(int(self.points[numeroDiente * 3 + indice].y() - 5 * window.datos.profundidades[numeroDiente][indice]))
            self.points2[numeroDiente * 3 + indice] = aux
        elif tipo == 2:  # Profundidad de sondaje
            aux = self.points[numeroDiente * 3 + indice]
            aux.setY(int(self.altura + 5 * (window.datos.margenes[numeroDiente][indice] - window.datos.profundidades[numeroDiente][indice])))
            self.points2[numeroDiente * 3 + indice] = aux
        self.update()

    def def_furca(self):
        self.update()


class Input03(QLineEdit):
    def __init__(self, height, furca=False, numDiente=0, parent=None):
        super().__init__(parent)

        regex = QRegularExpression("[0-3]")
        self.setValidator(QRegularExpressionValidator(regex))
        self.setAlignment(Qt.AlignCenter)
        self.setPlaceholderText("0")
        self.editingFinished.connect(lambda: self.guardartexto(numDiente, furca))
        self.setStyleSheet("QLineEdit { " + style + "font-size: 10px;} QLineEdit:focus { border: 1px solid #C3C3C3; }")
        self.setGeometry(QRect(0, height, 45, 18))

    def guardartexto(self, numDiente, furca):
        if furca:
            # actualizar datos
            window.datos.actualizar_defecto_furca(numDiente, self.text())
            # Actualizar dibujo dientes
            window.widgetDientes.update()
        else:
            # actualizar datos
            window.datos.actualizar_movilidad(numDiente, self.text())


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
            window.sangrado.actualizarPorcentajes(numDiente * 6 + ind, boton.isChecked())
            window.datos.actualizar_sangrado(int(numDiente), ind, boton.isChecked())
        elif tipo == 2:
            cambiar_color(boton, "#5860FF")
            window.placa.actualizarPorcentajes(int(numDiente) * 6 + ind, boton.isChecked())
            window.datos.actualizar_placa(int(numDiente), ind, boton.isChecked())
        elif tipo == 3:
            cambiar_color(boton, "#7CEBA0")
            # window.supuracion.actualizarPorcentajes(int(numDiente) * 6 + ind, boton.isChecked())
            window.datos.actualizar_supuracion(int(numDiente), ind, boton.isChecked())


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
        if tipo == 1 and es_numero(inpt.text()):
            if -21 < int(inpt.text()) < 21:
                if arriba:
                    window.datos.actualizar_margen(int(ndiente), num, int(inpt.text()))
                    window.widgetDientes.actualizar_alturas(int(ndiente), tipo, num)
                    window.cal.actualizarDatos(int(ndiente) * 6 + num, calcular_cal(int(ndiente), num))
                else:
                    window.datos.actualizar_margen(int(ndiente), num + 3, int(inpt.text()))
                    window.widgetDientesAbajo.actualizar_alturas(int(ndiente), tipo, num)
                    window.cal.actualizarDatos(int(ndiente) * 6 + num, calcular_cal(int(ndiente), num))
            else:
                inpt.setText("0")
        elif tipo == 2 and es_numero(inpt.text()):  # Profundidad de sondaje
            if 0 < int(inpt.text()) < 21:
                if int(inpt.text()) >= 4:
                    self.inpts[num].setStyleSheet("QLineEdit { " + style + "color: crimson; font-size: 12px; }")
                else:
                    self.inpts[num].setStyleSheet("QLineEdit { " + style + "color: black; font-size: 12px; }")
                if arriba:
                    window.datos.actualizar_profundidad(int(ndiente), num, int(inpt.text()))
                    window.widgetDientes.actualizar_alturas(int(ndiente), tipo, num)
                    window.ppd.actualizarDatos(int(ndiente) * 6 + num, int(inpt.text()))
                    window.cal.actualizarDatos(int(ndiente) * 6 + num, calcular_cal(int(ndiente), num))
                else:
                    window.datos.actualizar_profundidad(int(ndiente), num + 3, int(inpt.text()))
                    window.widgetDientesAbajo.actualizar_alturas(int(ndiente), tipo, num)
                    window.ppd.actualizarDatos(int(ndiente) * 6 + num, int(inpt.text()))
                    window.cal.actualizarDatos(int(ndiente) * 6 + num, calcular_cal(int(ndiente), num))
            else:
                inpt.setText("0")


class Columna(QFrame):
    def __init__(self, numDiente, left, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(left, 0, 45, parent.height()))

        self.incrementoHeight = 0

        botonNumeroDiente = QPushButton(str(dientes[numDiente]), self)
        botonNumeroDiente.setCheckable(True)
        botonNumeroDiente.setDefault(True)
        botonNumeroDiente.setStyleSheet(style + colorBoton + "font-weight: bold; font-size: 12px;")
        botonNumeroDiente.clicked.connect(lambda: self.desactivar_diente(numDiente))
        botonNumeroDiente.setGeometry(QRect(0, self.incrementoHeight, 45, 18))
        self.incrementoHeight += 18

        self.hijos = [botonNumeroDiente]

        self.anhadir_elementos(numDiente)

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
        if dientes[numDiente] in furcas:
            furca = Input03(self.incrementoHeight, True, numDiente, self)
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

        self.incrementoHeight += 137 + 90 + 137 + 10

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

        if window and numDiente in window.datos.inicializados:
            movilidad.setText(str(window.datos.movilidad[numDiente]))
            if window.datos.implantes[numDiente]:
                implante.setChecked(True)
                cambiar_color(implante, "#333333")
            # Si el diente actual tiene furca, buscamos el dato a introducir
            if dientes[numDiente] in furcas:
                furca.setText(str(window.datos.defectosfurca[furcas.index(dientes[numDiente])]))
            for i in range(0, 3):
                if window.datos.sangrados[numDiente][i]:
                    sangrado.botones[i].setChecked(True)
                    cambiar_color(sangrado.botones[i], "#FF2B32")
                if window.datos.placas[numDiente][i]:
                    placa.botones[i].setChecked(True)
                    cambiar_color(placa.botones[i], "#5860FF")
                if window.datos.supuraciones[numDiente][i]:
                    supuracion.botones[i].setChecked(True)
                    cambiar_color(supuracion.botones[i], "#7CEBA0")
                margenGingival.inpts[i].setText(str(window.datos.margenes[numDiente][i]))
                profSondaje.inpts[i].setText(str(window.datos.profundidades[numDiente][i]))
            for i in range(0, 3):
                if window.datos.sangrados[numDiente][i + 3]:
                    sangrado2.botones[i].setChecked(True)
                    cambiar_color(sangrado2.botones[i], "#FF2B32")
                if window.datos.placas[numDiente][i + 3]:
                    placa2.botones[i].setChecked(True)
                    cambiar_color(placa2.botones[i], "#5860FF")
                if window.datos.supuraciones[numDiente][i + 3]:
                    supuracion2.botones[i].setChecked(True)
                    cambiar_color(supuracion2.botones[i], "#7CEBA0")
                margenGingival2.inpts[i].setText(str(window.datos.margenes[numDiente][i + 3]))
                profSondaje2.inpts[i].setText(str(window.datos.profundidades[numDiente][i + 3]))

    def diente_implante(self, numDiente):
        boton = self.hijos[3]
        cambiar_color(boton, "#333333")
        # Actualizamos los datos
        window.datos.actualizar_implante(numDiente, boton.isChecked())

        # Actualizamos la imagen
        window.widgetDientes.actualizar_imagen()
        window.widgetDientesAbajo.actualizar_imagen()
        # Cambiamos el input de la furca si corresponde
        if dientes[numDiente] in furcas:
            inptfurca = self.hijos[2]
            inptfurca.deleteLater()
            self.hijos[2] = None
            if boton.isChecked():
                new = QLabel("")
                new.setParent(self)
                new.setGeometry(QRect(0, 36, 45, 18))
            else:
                new = Input03(36, True, numDiente, self)
                # Añadimos el dato anterior a desactivar la furca por activar implante
                new.setText(str(window.datos.defectosfurca[numDiente]))
            new.show()
            self.hijos[2] = new

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

    def desactivar_diente(self, numDiente):
        window.datos.actualizar_desactivados(int(numDiente))
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
                window.sangrado.actualizarPorcentajes(numDiente * 6 + i, window.datos.sangrados[numDiente][i])
                window.placa.actualizarPorcentajes(numDiente * 6 + i, window.datos.placas[numDiente][i])


class CuadroColores(QWidget):
    def __init__(self, profundidades, margenes, n, parent=None):
        super().__init__(parent)

        self.n = n
        if margenes is not None:
            # Para los cuadrados de CAL
            # Un site por cada medida del diente (6 por diente, 192 con todos los dientes)
            self.margenes = margenes
            self.profundidades = profundidades
            # Se inicializa con todo a 0
            self.listadatos = [0] * 6 * 16
        else:
            self.listadatos = aplanar_lista(profundidades)

        self.datos = defaultdict(int)
        # Para cada valor que hay en la lista de los datos, contamos el número de veces que aparece
        for i in self.listadatos:
            self.datos[int(i)] += 1

    def minimumSizeHint(self):
        return QSize(1, 1)

    def quitarDiente(self, indice):
        # Restamos las aparición de los valores de los inputs que tenía diente desactivado
        for i in range(6):
            self.datos[self.listadatos[indice * 6 + i]] -= 1
        self.update()

    def anhadirDiente(self, indice):
        for i in range(6):
            self.datos[self.listadatos[indice * 6 + i]] += 1
        self.update()

    def actualizarDatos(self, indice, nuevo):
        self.datos[self.listadatos[indice]] -= 1
        self.datos[nuevo] += 1
        self.listadatos[indice] = nuevo
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)

        if self.n == 4:
            self.setMinimumSize(191, 87)
            text = "CAL"
            d = ["0", "1-2", "3-4", "≥5"]
            nsites = [str(self.datos[0]), str(self.datos[1] + self.datos[2]),
                      str(self.datos[3] + self.datos[4]),
                      str(sum(self.datos.values()) - sum([self.datos[i] for i in range(0, 5)]))]
        else:
            self.setMinimumSize(228, 87)
            text = "PPD"
            d = ["0-3", "4", "5", "6-8", "≥9"]
            nsites = [str(self.datos[0] + self.datos[1] + self.datos[2] + self.datos[3]), str(self.datos[4]),
                      str(self.datos[5]), str(self.datos[6] + self.datos[7] + self.datos[8]),
                      str(sum(self.datos.values()) - sum([self.datos[i] for i in range(0, 9)]))]

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
        total = sum(self.datos.values()) - self.datos[-1]
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
    def __init__(self, datos, n, parent=None):
        super().__init__(parent)
        self.porcentaje = 0
        self.datos = aplanar_lista(datos)
        self.tipo = n

    def minimumSizeHint(self):
        return QSize(1, 1)

    def quitarDiente(self, indice):
        for i in range(6):
            self.datos[indice * 6 + i] = 0
        if len(window.datos.desactivados) == 16:
            self.porcentaje = 0
        else:
            self.porcentaje = (sum(self.datos)) / (len(self.datos) - (len(window.datos.desactivados) * 6))
        self.update()

    def actualizarPorcentajes(self, indice, nuevo):
        self.datos[indice] = nuevo
        self.porcentaje = (sum(self.datos)) / (len(self.datos) - (len(window.datos.desactivados) * 6))
        self.update()

    def paintEvent(self, event):
        self.setMinimumSize(150, 80)
        # Pintamos un rectángulo con un % pintado
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        width = 170
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
        txt = "Nº sites = " + str(sum(aplanar_lista(self.datos))) + "; % = " + str(
            round(self.porcentaje * 100, 2)) + "%"

        # Título y porcentajes
        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        qp.drawText(QPoint((self.width() - qp.fontMetrics().horizontalAdvance(tit)) / 2, 14), tit)
        qp.drawText(
            QPoint((self.width() - qp.fontMetrics().horizontalAdvance(txt)) / 2, qp.fontMetrics().height() + 45), txt)


class Datos:
    def __init__(self):
        self.sangrados = [[False, False, False, False, False, False] for _ in range(16)]
        self.placas = [[False, False, False, False, False, False] for _ in range(16)]
        self.supuraciones = [[False, False, False, False, False, False] for _ in range(16)]
        self.margenes = [[0, 0, 0, 0, 0, 0] for _ in range(16)]
        self.profundidades = [[0, 0, 0, 0, 0, 0] for _ in range(16)]
        self.defectosfurca = [0] * 16
        self.implantes = [False] * 16
        self.movilidad = [0] * 16
        self.desactivados = []
        self.inicializados = []

    def extraerDatos(self):
        dir = os.path.join(basedir, "./excel/datos" + datetime.datetime.now().strftime(
                "%y%m%d%H%M%S") + ".xlsx")
        ruta, _ = QFileDialog.getSaveFileName(window, "Guardar como", dir, "Libro de excel (*.xlsx)")
        if ruta != "":
            dfs = []
            for i in range(len(dientes)):
                diente = dientes[i]
                if i not in self.desactivados:
                    dfs.append(pd.DataFrame(
                        data=[self.movilidad[i], self.implantes[i], self.defectosfurca[i], self.sangrados[i][0],
                              self.placas[i][0], self.supuraciones[i][0], self.margenes[i][0], self.profundidades[i][0],
                              self.sangrados[i][3], self.placas[i][3], self.supuraciones[i][3], self.margenes[i][3], self.profundidades[i][3]],
                        columns=[diente]))
                    for j in range(1, 3):
                        dfs.append(pd.DataFrame(data=["", "", "", self.sangrados[i][j], self.placas[i][j],
                                                      self.supuraciones[i][j], self.margenes[i][j],
                                                      self.profundidades[i][j], self.sangrados[i][j + 3], self.placas[i][j + 3],
                                                      self.supuraciones[i][j + 3], self.margenes[i][j + 3], self.profundidades[i][j + 3]], columns=[""]))
            df = pd.concat(dfs, axis=1)
            df.index = ["Movilidad", "Implante", "Defecto de furca", "Sangrado al sondaje", "Placa", "Supuración",
                        "Margen gingival", "Profundidad de sondaje", "Sangrado al sondaje", "Placa", "Supuración", "Margen gingival",
                        "Profundidad de sondaje"]
            df2 = pd.DataFrame(data=[datetime.datetime.now().strftime("%d-%m-%y"), "Mateo García Rodriguez", "Juan Carlos ÁLvarez", "12-05-1984", True, False, False])
            df2.index = ["Fecha", "Odontólogo", "Paciente", "Fecha de nacimiento", "Tratamiento previo", "Colapso de mordida", "Tabaquismo"]
            df3 = pd.DataFrame(data=[])

            with pd.ExcelWriter(ruta) as writer:
                df2.to_excel(writer, sheet_name="Datos paciente")
                df.to_excel(writer, sheet_name="Datos periodontograma")
                df3.to_excel(writer, sheet_name="Datos calculados")
        else:
            print("Acción cancelada")

    def actualizar_movilidad(self, diente, valor):
        self.movilidad[int(diente)] = abs(int(valor))
        if int(diente) not in self.inicializados:
            self.inicializados.append(int(diente))

    def actualizar_implante(self, diente, valor):
        self.implantes[int(diente)] = valor
        if int(diente) not in self.inicializados:
            self.inicializados.append(int(diente))

    def actualizar_defecto_furca(self, diente, valor):
        self.defectosfurca[int(diente)] = abs(int(valor))
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
        if diente in self.desactivados:
            self.desactivados.remove(diente)
        else:
            self.desactivados.append(diente)


# if periodontitis
def calcular_estadio(cal, datos):
    # No se consideran dientes perdidos
    maxpd = max(aplanar_abs_lista(datos.profundidades))
    # if len(datos.desactivados) == 0:
    if 1 <= cal <= 2:
        if maxpd <= 4:
            colorClasificacion = "light orange"
            return "Stage I"
    elif 3 <= cal <= 4:
        if maxpd <= 5:
            colorClasificacion = "orange"
            return "Stage II"
    else:  # >= 5
        if maxpd >= 6:
            n_afectacionfurca = sum(1 for elemento in datos.furcas if elemento > 1)
            if n_afectacionfurca >= 1:
                if len(datos.desactivados) < 2:  # Cantidad de dientes totales >= 20
                    # if no colapso de mordida / disfuncion masticatoria
                    colorClasificacion = "red"
                    return "Stage III"
                # if colapso de mordida / disfuncion masticatoria
                colorClasificacion = "dark red"
                return "Stage IV"
    return "??"


def clasificacion_esquema1():
    # Calcular sangrado medio
    pd = int(sum(aplanar_abs_lista(window.datos.profundidades)) / (
                len(aplanar_abs_lista(window.datos.profundidades)) - (len(window.datos.desactivados) * 6)))
    bop = sum(aplanar_lista(window.datos.sangrados)) / (
                len(aplanar_lista(window.datos.sangrados)) - (len(window.datos.desactivados) * 6))
    margen = sum(aplanar_abs_lista(window.datos.margenes)) / (
                len(aplanar_abs_lista(window.datos.margenes)) - (len(window.datos.desactivados) * 6))
    # calcular rbl/cal
    # TODO: cambiar este cálculo
    cal = int((pd + margen) - 2)

    if pd <= 3:
        if bop < 0.1:
            colorClasificacion = "green"
            return "SANO"
        if cal == 0:
            colorClasificacion = "light orange"
            return "Gingivitis"
        # if tratamiento periodontal -> "Gingivitis en periodonto reducido"
        # if not tratamiento periodontal
        return calcular_estadio(cal, window.datos)
    if bop < 0.1:
        if cal == 0:
            colorClasificacion = "green"
            return "SANO"
        # if tratamiento periodontal -> "Sano en periodonto reducido"
        if pd == 4:
            colorClasificacion = "yellow"
            return "Sano en periodonto reducido"
        return calcular_estadio(cal, window.datos)
    if cal == 0:
        colorClasificacion = "light orange"
        return "Gingivitis"
    return calcular_estadio(cal, window.datos)


class Clasificacion(QLabel):
    def __init__(self, datos):
        super().__init__()
        colorClasificacion = "green"
        self.setStyleSheet("font-weight: bold; font-size: 16px; margin: 5px;" "text-color: " + colorClasificacion)
        self.setText("SANO")

    def actualizar(self):
        self.setText(clasificacion_esquema1())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.datos = Datos()
        self.setWindowTitle("Periostage")
        self.setStyleSheet("background-color: #ECECEC ")
        self.setMinimumSize(QSize(1000, 500))
        self.resizeEvent = self.actualizar_tam

        self.frameTitulo = QFrame(self)
        self.frameTitulo.setStyleSheet("text-align: center;")
        self.frameTitulo.setGeometry(QRect(0, 0, self.width(), 50))

        self.titulo = QLabel(self.frameTitulo)
        self.titulo.setText("Arcada superior")
        self.titulo.setStyleSheet("font-size: 16pt; font-weight: 350; color: black;")
        self.titulo.adjustSize()
        self.titulo.setGeometry(
            QRect((self.width() - self.titulo.width()) // 2, 10, self.titulo.width(), self.titulo.height()))

        self.frameColumnas = QFrame(self)
        self.frameColumnas.setGeometry(QRect(0, 50, self.width(), self.height()))

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
        self.frameDibujoDientes = QFrame(self)
        self.frameDibujoDientes.setGeometry(QRect(170, 220, self.width() - 176, 137))
        self.widgetDientes = LineasSobreDientes(self.datos, self.frameDibujoDientes)

        incrementoLeft = 170
        for n in range(0, 8):
            Columna(n, incrementoLeft, parent=self.frameColumnas)
            incrementoLeft += 45 + 4

        incrementoLeft += 16

        for n in range(8, 16):
            Columna(n, incrementoLeft, parent=self.frameColumnas)
            incrementoLeft += 45 + 4

        self.frameDatosMedios = QFrame(self)
        self.frameDatosMedios.setGeometry(150, 347, 970, 90)
        layoutDatosMedios = QHBoxLayout(self.frameDatosMedios)
        self.frameDatosMedios.setStyleSheet("background:none;")

        #self.clasificacion = Clasificacion(self.datos)
        self.ppd = CuadroColores(self.datos.profundidades, None, 5, self.frameDatosMedios)
        self.cal = CuadroColores(self.datos.profundidades, self.datos.margenes, 4, self.frameDatosMedios)
        self.sangrado = BarraPorcentajes(self.datos.sangrados, 1, self.frameDatosMedios)
        self.placa = BarraPorcentajes(self.datos.placas, 2, self.frameDatosMedios)

        self.boton = QPushButton("Exportar")
        self.boton.setGeometry(QRect(self.width() - 150, 17, 120, 50))
        self.boton.setCheckable(True)
        self.boton.setStyleSheet(
            "QPushButton { background-color: #9747FF; font-size: 12px; border: none; border-radius: 20%; padding: 2px 5px;} QPushButton:hover { background-color: #623897; }")
        self.boton.clicked.connect(lambda: self.datos.extraerDatos())

        # layoutDatosMedios.addWidget(self.clasificacion)
        layoutDatosMedios.addWidget(self.ppd)
        layoutDatosMedios.addWidget(self.cal)
        layoutDatosMedios.addWidget(self.sangrado)
        layoutDatosMedios.addWidget(self.placa)
        layoutDatosMedios.addWidget(self.boton)

        self.frameDatosMedios.setLayout(layoutDatosMedios)

        etiquetas2 = ["Sangrado al sondaje", "Placa", "Supuración",
                      "Margen Gingival", "Profundidad de sondaje"]

        incrementoHeight = 515
        for n in etiquetas2:
            label = QLabel(n, self.frameEtiquetas)
            label.setAlignment(Qt.AlignRight)
            label.setGeometry(QRect(0, incrementoHeight, 125, 18))
            incrementoHeight += 18

        self.frameDibujoDientesAbajo = QFrame(self)
        self.frameDibujoDientesAbajo.setGeometry(QRect(170, 445, self.width() - 176, 137))

        self.widgetDientesAbajo = LineasSobreDientesAbajo(self.datos, self.frameDibujoDientesAbajo)

    def actualizar_tam(self, event):
        self.frameTitulo.setGeometry(QRect(0, 0, self.width(), 60))
        self.titulo.setGeometry(
            QRect((self.width() - self.titulo.width()) // 2, 10, self.titulo.width(), self.titulo.height()))
        self.frameColumnas.setGeometry(QRect(0, 50, self.width(), self.height()))
        self.frameEtiquetas.setGeometry(QRect(25, 18, 125, self.height()))
        self.frameDibujoDientes.setGeometry(QRect(170, 220, self.width() - 176, 137))
        self.frameDatosMedios.setGeometry(QRect(10, 347, 970, 90))
        self.frameDibujoDientesAbajo.setGeometry(QRect(170, 445, self.width() - 176, 137))

        for columna in self.frameColumnas.findChildren(Columna):
            columna.newsize(self.height())


app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'diente.ico')))
window = None
window = MainWindow()
window.showMaximized()
window.show()
app.exec()

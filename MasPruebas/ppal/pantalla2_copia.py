import datetime
import sys, os
from collections import defaultdict

import pandas as pd
from PIL import Image
from PySide6 import QtGui
from PySide6.QtCore import Qt, QRegularExpression, QRect, QSize, QPoint
from PySide6.QtGui import QScreen, QRegularExpressionValidator, QImage, QPolygon, QBrush, QColor, QPainter, QPen, \
    QFontMetricsF
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget, QHBoxLayout, QSpacerItem, QLineEdit, QPushButton, QPointList, QFrame
)

# Obtenemos la ruta al directorio del script
basedir = os.path.dirname(__file__)
basedir = os.path.join(basedir, os.pardir)

try:
    from ctypes import windll

    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

arriba1 = [[1, 5], [5, 6], [4, 8], [9, 8], [9, 8], [7, 7], [6, 8], [10, 6]]  # del 18 al 11
arriba2 = [[7, 11], [6, 6], [7, 8], [8, 9], [8, 10], [7, 5], [5, 5], [2, 1]]  # del 21 al 28

dientes = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]

altura_rojo = [[0, 0, 0] for _ in range(16)]
altura_azul = [[0, 0, 0] for _ in range(16)]

style = "margin: 0.5px; border: 1px solid grey; border-radius: 3px;"


def aplanar_lista(lista):
    salida = []
    for i in lista:
        if isinstance(i, list):
            salida.extend(i)
        else:
            salida.append(i)
    return salida


class LineasSobreDientes(QWidget):
    def __init__(self, datos, *a):
        super().__init__(*a)
        self.imagen = ImagenDiente(18, 10, -1, 21, 29, 1, datos)  # imagen de los dientes con sus atributos

        # inicializamos las listas de los puntos de las líneas
        self.points = QPointList()
        self.points2 = QPointList()
        self.puntos_furca = QPointList()

        self.furcas = [18, 17, 16, 26, 27, 28]

        triangulos_arriba = [[62, 25], [64, 24], [66, 21], [64, 28], [63, 27], [60, 25]]

        dist = 5
        self.altura = 90
        # Valores iniciales de los puntos de los dientes
        for i, diente_imagen in enumerate(self.imagen.dientes1):
            if dientes[i] in self.furcas:
                self.puntos_furca.append(QPoint(dist + triangulos_arriba[self.furcas.index(dientes[i])][1],
                                                triangulos_arriba[self.furcas.index(dientes[i])][0]))
            dist += arriba1[i][0]
            self.points.append(QPoint(dist, int(self.altura)))  # inicio diente
            self.points2.append(QPoint(dist, int(self.altura)))
            wdiente = diente_imagen.width - arriba1[i][0] - arriba1[i][1]
            self.points.append(QPoint(dist + wdiente // 2, int(self.altura)))
            self.points2.append(QPoint(dist + wdiente // 2, int(self.altura)))
            dist += wdiente
            self.points.append(QPoint(dist, int(self.altura)))  # fin diente, ppio siguiente
            self.points2.append(QPoint(dist, int(self.altura)))
            dist += arriba1[i][1]
        dist += 30

        for i, diente_imagen in enumerate(self.imagen.dientes2):
            if dientes[i + 8] in self.furcas:
                self.puntos_furca.append(QPoint(dist + triangulos_arriba[self.furcas.index(dientes[i + 8])][1],
                                                triangulos_arriba[self.furcas.index(dientes[i + 8])][0]))
            dist += arriba2[i][0]
            self.points.append(QPoint(dist, int(self.altura)))
            self.points2.append(QPoint(dist, int(self.altura)))
            wdiente = diente_imagen.width - arriba2[i][0] - arriba2[i][1]
            self.points.append(QPoint(dist + wdiente // 2, int(self.altura)))
            self.points2.append(QPoint(dist + wdiente // 2, int(self.altura)))
            dist += wdiente
            self.points.append(QPoint(dist, int(self.altura)))
            self.points2.append(QPoint(dist, int(self.altura)))
            dist += arriba2[i][1]

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
        altura_ini = -5.6

        # Dibujamos las líneas negras horizontales
        for i in range(1, 18):
            altura_ini += 5.6
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
                if not window.datos.implantes[i] and dientes[i] in self.furcas and window.datos.defectosfurca[self.furcas.index(dientes[i])] > 0:
                    auxindice = self.furcas.index(dientes[i])
                    valor = window.datos.defectosfurca[auxindice]
                    qp.setPen(QPen(QColor(165, 10, 135, 210), 1.5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
                    auxpuntos = [self.puntos_furca[auxindice].x(),
                                 self.puntos_furca[auxindice].y()]
                    (poligono << QPoint(auxpuntos[0] - 8, auxpuntos[1]) <<
                     QPoint(auxpuntos[0], auxpuntos[1] + 11) << QPoint(auxpuntos[0] + 8, auxpuntos[1]))
                    if valor == "1":
                        qp.drawPolyline(poligono)  # triángulo sin cerrar y sin rellenar
                    else:
                        if valor == "3":
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
        self.imagen = ImagenDiente(18, 10, -1, 21, 29, 1, window.datos)

    def actualizar_alturas(self, numeroDiente, tipo, indice):
        if tipo == 1:  # Margen gingival
            aux = self.points[numeroDiente * 3 + indice]
            aux.setY(int(self.altura + 5.6 * altura_rojo[numeroDiente][indice]))
            self.points[numeroDiente * 3 + indice] = aux
            aux = self.points2[numeroDiente * 3 + indice]
            aux.setY(int(self.points[numeroDiente * 3 + indice].y() - 5.6 * altura_azul[numeroDiente][indice]))
            self.points2[numeroDiente * 3 + indice] = aux
        elif tipo == 2:  # Profundidad de sondaje
            aux = self.points[numeroDiente * 3 + indice]
            aux.setY(int(self.altura + 5.6 * (altura_rojo[numeroDiente][indice] - altura_azul[numeroDiente][indice])))
            self.points2[numeroDiente * 3 + indice] = aux

    def def_furca(self, numDiente, valor):
        self.update()


class ImagenDiente(QImage):
    def __init__(self, pos1, pos2, d1, pos3, pos4, d2, datos):
        super(ImagenDiente, self).__init__()

        width = 0
        # Añadir imagen del diente
        self.dientes1 = []
        # primer sector
        for i in range(pos1, pos2, d1):
            if datos.implantes[dientes.index(i)]:
                self.dientes1.append(
                    Image.open(os.path.join(basedir, "DIENTES", f"periodontograma-i{i}.png")))
                self.dientes1[-1] = self.dientes1[-1].convert("RGBA")
            else:
                self.dientes1.append(
                    Image.open(os.path.join(basedir, "DIENTES", f"periodontograma-{i}.png")))
                self.dientes1[-1] = self.dientes1[-1].convert("RGBA")
            width += self.dientes1[-1].width

        # segundo sector
        self.dientes2 = []
        for i in range(pos3, pos4, d2):
            if datos.implantes[dientes.index(i)]:
                self.dientes2.append(
                    Image.open(os.path.join(basedir, "DIENTES", f"periodontograma-i{i}.png")))
                # self.dientes2[-1] = self.dientes2[-1].convert("RGBA")
            else:
                self.dientes2.append(
                    Image.open(os.path.join(basedir, "DIENTES", f"periodontograma-{i}.png")))
                # self.dientes2[-1] = self.dientes2[-1].convert("RGBA")
            width += self.dientes2[-1].width

        imagen = Image.new('RGBA', (width + 40, 156), (0, 0, 0, 0))

        position = 5
        for d in self.dientes1:
            imagen.paste(d, (position, 0))
            position += d.width
        position += 30
        for d in self.dientes2:
            imagen.paste(d, (position, 0))
            position += d.width
        self.swap(imagen.toqimage())


# Input movilidad y defecto de furca
class Input03(QLineEdit):
    def __init__(self, furca=False, numDiente=0):
        super(Input03, self).__init__()
        regex = QRegularExpression("[0-3]")  # Expresión regular que permite solo números
        validator = QRegularExpressionValidator(regex)
        self.setValidator(validator)  # Aplicar la validación al QLineEdit
        self.setAlignment(Qt.AlignCenter)
        self.setPlaceholderText("0")
        self.editingFinished.connect(lambda: self.texto_cambiado(numDiente, furca))
        self.setStyleSheet("QLineEdit { " + style + "font-size: 10px; } QLineEdit:focus { border: 1px solid #C3C3C3; }")

    def texto_cambiado(self, numDiente, furca):
        if furca:
            # actualizar datos
            window.datos.actualizar_defecto_furca(numDiente, self.text())
            # Actualizar dibujo dientes
            window.widgetDientes.update()
        else:
            # actualizar datos
            window.datos.actualizar_movilidad(numDiente, self.text())


colorBoton = "background-color: #BEBEBE;"


def cambiar_color(boton, color):
    if boton.isChecked():
        boton.setStyleSheet(style + f"background-color: {color}")
    else:
        boton.setStyleSheet(style + colorBoton)


class InputSiNo3(QHBoxLayout):
    def __init__(self, numDiente, tipo):
        super(InputSiNo3, self).__init__()

        self.botones = []
        for n in range(1, 4):
            boton = QPushButton("")
            boton.setCheckable(True)
            boton.setStyleSheet("QPushButton { " + style + colorBoton + "}" +
                                "QPushButton:hover { background-color: #AAAAAA; }")
            boton.setDefault(True)
            boton.clicked.connect(lambda *args, ind=n - 1, t=tipo: self.pulsar_boton(ind, numDiente, t))
            self.addWidget(boton)
            self.botones.append(boton)

    def pulsar_boton(self, ind, numDiente, tipo):
        boton = self.botones[ind]

        if tipo == 1:
            cambiar_color(boton, "#FF2B32")
            window.sangrado.actualizarPorcentajes(int(numDiente) * 3 + ind, boton.isChecked())
            window.datos.actualizar_sangrado(int(numDiente), ind, boton.isChecked())
        elif tipo == 2:
            cambiar_color(boton, "#5860FF")
            window.placa.actualizarPorcentajes(int(numDiente) * 3 + ind, boton.isChecked())
            window.datos.actualizar_placa(int(numDiente), ind, boton.isChecked())
        elif tipo == 3:
            cambiar_color(boton, "#7CEBA0")
            # window.supuracion.actualizarPorcentajes(int(numDiente) * 3 + ind, boton.isChecked())
            window.datos.actualizar_supuracion(int(numDiente), ind, boton.isChecked())


def es_numero(texto):
    if len(texto) == 0:
        return False
    if texto[0] in ('-', '+'):
        return texto[1:].isdigit()
    return texto.isdigit()


class Input3(QHBoxLayout):
    def __init__(self, ndiente, tipo):
        super(Input3, self).__init__()
        self.validator = QRegularExpressionValidator(QRegularExpression(r"^[+-]?\d{1,2}$"))

        self.inpts = []

        for i in range(1, 4):
            inpt = QLineEdit()
            inpt.setValidator(self.validator)
            inpt.setStyleSheet(
                "QLineEdit { " + style + "font-size: 10px; } QLineEdit:focus { border: 1px solid #C3C3C3; }")
            inpt.setPlaceholderText("0")
            inpt.editingFinished.connect(lambda ind=i - 1: self.texto(ndiente, tipo, ind))
            self.addWidget(inpt)
            self.inpts.append(inpt)

    def texto(self, ndiente, tipo, num):
        inpt = self.inpts[num]
        if tipo == 1 and es_numero(inpt.text()):  # Margen gingival
            if -21 < int(inpt.text()) < 21:
                altura_rojo[int(ndiente)][num] = int(inpt.text())
                window.widgetDientes.actualizar_alturas(int(ndiente), tipo, num)
                window.widgetDientes.update()
                window.cal.actualizarDatos(int(ndiente) * 3 + num, abs(int(inpt.text())))
                window.datos.actualizar_margen(int(ndiente), num, abs(int(inpt.text())))
            else:
                inpt.setText("0")
        elif tipo == 2 and es_numero(inpt.text()):  # Profundidad de sondaje
            if 0 < int(inpt.text()) < 21:
                if (int(inpt.text()) >= 4):
                    self.inpts[num].setStyleSheet("QLineEdit { " + style + "color: crimson; font-size: 12px; }")
                else:
                    self.inpts[num].setStyleSheet("QLineEdit { " + style + "color: black; font-size: 12px; }")
                altura_azul[int(ndiente)][num] = int(inpt.text())
                window.widgetDientes.actualizar_alturas(int(ndiente), tipo, num)
                window.widgetDientes.update()
                window.ppd.actualizarDatos(int(ndiente) * 3 + num, abs(int(inpt.text())))
                window.datos.actualizar_profundidad(int(ndiente), num, abs(int(inpt.text())))
            else:
                inpt.setText("0")


class BarraPorcentajes(QWidget):
    def __init__(self, datos, n):
        super().__init__()
        self.setGeometry(QRect(0, 0, 220, 81))
        self.porcentaje = 0
        self.datos = aplanar_lista(datos)
        self.tipo = n

    def minimumSizeHint(self):
        return QSize(1, 1)

    def actualizarPorcentajes(self, indice, nuevo):
        self.datos[indice] = nuevo
        self.porcentaje = (sum(self.datos)) / len(self.datos)
        self.update()

    def paintEvent(self, event):
        self.setMinimumSize(220, 100)
        # Pintamos un rectángulo con un % pintado
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        width = 220
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
        qp.drawRect(0, 20, width, 20)
        qp.setBrush(QBrush(color, Qt.SolidPattern))

        # Rectángulo coloreado
        if w_coloreado > 0:
            qp.drawRect(0, 20, w_coloreado, 20)

        # Porcentajes
        txt = "Nº sites = " + str(sum(aplanar_lista(self.datos))) + "; % = " + str(
            round(self.porcentaje * 100, 2)) + "%"

        # Título y porcentajes
        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        qp.drawText(QPoint((self.width() - qp.fontMetrics().horizontalAdvance(tit)) / 2, 14), tit)
        qp.drawText(
            QPoint((self.width() - qp.fontMetrics().horizontalAdvance(txt)) / 2, qp.fontMetrics().height() + 45), txt)


class CuadroColores(QWidget):
    def __init__(self, datos, n):
        super().__init__()
        self.setGeometry(QRect(0, 0, 265, 81))

        self.n = n
        self.listadatos = aplanar_lista(datos)
        self.datos = defaultdict(int)
        for i in self.listadatos:
            self.datos[int(i)] += 1

    def minimumSizeHint(self):
        return QSize(1, 1)

    def actualizarDatos(self, indice, nuevo):
        self.datos[self.listadatos[indice]] -= 1
        self.datos[nuevo] += 1
        self.listadatos[indice] = nuevo
        self.update()

    def paintEvent(self, event):
        self.setMinimumSize(265, 81)

        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)

        if self.n == 4:
            text = "CAL"
            d = ["0", "1-2", "3-4", "≥5"]
            nsites = [str(self.datos[0]), str(self.datos[1] + self.datos[2]),
                      str(self.datos[3] + self.datos[4]),
                      str(sum(self.datos.values()) - sum([self.datos[i] for i in range(0, 5)]))]
        else:
            text = "PPD"
            d = ["0-3", "4", "5", "6-8", "≥9"]
            nsites = [str(self.datos[0] + self.datos[1] + self.datos[2] + self.datos[3]), str(self.datos[4]),
                      str(self.datos[5]), str(self.datos[6] + self.datos[7] + self.datos[8]),
                      str(sum(self.datos.values()) - sum([self.datos[i] for i in range(0, 9)]))]

        # Título del cuadro
        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        qp.drawText(QPoint((self.width() - qp.fontMetrics().horizontalAdvance(text)) / 2, 14), text)

        etiqs = ["mm", "Nº sites", "%"]

        # Ponemos las etiquetas de las filas
        first_h = 35
        total_h = first_h
        ancho_etq = qp.fontMetrics().horizontalAdvance("Nº sites")
        for t in etiqs:
            qp.drawText((ancho_etq - qp.fontMetrics().horizontalAdvance(t)) / 2, total_h, t)
            total_h += qp.fontMetrics().height() + 7

        colores = [Qt.green, Qt.yellow, QColor(255, 136, 30), Qt.red, QColor(200, 0, 0)]
        # Columnas de los datos
        total = sum(self.datos.values()) - self.datos[-1]
        total_w = ancho_etq + 5
        widthcuadro = 220 / self.n
        for i in range(self.n):
            total_h = first_h
            # Dibujamos los rectángulos de colores
            qp.setPen(QPen(Qt.transparent, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            qp.setBrush(QBrush(colores[i], Qt.SolidPattern))
            qp.setBrush(QBrush(colores[i], Qt.SolidPattern))
            qp.drawRect(total_w, 20, widthcuadro, 20)
            # Las etiquetas de las colummnas
            qp.setPen(QPen(Qt.black, 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            qp.drawText(total_w + widthcuadro / 2 - qp.fontMetrics().horizontalAdvance(d[i]) / 2, total_h, d[i])
            total_h += qp.fontMetrics().height() + 7
            # Cantidades
            qp.drawText(total_w + widthcuadro / 2 - qp.fontMetrics().horizontalAdvance(nsites[i]) / 2, total_h,
                        nsites[i])
            total_h += qp.fontMetrics().height() + 7
            # Porcentajes
            if total != 0:
                pct = str(round(int(nsites[i]) / total * 100, 1))
            else:
                pct = "0.0"
            qp.drawText(total_w + widthcuadro / 2 - qp.fontMetrics().horizontalAdvance(pct) / 2, total_h, pct)
            total_w += widthcuadro


class Datos():
    def __init__(self):
        self.sangrados = [[False, False, False] for _ in range(16)]
        self.placas = [[False, False, False] for _ in range(16)]
        self.supuraciones = [[False, False, False] for _ in range(16)]
        self.margenes = [[0, 0, 0] for _ in range(16)]
        self.profundidades = [[0, 0, 0] for _ in range(16)]
        self.defectosfurca = [0] * 16
        self.implantes = [False] * 16
        self.movilidad = [0] * 16
        self.desactivados = []
        self.inicializados = []

    def extraerDatos(self):
        data = {}
        for i in range(len(dientes)):
            diente = dientes[i]
            if diente not in self.desactivados:
                data[int(diente)] = [self.movilidad[i], self.implantes[i], self.defectosfurca[i], self.sangrados[i],
                                     self.placas[i], self.supuraciones[i], self.margenes[i], self.profundidades[i]]
        df = pd.DataFrame(data)
        df.index = ["Movilidad", "Implante", "Defecto de furca", "Sangrado al sondaje", "Placa", "Supuración",
                    "Margen gingival", "Profundidad de sondaje"]
        df.to_excel(os.path.join(basedir, "./excel/datos" + datetime.datetime.now().strftime("%y%m%d%H%M%S") + ".xlsx"))

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
        self.margenes[int(diente)][i] = abs(int(valor))
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


class Columna(QVBoxLayout):
    def __init__(self, numDiente, defFurca):
        super(Columna, self).__init__()

        botonNumeroDiente = QPushButton(str(dientes[int(numDiente)]))
        botonNumeroDiente.setCheckable(True)
        botonNumeroDiente.setStyleSheet(style + "background-color: #BEBEBE; font-weight: bold; font-size: 12px;")
        botonNumeroDiente.clicked.connect(lambda: self.desactivar_diente(numDiente, defFurca))
        self.addWidget(botonNumeroDiente)

        self.anhadir_elementos(numDiente, defFurca)

    def anhadir_elementos(self, numDiente, defFurca):
        # MOVILIDAD
        movilidad = Input03(False, numDiente)

        # DEFECTO DE FURCA
        if defFurca:
            furca = Input03(True, numDiente)
        else:
            furca = QLabel("")
            furca.setFixedSize(76, 22)

        # IMPLANTE
        boton = QPushButton("")
        boton.setCheckable(True)
        boton.setStyleSheet(
            "QPushButton { " + style + " background-color: #BEBEBE; } QPushButton:hover { background-color: #AAAAAA; }")
        boton.setDefault(True)
        boton.clicked.connect(lambda: self.diente_implante(numDiente, defFurca))

        # SANGRADO AL SONDAJE
        sangrado = InputSiNo3(numDiente, 1)

        # PLACA
        placa = InputSiNo3(numDiente, 2)

        # SUPURACION
        supuracion = InputSiNo3(numDiente, 3)

        # MARGEN GINGIVAL
        margenGingival = Input3(numDiente, 1)

        # PROFUNDIDAD DE SONDAJE
        profSondaje = Input3(numDiente, 2)

        numDiente = int(numDiente)

        if window and numDiente in window.datos.inicializados:
            movilidad.setText(str(window.datos.movilidad[numDiente]))
            if window.datos.implantes[numDiente]:
                boton.setChecked(True)
                cambiar_color(boton, "#333333")
            furca.setText(str(window.datos.defectosfurca[numDiente]))
            for i in range(0, 3):
                if window.datos.sangrados[numDiente + i]:
                    sangrado.layout().itemAt(i).widget().setChecked(True)
                    cambiar_color(sangrado.layout().itemAt(i).widget(), "#FF2B32")
                if window.datos.placas[numDiente + i]:
                    placa.layout().itemAt(i).widget().setChecked(True)
                    cambiar_color(placa.layout().itemAt(i).widget(), "#5860FF")
                if window.datos.supuraciones[numDiente + i]:
                    supuracion.layout().itemAt(i).widget().setChecked(True)
                    cambiar_color(supuracion.layout().itemAt(i).widget(), "#7CEBA0")
                margenGingival.layout().itemAt(i).widget().setText(str(window.datos.margenes[numDiente + i]))
                profSondaje.layout().itemAt(i).widget().setText(str(window.datos.profundidades[numDiente + i]))

        # añadimos los elementos
        self.addWidget(movilidad)
        self.addWidget(boton)
        self.addWidget(furca)
        self.addLayout(sangrado)
        self.addLayout(placa)
        self.addLayout(supuracion)
        self.addLayout(margenGingival)
        self.addLayout(profSondaje)

    def diente_implante(self, numDiente, deffurca):
        boton = self.layout().itemAt(2).widget()
        cambiar_color(boton, "#333333")
        # Actualizamos los datos
        window.datos.actualizar_implante(int(numDiente), boton.isChecked())

        # Actualizamos la imagen
        window.widgetDientes.actualizar_imagen()
        window.widgetDientes.update()
        # Desactivamos el input de la furca
        if deffurca == 1:
            inptfurca = self.layout().itemAt(3).widget()
            self.layout().removeWidget(inptfurca)
            inptfurca.deleteLater()
            if boton.isChecked():
                new = QLabel("")
                new.setFixedSize(76, 22)
            else:
                if deffurca == 1:
                    new = Input03(True, numDiente)
                else:
                    new = QLabel("")
                    new.setFixedSize(76, 22)
            self.layout().insertWidget(3, new)

    def eliminar_elementos(self, layout, ini):
        while layout.count() > ini:
            item = layout.takeAt(ini)
            if item:
                if isinstance(item, QHBoxLayout):
                    self.eliminar_elementos(item.layout(), 0)
                else:
                    widget = item.widget()
                    if widget:
                        layout.removeWidget(widget)
                        widget.deleteLater()
                    else:
                        layout.removeItem(item)

    def desactivar_diente(self, numDiente, defFurca):
        window.widgetDientes.update()
        window.datos.actualizar_desactivados(int(numDiente))
        # Si el botón de diente está pulsado, es decir, el diente está desactivado
        if self.itemAt(0).widget().isChecked():
            # Cogemos el tamaño de la columna
            geom = self.geometry()
            geom.setHeight(geom.height() - self.itemAt(0).geometry().height())
            # Quitamos todos los elementos del layout excepto el primero
            self.eliminar_elementos(self.layout(), 1)

            # Añadimos elementos no interaccionables
            label = QLabel("")
            # label.setFrameStyle(QLabel.Panel | QLabel.Sunken)
            # label.setFocusPolicy(Qt.NoFocus)
            label.setGeometry(geom)
            self.addWidget(label)
        else:
            while self.layout().count() > 1:
                child = self.layout().takeAt(1)
                if child.widget():
                    self.layout().removeWidget(child.widget())
                    child.widget().deleteLater()
            self.anhadir_elementos(numDiente, defFurca)


class ExtraerInformacion(QPushButton):
    def __init__(self):
        super(ExtraerInformacion, self).__init__()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Periostage")
        self.screen = QScreen().geometry()
        self.setStyleSheet("background-color: #ECECEC ")
        self.setMinimumSize(QSize(1000, 500))
        # self.setWindowState(Qt.WindowMaximized)
        self.ppd = None
        self.cal = None
        self.sangrado = None
        self.placa = None
        self.supuracion = None
        self.widgetDientes = None
        self.datos = Datos()
        self.elementos_pantalla()

    def elementos_pantalla(self):
        tit = QHBoxLayout()
        titu = QLabel("Arcada superior")
        tit.addWidget(titu)
        tit.setAlignment(Qt.AlignCenter)

        layoutCuadro1 = QHBoxLayout()

        # Etiquetas
        frameEtiquetas = QFrame()
        layoutEtiquetas = QVBoxLayout()
        etiquetas = ["", "Movilidad", "Implante", "Defecto de furca",
                     "Sangrado al sondaje", "Placa", "Supuración", "Margen Gingival", "Profundidad de sondaje"]

        for n in etiquetas:
            label = QLabel(n)
            # Alineamos el texto a la derecha
            label.setAlignment(Qt.AlignRight)
            layoutEtiquetas.addWidget(label)
        layoutEtiquetas.setSpacing(2)

        layoutCuadro1.addWidget(frameEtiquetas)

        frameEtiquetas.setGeometry(QRect(0, 0, self.fontMetrics().horizontalAdvance("Profundidad de sondaje"),
                                         len(etiquetas) * self.fontMetrics().height()))
        frameEtiquetas.setLayout(layoutEtiquetas)

        # Creamos antes la imagen de los dientes para poder pasar el objeto y actualizarlo
        self.widgetDientes = LineasSobreDientes(self.datos)

        layoutColumnas = QHBoxLayout()
        layoutColumnas.setAlignment(Qt.AlignLeft)
        for n in range(0, 3):
            col = Columna(str(n), True)
            col.setSpacing(0)
            layoutColumnas.addLayout(col)

        for n in range(3, 8):
            col = Columna(str(n), False)
            col.setSpacing(0)
            layoutColumnas.addLayout(col)

        layoutColumnas.addSpacerItem(QSpacerItem(20, frameEtiquetas.height()))

        for n in range(8, 13):
            col = Columna(str(n), False)
            col.setSpacing(0)
            layoutColumnas.addLayout(col)

        for n in range(13, 16):
            col = Columna(str(n), True)
            col.setSpacing(0)
            layoutColumnas.addLayout(col)

        layoutCuadro1.addLayout(layoutColumnas)

        self.ppd = CuadroColores(self.datos.profundidades, 5)
        self.cal = CuadroColores(self.datos.margenes, 4)
        self.sangrado = BarraPorcentajes(self.datos.sangrados, 1)
        self.placa = BarraPorcentajes(self.datos.placas, 2)
        # self.supuracion = BarraPorcentajes(self.datos.supuraciones, 3)

        layoutCuadro1.setContentsMargins(10, 5, 10, 10)
        layoutCuadro1.setSpacing(5)

        # Dientes
        layoutDientes = QHBoxLayout()
        layoutDientes.addWidget(QLabel("Vestibular"))
        layoutDientes.addWidget(self.widgetDientes)
        layoutDientes.setAlignment(Qt.AlignCenter)

        # Botón extraer información
        boton = QPushButton()
        boton.setGeometry(QRect(self.screen.width() - 150, self.screen.height() - 70, 120, 50))
        boton.setText("Exportar")
        boton.setCheckable(True)
        boton.setStyleSheet(
            "QPushButton { background-color: #9747FF; font-size: 12px; border-radius: 10px; padding: 3px 7px;} QPushButton:hover { background-color: #623897; }")
        boton.clicked.connect(lambda: self.datos.extraerDatos())

        # Datos medios
        layoutDatos = QHBoxLayout()
        layoutDatos.addWidget(self.ppd)
        layoutDatos.addWidget(self.cal)
        layoutDatos.addWidget(self.sangrado)
        layoutDatos.addWidget(self.placa)
        # layoutDatos.addWidget(self.supuracion)
        layoutDatos.addWidget(boton)
        layoutDatos.setAlignment(Qt.AlignCenter)

        total = QVBoxLayout()
        total.addLayout(tit)
        total.addLayout(layoutCuadro1)
        total.addLayout(layoutDientes)
        total.addLayout(layoutDatos)

        widget = QWidget()
        widget.setLayout(total)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
# app.setWindowIcon(QtGui.QIcon(f"C:/Users/Uxi/Documents/TFG/MasPruebas/diente.ico"))
app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'diente.ico')))
window = None
window = MainWindow()
window.showMaximized()
window.show()
app.exec()

import sys
from PIL import Image
from PySide6.QtCore import Qt, QRegularExpression, QRect, QSize, QPoint
from PySide6.QtGui import QScreen, QRegularExpressionValidator, QImage, QPolygon, QBrush, QGradient, QColor
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget, QHBoxLayout, QSpacerItem, QLineEdit, QPushButton, QPointList
)
from PySide6.QtGui import QPainter, QPen

arriba1 = [[1, 5], [5, 6], [4, 8], [9, 8], [9, 8], [7, 7], [6, 8], [10, 6]]  # del 18 al 11
arriba2 = [[7, 11], [6, 6], [7, 8], [8, 9], [8, 10], [7, 5], [5, 5], [2, 1]]  # del 21 al 28

dientes = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]

altura_rojo = [[0, 0, 0] for _ in range(16)]
altura_azul = [[0, 0, 0] for _ in range(16)]

style = "margin: 1px; border: 1px solid grey; border-radius: 3px;"

class LineasSobreDientes(QWidget):
    def __init__(self, imagen, *a):
        super().__init__(*a)
        self.imagen = imagen  # imagen de los dientes con sus atributos


    def paintEvent(self, event):
        qp = QPainter(self)
        imagen = QImage(self.imagen)  # imagen de los dientes
        tam = QRect(0, 0, imagen.width(), imagen.height())
        self.setMinimumSize(imagen.width(), imagen.height())
        qp.drawImage(tam, imagen)  # dibujar una línea

        pen = qp.pen()
        pen.setWidth(1.5)
        qp.setPen(pen)
        altura = -5.6
        for i in range(1, 18):
            altura += 5.6
            qp.drawLine(0, altura, tam.width(), altura)
        # termina con la altura de la última línea

        self.points = QPointList()
        self.points2 = QPointList()

        dist = 5  # inicio de la imagen del primer diente
        for i, diente in enumerate(self.imagen.dientes1):
            dist += arriba1[i][0]
            self.points.append(QPoint(dist, int(altura + 5.6*altura_rojo[i][0])))  # inicio diente
            self.points2.append(QPoint(dist, int(altura + 5.6*(altura_rojo[i][0] - altura_azul[i][0]))))
            wdiente = diente.width - arriba1[i][0] - arriba1[i][1]
            self.points.append(QPoint(dist + wdiente // 2, int(altura + 5.6*altura_rojo[i][1])))
            self.points2.append(QPoint(dist + wdiente // 2, int(altura + 5.6*(altura_rojo[i][1] - altura_azul[i][1]))))
            dist += wdiente
            self.points.append(QPoint(dist, int(altura + 5.6*altura_rojo[i][2])))  # fin diente, ppio siguiente
            self.points2.append(QPoint(dist, int(altura + 5.6*(altura_rojo[i][2] - altura_azul[i][2]))))
            dist += arriba1[i][1]

        dist += 30  # separación entre bloques de dientes

        for i, diente in enumerate(self.imagen.dientes2):
            dist += arriba2[i][0]
            self.points.append(QPoint(dist, int(altura + 5.6*altura_rojo[i+8][0])))
            self.points2.append(QPoint(dist, int(altura + 5.6*(altura_rojo[i+8][0] - altura_azul[i+8][0]))))
            wdiente = diente.width - arriba2[i][0] - arriba2[i][1]
            self.points.append(QPoint(dist + wdiente // 2, int(altura + 5.6*altura_rojo[i+8][1])))
            self.points2.append(QPoint(dist + wdiente // 2, int(altura + 5.6*(altura_rojo[i+8][1] -
                                                                              altura_azul[i+8][1]))))
            dist += wdiente
            self.points.append(QPoint(dist, int(altura + 5.6*altura_rojo[i+8][2])))
            self.points2.append(QPoint(dist, int(altura + 5.6*(altura_rojo[i+8][2] - altura_azul[i+8][2]))))
            dist += arriba2[i][1]

        qp.setPen(QPen(Qt.blue, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.drawPolyline(self.points2)
        qp.setPen(QPen(Qt.red, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        qp.drawPolyline(self.points)

        poligono = QPolygon()
        for punto in self.points:
            poligono.append(punto)
        for punto in reversed(self.points2):
            poligono.append(punto)

        brush = QBrush(QColor(50, 0, 100, 100))
        qp.setPen(QPen(Qt.NoPen))
        qp.setBrush(brush)
        qp.drawPolygon(poligono)

    def minimumSizeHint(self):
        return QSize(1, 1)


class ImagenDiente(QImage):
    def __init__(self, pos1, pos2, d1, pos3, pos4, d2):
        super(ImagenDiente, self).__init__()

        width = 0
        # Añadir imagen del diente
        self.dientes1 = []
        # primer sector
        for i in range(pos1, pos2, d1):
            self.dientes1.append(Image.open(f"../DIENTES/periodontograma-{i}.png"))
            width += self.dientes1[-1].width

        # segundo sector
        self.dientes2 = []
        for i in range(pos3, pos4, d2):
            self.dientes2.append(Image.open(f"../DIENTES/periodontograma-{i}.png"))
            width += self.dientes2[-1].width

        imagen = Image.new('RGB', (width + 40, 156), 'white')

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
class input0_3(QLineEdit):
    def __init__(self):
        super(input0_3, self).__init__()

        regex = QRegularExpression("[0-3]*")  # Expresión regular que permite solo números
        validator = QRegularExpressionValidator(regex)
        self.setValidator(validator)  # Aplicar la validación al QLineEdit
        self.setMaxLength(1)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(style)


colorBoton = "background-color: #BEBEBE;"


def cambiar_color(boton, color):
    if boton.isChecked():
        boton.setStyleSheet(style + f"background-color: {color}")
    else:
        boton.setStyleSheet(style + colorBoton)


class inputSiNo3(QHBoxLayout):
    def __init__(self, color):
        super(inputSiNo3, self).__init__()

        self.w1 = QPushButton("")
        self.w1.setCheckable(True)
        self.w1.setStyleSheet(style + colorBoton)
        self.w1.clicked.connect(lambda: cambiar_color(self.w1, color))
        self.addWidget(self.w1)

        self.w2 = QPushButton("")
        self.w2.setCheckable(True)
        self.w2.setStyleSheet(style + colorBoton)
        self.w2.clicked.connect(lambda: cambiar_color(self.w2, color))
        self.addWidget(self.w2)

        self.w3 = QPushButton("")
        self.w3.setCheckable(True)
        self.w3.setStyleSheet(style + colorBoton)
        self.w3.clicked.connect(lambda: cambiar_color(self.w3, color))
        self.addWidget(self.w3)


def es_numero(texto):
    if len(texto) == 0:
        return False
    if texto[0] in ('-', '+'):
        return texto[1:].isdigit()
    return texto.isdigit()


class input3(QHBoxLayout):
    def __init__(self, ndiente, tipo, widgetDientes):
        super(input3, self).__init__()

        self.w1 = QLineEdit()
        self.addWidget(self.w1)
        self.w1.setStyleSheet(style)
        self.w1.editingFinished.connect(lambda: self.texto(ndiente, tipo, widgetDientes, self.w1))

        self.w2 = QLineEdit()
        self.addWidget(self.w2)
        self.w2.setStyleSheet(style)
        self.w2.editingFinished.connect(lambda: self.texto(ndiente, tipo, widgetDientes, self.w2))

        self.w3 = QLineEdit()
        self.addWidget(self.w3)
        self.w3.setStyleSheet(style)
        self.w3.editingFinished.connect(lambda: self.texto(ndiente, tipo, widgetDientes, self.w3))

    def texto(self, ndiente, tipo, widgetDientes, inpt):
        if tipo == 1 and es_numero(self.w1.text()):
            if -21 < int(inpt.text()) < 21:
                altura_rojo[int(ndiente)][0] = int(inpt.text())
                widgetDientes.update()
            else:
                inpt.setText("")
        elif tipo == 2 and es_numero(inpt.text()):
            if 0 < int(inpt.text()) < 21:
                altura_azul[int(ndiente)][0] = int(inpt.text())
                widgetDientes.update()
            else:
                inpt.setText("")


class Columna(QVBoxLayout):
    def __init__(self, numDiente, defFurca, widgetDientes):
        super(Columna, self).__init__()

        label = QLabel(str(dientes[int(numDiente)]))
        label.setAlignment(Qt.AlignCenter)
        self.addWidget(label)

        # MOVILIDAD
        movilidad = input0_3()
        self.addWidget(movilidad)

        # IMPLANTE
        boton = QPushButton("")
        boton.setCheckable(True)
        boton.setStyleSheet("background-color: #BEBEBE; margin: 1px; border: 1px solid grey; border-radius: 3px;")
        boton.clicked.connect(lambda: cambiar_color(boton, "#333333"))
        self.addWidget(boton)

        # DEFECTO DE FURCA
        if defFurca == 1:
            defFurca = input0_3()
        else:
            defFurca = QLabel("")
            defFurca.setFixedSize(76, 22)
        self.addWidget(defFurca)

        # SANGRADO AL SONDAJE
        sangrado = inputSiNo3("#FF2B32")
        self.addLayout(sangrado)

        # PLACA
        placa = inputSiNo3("#5860FF")
        self.addLayout(placa)

        # SUPURACION
        supuracion = inputSiNo3("#7CEBA0")
        self.addLayout(supuracion)

        # MARGEN GINGIVAL
        margenGingival = input3(numDiente, 1, widgetDientes)
        self.addLayout(margenGingival)

        # PROFUNDIDAD DE SONDAJE
        profSondaje = input3(numDiente, 2, widgetDientes)
        self.addLayout(profSondaje)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Periostage")
        self.screen = QScreen().geometry()

        self.setMinimumSize(QSize(1000, 500))
        # self.setWindowState(Qt.WindowMaximized)

        self.info1()

    def info1(self):
        tit = QHBoxLayout()
        titu = QLabel("Cara superior")
        tit.addWidget(titu)
        tit.setAlignment(Qt.AlignCenter)

        layoutCuadro1 = QHBoxLayout()

        # Etiquetas
        layoutEtiquetas = QVBoxLayout()
        etiquetas = ["", "Movilidad", "Implante", "Defecto de furca",
                     "Sangrado al sondaje", "Placa", "Supuración", "Margen Gingival", "Profundidad de sondaje"]

        for n in etiquetas:
            label = QLabel(n)
            label.setAlignment(Qt.AlignRight)
            layoutEtiquetas.addWidget(label)

        # Creamos antes la imagen de los dientes para poder pasar el objeto y actualizarlo
        vestibular = ImagenDiente(18, 10, -1, 21, 29, 1)
        widgetDientes = LineasSobreDientes(vestibular)

        # Input de datos
        layoutCuadro1.addLayout(layoutEtiquetas)

        layoutCuadro1.setAlignment(Qt.AlignLeft)

        for n in range(0, 3):
            col = Columna(str(n), 1, widgetDientes)
            layoutCuadro1.addLayout(col)

        for n in range(3, 8):
            col = Columna(str(n), 0, widgetDientes)
            layoutCuadro1.addLayout(col)

        layoutCuadro1.addSpacerItem(QSpacerItem(20, 100))

        for n in range(8, 13):
            col = Columna(str(n), 0, widgetDientes)

            layoutCuadro1.addLayout(col)

        for n in range(13, 16):
            col = Columna(str(n), 1, widgetDientes)
            layoutCuadro1.addLayout(col)

        layoutCuadro1.setContentsMargins(10, 5, 10, 10)
        layoutCuadro1.setSpacing(0)

        # Dientes
        layoutDientes = QHBoxLayout()
        layoutDientes.addWidget(QLabel("Vestibular"))
        layoutDientes.addWidget(widgetDientes)
        layoutDientes.setAlignment(Qt.AlignCenter)

        total = QVBoxLayout()
        total.addLayout(tit)
        total.addLayout(layoutCuadro1)
        total.addLayout(layoutDientes)

        widget = QWidget()
        widget.setLayout(total)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

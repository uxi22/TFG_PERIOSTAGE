import sys
from PIL import Image
from PySide6.QtCore import Qt, QRegularExpression, QRect, QSize, QPoint
from PySide6.QtGui import QScreen, QRegularExpressionValidator, QPixmap, QImage
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget, QHBoxLayout, QSpacerItem, QLineEdit, QPushButton, QPointList
)
from PySide6.QtGui import QPainter, QPen

arriba1 = [[1, 4], [5, 6], [4, 8], [9, 8], [9, 8], [7, 7], [6, 8], [10, 6]]  # del 18 al 11
arriba2 = [[7, 11], [6, 6], [7, 8], [8, 9], [8, 10], [7, 5], [5, 5], [2, 1]]  # del 21 al 28


class Dientes(QWidget):
    def __init__(self, imagen, *a):
        super().__init__(*a)
        self.imagen = imagen # imagen de los dientes con sus atributos

    def paintEvent(self, event):
        qp = QPainter(self)
        imagen = QImage(self.imagen) # imagen de los dientes
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
        qp.setPen(QPen(Qt.red, 2))

        self.points = QPointList()
        dist = 5 # inicio de la imagen del primer diente
        for i, diente in enumerate(self.imagen.dientes1):
            dist += arriba1[i][0]
            self.points.append(QPoint(dist, altura))  # inicio diente
            wdiente = diente.width - arriba1[i][0] - arriba1[i][1]
            self.points.append(QPoint(dist + round(wdiente/2), altura))  # punto medio del diente
            dist += wdiente
            self.points.append(QPoint(dist, altura))  # fin diente, ppio siguiente
            dist += arriba1[i][1]

        dist += 30 # separación entre bloques de dientes

        for i, diente in enumerate(self.imagen.dientes2):
            dist += arriba2[i][0]
            self.points.append(QPoint(dist, altura))
            wdiente = diente.width - arriba2[i][0] - arriba2[i][1]
            self.points.append(QPoint(dist + round(wdiente/2), altura))
            dist += wdiente
            self.points.append(QPoint(dist, altura))
            dist += arriba2[i][1]

        qp.drawPolyline(self.points)

        qp.setPen(QPen(Qt.blue, 3))
        for point in self.points:
            qp.drawPoint(point)

    def minimumSizeHint(self):
        return QSize(1, 1)


class ImagenDiente(QImage):
    def __init__(self, pos1, pos2, d1, pos3, pos4, d2):
        super(ImagenDiente, self).__init__()

        width = 0
        # Añadir imagen del diente
        self.dientes1 = []
        #primer sector
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


class DrawingWidget(QWidget):
    def __init__(self, start_x, start_y, end_x, end_y):
        print("hola ", start_x, start_y, end_x, end_y)
        super().__init__()
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        print("Dibujando ", self.start_x, self.start_y, self.end_x, self.end_y)
        painter.drawLine(self.start_x, self.start_y, self.end_x, self.end_y)


class input0_3(QLineEdit):
    def __init__(self):
        super(input0_3, self).__init__()

        regex = QRegularExpression("[0-3]*")  # Expresión regular que permite solo números
        validator = QRegularExpressionValidator(regex)
        self.setValidator(validator)  # Aplicar la validación al QLineEdit


class inputSiNo3(QHBoxLayout):
    def __init__(self):
        super(inputSiNo3, self).__init__()

        self.w1 = QPushButton("")
        self.addWidget(self.w1)
        self.w2 = QPushButton("")
        self.addWidget(self.w2)
        self.w3 = QPushButton("")
        self.addWidget(self.w3)


class input3(QHBoxLayout):
    def __init__(self, min, max):
        super(input3, self).__init__()

        # expresion que permite los numeros entre min y max
        regex = QRegularExpression(f"[{min}-{max}]*")
        validator = QRegularExpressionValidator(regex)

        self.w1 = QLineEdit()
        self.w1.setValidator(validator)
        self.addWidget(self.w1)

        self.w2 = QLineEdit()
        self.w2.setValidator(validator)
        self.addWidget(self.w2)

        self.w3 = QLineEdit()
        self.w3.setValidator(validator)
        self.addWidget(self.w3)


class Columna(QVBoxLayout):
    def __init__(self, numDiente, defFurca):
        super(Columna, self).__init__()
        self

        label = QLabel(numDiente)
        label.setAlignment(Qt.AlignCenter)
        self.addWidget(label)

        # MOVILIDAD
        movilidad = input0_3()
        self.addWidget(movilidad)

        # añadir boton -> 0 clicks No, 1 click Si, 2 clicks No...
        # IMPLANTE
        boton = QPushButton("")
        self.addWidget(boton)

        # DEFECTO DE FURCA
        if defFurca == 1:
            defFurca = input0_3()
        else:
            defFurca = QLabel("")
            defFurca.setFixedSize(76, 22)
        self.addWidget(defFurca)

        # SANGRADO AL SONDAJE
        sangrado = inputSiNo3()
        self.addLayout(sangrado)

        # PLACA
        placa = inputSiNo3()
        self.addLayout(placa)

        # SUPURACION
        supuracion = inputSiNo3()
        self.addLayout(supuracion)

        # MARGEN GINGIVAL
        margenGingival = input3(-20, 20)
        self.addLayout(margenGingival)

        # PROFUNDIDAD DE SONDAJE
        profSondaje = input3(0, 20)
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

        # Input de datos
        layoutCuadro1.addLayout(layoutEtiquetas)

        layoutCuadro1.setAlignment(Qt.AlignLeft)

        for n in range(18, 15, -1):
            col = Columna(str(n), 1)
            layoutCuadro1.addLayout(col)

        for n in range(15, 10, -1):
            col = Columna(str(n), 0)
            layoutCuadro1.addLayout(col)

        layoutCuadro1.addSpacerItem(QSpacerItem(20, 100))

        for n in range(21, 26):
            col = Columna(str(n), 0)
            layoutCuadro1.addLayout(col)

        for n in range(26, 29):
            col = Columna(str(n), 1)
            layoutCuadro1.addLayout(col)

        layoutCuadro1.setContentsMargins(20, 20, 20, 20)
        layoutCuadro1.setSpacing(0)

        # Dientes
        layoutDientes = QHBoxLayout()
        layoutDientes.addWidget(QLabel("Vestibular"))

        vestibular = ImagenDiente(18, 10, -1, 21, 29, 1)

        widgetDientes = Dientes(vestibular)
        layoutDientes.addWidget(widgetDientes)
        layoutDientes.setAlignment(Qt.AlignCenter)

        total = QVBoxLayout()
        total.addLayout(tit)
        #total.addStretch()
        total.addLayout(layoutCuadro1)
        total.addLayout(layoutDientes)


        widget = QWidget()
        widget.setLayout(total)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

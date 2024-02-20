import sys
from PIL import Image
from PySide6.QtCore import Qt, QRegularExpression, QRect
from PySide6.QtGui import QScreen, QRegularExpressionValidator, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget, QHBoxLayout, QSpacerItem, QLineEdit, QPushButton
)
from PySide6.QtGui import QPainter, QPen


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


class ImagenDiente(QLabel):
    def __init__(self, pos1, pos2, d):
        super(ImagenDiente, self).__init__()

        width = 0
        # Añadir imagen del diente
        self.dientes = []
        for i in range(pos1, pos2, d):
            self.dientes.append(Image.open(f"../DIENTES/periodontograma-{i}.png"))
            width += self.dientes[-1].width
        imagen = Image.new('RGB', (width, 156), 'black')
        position = 0
        for d in self.dientes:
            imagen.paste(d, (position, 0))
            position += d.width

        pixmap = QPixmap.fromImage(imagen.toqimage())
        self.setPixmap(pixmap)



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Periostage")
        self.screen = QScreen().geometry()

        # self.setMinimumSize(QSize(400, 300))
        # self.setMaximumSize(QSize(self.screen.width(), self.screen.height()))
        # self.setFixedSize(QSize(1000, 600))
        # self.resize(QSize(1200, 600))
        self.setWindowState(Qt.WindowMaximized)

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

        sector1 = ImagenDiente(18,10, -1)
        layoutDientes.addWidget(sector1)

        layoutDientes.addSpacerItem(QSpacerItem(20, 100))

        sector2 = ImagenDiente(21, 29, 1)
        layoutDientes.addWidget(sector2)
        layoutDientes.setSpacing(10)
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
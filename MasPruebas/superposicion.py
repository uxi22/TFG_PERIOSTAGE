import sys
from PIL import Image
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

arriba1 = [[1, 4], [5, 6], [4, 8], [9, 8], [9, 8], [7, 7], [6, 8], [10, 6]]  # del 18 al 11
arriba2 = [[7, 11], [6, 6], [7, 8], [8, 9], [8, 10], [7, 5], [5, 5], [2, 1]]  # del 21 al 28


class Dientes(QWidget):
    def __init__(self, imagen, *a):
        super().__init__(*a)
        self.imagen = imagen # imagen de los dientes con sus atributos

    def paintEvent(self, event):
        qp = QPainter(self)
        imagen = QImage(self.imagen) # imagen de los dientes
        """
        imagen_escalada = imagen.scaled(imagen.width() * 1.2, imagen.height() * 1.2, Qt.KeepAspectRatio)
        tam = QRect(0, 0, imagen_escalada.width(), imagen_escalada.height())
        self.setMinimumSize(imagen_escalada.width(), imagen_escalada.height())
        qp.drawImage(tam, imagen_escalada)  # dibujar una línea
        """
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
            self.dientes1.append(Image.open(f"./DIENTES/periodontograma-{i}.png"))
            width += self.dientes1[-1].width

        # segundo sector
        self.dientes2 = []
        for i in range(pos3, pos4, d2):
            self.dientes2.append(Image.open(f"./DIENTES/periodontograma-{i}.png"))
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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Periostage")
        self.screen = QScreen().geometry()
        self.setWindowState(Qt.WindowMaximized)

        self.info1()

    def info1(self):
        tit = QHBoxLayout()
        titu = QLabel("Cara superior")
        tit.addWidget(titu)
        tit.setAlignment(Qt.AlignCenter)

        # Dientes

        layoutDientes = QHBoxLayout()
        layoutDientes.addWidget(QLabel("Vestibular"))

        vestibular = ImagenDiente(18,10, -1, 21, 29, 1)


        widgetDientes = Dientes(vestibular)
        layoutDientes.addWidget(widgetDientes)
        layoutDientes.setAlignment(Qt.AlignCenter)

        total = QVBoxLayout()
        total.addLayout(tit)
        total.addLayout(layoutDientes)

        widget = QWidget()
        widget.setLayout(total)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QCheckBox, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        checkbox = QCheckBox()
        checkbox.setCheckState(Qt.CheckState.Checked)
        #checkbox.setCheckState(Qt.PartiallyChecked) #para que haya tres estados
        #tb se pueden establecer 3 estados con
        checkbox.setTristate(True)

        checkbox.stateChanged.connect(self.show_state)
        self.setCentralWidget(checkbox)

    def show_state(self, state):
        print(state == Qt.CheckState.Checked.value)
        print(state)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
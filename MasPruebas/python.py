import sys
from PySide6.QtWidgets import QApplication, QFileDialog

app = QApplication(sys.argv)

string, filtro = QFileDialog.getSaveFileName(None, "Guardar como", "/", "Python (*.py);;Todos los archivos (*.*)")

if string!= '':
    print("No se ha seleccionado ningún nombre de archivo")
else:
    print("Hola, aqui guardamos el archivo en la ruta: ", string)
    print("Filtro de archivo?: ", filtro)

sys.exit(app.exec())
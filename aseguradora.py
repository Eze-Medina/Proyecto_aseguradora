from PyQt6.QtWidgets import QApplication
from gui.interfaz_general_1 import Interfaz_general_1

class Aseguradora():
    def __init__(self):
        self.app = QApplication([])
        self.Interfaz_general_1 = Interfaz_general_1()
        self.app.exec()
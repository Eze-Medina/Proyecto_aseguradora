from PyQt6 import uic
from gui.busqueda_cliente import Busqueda_cliente
from logica.gestor import GestorSis

class Interfaz_general_1():
    def __init__(self):
        self.interfaz = uic.loadUi("gui/interfaz_general_1.ui")
        self.btnAltaPoliza()
        self.interfaz.show()

    def btnAltaPoliza(self):
        self.interfaz.btnAltaPoliza.clicked.connect(self.IngAltaPoliza)
    
    def IngAltaPoliza(self):
        self.busqueda_cliente = Busqueda_cliente(self)
        self.interfaz.hide()
        
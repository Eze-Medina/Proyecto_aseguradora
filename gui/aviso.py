from PyQt6 import uic, QtWidgets


class Aviso():
    def __init__(self, interfaz, problema):
        self.aviso = uic.loadUi("gui/aviso.ui")
        self.problema = problema
        self.aviso.txtAviso.setText(problema)
        self.interfaz = interfaz
        self.btnAceptar()
        self.mostrar_aviso()

    def mostrar_aviso(self):
        self.aviso.setModal(True)
        self.aviso.show()
        
    def btnAceptar(self):
        self.aviso.btnAceptar.clicked.connect(self.cerrar)
        
    def cerrar(self):
        self.interfaz.interfaz.show()
        self.aviso.close()
        
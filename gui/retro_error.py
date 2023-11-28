from PyQt6 import uic


class retro_error():
    def __init__(self,busqueda_cliente,clienteDTO:ClienteDTO):
        self.retro_error = uic.loadUi("gui/retro_error.ui")
from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDialog
from gui.ingreso_datos_poliza import Ingreso_datos_poliza
from logica.gestor import GestorSis
from model.modelDTO import ClienteDTO


class Busqueda_cliente():
    def __init__(self,interfaz_general_1):
        self.interfaz = uic.loadUi("gui/busqueda_cliente.ui")
        self.interfaz_general_1=interfaz_general_1
        self.btnBuscar()
        self.btnSeleccionar()
        self.btnVolver()
        self.interfaz.show()
        
    
           
    def btnSeleccionar(self):
        self.interfaz.btnSeleccionar.clicked.connect(self.IngDatosPoliza)

    def IngDatosPoliza(self):
        
        fila_seleccionada = self.interfaz.tableDatosClientes.currentRow()
        item = self.interfaz.tableDatosClientes.item(fila_seleccionada, 0)
        dato = int(item.text())
        
        gestor=GestorSis()
        direc=ClienteDTO(idCliente=dato)
        clienteDTO=gestor.buscar_cliente(direc)

        try:
            self.ingreso_datos_poliza = Ingreso_datos_poliza(self,clienteDTO)
            self.interfaz.hide()
        except Exception as e:
            print(f"Error: {e}")
        
    def btnBuscar(self):
        self.interfaz.btnBuscar.clicked.connect(self.listar)
    
    def listar(self):
        try:
            gestor = GestorSis()
            
            filtro = ClienteDTO(idCliente=self.interfaz.txtNumero.text(),
                             numeroDocumento=self.interfaz.txtDocumento.text(),
                             nombre=self.interfaz.txtNombre.text(),
                             apellido=self.interfaz.txtApellido.text())

            lista_clientes = gestor.listar_clientes(filtro)
            
            rowCount = self.interfaz.tableDatosClientes.rowCount()

            for i, cliente in enumerate(lista_clientes):
                self.centrar_elemento(i, 0, str(cliente.idCliente))
                self.centrar_elemento(i, 1, cliente.nombre)
                self.centrar_elemento(i, 2, cliente.apellido)
                self.centrar_elemento(i, 3, cliente.tipoDocumento)
                self.centrar_elemento(i, 4, str(cliente.numeroDocumento))
                rowCount += 1
            
        except Exception as e:
            print(f"Error en prueba(): {e}")
            
            
    def centrar_elemento(self, row, column, text):
        elemento = QTableWidgetItem(text)
        elemento.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.interfaz.tableDatosClientes.setItem(row, column, elemento)
        
    def btnVolver(self):
        self.interfaz.btnVolver.clicked.connect(self.volver)
        
    def volver(self):
        self.interfaz_general_1.interfaz.show()
        self.interfaz.close()
        
from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDialog
from gui.ingreso_datos_poliza import Ingreso_datos_poliza
from gui.aviso import Aviso
from logica.gestor import GestorCliente
from model.modelDTO import ClienteDTO


class Busqueda_cliente():
    def __init__(self,interfaz_general_1):
        self.interfaz = uic.loadUi("gui/busqueda_cliente.ui")
        self.interfaz_general_1=interfaz_general_1
        self.interfaz.btnBuscar.clicked.connect(self.btnBuscar)
        self.lista_clientes = []
        self.grupoRadioButton()
        self.btnSeleccionar()
        self.initComboBox_Documentos()
        self.innit_table()
        self.btnVolver()
        self.verificar()
        self.btnSigPagina()
        self.btnAntPagina()
        self.interfaz.show()
        self.interfaz.rb10.setChecked(True)
        self.interfaz.rb10.clicked.connect(self.innit_table)
        self.interfaz.rb20.clicked.connect(self.innit_table)
        self.interfaz.rb30.clicked.connect(self.innit_table)
        
    def initComboBox_Documentos(self):
        try:
            gestor = GestorCliente()
            lista_documentos = gestor.listar_documentos()
            
            for documentos in lista_documentos:
                self.interfaz.cbTipoDocumento.addItem(documentos.tipoDocumento)
            
        except Exception as e:
            print(f"Error listar tipos de documentos: {e}")    
           
    def btnSeleccionar(self):
        self.interfaz.btnSeleccionar.clicked.connect(self.IngDatosPoliza)

    def grupoRadioButton(self):
        try:
            # Grupo 1
            self.interfaz.buttonGroup_1 = QtWidgets.QButtonGroup()
            self.interfaz.buttonGroup_1.addButton(self.interfaz.rb10)
            self.interfaz.buttonGroup_1.addButton(self.interfaz.rb20)
            self.interfaz.buttonGroup_1.addButton(self.interfaz.rb30)
           
        except Exception as e:
            print(f"Error al generar grupo de rb: {e}") 
            
    def verificar(self):
        try:
            if (self.interfaz.txtNumero.text()== "" and 
                self.interfaz.txtNombre.text()== "" and 
                self.interfaz.txtApellido.text()== "" and 
                self.interfaz.cbTipoDocumento.currentIndex()== 0 and
                self.interfaz.txtDocumento.text()== ""
                ):
                return True
                
        except Exception as e:
                print(f"Error en verificacion: {e}")
                
    def IngDatosPoliza(self):
        
        fila_seleccionada = self.interfaz.tableDatosClientes.currentRow()
        item = self.interfaz.tableDatosClientes.item(fila_seleccionada, 0)
        
        try:
            if item == None:
                self.aviso=Aviso(self,'Seleccione un cliente')
          
            else:
                dato = int(item.text())
                
                gestor=GestorCliente()
                direc=ClienteDTO(idCliente=dato)
                clienteDTO=gestor.buscar_cliente(direc)

                self.ingreso_datos_poliza = Ingreso_datos_poliza(self,clienteDTO)
                self.interfaz.hide()
                
        except Exception as e:
            print(f"Error: {e}")
        
    def btnBuscar(self):
        try:
            if not self.verificar():
                self.interfaz.btnBuscar.clicked.connect(self.obtener_clientes)
            else:
                try:
                    self.aviso=Aviso(self,'Completar los datos por favor')
                except Exception as e:
                    print(f"Error: {e}")   
                    self.aviso=Aviso(self,f'Error: {e}')
        except Exception as e:
            print(f"Error en buscar: {e}")
    
    def btnSigPagina(self):
        self.interfaz.btnSigPagina.clicked.connect(self.pasarPagina)
    
    def pasarPagina(self):
        try:
            boton_seleccionado = self.interfaz.buttonGroup_1.checkedButton()
            texto_boton = boton_seleccionado.text()
            ultimos_dos_digitos_str = texto_boton[-2:]
            cant_vista = int(ultimos_dos_digitos_str)
            
            num_clientes_por_pagina = self.interfaz.tableDatosClientes.rowCount()
            
            if len(self.lista_clientes) < cant_vista:
                pass
            else:
                numero_pag = self.interfaz.txtNumPag.text()
                numeros = [int(s) for s in numero_pag.split() if s.isdigit()]
            
                pag_siguiente = numeros[0] + 1
                self.interfaz.txtNumPag.setText(f"{pag_siguiente}  de  {numeros[1]}")
                self.listar_pag(self.lista_clientes)
            
        except Exception as e:
            print(f"Error en pasar pagina: {e}")
    
    
    def btnAntPagina(self):
        self.interfaz.btnAntPagina.clicked.connect(self.volverPagina)
    
    def volverPagina(self):
        try:
            boton_seleccionado = self.interfaz.buttonGroup_1.checkedButton()
            texto_boton = boton_seleccionado.text()
            ultimos_dos_digitos_str = texto_boton[-2:]
            cant_vista = int(ultimos_dos_digitos_str)
            
            num_clientes_por_pagina = self.interfaz.tableDatosClientes.rowCount()
            
            if len(self.lista_clientes) < cant_vista:
                pass
            else:
                numero_pag = self.interfaz.txtNumPag.text()
                numeros = [int(s) for s in numero_pag.split() if s.isdigit()]
            
                pag_siguiente = numeros[0] - 1
                self.interfaz.txtNumPag.setText(f"{pag_siguiente}  de  {numeros[1]}")
                self.listar_pag(self.lista_clientes)
            
        except Exception as e:
            print(f"Error en pasar pagina: {e}")
            
             
    def innit_table(self):
        
        try:
            # rowCount = self.interfaz.tableDatosClientes.rowCount()
            # for i in range(rowCount - 1, -1, -1):
            #     self.interfaz.tableDatosClientes.removeRow(i)
            
            if self.interfaz.rb10.isChecked():
                self.interfaz.tableDatosClientes.setRowCount(10)
                self.mostrar_pag(self.lista_clientes)

            if self.interfaz.rb20.isChecked():
                self.interfaz.tableDatosClientes.setRowCount(20)
                self.mostrar_pag(self.lista_clientes)
                
            if self.interfaz.rb30.isChecked():
                self.interfaz.tableDatosClientes.setRowCount(30)
                self.mostrar_pag(self.lista_clientes)
        except Exception as e:
            print(f"Error en innit table: {e}")

    def obtener_clientes(self):
        try:
            gestor = GestorCliente()
            
            filtro = ClienteDTO(idCliente=self.interfaz.txtNumero.text(),
                             numeroDocumento=self.interfaz.txtDocumento.text(),
                             nombre=self.interfaz.txtNombre.text(),
                             apellido=self.interfaz.txtApellido.text(),
                             tipoDocumento=self.interfaz.cbTipoDocumento.currentText())    
            print(filtro)        
            lista_clientes = gestor.listar_clientes(filtro)
            self.lista_clientes = lista_clientes
            self.mostrar_pag(lista_clientes)
            
        except Exception as e:
            print(f"Error en listar() dentro de busqueda_cliente: {e}")            
    
    def mostrar_pag(self, lista_clientes):
        try:
            num_clientes_por_pagina = self.interfaz.tableDatosClientes.rowCount()
            cantidad_paginas = len(lista_clientes) // num_clientes_por_pagina

            if len(lista_clientes) % num_clientes_por_pagina != 0:
                cantidad_paginas += 1

            self.interfaz.txtNumPag.setText(f"1  de  {cantidad_paginas}")
            self.listar_pag(lista_clientes)
            
        except Exception as e:
            print(f"Error en mostrar_pag(): {e}")
       
    def listar_pag(self, lista_clientes):
        
        numero_pag = self.interfaz.txtNumPag.text()
        numeros = [int(s) for s in numero_pag.split() if s.isdigit()]
            
        rowCount = self.interfaz.tableDatosClientes.rowCount()
            
        inicio = (numeros[0] * rowCount) - rowCount 
        fin = numeros[0] * rowCount
            
        try:
            self.interfaz.tableDatosClientes.clearContents()
            

            lista_clientes_rango = lista_clientes[inicio:fin]

            for i, cliente in enumerate(lista_clientes_rango):
                self.centrar_elemento(i, 0, str(cliente.idCliente))
                self.centrar_elemento(i, 1, cliente.nombre)
                self.centrar_elemento(i, 2, cliente.apellido)
                self.centrar_elemento(i, 3, cliente.tipoDocumento)
                self.centrar_elemento(i, 4, str(cliente.numeroDocumento))
                rowCount += 1

        except Exception as e:
            print(f"Error en listar_pag(): {e}")          
            
    def centrar_elemento(self, row, column, text):
        elemento = QTableWidgetItem(text)
        elemento.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.interfaz.tableDatosClientes.setItem(row, column, elemento)
        
    def btnVolver(self):
        self.interfaz.btnVolver.clicked.connect(self.volver)
        
    def volver(self):
        self.interfaz_general_1.interfaz.show()
        self.interfaz.close()
        
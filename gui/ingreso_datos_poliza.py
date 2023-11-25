from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox, QComboBox, QCheckBox, QVBoxLayout
from gui.seleccion_tipo_poliza import Seleccion_tipo_poliza
from logica.gestor import GestorSis
from model.modelDTO import ClienteDTO, ProvinciaDTO, MarcaDTO, LocalidadDTO, hijoDTO, polizaDTO
from datetime import datetime

class Ingreso_datos_poliza():
    def __init__(self,busqueda_cliente,clienteDTO:ClienteDTO):
        self.ingreso_datos_poliza = uic.loadUi("gui/ingreso_datos_poliza.ui")
        self.busqueda_cliente=busqueda_cliente
        self.datosCliente=clienteDTO
        self.ingreso_datos_poliza.txtNombre.setText(f"{clienteDTO.nombre}")
        self.ingreso_datos_poliza.txtApellido.setText(f"{clienteDTO.apellido}")
        self.ingreso_datos_poliza.txtNumeroCliente.setText(f"{clienteDTO.idCliente}")
        self.ingreso_datos_poliza.txtDomicilio.setText(f"{clienteDTO.nombreVivienda} {clienteDTO.numeroVivienda}")
        self.ingreso_datos_poliza.txtTipoDocumento.setText(f"{clienteDTO.tipoDocumento}")
        self.ingreso_datos_poliza.txtNumeroDocumento.setText(f"{clienteDTO.numeroDocumento}")
        self.datosPoliza=polizaDTO()
        
        self.initComboBox_Provicias()
        self.comboBoxProvincias_changed()
        self.initComboBox_Marcas()
        self.comboBoxMarca_changed()
        self.comboBoxModelo_changed()
        self.initcomboBox_NroSiniestro()
        self.initcomboBox_Hijos()
        self.recuperarDatosPoliza()
        
        self.btnLimpiar()
        self.btnAgregar()
        self.btnConfirmar()
        self.btnVolver()
        self.ingreso_datos_poliza.show()
    
    def initcomboBox_Hijos(self):
        gestor = GestorSis()
        
        sexo=["Femenino","Masculino"] #esta de mas esto?
        for i in sexo:
            self.ingreso_datos_poliza.cbSexo.addItem(i)
        
        lista_estadoCivil = gestor.listar_estadoCivil()  
          
        for estado in lista_estadoCivil:
            self.ingreso_datos_poliza.cbEstadoCivil.addItem(estado.estado)
            
    def initcomboBox_NroSiniestro(self):
        gestor = GestorSis()
        lista_siniestros = gestor.listar_siniestros()  
          
        for siniestros in lista_siniestros:
            self.ingreso_datos_poliza.cbNumeroSiniestros.addItem(siniestros.cantidad)
            
    def initComboBox_Provicias(self):
        try:
            gestor = GestorSis()
            filtro = ProvinciaDTO()
            lista_provicias = gestor.listar_provincias(filtro)

            for provincia in lista_provicias:
                self.ingreso_datos_poliza.cbProvincia.addItem(provincia.nombre)
            
        except Exception as e:
            print(f"Error en pruebaComboBox(): {e}")
    
    def comboBoxProvincias_changed(self):
        try:
            self.ingreso_datos_poliza.cbProvincia.activated.connect(self.initComboBox_Localidades)
        except Exception as e:
            print(f"Error en prueba(): {e}")

    def initComboBox_Localidades(self, index):
        provinciaSeleccionada = self.ingreso_datos_poliza.cbProvincia.itemText(index)
        
        self.ingreso_datos_poliza.cbLocalidad.clear()
        self.ingreso_datos_poliza.cbLocalidad.addItem("--- Seleccione una opción")
        try:
            gestor = GestorSis()
            lista_localidades = gestor.listar_localidades(provinciaSeleccionada)

            for localidad in lista_localidades:
                self.ingreso_datos_poliza.cbLocalidad.addItem(localidad.nombre)
            
        except Exception as e:
            print(f"Error en pruebaComboBox(): {e}")
  
    def initComboBox_Marcas(self):
        try:
            gestor = GestorSis()
            filtro = MarcaDTO()
            lista_marcas = gestor.listar_marcas(filtro)

            for marca in lista_marcas:
                self.ingreso_datos_poliza.cbMarcaVehiculo.addItem(marca.nombre)
            
        except Exception as e:
            print(f"Error en pruebaComboBox(): {e}")
        
    def comboBoxMarca_changed(self):
        try:
            self.ingreso_datos_poliza.cbMarcaVehiculo.activated.connect(self.initComboBox_modelo)
        except Exception as e:
            print(f"Error en prueba(): {e}") 
    
    def initComboBox_modelo(self, index):
        marcaSeleccionada = self.ingreso_datos_poliza.cbMarcaVehiculo.itemText(index)
        
        self.ingreso_datos_poliza.cbModeloVehiculo.clear()
        self.ingreso_datos_poliza.cbModeloVehiculo.addItem("--- Seleccione una opción")
        
        try:
            gestor = GestorSis()
            lista_modelos = gestor.listar_modelos(marcaSeleccionada)

            for modelos in lista_modelos:
                self.ingreso_datos_poliza.cbModeloVehiculo.addItem(modelos.nombre)
            
        except Exception as e:
            print(f"Error en initComboBox_modelo(): {e}")
            
    def comboBoxModelo_changed(self):
        try:
            self.ingreso_datos_poliza.cbModeloVehiculo.activated.connect(self.initcomboBox_Anio)
        except Exception as e:
            print(f"Error en comboBoxModelo_changed(): {e}") 
            
    def initcomboBox_Anio(self,index):
        gestor=GestorSis()
        modeloSeleccionado = self.ingreso_datos_poliza.cbModeloVehiculo.itemText(index)
        
        self.ingreso_datos_poliza.cbAnioVehiculo.clear()
        self.ingreso_datos_poliza.cbAnioVehiculo.addItem("--- Seleccione una opción")
        
        try:
            lista=gestor.listar_anios(modeloSeleccionado)
            for anios in lista:
                self.ingreso_datos_poliza.cbAnioVehiculo.addItem(f"{anios}")
        except Exception as e:
            print(f"Error en initcomboBox_Anno(): {e}")
            
    def btnAgregar(self):
        self.ingreso_datos_poliza.btnAgregar.clicked.connect(self.agregarHijo)
        
    def agregarHijo(self):
        sexoSeleccionado = self.ingreso_datos_poliza.cbSexo.currentText()
        estadoCivilSeleccionado = self.ingreso_datos_poliza.cbEstadoCivil.currentText()
        
        nuevo_hijo=hijoDTO(sexo=sexoSeleccionado,estadoCivil=estadoCivilSeleccionado)
        self.datosPoliza.hijos.append(nuevo_hijo)
        
        cant=int(self.ingreso_datos_poliza.txtCantidadHijos.text())
        self.ingreso_datos_poliza.txtCantidadHijos.setText(f"{cant+1}")  
    
    def btnLimpiar(self):
        self.ingreso_datos_poliza.btnLimpiar.clicked.connect(self.vaciarLista)
        
    def recuperarDatosPoliza(self):
        try:
            self.datosPoliza.provincia=self.ingreso_datos_poliza.cbProvincia.currentText()
            self.datosPoliza.localidad=self.ingreso_datos_poliza.cbLocalidad.currentText()
            self.datosPoliza.marcaVehiculo=self.ingreso_datos_poliza.cbMarcaVehiculo.currentText()
            self.datosPoliza.modeloVehiculo=self.ingreso_datos_poliza.cbModeloVehiculo.currentText()
            self.datosPoliza.anioVehiculo=int(self.ingreso_datos_poliza.cbAnioVehiculo.currentText())
            self.datosPoliza.sumaAsegurada=int(self.ingreso_datos_poliza.txtSumaAsegurada.text())
            self.datosPoliza.motor=self.ingreso_datos_poliza.txtMotor.text()
            self.datosPoliza.chasis=self.ingreso_datos_poliza.txtChasis.text()
            self.datosPoliza.patente=self.ingreso_datos_poliza.txtPatente.text()
            self.datosPoliza.kilometrosAnio=int(self.ingreso_datos_poliza.txtKilometrosAnio.text())
            self.datosPoliza.cantSiniestros=self.ingreso_datos_poliza.cbNumeroSiniestros.currentText()
            
            if self.ingreso_datos_poliza.chbGaraje.isChecked():
                self.datosPoliza.medidas.append(1)
            else:
                pass
            if (self.ingreso_datos_poliza.chbAlarma.isChecked()):
                self.datosPoliza.medidas.append(2)
            else:
                pass
            if self.ingreso_datos_poliza.chbRastreo.isChecked():
                self.datosPoliza.medidas.append(3)
            else:
                pass
            if self.ingreso_datos_poliza.chbTuerca.isChecked():
                self.datosPoliza.medidas.append(4)
            else:
                pass
            
        except Exception as e:
            print(f"Error en recuperacion: {e}")

    def vaciarLista(self):
        self.datosPoliza.hijos.clear()
        self.ingreso_datos_poliza.txtCantidadHijos.setText("0") 

    def IngSeleccionTipo(self):
        try:
            self.seleccion_tipo_poliza = Seleccion_tipo_poliza(self,self.datosCliente,self.datosPoliza)
            self.ingreso_datos_poliza.hide()
        except Exception as e:
            print(f"Error: {e}")

    def btnConfirmar(self):
        self.ingreso_datos_poliza.btnConfirmar.clicked.connect(self.recuperarDatosPoliza)
        self.ingreso_datos_poliza.btnConfirmar.clicked.connect(self.IngSeleccionTipo)

    def btnVolver(self):
         self.ingreso_datos_poliza.btnVolver.clicked.connect(self.volver)
        
    def volver(self):
         self.busqueda_cliente.busqueda_cliente.show()
         self.ingreso_datos_poliza.close()
         
    def finalizar(self):
        self.busqueda_cliente.volver()
        self.ingreso_datos_poliza.close() 
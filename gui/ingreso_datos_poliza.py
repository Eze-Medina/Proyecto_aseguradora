from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox, QComboBox, QCheckBox, QVBoxLayout
from gui.seleccion_tipo_poliza import Seleccion_tipo_poliza
from gui.aviso import Aviso
from logica.gestor import GestorDatos,GestorVehiculo,GestorUbicacion,GestorAseguradora
from model.modelDTO import ClienteDTO, ProvinciaDTO, MarcaDTO, LocalidadDTO, hijoDTO, polizaDTO
from datetime import datetime

class Ingreso_datos_poliza():
    def __init__(self,busqueda_cliente,clienteDTO:ClienteDTO):
        self.interfaz = uic.loadUi("gui/ingreso_datos_poliza.ui")
        self.busqueda_cliente=busqueda_cliente
        self.datosCliente=clienteDTO
        self.interfaz.txtNombre.setText(f"{clienteDTO.nombre}")
        self.interfaz.txtApellido.setText(f"{clienteDTO.apellido}")
        self.interfaz.txtNumeroCliente.setText(f"{clienteDTO.idCliente}")
        self.interfaz.txtDomicilio.setText(f"{clienteDTO.nombreVivienda} {clienteDTO.numeroVivienda}")
        self.interfaz.txtTipoDocumento.setText(f"{clienteDTO.tipoDocumento}")
        self.interfaz.txtNumeroDocumento.setText(f"{clienteDTO.numeroDocumento}")
        self.datosPoliza=polizaDTO()
        
        self.initComboBox_Provicias()
        self.comboBoxProvincias_changed()
        self.initComboBox_Marcas()
        self.comboBoxMarca_changed()
        self.comboBoxModelo_changed()
        self.comboBoxAnioVehiculo_changed()
        self.initSumaAsegurada()
        self.initcomboBox_NroSiniestro()
        self.initcomboBox_Hijos()
        
        
        self.btnLimpiar()
        self.btnAgregar()
        self.btnConfirmar()
        self.btnVolver()
        self.interfaz.show()
    
    def initcomboBox_Hijos(self):
        gestor = GestorDatos()
        
        sexo=["Femenino","Masculino"] #esta de mas esto?
        for i in sexo:
            self.interfaz.cbSexo.addItem(i)
        
        lista_estadoCivil = gestor.listar_estadoCivil()  
          
        for estado in lista_estadoCivil:
            self.interfaz.cbEstadoCivil.addItem(estado.estado)
            
    def initcomboBox_NroSiniestro(self):
        gestor = GestorVehiculo()
        lista_siniestros = gestor.listar_siniestros()  
          
        for siniestros in lista_siniestros:
            self.interfaz.cbNumeroSiniestros.addItem(siniestros.cantidad)
            
    def initComboBox_Provicias(self):
        try:
            gestor = GestorUbicacion()
            filtro = ProvinciaDTO()
            lista_provincias = gestor.listar_provincias(filtro)

            lista_provincias_ordenada = sorted(lista_provincias, key=lambda x: x.nombre)
            
            for provincia in lista_provincias_ordenada:
                self.interfaz.cbProvincia.addItem(provincia.nombre)
            
        except Exception as e:
            print(f"Error en pruebaComboBox(): {e}")
    
    def comboBoxProvincias_changed(self):
        try:
            self.interfaz.cbProvincia.activated.connect(self.initComboBox_Localidades)
        except Exception as e:
            print(f"Error en prueba(): {e}")

    def initComboBox_Localidades(self, index):
        provinciaSeleccionada = self.interfaz.cbProvincia.itemText(index)
        
        self.interfaz.cbLocalidad.clear()
        self.interfaz.cbLocalidad.addItem("--- Seleccione una opción")
        try:
            gestor = GestorUbicacion()
            lista_localidades = gestor.listar_localidades(provinciaSeleccionada)

            lista_localidades_ordenada = sorted(lista_localidades, key=lambda x: x.nombre)
            
            for localidad in lista_localidades_ordenada:
                self.interfaz.cbLocalidad.addItem(localidad.nombre)
            
        except Exception as e:
            print(f"Error en pruebaComboBox(): {e}")
  
    def initComboBox_Marcas(self):
        try:
            gestor = GestorVehiculo()
            filtro = MarcaDTO()
            lista_marcas = gestor.listar_marcas(filtro)
            
            lista_marcas_ordenada = sorted(lista_marcas, key=lambda x: x.nombre)
            
            for marca in lista_marcas_ordenada:
                self.interfaz.cbMarcaVehiculo.addItem(marca.nombre)
            
        except Exception as e:
            print(f"Error en pruebaComboBox(): {e}")
        
    def comboBoxMarca_changed(self):
        try:
            self.interfaz.cbMarcaVehiculo.activated.connect(self.initComboBox_modelo)
        except Exception as e:
            print(f"Error en prueba(): {e}") 
    
    def initComboBox_modelo(self, index):
        marcaSeleccionada = self.interfaz.cbMarcaVehiculo.itemText(index)
        
        self.interfaz.cbModeloVehiculo.clear()
        self.interfaz.cbModeloVehiculo.addItem("--- Seleccione una opción")
        
        try:
            gestor = GestorVehiculo()
            lista_modelos = gestor.listar_modelos(marcaSeleccionada)
            
            lista_modelo_ordenada = sorted(lista_modelos, key=lambda x: x.nombre)
            
            for modelos in lista_modelo_ordenada:
                self.interfaz.cbModeloVehiculo.addItem(modelos.nombre)
            
        except Exception as e:
            print(f"Error en initComboBox_modelo(): {e}")
            
    def comboBoxModelo_changed(self):
        try:
            self.interfaz.cbModeloVehiculo.activated.connect(self.initcomboBox_Anio)
        except Exception as e:
            print(f"Error en comboBoxModelo_changed(): {e}") 
            
    def initcomboBox_Anio(self,index):
        gestor=GestorVehiculo()
        modeloSeleccionado = self.interfaz.cbModeloVehiculo.itemText(index)
        
        self.interfaz.cbAnioVehiculo.clear()
        self.interfaz.cbAnioVehiculo.addItem("--- Seleccione una opción")
        
        try:
            lista=gestor.listar_anios(modeloSeleccionado)
            for anios in lista:
                self.interfaz.cbAnioVehiculo.addItem(f"{anios}")
        except Exception as e:
            print(f"Error en initcomboBox_Anno(): {e}")
    
    def comboBoxAnioVehiculo_changed(self):
        try:
            self.interfaz.cbAnioVehiculo.activated.connect(self.initSumaAsegurada)
        except Exception as e:
            print(f"Error en prueba(): {e}") 
    
    def initSumaAsegurada(self):
        
        anioSeleccionado = self.interfaz.cbModeloVehiculo.currentText()
        if (anioSeleccionado != "--- Seleccione una opción"):
            try:
                gestor = GestorAseguradora()
                suma = gestor.recuperar_SumaAsegurada()
                self.interfaz.txtSumaAsegurada.setText(f"{suma}")
                
            except Exception as e:
                print(f"Error en initSumaAsegurada(): {e}")
        else:
            pass
        
    def btnAgregar(self):
        self.interfaz.btnAgregar.clicked.connect(self.agregarHijo)
        
    def agregarHijo(self):
        sexoSeleccionado = self.interfaz.cbSexo.currentText()
        estadoCivilSeleccionado = self.interfaz.cbEstadoCivil.currentText()
        
        nuevo_hijo=hijoDTO(sexo=sexoSeleccionado,estadoCivil=estadoCivilSeleccionado)
        self.datosPoliza.hijos.append(nuevo_hijo)
        
        cant=int(self.interfaz.txtCantidadHijos.text())
        self.interfaz.txtCantidadHijos.setText(f"{cant+1}")  
    
    def btnLimpiar(self):
        self.interfaz.btnLimpiar.clicked.connect(self.vaciarLista)
    
    def verificar(self):
        try:
            if (self.interfaz.cbProvincia.currentIndex()!= 0 and
                self.interfaz.cbLocalidad.currentIndex()!= 0 and
                self.interfaz.cbMarcaVehiculo.currentIndex()!= 0 and
                self.interfaz.cbModeloVehiculo.currentIndex()!= 0 and
                self.interfaz.cbAnioVehiculo.currentIndex()!= 0 and
                self.interfaz.txtMotor.text() != "" and 
                self.interfaz.txtChasis.text() != "" and 
                self.interfaz.txtKilometrosAnio.text() != "" and
                self.interfaz.cbNumeroSiniestros.currentIndex()!= 0
                ):
                    print("FUNCO LA VERIFICACION")
                    return True
        except Exception as e:
            print(f"Error en verificacion: {e}")
        
    def recuperarDatosPoliza(self):

        try:
            self.datosPoliza.provincia=self.interfaz.cbProvincia.currentText()
            self.datosPoliza.localidad=self.interfaz.cbLocalidad.currentText()
            self.datosPoliza.marcaVehiculo=self.interfaz.cbMarcaVehiculo.currentText()
            self.datosPoliza.modeloVehiculo=self.interfaz.cbModeloVehiculo.currentText()
            self.datosPoliza.anioVehiculo=int(self.interfaz.cbAnioVehiculo.currentText())
            self.datosPoliza.sumaAsegurada=int(self.interfaz.txtSumaAsegurada.text())
            self.datosPoliza.motor=self.interfaz.txtMotor.text()
            self.datosPoliza.chasis=self.interfaz.txtChasis.text()
            self.datosPoliza.patente=self.interfaz.txtPatente.text()
            self.datosPoliza.kilometrosAnio=int(self.interfaz.txtKilometrosAnio.text())
            self.datosPoliza.cantSiniestros=self.interfaz.cbNumeroSiniestros.currentText()
            
        except Exception as e:
            print(f"Error en recuperacion1: {e}")
        try:    
            self.datosPoliza.medidas.clear()
            
            if self.interfaz.chbGaraje.isChecked():
                self.datosPoliza.medidas.append(1)
            else:
                pass
            if (self.interfaz.chbAlarma.isChecked()):
                self.datosPoliza.medidas.append(2)
            else:
                pass
            if self.interfaz.chbRastreo.isChecked():
                self.datosPoliza.medidas.append(3)
            else:
                pass
            if self.interfaz.chbTuerca.isChecked():
                self.datosPoliza.medidas.append(4)
            else:
                pass
            
        except Exception as e:
            print(f"Error en recuperacion2: {e}")    
        
    def vaciarLista(self):
        self.datosPoliza.hijos.clear()
        self.interfaz.txtCantidadHijos.setText("0") 

    def IngSeleccionTipo(self):
        try:
            if self.verificar():
                self.recuperarDatosPoliza()
                self.seleccion_tipo_poliza = Seleccion_tipo_poliza(self,self.datosCliente,self.datosPoliza)
                self.interfaz.hide()
            else:
                try:
                    self.aviso=Aviso(self,'Completar los datos por favor')
                except Exception as e:
                    print(f"Error: {e}")   
                    self.aviso=Aviso(self,f'Error: {e}')
        except Exception as e:
            print(f"Error: {e}")

    def btnConfirmar(self):
            self.interfaz.btnConfirmar.clicked.connect(self.IngSeleccionTipo)

    def btnVolver(self):
         self.interfaz.btnVolver.clicked.connect(self.volver)
        
    def volver(self):
         self.busqueda_cliente.interfaz.show()
         self.interfaz.close()
         
    
    
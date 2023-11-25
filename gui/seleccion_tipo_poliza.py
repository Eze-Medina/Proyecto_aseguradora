from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox, QComboBox, QCheckBox, QVBoxLayout
from gui.confirmacion_poliza_1 import Confirmacion_poliza_1
from gui.confirmacion_poliza_6 import Confirmacion_poliza_6
from model.modelDTO import ClienteDTO, polizaDTO
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Seleccion_tipo_poliza():
    def __init__(self,ingreso_datos_poliza,clienteDTO,polizaDTO):
        self.seleccion_tipo_poliza = uic.loadUi("gui/seleccion_tipo_poliza.ui")
        self.ingreso_datos_poliza=ingreso_datos_poliza
        self.datosCliente=clienteDTO
        self.datosPoliza=polizaDTO
        self.seleccion_tipo_poliza.txtNombre.setText(f"{clienteDTO.nombre}")
        self.seleccion_tipo_poliza.txtApellido.setText(f"{clienteDTO.apellido}")
        self.seleccion_tipo_poliza.txtNumeroCliente.setText(f"{clienteDTO.idCliente}")
        self.seleccion_tipo_poliza.txtDomicilio.setText(f"{clienteDTO.nombreVivienda}{clienteDTO.numeroVivienda}")
        self.seleccion_tipo_poliza.txtTipoDocumento.setText(f"{clienteDTO.tipoDocumento}")
        self.seleccion_tipo_poliza.txtNumeroDocumento.setText(f"{clienteDTO.numeroDocumento}")
        
        #print(polizaDTO)
        self.sumar_seis_meses_str() 
        self.btnConfirmar()
        self.btnVolver()
        self.seleccion_tipo_poliza.show()
      
    def recuperarDatosPoliza(self):
        try:
            if self.seleccion_tipo_poliza.rbRespCivil.isChecked():
                self.datosPoliza.tipoCobertura = 1
            else:
                pass
            if self.seleccion_tipo_poliza.rbIncendioTotel.isChecked():
                self.datosPoliza.tipoCobertura = 2
            else:
                pass
            if self.seleccion_tipo_poliza.rbTodoTotal.isChecked():
                self.datosPoliza.tipoCobertura = 3
            else:
                pass
            if self.seleccion_tipo_poliza.rbTercerosCompletos.isChecked():
                self.datosPoliza.tipoCobertura = 4
            else:
                pass
            if self.seleccion_tipo_poliza.rbTodoRiesgo.isChecked():
                self.datosPoliza.tipoCobertura = 5
            else:
                pass
            
            self.datosPoliza.fechaInicioVigencia = self.seleccion_tipo_poliza.txtFechaInicioVigencia.text()
            self.datosPoliza.fechaFinVigencia = self.sumar_seis_meses_str()
            self.datosPoliza.formaPago = self.seleccion_tipo_poliza.cbFormaPago.currentText()
            
        except Exception as e:
            print(f"Error en recuperacion: {e}")
      
    def IngConfirmacion_poliza(self):
        try:
            fp=self.seleccion_tipo_poliza.cbFormaPago.currentText()
            if  fp == "Semestral":
                self.confirmacion_poliza_1 = Confirmacion_poliza_1(self,self.datosCliente,self.datosPoliza)
                self.seleccion_tipo_poliza.hide()
            else:
                self.confirmacion_poliza_6 = Confirmacion_poliza_6(self,self.datosCliente,self.datosPoliza)
                self.seleccion_tipo_poliza.hide()  
            
        except Exception as e:
            print(f"Error en muestra: {e}")    

    def btnConfirmar(self):
        self.seleccion_tipo_poliza.btnConfirmar.clicked.connect(self.recuperarDatosPoliza)
        self.seleccion_tipo_poliza.btnConfirmar.clicked.connect(self.IngConfirmacion_poliza)
    
    def btnVolver(self):
         self.seleccion_tipo_poliza.btnVolver.clicked.connect(self.volver)
        
    def volver(self):
         self.ingreso_datos_poliza.ingreso_datos_poliza.show()
         self.seleccion_tipo_poliza.close()
         
    def sumar_seis_meses_str(self):
        try:
            fechaFin = self.datosPoliza.fechaInicioVigencia
            datetime_object = datetime.strptime(fechaFin, '%d/%m/%Y').date()
            fecha_resultado = datetime_object + relativedelta(months=6)
            return fecha_resultado
        
        except Exception as e:
            print(f"Error en fecha2: {e}")
            
    def finalizar(self):
        self.ingreso_datos_poliza.finalizar()
        self.seleccion_tipo_poliza.close()
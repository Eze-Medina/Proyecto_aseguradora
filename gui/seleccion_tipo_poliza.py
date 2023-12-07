from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox, QComboBox, QCheckBox, QVBoxLayout
from gui.confirmacion_poliza_1 import Confirmacion_poliza_1
from gui.confirmacion_poliza_6 import Confirmacion_poliza_6
from gui.aviso import Aviso
from model.modelDTO import ClienteDTO, polizaDTO
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Seleccion_tipo_poliza():
    def __init__(self,ingreso_datos_poliza,clienteDTO,polizaDTO):
        self.interfaz = uic.loadUi("gui/seleccion_tipo_poliza.ui")
        self.ingreso_datos_poliza=ingreso_datos_poliza
        self.datosCliente=clienteDTO
        self.datosPoliza=polizaDTO
        self.interfaz.txtNombre.setText(f"{clienteDTO.nombre}")
        self.interfaz.txtApellido.setText(f"{clienteDTO.apellido}")
        self.interfaz.txtNumeroCliente.setText(f"{clienteDTO.idCliente}")
        self.interfaz.txtDomicilio.setText(f"{clienteDTO.nombreVivienda}{clienteDTO.numeroVivienda}")
        self.interfaz.txtTipoDocumento.setText(f"{clienteDTO.tipoDocumento}")
        self.interfaz.txtNumeroDocumento.setText(f"{clienteDTO.numeroDocumento}")
        
        #print(polizaDTO)
        self.sumar_seis_meses_str() 
        self.innit_fechaInicio()
        self.btnConfirmar()
        self.btnVolver()
        self.interfaz.show()
    
    def verificar(self):
        try:
            if ((self.interfaz.cbFormaPago.currentIndex()!= 0 and
                 self.interfaz.txtFechaInicioVigencia.text() != "") and (
                 self.interfaz.rbRespCivil.isChecked() or
                 self.interfaz.rbIncendioTotel.isChecked() or
                 self.interfaz.rbTodoTotal.isChecked() or
                 self.interfaz.rbTercerosCompletos.isChecked() or
                 self.interfaz.rbTodoRiesgo.isChecked()
                )):
                    print("FUNCO LA VERIFICACION")
                    return True
        except Exception as e:
            print(f"Error en verificacion: {e}")
              
    def recuperarDatosPoliza(self):
        try:
            if self.interfaz.rbRespCivil.isChecked():
                self.datosPoliza.tipoCobertura = 1
            else:
                pass
            if self.interfaz.rbIncendioTotel.isChecked():
                self.datosPoliza.tipoCobertura = 2
            else:
                pass
            if self.interfaz.rbTodoTotal.isChecked():
                self.datosPoliza.tipoCobertura = 3
            else:
                pass
            if self.interfaz.rbTercerosCompletos.isChecked():
                self.datosPoliza.tipoCobertura = 4
            else:
                pass
            if self.interfaz.rbTodoRiesgo.isChecked():
                self.datosPoliza.tipoCobertura = 5
            else:
                pass
            
            self.datosPoliza.fechaInicioVigencia = self.interfaz.txtFechaInicioVigencia.text()
            self.datosPoliza.fechaFinVigencia = self.sumar_seis_meses_str()
            self.datosPoliza.formaPago = self.interfaz.cbFormaPago.currentText()
        except Exception as e:
            print(f"Error en recuperacion: {e}")
      
    def IngConfirmacion_poliza(self):
          
        if self.verificar():    
            try:
                self.recuperarDatosPoliza()
                fp=self.interfaz.cbFormaPago.currentText()
                print(self.datosPoliza)
                if  fp == "Semestral":
                    self.confirmacion_poliza_1 = Confirmacion_poliza_1(self,self.datosCliente,self.datosPoliza)
                    self.interfaz.hide()
                else:
                    self.confirmacion_poliza_6 = Confirmacion_poliza_6(self,self.datosCliente,self.datosPoliza)
                    self.interfaz.hide()  
                
            except Exception as e:
                print(f"Error en muestra: {e}")  
        else:    
            try:
                self.aviso=Aviso(self,'Completar los datos por favor')
            except Exception as e:
                print(f"Error: {e}")  

    def btnConfirmar(self):
        self.interfaz.btnConfirmar.clicked.connect(self.IngConfirmacion_poliza)
    
    def btnVolver(self):
         self.interfaz.btnVolver.clicked.connect(self.volver)
        
    def volver(self):
         self.ingreso_datos_poliza.interfaz.show()
         self.interfaz.close()
         
    def sumar_seis_meses_str(self):
        try:
            fechaFin = self.datosPoliza.fechaInicioVigencia
            datetime_object = datetime.strptime(fechaFin, '%d/%m/%Y').date()
            fecha_resultado = datetime_object + relativedelta(months=6)
            return fecha_resultado
        
        except Exception as e:
            print(f"Error en interfaz fecha 1: {e}")
    
    def innit_fechaInicio(self):
        try:
            fecha_actual = datetime.now()
            fecha_resultado = fecha_actual + relativedelta(days=1)
            fecha_formateada = fecha_resultado.strftime('%d/%m/%Y')
            self.interfaz.txtFechaInicioVigencia.setText(fecha_formateada)
            
            return fecha_formateada
        
        except Exception as e:
            print(f"Error en interfaz fecha 2: {e}")
            
    def finalizar(self):
        self.ingreso_datos_poliza.volver()
        self.interfaz.close()
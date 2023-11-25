from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from model.modelDTO import ClienteDTO, polizaDTO
from logica.gestor import GestorSis
from datetime import datetime, timedelta
from dateutil.relativedelta import *

class Confirmacion_poliza_6():
    def __init__(self,seleccion_tipo_poliza,clienteDTO,polizaDTO):
        self.confirmacion_poliza_6 = uic.loadUi("gui/confirmacion_poliza_6.ui")
        self.seleccion_tipo_poliza=seleccion_tipo_poliza
        self.datosCliente=clienteDTO
        self.datosPoliza=polizaDTO
        
        try:
            self.confirmacion_poliza_6.txtNombre.setText(f"{clienteDTO.nombre}")
            self.confirmacion_poliza_6.txtApellido.setText(f"{clienteDTO.apellido}")
            self.confirmacion_poliza_6.txtMarcaVehiculo.setText(f"{polizaDTO.marcaVehiculo}")
            self.confirmacion_poliza_6.txtModeloVehiculo.setText(f"{polizaDTO.modeloVehiculo}")
            self.confirmacion_poliza_6.txtPatente.setText(f"{polizaDTO.patente}")
            self.confirmacion_poliza_6.txtMotor.setText(f"{polizaDTO.motor}")
            self.confirmacion_poliza_6.txtChasis.setText(f"{polizaDTO.chasis}")
            self.confirmacion_poliza_6.txtSumaAsegurada.setText(f"{polizaDTO.sumaAsegurada}")
            self.confirmacion_poliza_6.txtImportesPorDescuentos.setText("1000")
            self.confirmacion_poliza_6.txtPremio.setText("1000")
            self.confirmacion_poliza_6.txtFechaInicio.setText(f"{polizaDTO.fechaInicioVigencia}")
            self.confirmacion_poliza_6.txtMontoAbonar.setText("7000")
            self.confirmacion_poliza_6.txtImporteCuota.setText("1000")
            
        except Exception as e:
            print(f"Error en muestra: {e}")
        
        self.sumar_seis_meses_str() 
        self.btnVolver()
        self.btnImprimir()
        self.confirmacion_poliza_6.show()
    
    def btnVolver(self):
         self.confirmacion_poliza_6.btnVolver.clicked.connect(self.volver)
        
    def volver(self):
         self.seleccion_tipo_poliza.seleccion_tipo_poliza.show()
         self.confirmacion_poliza_6.close()
    
    def btnImprimir(self):
        self.confirmacion_poliza_6.btnImprimir.clicked.connect(self.guardar)
    
    def guardar(self):
        
        try:
            gestor = GestorSis()
            gestor.guardar_Poliza(self.datosPoliza,self.datosCliente)
        except Exception as e:
            print(f"Error en interfaz: {e}")
            self.finalizar()
            
    def sumar_seis_meses_str(self):
        try:
            fechaFin = self.datosPoliza.fechaInicioVigencia
            datetime_object = datetime.strptime(fechaFin, '%d/%m/%Y').date()
            fecha_resultado = datetime_object + relativedelta(months=+6)
            self.confirmacion_poliza_6.txtFechaFin.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            self.confirmacion_poliza_6.txtCuota6.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            
            fecha_resultado = datetime_object + relativedelta(months=+1)
            self.confirmacion_poliza_6.txtCuota1.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = datetime_object + relativedelta(months=+2)
            self.confirmacion_poliza_6.txtCuota2.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = datetime_object + relativedelta(months=+3)
            self.confirmacion_poliza_6.txtCuota3.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = datetime_object + relativedelta(months=+4)
            self.confirmacion_poliza_6.txtCuota4.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = datetime_object + relativedelta(months=+5)
            self.confirmacion_poliza_6.txtCuota5.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            
        except Exception as e:
            print(f"Error en suma: {e}")
            
    def finalizar(self):
        self.seleccion_tipo_poliza.finalizar()
        self.confirmacion_poliza_6.close()
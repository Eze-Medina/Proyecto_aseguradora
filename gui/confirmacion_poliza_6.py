from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from model.modelDTO import ClienteDTO, polizaDTO
from logica.gestor import GestorSis
from datetime import datetime, timedelta
from dateutil.relativedelta import *

class Confirmacion_poliza_6():
    def __init__(self,seleccion_tipo_poliza,clienteDTO,polizaDTO):
        self.interfaz = uic.loadUi("gui/confirmacion_poliza_6.ui")
        self.seleccion_tipo_poliza=seleccion_tipo_poliza
        self.datosCliente=clienteDTO
        self.datosPoliza=polizaDTO
        
        try:
            self.interfaz.txtNombre.setText(f"{clienteDTO.nombre}")
            self.interfaz.txtApellido.setText(f"{clienteDTO.apellido}")
            self.interfaz.txtMarcaVehiculo.setText(f"{polizaDTO.marcaVehiculo}")
            self.interfaz.txtModeloVehiculo.setText(f"{polizaDTO.modeloVehiculo}")
            self.interfaz.txtPatente.setText(f"{polizaDTO.patente}")
            self.interfaz.txtMotor.setText(f"{polizaDTO.motor}")
            self.interfaz.txtChasis.setText(f"{polizaDTO.chasis}")
            self.interfaz.txtSumaAsegurada.setText(f"{polizaDTO.sumaAsegurada}")
            self.interfaz.txtImportesPorDescuentos.setText("1000")
            self.interfaz.txtPremio.setText("1000")
            self.interfaz.txtFechaInicio.setText(f"{polizaDTO.fechaInicioVigencia}")
            self.interfaz.txtMontoAbonar.setText("7000")
            self.interfaz.txtImporteCuota.setText("1000")
            
        except Exception as e:
            print(f"Error en muestra: {e}")
        
        self.sumar_seis_meses_str() 
        self.btnVolver()
        self.btnImprimir()
        self.interfaz.show()
    
    def btnVolver(self):
         self.interfaz.btnVolver.clicked.connect(self.volver)
        
    def volver(self):
         self.seleccion_tipo_poliza.interfaz.show()
         self.interfaz.close()
    
    def btnImprimir(self):
        self.interfaz.btnImprimir.clicked.connect(self.guardar)
    
    def guardar(self):
        gestor = GestorSis()
        gestor.guardar_Poliza(self.datosPoliza,self.datosCliente)
        self.finalizar()
            
    def sumar_seis_meses_str(self):
        try:
            fechaFin = self.datosPoliza.fechaInicioVigencia
            datetime_object = datetime.strptime(fechaFin, '%d/%m/%Y').date()
            fecha_resultado = datetime_object + relativedelta(months=+6)
            self.interfaz.txtFechaFin.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            self.interfaz.txtCuota6.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            
            fecha_resultado = datetime_object + relativedelta(months=+1)
            self.interfaz.txtCuota1.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = datetime_object + relativedelta(months=+2)
            self.interfaz.txtCuota2.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = datetime_object + relativedelta(months=+3)
            self.interfaz.txtCuota3.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = datetime_object + relativedelta(months=+4)
            self.interfaz.txtCuota4.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = datetime_object + relativedelta(months=+5)
            self.interfaz.txtCuota5.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            
        except Exception as e:
            print(f"Error en suma: {e}")
            
    def finalizar(self):
        self.seleccion_tipo_poliza.finalizar()
        self.interfaz.close()
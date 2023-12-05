from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from model.modelDTO import ClienteDTO, polizaDTO
from logica.gestor import GestorPoliza
from datetime import datetime, timedelta
from gui.aviso import Aviso
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
            self.interfaz.txtImportesPorDescuentos.setText(f"{100:.2f}")
            self.interfaz.txtPremio.setText(f"{1000:.2f}")
            self.interfaz.txtFechaInicio.setText(f"{polizaDTO.fechaInicioVigencia}")
            self.interfaz.txtMontoAbonar.setText(f"{900:.2f}")
            self.interfaz.txtImporteCuota.setText(f"{900/6:.2f}")
            
        except Exception as e:
            print(f"Error en muestra: {e}")
        
        self.initMesesPago() 
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
        gestor = GestorPoliza()
        gestor.guardar_Poliza(self.datosPoliza,self.datosCliente)
        self.finalizar()
            
    def initMesesPago(self):
        try:
            fechaFin = self.datosPoliza.fechaInicioVigencia
            datetime_object = datetime.strptime(fechaFin, '%d/%m/%Y').date() 
            datetime_object = datetime_object - relativedelta(days=1)
            fecha_resultado = self.datosPoliza.fechaFinVigencia
            self.interfaz.txtFechaFin.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = self.datosPoliza.fechaFinVigencia - relativedelta(days=1)
            self.interfaz.txtCuota6.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            
            fecha_resultado = datetime_object 
            self.interfaz.txtCuota1.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = datetime_object + relativedelta(months=1)
            self.interfaz.txtCuota2.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = datetime_object + relativedelta(months=2)
            self.interfaz.txtCuota3.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = datetime_object + relativedelta(months=3)
            self.interfaz.txtCuota4.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = datetime_object + relativedelta(months=4)
            self.interfaz.txtCuota5.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            fecha_resultado = datetime_object + relativedelta(months=5)
            self.interfaz.txtCuota6.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            
        except Exception as e:
            print(f"Error en suma: {e}")
            self.aviso=Aviso(self,f'Error en suma: {e}')
            
    def finalizar(self):
        self.seleccion_tipo_poliza.finalizar()
        self.interfaz.close()
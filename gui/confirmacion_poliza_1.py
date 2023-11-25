from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from model.modelDTO import ClienteDTO, polizaDTO
from logica.gestor import GestorSis
from datetime import datetime, timedelta
from dateutil.relativedelta import *

class Confirmacion_poliza_1():
    def __init__(self,seleccion_tipo_poliza,clienteDTO,polizaDTO):
        self.confirmacion_poliza_1 = uic.loadUi("gui/confirmacion_poliza_1.ui")
        self.seleccion_tipo_poliza=seleccion_tipo_poliza
        self.datosCliente=clienteDTO
        self.datosPoliza=polizaDTO
        
        try:
            self.confirmacion_poliza_1.txtNombre.setText(f"{clienteDTO.nombre}")
            self.confirmacion_poliza_1.txtApellido.setText(f"{clienteDTO.apellido}")
            self.confirmacion_poliza_1.txtMarcaVehiculo.setText(f"{polizaDTO.marcaVehiculo}")
            self.confirmacion_poliza_1.txtModeloVehiculo.setText(f"{polizaDTO.modeloVehiculo}")
            self.confirmacion_poliza_1.txtPatente.setText(f"{polizaDTO.patente}")
            self.confirmacion_poliza_1.txtMotor.setText(f"{polizaDTO.motor}")
            self.confirmacion_poliza_1.txtChasis.setText(f"{polizaDTO.chasis}")
            self.confirmacion_poliza_1.txtSumaAsegurada.setText(f"{polizaDTO.sumaAsegurada}")
            self.confirmacion_poliza_1.txtImportesPorDescuentos.setText("1000")
            self.confirmacion_poliza_1.txtPremio.setText("1000")
            self.confirmacion_poliza_1.txtFechaInicio.setText(f"{polizaDTO.fechaInicioVigencia}")
            self.confirmacion_poliza_1.txtUltimoPago.setText("1000")
            self.confirmacion_poliza_1.txtMontoAbonar.setText("1000")
            
        except Exception as e:
            print(f"Error en muestra: {e}")
        print(polizaDTO)
        self.sumar_seis_meses_str()   
        self.btnVolver()
        self.btnImprimir()
        self.confirmacion_poliza_1.show()
    
    def sumar_seis_meses_str(self):
        try:
            fechaFin = self.datosPoliza.fechaInicioVigencia
            datetime_object = datetime.strptime(fechaFin, '%d/%m/%Y').date()
            fecha_resultado = datetime_object + relativedelta(months=6)
            self.confirmacion_poliza_1.txtFechaFin.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            
        except Exception as e:
            print(f"Error en fecha3: {e}")
       
    def btnVolver(self):
         self.confirmacion_poliza_1.btnVolver.clicked.connect(self.volver)
        
    def volver(self):
        self.seleccion_tipo_poliza.seleccion_tipo_poliza.show()
        self.confirmacion_poliza_1.close()
        
    def btnImprimir(self):
        self.confirmacion_poliza_1.btnImprimir.clicked.connect(self.guardar)
    
    def guardar(self):
        gestor = GestorSis()
        gestor.guardar_Poliza(self.datosPoliza,self.datosCliente)
        self.finalizar()
        
    def finalizar(self):
        self.seleccion_tipo_poliza.finalizar()
        self.confirmacion_poliza_1.close()
    
    
             
    
            
    
            
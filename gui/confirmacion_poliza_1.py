from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from model.modelDTO import ClienteDTO, polizaDTO
from logica.gestor import GestorSis
from datetime import datetime, timedelta
from dateutil.relativedelta import *

class Confirmacion_poliza_1():
    def __init__(self,seleccion_tipo_poliza,clienteDTO,polizaDTO):
        self.interfaz = uic.loadUi("gui/confirmacion_poliza_1.ui")
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
            self.interfaz.txtUltimoPago.setText("1000")
            self.interfaz.txtMontoAbonar.setText("1000")
            
        except Exception as e:
            print(f"Error en muestra: {e}")
        print(polizaDTO)
        self.sumar_seis_meses_str()   
        self.btnVolver()
        self.btnImprimir()
        self.interfaz.show()
    
    def sumar_seis_meses_str(self):
        try:
            fechaFin = self.datosPoliza.fechaInicioVigencia
            datetime_object = datetime.strptime(fechaFin, '%d/%m/%Y').date()
            fecha_resultado = datetime_object + relativedelta(months=6)
            self.interfaz.txtFechaFin.setText(f"{fecha_resultado.day}/{fecha_resultado.month}/{fecha_resultado.year}")
            
        except Exception as e:
            print(f"Error en fecha3: {e}")
       
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
        
    def finalizar(self):
        self.seleccion_tipo_poliza.finalizar()
        self.interfaz.close()
    
    
             
    
            
    
            
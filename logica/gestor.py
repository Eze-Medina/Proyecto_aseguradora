from datetime import datetime
from data.modelDAO import clienteDAO, provinciaDAO, marcaDAO, localidaDAO, modeloDAO, estadoCivilDAO, factorKmDAO
from data.modelDAO import cantSiniestrosDAO, hijoDAO, polizaDAO, DAO, polizaSegDAO, cuotaDAO, vehiculoDAO
from model.modelDTO import ClienteDTO, ProvinciaDTO, MarcaDTO, LocalidadDTO, modeloDTO
from model.modelDTO import estadoCivilDTO, cantSiniestrosDTO, hijoDTO, polizaDTO
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class GestorUbicacion:
    
    def listar_provincias(self, provinciaDTO: ProvinciaDTO):
        provDAO=provinciaDAO()
        lista=provDAO.listar_provincias(provinciaDTO)
        listaRES=[]
        for provincia in lista:
            provinciaRES=ProvinciaDTO(nombre=provincia.nombre)
            listaRES.append(provinciaRES)
        return listaRES
    
    def listar_localidades(self, txtProvincia):
        provDAO=provinciaDAO()
        prov=provDAO.buscar_provincia(txtProvincia)
        print(f"Provincia seleccionada: {prov.nombre}")
        codProv=prov.codigoProvincia
        locDAO=localidaDAO()
        lista= locDAO.listar_localidades(codProv)
        listaRES=[]
        for localidad in lista:
            locRES=LocalidadDTO(nombre=localidad.nombre)
            listaRES.append(locRES)           
        return listaRES
    
class GestorVehiculo:
    
    def listar_marcas(self, marcaDTO: MarcaDTO):
        marDAO=marcaDAO()
        lista= marDAO.listar_marcas(marcaDTO)
        listaRES=[]
        for marca in lista:
            marcaRES=MarcaDTO(nombre=marca.nombre)
            listaRES.append(marcaRES)
        return listaRES
    
    def listar_modelos(self, txtMarca):
        marDAO=marcaDAO()
        marca=marDAO.buscar_marca(txtMarca)
        print(f"Provincia seleccionada: {marca.nombre}")
        idMarca=marca.idMarca
        modDAO=modeloDAO()
        lista= modDAO.listar_modelos(idMarca)
        listaRES=[]
        for modelo in lista:
            modRES=modeloDTO(nombre=modelo.nombre)
            listaRES.append(modRES)           
        return listaRES
    
    def listar_siniestros(self):
        sinisDAO=cantSiniestrosDAO()
        lista=sinisDAO.listar_siniestros()
        listaRES=[]
        for cantSini in lista:
            siniRES=cantSiniestrosDTO(cantidad=cantSini.cantidad)
            listaRES.append(siniRES)
        return listaRES
    
    def listar_anios(self,txtModelo):
        modelDAO=modeloDAO()
        modelo=modelDAO.buscar_modelo(txtModelo)
        try:
            inicio=int(modelo.inicioProduccion.year)
            fin=int(modelo.finProduccion.year)
            anios=[]
            for i in range(inicio, fin + 1):
                anios.append(i)
        except Exception as e:
            print(f"Error en listar_anios(): {e}")    
               
        return anios
    
    def vehiculo_id(self):
        vehiculoDao=vehiculoDAO()
        newIdVehiculo = vehiculoDao.ulimo_id()
        return newIdVehiculo

    def guardar(self,polizaDTO: polizaDTO):
        vehiculoDao = vehiculoDAO()
        modeloDao = modeloDAO()
        factorKmDao = factorKmDAO()
        siniDao=cantSiniestrosDAO()
        try:
            modelo = modeloDao.buscar_modelo(polizaDTO.modeloVehiculo)
            idModelo = modelo.idModelo
            idFactorKm = factorKmDao.buscar_id(polizaDTO.kilometrosAnio)
            idSini= siniDao.buscar_id(polizaDTO.cantSiniestros)
            vehiculoDao.guardar(polizaDTO.patente,idModelo,idSini,idFactorKm,polizaDTO.anioVehiculo,polizaDTO.kilometrosAnio,
                                polizaDTO.chasis,polizaDTO.motor)
        except Exception as e:
            print(f"Error en VEHICULO(): {e}") 
                
class GestorCliente:
    
    def listar_clientes(self, clienteDTO: ClienteDTO):
        try:
            cliDAO=clienteDAO()
            lista=cliDAO.listar_clientes(clienteDTO)
            listaRES=[]
            for cliente in lista:
                clienteRES=ClienteDTO(idCliente=cliente.idCliente,
                                numeroDocumento=cliente.numeroDocumento,
                                nombre=cliente.nombre,
                                apellido=cliente.apellido,
                                tipoDocumento = cliente.tipo_documento.tipoDocumento)
                listaRES.append(clienteRES)
            return listaRES
        
        except Exception as e:
            print(f"Error en gestor en funcion listar_cliente: {e}")
           
    def buscar_cliente(self, clienteDTO: ClienteDTO):
        cliDAO=clienteDAO()
        cliente=cliDAO.buscar_cliente(clienteDTO)
        newClienteDTO= ClienteDTO(idCliente=cliente.idCliente,
                             numeroDocumento=cliente.numeroDocumento,
                             nombre=cliente.nombre,
                             apellido=cliente.apellido,
                             tipoDocumento = cliente.tipo_documento.tipoDocumento,
                             numeroVivienda= cliente.vivienda.numero,
                             nombreVivienda= cliente.vivienda.calle)
        
        return newClienteDTO
    
    def listar_documentos(self):
        try: 
            documentos = clienteDAO()
            tiposDocumentos = documentos.listar_documentos()
            return tiposDocumentos
        except Exception as e:
            print(f"Error en gestor: {e}")
    
class GestorDatos:
    
    def listar_estadoCivil(self):
        estadDAO=estadoCivilDAO()
        lista=estadDAO.listar_estados()
        listaRES=[]
        for estadoC in lista:
            estadoRES=estadoCivilDTO(estado=estadoC.estado)
            listaRES.append(estadoRES)
        return listaRES
    
    def hijo_id(self):
        hijoDao=hijoDAO()
        newIdHijo = hijoDao.ulimo_id()
        newIdHijo += 1
        return newIdHijo
    
    def guardarHijos(self,polizaDTO: polizaDTO,newIdPoliza):
        estCivilDao=estadoCivilDAO()
        hijoDao = hijoDAO()
        try:
            for hijo in polizaDTO.hijos:
                idEstado=estCivilDao.buscar_id(hijo.estadoCivil)
                hijoDao.guardar(idEstado,newIdPoliza,hijo.edad,hijo.sexo)       
        except Exception as e:
            print(f"Error en HIJO(): {e}")

class GestorPoliza:
    
    def guardar_Poliza(self, polizaDTO: polizaDTO, clienteDTO: ClienteDTO):
        gesVehiculo=GestorVehiculo() 
        gesDatos=GestorDatos()
        polizaDao = polizaDAO()
        poliSegDao = polizaSegDAO()
        cuotaDao = cuotaDAO()
        
        # ////////////////////////polizaDao.guardar_poliza(polizaDTO, clienteDTO)/////////////////////////
        
        # inicio de vigencia
       
        fechaInicio = datetime.strptime(polizaDTO.fechaInicioVigencia, '%d/%m/%Y').date()
        
        # CREACION DE OBJETO: VEHICULO
        
        try:
            gesVehiculo.guardar(polizaDTO)
            newIdVehiculo = gesVehiculo.vehiculo_id()
        except Exception as e:
            print(f"Error en VEHICULO(): {e}")
            
        # CREACION DE OBJETO: POLIZA
        
        try:
            polizaDao.guardar(clienteDTO.idCliente,newIdVehiculo,polizaDTO.tipoCobertura,
                              polizaDTO.fechaFinVigencia,fechaInicio,polizaDTO.sumaAsegurada)
            newIdPoliza = polizaDao.ulimo_id()
        except Exception as e:
            print(f"Error en POLIZA(): {e}")
            
        # CREACION DE OBJETOS: POLIZA SEGURIDAD
        try:       
            for medida in polizaDTO.medidas:
                poliSegDao.guardar(medida,newIdPoliza)
        except Exception as e:
            print(f"Error en SEGURIDAD(): {e}") 
              
        # CREACION DE OBJETOS: HIJO
        
        try: 
            gesDatos.guardarHijos(polizaDTO,newIdPoliza)
        except Exception as e:
            print(f"Error en HIJO(): {e}") 
                           
        # CREACION DE OBJETO: CUOTAS
        
        newIdCuota = cuotaDao.ulimo_id()
        newIdCuota += 1
        
        try:
            cuota_time = fechaInicio - timedelta(days=1)
        
            if polizaDTO.formaPago=="Semestral":
                cuotaDao.guardar(newIdPoliza,1,cuota_time,100,1000,900)
                
            elif polizaDTO.formaPago=="Mensual":
            
                for i in range(1, 7):
                    cuotaDao.guardar(newIdPoliza,i,cuota_time,100,1000,900/6)
                    cuota_time = cuota_time + relativedelta(months=1)           
        except Exception as e:
            print(f"Error en CUOTAS(): {e}")
            
    def verificar_datos(self, polizaDTO: polizaDTO):
        vehiculoDao = vehiculoDAO()
        polizaDao = polizaDAO()
        año_actual = datetime.now().year
        diferencia = año_actual - polizaDTO.anioVehiculo
        print(diferencia)
        
        if diferencia > 10 and polizaDTO.tipoCobertura != 1:
            return "Vehiculo con antiguedad mayor a 10 años, solo puede seleccionar cobertura de Responsabilidad Civil"
        else:
            pass
        
        try:
            vehiculo_existente = vehiculoDao.buscar_vehiculo(polizaDTO)
        except Exception as e:
            print(f"Error en verificar_datos() al buscar_vehiculo(): {e}")
            
        if vehiculo_existente is None:
            return ""
        else:
            poliza_encontrada = polizaDao.comprobar_existencia(vehiculo_existente.idVehiculo)
            if poliza_encontrada is not None:
                return "Vehiculo con poliza vigente - Revisar patente"
            else:
                return ""
        
class GestorAseguradora:
    def recuperar_SumaAsegurada(self):
        return 15000
    
        try: 
            documentos = clienteDAO()
            tiposDocumentos = documentos.listar_documentos()
            return tiposDocumentos
        except Exception as e:
            print(f"Error en gestor: {e}") 
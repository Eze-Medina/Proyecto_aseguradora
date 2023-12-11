from datetime import datetime
from data.modelDAO import clienteDAO, provinciaDAO, marcaDAO, localidaDAO, modeloDAO, estadoCivilDAO, factorKmDAO, registroFactoresDAO, medidaDeSeguridadDAO
from data.modelDAO import cantSiniestrosDAO, hijoDAO, polizaDAO, DAO, polizaSegDAO, cuotaDAO, vehiculoDAO, cambioEstadoDAO, tipoCoberturaDAO, factorUniDAO
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
    
    def getFactorLoca(self,localidad):
        localidadDao=localidaDAO()
        factor=localidadDao.buscarFactor(localidad)
        return factor
    
    def getFactorProv(self,provincia):
        provinciaDao=provinciaDAO()
        factor=provinciaDao.buscarFactor(provincia)
        return factor
    
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
      
    def getFactorMode(self,modeloVehiculo):
        modeloDao=modeloDAO()
        factor=modeloDao.buscarFactor(modeloVehiculo)
        return factor
        
    def getFactorKilm(self,kilometrosAnio):
        factorKmDao=factorKmDAO()
        factor=factorKmDao.buscarFactor(kilometrosAnio)
        return factor
               
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

    def actualizarEstado(self,clienteDTO: ClienteDTO):
        clienteDao=clienteDAO()
        cambioEstDao=cambioEstadoDAO()
        cliente=clienteDao.buscar_cliente_completo(clienteDTO)
        fechaActual = datetime.now()
        
        try:
            primeraPoliza=True
            contador=0
            for cambio in cliente.cambioEstado:
                if cambio.estado.tipoEstado=='Normal':
                    primeraPoliza=False
                    break
        except Exception as e:
            print(f"Error en primeraPoliza: {e}")
            
        try:
            existeSini=False
            for poliza in cliente.polizas:
                fechaFin = poliza.fechaFin
                diff=relativedelta(fechaActual,fechaFin).years
                if ((diff<1)and(poliza.vehiculo.cantSiniestros.cantidad!='Ninguno')):
                    existeSini=True
                    break
        except Exception as e:
            print(f"Error en existeSini: {e}")
        
        try:    
            existeImpago=False
            contador=1
            for poliza in cliente.polizas:
                if contador<len(cliente.polizas):
                    for cuota in poliza.cuotas:
                        if cuota.idRecibo==None:
                            existeImpago=True
                            break
                if existeImpago:
                    break
                contador+=1
        except Exception as e:
            print(f"Error en existeImpago: {e}")
            
        try:       
            existeIncont=False
            for cambio in cliente.cambioEstado:
                fechaCambio=cambio.fechaCambio
                diff=relativedelta(fechaActual,fechaCambio).years
                if (cambio.estado.tipoEstado=='Inactivo') and (diff<2):
                    existeIncont=True
                    break
        except Exception as e:
            print(f"Error en existeIncont: {e}")
        
        try:
            print(f"{primeraPoliza}____{existeSini}____{existeImpago}____{existeIncont}")
            if primeraPoliza:
                newIdEstado=3
                cambioEstDao.guardar(newIdEstado,cliente.idCliente,fechaActual)
            elif (existeSini or existeImpago or existeIncont):
                newIdEstado=3
                cambioEstDao.guardar(newIdEstado,cliente.idCliente,fechaActual)
            else:
                newIdEstado=4
                cambioEstDao.guardar(newIdEstado,cliente.idCliente,fechaActual)
        except Exception as e:
            print(f"Error en actualizar poliza: {e}")
    
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
            
    def getFactorTipo(self,tipoCobertura):
        tipoCoberDao=tipoCoberturaDAO()
        factor=tipoCoberDao.buscarFactor(tipoCobertura)
        return factor
        
    def getFactorSini(self,cantSiniestros):
        cantSiniestrosDao=cantSiniestrosDAO()
        factor=cantSiniestrosDao.buscarFactor(cantSiniestros)
        return factor
        
    def getFactorGar(self,medida):
        medidasDao=medidaDeSeguridadDAO()
        if medida[0]==1:
            factor=medidasDao.buscarFactor(medida[0])
            return factor
        else:
            return 1
        
    def getFactorAla(self,medida):
        medidasDao=medidaDeSeguridadDAO()
        if medida[1]==2:
            factor=medidasDao.buscarFactor(medida[1])
            return factor
        else:
            return 1
          
    def getFactorRas(self,medida):
        medidasDao=medidaDeSeguridadDAO()
        if medida[2]==3:
            factor=medidasDao.buscarFactor(medida[2])
            return factor     
        else:
            return 1
        
    def getFactorTue(self,medida):
        medidasDao=medidaDeSeguridadDAO()
        if medida[3]==4:
            factor=medidasDao.buscarFactor(medida[3])
            return factor     
        else:
            return 1
        
    def getFactorHijo(self):
        factorUniDao=factorUniDAO()
        factor=factorUniDao.buscarFactorHijo()
        return factor

class GestorPoliza:
    
    def cargarEj(self):
        cuotaDao=cuotaDAO()
        cuotaDao.cargarEj()
    
    def guardar_Poliza(self, polizaDTO: polizaDTO, clienteDTO: ClienteDTO):
        gesVehiculo=GestorVehiculo() 
        gesDatos=GestorDatos()
        gesCliente=GestorCliente()
        gesUbicacion=GestorUbicacion()
        polizaDao = polizaDAO()
        poliSegDao = polizaSegDAO()
        cuotaDao = cuotaDAO()
        regFactor= registroFactoresDAO()
        
        # ////////////////////////polizaDao.guardar_poliza(polizaDTO, clienteDTO)/////////////////////////
        
        # inicio de vigencia
       
        fechaInicio = datetime.strptime(polizaDTO.fechaInicioVigencia, '%d/%m/%Y').date()
        
        
        try:
            
            # CREACION DE OBJETO: VEHICULO
            gesVehiculo.guardar(polizaDTO)
            newIdVehiculo = gesVehiculo.vehiculo_id()
                
            # CREACION DE OBJETO: POLIZA
            
            polizaDao.guardar(clienteDTO.idCliente,newIdVehiculo,polizaDTO.tipoCobertura,
                            polizaDTO.fechaFinVigencia,fechaInicio,polizaDTO.sumaAsegurada)
            newIdPoliza = polizaDao.ulimo_id()
                
            # CREACION DE OBJETOS: POLIZA SEGURIDAD
                   
            for medida in polizaDTO.medidas:
                poliSegDao.guardar(medida,newIdPoliza)
               
            # CREACION DE OBJETOS: HIJO
        
            gesDatos.guardarHijos(polizaDTO,newIdPoliza) 
                            
            # CREACION DE OBJETO: CUOTAS
            
            newIdCuota = cuotaDao.ulimo_id()
            newIdCuota += 1
        
            cuota_time = fechaInicio - timedelta(days=1)
        
            if polizaDTO.formaPago=="Semestral":
                cuotaDao.guardar(newIdPoliza,1,cuota_time,100,1000,900)
                
            elif polizaDTO.formaPago=="Mensual":
            
                for i in range(1, 7):
                    cuotaDao.guardar(newIdPoliza,i,cuota_time,100,1000,900/6)
                    cuota_time = cuota_time + relativedelta(months=1)           

            # CREACION DE OBJETO: REGISTROFACTORES
            try:
                newFactorTipo=gesDatos.getFactorTipo(polizaDTO.tipoCobertura)
                newFactorSini=gesDatos.getFactorSini(polizaDTO.cantSiniestros)
                newFactorGar=gesDatos.getFactorGar(polizaDTO.medidas)
                newFactorAla=gesDatos.getFactorAla(polizaDTO.medidas)
                newFactorRas=gesDatos.getFactorRas(polizaDTO.medidas)
                newFactorTue=gesDatos.getFactorTue(polizaDTO.medidas)
                newFactorHijo=gesDatos.getFactorHijo()
                newFactorMode=gesVehiculo.getFactorMode(polizaDTO.modeloVehiculo)
                newFactorKilm=gesVehiculo.getFactorKilm(polizaDTO.kilometrosAnio)
                newFactorLoca=gesUbicacion.getFactorLoca(polizaDTO.localidad)
                newFactorProv=gesUbicacion.getFactorProv(polizaDTO.provincia)
            except Exception as e:
                print(f"Error en guardar poliza(): {e}")
            try:
                regFactor.guardar(
                    newIdPoliza,
                    newFactorTipo,
                    newFactorSini,
                    newFactorGar,
                    newFactorAla,
                    newFactorRas,
                    newFactorTue,
                    newFactorHijo,
                    newFactorMode,
                    newFactorKilm,
                    newFactorLoca,
                    newFactorProv
                )
            except Exception as e:
                print(f"Error en guardar poliza(): {e}")
            #ACTUALIZAR ESTADO:
            
            gesCliente.actualizarEstado(clienteDTO)
        
        except Exception as e:
            print(f"Error en guardar poliza(): {e}")
            
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
    
        # try: 
        #     documentos = clienteDAO()
        #     tiposDocumentos = documentos.listar_documentos()
        #     return tiposDocumentos
        # except Exception as e:
        #     print(f"Error en gestor: {e}") 
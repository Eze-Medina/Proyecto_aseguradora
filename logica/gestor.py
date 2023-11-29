from datetime import datetime
from data.modelDAO import clienteDAO, provinciaDAO, marcaDAO, localidaDAO, modeloDAO, estadoCivilDAO, factorKmDAO
from data.modelDAO import cantSiniestrosDAO, hijoDAO, polizaDAO, DAO, polizaSegDAO, cuotaDAO, vehiculoDAO
from model.modelDTO import ClienteDTO, ProvinciaDTO, MarcaDTO, LocalidadDTO, modeloDTO
from model.modelDTO import estadoCivilDTO, cantSiniestrosDTO, hijoDTO, polizaDTO
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
class GestorSis():
    def listar_clientes(self, clienteDTO: ClienteDTO):
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
    
    def listar_provincias(self, provinciaDTO: ProvinciaDTO):
        provDAO=provinciaDAO()
        lista=provDAO.listar_provincias(provinciaDTO)
        listaRES=[]
        for provincia in lista:
            provinciaRES=ProvinciaDTO(nombre=provincia.nombre)
            listaRES.append(provinciaRES)
        return listaRES
    
    def listar_marcas(self, marcaDTO: MarcaDTO):
        marDAO=marcaDAO()
        lista= marDAO.listar_marcas(marcaDTO)
        listaRES=[]
        for marca in lista:
            marcaRES=MarcaDTO(nombre=marca.nombre)
            listaRES.append(marcaRES)
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
    
    def recuperar_SumaAsegurada(self):
        return 15000
        
    def listar_estadoCivil(self):
        estadDAO=estadoCivilDAO()
        lista=estadDAO.listar_estados()
        listaRES=[]
        for estadoC in lista:
            estadoRES=estadoCivilDTO(estado=estadoC.estado)
            listaRES.append(estadoRES)
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


    def guardar_Poliza(self, polizaDTO: polizaDTO, clienteDTO: ClienteDTO):
        polizaDao = polizaDAO()
        poliSegDao = polizaSegDAO()
        hijoDao = hijoDAO()
        cuotaDao = cuotaDAO()
        vehiculoDao = vehiculoDAO()
        modeloDao = modeloDAO()
        factorKmDao = factorKmDAO()
        siniDao=cantSiniestrosDAO()
        estCivilDao=estadoCivilDAO()
        # ////////////////////////polizaDao.guardar_poliza(polizaDTO, clienteDTO)/////////////////////////
        
        # inicio de vigencia
        fechaInicio = datetime.strptime(polizaDTO.fechaInicioVigencia, '%d/%m/%Y').date()
        
        # identifiacion de los proximos ID
        
        newIdPoliza = polizaDao.ulimo_id()
        newIdPoliza += 1
        
        newIdPolizaSeg = poliSegDao.ulimo_id()
        newIdPolizaSeg += 1
        
        newIdHijo = hijoDao.ulimo_id()
        newIdHijo += 1
        
        newIdCuota = cuotaDao.ulimo_id()
        newIdCuota += 1
        
        newIdVehiculo = vehiculoDao.ulimo_id()
        newIdVehiculo += 1
        
        # CREACION DE OBJETOS: POLIZA SEGURIDAD
        
        try:
            for medida in polizaDTO.medidas:
                poliSegDao.guardar(medida,newIdPolizaSeg,newIdPoliza)
                newIdPolizaSeg += 1 
        except Exception as e:
            print(f"Error en SEGURIDAD(): {e}") 
              
        # CREACION DE OBJETO: POLIZA
        
        try:
            polizaDao.guardar(newIdPoliza,clienteDTO.idCliente,newIdVehiculo,polizaDTO.tipoCobertura,
                            polizaDTO.fechaFinVigencia,fechaInicio,polizaDTO.sumaAsegurada)
        except Exception as e:
            print(f"Error en POLIZA(): {e}")
            
        # CREACION DE OBJETO: VEHICULO
        
        try:
            modelo = modeloDao.buscar_modelo(polizaDTO.modeloVehiculo)
            idModelo = modelo.idModelo
            idFactorKm = factorKmDao.buscar_id(polizaDTO.kilometrosAnio)
            idSini= siniDao.buscar_id(polizaDTO.cantSiniestros)
            vehiculoDao.guardar(newIdVehiculo,polizaDTO.patente,idModelo,idSini,idFactorKm,polizaDTO.anioVehiculo,polizaDTO.kilometrosAnio,
                                polizaDTO.chasis,polizaDTO.motor)
        except Exception as e:
            print(f"Error en VEHICULO(): {e}")  
            
        # CREACION DE OBJETOS: HIJO
        
        try:
            for hijo in polizaDTO.hijos:
                idEstado=estCivilDao.buscar_id(hijo.estadoCivil)
                hijoDao.guardar(newIdHijo,idEstado,newIdPoliza,hijo.edad,hijo.sexo)
                newIdHijo += 1       
            
        except Exception as e:
            print(f"Error en HIJO(): {e}")
                    
        # CREACION DE OBJETO: CUOTAS
        
        try:
            cuota_time = fechaInicio - timedelta(days=1)
        
            if polizaDTO.formaPago=="Semestral":
                cuotaDao.guardar(newIdCuota,newIdPoliza,1,cuota_time,100,1000,900)
                
            elif polizaDTO.formaPago=="Mensual":
            
                for i in range(1, 7):
                    cuotaDao.guardar(newIdCuota,newIdPoliza,i,cuota_time,100,1000,900/6)
                    newIdCuota += 1
                    cuota_time = cuota_time + relativedelta(months=1)
                         
        except Exception as e:
            print(f"Error en CUOTAS(): {e}")

        
          
    # def AAAAAAAA(self):
    #     print("------------------------------------------------------------------------------------------------------------")
    #     dao=DAO()
    #     poliza=dao.prueba()
    #     print(poliza)
    #     print(poliza.vehiculo)
    #     for hijo in poliza.hijo: 
    #          print(hijo," ",hijo.estadoCivil)
        
        
            
        
                
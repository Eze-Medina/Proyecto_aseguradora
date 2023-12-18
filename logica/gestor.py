from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine, select, func, insert, desc, and_, asc, or_
from sqlalchemy.sql.functions import coalesce


from datetime import datetime
from data.modelDAO import clienteDAO, provinciaDAO, marcaDAO, localidaDAO, modeloDAO, estadoCivilDAO, factorKmDAO, medidaDeSeguridadDAO
from data.modelDAO import cantSiniestrosDAO, hijoDAO, polizaDAO, cuotaDAO, vehiculoDAO, tipoCoberturaDAO, factorUniDAO ,cambioEstadoDAO
from model.modelDTO import ClienteDTO, ProvinciaDTO, MarcaDTO, LocalidadDTO, modeloDTO
from model.modelDTO import estadoCivilDTO, cantSiniestrosDTO, polizaDTO
from model.models import cuotas, poliza, registroFactores, cliente
from model.models import vehiculo, hijo, poliza_Seguridad
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
    
    def vehiculos_existentes(self, polizaDTO: polizaDTO):
        vehiculoDao = vehiculoDAO()
        try:
            vehiculos_existente = vehiculoDao.buscar_vehiculo(polizaDTO)
        except Exception as e:
            print(f"Error en verificar_datos() al buscar_vehiculo(): {e}")
        return vehiculos_existente
             
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
        cliente_encontrado=clienteDao.buscar_cliente_completo(clienteDTO)
        fechaActual = datetime.now()
        
        try:
            primeraPoliza=True
            contador=0
            for cambio in cliente_encontrado.cambioEstado:
                if cambio.estado.tipoEstado=='Normal':
                    primeraPoliza=False
                    break
        except Exception as e:
            print(f"Error en primeraPoliza: {e}")
            
        try:
            existeSini=False
            for poliza in cliente_encontrado.polizas:
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
            for poliza in cliente_encontrado.polizas:
                if contador<len(cliente_encontrado.polizas):
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
            for cambio in cliente_encontrado.cambioEstado:
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
                cambioEstDao.guardar(newIdEstado,cliente_encontrado.idCliente,fechaActual)
            elif (existeSini or existeImpago or existeIncont):
                newIdEstado=3
                cambioEstDao.guardar(newIdEstado,cliente_encontrado.idCliente,fechaActual)
            else:
                newIdEstado=4
                cambioEstDao.guardar(newIdEstado,cliente_encontrado.idCliente,fechaActual)
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
                hijoDao.guardar(idEstado,newIdPoliza,hijo.fechaNacimiento,hijo.sexo)       
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
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        try:
            cliente_encontrado = session.query(cliente)\
                .filter_by(
                    idCliente=1040000002
                ).first()
            print(cliente_encontrado.polizas[0].vehiculo.cantSiniestros)
            for poliza in cliente_encontrado.polizas:
                if (poliza.vehiculo.cantSiniestros.cantidad!='Ninguno'):
                    print(cliente_encontrado.polizas[0].vehiculo.cantSiniestros)
                    break
        except Exception as e:    
            print(f"Error en ej////////////////////: {e}")
    
    def guardar_Poliza(self, polizaDTO: polizaDTO, clienteDTO: ClienteDTO):
        gesCliente=GestorCliente()
        polizaDao = polizaDAO()
        modeloDao = modeloDAO()
        factorKmDao = factorKmDAO()
        siniDao=cantSiniestrosDAO()
        estCivilDao=estadoCivilDAO()
        tipoCoberDao=tipoCoberturaDAO()
        medidasDao=medidaDeSeguridadDAO()
        factorUniDao=factorUniDAO()
        localidadDao=localidaDAO()
        provinciaDao=provinciaDAO()
        
        
        # ////////////////////////polizaDao.guardar_poliza(polizaDTO, clienteDTO)/////////////////////////
        
        # inicio de vigencia
       
        fechaInicio = datetime.strptime(polizaDTO.fechaInicioVigencia, '%d/%m/%Y').date()
        
        try:
            
        #/////////////////////////////////////CREAR Y GUARDAR POLIZA////////////////////////////////////////////
        
            try:
                new_poliza=poliza(idCliente=clienteDTO.idCliente, 
                                    idTipoCobertura=polizaDTO.tipoCobertura,
                                    estadoPoliza='Suspendida',
                                    fechaInicio=fechaInicio,
                                    fechaFin=polizaDTO.fechaFinVigencia, 
                                    sumaAsegurada=float(polizaDTO.sumaAsegurada)     
                                )
            except Exception as e:    
                print(f"Error en guardar poliza(poliza): {e}")
                
        #/////////////////////////////////////CREAR Y GUARDAR VEHICULO////////////////////////////////////////////    
           
            try:
                modelo = modeloDao.buscar_modelo(polizaDTO.modeloVehiculo)
                new_idModelo = modelo.idModelo
                new_idFactorKm = factorKmDao.buscar_id(polizaDTO.kilometrosAnio)
                new_idSini= siniDao.buscar_id(polizaDTO.cantSiniestros)
                
                new_poliza.vehiculo=vehiculo(patente=polizaDTO.patente,
                                                idModelo=new_idModelo,
                                                idFactorKm=new_idFactorKm,
                                                idSiniestros=new_idSini,
                                                anioVehiculo=int(polizaDTO.anioVehiculo),
                                                kilometrosAnio=int(polizaDTO.kilometrosAnio),
                                                chasis=polizaDTO.chasis,
                                                motor=polizaDTO.motor
                                            )
            except Exception as e:    
                print(f"Error en guardar poliza(vehiculo): {e}")
        
        #/////////////////////////////////////CREAR Y GUARDAR MEDIDAS////////////////////////////////////////////
                
            try:
                for medida in polizaDTO.medidas:
                    if medida!=0:
                        new_polSeg = poliza_Seguridad(idMedidaSeguridad=medida)
                        new_poliza.poliza_Seguridad.append(new_polSeg)
            except Exception as e:    
                print(f"Error en guardar poliza(medidas): {e}")
        
        #/////////////////////////////////////CREAR Y GUARDAR HIJOS////////////////////////////////////////////
                
            try:
                for listaHijo in polizaDTO.hijos:
                    idEstado=estCivilDao.buscar_id(listaHijo.estadoCivil)
                    new_hijo=hijo(idEstadoCivil=idEstado,
                                    fechaNacimiento=listaHijo.fechaNacimiento,
                                    sexo=listaHijo.sexo)
                    new_poliza.hijo.append(new_hijo)
            except Exception as e:    
                print(f"Error en guardar poliza(hijos): {e}")
        
        #/////////////////////////////////////CREAR Y GUARDAR CUOTAS////////////////////////////////////////////
                
            try:
                cuota_time = fechaInicio - timedelta(days=1)
                new_premio=1000
                new_descuento=100
                new_importe=900
                
                if polizaDTO.formaPago=="Semestral":
                    new_poliza.cuotas=[cuotas(cuotaNro = 1,
                                                fechaVencimiento = cuota_time,
                                                premio = new_premio,
                                                descuento = new_descuento,
                                                importeFinal = new_importe
                                        )]
                    
                elif polizaDTO.formaPago=="Mensual":
                
                    for i in range(1, 7): 
                        new_cuota=cuotas(cuotaNro = i,
                                            fechaVencimiento = cuota_time,
                                            premio = new_premio,
                                            descuento = new_descuento,
                                            importeFinal = (new_importe/6)
                                        )
                        new_poliza.cuotas.append(new_cuota)
                        cuota_time = cuota_time + relativedelta(months=1)  
            except Exception as e:    
                print(f"Error en guardar poliza(cuota): {e}")
            
        #/////////////////////////////////////CREAR Y GUARDAR REGISTRO DE FACTORES////////////////////////////////////////////
            
            try:
                factores=[]
                factores.append(tipoCoberDao.buscarFactor(polizaDTO.tipoCobertura))
                factores.append(siniDao.buscarFactor(polizaDTO.cantSiniestros))
                
                if polizaDTO.medidas[0]==1:
                    factores.append(medidasDao.buscarFactor(polizaDTO.medidas[0]))
                else:
                    factores.append(1)
                if polizaDTO.medidas[1]==2:
                    factores.append(medidasDao.buscarFactor(polizaDTO.medidas[1]))
                else:
                    factores.append(1)
                if polizaDTO.medidas[2]==3:
                    factores.append(medidasDao.buscarFactor(polizaDTO.medidas[2]))
                else:
                    factores.append(1)
                if polizaDTO.medidas[3]==4:
                    factores.append(medidasDao.buscarFactor(polizaDTO.medidas[3]))
                else:
                    factores.append(1)
                
                factores.append(factorUniDao.buscarFactorHijo())
                factores.append(modeloDao.buscarFactor(polizaDTO.modeloVehiculo))
                factores.append(factorKmDao.buscarFactor(polizaDTO.kilometrosAnio))
                factores.append(localidadDao.buscarFactor(polizaDTO.localidad))
                factores.append(provinciaDao.buscarFactor(polizaDTO.provincia))
                
                    
                
                new_poliza.registroFactores=[registroFactores(factorCobertura = factores[0],
                                                                siniestro = factores[1],
                                                                segGarage = factores[2],
                                                                segAlarma = factores[3],
                                                                segRastreo = factores[4],
                                                                segTuerca = factores[5],
                                                                cantHijos = factores[6],
                                                                estRoboModelo = factores[7],
                                                                kilometraje = factores[8],
                                                                riesgoLocalidad = factores[9],
                                                                riesgoProvincia = factores[10] 
                                                            )]
            
            except Exception as e:    
                print(f"Error en guardar poliza(registro factores): {e}")
        
        
                  
        except Exception as e:    
            print(f"Error en guardar poliza: {e}")
           
        try:
            #/////////////////////////////////////--GUARDAR--////////////////////////////////////////////
            
            polizaDao.guardar(new_poliza)
            
            #/////////////////////////////////////--ACTUALIZAR ESTADO--////////////////////////////////////////////
            
            gesCliente.actualizarEstado(clienteDTO)
            
        except Exception as e:
            print(f"Error en guardar poliza(): {e}")
            
    def verificar_datos(self, polizaDTO: polizaDTO):
        gesVehiculo = GestorVehiculo()
        polizaDao = polizaDAO()
        año_actual = datetime.now().year
        diferencia = año_actual - polizaDTO.anioVehiculo
        
        if diferencia > 10 and polizaDTO.tipoCobertura != 1:
            return "Vehiculo con antiguedad mayor a 10 años, solo puede seleccionar cobertura de Responsabilidad Civil"
        else:
            pass
        
        try:
            vehiculos_existente = gesVehiculo.vehiculos_existentes(polizaDTO)
        except Exception as e:
            print(f"Error en verificar_datos() al buscar_vehiculo(): {e}")
        
        if not vehiculos_existente:
            return ""
        else:
            contador = 1
            for lista in vehiculos_existente:
                try:
                    print(f"{lista[0]}")
                except Exception as e:
                    pass
                if lista != []:
                    for vehiculo in lista:
                        poliza_encontrada = polizaDao.comprobar_existencia(vehiculo.idPoliza)
                        if poliza_encontrada is not None:
                            if contador == 1:
                                return "Vehiculo con poliza vigente - Revisar Patente"
                            elif contador == 2:
                                return "Vehiculo con poliza vigente - Revisar Chasis"
                            elif contador == 3:
                                return "Vehiculo con poliza vigente - Revisar Motor"
                        else:
                            pass
                else:
                    contador += 1
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
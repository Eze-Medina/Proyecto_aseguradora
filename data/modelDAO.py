from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine, select, func, insert, desc, and_, asc, or_
from sqlalchemy.sql.functions import coalesce
from model.models import cuotas,cliente, provincia, marca, localidad, modelo, estadoCivil, tipoCobertura, cantSiniestros, poliza, registroFactores, factoresUniversales, vehiculo, cambioEstado, medidaDeSeguridad, tipoCobertura, hijo, poliza_Seguridad, factorKm, tipoDocumento, tipoEstado
from model.modelDTO import ClienteDTO, ProvinciaDTO, MarcaDTO, polizaDTO, hijoDTO
from dateutil.relativedelta import relativedelta

class DAO():
    def prueba(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
       
        resultado = session.query(poliza).filter_by(idPoliza=2).options(joinedload(poliza.vehiculo),\
                                                                        joinedload(poliza.hijo).joinedload(hijo.estadoCivil)).first()
        
        session.close()
        
        return resultado
                
class clienteDAO():
    def listar_clientes(self, clienteDTO: ClienteDTO):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        try:
            query = session.query(cliente).options(joinedload(cliente.tipo_documento), joinedload(cliente.vivienda))
            filtros = []

            if clienteDTO.idCliente:
                filtros.append(cliente.idCliente.like(f"{clienteDTO.idCliente}%"))
            if clienteDTO.numeroDocumento:
                filtros.append(cliente.numeroDocumento.like(f"{clienteDTO.numeroDocumento}%"))
            if clienteDTO.nombre:
                filtros.append(cliente.nombre.like(f"{clienteDTO.nombre}%"))
            if clienteDTO.apellido:
                filtros.append(cliente.apellido.like(f"{clienteDTO.apellido}%"))
            if clienteDTO.tipoDocumento:
                documento = session.query(tipoDocumento).filter_by(tipoDocumento=clienteDTO.tipoDocumento).first()
                if documento:
                    filtros.append(cliente.idDocumento == documento.idDocumento)

            cliente_encontrado = query.filter(and_(*filtros)).all()
            
        except Exception as e:
            print(f"Error en DAO listar_cliente(): {e}")

        session.close()
        return cliente_encontrado

    def buscar_cliente(self, clienteDTO: ClienteDTO):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            cliente_encontrado = session.query(cliente)\
            .filter_by(
                idCliente=clienteDTO.idCliente
            )\
            .options(
                joinedload(cliente.tipo_documento),
                joinedload(cliente.vivienda)
            )\
            .first()
            
        except Exception as e:
            print(f"Error en DAO buscar_cliente(): {e}")

        session.close()
        return cliente_encontrado
    
    def buscar_cliente_completo(self, clienteDTO: ClienteDTO):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            cliente_encontrado = session.query(cliente)\
            .filter_by(
                idCliente=clienteDTO.idCliente
            )\
            .options(
                joinedload(cliente.tipo_documento),
                joinedload(cliente.vivienda),
                joinedload(cliente.polizas).options(
                    joinedload(poliza.vehiculo).joinedload(vehiculo.cantSiniestros),
                    joinedload(poliza.cuotas)
                ),
                joinedload(cliente.cambioEstado).joinedload(cambioEstado.estado)
            )\
            .first()
            
        except Exception as e:
            print(f"Error en DAO buscar_cliente_completo(): {e}")

        session.close()
        return cliente_encontrado
    
    def listar_documentos(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
            
        try:
           documentos = session.query(tipoDocumento).all()
            
        except Exception as e:
            print(f"Error en DAO listar_documentos(): {e}")

        session.close()
        return documentos
     
class cambioEstadoDAO():
    def guardar(self,newIdEstado,newIdCliente,newFecha):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        try:
            nuevo_cambio = cambioEstado(idEstado=newIdEstado,
                                        idCliente=newIdCliente,
                                        fechaCambio=newFecha
                )
            session.add(nuevo_cambio)
            session.commit()
        except Exception as e:
            print(f"Error en DAO guardar() en cambioEstadoDAO: {e}")
        session.close()
        pass
    
class provinciaDAO():
    def listar_provincias(self, provinciaDTO: ProvinciaDTO):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
                
        resultados = session.query(provincia).all()

        if resultados:
            session.close()
            return resultados
        else:
            session.close()
            return None
        
    def buscar_provincia(self, nombProvincia):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            provincia_encontrada = session.query(provincia)\
            .filter_by(
                nombre=nombProvincia
            ).first()
            
        except Exception as e:
            print(f"Error en DAO buscar_provincia(): {e}")

        session.close()
        return provincia_encontrada
    
    def buscarFactor(self, filtro):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            provincia_encontrada = session.query(provincia)\
            .filter_by(
                nombre=filtro
            ).first()
            
        except Exception as e:
            print(f"Error en provinciaDAO buscarFactor(): {e}")

        session.close()
        return provincia_encontrada.riesgoProvincia
    
class marcaDAO():
    def listar_marcas(self, marcaDTO: MarcaDTO):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
                
        resultados = session.query(marca).all()

        if resultados:
            session.close()
            return resultados
        else:
            session.close()
            return None
        
    def buscar_marca(self, nombMarca):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            marca_encontrada = session.query(marca)\
            .filter_by(
                nombre=nombMarca
            ).first()
            
        except Exception as e:
            print(f"Error en DAO buscar_marca(): {e}")

        session.close()
        return marca_encontrada
        
class localidaDAO():
    def listar_localidades(self, provincia):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            localidades_encontradas = session.query(localidad)\
            .filter_by(
                codigoProvincia=provincia
            ).all()
            
        except Exception as e:
            print(f"Error en DAO listar_localidades(): {e}")
        
        session.close()       
        return localidades_encontradas

    def buscarFactor(self, filtro):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            localidad_encontrada = session.query(localidad)\
            .filter_by(
                nombre=filtro
            ).first()
            
        except Exception as e:
            print(f"Error en localidaDAO buscarFactor(): {e}")

        session.close()
        return localidad_encontrada.riesgoLocalidad
    
class modeloDAO():
    def listar_modelos(self, marca):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            modelos_encontrados = session.query(modelo)\
            .filter_by(
                idMarca=marca
            ).all()
            
        except Exception as e:
            print(f"Error en DAO listar_modelos(): {e}")
        
        session.close()       
        return modelos_encontrados
    
    def buscar_modelo(self,txtModelo):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            modelo_encontrado = session.query(modelo)\
            .filter_by(
                nombre=txtModelo
            ).first()
            
        except Exception as e:
            print(f"Error en DAO buscar_modelo(): {e}")
        
        session.close()       
        return modelo_encontrado
    
    def buscarFactor(self,filtro):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            modelo_encontrado = session.query(modelo)\
            .filter_by(
                nombre=filtro
            ).first()
            
        except Exception as e:
            print(f"Error en modeloDAO buscarFactor(): {e}")
        
        session.close()       
        return modelo_encontrado.factorRobo
    
class estadoCivilDAO():
    def listar_estados(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            estados_encontrados = session.query(estadoCivil).all()
            
        except Exception as e:
            print(f"Error en DAO listar_estados(): {e}")
        
        session.close()       
        return estados_encontrados
    
    def buscar_id(self,filtro):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            estado = session.query(estadoCivil).filter_by(estado=filtro).first()
            
        except Exception as e:
            print(f"Error en DAO buscar_id() de estadoCivilDAO: {e}")
        
        session.close()       
        return estado.idEstadoCivil

class cantSiniestrosDAO():
    def listar_siniestros(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            siniestros_encontrados = session.query(cantSiniestros).all()
            
        except Exception as e:
            print(f"Error en DAO listar_siniestros(): {e}")
        
        session.close()       
        return siniestros_encontrados
    
    def buscar_id(self,filtro):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            siniestro_encontrado = session.query(cantSiniestros)\
            .filter_by(
                cantidad=filtro
            ).first()
            
        except Exception as e:
            print(f"Error en DAO buscar_id() en cantSiniestrosDAO: {e}")
        
        session.close()       
        return siniestro_encontrado.idSiniestros
    
    def buscarFactor(self,filtro):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            siniestro_encontrado = session.query(cantSiniestros)\
            .filter_by(
                cantidad=filtro
            ).first()
            
        except Exception as e:
            print(f"Error en DAO buscarFactor() en cantSiniestrosDAO: {e}")
        
        session.close()       
        return siniestro_encontrado.factorSiniestros
              
class hijoDAO():
    def ulimo_id(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            id = session.query(func.max(hijo.idHijo)).scalar()
            if id == None:
                id = 0
        except Exception as e:
            print(f"Error en ulimo_id() en hijoDAO: {e}")

        session.close()
        return id
    
    def guardar(self,newIdEstado,newIdPoliza,newEdad,newSexo):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        try:
            nuevo_hijo = hijo(idEstadoCivil=newIdEstado,
                                idPoliza=newIdPoliza,
                                edad=newEdad,
                                sexo=newSexo
                )
            session.add(nuevo_hijo)
            session.commit()
        except Exception as e:
            print(f"Error en DAO guardar() en hijoDAO: {e}")
        session.close()

class polizaDAO():
    def comprobar_existencia(self, idVehiculo):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        try:
            poliza_encontrada = session.query(poliza)\
                .filter(and_(
                    poliza.idVehiculo == idVehiculo,
                    poliza.estadoPoliza != "Suspendida"
                )).first()
            
            return poliza_encontrada
            
        except Exception as e:
            print(f"Error en polizaDAO comprobar_existencia(): {e}")
    
    def guardar(self,newidCliente,newIdVehiculo,newtipoCobertura,newfechaFinVigencia,newfechaInicio,newsumaAsegurada):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        try:
            nueva_poliza = poliza(idCliente=newidCliente,
                                    idVehiculo=newIdVehiculo,
                                    idTipoCobertura=newtipoCobertura,
                                    estadoPoliza="Suspendida",
                                    fechaInicio=newfechaInicio,
                                    fechaFin=newfechaFinVigencia,
                                    sumaAsegurada=float(newsumaAsegurada)
            )
            session.add(nueva_poliza)
            session.commit()
        except Exception as e:
            print(f"Error en POLIZA(): {e}")
        session.close()
            
    def buscar_poliza(self, filtro):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            poliza_encontrada = session.query(poliza)\
            .filter_by(
                nombre=filtro
            ).first()
            
        except Exception as e:
            print(f"Error en polizaDAO buscar_provincia(): {e}")

        session.close()
        return poliza_encontrada
    
    def ulimo_id(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            id = session.query(func.max(poliza.idPoliza)).scalar()
            if id == None:
                id = 0
        except Exception as e:
            print(f"Error en polizaDAO ulimo_id(): {e}")

        session.close()
        return id
    
class polizaSegDAO():
    def guardar(self,medida,newIdPoliza):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        med=medida
        nIdPoliza=newIdPoliza
        try:
            nuevo_polizaSeg=poliza_Seguridad(idMedidaSeguridad=med,
                                                idPoliza=nIdPoliza,
            )
            session.add(nuevo_polizaSeg)    
            session.commit() 
        except Exception as e:
            print(f"Error en polizaSegDAO guardar(): {e}")
        session.close()
        
    def ulimo_id(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            id = session.query(func.max(poliza_Seguridad.idPolizaSeguridad)).scalar()
            if  id == None:
                id = 0
        except Exception as e:
            print(f"Error en polizaSegDAO ulimo_id(): {e}")

        session.close()
        return id
    
class cuotaDAO():
    def cargarEj(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        cuotas_a_actualizar = session.query(cuotas).filter_by(idPoliza=1040000000001).all()
        
        for i, cuota in enumerate(cuotas_a_actualizar, start=1):
            cuota.idRecibo = i
        session.commit()
        session.close()
        
    def ulimo_id(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            id = session.query(func.max(cuotas.idCuota)).scalar()
            if id == None:
                id = 0
        except Exception as e:
            print(f"Error en cuotaDAO ulimo_id(): {e}")

        session.close()
        return id
    
    def guardar(self,newIdPoliza,newNro,newCuota_time,newDes,newPrim,newImpo):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        try:
            nueva_cuota = cuotas(idPoliza=newIdPoliza,
                                    cuotaNro=newNro,
                                    fechaVencimiento=newCuota_time,
                                    descuento=newDes,
                                    premio=newPrim,
                                    importeFinal=newImpo
                )
            session.add(nueva_cuota)
            session.commit()
        except Exception as e:
            print(f"Error en cuotaDAO guardar(): {e}")
        session.close()

class vehiculoDAO():
    def ulimo_id(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            id = session.query(func.max(vehiculo.idVehiculo)).scalar()
            if id == None:
                id = 0
        except Exception as e:
            print(f"Error en vehiculoDAO ulimo_id(): {e}")

        session.close()
        return id
    
    def guardar(self,newPatente,newIdModelo,newIdSini,newIdFactor,newAnioVehiculo,newKilometrosAnio,newChasis,newMotor):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        try:
            nuevo_vehiculo = vehiculo(patente=newPatente,
                                        idModelo=newIdModelo,
                                        idSiniestros=newIdSini,
                                        idFactorKm=newIdFactor,
                                        anioVehiculo=int(newAnioVehiculo),
                                        kilometrosAnio=int(newKilometrosAnio),
                                        chasis=newChasis,
                                        motor=newMotor
            )
            session.add(nuevo_vehiculo)
            session.commit()
        except Exception as e:
            print(f"Error en vehiculoDAO guardar(): {e}")
        session.close()  
        
    def buscar_vehiculo(self, polizaDTO: polizaDTO):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        vehiculos_encontrados = []

        try:
            query = session.query(vehiculo)

            if polizaDTO.patente:
                vehiculos_patente = query.filter(vehiculo.patente == polizaDTO.patente).all()
                vehiculos_encontrados.append(vehiculos_patente)
            if polizaDTO.motor:
                vehiculos_chasis = query.filter(vehiculo.chasis == polizaDTO.chasis).all()
                vehiculos_encontrados.append(vehiculos_chasis)
            if polizaDTO.chasis:
                vehiculos_motor = query.filter(vehiculo.motor == polizaDTO.motor).all()
                vehiculos_encontrados.append(vehiculos_motor)   
            return vehiculos_encontrados
        except Exception as e:
            print(f"Error en vehiculoDAO buscar_vehiculo(): {e}")
        
class factorKmDAO():
    def buscar_id(self,kilometros):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            factor = session.query(factorKm)\
            .filter(
                factorKm.rango>kilometros
            ).order_by(factorKm.rango).first()   
        except Exception as e:
            print(f"Error en factorKmDAO buscar_id(): {e}")

        session.close()
        return factor.idFactorKm
    
    def buscarFactor(self,filtro):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            factor = session.query(factorKm)\
            .filter(
                factorKm.rango>filtro
            ).order_by(factorKm.rango).first()   
        except Exception as e:
            print(f"Error en factorKmDAO buscarFactor(): {e}")

        session.close()
        return factor.factorKm
    
class registroFactoresDAO():
    def guardar(self,newIdPoliza, newFactorTipo, newFactorSini, newFactorGar, newFactorAla, newFactorRas, newFactorTue, newFactorHijo, newFactorMode, newFactorKilm, newFactorLoca, newFactorProv):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        try:
            nuevo_registro = registroFactores(idPoliza=newIdPoliza,
                                                factorCobertura=newFactorTipo,
                                                siniestro=newFactorSini,
                                                segGarage=newFactorGar,
                                                segAlarma=newFactorAla,
                                                segRastreo=newFactorRas,
                                                segTuerca=newFactorTue,
                                                cantHijos=newFactorHijo,
                                                estRoboModelo=newFactorMode,
                                                kilometraje=newFactorKilm,
                                                riesgoLocalidad=newFactorLoca,
                                                riesgoProvincia=newFactorProv
            )
            session.add(nuevo_registro)
            session.commit()
        except Exception as e:
            print(f"Error en vehiculoDAO guardar(): {e}")
        session.close() 
    
class tipoCoberturaDAO():
    def buscarFactor(self,filtro):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        try:
            factor = session.query(tipoCobertura)\
            .filter(
                tipoCobertura.idTipoCobertura==filtro
            ).first()   
        except Exception as e:
            print(f"Error en tipoCoberturaDAO buscarFactor(): {e}")

        session.close()
        return factor.factorTipo
    
class medidaDeSeguridadDAO():
    def buscarFactor(self,filtro):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        try:
            factor = session.query(medidaDeSeguridad)\
            .filter(
                medidaDeSeguridad.idMedidaSeguridad==filtro
            ).first()   
        except Exception as e:
            print(f"Error en medidaDeSeguridadDAO buscarFactor(): {e}")

        session.close()
        return factor.factorMedida
    
class factorUniDAO():
    def buscarFactorHijo(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        try:
            factor = session.query(factoresUniversales)\
            .filter(
                factoresUniversales.idFactoresUniversales==1
            ).first()   
        except Exception as e:
            print(f"Error en factorUniDAO buscarFactor(): {e}")

        session.close()
        return factor.factorHijo
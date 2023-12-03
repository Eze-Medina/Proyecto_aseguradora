from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine, select, func, insert, desc
from sqlalchemy.sql.functions import coalesce
from model.models import cuotas,cliente, provincia, marca, localidad, modelo, estadoCivil, cantSiniestros, poliza, vehiculo, medidaDeSeguridad, tipoCobertura, hijo, poliza_Seguridad, factorKm, tipoDocumento
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

            filtros = {}
            if clienteDTO.idCliente:
                filtros['idCliente'] = clienteDTO.idCliente
            if clienteDTO.numeroDocumento:
                filtros['numeroDocumento'] = clienteDTO.numeroDocumento
            if clienteDTO.nombre:
                filtros['nombre'] = clienteDTO.nombre
            if clienteDTO.apellido:
                filtros['apellido'] = clienteDTO.apellido
            if clienteDTO.tipoDocumento:
                documento = session.query(tipoDocumento).filter_by(tipoDocumento=clienteDTO.tipoDocumento).first()
                if documento:
                    filtros['idDocumento'] = documento.idDocumento

            cliente_encontrado = query.filter_by(**filtros).all()
            
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
            print(f"Error en prueba(): {e}")

        session.close()
        return cliente_encontrado
    
    def listar_documentos(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
            
        try:
           documentos = session.query(tipoDocumento).all()
            
        except Exception as e:
            print(f"Error en listado de documentos en DAO(): {e}")

        session.close()
        return documentos
        
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
            print(f"Error en prueba(): {e}")

        session.close()
        return provincia_encontrada
    
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
            print(f"Error en prueba(): {e}")

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
            print(f"Error en prueba(): {e}")
        
        session.close()       
        return localidades_encontradas

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
            print(f"Error en prueba(): {e}")
        
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
            print(f"Error en modeloDAO buscar_modelo(): {e}")
        
        session.close()       
        return modelo_encontrado
    
class estadoCivilDAO():
    def listar_estados(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            estados_encontrados = session.query(estadoCivil).all()
            
        except Exception as e:
            print(f"Error en prueba(): {e}")
        
        session.close()       
        return estados_encontrados
    
    def buscar_id(self,filtro):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            estado = session.query(estadoCivil).filter_by(estado=filtro).first()
            
        except Exception as e:
            print(f"Error en prueba(): {e}")
        
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
            print(f"Error en prueba(): {e}")
        
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
            print(f"Error en cantSiniestrosDAO buscar_id(): {e}")
        
        session.close()       
        return siniestro_encontrado.idSiniestros
    
class hijoDAO():
    def ulimo_id(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            id = session.query(func.max(hijo.idHijo)).scalar()
            
        except Exception as e:
            print(f"Error en hijoDAO ulimo_id(): {e}")

        session.close()
        return id
    
    def guardar(self,newIdHijo,newIdEstado,newIdPoliza,newEdad,newSexo):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        try:
            nuevo_hijo = hijo(idHijo=newIdHijo,
                                idEstadoCivil=newIdEstado,
                                idPoliza=newIdPoliza,
                                edad=newEdad,
                                sexo=newSexo
                )
            session.add(nuevo_hijo)
            session.commit()
        except Exception as e:
            print(f"Error en hijoDAO guardar(): {e}")
        session.close()

class polizaDAO():
    
    def guardar(self,newIdPoliza,newidCliente,newIdVehiculo,newtipoCobertura,newfechaFinVigencia,newfechaInicio,newsumaAsegurada):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        try:
            nueva_poliza = poliza(idPoliza=newIdPoliza,
                                    idCliente=newidCliente,
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
            
        except Exception as e:
            print(f"Error en polizaDAO ulimo_id(): {e}")

        session.close()
        return id
    
class polizaSegDAO():
    def guardar(self,medida,newIdPolizaSeg,newIdPoliza):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        med=medida
        nIdPoliza=newIdPoliza
        nIdPolizaSeg=newIdPolizaSeg
        try:
            nuevo_polizaSeg=poliza_Seguridad(idPolizaSeguridad=nIdPolizaSeg,
                                                idMedidaSeguridad=med,
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
            
        except Exception as e:
            print(f"Error en polizaSegDAO ulimo_id(): {e}")

        session.close()
        return id
    
class cuotaDAO():
    def ulimo_id(self):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()

        try:
            id = session.query(func.max(cuotas.idCuota)).scalar()
            
        except Exception as e:
            print(f"Error en cuotaDAO ulimo_id(): {e}")

        session.close()
        return id
    
    def guardar(self,newIdCuota,newIdPoliza,newNro,newCuota_time,newDes,newPrim,newImpo):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        try:
            nueva_cuota = cuotas(idCuota=newIdCuota,
                                    idPoliza=newIdPoliza,
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
            
        except Exception as e:
            print(f"Error en vehiculoDAO ulimo_id(): {e}")

        session.close()
        return id
    
    def guardar(self,newIdVehiculo,newPatente,newIdModelo,newIdSini,newIdFactor,newAnioVehiculo,newKilometrosAnio,newChasis,newMotor):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        try:
            nuevo_vehiculo = vehiculo(patente=newPatente,
                                        idVehiculo=newIdVehiculo,
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
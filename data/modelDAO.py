from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine, select, func, insert
from sqlalchemy.sql.functions import coalesce
from model.models import cuotas,cliente, provincia, marca, localidad, modelo, estadoCivil, cantSiniestros, poliza, vehiculo, medidaDeSeguridad, tipoCobertura, hijo, poliza_Seguridad, factorKm
from model.modelDTO import ClienteDTO, ProvinciaDTO, MarcaDTO, polizaDTO, hijoDTO
from datetime import datetime, timedelta
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
            resultados = session.query(cliente).options(joinedload(cliente.tipo_documento)).all()
        except Exception as e:
            print(f"Error en listarclientesDAO(): {e}") 
        if resultados:
            session.close()
            return resultados
        else:
            session.close()
            return None

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
            print(f"Error en buscar_modelo(): {e}")
        
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
    
class hijoDAO():
    pass

class polizaDAO():
    def guardar_poliza(self, polizaDTO, clienteDTO):
        engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
        Session = sessionmaker(engine)
        session = Session()
        
        # inicio de vigencia
        fechaInicio = datetime.strptime(polizaDTO.fechaInicioVigencia, '%d/%m/%Y').date()
        # identifiacion de los proximos ID
        newIdPoliza = session.query(func.max(poliza.idPoliza)).scalar()
        newIdPoliza += 1
        
        newIdPolizaSeg = session.query(func.max(poliza_Seguridad.idPolizaSeguridad)).scalar()
        newIdPolizaSeg += 1
        
        newIdHijo = session.query(func.max(hijo.idHijo)).scalar()
        newIdHijo += 1
        
        newIdCuota = session.query(func.max(cuotas.idCuota)).scalar()
        newIdCuota += 1
        
        # CREACION DE OBJETOS: POLIZA SEGURIDAD
        try:
            for medida in polizaDTO.medidas:
                nuevo_polizaSeg=poliza_Seguridad(
                    idPolizaSeguridad=newIdPolizaSeg,
                    idMedidaSeguridad=medida,
                    idPoliza=newIdPoliza,
                )
                newIdPolizaSeg += 1
                session.add(nuevo_polizaSeg)    
            session.commit()
        except Exception as e:
            print(f"Error en SEGURIDAD(): {e}")
        
        # CREACION DE OBJETO: POLIZA
        try:
            nueva_poliza = poliza(
                idPoliza=newIdPoliza,
                idCliente=clienteDTO.idCliente,
                patente=polizaDTO.patente,
                idTipoCobertura=polizaDTO.tipoCobertura,
                estadoPoliza="Suspendida",
                fechaInicio=fechaInicio,
                fechaFin=polizaDTO.fechaFinVigencia,
                sumaAsegurada=float(polizaDTO.sumaAsegurada)
            )
            session.add(nueva_poliza)
            session.commit()
        except Exception as e:
            print(f"Error en POLIZA(): {e}")
        
        
        # CREACION DE OBJETO: VEHICULO
        try:
            idModelo = session.query(modelo).filter_by(nombre=polizaDTO.modeloVehiculo).first()
            factoresKM = session.query(factorKm).all()
            for factor in factoresKM:
                if polizaDTO.kilometrosAnio <= factor.rango:
                    idFactor = factor.idFactorKm
                    break
            
            idSini = session.query(cantSiniestros).filter_by(cantidad=polizaDTO.cantSiniestros).first()
            print(idModelo.idModelo)
            nuevo_vehiculo = vehiculo(patente=polizaDTO.patente,
                                    idModelo=idModelo.idModelo,
                                    idSiniestros=idSini.idSiniestros,
                                    idFactorKm=idFactor,
                                    anioVehiculo=int(polizaDTO.anioVehiculo),
                                    kilometrosAnio=int(polizaDTO.kilometrosAnio),
                                    chasis=polizaDTO.chasis,
                                    motor=polizaDTO.motor
            )
            session.add(nuevo_vehiculo)
            session.commit()
        except Exception as e:
            print(f"Error en VEHICULO(): {e}") 
        
        # CREACION DE OBJETOS: HIJO
        try:
            lista_hijos = []

            for datos_hijo in polizaDTO.hijos:
                #nombre_estado_civil = datos_hijo.estadoCivil
                estado_civil = session.query(estadoCivil).filter_by(estado=datos_hijo.estadoCivil).first()
                    
                nuevo_hijo = hijo(
                    idHijo=newIdHijo,
                    idEstadoCivil=estado_civil.idEstadoCivil,
                    idPoliza=newIdPoliza,
                    edad=datos_hijo.edad,
                    sexo=datos_hijo.sexo
                )
                lista_hijos.append(nuevo_hijo)
                newIdHijo += 1
                
            for hijo_instancia in lista_hijos:
                session.add(hijo_instancia)
            session.commit()
        except Exception as e:
            print(f"Error en HIJO(): {e}")        
                
        # CREACION DE OBJETO: CUOTAS
        try:
            fecha_fin_str = polizaDTO.fechaFinVigencia
            cuota_time = fecha_fin_str - timedelta(days=1)
        
            if polizaDTO.formaPago=="Semestral":
                nueva_cuota = cuotas(idCuota=newIdCuota,
                                    idPoliza=newIdPoliza,
                                    cuotaNro=1,
                                    fechaVencimiento=cuota_time,
                                    premio=1000,
                                    importeFinal=2000
                )
                session.add(nueva_cuota)
                
            elif polizaDTO.formaPago=="Mensual":
                
                fecha_inicio_str = polizaDTO.fechaInicioVigencia
                datetime_object = datetime.strptime(fecha_inicio_str, '%d/%m/%Y')

                

                for i in range(1, 7):
                    cuota_time = datetime_object + relativedelta(months=1)
                    
                    nueva_cuota = cuotas(idCuota=newIdCuota,
                                        idPoliza=newIdPoliza,
                                        cuotaNro=i,
                                        fechaVencimiento=cuota_time,
                                        premio=1000,
                                        importeFinal=2000
                    )
                    datetime_object = cuota_time
                    newIdCuota += 1
                    session.add(nueva_cuota)
            
            session.commit()
            
        except Exception as e:
            print(f"Error en CUOTAS(): {e}")
        
        session.close() 
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.models import Base, tipoDocumento, cliente, pais, provincia, localidad, vivienda, marca, modelo, factoresUniversales, cuotas, tipoEstado
from model.models import cantSiniestros, tipoCobertura, medidaDeSeguridad, hijo, poliza, estadoCivil, factorKm, poliza_Seguridad, vehiculo, cambioEstado

engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
    
Session = sessionmaker(engine)
session = Session()
    
if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
try:
    documentos = [
        tipoDocumento( tipoDocumento="DNI", descripcion="Documento Nacional de Identidad"),
        tipoDocumento( tipoDocumento="CI", descripcion="Cédula de Identidad"),
        tipoDocumento( tipoDocumento="Licencia de conducir", descripcion="Licencia de conducir"),
        tipoDocumento( tipoDocumento="Pasaporte", descripcion="Pasaporte")
    ]
    for documento in documentos:
        session.add(documento)

    paices = [
        pais(nombre="Argentina"),
        pais(nombre="Estados Unidos"),
        pais(nombre="Japón"),
        pais(nombre="España"),
        pais(nombre="Corea del Sur")
    ]
    for pais in paices:
        session.add(pais)
        
    provincias = [
        provincia(codigoPais=1,nombre="Santa fe", riesgoProvincia=1.25),
        provincia(codigoPais=1,nombre="Cordoba", riesgoProvincia=1.25),
        provincia(codigoPais=1,nombre="Formosa", riesgoProvincia=1.25),
        provincia(codigoPais=1,nombre="Tierra del Fuego", riesgoProvincia=1.25),
        provincia(codigoPais=1,nombre="Mendoza", riesgoProvincia=1.25),
        provincia(codigoPais=1,nombre="Santiago del Estero", riesgoProvincia=1.25)
    ]
    for provincia in provincias:
        session.add(provincia)

    localidades = [
        localidad(codigoProvincia=1,codigoPostal=3000, nombre="Santa fe", riesgoLocalidad=1.3),
        localidad(codigoProvincia=1,codigoPostal=3000, nombre="Constitución", riesgoLocalidad=1.3),
        localidad(codigoProvincia=1,codigoPostal=3000, nombre="Calamuchita", riesgoLocalidad=1.3),
        localidad(codigoProvincia=2,codigoPostal=3000, nombre="Río Cuarto", riesgoLocalidad=1.3),
        localidad(codigoProvincia=3,codigoPostal=3000, nombre="Formosa", riesgoLocalidad=1.3),
        localidad(codigoProvincia=3,codigoPostal=3000, nombre="Pilcomayo", riesgoLocalidad=1.3),
        localidad(codigoProvincia=4,codigoPostal=3000, nombre="Río Grande", riesgoLocalidad=1.3),
        localidad(codigoProvincia=4,codigoPostal=3000, nombre="Ushuaia", riesgoLocalidad=1.3),
        localidad(codigoProvincia=5,codigoPostal=3000, nombre="Sección Primera", riesgoLocalidad=1.3),
        localidad(codigoProvincia=5,codigoPostal=3000, nombre="Sección Segunda", riesgoLocalidad=1.3),
        localidad(codigoProvincia=6,codigoPostal=3000, nombre="Avellaneda", riesgoLocalidad=1.3),
        localidad(codigoProvincia=6,codigoPostal=3000, nombre="Capital", riesgoLocalidad=1.3),
    ]
    for localidad in localidades:
        session.add(localidad)

    viviendas = [
        vivienda(codigoLocalidad=1, calle="Las heras", numero=7460, piso=0, depto=0),
        vivienda(codigoLocalidad=2, calle="Francia", numero=2222, piso=0, depto=0),
        vivienda(codigoLocalidad=3, calle="San Jeronimo", numero=4891, piso=0, depto=0),
        vivienda(codigoLocalidad=4, calle="Las Ramblas", numero=4174, piso=0, depto=0),
        vivienda(codigoLocalidad=5, calle="Primera Junta", numero=1547, piso=0, depto=0),
        vivienda(codigoLocalidad=6, calle="Rivadavia", numero=2347, piso=0, depto=0),
        vivienda(codigoLocalidad=7, calle="Cordoba", numero=6577, piso=0, depto=0),
        vivienda(codigoLocalidad=8, calle="J.J Paso", numero=8977, piso=0, depto=0),
        vivienda(codigoLocalidad=11, calle="Galicia", numero=5641, piso=0, depto=0),
    ]
    for vivienda in viviendas:
        session.add(vivienda)

    clientes = [
        cliente(nombre='admin',apellido="admin",idCliente=1040000000,idVivienda=1,idDocumento=1,numeroDocumento=99999999),
        cliente(nombre="Ezequiel", apellido="Medina", idVivienda=1, idDocumento=1, numeroDocumento=41940644),
        cliente(nombre="Agustin", apellido="Medina", idVivienda=1, idDocumento=1, numeroDocumento=40646933),
        cliente(nombre="Marta", apellido="García", idVivienda=2, idDocumento=2, numeroDocumento=42345678),
        cliente(nombre="Carlos", apellido="López", idVivienda=3, idDocumento=1, numeroDocumento=48765432),
        cliente(nombre="Laura", apellido="González", idVivienda=4, idDocumento=1, numeroDocumento=44321678),
        cliente(nombre="Andrés", apellido="Sánchez", idVivienda=6, idDocumento=3, numeroDocumento=47654321),
        cliente(nombre="Sofía", apellido="Ramírez", idVivienda=7, idDocumento=1, numeroDocumento=44567812),
        cliente(nombre="Juan", apellido="Chayanne", idVivienda=8, idDocumento=1, numeroDocumento=45432187),
        cliente(nombre="Luca", apellido="Polola", idVivienda=9, idDocumento=4, numeroDocumento=45764887),
        cliente(nombre="Luismi", apellido="Amor", idVivienda=9, idDocumento=4, numeroDocumento=45778414),
        cliente(nombre="Nicolas", apellido="Edche", idVivienda=2, idDocumento=1, numeroDocumento=45432535),
        cliente(nombre="Ana", apellido="Dubois", idVivienda=6, idDocumento=1, numeroDocumento=45947644),
        cliente(nombre="Finn", apellido="Kim", idVivienda=9, idDocumento=1, numeroDocumento=31900784),
        cliente(nombre="Javier", apellido="López", idVivienda=7, idDocumento=1, numeroDocumento=70944764),
        cliente(nombre="Diego", apellido="Alves", idVivienda=3, idDocumento=1, numeroDocumento=32450644),
        cliente(nombre="Valentina", apellido="Patel", idVivienda=8, idDocumento=1, numeroDocumento=38940684),
        cliente(nombre="Juana", apellido="Alvarez", idVivienda=7, idDocumento=1, numeroDocumento=45715491),
        cliente(nombre="Lucia", apellido="Chang", idVivienda=6, idDocumento=1, numeroDocumento=40731845),
    ]
    for cliente in clientes:
        session.add(cliente)

    marcas = [
        marca(nombre="BMW"),
        marca(nombre="Audi"),
        marca(nombre="Ford"),
        marca(nombre="Mercedes Benz"),
        marca(nombre="Nissan"),
        marca(nombre="Suzuki"),
        marca(nombre="Toyota"),
        marca(nombre="Chevrolet"),
        marca(nombre="Subaru"),
        marca(nombre="Jeep"),
    ]
    for marca in marcas:
        session.add(marca)

    modelos = [
        modelo(idMarca=3, nombre="Bronco Sport",factorRobo=1.1,inicioProduccion=datetime(2014, 1, 1),finProduccion=datetime(2023, 1, 1)),
        modelo(idMarca=3, nombre="F-150 Raptor",factorRobo=1.1,inicioProduccion=datetime(2018, 1, 1),finProduccion=datetime(2023, 1, 1)),
        modelo(idMarca=3, nombre="Mustang",factorRobo=1.1,inicioProduccion=datetime(2009, 1, 1),finProduccion=datetime(2023, 1, 1)),
        modelo(idMarca=1, nombre="M5 Sedán",factorRobo=1.1,inicioProduccion=datetime(2019, 1, 1),finProduccion=datetime(2023, 1, 1)),
        modelo(idMarca=1, nombre="X3 M",factorRobo=1.1,inicioProduccion=datetime(2021, 1, 1),finProduccion=datetime(2023, 1, 1)),
    ]
    for mod in modelos:
        session.add(mod)

    estados = [
        estadoCivil(estado="Soltero/a"),
        estadoCivil(estado="Casado/a"),
        estadoCivil(estado="Divorciado/a"),
        estadoCivil(estado="Viudo/a")
    ]
    for estado in estados:
        session.add(estado)
    
    tipoEstados=[
        tipoEstado(tipoEstado="Inactivo"),
        tipoEstado(tipoEstado="Activo"),
        tipoEstado(tipoEstado="Normal"),
        tipoEstado(tipoEstado="Platino")
    ]   
    for estado in tipoEstados:
        session.add(estado)
         
    cantidades = [
        cantSiniestros(cantidad="Ninguno",factorSiniestros=1),
        cantSiniestros(cantidad="Uno",factorSiniestros=1.2),
        cantSiniestros(cantidad="Dos",factorSiniestros=1.4),
        cantSiniestros(cantidad="Más de dos",factorSiniestros=2)
    ]
    for cantidad in cantidades:
        session.add(cantidad)
        
    tipoCoberturas = [
        tipoCobertura(tipoCobertura="Responsabilidad Civil",descripcion="",factorTipo=1.5),
        tipoCobertura(tipoCobertura="Resp. Civil, Robo o incendio total",descripcion="",factorTipo=1.5),
        tipoCobertura(tipoCobertura="Todo total",descripcion="",factorTipo=1.5),
        tipoCobertura(tipoCobertura="Terceros Completos",descripcion="",factorTipo=1.5),
        tipoCobertura(tipoCobertura="Todo Riesgo con Franquicia",descripcion="",factorTipo=1.5)
    ]    
    for tipoCobertura in tipoCoberturas:
        session.add(tipoCobertura)
        
    medidasDeSeguridad = [
        medidaDeSeguridad(medida="¿Se guarda en garaje?", descripcion="", factorMedida=1.45),
        medidaDeSeguridad(medida="¿Tiene alarma?", descripcion="", factorMedida=1.45),
        medidaDeSeguridad(medida="¿Posee dispostivo de rastreo vehicular?", descripcion="", factorMedida=1.45),
        medidaDeSeguridad(medida="¿Posee tuercas antirrobo en las cuatro ruedas?", descripcion="", factorMedida=1.45)
    ]
    for medidaDeSeguridad in medidasDeSeguridad:
        session.add(medidaDeSeguridad)

    factorkms = [
        factorKm(rango= 10000, factorKm=1.1),
        factorKm(rango= 20000, factorKm=1.2),
        factorKm(rango= 30000, factorKm=1.3),
        factorKm(rango= 40000, factorKm=1.4),
        factorKm(rango= 50000, factorKm=1.5)
    ]    
    for factor in factorkms:
        session.add(factor)
        
    factorUni = [
        factoresUniversales(idFactoresUniversales=1, factorDerechoEmision= 1.1, factorDescuentoUnidadAd=1.1, factorHijo=1.05)
    ]    
    for factor in factorUni:
        session.add(factor)

    cambios = [
        cambioEstado(idEstado= 2, idCliente=1040000001, fechaCambio=datetime(year=2020, month=6, day=20)),
        cambioEstado(idEstado= 2, idCliente=1040000001, fechaCambio=datetime(year=2022, month=12, day=20))
    ]    
    for cambio in cambios:
        session.add(cambio)
        
    polizas = [
        poliza(idPoliza= 1040000000000, 
               idCliente=1040000000, 
               idTipoCobertura=3, 
               idVehiculo=1, 
               estadoPoliza='Suspendida',
               fechaInicio=datetime(year=2023, month=6, day=20),
               fechaFin=datetime(year=2023, month=12, day=20), 
               sumaAsegurada=15000     
        )
    ]    
    for poli in polizas:
        session.add(poli)
        
    vehiculos=[
        vehiculo(idVehiculo=1,
                 patente='ADM MIN',
                 idModelo=1,
                 idFactorKm=1,
                 idSiniestros=1,
                 anioVehiculo=2020,
                 kilometrosAnio=5000,
                 chasis='ADM',
                 motor='MIN'  
        )
    ]
    for vehi in vehiculos:
        session.add(vehi)
        
except Exception as e:
            print(f"Error en carga de datosBase: {e}")
            
session.commit()
session.close()
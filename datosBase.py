from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.models import Base, tipoDocumento, cliente, pais, provincia, localidad, vivienda, marca, modelo, factoresUniversales, cuotas
from model.models import cantSiniestros, tipoCobertura, medidaDeSeguridad, hijo, poliza, estadoCivil, factorKm, poliza_Seguridad, vehiculo

engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
    
Session = sessionmaker(engine)
session = Session()
    
if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
try:
    documentos = [
        tipoDocumento(idDocumento=1, tipoDocumento="DNI", descripcion="Documento Nacional de Identidad"),
        tipoDocumento(idDocumento=2, tipoDocumento="CI", descripcion="Cédula de Identidad"),
        tipoDocumento(idDocumento=3, tipoDocumento="Licencia de conducir", descripcion="Licencia de conducir"),
        tipoDocumento(idDocumento=4, tipoDocumento="Pasaporte", descripcion="Pasaporte")
    ]
    for documento in documentos:
        session.add(documento)

    paices = [
        pais(codigoPais=1, nombre="Argentina"),
        pais(codigoPais=2, nombre="Estados Unidos"),
        pais(codigoPais=3, nombre="Japón"),
        pais(codigoPais=4, nombre="España"),
        pais(codigoPais=5, nombre="Corea del Sur")
    ]
    for pais in paices:
        session.add(pais)
        
    provincias = [
        provincia(codigoProvincia=21, codigoPais=1,nombre="Santa fe", riesgoProvincia=1.25),
        provincia(codigoProvincia=70, codigoPais=1,nombre="Cordoba", riesgoProvincia=1.25),
        provincia(codigoProvincia=34, codigoPais=1,nombre="Formosa", riesgoProvincia=1.25),
        provincia(codigoProvincia=98, codigoPais=1,nombre="Tierra del Fuego", riesgoProvincia=1.25),
        provincia(codigoProvincia=23, codigoPais=1,nombre="Mendoza", riesgoProvincia=1.25),
        provincia(codigoProvincia=15, codigoPais=1,nombre="Santiago del Estero", riesgoProvincia=1.25)
    ]
    for provincia in provincias:
        session.add(provincia)

    localidades = [
        localidad(codigoLocalidad=98, codigoProvincia=21,codigoPostal=3000, nombre="Santa fe", riesgoLocalidad=1.3),
        localidad(codigoLocalidad=32, codigoProvincia=21,codigoPostal=3000, nombre="Constitución", riesgoLocalidad=1.3),
        localidad(codigoLocalidad=65, codigoProvincia=21,codigoPostal=3000, nombre="Calamuchita", riesgoLocalidad=1.3),
        localidad(codigoLocalidad=87, codigoProvincia=70,codigoPostal=3000, nombre="Río Cuarto", riesgoLocalidad=1.3),
        localidad(codigoLocalidad=81, codigoProvincia=34,codigoPostal=3000, nombre="Formosa", riesgoLocalidad=1.3),
        localidad(codigoLocalidad=13, codigoProvincia=34,codigoPostal=3000, nombre="Pilcomayo", riesgoLocalidad=1.3),
        localidad(codigoLocalidad=16, codigoProvincia=98,codigoPostal=3000, nombre="Río Grande", riesgoLocalidad=1.3),
        localidad(codigoLocalidad=30, codigoProvincia=98,codigoPostal=3000, nombre="Ushuaia", riesgoLocalidad=1.3),
        localidad(codigoLocalidad=64, codigoProvincia=23,codigoPostal=3000, nombre="Sección Primera", riesgoLocalidad=1.3),
        localidad(codigoLocalidad=89, codigoProvincia=23,codigoPostal=3000, nombre="Sección Segunda", riesgoLocalidad=1.3),
        localidad(codigoLocalidad=27, codigoProvincia=15,codigoPostal=3000, nombre="Avellaneda", riesgoLocalidad=1.3),
        localidad(codigoLocalidad=78, codigoProvincia=15,codigoPostal=3000, nombre="Capital", riesgoLocalidad=1.3),
    ]
    for localidad in localidades:
        session.add(localidad)

    viviendas = [
        vivienda(idVivienda=423, codigoLocalidad=98, calle="Las heras", numero=7460, piso=0, depto=0),
        vivienda(idVivienda=165, codigoLocalidad=32, calle="Francia", numero=2222, piso=0, depto=0),
        vivienda(idVivienda=123, codigoLocalidad=65, calle="San Jeronimo", numero=4891, piso=0, depto=0),
        vivienda(idVivienda=784, codigoLocalidad=87, calle="Las Ramblas", numero=4174, piso=0, depto=0),
        vivienda(idVivienda=745, codigoLocalidad=81, calle="Primera Junta", numero=1547, piso=0, depto=0),
        vivienda(idVivienda=889, codigoLocalidad=13, calle="Rivadavia", numero=2347, piso=0, depto=0),
        vivienda(idVivienda=874, codigoLocalidad=16, calle="Cordoba", numero=6577, piso=0, depto=0),
        vivienda(idVivienda=324, codigoLocalidad=30, calle="J.J Paso", numero=8977, piso=0, depto=0),
        vivienda(idVivienda=453, codigoLocalidad=27, calle="Galicia", numero=5641, piso=0, depto=0),
    ]
    for vivienda in viviendas:
        session.add(vivienda)

    clientes = [
        cliente(idCliente=1, nombre="Ezequiel", apellido="Medina", idVivienda=423, idDocumento=1, numeroDocumento=41940644),
        cliente(idCliente=2, nombre="Agustin", apellido="Medina", idVivienda=423, idDocumento=1, numeroDocumento=40646933),
        cliente(idCliente=3, nombre="Marta", apellido="García", idVivienda=165, idDocumento=2, numeroDocumento=42345678),
        cliente(idCliente=4, nombre="Carlos", apellido="López", idVivienda=123, idDocumento=1, numeroDocumento=48765432),
        cliente(idCliente=5, nombre="Laura", apellido="González", idVivienda=784, idDocumento=1, numeroDocumento=44321678),
        cliente(idCliente=6, nombre="Andrés", apellido="Sánchez", idVivienda=745, idDocumento=3, numeroDocumento=47654321),
        cliente(idCliente=7, nombre="Sofía", apellido="Ramírez", idVivienda=889, idDocumento=1, numeroDocumento=44567812),
        cliente(idCliente=8, nombre="Juan", apellido="Chayanne", idVivienda=874, idDocumento=1, numeroDocumento=45432187),
        cliente(idCliente=9, nombre="Luca", apellido="Polola", idVivienda=324, idDocumento=4, numeroDocumento=45764887),
        cliente(idCliente=10, nombre="Luismi", apellido="Amor", idVivienda=324, idDocumento=4, numeroDocumento=45778414),
        cliente(idCliente=11, nombre="Nicolas", apellido="Edche", idVivienda=165, idDocumento=1, numeroDocumento=45432535),
        cliente(idCliente=12, nombre="Ana", apellido="Dubois", idVivienda=745, idDocumento=1, numeroDocumento=45947644),
        cliente(idCliente=13, nombre="Finn", apellido="Kim", idVivienda=324, idDocumento=1, numeroDocumento=31900784),
        cliente(idCliente=14, nombre="Javier", apellido="López", idVivienda=889, idDocumento=1, numeroDocumento=70944764),
        cliente(idCliente=15, nombre="Diego", apellido="Alves", idVivienda=123, idDocumento=1, numeroDocumento=32450644),
        cliente(idCliente=16, nombre="Valentina", apellido="Patel", idVivienda=874, idDocumento=1, numeroDocumento=38940684),
        cliente(idCliente=17, nombre="Juana", apellido="Alvarez", idVivienda=889, idDocumento=1, numeroDocumento=45715491),
        cliente(idCliente=18, nombre="Lucia", apellido="Chang", idVivienda=745, idDocumento=1, numeroDocumento=40731845),
    ]
    for cliente in clientes:
        session.add(cliente)

    marcas = [
        marca(idMarca=1, nombre="BMW"),
        marca(idMarca=2, nombre="Audi"),
        marca(idMarca=3, nombre="Ford"),
        marca(idMarca=4, nombre="Mercedes Benz"),
        marca(idMarca=5, nombre="Nissan"),
        marca(idMarca=6, nombre="Suzuki"),
        marca(idMarca=7, nombre="Toyota"),
        marca(idMarca=8, nombre="Chevrolet"),
        marca(idMarca=9, nombre="Subaru"),
        marca(idMarca=10, nombre="Jeep"),
    ]
    for marca in marcas:
        session.add(marca)

    modelos = [
        modelo(idModelo=1,idMarca=3, nombre="Bronco Sport",factorRobo=1.1,inicioProduccion=datetime(2014, 1, 1),finProduccion=datetime(2023, 1, 1)),
        modelo(idModelo=2,idMarca=3, nombre="F-150 Raptor",factorRobo=1.1,inicioProduccion=datetime(2018, 1, 1),finProduccion=datetime(2023, 1, 1)),
        modelo(idModelo=3,idMarca=3, nombre="Mustang",factorRobo=1.1,inicioProduccion=datetime(2009, 1, 1),finProduccion=datetime(2023, 1, 1)),
        modelo(idModelo=4,idMarca=1, nombre="M5 Sedán",factorRobo=1.1,inicioProduccion=datetime(2019, 1, 1),finProduccion=datetime(2023, 1, 1)),
        modelo(idModelo=5,idMarca=1, nombre="X3 M",factorRobo=1.1,inicioProduccion=datetime(2021, 1, 1),finProduccion=datetime(2023, 1, 1)),
    ]
    for mod in modelos:
        session.add(mod)

    estados = [
        estadoCivil(idEstadoCivil=1,estado="Soltero/a"),
        estadoCivil(idEstadoCivil=2,estado="Casado/a"),
        estadoCivil(idEstadoCivil=3,estado="Divorciado/a"),
        estadoCivil(idEstadoCivil=4,estado="Viudo/a")
    ]
    for estado in estados:
        session.add(estado)
        
    cantidades = [
        cantSiniestros(idSiniestros=1,cantidad="Ninguno",factorSiniestros=1),
        cantSiniestros(idSiniestros=2,cantidad="Uno",factorSiniestros=1.2),
        cantSiniestros(idSiniestros=3,cantidad="Dos",factorSiniestros=1.4),
        cantSiniestros(idSiniestros=4,cantidad="Más de dos",factorSiniestros=2)
    ]
    for cantidad in cantidades:
        session.add(cantidad)
        
    tipoCoberturas = [
        tipoCobertura(idTipoCobertura=1, tipoCobertura="   Responsabilidad Civil",descripcion="",factorTipo=1.5),
        tipoCobertura(idTipoCobertura=2, tipoCobertura="   Resp. Civil, Robo o incendio total",descripcion="",factorTipo=1.5),
        tipoCobertura(idTipoCobertura=3, tipoCobertura="   Todo total",descripcion="",factorTipo=1.5),
        tipoCobertura(idTipoCobertura=4, tipoCobertura="   Terceros Completos",descripcion="",factorTipo=1.5),
        tipoCobertura(idTipoCobertura=5, tipoCobertura="   Todo Riesgo con Franquicia",descripcion="",factorTipo=1.5)
    ]    
    for tipoCobertura in tipoCoberturas:
        session.add(tipoCobertura)
        
    medidasDeSeguridad = [
        medidaDeSeguridad(idMedidaSeguridad=1, medida="¿Se guarda en garaje?", descripcion="", factorMedida=1.45),
        medidaDeSeguridad(idMedidaSeguridad=2, medida="¿Tiene alarma?", descripcion="", factorMedida=1.45),
        medidaDeSeguridad(idMedidaSeguridad=3, medida="¿Posee dispostivo de rastreo vehicular?", descripcion="", factorMedida=1.45),
        medidaDeSeguridad(idMedidaSeguridad=4, medida="¿Posee tuercas antirrobo en las cuatro ruedas?", descripcion="", factorMedida=1.45)
    ]
    for medidaDeSeguridad in medidasDeSeguridad:
        session.add(medidaDeSeguridad)

    factorkms = [
        factorKm(idFactorKm=1, rango= 10000, factorKm=1.1),
        factorKm(idFactorKm=2, rango= 20000, factorKm=1.2),
        factorKm(idFactorKm=3, rango= 30000, factorKm=1.3),
        factorKm(idFactorKm=4, rango= 40000, factorKm=1.4),
        factorKm(idFactorKm=5, rango= 50000, factorKm=1.5)
    ]    
    for factor in factorkms:
        session.add(factor)
        
    factorUni = [
        factoresUniversales(idFactoresUniversales=1, factorDerechoEmision= 1.1, factorDescuentoUnidadAd=1.1, factorHijo=1.05)
    ]    
    for factor in factorUni:
        session.add(factor)
        
    poliza_base=poliza(idPoliza=0)
    session.add(poliza_base)  
   
    hijo_base=hijo(idHijo=0)
    session.add(hijo_base) 
    
    vehiculo_base=vehiculo(idVehiculo=0)
    session.add(vehiculo_base) 
    
    poliza_base=poliza_Seguridad(idPolizaSeguridad=0)
    session.add(poliza_base)
    
    cuota_base=cuotas(idCuota=0)
    session.add(cuota_base)

except Exception as e:
            print(f"Error en carga de datosBase: {e}")
            
session.commit()
session.close()
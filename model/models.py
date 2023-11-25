from sqlalchemy import Column, Integer, String, DateTime, Float, Time, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///datosAseguradora.db', echo=True)
Session = sessionmaker(engine)
session = Session()

class Base(DeclarativeBase):
    pass

class poliza(Base):
    __tablename__ = 'poliza'
    
    idPoliza = Column(Integer(),primary_key=True)
    idCliente = Column(Integer, ForeignKey('cliente.idCliente'))
    idTipoCobertura = Column(Integer, ForeignKey('tipoCobertura.idTipoCobertura'))
    patente = Column(Integer, ForeignKey('vehiculo.patente'))
    estadoPoliza = Column(String(50))
    fechaInicio = Column(DateTime())
    fechaFin = Column(DateTime())
    importeOriginar = Column(Float())
    sumaAsegurada = Column(Float())
    
    def __str__(self):
        return f"Poliza: {self.idPoliza} {self.idCliente}"
    
    cliente = relationship('cliente', back_populates='polizas')
    vehiculo = relationship('vehiculo')
    cuotas = relationship('cuotas')
    hijo = relationship('hijo')
    tipoCobertura = relationship('tipoCobertura')
    registroFactores = relationship('registroFactores')
    poliza_Seguridad = relationship("poliza_Seguridad", back_populates="polizas")


class cuotas(Base):
    __tablename__ = 'cuotas'
    
    idCuota = Column(Integer(),primary_key=True)
    idPoliza = Column(Integer, ForeignKey('poliza.idPoliza'))
    idRecibo = Column(Integer, ForeignKey('recibo.idRecibo'))
    cuotaNro = Column(Integer)
    fechaVencimiento = Column(DateTime())
    fechaPago = Column(DateTime())
    premio = Column(Float())
    descuento = Column(Float())
    importeFinal = Column(Float())
    
    def __str__(self):
        return self.idCuota


class recibo(Base):
    __tablename__ = 'recibo'
    
    idRecibo = Column(Integer(),primary_key=True)
    fechaPago = Column(DateTime())
    horaPago = Column(Time())
    premio = Column(Float())
    recargo = Column(Float())
    descuento = Column(Float())
    anioAbonado = Column(Integer)
    operador = Column(String(50))
    
    def __str__(self):
        return self.idRecibo
    
    cuotas = relationship('cuotas')


class mesAbonado(Base):
    __tablename__ = 'mesAbonado'
    
    idMesAbonado = Column(Integer(),primary_key=True)
    mesAbonado = Column(DateTime())
    idRecibo = Column(Integer)
    
    def __str__(self):
        return self.idRecibo


class registroFactores(Base):
    __tablename__ = 'registroFactores'
    
    idRegistro = Column(Integer(),primary_key=True)
    idPoliza = Column(Integer, ForeignKey('poliza.idPoliza'))
    factorCobertura = Column(Integer)
    siniestro = Column(Integer)
    segGarage = Column(Integer)
    segAlarma = Column(Integer)
    segRastreo = Column(Integer)
    segTuerca = Column(Integer)
    cantHijos = Column(Integer)
    estRoboModelo = Column(Integer)
    estRoboMarca = Column(Integer)
    riesgoLocalidad = Column(Integer)
    kilometraje = Column(Integer)

    def __str__(self):
        return self.idRegistro
    
    poliza = relationship('poliza', back_populates='registroFactores')


class cliente(Base):
    __tablename__ = 'cliente'

    idCliente = Column(Integer, primary_key=True)
    idDocumento = Column(Integer, ForeignKey('tipoDocumento.idDocumento'))
    idVivienda = Column(Integer, ForeignKey('vivienda.idVivienda'))
    numeroDocumento = Column(Integer)
    nombre = Column(String(50))
    apellido = Column(String(50))
    estadoCliente = Column(String(50))
    anioRegistro = Column(String(50))

    def __str__(self):
        return f"Cliente: {self.nombre} {self.apellido}"
    
    vivienda = relationship("vivienda")
    tipo_documento = relationship("tipoDocumento")
    polizas = relationship("poliza", back_populates="cliente")

class tipoDocumento(Base):
    __tablename__ = 'tipoDocumento'
    
    idDocumento = Column(Integer(),primary_key=True)
    tipoDocumento = Column(String(50))
    descripcion = Column(String(50))
    
    def __str__(self):
        return self.idDocumento

class pais(Base):
    __tablename__ = 'pais'
    
    codigoPais = Column(Integer(),primary_key=True)
    nombre = Column(String(50))

    def __str__(self):
        return self.codigoPais


class provincia(Base):
    __tablename__ = 'provincia'
    
    codigoProvincia = Column(Integer(),primary_key=True)
    codigoPais = Column(Integer, ForeignKey('pais.codigoPais'))
    nombre = Column(String(50))
    riesgoProvincia = Column(Float())

    def __str__(self):
        return self.codigoProvincia
    
    pais = relationship("pais")


class localidad(Base):
    __tablename__ = 'localidad'
    
    codigoLocalidad = Column(Integer(),primary_key=True)
    codigoProvincia = Column(Integer, ForeignKey('provincia.codigoProvincia'))
    codigoPostal = Column(Integer)
    nombre = Column(String(50))
    riesgoLocalidad = Column(Integer)
    
    def __str__(self):
        return self.codigoLocalidad
    
    provincia = relationship("provincia")


class vivienda(Base):
    __tablename__ = 'vivienda'
    
    idVivienda = Column(Integer(),primary_key=True)
    
    codigoLocalidad = Column(Integer, ForeignKey('localidad.codigoLocalidad'))
    calle = Column(String(50))
    numero = Column(Integer)
    piso = Column(Integer)
    depto = Column(Integer)

    def __str__(self):
        return self.idVivienda

    localidad = relationship("localidad")
    
    
class poliza_Seguridad(Base):
    __tablename__ = 'poliza_Seguridad'
    
    
    idPolizaSeguridad = Column(Integer(), primary_key=True)
    idPoliza = Column(Integer(), ForeignKey('poliza.idPoliza'))
    idMedidaSeguridad = Column(Integer(), ForeignKey('medidaDeSeguridad.idMedidaSeguridad'))
    
    def __str__(self):
        return self.idPolizaSeguridad
    
    polizas = relationship("poliza", back_populates="poliza_Seguridad")
    medidasDeSeguridad = relationship("medidaDeSeguridad", back_populates="poliza_Seguridad")
    
    
class medidaDeSeguridad(Base):
    __tablename__ = 'medidaDeSeguridad'
    
    idMedidaSeguridad = Column(Integer(),primary_key=True)
    descripcion = Column(String(50))
    medida = Column(String(50))
    factorMedida = Column(Integer)

    def __str__(self):
        return f"Poliza: {self.medida}"
    
    poliza_Seguridad = relationship("poliza_Seguridad", back_populates="medidasDeSeguridad")
    registro_Seguridad = relationship("registro_Seguridad", back_populates="medidasDeSeguridad")
    
class registro_Seguridad(Base):
    __tablename__ = 'registro_Seguridad'
    
    idRegistroSeguridad = Column(Integer(), primary_key=True)
    idRegistroCambios = Column(Integer(), ForeignKey('registroCambiosPoliza.idRegistroCambios'))
    idMedidaSeguridad = Column(Integer(), ForeignKey('medidaDeSeguridad.idMedidaSeguridad'))
    
    def __str__(self):
        return self.idPolizaSeguridad
    
    registroCambiosPoliza = relationship("registroCambiosPoliza", back_populates="registros_Seguridad")
    medidasDeSeguridad = relationship("medidaDeSeguridad", back_populates="registro_Seguridad")
  
class registroCambiosPoliza(Base):
    __tablename__ = 'registroCambiosPoliza'
    
    idRegistroCambios = Column(Integer(),primary_key=True)
    patente = Column(Integer, ForeignKey('vehiculo.patente'))
    idTipoCobertura = Column(Integer, ForeignKey('tipoCobertura.idTipoCobertura'))
    anioVehiculo = Column(Integer)
    nroSiniestros = Column(Integer)
    kmAnual = Column(Integer)
    motor = Column(String(50))
    
    def __str__(self):
        return self.idRegistroCambios 
    
    vehiculo = relationship("vehiculo", back_populates="registroCambiosPoliza") 
    registros_Seguridad = relationship("registro_Seguridad", back_populates="registroCambiosPoliza")
    hijos = relationship("hijo", back_populates="registroCambiosPoliza")
    tiposCobertura = relationship("tipoCobertura", back_populates="registroCambiosPoliza")

class hijo(Base):
    __tablename__ = 'hijo'
    
    idHijo = Column(Integer(),primary_key=True)
    idEstadoCivil = Column(Integer, ForeignKey('estadoCivil.idEstadoCivil'))
    idRegistroCambios = Column(Integer, ForeignKey('registroCambiosPoliza.idRegistroCambios'))
    idPoliza = Column(Integer, ForeignKey('poliza.idPoliza'))
    edad = Column(Integer)
    sexo = Column(String(50))

    def __str__(self):
        return f"Hijo: {self.sexo}"
    
    estadoCivil = relationship("estadoCivil") 
    registroCambiosPoliza = relationship("registroCambiosPoliza", back_populates="hijos")  


class estadoCivil(Base):
    __tablename__ = 'estadoCivil'
    
    idEstadoCivil = Column(Integer(),primary_key=True)
    estado = Column(String(50))

    def __str__(self):
        return f"Estado: {self.estado}"


class tipoCobertura(Base):
    __tablename__ = 'tipoCobertura'
    
    idTipoCobertura = Column(Integer(),primary_key=True)
    tipoCobertura = Column(String(50))
    descripcion = Column(String(50))
    factorTipo = Column(Integer)

    def __str__(self):
        return self.idTipoCobertura
    
    registroCambiosPoliza = relationship("registroCambiosPoliza", back_populates="tiposCobertura")


class vehiculo(Base):
    __tablename__ = 'vehiculo'
    
    patente = Column(String(50),primary_key=True)
    idModelo = Column(Integer, ForeignKey('modelo.idModelo'))
    idFactorKm = Column(Integer, ForeignKey('factorKm.idFactorKm'))
    idSiniestros = Column(Integer, ForeignKey('cantSiniestros.idSiniestros'))
    anioVehiculo = Column(Integer)
    kilometrosAnio = Column(Integer)
    chasis = Column(String(50))
    motor = Column(String(50))

    def __str__(self):
        return f"Vehiculo: {self.patente}"
    
    modelo = relationship("modelo")
    registroCambiosPoliza = relationship("registroCambiosPoliza", back_populates="vehiculo") 
    factorKm = relationship("factorKm") 
    cantSiniestros = relationship("cantSiniestros") 


class marca(Base):
    __tablename__ = 'marca'
    
    idMarca = Column(Integer(),primary_key=True)
    nombre = Column(String(50))

    def __str__(self):
        return self.idMarca


class modelo(Base):
    __tablename__ = 'modelo'
    
    idModelo = Column(Integer(),primary_key=True)
    idMarca = Column(Integer, ForeignKey('marca.idMarca'))
    nombre = Column(String(50))
    inicioProduccion = Column(DateTime())
    finProduccion = Column(DateTime())
    factorRobo = Column(Integer)

    def __str__(self):
        return self.idModelo
    
    marca = relationship("marca")
 
    
class cantSiniestros(Base):
    __tablename__ = 'cantSiniestros'
    
    idSiniestros = Column(Integer(),primary_key=True)
    cantidad = Column(String(50))
    factorSiniestros = Column(Integer)

    def __str__(self):
        return self.idSiniestros


class factorKm(Base):
    __tablename__ = 'factorKm'
    
    idFactorKm = Column(Integer(),primary_key=True)
    rango = Column(Integer)
    factorKm = Column(Integer)

    def __str__(self):
        return self.idFactorKm
    
    
class registroCambio(Base):
    __tablename__ = 'registroCambio'
    
    idCambios = Column(Integer(),primary_key=True)
    fechaDeCambio = Column(DateTime())
    claseCambio = Column(String(50))
    idObjeto = Column(Integer)

    def __str__(self):
        return self.idCambios
 
    
class factoresUniversales(Base):
    __tablename__ = 'factoresUniversales'
    
    idFactoresUniversales = Column(Integer(),primary_key=True)
    factorDerechoEmision = Column(Integer)
    factorDescuentoUnidadAd = Column(Integer)
    factorHijo = Column(Integer)


class usuario(Base):
    __tablename__ = 'usuario'
    
    idUsuario = Column(Integer(),primary_key=True)
    nombre = Column(String(50))
    contrasenia = Column(String(50))
    idRol = Column(Integer, ForeignKey('rol.idRol'))

    def __str__(self):
        return self.idUsuario
    
    rol = relationship("rol")


class rol(Base):
    __tablename__ = 'rol'
    
    idRol = Column(Integer(),primary_key=True)
    nombre = Column(String(50))

    def __str__(self):
        return self.idRol
    
    
Base.metadata.create_all(engine)
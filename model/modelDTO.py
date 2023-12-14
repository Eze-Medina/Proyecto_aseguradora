class ClienteDTO():
    def __init__(self,idCliente="", idPais="", idVivienda="",nombreVivienda="",numeroVivienda="", idDocumento="", tipoDocumento="", numeroDocumento="", nombre="", apellido="", estadoCliente="", anioRegistro=""):
        self.idCliente = idCliente
        self.idPais = idPais
        self.idVivienda = idVivienda
        self.nombreVivienda = nombreVivienda
        self.numeroVivienda = numeroVivienda
        self.idDocumento = idDocumento
        self.tipoDocumento = tipoDocumento
        self.numeroDocumento = numeroDocumento
        self.nombre = nombre
        self.apellido = apellido
        self.estadoCliente = estadoCliente
        self.anioRegistro = anioRegistro
        
    def __str__(self):
        return f"ID Cliente: {self.idCliente}, " \
               f"Número Documento: {self.numeroDocumento}, " \
               f"Nombre: {self.nombre}, " \
               f"Apellido: {self.apellido}, " \
               f"Tipo Documento: {self.tipoDocumento}, " \
               f"Número Vivienda: {self.numeroVivienda}, " \
               f"Nombre Vivienda: {self.nombreVivienda}"
               
class ProvinciaDTO():
    def __init__(self, codigoProvincia="", codigoPais="", nombre="", riesgoProvincia=""):
        self.codigoProvincia = codigoProvincia
        self.codigoPais = codigoPais
        self.nombre = nombre
        self.riesgoProvincia = riesgoProvincia
        
    def __str__(self):
        return f"Código de Provincia={self.codigoProvincia}," \
               f"Código de País={self.codigoPais}," \
               f"Nombre={self.nombre}," \
               f"Riesgo={self.riesgoProvincia}"
               
class MarcaDTO():
    def __init__(self, idMarca="", nombre=""):
        self.idMarca = idMarca
        self.nombre = nombre
        
    def __str__(self):
        return f"Nombre={self.nombre}"

class LocalidadDTO():
    def __init__(self,idLocalidad="",nombre=""):
        self.idLocalidad = idLocalidad
        self.nombre = nombre
    
    def __str__(self):
        return f"Nombre={self.nombre}"

class modeloDTO():
    def __init__(self,idModelo="",nombre=""):
        self.idModelo = idModelo
        self.nombre = nombre
    
    def __str__(self):
        return f"Nombre={self.nombre}"
    
class estadoCivilDTO():
    def __init__(self,idEstadoCivil="",estado=""):
        self.idEstadoCivil = idEstadoCivil
        self.estado = estado
    
    def __str__(self):
        return f"Nombre={self.estado}"

class cantSiniestrosDTO():
    def __init__(self,idSiniestros="",cantidad="",factorSiniestros=""):
        self.idSiniestros = idSiniestros
        self.cantidad = cantidad
        self.factorSiniestros = factorSiniestros
    
    def __str__(self):
        return f"Nombre={self.cantidad}"

class hijoDTO():
    def __init__(self, fechaNacimiento="", sexo="", estadoCivil=""):
        self.fechaNacimiento = fechaNacimiento
        self.sexo = sexo
        self.estadoCivil = estadoCivil
    
    def __str__(self):
        return f"Edad: {self.edad}, Sexo: {self.sexo}, Estado Civil: {self.estadoCivil}"

class polizaDTO():
    def __init__(self, provincia="", localidad="", marcaVehiculo="", modeloVehiculo="", anioVehiculo="",
                 sumaAsegurada="", motor="", chasis="", patente="", kilometrosAnio="",cantSiniestros="", 
                 hijos="", medida1="",medida2="",medida3="",medida4="", tipoCobertura="", fechaInicioVigencia="", fechaFinVigencia="", formaPago=""):
        self.provincia = provincia
        self.localidad = localidad
        self.marcaVehiculo = marcaVehiculo
        self.modeloVehiculo = modeloVehiculo
        self.anioVehiculo = anioVehiculo
        self.sumaAsegurada = sumaAsegurada
        self.motor = motor
        self.chasis = chasis
        self.patente = patente
        self.kilometrosAnio = kilometrosAnio
        self.cantSiniestros = cantSiniestros
        self.hijos = []
        self.medidas= []
        self.tipoCobertura = tipoCobertura
        self.fechaInicioVigencia = fechaInicioVigencia
        self.fechaFinVigencia = fechaFinVigencia
        self.formaPago = formaPago

    def __str__(self):
        hijos_info = "\n".join(str(hijo) for hijo in self.hijos)
        return f"Provincia: {self.provincia}\n" \
               f"Localidad: {self.localidad}\n" \
               f"Marca del Vehículo: {self.marcaVehiculo}\n" \
               f"Modelo del Vehículo: {self.modeloVehiculo}\n" \
               f"Año del Vehículo: {self.anioVehiculo}\n" \
               f"Suma Asegurada: {self.sumaAsegurada}\n" \
               f"Motor: {self.motor}\n" \
               f"Chasis: {self.chasis}\n" \
               f"Patente: {self.patente}\n" \
               f"Kilómetros por Año: {self.kilometrosAnio}\n" \
               f"Cantidad de siniestros: {self.cantSiniestros}\n" \
               f"Hijos:\n{hijos_info}\n" \
               f"Medida1: {self.medidas}\n" \
               f"Tipo Cobertura: {self.tipoCobertura}\n" \
               f"Fecha inicio Vigencia: {self.fechaInicioVigencia}\n" \
               f"Fecha fin Vigencia: {self.fechaFinVigencia}\n" \
               f"Forma de pago: {self.formaPago}"
    
class vehiculoDTO():
    pass


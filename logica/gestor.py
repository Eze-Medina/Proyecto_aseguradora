from data.modelDAO import clienteDAO, provinciaDAO, marcaDAO, localidaDAO, modeloDAO, estadoCivilDAO, cantSiniestrosDAO, hijoDAO, polizaDAO, DAO
from model.modelDTO import ClienteDTO, ProvinciaDTO, MarcaDTO, LocalidadDTO, modeloDTO, estadoCivilDTO, cantSiniestrosDTO, hijoDTO, polizaDTO

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
        datos = polizaDAO()
        datos.guardar_poliza(polizaDTO, clienteDTO)
        
            
    def AAAAAAAA(self):
        print("------------------------------------------------------------------------------------------------------------")
        dao=DAO()
        poliza=dao.prueba()
        print(poliza)
        print(poliza.vehiculo)
        for hijo in poliza.hijo: 
             print(hijo," ",hijo.estadoCivil)
        
        
            
        
                
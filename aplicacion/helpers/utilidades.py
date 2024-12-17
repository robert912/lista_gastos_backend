import datetime
import base64, binascii
import sys, os, json, random
from aplicacion.config import app_config
from aplicacion.enviroment import env
class Utilidades():

    @staticmethod
    def mayusculas(texto):
        try:
            return str(texto).upper()
        except Exception as e:
            return texto

    @staticmethod
    def formatoFecha(fecha):
        """
        Valida fecha en formato dd-mm-YYYY
        """
        try:
            dia = str(fecha.day)
            dia = "0"+dia if len(dia) == 1 else dia
            mes = str(fecha.month)
            mes = "0"+mes if len(mes) == 1 else mes
            anio = str(fecha.year)

            fechaFormateada =  dia + "-" + mes + "-" + anio
            return fechaFormateada
        except ValueError:
            return False

    @staticmethod
    def formatoFechaHora(fecha):
        try:
            return str(fecha.strftime("%d-%m-%Y %H:%M"))
        except ValueError:
            return False
        
    @staticmethod
    def validarDate(date_text, formato):
        try:
            if str(date_text) != datetime.datetime.strptime(str(date_text), formato).strftime(formato):
                raise ValueError
            return True
        except ValueError:
            return False
 
    @staticmethod
    def obtener_datos(query):
        try:
            jsonData = []
            if query:
                """
                Esta funcion sirve solo cuando la query es de tipo sql 1 model list  o sql model(first)
                """
                if isinstance(query, list):
                    for datos in query:
                        d = {}
                        for column in datos.__table__.columns:
                            data = getattr(datos, column.name)
                            if isinstance(data, bytes):
                                Bi = binascii.hexlify(data)
                                Bi = str(Bi.decode('ascii'))
                                data = Bi
                            if isinstance(data, datetime.datetime):
                                data = Utilidades.formatoFechaHora(data)

                            if isinstance(data, datetime.date):
                                data = Utilidades.formatoFecha(data)

                            d[column.name] = data
                        jsonData.append(d)
                else:
                    d = {}
                    for column in query.__table__.columns:
                        data = getattr(query, column.name)
                        if isinstance(data, bytes):
                            Bi = binascii.hexlify(data)
                            Bi = str(Bi.decode('ascii'))
                            data = Bi
                        if isinstance(data, datetime.datetime):
                            data = Utilidades.formatoFechaHora(data)
                        if isinstance(data, datetime.date):
                                data = Utilidades.formatoFecha(data)
                        d[column.name] = data
                    jsonData.append(d)
            return  jsonData
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # exc_type, fname, exc_tb.tb_lineno
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500

    @staticmethod
    def obtener_datos_collection(query):
        """
            Esta funcion sirve solo cuando la query es de tipo select all()
        """
        first = False
        name_first_table = ""
        json_primary = {}
        primary_key = None
        foreign_key = None
        if query:
            for tablas in query:
                for datos in tablas:
                    if datos:
                        tabla_actual = str(datos.__table__)
                        if not first:
                            name_first_table = tabla_actual
                            first = True

                        col = {}
                        for column in datos.__table__.columns:
                            data = getattr(datos, column.name)

                            if isinstance(data, bytes):
                                Bi = binascii.hexlify(data)
                                Bi = str(Bi.decode('ascii'))
                                data = Bi
                                #data = data.decode("ISO-8859-1")
                            if isinstance(data, datetime.datetime):
                                data = Utilidades.formatoFechaHora(data)
                                
                            if isinstance(data, datetime.date):
                                data = Utilidades.formatoFecha(data)
                            col[column.name] = data

                        if name_first_table == tabla_actual:
                            primary_key = int(getattr(datos, "id"))
                            if not primary_key in json_primary:
                                
                                json_primary[primary_key] = {}
                                json_primary[primary_key] = col
                        else:
                            foreign_key = int(getattr(datos, "id"))
                            if not tabla_actual in json_primary[primary_key]:
                                json_primary[primary_key][tabla_actual] = {}
                                if not foreign_key in json_primary[primary_key][tabla_actual]:
                                    json_primary[primary_key][tabla_actual][foreign_key] = {}
                                    json_primary[primary_key][tabla_actual][foreign_key] = col
                                else:
                                    json_primary[primary_key][tabla_actual][foreign_key] = col
                            else:
                                if not foreign_key in json_primary[primary_key][tabla_actual]:
                                    json_primary[primary_key][tabla_actual][foreign_key] = {}
                                    json_primary[primary_key][tabla_actual][foreign_key] = col
                                else:
                                    json_primary[primary_key][tabla_actual][foreign_key] = col
        return  json_primary
    

    @staticmethod
    def generar_rut_chileno():
        existe_rut = ["Data"]
        # Generar un número aleatorio entre 90.000.000 y 99.999.999
        while True:
            ram_digito = random.randrange(99000000,99999999)
            existe_rut = Persona.get_data_by_identificacion_tipo(ram_digito, 2)
            if len(existe_rut) == 0:
                break
        
        reverso = map(int, reversed(str(ram_digito)))
        serie = [2, 3, 4, 5, 6, 7]
        digito_verificador = sum(d * serie[i % 6] for i, d in enumerate(reverso)) % 11
        digito_verificador = '0' if digito_verificador == 11 or digito_verificador == 0 else str(11 - digito_verificador)
        if digito_verificador == '10':
            digito_verificador = 'K'

        # Combinar número y dígito verificador
        return f"{ram_digito}-{digito_verificador}"
    
    
    @staticmethod
    def get_decode(data):
        """
        decodificar PW
        """
        try:
            decoded = base64.b64decode(data)
            return decoded.decode('utf-8')
        except Exception as e:
            return None
    
    
    """
     * [Procesa la peticion a la api de google]
     * @return {json} [retirna json con la informacion obtenida de la API]
     """
    def getConfig():
        config = None
        try:
            enviroment = env
            config = app_config[enviroment]
            return config
        except Exception as e:
            return config
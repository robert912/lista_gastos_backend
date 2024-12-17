import sys, os, datetime
from flask import jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Persona import Persona

class PersonaIdentificacion(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('identificacion', type=str, required=True, help="Debe indicar la identificación de la persona")
        data = parser.parse_args()

        try:
            if data["identificacion"]:
                person = Persona.get_data_by_identificacion(data["identificacion"])
                if person:
                    return {'success': True, 'message': 'Persona enocontrada', 'data': person}, 200
                else:
                    return {'success': False, 'message': "No se encontraron resultados.", 'data': person}, 200
            return {'success': False, 'message': "Faltan parámetros requeridos. Acceso denegado.", 'data':[]}, 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500

class PersonaResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=False, help="Debe indicar la id persona")
        data = parser.parse_args()

        try:
            if data["id"]:
                person = Persona.get_data(data["id"])
                if person:
                    return {'success': True, 'message': 'Persona enocontrada', 'data': person}, 200
                else:
                    return {'success': False, 'message': "No se encontraron resultados.", 'data': person}, 200
            else:
                person = Persona.get_data_all()
                if person:
                    return {'success': True, 'message': 'Persona enocontrada', 'data': person}, 200
                else:
                    return {'success': False, 'message': "No se encontraron resultados.", 'data': person}, 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500
    

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nombre', type=str, required=True, help="Debe indicar el nombre")
        parser.add_argument('apellido', type=str, required=False, help="Debe indicar el primer Apellido")
        parser.add_argument('identificacion', type=str, required=True, help="Debe indicar Identificación")

        data = parser.parse_args()
        try:
            if data and 'nombre' in data and data["nombre"] != '':
                if data and 'identificacion' in data and data['identificacion'] != '':
                    persona_existente = Persona.get_data_by_identificacion(data['identificacion'])
                    if persona_existente  and data['id'] == None:
                        return {'success': True, 'message': "Persona ya existe", 'data': {"id_persona":persona_existente[0]["id"]}}, 200

                    data_persona = {
                        'nombre' : data['nombre'],
                        'apellido' : data['apellido'],
                        'identificacion' : data['identificacion']
                    }
                    persona = Persona.insert_data(data_persona)
                    if persona:
                        return {'success': True, 'message': "Registro ingresado con exito", 'data': persona}, 200
                    return {'success': False, 'message': "No se pudo ingresado el registro", 'data': persona}, 200
                else:
                    return {'success': False, 'message': "Faltan parámetros requeridos. Acceso denegado.", 'data': []}, 200
            else:
                return {'success': False, 'message': "Faltan parámetros requeridos. Acceso denegado.", 'data': []}, 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500


    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="Debe indicar la id persona")
        parser.add_argument('identificacion', type=str, required=False, help="La identificación es requerida")
        parser.add_argument('nombre', type=str, required=False, help="El nombre es requerido")
        parser.add_argument('apellido', type=str, required=False, help="El apellido es requerido")
        data = parser.parse_args()

        try:
            person = Persona.update_data(data['id'], data)
            if not person:
                 return {'success': False, 'message': "Persona no encontrada.", 'data': []}, 200
            return {'success': True, 'message': 'Persona actualizada exitosamente', 'data': person}, 200
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500


    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="Debe indicar la id persona")
        data = parser.parse_args()
        try:
            person = Persona.delete_data(data['id'])
            if not person:
                 return {'success': False, 'message': "Persona no encontrada.", 'data': []}, 200
            return {'success': True, 'message': 'Persona eliminada exitosamente', 'data': person}, 200
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500
        
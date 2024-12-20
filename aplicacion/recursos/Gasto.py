import sys, os, datetime
from flask import jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Gasto import Gasto

class GastoPorMes(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_gasto_mes', type=str, required=True, help="Debe indicar el id_gasto_mes")
        data = parser.parse_args()

        try:
            if data["id_gasto_mes"]:
                mensual  = Gasto.get_by_gasto_mensual(data["id_gasto_mes"])
                if mensual:
                    return {'success': True, 'message': 'Gasto enocontrada', 'data': mensual}, 200
                else:
                    return {'success': False, 'message': "No se encontraron resultados.", 'data': mensual}, 200
            return {'success': False, 'message': "Faltan parámetros requeridos. Acceso denegado.", 'data':[]}, 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500

class GastoResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=False, help="Debe indicar la id")
        data = parser.parse_args()
        try:
            if data["id"]:
                person = Gasto.get_data(data["id"])
                if person:
                    return {'success': True, 'message': 'Gasto enocontrada', 'data': person}, 200
                else:
                    return {'success': False, 'message': "No se encontraron resultados.", 'data': person}, 200
            else:
                person = Gasto.get_data_all()
                if person:
                    return {'success': True, 'message': 'Gasto enocontrada', 'data': person}, 200
                else:
                    return {'success': False, 'message': "No se encontraron resultados.", 'data': person}, 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500
    

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_gasto_mensual', type=int, required=True, help="Debe indicar el id_gasto_mensual")
        parser.add_argument('descripcion', type=str, required=True, help="Debe indicar descripcion")
        parser.add_argument('monto', type=int, required=True, help="Debe indicar monto")
        parser.add_argument('categoria', type=str, required=False, help="Debe indicar categoria")
        parser.add_argument('pagado', type=int, required=False, help="Debe indicar pagado")
        parser.add_argument('fecha_vencimiento', type=str, required=False, help="Debe indicar fecha_vencimiento")

        data = parser.parse_args()
        try:
            if data and 'id_gasto_mensual' in data and data["id_gasto_mensual"]:
                gasto_mensual = Gasto.insert_data(data)
                if gasto_mensual:
                    return {'success': True, 'message': "Registro ingresado con exito", 'data': gasto_mensual}, 200
                else:
                    return {'success': False, 'message': "No se pudo ingresado el registro", 'data': gasto_mensual}, 200
            else:
                return {'success': False, 'message': "Falta el ID de usuario.", 'data': []}, 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500


    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="Debe indicar la id del gasto_mensual")
        parser.add_argument('id_gasto_mensual', type=int, required=False, help="La id_gasto_mensual es requerida")
        parser.add_argument('descripcion', type=str, required=False, help="El descripcion es requerido")
        parser.add_argument('monto', type=int, required=False, help="El monto es requerido")
        parser.add_argument('categoria', type=str, required=False, help="El categoria es requerido")
        parser.add_argument('pagado', type=int, required=False, help="El pagado es requerida")
        parser.add_argument('fecha_vencimiento', type=str, required=False, help="El fecha_vencimiento es requerida")
        parser.add_argument('estado', type=int, required=False, help="El estado es requerida")
        data = parser.parse_args()

        try:
            gasto_mensual = Gasto.update_data(data['id'], data)
            if not gasto_mensual:
                 return {'success': False, 'message': "Gasto no encontrada.", 'data': []}, 200
            return {'success': True, 'message': 'Gasto actualizada exitosamente', 'data': gasto_mensual}, 200
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500


    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="Debe indicar la id del gasto_mensual")
        data = parser.parse_args()
        try:
            person = Gasto.delete_data(data['id'])
            if not person:
                 return {'success': False, 'message': "Gasto no encontrada.", 'data': []}, 200
            return {'success': True, 'message': 'Gasto eliminada exitosamente', 'data': person}, 200
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500
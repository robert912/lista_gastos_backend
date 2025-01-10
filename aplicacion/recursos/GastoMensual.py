import sys, os, datetime
from datetime import datetime, timedelta
from flask import jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.GastoMensual import GastoMensual
from aplicacion.modelos.Gasto import Gasto

class GastoUsuario(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_usuario', type=str, required=True, help="Debe indicar la id_usuario")
        data = parser.parse_args()

        try:
            if data["id_usuario"]:
                gasto_mensual = GastoMensual.get_by_usuario(data["id_usuario"])
                if gasto_mensual:
                    return {'success': True, 'message': 'GastoMensual enocontrada', 'data': gasto_mensual}, 200
                else:
                    return {'success': False, 'message': "No se encontraron resultados.", 'data': gasto_mensual}, 200
            return {'success': False, 'message': "Faltan parámetros requeridos. Acceso denegado.", 'data':[]}, 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500

class GastoMensualResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=False, help="Debe indicar la id")
        data = parser.parse_args()
        try:
            if data["id"]:
                person = GastoMensual.get_data(data["id"])
                if person:
                    return {'success': True, 'message': 'GastoMensual enocontrada', 'data': person}, 200
                else:
                    return {'success': False, 'message': "No se encontraron resultados.", 'data': person}, 200
            else:
                person = GastoMensual.get_data_all()
                if person:
                    return {'success': True, 'message': 'GastoMensual enocontrada', 'data': person}, 200
                else:
                    return {'success': False, 'message': "No se encontraron resultados.", 'data': person}, 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500
    

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_usuario', type=str, required=True, help="Debe indicar el id_usuario")
        parser.add_argument('total_gastos', type=str, required=True, help="Debe indicar total_gastos")

        data = parser.parse_args()
        try:
            if data and 'id_usuario' in data and data["id_usuario"]:
                data["mes"] = datetime.now().month
                data["anio"] = datetime.now().year
                gasto_mensual = GastoMensual.insert_data(data)
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
        parser.add_argument('id_usuario', type=str, required=False, help="La id_usuario es requerida")
        parser.add_argument('mes', type=str, required=False, help="El mes es requerido")
        parser.add_argument('anio', type=str, required=False, help="El anio es requerido")
        parser.add_argument('total_gastos', type=str, required=False, help="El total_gastos es requerido")
        parser.add_argument('estado', type=str, required=False, help="El estado es requerida")
        data = parser.parse_args()

        try:
            gasto_mensual = GastoMensual.update_data(data['id'], data)
            if not gasto_mensual:
                 return {'success': False, 'message': "GastoMensual no encontrada.", 'data': []}, 200
            return {'success': True, 'message': 'GastoMensual actualizada exitosamente', 'data': person}, 200
        
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
            person = GastoMensual.delete_data(data['id'])
            if not person:
                 return {'success': False, 'message': "GastoMensual no encontrada.", 'data': []}, 200
            return {'success': True, 'message': 'GastoMensual eliminada exitosamente', 'data': person}, 200
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500
        
class GastoDelMes(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_usuario', type=int, required=True, help="Debe indicar la id_usuario")
        data = parser.parse_args()
        try:
            if data["id_usuario"]:
                data["mes"] = datetime.now().month
                data["anio"] = datetime.now().year
                gasto_mensual = GastoMensual.get_data_mes(data)
                if not gasto_mensual:
                    mensual = GastoMensual.insert_data(data)
                    if mensual:
                        gasto_mensual = GastoMensual.get_data_mes(data)

                        fecha_actual = datetime.now()
                        mes_anterior = (fecha_actual.replace(day=1) - timedelta(days=1)).month
                        anio_mes_anterior = (fecha_actual.replace(day=1) - timedelta(days=1)).year
                        data_mes_anterior ={
                            'id_usuario':data["id_usuario"],
                            'mes':mes_anterior,
                            'anio':anio_mes_anterior
                        }
                        gasto_mensual_anterior = GastoMensual.get_data_mes(data_mes_anterior)
                        if gasto_mensual_anterior:
                            lista_gasto_anterior = Gasto.get_by_gasto_mensual(gasto_mensual_anterior[0]['id'])

                            for item in lista_gasto_anterior:
                                nuevo_item = {
                                    "id_gasto_mensual": gasto_mensual[0]['id'],
                                    "descripcion": item["descripcion"],
                                    "monto": item["monto"],
                                    "categoria": item["categoria"],
                                    "pagado": 0,
                                    "fecha_vencimiento": item["fecha_vencimiento"],
                                    "estado": item["estado"]
                                }
                                Gasto.insert_data(nuevo_item)

                lista_gasto = Gasto.get_by_gasto_mensual(gasto_mensual[0]['id'])
                gasto_mensual[0]['lista_gasto'] = lista_gasto
                return {'success': True, 'message': "Gasto mensual enocontrada.", 'data': gasto_mensual[0]}, 200
            return {'success': False, 'message': "Faltan parámetros requeridos. Acceso denegado.", 'data':[]}, 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500
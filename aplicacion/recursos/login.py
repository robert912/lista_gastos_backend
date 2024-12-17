import sys, os
from flask_restful import Resource, reqparse
from flask import request
from google.oauth2 import id_token
from google.auth.transport import requests

from aplicacion.redis import redis
from aplicacion.modelos.Usuario import Usuario
from aplicacion.helpers.sesion import Sesion

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('usuario', type=str, required=True, help="El usuario es requerido")
        parser.add_argument('password', type=str, required=True, help="La contraseña es requerida")
        data = parser.parse_args()
        try:
            user = Usuario.get_by_usuario(data['usuario'])
            passw = Usuario.getHash(data['password'])
            if user and 'password_hash' in user[0] and user[0]['password_hash'] == passw:
                tokenId = Sesion.generar_tokenid(user[0]['usuario'], user[0]['password_hash'], 'Admin')
                return {'success': True, 'message': 'Bienvenido', "access_token": tokenId}, 200
            return {'success': False, 'message': 'Usuario o contraseña incorrectos'}, 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500  

    def get(self):
        try:
            if request.headers.get('token'):
                dataRedis = Sesion.validar_token(request.headers.get('token'))
                if dataRedis['es_valido'] == False:
                    return {'success' : False, 'message' :'Acceso denegado'}, 500
                else:
                    return {'success' : True, "data":dataRedis['data']}, 200
            else:
                return {'success' : False, 'message' :'Acceso denegado'}, 500

        except Exception as e:
            return {"message": "Ha ocurrido un error de token."}, 500


class LogoutResource(Resource):
    def post(self):
        """@apiDescription elimina la session asociada al token"""
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True, location="headers", help="Debe indicar token")
        headers = parser.parse_args()
        try:
            dataLogin = {'url':'login.html'}
            tokenId = headers["token"]
            if (redis.exists(tokenId)):
                delRedis = redis.delete(tokenId)#FIN DE CONTROL DE USUARIOS
                if delRedis:
                    return {'success': True, 'message': 'Acción realizada con exito', 'data':dataLogin }, 200
                else:
                    return {'success': False, 'message': 'Ha ocurrido un error inesperado.', 'data':dataLogin }, 200
            else:
                    return {'success': False, 'message': 'Ha ocurrido un error inesperado.', 'data':dataLogin }, 200
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = "Error: "+ str(exc_obj) + " File: " + fname +" linea: "+ str(exc_tb.tb_lineno)
            return {'success': False,"mensaje": "Ha ocurrido un error inesperado", "error":msj}, 500


class LoginGoogle(Resource):
    def post(self):
        try:
            token = request.json.get("credential")
            CLIENT_ID = "1012040646527-eehun94ltjsmt0tolmjp31qvgaibe67l.apps.googleusercontent.com"
            if not token:
                return {'success': False, 'message': "Token no recibido", 'data':[] }, 400
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            email = idinfo.get("email")
            user = Usuario.get_by_usuario(email)
            if not user:
                Usuario.insert_data(idinfo)
                user = Usuario.get_by_usuario(email)
            tokenId = Sesion.generar_tokenid(user[0]['usuario'], user[0]['google_id'], 'Admin')
            return {'success': True, 'message': 'Bienvenido', "access_token": tokenId, "data":user[0]}, 200
        except ValueError:
            return {'success': False, 'message': "Token inválido", 'data':[] }, 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = "Error: "+ str(exc_obj) + " File: " + fname +" linea: "+ str(exc_tb.tb_lineno)
            return {"estado":0,"mensaje": "Ha ocurrido un error inesperado", "error":msj}, 500
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,click,json

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from aplicacion.config import app_config
from aplicacion.enviroment import env
from aplicacion.db import db
from aplicacion.redis import redis
from aplicacion.modelos import *

from tests.app_tests import Prueba
from aplicacion.helpers.sesion import Sesion
from aplicacion.recursos.Gasto import GastoPorMes, GastoResource
from aplicacion.recursos.GastoMensual import GastoUsuario, GastoMensualResource, GastoDelMes
from aplicacion.recursos.login import Login, LogoutResource, LoginGoogle
from aplicacion.recursos.Persona import PersonaResource, PersonaIdentificacion
from aplicacion.recursos.PdfGenerator import GeneratePdf


app = Flask(__name__)
CORS(app)

enviroment = "development"

app.config.from_object(app_config[enviroment])
db.init_app(app)
redis.init_app(app)
api = Api(app)


@app.before_request
def verifica_token():
    if request.method != 'OPTIONS' and request.endpoint not in ['login', 'logingoogle', 'prueba']:
        if not request.headers.get('Authorization'):
            return jsonify({'message': 'Acceso denegado'}), 403
        else:
            resultado = Sesion.validar_token(request.headers.get('Authorization'), request.headers.get('idUsuario'))
            es_valido = resultado.get("es_valido")
            if not es_valido:
                return jsonify({'message' :'Acceso denegado'}), 403


api.add_resource(GeneratePdf,'/generate_pdf')
api.add_resource(GastoDelMes,'/gastodelmes/obtener')
api.add_resource(Login, '/login', '/login/validar')
api.add_resource(LoginGoogle, '/login/google')
api.add_resource(LogoutResource, '/logout/system')
api.add_resource(PersonaResource, '/getpersona')
api.add_resource(PersonaIdentificacion, '/personabyrut')
api.add_resource(Prueba, '/prueba')

app.run(host='0.0.0.0', port=5000)
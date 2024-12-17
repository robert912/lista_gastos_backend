#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, json
from aplicacion.db import db
from sqlalchemy import text
import random
import hashlib
from datetime import datetime
from aplicacion.redis import redis
from aplicacion.modelos.Persona import Persona

class Sesion():

    @staticmethod
    def generar_tokenid(username, password, perfil):
        try:
            fecha_actual = datetime.now()
            base = username+password+str(fecha_actual.minute)+str(fecha_actual.second)
            token_id = hashlib.md5(base.encode()).hexdigest()
            data = {"username":username,"perfil":perfil}
            redis.setex(token_id, 3600, json.dumps(data))
            value = redis.get(token_id)
            if value:
                return token_id
            else:
                return 'No se pudo recuperar el valor de Redis.', 500
        except Exception as e:
            return None


    @staticmethod
    def eliminar_tokenid(token_id):
        try:
            redis.delete(token_id)
            return True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500


    @staticmethod
    def validar_token(token_id):
        existe = redis.exists(token_id)
        data = redis.get(token_id)
        return {"es_valido":existe, "data":json.loads(data)}
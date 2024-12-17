from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Index, Integer, String, Table, Text, Time, distinct, and_
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.dialects.mysql.enumerated import ENUM
import sys, os, datetime

from aplicacion.db import db, dataBase
from aplicacion.helpers.utilidades import Utilidades

class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {'schema': dataBase}

    id              = db.Column(db.Integer, primary_key=True)
    usuario         = db.Column(db.String(150), unique=True, nullable=False)
    nombre          = db.Column(db.String(100), unique=True, nullable=False)
    password_hash   = db.Column(db.String(255))
    google_id       = db.Column(db.String(255))
    avatar          = db.Column(db.String(255))
    created_at      = db.Column(db.DateTime, server_default=db.FetchedValue())

    @classmethod
    def get_data(cls, _id):
        query =  cls.query.filter_by(id=_id).first()
        return  Utilidades.obtener_datos(query)

    @classmethod
    def get_by_usuario(cls, usuario):
        query =  cls.query.filter_by(usuario=usuario).first()
        return  Utilidades.obtener_datos(query)
    
    @classmethod
    def getHash(cls, password):
         sql =  "SELECT SHA2(AES_ENCRYPT('"+ password +"','40ba08ea0c8f66bde25f92f56f7c4fa6'), 256) AS hash FROM dual LIMIT 1"
         hash_password = db.session.execute(sql).scalar()
         return hash_password

    @classmethod
    def insert_data(cls, dataJson):
        query = Usuario( 
            usuario = dataJson['email'].lower().strip(),
            nombre = dataJson['name'].lower() if dataJson['name'] != None else '',
            google_id = dataJson['sub'] if dataJson['sub'] != None else '',
            avatar = dataJson['picture'] if dataJson['picture'] != None else '',
            created_at = func.NOW(),
            )
        Usuario.guardar(query)
        if query.id:                            
            return query.id 
        return  None


    def guardar(self):
        db.session.add(self)
        db.session.commit()
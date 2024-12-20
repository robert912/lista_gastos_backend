from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Index, Integer, String, Table, Text, Time, distinct, and_
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.dialects.mysql.enumerated import ENUM
import sys, os, datetime

from aplicacion.db import db, dataBase
from aplicacion.helpers.utilidades import Utilidades

class GastoMensual(db.Model):
    __tablename__ = 'gasto_mensual'
    __table_args__ = {'schema': dataBase}

    id              = db.Column(db.Integer, primary_key=True)
    id_usuario      = db.Column(db.Integer, nullable=False)
    mes             = db.Column(db.Integer, nullable=False)
    anio             = db.Column(db.Integer, nullable=False)
    total_gastos    = db.Column(db.Integer, default=0)
    estado          = db.Column(db.Integer, default=1)
    created_at      = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at      = db.Column(db.DateTime, server_default=db.FetchedValue())


    @classmethod
    def get_data(cls, _id):
        query =  cls.query.filter_by(id=_id).first()
        return  Utilidades.obtener_datos(query)
    
    @classmethod
    def get_data_all(cls):
        query =  cls.query.all()
        return  Utilidades.obtener_datos(query)
    
    @classmethod
    def get_by_usuario(cls, id_usuario):
        query = cls.query.filter_by(id_usuario=id_usuario).all()
        return Utilidades.obtener_datos(query)

    @classmethod
    def insert_data(cls, dataJson):
        query = GastoMensual(
            id_usuario = dataJson['id_usuario'],
            mes = dataJson['mes'],
            anio = dataJson['anio'],
            total_gastos = dataJson.get('total_gastos', 0),
            estado = 1,
            created_at = func.NOW()
        )
        query.guardar()
        return query.id if query.id else None

    @classmethod
    def update_data(cls, _id, dataJson):
        query = cls.query.filter_by(id=_id).first()
        if query:
            if 'id_usuario' in dataJson and dataJson['id_usuario'] != None:
                query.id_usuario = dataJson['id_usuario']
            if 'mes' in dataJson and dataJson['mes'] != None:
                query.mes = dataJson['mes']
            if 'anio' in dataJson and dataJson['anio'] != None:
                query.anio = dataJson['anio']
            if 'total_gastos' in dataJson and dataJson['total_gastos'] != None:
                query.total_gastos = dataJson['total_gastos']
            if 'estado' in dataJson and dataJson['estado'] != None:
                query.estado = dataJson['estado']
            query.updated_at = func.NOW()
           
            db.session.commit()
            if query.id:                            
                return query.id
        return  None

    @classmethod
    def delete_data(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            GastoMensual.eliminar(query)
            if query.id:                            
                return query.id
        return  None

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
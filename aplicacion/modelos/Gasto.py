from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Index, Integer, String, Table, Text, Time, distinct, and_
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.dialects.mysql.enumerated import ENUM
import sys, os, datetime

from aplicacion.db import db, dataBase
from aplicacion.helpers.utilidades import Utilidades

class Gasto(db.Model):
    __tablename__ = 'gasto'
    __table_args__ = {'schema': dataBase}

    id                  = db.Column(db.Integer, primary_key=True)
    id_gasto_mensual    = db.Column(db.Integer, nullable=False)
    descripcion         = db.Column(db.String(255), nullable=False)
    monto               = db.Column(db.Integer, nullable=False)
    categoria           = db.Column(db.String(100), default='')
    pagado              = db.Column(db.Integer, default=0)
    fecha_vencimiento   = db.Column(db.Date)
    estado              = db.Column(db.Integer, default=1)
    created_at          = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at          = db.Column(db.DateTime, server_default=db.FetchedValue())

    @classmethod
    def get_data(cls, _id):
        query =  cls.query.filter_by(id=_id).first()
        return  Utilidades.obtener_datos(query)

    @classmethod
    def get_data_all(cls):
        query =  cls.query.all()
        return  Utilidades.obtener_datos(query)

    @classmethod
    def get_by_gasto_mensual(cls, id_gasto_mensual):
        query = cls.query.filter_by(id_gasto_mensual=id_gasto_mensual).filter_by(estado = 1).all()
        return Utilidades.obtener_datos(query)

    @classmethod
    def insert_data(cls, dataJson):
        query = Gasto(
            id_gasto_mensual=dataJson['id_gasto_mensual'],
            descripcion=dataJson['descripcion'],
            monto=dataJson['monto'],
            categoria=dataJson.get('categoria', ''),
            pagado=dataJson.get('pagado', 0),
            fecha_vencimiento=dataJson.get('fecha_vencimiento', None),
            estado = 1,
            created_at = func.NOW()
        )
        query.guardar()
        return query.id if query.id else None
    

    @classmethod
    def update_data(cls, _id, dataJson):
        query = cls.query.filter_by(id=_id).first()
        if query:
            if 'id_gasto_mensual' in dataJson and dataJson['id_gasto_mensual'] != None:
                query.id_gasto_mensual = dataJson['id_gasto_mensual']
            if 'descripcion' in dataJson and dataJson['descripcion'] != None:
                query.descripcion = dataJson['descripcion'].strip()
            if 'monto' in dataJson and dataJson['monto'] != None:
                query.monto = dataJson['monto']
            if 'categoria' in dataJson and dataJson['categoria'] != None:
                query.categoria = dataJson['categoria'].strip()
            if 'pagado' in dataJson and dataJson['pagado'] != None:
                query.pagado = dataJson['pagado']
            if 'fecha_vencimiento' in dataJson and dataJson['fecha_vencimiento'] != None:
                query.fecha_vencimiento = dataJson['fecha_vencimiento']
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
            Gasto.eliminar(query)
            if query.id:                            
                return query.id
        return  None

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
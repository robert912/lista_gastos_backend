import sys, os
from sqlalchemy.sql.functions import func
from aplicacion.db import db, dataBase
from aplicacion.helpers.utilidades import Utilidades

class Persona(db.Model):

    __tablename__ = 'persona'
    __table_args__ = (
        db.Index('identificacion'),
        {'schema': dataBase}
    )

    id = db.Column(db.Integer, primary_key=True)
    identificacion = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    
    #CRUD

    @classmethod
    def get_data(cls, _id):
        query =  cls.query.filter_by(id=_id).first()
        return  Utilidades.obtener_datos(query)

    @classmethod
    def get_data_all(cls):
        query =  cls.query.all()
        return  Utilidades.obtener_datos(query)
    
    @classmethod
    def get_data_by_identificacion(cls, rut):
        query =  cls.query.filter_by(identificacion=rut).first()
        return  Utilidades.obtener_datos(query)
    
    @classmethod
    def insert_data(cls, dataJson):
        query = Persona( 
            nombre = dataJson['nombre'],
            apellido = dataJson['apellido'] if dataJson['apellido'] != None else '',
            identificacion = dataJson['identificacion'].strip(),
            created_at = func.NOW(),
            updated_at = func.NOW(),
            )
        Persona.guardar(query)
        if query.id:                            
            return query.id 
        return  None

    @classmethod
    def update_data(cls, _id, dataJson):
        query = cls.query.filter_by(id=_id).first()
        if query:
            if 'nombre' in dataJson and dataJson['nombre'] != None:
                query.nombre = dataJson['nombre']
            if 'apellido' in dataJson and dataJson['apellido'] != None:
                query.apellido = dataJson['apellido']
            if 'identificacion' in dataJson and dataJson['identificacion'] != None:
                identificacion = dataJson['identificacion'].strip()
                query.identificacion = identificacion
            if 'created_at' in dataJson and dataJson['created_at'] != None:
                query.created_at = dataJson['created_at']
            if 'updated_at' in dataJson and dataJson['updated_at'] != None:
                query.updated_at = dataJson['updated_at']
           
            db.session.commit()
            if query.id:                            
                return query.id
        return  None

    @classmethod
    def delete_data(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            Persona.eliminar(query)
            if query.id:                            
                return query.id
        return  None

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
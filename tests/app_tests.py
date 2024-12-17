from flask_restful import Resource

class Prueba(Resource):
    def get(self):
        try:
            # Lógica para verificar si los servicios están activos
            # Por ejemplo, comprobar conexión a la base de datos:
            # db_status = check_database_connection()
            
            # Si todo está bien
            return {'message': 'La API está funcionando correctamente'}, 200
        except Exception as e:
            # En caso de error
            return {'success': False, 'message': str(e)}, 500

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
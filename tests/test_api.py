import pytest
import requests

BASE_URL = "http://localhost:5000"  # Asegúrate de que este es el URL correcto para tu API

def test_api_status():
    """Verifica si la API está activa y responde con un código de estado 200"""
    response = requests.get(f"{BASE_URL}/prueba")
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

def test_api_response_data():
    """Verifica que la API devuelve los datos correctos"""
    response = requests.get(f"{BASE_URL}/prueba")
    json_data = response.json()
    assert 'message' in json_data, "La clave 'message' no se encuentra en la respuesta"
    assert json_data['message'] == 'La API está funcionando correctamente', "El mensaje no es el esperado"

def test_acceso_denegado_sin_token():
    """Verifica que se deniegue el acceso si no se envía un token"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 403
    assert response.json() == {'message': 'Acceso denegado'}
import unittest
from app import app

class TestSeguridadMotos(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    # Prueba de disponibilidad
    def test_home_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # PRUEBA OWASP: Intento de Inyección SQL
    def test_sql_injection_attempt(self):
        # Intentamos enviar un código malicioso común (' OR '1'='1)
        # Si la app es segura, simplemente no encontrará resultados o dará error controlado,
        # pero NO debería romperse el servidor ni soltar toda la base de datos.
        response = self.client.get('/buscar?marca=\' OR \'1\'=\'1')
        self.assertEqual(response.status_code, 200) 
        # Verificamos que no se filtre información sensible en el error
        self.assertNotIn(b"mysql.connector.errors", response.data)

if __name__ == '__main__':
    unittest.main()
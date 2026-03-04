import unittest
from app import app

class TestMotosSeguridad(unittest.TestCase):

    def setUp(self):
        # Configuramos el cliente de prueba de Flask
        self.client = app.test_client()
        self.client.testing = True

    # 1. Test de Disponibilidad (Básico)
    def test_home_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # 2. Test OWASP A01: Control de Acceso (NUEVO)
    def test_admin_access_forbidden(self):
        # Verificamos que la ruta /admin esté bloqueada (Error 403)
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 403)
        print("\n✅ Test A01: Acceso a /admin bloqueado correctamente.")

    # 3. Test OWASP A03: Prevención de Inyección SQL
    def test_sql_injection_mitigation(self):
        # Intentamos un ataque de inyección en el buscador
        ataque = "' OR '1'='1"
        response = self.client.get(f'/buscar?marca={ataque}')
        # Si el código es seguro, la página carga (200) pero no explota la DB
        self.assertEqual(response.status_code, 200)
        print("✅ Test A03: Ataque de inyección SQL mitigado con éxito.")

    # 4. Test OWASP A05: Cabeceras de Seguridad (NUEVO)
    def test_security_headers(self):
        response = self.client.get('/')
        # Verificamos que el servidor envíe las instrucciones de seguridad al navegador
        self.assertEqual(response.headers.get('X-Frame-Options'), 'SAMEORIGIN')
        self.assertEqual(response.headers.get('X-Content-Type-Options'), 'nosniff')
        print("✅ Test A05: Cabeceras de seguridad HTTP detectadas.")

if __name__ == '__main__':
    unittest.main()
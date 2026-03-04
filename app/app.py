from flask import Flask, render_template_string, request, abort
import mysql.connector
import os
import logging # Para OWASP A09 (Registro de actividad)

app = Flask(__name__)

# --- 1. CONFIGURACIÓN DE LOGS (OWASP A09:2021 - Registro y Supervisión) ---
# Esto creará un archivo 'access.log'
logging.basicConfig(
    filename='access.log', 
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s: %(message)s'
)

def conectar_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME')
    )

# --- 2. CABECERAS DE SEGURIDAD (OWASP A05:2021 - Configuración Incorrecta) ---
# Estas líneas protegen al navegador del usuario contra ataques comunes.
@app.after_request
def añadir_cabeceras_seguridad(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN' # Evita Clickjacking
    response.headers['X-Content-Type-Options'] = 'nosniff' # Evita ejecución de scripts falsos
    response.headers['X-XSS-Protection'] = '1; mode=block' # Filtro XSS básico
    return response


HTML_BASE = """
<!DOCTYPE html>
<html>
<head><title>Buscador de Motos Seguro</title></head>
<body>
    <h1>Buscador de Modelos de Moto</h1>
    <form method="GET" action="/buscar">
        <input type="text" name="marca" placeholder="Ej: Honda">
        <button type="submit">Buscar</button>
    </form>
    <br>
    <table border="1">
        <tr>
            <th>Marca</th><th>Modelo</th><th>CC</th><th>Precio</th>
        </tr>
        {% for moto in motos %}
        <tr>
            <td>{{ moto.marca }}</td>
            <td>{{ moto.modelo }}</td>
            <td>{{ moto.cilindrada }}</td>
            <td>{{ moto.precio_estimado }}€</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_BASE, motos=[])

# --- 3. CONTROL DE ACCESO (OWASP A01:2021 - Control de Acceso Quebrado) ---
@app.route('/admin')
def admin():
    # Bloqueamos esta ruta para demostrar que no cualquiera puede entrar.
    logging.warning("Intento de acceso NO AUTORIZADO a la zona /admin")
    abort(403) # Devuelve error "Prohibido"

@app.route('/buscar')
def buscar():
    marca = request.args.get('marca', '')
    
    # Registro de actividad (A09)
    logging.info(f"Búsqueda realizada por el usuario: {marca}")
    
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    
    # --- 4. PREVENCIÓN DE INYECCIÓN (OWASP A03:2021 - Inyección) ---
    # Usamos %s (consultas parametrizadas) para que sea imposible hackear la DB.
    query = "SELECT * FROM motos WHERE marca LIKE %s"
    cursor.execute(query, (f"%{marca}%",))
    
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template_string(HTML_BASE, motos=resultados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
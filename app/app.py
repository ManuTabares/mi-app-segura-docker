from flask import Flask, render_template_string, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

def conectar_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME')
    )

# Diseño HTML super simple integrado en el código
HTML_BASE = """
<!DOCTYPE html>
<html>
<head><title>Buscador de Motos</title></head>
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

@app.route('/buscar')
def buscar():
    marca = request.args.get('marca', '')
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    
    # SEGURIDAD OWASP: Usamos %s para evitar SQL Injection
    query = "SELECT * FROM motos WHERE marca LIKE %s"
    cursor.execute(query, (f"%{marca}%",))
    
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template_string(HTML_BASE, motos=resultados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
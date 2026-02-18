from flask import Flask, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

def conectar_db():
    # Intentamos conectar usando las variables que definimos en el Docker
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME')
    )

@app.route('/')
def inicio():
    return "<h1>Servidor Flask funcionando con MySQL</h1>"

@app.route('/datos')
def ver_datos():
    try:
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
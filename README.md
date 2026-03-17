# 🏍️ MotoScan Pro: Seguridad OWASP & Despliegue Automatizado (CI/CD)

Este proyecto es una plataforma web de consulta de motocicletas desarrollada con un enfoque "Security by Design". No es solo una aplicación funcional, sino un entorno completo que integra contenedores, bases de datos persistentes y auditorías de seguridad automatizadas basadas en el estándar **OWASP Top 10 2021**.

---

## 🛠️ Stack Tecnológico
* **Backend:** Python 3.9 + Flask para la lógica del servidor.
* **Base de Datos:** MySQL 8.0 para el almacenamiento de datos de motos.
* **Infraestructura:** Docker & Docker Compose para la contenedorización y orquestación de servicios.
* **Automatización:** Jenkins (CI/CD Pipeline) para la integración continua.
* **Seguridad:** Estándares OWASP Top 10 y Postman para auditoría externa.

---

## 🚀 Guía de Instalación Paso a Paso (Desde Cero)

### 1. Requisitos Previos
Para replicar este entorno en cualquier ordenador, es necesario instalar:
* **Docker Desktop:** Para gestionar los contenedores de la aplicación y la base de datos.
* **Visual Studio Code:** Como editor de código principal.
* **Postman:** Para realizar las pruebas de seguridad externas.

---

### 2. Estructura del Proyecto
Debes organizar los archivos de la siguiente manera en tu carpeta de trabajo:

```text
Mi-primer-docker/
├── app/
│   ├── app.py             # Lógica de la aplicación y medidas de seguridad
│   ├── requirements.txt   # Librerías necesarias (Flask, mysql-connector)
│   └── test_app.py        # Pruebas unitarias para el Pipeline
├── .env                   # Variables de entorno con credenciales de la DB
├── Dockerfile             # Configuración de la imagen Docker de Python
├── docker-compose.yml     # Orquestador que levanta la web y la DB
├── init.sql               # Script de creación de tablas y datos iniciales
└── Jenkinsfile            # Definición del flujo de trabajo de Jenkins

3. Configuración y Lanzamiento
Configura las credenciales: Crea un archivo .env en la raíz con los datos de conexión a la base de datos.

Levanta el entorno: Abre una terminal en la carpeta raíz y ejecuta el comando de construcción:

Bash
docker-compose up --build -d
Este comando descarga las imágenes, crea la base de datos y activa el servidor web automáticamente.

Verifica el estado: Los contenedores web-1 y db-1 deben aparecer en verde y en estado "Running" en Docker Desktop.

🛡️ Implementación de Seguridad (OWASP Top 10)
La aplicación ha sido blindada contra las amenazas más críticas del sector:

A01:2021 - Control de Acceso Quebrado
Implementación: Se ha restringido el acceso a la ruta /admin mediante la función abort(403).

Resultado: Cualquier intento de acceso no autorizado devuelve un error 403 Forbidden, protegiendo la zona administrativa de ataques externos.

A03:2021 - Inyección (SQLi)
Implementación: El buscador utiliza consultas parametrizadas (%s) en lugar de concatenar texto directamente en la sentencia SQL.

Resultado: Los intentos de ataque como ' OR 1=1 -- son tratados como texto plano y no pueden manipular la base de datos.

A05:2021 - Configuración Incorrecta de Seguridad
Implementación:

Gestión de secretos y claves mediante variables de entorno en el archivo .env.

Configuración de cabeceras de seguridad HTTP (X-Frame-Options, X-Content-Type-Options) para evitar ataques de Clickjacking y sniffing.

A09:2021 - Fallos en el Registro y Supervisión
Implementación: Se ha integrado un sistema de Logging interno que registra la actividad en el archivo access.log.

Resultado: Cada búsqueda y cada intento de acceso no autorizado a /admin queda registrado con marca de tiempo, permitiendo auditorías de seguridad en tiempo real.

🧪 Validación y Auditoría
Automatización con Jenkins (CI/CD)
El Pipeline de Jenkins (mi-app-segura-docker) garantiza que cada cambio en el código pase los tests unitarios de test_app.py antes de considerarse estable, asegurando que las protecciones no se desactiven por error durante el desarrollo.

Pruebas Externas con Postman
Se ha configurado una colección de auditoría que valida los siguientes puntos críticos:

Test A: Disponibilidad del servicio y presencia de cabeceras de seguridad obligatorias.

Test B: Mitigación de Inyección SQL en la barra de búsqueda mediante pruebas de penetración simuladas.

Test C: Bloqueo efectivo del acceso a la zona /admin con verificación de código de estado 403.

Autor: Manuel Reinoso Tabares
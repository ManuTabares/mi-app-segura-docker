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
```
### 3. Configuración y Lanzamiento
Configura las credenciales: Crea un archivo .env en la raíz con los datos de conexión a la base de datos.

Levanta el entorno: Abre una terminal en la carpeta raíz y ejecuta el comando de construcción:

Bash
docker-compose up --build -d
Este comando descarga las imágenes, crea la base de datos y activa el servidor web automáticamente.

Verifica el estado: Los contenedores web-1 y db-1 deben aparecer en verde y en estado "Running" en Docker Desktop.

## 🛡️ Análisis detallado de Seguridad (OWASP Top 10)
Aquí explicamos qué hemos hecho para evitar que nos hackeen la aplicación:

A01:2021 - Control de Acceso Quebrado
Funcionamiento: Hemos creado un "honeypot" o zona restringida en /admin. En lugar de dejar la puerta abierta o dar un error genérico, el sistema identifica el acceso no autorizado y utiliza el protocolo HTTP de forma estricta devolviendo un 403 Forbidden.

Código: Ubicado en la función admin() de app.py.

A03:2021 - Inyección (SQLi)
Funcionamiento: El ataque más común consiste en escribir código SQL en la caja de búsqueda (ej: ' OR 1=1).

Solución Técnica: Usamos Consultas Parametrizadas. Esto significa que el driver de MySQL trata lo que escriba el usuario como simple "texto de búsqueda" y nunca como "órdenes" para la base de datos.

Código: Ubicado en el método cursor.execute(query, (params,)).

A05:2021 - Configuración Incorrecta de Seguridad
Funcionamiento: Las aplicaciones suelen dejar pistas a los hackers (versiones de software, errores técnicos).

Solución: 1.  Headers: Forzamos al navegador a no permitir "iframes" (evita que nos clonen la web para robar clicks) y a no adivinar el tipo de archivo (evita ejecución de scripts ocultos).
### Variables de Entorno: Las claves nunca viajan al repositorio de código (GitHub), se quedan en el archivo local .env.

A09:2021 - Fallos en el Registro y Supervisión
Funcionamiento: Un ataque que no se registra es un ataque que se repetirá.

Solución: Hemos integrado un sistema de Logging Industrial. Cada vez que alguien busca o intenta entrar en zonas prohibidas, se genera una línea en access.log. Esto permite a un administrador forense revisar qué pasó hace una hora o hace un mes.

## 🧪 Validación y Auditoría
Automatización con Jenkins (CI/CD)
El Pipeline de Jenkins (mi-app-segura-docker) garantiza que cada cambio en el código pase los tests unitarios de test_app.py antes de considerarse estable, asegurando que las protecciones no se desactiven por error durante el desarrollo.

Auditoría Externa con Postman
Para validar que la aplicación cumple con los estándares de OWASP, hemos diseñado una "Suite de Pruebas" automatizada. Cada prueba tiene un objetivo específico de seguridad:

### 1. Test A: Verificación de Integridad y Hardening (OWASP A05)
¿Qué hace?: Realiza una petición normal a la página de inicio (/).

Lo que comprobamos (Scripts):

Estado 200 OK: Confirmamos que el servidor está vivo y responde.

Security Headers: Aquí es donde verificamos el Hardening (endurecimiento) del servidor. Comprobamos que el código Python ha inyectado correctamente las cabeceras X-Frame-Options (para que nadie pueda meter tu web en un marco y robar clics) y X-Content-Type-Options (para obligar al navegador a no ejecutar archivos sospechosos).

Conclusión: Si este test sale verde, el servidor está configurado de forma segura frente a ataques de secuestro de sesión básicos.

### 2. Test B: Simulación de Ataque por Inyección (OWASP A03)
¿Qué hace?: Envía una cadena maliciosa a través del buscador: {{baseUrl}}/buscar?marca=' OR 1=1 --. Este es el ataque clásico para intentar saltarse el filtro y que la base de datos te devuelva todas las motos de todos los usuarios a la vez.

Lo que comprobamos (Scripts):

Respuesta Segura: Verificamos que el servidor no se "rompe" (no da error 500).

Mitigación: Validamos que la respuesta no contiene errores internos de MySQL. Si el ataque hubiera funcionado, veríamos datos que no deberían estar ahí; como no aparecen, confirmamos que las Consultas Parametrizadas de tu app.py han neutralizado el código malicioso tratándolo como simple texto.

Conclusión: Demostramos que la base de datos es inmune a manipulaciones externas vía URL.

### 3. Test C: Auditoría de Control de Acceso (OWASP A01)
¿Qué hace?: Intenta forzar la entrada a la ruta restringida {{baseUrl}}/admin.

Lo que comprobamos (Scripts):

Código 403 Forbidden: Esta es la clave. El test solo se marca como VERDE si el servidor responde con un ROJO (403).

¿Por qué es importante?: En una aplicación insegura, esta ruta daría un 200 (acceso permitido) o un 404 (ruta no encontrada). Al dar un 403, estamos demostrando que la ruta existe pero que hay un mecanismo de control de acceso activo que identifica al usuario como "no autorizado" y lo expulsa.

Conclusión: El sistema es capaz de distinguir entre áreas públicas y áreas privadas, protegiendo la información sensible.

Autor: Manuel Reinoso Tabares
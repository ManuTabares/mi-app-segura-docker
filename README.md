# 🏍️ Buscador de Motos Seguro (Full-Stack & DevOps)

Este proyecto es una plataforma de consulta de especificaciones y precios de motocicletas, diseñada con un enfoque en **Seguridad (OWASP)** y **Automatización (CI/CD)**.

## 🏗️ Arquitectura del Proyecto
La aplicación está completamente containerizada para garantizar que funcione en cualquier entorno:
* **Backend:** Flask (Python 3.12)
* **Base de Datos:** MySQL 8.0
* **Orquestación:** Docker Compose para gestionar el despliegue multi-contenedor

## 🛡️ Auditoría de Seguridad (Estándar OWASP)
Se ha puesto especial foco en prevenir vulnerabilidades críticas del **OWASP Top 10**:

* **A03:2021-Injection:** El buscador utiliza **consultas parametrizadas** (`%s`). Esto evita que atacantes puedan ejecutar código malicioso en la base de datos mediante la barra de búsqueda.
* **A05:2021-Security Misconfiguration:** Se utiliza un archivo `.env` para separar las credenciales del código fuente.

## 🧪 Pruebas y Validación
Para asegurar la calidad del software, se han implementado dos niveles de testeo:

1. **Pruebas Unitarias Automáticas:** El archivo `test_app.py` verifica la disponibilidad del servicio y simula intentos de Inyección SQL para confirmar que son bloqueados.
2. **Validación Manual con Postman:** Se han testeado los endpoints de la API enviando payloads maliciosos (`' OR 1=1 --`), confirmando que la aplicación responde de forma segura (200 OK sin fuga de datos).

## ⚙️ Automatización CI/CD (Jenkins)
El proyecto incluye un **Jenkinsfile** que define un pipeline de integración continua:
* **Build:** Construcción automática de las imágenes Docker.
* **Test:** Ejecución de las pruebas unitarias de seguridad dentro del contenedor.
* **Resultados:** Solo si los tests pasan, la aplicación se considera apta para producción.

---
**Desarrollado por:** Manuel Reinoso Tabares

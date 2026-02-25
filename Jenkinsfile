pipeline {
    agent any
    stages {
        stage('Limpieza') {
            steps {
                sh 'docker-compose down -v'
            }
        }
        stage('Construir Aplicación') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }
        stage('Pasar Pruebas de Seguridad (OWASP)') {
            steps {
                // Ejecuta los tests dentro del contenedor de python
                sh 'docker exec mi-primer-docker-web-1 python -m unittest test_app.py'
            }
        }
    }
    post {
        always {
            echo 'Pipeline terminado.'
        }
    }
}
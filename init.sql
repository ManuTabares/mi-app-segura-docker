CREATE DATABASE IF NOT EXISTS prueba_db;
USE prueba_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50)
);

INSERT INTO usuarios (nombre) VALUES ('Primer Usuario de Prueba');
CREATE DATABASE IF NOT EXISTS mi_aplicacion_db;
USE mi_aplicacion_db;

CREATE TABLE IF NOT EXISTS motos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    cilindrada VARCHAR(20),
    precio_estimado DECIMAL(10, 2)
);

INSERT INTO motos (marca, modelo, cilindrada, precio_estimado) VALUES 
('Honda', 'CB500F', '500cc', 6500.00),
('Yamaha', 'MT-07', '689cc', 7200.00),
('Kawasaki', 'Z900', '948cc', 10500.00),
('Ducati', 'Monster', '937cc', 12000.00);
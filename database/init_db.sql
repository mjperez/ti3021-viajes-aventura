-- ============================================
-- Limpieza de Base de Datos
-- ============================================
DROP DATABASE IF EXISTS viajes_aventura;
DROP USER IF EXISTS 'admin_aventura'@'localhost';

-- ============================================
-- Script de creación de Base de Datos
-- Sistema de Reservas - Viajes Aventura
-- ============================================

-- Crear la base de datos
CREATE DATABASE viajes_aventura;

-- ============================================
-- Creación de usuario administrador con sus 
-- privilegios corresopndientes.
-- ============================================
CREATE USER IF NOT EXISTS 'admin_aventura'@'localhost' IDENTIFIED BY 'Aventura123';
GRANT ALL PRIVILEGES ON viajes_aventura.* TO 'admin_aventura'@'localhost';
FLUSH PRIVILEGES;

-- Seleccionar base de datos
USE viajes_aventura;

-- ============================================
-- Tabla: Usuarios
-- Gestión de usuarios del sistema (Clientes y Administradores)
-- ============================================
CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    rol ENUM('ADMIN', 'CLIENTE') NOT NULL DEFAULT 'CLIENTE',
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_rol (rol)
) ENGINE=InnoDB;

-- ============================================
-- Tabla: Destinos
-- Información de destinos turísticos
-- ============================================
CREATE TABLE Destinos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500) NOT NULL,
    costo_base DECIMAL(10,2) NOT NULL,
    cupos_disponibles INT NOT NULL DEFAULT 50 CHECK (cupos_disponibles >= 0),
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB;

-- ============================================
-- Tabla: Actividades
-- Actividades disponibles en cada destino
-- ============================================
CREATE TABLE Actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500),
    duracion_horas INT NOT NULL,
    precio_base DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    destino_id INT NOT NULL,
    FOREIGN KEY (destino_id) REFERENCES Destinos(id) ON DELETE CASCADE,
    INDEX idx_destino (destino_id)
) ENGINE=InnoDB;

-- ============================================
-- Tabla: PoliticasCancelacion
-- Políticas de cancelación para paquetes
-- ============================================
CREATE TABLE PoliticasCancelacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre ENUM('Flexible', 'Estricta') NOT NULL UNIQUE,
    dias_aviso INT NOT NULL,
    porcentaje_reembolso INT NOT NULL,
    CHECK (dias_aviso > 0),
    CHECK (porcentaje_reembolso >= 0 AND porcentaje_reembolso <= 100)
) ENGINE=InnoDB;

-- ============================================
-- Tabla: Paquetes
-- Paquetes turísticos disponibles
-- ============================================
CREATE TABLE Paquetes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NOT NULL,
    precio_total DECIMAL(10,2) NOT NULL,
    cupos_disponibles INT NOT NULL,
    politica_id INT NOT NULL,
    FOREIGN KEY (politica_id) REFERENCES PoliticasCancelacion(id),
    CHECK (fecha_fin > fecha_inicio),
    CHECK (cupos_disponibles >= 0),
    CHECK (precio_total >= 0),
    INDEX idx_fechas (fecha_inicio, fecha_fin),
    INDEX idx_disponibilidad (cupos_disponibles)
) ENGINE=InnoDB;

-- ============================================
-- Tabla: Paquete_Destino
-- Relación muchos a muchos entre Paquetes y Destinos
-- ============================================
CREATE TABLE Paquete_Destino (
    paquete_id INT NOT NULL,
    destino_id INT NOT NULL,
    orden_visita INT NOT NULL,
    PRIMARY KEY (paquete_id, destino_id),
    FOREIGN KEY (paquete_id) REFERENCES Paquetes(id) ON DELETE CASCADE,
    FOREIGN KEY (destino_id) REFERENCES Destinos(id) ON DELETE CASCADE,
    INDEX idx_paquete (paquete_id),
    INDEX idx_destino (destino_id)
) ENGINE=InnoDB;

-- ============================================
-- Tabla: Reservas
-- Reservas de paquetes realizadas por clientes
-- ============================================
CREATE TABLE Reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_reserva DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('PENDIENTE', 'CONFIRMADA', 'CANCELADA', 'PAGADA') NOT NULL DEFAULT 'PENDIENTE',
    monto_total DECIMAL(10,2) NOT NULL,
    numero_personas INT NOT NULL,
    usuario_id INT NOT NULL,
    paquete_id INT NULL,
    destino_id INT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (paquete_id) REFERENCES Paquetes(id) ON DELETE CASCADE,
    FOREIGN KEY (destino_id) REFERENCES Destinos(id) ON DELETE CASCADE,
    CHECK (monto_total >= 0),
    CHECK (numero_personas > 0),
    CHECK ((paquete_id IS NOT NULL AND destino_id IS NULL) OR (paquete_id IS NULL AND destino_id IS NOT NULL)),
    INDEX idx_usuario (usuario_id),
    INDEX idx_paquete (paquete_id),
    INDEX idx_destino (destino_id),
    INDEX idx_estado (estado),
    INDEX idx_fecha (fecha_reserva)
) ENGINE=InnoDB;

-- ============================================
-- Tabla: Pagos
-- Registro de pagos asociados a reservas
-- ============================================
CREATE TABLE Pagos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    monto DECIMAL(10,2) NOT NULL,
    fecha_pago DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metodo ENUM('EFECTIVO', 'TARJETA', 'TRANSFERENCIA') NOT NULL,
    estado ENUM('PENDIENTE', 'COMPLETADO', 'FALLIDO') NOT NULL DEFAULT 'PENDIENTE',
    reserva_id INT NOT NULL,
    FOREIGN KEY (reserva_id) REFERENCES Reservas(id) ON DELETE CASCADE,
    CHECK (monto > 0),
    INDEX idx_reserva (reserva_id),
    INDEX idx_estado (estado),
    INDEX idx_fecha (fecha_pago)
) ENGINE=InnoDB;

-- ============================================
-- Inserción de datos iniciales
-- ============================================

-- Políticas de cancelación
INSERT INTO PoliticasCancelacion (nombre, dias_aviso, porcentaje_reembolso) VALUES
('Flexible', 7, 100),
('Estricta', 30, 50);

-- Usuario administrador por defecto
-- Contraseña: admin123 (debe hashearse en la aplicación)
INSERT INTO Usuarios (email, password_hash, nombre, rol) VALUES
('admin@viajes-aventura.com', 'hash_aqui', 'Administrador', 'ADMIN');

-- Destinos de ejemplo
INSERT INTO Destinos (nombre, descripcion, costo_base, cupos_disponibles) VALUES
('París', 'La ciudad de la luz, famosa por la Torre Eiffel y el Louvre', 1200.00, 50),
('Roma', 'Ciudad histórica con el Coliseo y el Vaticano', 1000.00, 50),
('Barcelona', 'Ciudad mediterránea con arquitectura de Gaudí', 800.00, 50),
('Tokio', 'Metrópolis moderna con tradición japonesa', 1800.00, 50);

-- Actividades de ejemplo
INSERT INTO Actividades (nombre, descripcion, duracion_horas, precio_base, destino_id) VALUES
-- París
('Tour Eiffel con cena', 'Visita guiada a la Torre Eiffel con cena romántica en restaurante panorámico', 4, 150.00, 1),
('Museo del Louvre', 'Recorrido por las obras maestras del museo más famoso del mundo', 3, 80.00, 1),
('Crucero por el Sena', 'Paseo en barco por el río Sena con vistas a monumentos parisinos', 2, 120.00, 1),
-- Roma
('Tour del Coliseo', 'Visita guiada al Coliseo Romano y Foro Romano con historiador', 3, 100.00, 2),
('Visita al Vaticano', 'Recorrido por los Museos Vaticanos y Capilla Sixtina', 4, 90.00, 2),
('Clase de cocina italiana', 'Aprende a preparar pasta fresca y platos tradicionales italianos', 3, 110.00, 2),
-- Barcelona
('Tour Sagrada Familia', 'Visita guiada a la obra maestra de Gaudí con acceso prioritario', 2, 95.00, 3),
('Park Güell', 'Recorrido por el parque modernista diseñado por Antoni Gaudí', 2, 70.00, 3),
('Degustación de tapas', 'Tour gastronómico por los mejores bares de tapas del barrio Gótico', 3, 85.00, 3),
-- Tokio
('Tour templos tradicionales', 'Visita a templos históricos de Asakusa y jardines zen', 4, 130.00, 4),
('Experiencia de sushi', 'Clase magistral de preparación de sushi con chef profesional', 2, 140.00, 4),
('Visita Monte Fuji', 'Excursión de día completo al Monte Fuji y lago Kawaguchi', 8, 200.00, 4);

-- Paquete de ejemplo
INSERT INTO Paquetes (nombre, descripcion, fecha_inicio, fecha_fin, precio_total, cupos_disponibles, politica_id) VALUES
('Europa Clásica', 'Recorre las principales capitales europeas: París, Roma, Londres y Madrid', '2025-06-01 09:00:00', '2025-06-15 18:00:00', 3500.00, 20, 1),
('Tour Mediterráneo', 'Disfruta del sol y las playas de Grecia, Italia y España', '2025-07-10 10:00:00', '2025-07-20 16:00:00', 2800.00, 15, 2),
('Aventura Asiática', 'Explora la cultura milenaria de Japón, China y Tailandia', '2025-08-05 08:00:00', '2025-08-18 20:00:00', 4200.00, 12, 1);

-- Relación Paquetes-Destinos
INSERT INTO Paquete_Destino (paquete_id, destino_id, orden_visita) VALUES
-- Europa Clásica: París -> Roma -> Barcelona
(1, 1, 1),
(1, 2, 2),
(1, 3, 3),
-- Tour Mediterráneo: Roma -> Barcelona
(2, 2, 1),
(2, 3, 2),
-- Aventura Asiática: Tokio
(3, 4, 1);

-- ============================================
-- Vistas útiles
-- ============================================

-- Vista: Paquetes con información completa
CREATE VIEW Vista_Paquetes_Completos AS
SELECT 
    p.id,
    p.nombre,
    p.fecha_inicio,
    p.fecha_fin,
    p.precio_total,
    p.cupos_disponibles,
    pc.nombre AS politica_cancelacion,
    pc.dias_aviso,
    pc.porcentaje_reembolso,
    GROUP_CONCAT(d.nombre ORDER BY pd.orden_visita SEPARATOR ' → ') AS ruta_destinos
FROM Paquetes p
JOIN PoliticasCancelacion pc ON p.politica_id = pc.id
LEFT JOIN Paquete_Destino pd ON p.id = pd.paquete_id
LEFT JOIN Destinos d ON pd.destino_id = d.id
GROUP BY p.id, p.nombre, p.fecha_inicio, p.fecha_fin, p.precio_total, 
         p.cupos_disponibles, pc.nombre, pc.dias_aviso, pc.porcentaje_reembolso;

-- Vista: Reservas con información del cliente y paquete
CREATE VIEW Vista_Reservas_Detalladas AS
SELECT 
    r.id AS reserva_id,
    r.fecha_reserva,
    r.estado AS estado_reserva,
    r.monto_total,
    r.numero_personas,
    u.nombre AS cliente_nombre,
    u.email AS cliente_email,
    p.nombre AS paquete_nombre,
    p.fecha_inicio AS fecha_viaje_inicio,
    p.fecha_fin AS fecha_viaje_fin,
    COALESCE(SUM(pg.monto), 0) AS total_pagado,
    (r.monto_total - COALESCE(SUM(pg.monto), 0)) AS saldo_pendiente
FROM Reservas r
JOIN Usuarios u ON r.usuario_id = u.id
JOIN Paquetes p ON r.paquete_id = p.id
LEFT JOIN Pagos pg ON r.id = pg.reserva_id AND pg.estado = 'COMPLETADO'
GROUP BY r.id, r.fecha_reserva, r.estado, r.monto_total, r.numero_personas,
         u.nombre, u.email, p.nombre, p.fecha_inicio, p.fecha_fin;

-- ============================================
-- Triggers para lógica de negocio
-- ============================================

DELIMITER $$

-- Trigger: Reducir cupos al crear reserva confirmada
CREATE TRIGGER trg_reducir_cupos_reserva
AFTER INSERT ON Reservas
FOR EACH ROW
BEGIN
    IF NEW.estado IN ('CONFIRMADA', 'PAGADA') THEN
        UPDATE Paquetes 
        SET cupos_disponibles = cupos_disponibles - 1
        WHERE id = NEW.paquete_id AND cupos_disponibles > 0;
    END IF;
END$$

-- Trigger: Restaurar cupos al cancelar reserva
CREATE TRIGGER trg_restaurar_cupos_cancelacion
AFTER UPDATE ON Reservas
FOR EACH ROW
BEGIN
    IF OLD.estado IN ('CONFIRMADA', 'PAGADA') AND NEW.estado = 'CANCELADA' THEN
        UPDATE Paquetes 
        SET cupos_disponibles = cupos_disponibles + 1
        WHERE id = NEW.paquete_id;
    END IF;
END$$

-- Trigger: Validar cupos antes de confirmar reserva
CREATE TRIGGER trg_validar_cupos_antes_confirmar
BEFORE UPDATE ON Reservas
FOR EACH ROW
BEGIN
    DECLARE cupos_actuales INT;
    
    IF OLD.estado = 'PENDIENTE' AND NEW.estado IN ('CONFIRMADA', 'PAGADA') THEN
        SELECT cupos_disponibles INTO cupos_actuales
        FROM Paquetes 
        WHERE id = NEW.paquete_id;
        
        IF cupos_actuales <= 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No hay cupos disponibles para este paquete';
        END IF;
    END IF;
END$$

DELIMITER ;

-- ============================================
-- Consultas útiles para verificación
-- ============================================

-- Mostrar todos los paquetes con sus destinos
SELECT * FROM Vista_Paquetes_Completos;

-- Mostrar estructura de todas las tablas
SHOW TABLES;

-- Verificar políticas de cancelación
SELECT * FROM PoliticasCancelacion;

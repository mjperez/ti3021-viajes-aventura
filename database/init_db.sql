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
    rut VARCHAR(12) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    rol ENUM('ADMIN', 'CLIENTE') NOT NULL DEFAULT 'CLIENTE',
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_rut (rut),
    INDEX idx_email (email),
    INDEX idx_rol (rol)
) ENGINE=InnoDB;

-- ============================================
-- Tabla: PoliticasCancelacion
-- Políticas de cancelación para paquetes y destinos
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
-- Tabla: Destinos
-- Información de destinos turísticos
-- ============================================
CREATE TABLE Destinos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500) NOT NULL,
    costo_base INT NOT NULL,
    cupos_disponibles INT NOT NULL DEFAULT 50 CHECK (cupos_disponibles >= 0),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    politica_id INT NOT NULL DEFAULT 1,
    FOREIGN KEY (politica_id) REFERENCES PoliticasCancelacion(id),
    INDEX idx_nombre (nombre),
    INDEX idx_activo (activo)
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
    precio_base INT NOT NULL DEFAULT 0,
    destino_id INT NOT NULL,
    FOREIGN KEY (destino_id) REFERENCES Destinos(id) ON DELETE CASCADE,
    INDEX idx_destino (destino_id)
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
    precio_total INT NOT NULL,
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
    monto_total INT NOT NULL,
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
    monto INT NOT NULL,
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
-- Credenciales: admin@viajes-aventura.com / Admin123
INSERT INTO Usuarios (rut, email, password_hash, nombre, rol) VALUES
('99.999.999-9', 'admin@viajes-aventura.com', '$2b$12$MmQxlm77yoa.XQMHKDWffeU0KJB28f/.NDBXHG4gAu4qb4QuyTRTy', 'Administrador', 'ADMIN');

-- Destinos de ejemplo (con politica de cancelacion)
-- Precios en pesos chilenos
INSERT INTO Destinos (nombre, descripcion, costo_base, cupos_disponibles, politica_id) VALUES
('Paris', 'La ciudad de la luz, famosa por la Torre Eiffel y el Louvre', 850000, 50, 1),
('Roma', 'Ciudad historica con el Coliseo y el Vaticano', 720000, 50, 1),
('Barcelona', 'Ciudad mediterranea con arquitectura de Gaudi', 580000, 50, 2),
('Tokio', 'Metropolis moderna con tradicion japonesa', 1250000, 50, 2);

-- Actividades de ejemplo
-- Precios en pesos chilenos
INSERT INTO Actividades (nombre, descripcion, duracion_horas, precio_base, destino_id) VALUES
-- Paris
('Tour Eiffel con cena', 'Visita guiada a la Torre Eiffel con cena romantica en restaurante panoramico', 4, 95000, 1),
('Museo del Louvre', 'Recorrido por las obras maestras del museo mas famoso del mundo', 3, 45000, 1),
('Crucero por el Sena', 'Paseo en barco por el rio Sena con vistas a monumentos parisinos', 2, 72000, 1),
-- Roma
('Tour del Coliseo', 'Visita guiada al Coliseo Romano y Foro Romano con historiador', 3, 58000, 2),
('Visita al Vaticano', 'Recorrido por los Museos Vaticanos y Capilla Sixtina', 4, 52000, 2),
('Clase de cocina italiana', 'Aprende a preparar pasta fresca y platos tradicionales italianos', 3, 65000, 2),
-- Barcelona
('Tour Sagrada Familia', 'Visita guiada a la obra maestra de Gaudi con acceso prioritario', 2, 55000, 3),
('Park Guell', 'Recorrido por el parque modernista disenado por Antoni Gaudi', 2, 38000, 3),
('Degustacion de tapas', 'Tour gastronomico por los mejores bares de tapas del barrio Gotico', 3, 48000, 3),
-- Tokio
('Tour templos tradicionales', 'Visita a templos historicos de Asakusa y jardines zen', 4, 78000, 4),
('Experiencia de sushi', 'Clase magistral de preparacion de sushi con chef profesional', 2, 85000, 4),
('Visita Monte Fuji', 'Excursion de dia completo al Monte Fuji y lago Kawaguchi', 8, 125000, 4);

-- Paquetes de ejemplo
-- Precios en pesos chilenos
INSERT INTO Paquetes (nombre, descripcion, fecha_inicio, fecha_fin, precio_total, cupos_disponibles, politica_id) VALUES
('Europa Clasica', 'Recorre las principales capitales europeas: Paris, Roma y Barcelona', '2025-06-01 09:00:00', '2025-06-15 18:00:00', 2450000, 20, 1),
('Tour Mediterraneo', 'Disfruta del sol y las playas del Mediterraneo visitando Italia y Espana', '2025-07-10 10:00:00', '2025-07-20 16:00:00', 1890000, 15, 2),
('Aventura Asiatica', 'Explora la cultura milenaria de Japon con templos y gastronomia', '2025-08-05 08:00:00', '2025-08-18 20:00:00', 2980000, 12, 1),
('Escapada Paris', 'Fin de semana romantico en la ciudad del amor', '2025-05-15 09:00:00', '2025-05-18 18:00:00', 980000, 30, 1),
('Roma Imperial', 'Viaje cultural por la Roma antigua y el Vaticano', '2025-09-01 08:00:00', '2025-09-07 20:00:00', 1250000, 25, 2);

-- Relacion Paquetes-Destinos
INSERT INTO Paquete_Destino (paquete_id, destino_id, orden_visita) VALUES
-- Europa Clasica: Paris -> Roma -> Barcelona
(1, 1, 1),
(1, 2, 2),
(1, 3, 3),
-- Tour Mediterraneo: Roma -> Barcelona
(2, 2, 1),
(2, 3, 2),
-- Aventura Asiatica: Tokio
(3, 4, 1),
-- Escapada Paris: Paris
(4, 1, 1),
-- Roma Imperial: Roma
(5, 2, 1);

-- ============================================
-- Usuarios cliente de ejemplo para demo
-- Password para todos: Cliente123
-- ============================================
INSERT INTO Usuarios (rut, email, password_hash, nombre, rol) VALUES
('11.111.111-1', 'maria.gonzalez@email.com', '$2b$12$MmQxlm77yoa.XQMHKDWffeU0KJB28f/.NDBXHG4gAu4qb4QuyTRTy', 'Maria Gonzalez', 'CLIENTE'),
('22.222.222-2', 'juan.perez@email.com', '$2b$12$MmQxlm77yoa.XQMHKDWffeU0KJB28f/.NDBXHG4gAu4qb4QuyTRTy', 'Juan Perez', 'CLIENTE'),
('33.333.333-3', 'ana.martinez@email.com', '$2b$12$MmQxlm77yoa.XQMHKDWffeU0KJB28f/.NDBXHG4gAu4qb4QuyTRTy', 'Ana Martinez', 'CLIENTE');

-- ============================================
-- Reservas de ejemplo para demo
-- Montos en pesos chilenos
-- ============================================
INSERT INTO Reservas (fecha_reserva, estado, monto_total, numero_personas, usuario_id, paquete_id, destino_id) VALUES
-- Maria Gonzalez: Reserva confirmada de Europa Clasica (2 personas)
('2025-01-15 10:30:00', 'CONFIRMADA', 4900000, 2, 2, 1, NULL),
-- Maria Gonzalez: Reserva pendiente de destino Paris (1 persona)
('2025-02-20 14:15:00', 'PENDIENTE', 850000, 1, 2, NULL, 1),
-- Juan Perez: Reserva pagada de Tour Mediterraneo (3 personas)
('2025-02-01 09:00:00', 'PAGADA', 5670000, 3, 3, 2, NULL),
-- Juan Perez: Reserva cancelada de Aventura Asiatica
('2025-01-10 16:45:00', 'CANCELADA', 2980000, 1, 3, 3, NULL),
-- Ana Martinez: Reserva confirmada de Escapada Paris (2 personas)
('2025-03-05 11:20:00', 'CONFIRMADA', 1960000, 2, 4, 4, NULL),
-- Ana Martinez: Reserva pendiente de destino Barcelona
('2025-03-10 08:30:00', 'PENDIENTE', 1160000, 2, 4, NULL, 3);

-- ============================================
-- Pagos de ejemplo para demo
-- Montos en pesos chilenos
-- ============================================
INSERT INTO Pagos (monto, fecha_pago, metodo, estado, reserva_id) VALUES
-- Pago completo de Maria (reserva 1 - Europa Clasica)
(4900000, '2025-01-15 11:00:00', 'TARJETA', 'COMPLETADO', 1),
-- Pago parcial de Juan (reserva 3 - Tour Mediterraneo)
(2835000, '2025-02-01 10:00:00', 'TRANSFERENCIA', 'COMPLETADO', 3),
(2835000, '2025-02-05 10:00:00', 'TRANSFERENCIA', 'COMPLETADO', 3),
-- Pago de Ana (reserva 5 - Escapada Paris)
(1960000, '2025-03-05 12:00:00', 'EFECTIVO', 'COMPLETADO', 5);

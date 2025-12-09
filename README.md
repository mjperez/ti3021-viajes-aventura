# Sistema de Reservas - Viajes Aventura 🌍✈️

Este proyecto es una aplicación de consola para la gestión de reservas de paquetes turísticos y destinos.

## Cómo Ejecutar el Proyecto

1. **Requisitos Previos**:
   - Python 3.10+
   - Servidor MySQL (WAMP/XAMPP/MySQL WorkBench) en puerto 3306.
   - Base de datos inicializada con `database/init_db.sql`.

2. **Instalación de Dependencias**:
   ```bash
   pip install pymysql python-dotenv bcrypt cryptography
   ```

3. **Ejecución**:
   ```bash
   python main.py
   ```

## Credenciales de Acceso

El sistema cuenta con dos roles principales:

### 1. Administrador
Acceso total para gestionar usuarios, reservas, paquetes y reportes.
- **Email**: `admin@viajes-aventura.com`
- **Contraseña**: `Admin123`

### 2. Clientes (Demo)
Usuarios que pueden buscar viajes, reservar y pagar.
- **Usuario 1**: `maria.gonzalez@email.com` / `Cliente123`
- **Usuario 2**: `juan.perez@email.com` / `Cliente123`

## Glosario de Estados y Entidades

### Estados de Reserva
El ciclo de vida de una reserva pasa por los siguientes estados:

1. **PENDIENTE**: La reserva ha sido creada por el cliente, pero aún no se ha registrado ningún pago. Ocupa cupos temporalmente.
2. **PAGADA**: El cliente ha registrado el pago. La reserva está en espera de confirmación administrativa.
3. **CONFIRMADA**: El administrador ha verificado el pago y confirmado la reserva. El viaje está asegurado.
4. **CANCELADA**: La reserva ha sido anulada (por el cliente o el admin). Se liberan los cupos. Si estaba pagada, aplica política de reembolso.

### Estructura de Viajes
- **Destino**: Un lugar específico (ej: París, Roma). Tiene un costo base y actividades asociadas.
- **Actividad**: Experiencias complementarias en un destino (ej: Tour Torre Eiffel).
- **Paquete**: Un conjunto de destinos organizados por fechas (ej: "Europa Clásica"). Incluye transporte y alojamiento en el precio total.

### Políticas de Cancelación
Cada paquete o destino tiene una política que define cuánto dinero se devuelve al cancelar:
- **Flexible**: Permite cancelar hasta 3 días antes con **100% de reembolso**.
- **Estricta**: Requiere 7 días de aviso y solo reembolsa el **50%**.

## Tecnologías Usadas
- **Lenguaje**: Python
- **Base de Datos**: MySQL
- **Librerías Clave**: 
  - `pymysql` (Conexión DB)
  - `bcrypt` (Seguridad y Hashing de contraseñas)

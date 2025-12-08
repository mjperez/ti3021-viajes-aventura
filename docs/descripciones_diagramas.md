# Descripciones de Diagramas - Viajes Aventura

## 1. Diagrama de Clases UML

### Descripción General

El diagrama de clases representa la estructura del sistema "Viajes Aventura" utilizando los cuatro pilares fundamentales de la Programación Orientada a Objetos (POO): **Abstracción**, **Encapsulación**, **Herencia** y **Polimorfismo**.

### Estructura del Diagrama

El diagrama está organizado en cuatro capas principales que siguen el patrón de arquitectura en capas:

#### 1. Patrón de Herencia - Políticas de Cancelación

Esta sección ilustra los conceptos de **Abstracción**, **Herencia** y **Polimorfismo**:

- **`PoliticaCancelacion`** es una **clase abstracta** que define el "contrato" o plantilla que deben seguir todas las políticas de cancelación. Contiene atributos protegidos (marcados con `#`) como `nombre`, `dias_aviso` y `porcentaje_reembolso`, además de un método abstracto `calcular_monto_reembolso()` que debe ser implementado por las clases hijas.

- **`PoliticaFlexible`** y **`PoliticaEstricta`** son **clases concretas** que heredan de `PoliticaCancelacion`. Cada una implementa el método `calcular_monto_reembolso()` de manera diferente:
  - *Flexible*: Requiere 3 días de aviso y reembolsa el 100%
  - *Estricta*: Requiere 7 días de aviso y reembolsa solo el 50%

- Las flechas con triángulo vacío (`◁──`) representan la **relación de herencia**, indicando que las subclases "extienden" la clase padre.

#### 2. Capa de Servicios (Business)

Esta capa demuestra el principio de **Encapsulación**:

- **`AuthService`**: Servicio de autenticación que contiene métodos privados (marcados con `-`) como `_hashear_password()` y `_verificar_password()`. Estos métodos ocultan la complejidad del manejo de contraseñas, exponiendo solo las funciones públicas `login()` y `registrar_usuario()`.

- **`ReservaService`**: Gestiona las reservas y utiliza **polimorfismo** al trabajar con `PoliticaCancelacion`. Cuando calcula reembolsos, llama al método `calcular_monto_reembolso()` sin importar si la política es Flexible o Estricta; el comportamiento correcto se ejecuta automáticamente según el tipo real del objeto.

- **`PaqueteService`** y **`DestinoService`**: Manejan la lógica de negocio para paquetes turísticos y destinos respectivamente.

#### 3. Capa DTO (Data Transfer Objects)

Los DTOs son objetos simples que transportan datos entre capas:

- **`UsuarioDTO`**, **`ReservaDTO`**, **`PaqueteDTO`**, **`DestinoDTO`**: Cada uno contiene atributos públicos (marcados con `+`) que representan los datos de una entidad. No contienen lógica de negocio, solo datos.

#### 4. Capa DAO (Data Access Objects)

Los DAOs manejan la comunicación con la base de datos:

- **`UsuarioDAO`**, **`ReservaDAO`**, **`PaqueteDAO`**, **`DestinoDAO`**: Cada uno proporciona métodos CRUD (Crear, Leer, Actualizar, Eliminar) para su entidad correspondiente.

### Relaciones en el Diagrama

- **Flecha sólida (`→`)**: Indica dependencia o uso directo (ej: `AuthService → UsuarioDAO`)
- **Flecha punteada (`⇢`)**: Indica que un método retorna o usa ese tipo (ej: `AuthService ⇢ UsuarioDTO`)
- **Flecha con triángulo (`◁──`)**: Indica herencia

### Conceptos POO Demostrados

| Concepto | Ejemplo en el Diagrama |
|----------|------------------------|
| **Abstracción** | `PoliticaCancelacion` define un contrato abstracto sin implementación completa |
| **Encapsulación** | `AuthService` oculta `_hashear_password()` como método privado |
| **Herencia** | `PoliticaFlexible` y `PoliticaEstricta` heredan de `PoliticaCancelacion` |
| **Polimorfismo** | `ReservaService` usa `calcular_monto_reembolso()` sin conocer el tipo concreto |

---

## 2. Diagrama Entidad-Relación (ER)

### Descripción General

El diagrama Entidad-Relación representa la estructura de la base de datos del sistema "Viajes Aventura". Muestra las **entidades** (tablas), sus **atributos** (columnas) y las **relaciones** entre ellas.

### Entidades del Sistema

#### 1. Usuarios
Almacena la información de todos los usuarios del sistema (clientes y administradores).
- **Atributos clave**: `id` (clave primaria), `rut` y `email` (únicos), `password_hash` (contraseña encriptada), `rol` (ADMIN o CLIENTE)
- **Propósito**: Gestionar acceso y autenticación al sistema

#### 2. PoliticasCancelacion
Define las reglas para cancelar reservas.
- **Atributos clave**: `nombre` (Flexible o Estricta), `dias_aviso` (días mínimos de anticipación), `porcentaje_reembolso`
- **Propósito**: Determinar cuánto se reembolsa según la anticipación de la cancelación

#### 3. Destinos
Representa los lugares turísticos disponibles.
- **Atributos clave**: `nombre`, `descripcion`, `costo_base`, `cupos_disponibles`, `politica_id` (referencia a PoliticasCancelacion)
- **Propósito**: Catálogo de destinos que los clientes pueden reservar

#### 4. Actividades
Actividades disponibles en cada destino.
- **Atributos clave**: `nombre`, `duracion_horas`, `precio_base`, `destino_id` (referencia a Destinos)
- **Propósito**: Complementar la oferta de cada destino

#### 5. Paquetes
Ofertas turísticas con fechas específicas que incluyen destinos y actividades.
- **Atributos clave**: `nombre`, `fecha_inicio`, `fecha_fin`, `precio_total`, `politica_id`
- **Propósito**: Agrupar destinos en ofertas con fechas definidas

#### 6. Paquete_Destino (Tabla Intermedia)
Relaciona paquetes con destinos (relación muchos-a-muchos).
- **Atributos clave**: `paquete_id`, `destino_id` (ambos forman la clave primaria compuesta), `orden_visita`
- **Propósito**: Permitir que un paquete incluya múltiples destinos

#### 7. Reservas
Registro de reservas realizadas por los clientes.
- **Atributos clave**: `estado` (PENDIENTE, PAGADA, CONFIRMADA, CANCELADA, COMPLETADA), `monto_total`, `numero_personas`, `usuario_id`, `paquete_id` o `destino_id`
- **Propósito**: Controlar el ciclo de vida de cada reserva

#### 8. Pagos
Historial de pagos realizados.
- **Atributos clave**: `monto`, `metodo` (EFECTIVO, TARJETA, TRANSFERENCIA), `estado`, `reserva_id`
- **Propósito**: Registrar transacciones financieras

### Tipos de Relaciones

#### Uno a Muchos (1:N)
Representadas con línea que tiene un extremo con "1" y otro con "N" o "cuervo":

- **Usuarios → Reservas**: Un usuario puede tener muchas reservas, pero cada reserva pertenece a un solo usuario
- **Destinos → Actividades**: Un destino puede tener muchas actividades, pero cada actividad pertenece a un solo destino
- **Reservas → Pagos**: Una reserva puede tener múltiples pagos (ej: pagos parciales)
- **PoliticasCancelacion → Destinos/Paquetes**: Una política puede aplicar a múltiples destinos o paquetes

#### Muchos a Muchos (N:M)
Implementada mediante tabla intermedia:

- **Paquetes ↔ Destinos**: Un paquete puede incluir varios destinos, y un destino puede estar en varios paquetes. La tabla `Paquete_Destino` resuelve esta relación.

### Notación del Diagrama

| Símbolo | Significado |
|---------|-------------|
| **PK** | Clave Primaria (Primary Key) - Identificador único |
| **FK** | Clave Foránea (Foreign Key) - Referencia a otra tabla |
| **UK** | Clave Única (Unique Key) - Valor no repetible |
| `*` | Campo obligatorio (NOT NULL) |
| `||--o{` | Relación uno a muchos |

### Integridad Referencial

Las claves foráneas aseguran la **integridad referencial** del sistema:
- No se puede crear una reserva para un usuario que no existe
- No se puede asociar una actividad a un destino inexistente
- Al eliminar un destino, se deben considerar las actividades y reservas asociadas

---

## Resumen

Ambos diagramas representan el sistema desde perspectivas complementarias:

| Aspecto | Diagrama de Clases | Diagrama ER |
|---------|-------------------|-------------|
| **Enfoque** | Estructura del código | Estructura de datos |
| **Muestra** | Clases, métodos, relaciones de herencia | Tablas, columnas, relaciones de base de datos |
| **Conceptos** | POO (herencia, encapsulación, polimorfismo) | Modelo relacional (claves, relaciones) |
| **Usado por** | Desarrolladores de software | Diseñadores de base de datos |
| **Herramienta** | UML (Unified Modeling Language) | Notación ER (Chen o Crow's Foot) |

Juntos, estos diagramas proporcionan una visión completa de cómo está estructurado el sistema "Viajes Aventura", tanto a nivel de programación como de almacenamiento de datos.

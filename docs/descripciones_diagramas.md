# Descripciones de Diagramas - Viajes Aventura

## 1. Diagrama de Clases UML

### Descripción General

El diagrama de clases representa la estructura del sistema "Viajes Aventura" utilizando los cuatro pilares fundamentales de la Programación Orientada a Objetos (POO): **Abstracción**, **Encapsulación**, **Herencia** y **Polimorfismo**.

### Estructura del Diagrama

El diagrama está organizado en cuatro capas principales que siguen el patrón de arquitectura en capas:

#### 1. Patrón de Herencia - Políticas de Cancelación

Esta sección ilustra los conceptos de **Abstracción**, **Herencia** y **Polimorfismo**:

- **`PoliticaCancelacion`** es una **clase abstracta** que define el "contrato" o plantilla que deben seguir todas las políticas de cancelación. Contiene atributos protegidos (marcados con `#`) y un método abstracto `calcular_monto_reembolso()`.

- **`PoliticaFlexible`** y **`PoliticaEstricta`** son **clases concretas** que heredan de `PoliticaCancelacion`. Implementan comportamientos específicos para el reembolso.

- Las flechas con triángulo vacío (`◁──`) representan la **relación de herencia**.

#### 2. Capa de Servicios (Business)

Esta capa demuestra el principio de **Encapsulación** y manejo de lógica de negocio:

- **`AuthService`**: Gestiona la autenticación con métodos privados para la seguridad de contraseñas.
- **`ReservaService`**: Utiliza **polimorfismo** con `PoliticaCancelacion` para calcular reembolsos.
- **`PaqueteService`**: Gestiona paquetes y coordina con `PaqueteActividadDAO` para la asignación de actividades.
- **`DestinoService`** y **`ActividadService`**: Manejan la lógica para destinos y actividades turísticas.

#### 3. Capa DTO (Data Transfer Objects)

Transportan datos entre capas sin lógica de negocio:
- **`UsuarioDTO`**, **`ReservaDTO`**, **`PaqueteDTO`**, **`DestinoDTO`**, **`ActividadDTO`**.

#### 4. Capa DAO (Data Access Objects)

Manejan la comunicación con la base de datos y la persistencia:
- **`UsuarioDAO`**, **`ReservaDAO`**, **`PaqueteDAO`**, **`DestinoDAO`**, **`ActividadDAO`**.
- **`PaqueteActividadDAO`**: Gestiona la tabla intermedia para la relación muchos a muchos entre paquetes y actividades.
- Los DAOs implementan **Soft Delete** (eliminación lógica) actualizando el campo `activo` en lugar de borrar registros.

### Conceptos POO Demostrados

| Concepto | Ejemplo en el Diagrama |
|----------|------------------------|
| **Abstracción** | `PoliticaCancelacion` define contrato abstracto |
| **Encapsulación** | `AuthService` oculta implementación de seguridad |
| **Herencia** | Políticas concretas heredan de abstracta |
| **Polimorfismo** | `ReservaService` usa políticas sin conocer su tipo concreto |

---

## 2. Diagrama Entidad-Relación (ER)

### Descripción General

Representa la estructura de la base de datos relacional, incluyendo el soporte para **Soft Delete** y nuevas relaciones.

### Entidades Principales

#### 1. Entidades Base con Soft Delete
- **Destinos**, **Actividades**, **Paquetes**: Incluyen el campo `activo` (BOOLEAN) para permitir la desactivación temporal en lugar de eliminación física.

#### 2. Tablas Intermedias
- **Paquete_Destino**: Relación N:M entre Paquetes y Destinos.
- **Paquete_Actividad**: Nueva entidad para gestionar qué actividades específicas incluye un paquete, independiente del destino base.

#### 3. Gestión de Usuarios y Reservas
- **Usuarios**: Clientes y Administradores.
- **Reservas**: Ciclo de vida completo (Pendiente -> Pagada -> Confirmada).
- **Pagos**: Registro de transacciones.

### Relaciones Clave
- **Paquetes ↔ Actividades**: Relación muchos a muchos gestionada explícitamente.
- **Políticas ↔ Paquetes/Destinos**: Asignación de reglas de cancelación.

---

## 3. Diagramas de Flujo y Procesos

### Flujo Administrador
- Incluye el nuevo **Dashboard** de estadísticas.
- Muestra la gestión de **Políticas (Solo Lectura)**.
- Detalla la gestión específica de **Actividades por Paquete**.

### Flujo Cliente
- Muestra la capacidad de ver el **detalle completo** de paquetes, incluyendo actividades y precios desglosados.

### Procesos Específicos
- **Eliminar (Soft Delete)**: Los diagramas de proceso reflejan que la acción "Eliminar" ahora realiza una actualización del estado `activo = FALSE` en lugar de un `DELETE` SQL.

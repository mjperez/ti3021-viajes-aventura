# Flujo del Programa - Viajes Aventura

## 🏠 Menú Principal (Sin Sesión)

```
┌─────────────────────────────┐
│     VIAJES AVENTURA         │
│     Menú Principal          │
├─────────────────────────────┤
│ 1. Iniciar Sesión           │ → Ir a menú según rol
│ 2. Registrarse              │ → Crear cuenta cliente
│ 3. Ver Destinos Disponibles │ → Ver catálogo (sin login)
│ 4. Ver Paquetes Disponibles │ → Ver ofertas (sin login)
│ 5. Salir                    │
└─────────────────────────────┘
```

---

## 👤 FLUJO DEL CLIENTE

### Menú Principal Cliente
```
┌──────────────────────────────────────┐
│  CLIENTE: [Nombre del Usuario]       │
├──────────────────────────────────────┤
│ 1. Ver Destinos                      │
│ 2. Ver Paquetes                      │
│ 3. Realizar Reserva                  │
│ 4. Mis Reservas                      │
│ 5. Ver Políticas de Cancelación      │
│ 6. Cerrar Sesión                     │
└──────────────────────────────────────┘
```

### ¿Qué puede hacer el CLIENTE?

#### ✅ VER DESTINOS
- Lista todos los destinos disponibles
- Muestra: nombre, costo, cupos, política de cancelación

#### ✅ VER PAQUETES
- Lista todos los paquetes con cupos disponibles
- Muestra: nombre, precio, fechas, cupos, actividades incluidas

#### ✅ REALIZAR RESERVA
```
Paso 1: Elegir tipo
        ├── Destino Individual
        └── Paquete Turístico

Paso 2: Seleccionar destino/paquete por ID

Paso 3: Indicar número de personas

Paso 4: Confirmar reserva
        → Estado inicial: PENDIENTE
        → Se descuentan cupos automáticamente
```

#### ✅ MIS RESERVAS
```
┌─────────────────────────────────────┐
│ 1. Ver todas mis reservas           │ → Lista con estado
│ 2. Ver detalle de reserva           │ → Info completa
│ 3. Pagar reserva                    │ → Cambiar a PAGADA
│ 4. Cancelar reserva                 │ → Según política
│ 5. Volver                           │
└─────────────────────────────────────┘
```

##### Flujo de PAGO:
```
PENDIENTE → [Pagar] → PAGADA → [Admin confirma] → CONFIRMADA
```

##### Flujo de CANCELACIÓN:
```
Si días antes ≥ días_aviso de la política:
    → Reembolso según porcentaje_reembolso
    → Cupos devueltos
    
Si días antes < días_aviso:
    → Sin reembolso (o parcial)
    → Cupos devueltos
```

#### ✅ VER POLÍTICAS
- Muestra las políticas de cancelación disponibles
- Ejemplo: Flexible (3 días, 100%) vs Estricta (7 días, 50%)

---

## 🔧 FLUJO DEL ADMINISTRADOR

### Menú Principal Admin
```
┌──────────────────────────────────────┐
│  ADMIN: [Nombre del Admin]           │
├──────────────────────────────────────┤
│ 1. Destinos                          │
│ 2. Actividades                       │
│ 3. Paquetes                          │
│ 4. Reservas                          │
│ 5. Usuarios                          │
│ 6. Políticas de Cancelación          │
│ 7. Reportes                          │
│ 8. Cerrar Sesión                     │
└──────────────────────────────────────┘
```

### ¿Qué puede hacer el ADMINISTRADOR?

---

#### 1️⃣ GESTIÓN DE DESTINOS
```
┌─────────────────────────────────────┐
│ 1. Listar Destinos                  │
│ 2. Agregar Destino                  │ → nombre, descripción, costo, cupos, política
│ 3. Editar Destino                   │ → modificar cualquier campo
│ 4. Eliminar Destino                 │ → elimina permanentemente
│ 5. Volver                           │
└─────────────────────────────────────┘
```

---

#### 2️⃣ GESTIÓN DE ACTIVIDADES
```
┌─────────────────────────────────────┐
│ 1. Listar Actividades               │ → muestra nombre de destino
│ 2. Agregar Actividad                │ → elegir destino PRIMERO
│ 3. Editar Actividad                 │
│ 4. Eliminar Actividad               │
│ 5. Volver                           │
└─────────────────────────────────────┘

⚠️ Cada actividad está asociada a UN destino
```

---

#### 3️⃣ GESTIÓN DE PAQUETES
```
┌─────────────────────────────────────┐
│ 1. Listar Paquetes                  │ → con actividades y política
│ 2. Agregar Paquete                  │ → destino, fechas, precio, política
│ 3. Editar Paquete                   │
│ 4. Eliminar Paquete                 │
│ 5. Volver                           │
└─────────────────────────────────────┘

⚠️ VALIDA: fecha_inicio NO puede estar en el pasado
⚠️ VALIDA: fecha_fin debe ser posterior a fecha_inicio
```

**Estructura de un Paquete:**
```
PAQUETE
├── Nombre y descripción
├── Fecha inicio → Fecha fin
├── Precio total
├── Cupos disponibles
├── Política de cancelación (1=Flexible, 2=Estricta)
└── Destino(s) asociado(s)
    └── Actividades del destino
```

---

#### 4️⃣ GESTIÓN DE RESERVAS
```
┌─────────────────────────────────────────────────┐
│ 1. Ver Reservas Pagadas (pendientes confirmar)  │
│ 2. Confirmar Reserva Pagada                     │ → PAGADA → CONFIRMADA
│ 3. Cancelar Reserva                             │ → Sin aplicar política
│ 4. Ver todas las Reservas                       │ → Filtrar por estado
│ 5. Volver                                       │
└─────────────────────────────────────────────────┘
```

**Estados de Reserva:**
```
PENDIENTE → PAGADA → CONFIRMADA
     ↓         ↓
 CANCELADA  CANCELADA
```

---

#### 5️⃣ GESTIÓN DE USUARIOS
```
┌─────────────────────────────────────┐
│ 1. Ver todos los Usuarios           │
│ 2. Ver solo Clientes                │
│ 3. Ver solo Administradores         │
│ 4. Buscar Usuario por Email         │ → ¡Incluye sus reservas!
│ 5. Volver                           │
└─────────────────────────────────────┘
```

---

#### 6️⃣ GESTIÓN DE POLÍTICAS
```
┌─────────────────────────────────────┐
│ 1. Listar Políticas                 │
│ 2. Agregar Política                 │ → nombre, días_aviso, %reembolso
│ 3. Editar Política                  │
│ 4. Eliminar Política                │
│ 5. Volver                           │
└─────────────────────────────────────┘

Para cancelar: escribir 'cancelar' (NO usar 0)
```

---

#### 7️⃣ REPORTES
```
┌─────────────────────────────────────────────────────┐
│ 1. Ver todas las Reservas                           │ → Filtrar por estado
│ 2. Reporte de Ventas                                │ → Por rango de fechas
│ 3. Reporte de Clientes                              │ → Lista todos los clientes
│ 4. Volver                                           │
└─────────────────────────────────────────────────────┘
```

**Reporte de Ventas:**
- Muestra rango de fechas disponibles
- Valida formato YYYY-MM-DD
- Muestra: total pagos, monto total, detalle

---

## 🔄 DIAGRAMA DE FLUJO GENERAL

```
                    ┌─────────────────┐
                    │   INICIO        │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ ¿Tiene cuenta?  │
                    └────────┬────────┘
                     NO      │      SI
                ┌────────────┴────────────┐
                │                         │
        ┌───────▼───────┐        ┌───────▼───────┐
        │  Registrarse  │        │ Iniciar Sesión│
        │ (solo cliente)│        └───────┬───────┘
        └───────┬───────┘                 │
                │               ┌─────────┴─────────┐
                │               │                   │
        ┌───────▼───────┐  ┌────▼─────┐     ┌──────▼──────┐
        │ Menú Cliente  │  │ CLIENTE  │     │    ADMIN    │
        └───────────────┘  └────┬─────┘     └──────┬──────┘
                                │                   │
                    ┌───────────┴───────────┐      │
                    │                       │      │
            ┌───────▼───────┐       ┌───────▼───────┐
            │ Ver destinos/ │       │ Hacer reserva │
            │   paquetes    │       │ y pagarla     │
            └───────────────┘       └───────┬───────┘
                                            │
                                    ┌───────▼───────┐
                                    │ Admin confirma│
                                    │  la reserva   │
                                    └───────┬───────┘
                                            │
                                    ┌───────▼───────┐
                                    │   ¡VIAJE!     │
                                    └───────────────┘
```

---

## 📋 RESUMEN DE PERMISOS

| Acción                        | Cliente | Admin |
|-------------------------------|:------- |:----- |
| Ver destinos/paquetes         | ✅      | ✅    |
| Crear/editar destinos         | ❌      | ✅    |
| Crear/editar actividades      | ❌      | ✅    |
| Crear/editar paquetes         | ❌      | ✅    |
| Hacer reservas                | ✅      | ❌    |
| Pagar reservas                | ✅      | ❌    |
| Confirmar reservas            | ❌      | ✅    |
| Cancelar sus reservas         | ✅      | ❌    |
| Cancelar cualquier reserva    | ❌      | ✅    |
| Ver todos los usuarios        | ❌      | ✅    |
| Gestionar políticas           | ❌      | ✅    |
| Ver reportes                  | ❌      | ✅    |

---

## ⚠️ VALIDACIONES IMPORTANTES

1. **Fechas de paquetes**: No pueden estar en el pasado
2. **Cupos**: Se descuentan al reservar, se devuelven al cancelar
3. **Políticas**: Solo opciones 1 (Flexible) o 2 (Estricta)
4. **Campos vacíos**: Se validan antes de guardar
5. **Cancelaciones**: Dependen de la política y días de anticipación
6. **Passwords**: Se almacenan hasheados con bcrypt (seguros)

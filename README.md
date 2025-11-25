# Sistema de Reservas - Viajes Aventura

Proyecto de Programación Orientada a Objetos (POO) para gestión de una agencia de viajes.

## 📋 Descripción

Sistema de gestión de reservas turísticas desarrollado en Python con arquitectura DAO/DTO, autenticación segura mediante hash y conexión a base de datos MySQL.

## 🏗️ Arquitectura

- **DTO (Data Transfer Object)**: Objetos para transferencia de datos
- **DAO (Data Access Object)**: Acceso a la base de datos
- **Business**: Lógica de negocio
- **UI**: Interfaz de usuario por consola

## 🚀 Instalación

1. Clonar el repositorio
2. Crear entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar base de datos:
   - Crear base de datos en MySQL: `mysql -u root -p < database/crear_bd.sql`
   - Copiar `.env.example` a `.env` y configurar credenciales

5. Ejecutar:

```bash
python main.py
```

## 📁 Estructura del Proyecto

```
ti3021-viajes-ventura/
├── src/
│   ├── dto/              # Data Transfer Objects
│   ├── dao/              # Data Access Objects
│   ├── business/         # Lógica de negocio
│   ├── ui/               # Interfaz de usuario
│   ├── utils/            # Utilidades
│   └── config/           # Configuración
├── database/             # Scripts SQL
├── docs/                 # Documentación
├── logs/                 # Archivos de log
└── main.py              # Punto de entrada
```

## 👥 Autoras

- Maria Jesus Perez Casasbellas
- Maria Isabel Rubio Cienfuegos

## 📚 Asignatura

- **Código**: TI3021
- **Nombre**: Programación Orientada a Objetos Seguro
- **Carrera**: Analista Programador

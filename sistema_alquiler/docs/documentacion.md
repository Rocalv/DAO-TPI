# Sistema de Alquiler de Vehículos
**Documentación Técnica v1.0**

## 📋 Índice
1. [Información General](#información-general)
2. [Tecnologías Utilizadas](#tecnologías-utilizadas)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Estructura de Clases](#estructura-de-clases)
5. [Base de Datos](#base-de-datos)
6. [Casos de Uso](#casos-de-uso)
7. [Validaciones y Reglas de Negocio](#validaciones-y-reglas-de-negocio)

---

## 📌 Información General

### Objetivo del Sistema
Desarrollar una aplicación integral para la gestión de un negocio de alquiler de vehículos que permita:
- Administrar clientes, vehículos y empleados
- Gestionar alquileres con control de disponibilidad
- Registrar mantenimientos preventivos y correctivos
- Controlar multas y daños
- Generar reportes detallados y estadísticos

### Alcance Funcional
- **Módulo de Clientes**: ABM completo con validación de DNI único
- **Módulo de Vehículos**: Control de estado, disponibilidad y mantenimiento
- **Módulo de Empleados**: Gestión de personal activo
- **Módulo de Alquileres**: Transacción principal con cálculo automático de costos
- **Módulo de Mantenimiento**: Registro y seguimiento de servicios
- **Módulo de Multas**: Gestión de penalizaciones
- **Módulo de Reservas**: Sistema de reservas anticipadas
- **Módulo de Reportes**: Listados y estadísticas

---

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología | Versión |
|------------|------------|---------|
| Lenguaje | Python | 3.10+ |
| Framework UI | Flet | Latest |
| Base de Datos | SQLite | 3 |
| ORM/Database | sqlite3 (nativo) | - |

### Librerías Principales
```python
flet>=0.21.0
matplotlib>=3.7.0  # Para gráficos en reportes
reportlab>=4.0.0   # Para generación de PDFs
```

---

## 🏗️ Arquitectura del Sistema

### Programación Orientada a Objetos

```
┌─────────────────┐
│   Interfaz UI   │  (Flet - Vista)
│    (Views)      │
└────────┬────────┘
         │
┌────────▼────────┐
│     Models      │  (Clases de Negocio + Persistencia)
│  (Cliente,      │
│   Vehiculo,     │
│   Alquiler...)  │
└────────┬────────┘
         │
┌────────▼────────┐
│   SQLite DB     │  (Base de Datos)
└─────────────────┘
```

### Estructura de Directorios
```
sistema_alquiler/
├── main.py
├── backend/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db_config.py
│   │   └── crear_tablas.py
|   |   |__ alquiler.db
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cliente.py
│   │   ├── empleado.py
│   │   ├── vehiculo.py
│   │   ├── categoria.py
│   │   ├── alquiler.py
│   │   ├── mantenimiento.py
│   │   ├── multa.py
│   │   └── reserva.py
│   └── utils/
│       ├── __init__.py
│       ├── validaciones.py
│       └── reportes.py
├── frontend/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── main_view.py
│   │   ├── cliente_view.py
│   │   ├── vehiculo_view.py
│   │   ├── alquiler_view.py
│   │   └── reporte_view.py
│   └── components/
│       ├── __init__.py
│       └── widgets.py
└── docs/
    └── documentacion.md
```

---

## 🎯 Patrones de Diseño Aplicados

### 1. Patrón SINGLETON - Conexión a Base de Datos

Se utiliza el patrón SINGLETON para garantizar una única instancia de conexión a la base de datos en toda la aplicación.

**Problema que resuelve:**
- Evita múltiples conexiones simultáneas a SQLite
- Mejora el rendimiento reutilizando la conexión
- Previene problemas de concurrencia y bloqueos
- Centraliza la gestión de la conexión

**Implementación:**
```python
class DatabaseConnection:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect('alquiler.db')
        return self._connection
```

**Beneficios:**
- Una sola instancia en toda la aplicación
- Acceso global controlado a la BD
- Gestión eficiente de recursos

---

### 2. Patrón STATE - Estados del Vehículo

Se utiliza el patrón STATE para gestionar los diferentes estados de un vehículo de manera elegante y extensible.

**Diagrama de Estados:**
```
┌─────────────┐
│ Disponible  │ ◄──┐
└──────┬──────┘    │
       │           │
       ▼           │
┌─────────────┐    │
│  Alquilado  │ ───┘
└──────┬──────┘
       │
       ▼
┌─────────────┐    
│Mantenimiento│ ───┐
└──────┬──────┘    │
       │           │
       ▼           │
┌─────────────┐    │
│Fuera Servicio────┘
└─────────────┘
```

**Clases:**
```python
# Interfaz base
class EstadoVehiculo:
    def puede_alquilarse(self) -> bool: pass
    def puede_ir_a_mantenimiento(self) -> bool: pass
    def nombre_estado(self) -> str: pass

# Estados concretos
class EstadoDisponible(EstadoVehiculo): ...
class EstadoAlquilado(EstadoVehiculo): ...
class EstadoEnMantenimiento(EstadoVehiculo): ...
class EstadoFueraServicio(EstadoVehiculo): ...
```

**Beneficios:**
- Fácil agregar nuevos estados sin modificar Vehiculo
- Cada estado encapsula su comportamiento
- Transiciones de estado explícitas y controladas

---

## 📦 Estructura de Clases

### 1. Clase Cliente
**Ubicación**: `models/cliente.py`

```python
class Cliente:
    """
    Representa un cliente del sistema de alquiler.
    Contiene información personal y métodos para gestión de clientes.
    """
    
    # Atributos
    - id_cliente: int (PK, autoincremental)
    - nombre: str (max 100, requerido)
    - apellido: str (max 100, requerido)
    - dni: str (max 20, único, requerido)
    - telefono: str (max 20)
    - email: str (max 150)
    - direccion: str (max 200)
    - fecha_registro: date (auto)
    - activo: bool (default True)
    
```

---

### 2. Clase Empleado
**Ubicación**: `models/empleado.py`

```python
class Empleado:
    """
    Representa un empleado de la empresa de alquiler.
    """
    
    # Atributos
    - id_empleado: int (PK, autoincremental)
    - dni: str (max 20, único, requerido)
    - nombre: str (max 100, requerido)
    - apellido: str (max 100, requerido)
    - cargo: str (max 100)
    - telefono: str (max 20)
    - email: str (max 150)
    - activo: bool (default True)
    
```

---

### 3. Clase Categoria
**Ubicación**: `models/categoria.py`

```python
class Categoria:
    """
    Define categorías de vehículos con características comunes.
    """
    
    # Atributos
    - id_categoria: int (PK, autoincremental)
    - nombre: str (max 50, único, requerido)
    - descripcion: str (max 200)
    - precio_base: Decimal (requerido, > 0)
    - dias_mantenimiento: int (default 90)
    
```

**Ejemplos**: Económico, Sedan, SUV, Camioneta, Utilitario

---

### 4. Clase Vehiculo
**Ubicación**: `models/vehiculo.py`

```python
class Vehiculo:
    """
    Representa un vehículo disponible para alquiler.
    """
    
    # Atributos
    - id_vehiculo: int (PK, autoincremental)
    - patente: str (max 10, único, requerido)
    - marca: str (max 50, requerido)
    - modelo: str (max 50, requerido)
    - anio: int (requerido)
    - color: str (max 30)
    - precio_dia: Decimal (requerido, > 0)
    - estado: str (disponible|alquilado|mantenimiento|fuera_servicio)
    - disponible: bool (calculado)
    - kilometraje: int (default 0)
    - kilometraje_mantenimiento: int (próximo mantenimiento)
    - id_categoria: int (FK -> Categoria)
    
```

**Estados**: disponible, alquilado, mantenimiento, fuera_servicio

---

### 5. Clase Seguro
**Ubicación**: `models/seguro.py`

```python
class Seguro:
    """
    Define tipos de seguro para alquileres.
    """
    
    # Atributos
    - id_seguro: int (PK, autoincremental)
    - tipo: str (max 50, requerido)
    - cobertura: str (max 500)
    - costo_diario: Decimal (requerido, >= 0)
    - deducible: Decimal (default 0)
    
```

**Tipos**: Básico, Completo, Premium

---

### 6. Clase Alquiler (Transacción Principal)
**Ubicación**: `models/alquiler.py`

```python
class Alquiler:
    """
    Representa la transacción principal del sistema.
    Gestiona el alquiler de un vehículo por un cliente.
    """
    
    # Atributos
    - id_alquiler: int (PK, autoincremental)
    - fecha_inicio: date (requerido)
    - fecha_fin: date (requerido)
    - fecha_entrega_real: date (nullable)
    - costo_total: Decimal (calculado)
    - deposito: Decimal (requerido)
    - estado: str (pendiente|activo|finalizado|cancelado)
    - observaciones: str (max 500)
    - costo_seguro: Decimal (calculado)
    - id_cliente: int (FK -> Cliente, requerido)
    - id_vehiculo: int (FK -> Vehiculo, requerido)
    - id_empleado: int (FK -> Empleado, requerido)
    - id_seguro: int (FK -> Seguro, requerido)
    
```

**Estados**: pendiente, activo, finalizado, cancelado

---

### 7. Clase Mantenimiento
**Ubicación**: `models/mantenimiento.py`

```python
class Mantenimiento:
    """
    Registra servicios de mantenimiento en vehículos.
    """
    
    # Atributos
    - id_mantenimiento: int (PK, autoincremental)
    - fecha_inicio: date (requerido)
    - fecha_fin: date (nullable)
    - tipo: str (preventivo|correctivo|revision)
    - descripcion: str (max 500)
    - costo: Decimal (>= 0)
    - kilometraje: int (requerido)
    - proveedor: str (max 150)
    - estado: str (pendiente|en_proceso|finalizado)
    - id_vehiculo: int (FK -> Vehiculo, requerido)
    - id_empleado: int (FK -> Empleado, requerido)
    
```

**Tipos**: preventivo, correctivo, revision  
**Estados**: pendiente, en_proceso, finalizado

---

### 8. Clase Multa
**Ubicación**: `models/multa.py`

```python
class Multa:
    """
    Registra multas asociadas a alquileres.
    """
    
    # Atributos
    - id_multa: int (PK, autoincremental)
    - motivo: str (max 200, requerido)
    - monto: Decimal (requerido, > 0)
    - fecha: date (auto)
    - pagada: bool (default False)
    - descripcion: str (max 500)
    - id_alquiler: int (FK -> Alquiler, requerido)
    
```

**Motivos comunes**: Retraso, Daños, Infracción de tránsito, Limpieza

---

### 9. Clase Reserva
**Ubicación**: `models/reserva.py`

```python
class Reserva:
    """
    Gestiona reservas anticipadas de vehículos.
    """
    
    # Atributos
    - id_reserva: int (PK, autoincremental)
    - fecha_reserva: date (auto)
    - fecha_inicio: date (requerido)
    - fecha_fin: date (requerido)
    - estado: str (pendiente|confirmada|cancelada|convertida)
    - fecha_confirmacion: date (nullable)
    - senia: Decimal (>= 0)
    - id_cliente: int (FK -> Cliente, requerido)
    - id_vehiculo: int (FK -> Vehiculo, requerido)
    - id_alquiler: int (FK -> Alquiler, nullable)
    
```

**Estados**: pendiente, confirmada, cancelada, convertida

---

## 🗄️ Base de Datos

### Diagrama Entidad-Relación
```
CLIENTE (1) ──── (N) ALQUILER (N) ──── (1) VEHICULO
                      │                      │
                      │                      │
                     (1)                    (N)
                      │                      │
                   MULTA              MANTENIMIENTO
```

### Tablas Principales

#### Tabla: clientes
```sql
CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni TEXT UNIQUE NOT NULL,
    telefono TEXT,
    email TEXT,
    direccion TEXT,
    fecha_registro DATE DEFAULT CURRENT_DATE,
    activo BOOLEAN DEFAULT 1
);
```

#### Tabla: empleados
```sql
CREATE TABLE empleados (
    id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    cargo TEXT,
    telefono TEXT,
    email TEXT,
    activo BOOLEAN DEFAULT 1
);
```

#### Tabla: categorias
```sql
CREATE TABLE categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT,
    precio_base REAL NOT NULL,
    dias_mantenimiento INTEGER DEFAULT 90
);
```

#### Tabla: vehiculos
```sql
CREATE TABLE vehiculos (
    id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
    patente TEXT UNIQUE NOT NULL,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    anio INTEGER NOT NULL,
    color TEXT,
    precio_dia REAL NOT NULL,
    estado TEXT DEFAULT 'disponible',
    kilometraje INTEGER DEFAULT 0,
    kilometraje_mantenimiento INTEGER,
    id_categoria INTEGER,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);
```

#### Tabla: alquileres
```sql
CREATE TABLE alquileres (
    id_alquiler INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    fecha_entrega_real DATE,
    costo_total REAL,
    deposito REAL NOT NULL,
    estado TEXT DEFAULT 'pendiente',
    observaciones TEXT,
    id_cliente INTEGER NOT NULL,
    id_vehiculo INTEGER NOT NULL,
    id_empleado INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);
```

#### Tabla: mantenimientos
```sql
CREATE TABLE mantenimientos (
    id_mantenimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    tipo TEXT NOT NULL,
    descripcion TEXT,
    costo REAL DEFAULT 0,
    kilometraje INTEGER NOT NULL,
    proveedor TEXT,
    estado TEXT DEFAULT 'pendiente',
    id_vehiculo INTEGER NOT NULL,
    id_empleado INTEGER NOT NULL,
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);
```

#### Tabla: multas
```sql
CREATE TABLE multas (
    id_multa INTEGER PRIMARY KEY AUTOINCREMENT,
    motivo TEXT NOT NULL,
    monto REAL NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    pagada BOOLEAN DEFAULT 0,
    descripcion TEXT,
    id_alquiler INTEGER NOT NULL,
    FOREIGN KEY (id_alquiler) REFERENCES alquileres(id_alquiler)
);
```

#### Tabla: reservas
```sql
CREATE TABLE reservas (
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_reserva DATE DEFAULT CURRENT_DATE,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado TEXT DEFAULT 'pendiente',
    fecha_confirmacion DATE,
    senia REAL DEFAULT 0,
    id_cliente INTEGER NOT NULL,
    id_vehiculo INTEGER NOT NULL,
    id_alquiler INTEGER,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo),
    FOREIGN KEY (id_alquiler) REFERENCES alquileres(id_alquiler)
);
```

---

## ✅ Validaciones y Reglas de Negocio

### Validaciones de Datos

#### Cliente
- DNI: único, numérico, 7-8 dígitos
- Email: formato válido (regex: `^[\w\.-]+@[\w\.-]+\.\w+$`)
- Teléfono: numérico, 10-15 dígitos
- Nombre/Apellido: no vacíos, solo letras y espacios

#### Vehículo
- Patente: única, formato válido (ABC123 o AB123CD)
- Año: entre 1980 y año actual + 1
- Precio por día: mayor a 0
- Kilometraje: no negativo

#### Alquiler
- fecha_fin > fecha_inicio
- Mínimo 1 día de alquiler
- Depósito: mínimo 30% del costo total estimado
- Vehículo debe estar "disponible"

### Reglas de Negocio

1. **Disponibilidad de Vehículo**:
   - No puede estar en dos alquileres simultáneos
   - Si está en mantenimiento, no se puede alquilar

2. **Cálculo de Costos**:
   ```
   días = (fecha_fin - fecha_inicio).days
   costo_total = días × precio_dia_vehiculo
   ```

3. **Multas por Retraso**:
   ```
   días_retraso = (fecha_entrega_real - fecha_fin).days
   si días_retraso > 0:
       multa = días_retraso × (precio_dia × 1.20)
   ```

4. **Mantenimiento Preventivo**:
   - Si (kilometraje_actual - kilometraje_último_mantenimiento) >= categoría.dias_mantenimiento × 100
   - Mostrar alerta de mantenimiento necesario

5. **Reservas**:
   - Seña = 20% del costo estimado
   - Vence si no se confirma 24hs antes
   - Al convertir a alquiler, seña se descuenta del depósito

---

## 📊 Reportes Requeridos

### Reportes Detallados
1. **Listado de alquileres por cliente**
2. **Vehículos más alquilados**
3. **Alquileres por período (mes, trimestre)**

### Reportes Estadísticos
1. **Facturación mensual** (gráfico de barras)
2. **Ocupación de vehículos**
3. **Mantenimientos por vehículo**

---

## 🚀 Próximos Pasos

1. Implementar estructura de carpetas
2. Crear configuración de base de datos
3. Desarrollar modelos de datos
4. Implementar capa DAO
5. Crear controllers
6. Diseñar interfaz con Flet
7. Implementar módulo de reportes
8. Testing y ajustes finales
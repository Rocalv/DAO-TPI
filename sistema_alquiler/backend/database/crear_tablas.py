# database/crear_tablas.py
from .db_config import db

def crear_tablas():
    """ Crea todas las tablas necesarias para el sistema de alquiler """
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        # Tabla: clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                dni TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                telefono TEXT,
                email TEXT,
                direccion TEXT,
                fecha_registro DATE DEFAULT CURRENT_DATE,
                activo BOOLEAN DEFAULT 1
            )
        """)

        # --- TABLA: estados_vehiculo ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estados_vehiculo (
                id_estado INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            )
        """)

        # --- TABLA: cargos_empleado ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cargos_empleado (
                id_cargo INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                descripcion TEXT
            )
        """)

        # --- TABLA EMPLEADOS (MODIFICADA) ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleados (
                id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                dni TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                -- cargo TEXT,  <-- CAMPO ELIMINADO
                telefono TEXT,
                email TEXT,
                foto_path TEXT,
                activo BOOLEAN DEFAULT 1,
                id_cargo INTEGER, -- <-- CAMPO NUEVO
                FOREIGN KEY (id_cargo) REFERENCES cargos_empleado(id_cargo)
            )
        """)
        
        # Tabla: categorias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                descripcion TEXT,
                precio_dia REAL NOT NULL
            )
        """)

        # Tabla: servicios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS servicios (
                id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                descripcion TEXT,
                costo_base REAL NOT NULL
            )
        """)

        # Tabla: tipos_multa
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tipos_multa (
                id_tipo_multa INTEGER PRIMARY KEY AUTOINCREMENT,
                motivo TEXT UNIQUE NOT NULL,
                descripcion TEXT,
                monto_sugerido REAL NOT NULL
            )
        """)

        # Tabla: vehiculos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehiculos (
                id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
                patente TEXT UNIQUE NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                anio INTEGER NOT NULL,
                color TEXT,
                -- estado TEXT DEFAULT 'disponible', <-- ELIMINADO
                kilometraje INTEGER DEFAULT 0,
                km_mantenimiento INTEGER DEFAULT 10000,
                foto_path TEXT,
                -- activo BOOLEAN DEFAULT 1, <-- ELIMINADO
                id_categoria INTEGER NOT NULL,
                id_estado INTEGER NOT NULL, -- <-- NUEVO
                FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
                FOREIGN KEY (id_estado) REFERENCES estados_vehiculo(id_estado)
            )
        """)
        
        # Tabla: alquileres
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alquileres (
                id_alquiler INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_inicio DATE NOT NULL,
                fecha_fin DATE NOT NULL,
                fecha_entrega_real DATE,
                costo_total REAL,
                estado TEXT DEFAULT 'pendiente',
                observaciones TEXT,
                id_cliente INTEGER NOT NULL,
                id_vehiculo INTEGER NOT NULL,
                id_empleado INTEGER NOT NULL,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo),
                FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
            )
        """)
        
        # Tabla: mantenimientos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mantenimientos (
                id_mantenimiento INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_inicio DATE NOT NULL,
                fecha_fin DATE,
                descripcion TEXT,
                costo REAL DEFAULT 0,
                kilometraje INTEGER NOT NULL,
                proveedor TEXT,
                estado TEXT DEFAULT 'pendiente',
                id_vehiculo INTEGER NOT NULL,
                id_empleado INTEGER NOT NULL,
                id_servicio INTEGER NOT NULL,
                FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo),
                FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
                FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio)
            )
        """)
        
        # Tabla: multas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS multas (
                id_multa INTEGER PRIMARY KEY AUTOINCREMENT,
                monto REAL NOT NULL,
                fecha DATE DEFAULT CURRENT_DATE,
                estado TEXT DEFAULT 'pendiente',
                descripcion TEXT,
                id_alquiler INTEGER NOT NULL,
                id_tipo_multa INTEGER NOT NULL,
                FOREIGN KEY (id_alquiler) REFERENCES alquileres(id_alquiler),
                FOREIGN KEY (id_tipo_multa) REFERENCES tipos_multa(id_tipo_multa)
            )
        """)
        
        db.commit()
        print("> Tablas creadas y/o actualizadas exitosamente")
        
    except Exception as e:
        print(f"> Error al crear tablas: {e}")
        db.rollback()
        raise


def insertar_datos_prueba():
    """ Inserta datos de prueba en las tablas """
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        # --- DATOS DE NORMALIZACIÓN ---        
        cursor.execute("INSERT OR IGNORE INTO tipos_multa (motivo, descripcion, monto_sugerido) VALUES ('Retraso en entrega', 'Devolución fuera de término (por día)', 4000)")
        cursor.execute("INSERT OR IGNORE INTO tipos_multa (motivo, descripcion, monto_sugerido) VALUES ('Daño leve', 'Rayón o abolladura menor', 20000)")

        servicios = [
        ("Mantenimiento Preventivo", "Servicio estándar programado", 50000),
        ("Inspeccion Neumaticos", "Revisión y rotación de neumáticos", 15000),
        ("Cambio Liquidos", "Cambio de aceite, refrigerante y frenos", 30000),
        ("Reparacion Mecanica", "Reparación de motor, transmisión, etc.", 80000),
        ("Reparacion Electrica", "Reparación de sistema eléctrico", 70000),
        ("Limpieza", "Limpieza profunda de interior y exterior", 10000),
        ("Reparacion Colision", "Reparación de chapa y pintura", 150000)
    ]
        for nombre, desc, costo in servicios:
            cursor.execute("INSERT OR IGNORE INTO servicios (nombre, descripcion, costo_base) VALUES (?, ?, ?)", (nombre, desc, costo))

        # --- CATEGORÍAS DE VEHÍCULOS ---
        categorias = [
            ('Compactos-Económicos', 'Autos pequeños, bajo consumo', 15000),
            ('Intermedios-Medianos', 'Sedán 4 puertas, mayor confort', 22000),
            ('Premium-Sedán', 'Autos de alta gama', 35000),
            ('Premium-Plus', 'Lujo superior', 50000),
            ('SUV-Automática', 'Camioneta urbana, caja automática', 40000),
            ('SUV-Manual', 'Camioneta urbana, caja manual', 38000),
            ('Camioneta 4x4', 'Todo terreno', 60000),
            ('Deportivo', 'Alta performance', 80000)
        ]
        for nombre, desc, precio in categorias:
            cursor.execute("INSERT OR IGNORE INTO categorias (nombre, descripcion, precio_dia) VALUES (?, ?, ?)", (nombre, desc, precio))
        
        # --- CARGOS ---
        cursor.execute("INSERT OR IGNORE INTO cargos_empleado (nombre, descripcion) VALUES ('Gerente', 'Responsable de sucursal')")
        cursor.execute("INSERT OR IGNORE INTO cargos_empleado (nombre, descripcion) VALUES ('Vendedor', 'Atención al público y alquileres')")
        cursor.execute("INSERT OR IGNORE INTO cargos_empleado (nombre, descripcion) VALUES ('Mecánico', 'Mantenimiento de flota')")

        # --- EMPLEADOS ---
        cursor.execute("""
            INSERT OR IGNORE INTO empleados (dni, nombre, apellido, id_cargo, telefono, email, foto_path)
            VALUES ('12345678', 'Juan', 'Pérez', 1, '3511234567', 'juan@alquiler.com', NULL)
        """)
        cursor.execute("""
            INSERT OR IGNORE INTO empleados (dni, nombre, apellido, id_cargo, telefono, email, foto_path)
            VALUES ('87654321', 'María', 'González', 2, '3517654321', 'maria@alquiler.com', NULL)
        """)
        cursor.execute("""
            INSERT OR IGNORE INTO empleados (dni, nombre, apellido, id_cargo, telefono, email, foto_path)
            VALUES ('30123456', 'Carlos', 'Gómez', 3, '3515551234', 'carlos@alquiler.com', NULL)
        """)
        cursor.execute("""
            INSERT OR IGNORE INTO empleados (dni, nombre, apellido, id_cargo, telefono, email, foto_path)
            VALUES ('45821252', 'Martin', 'Velez', 3, '3515887425', 'martin@alquiler.com', NULL)
        """)
        
        # --- CLIENTES ---
        cursor.execute("INSERT OR IGNORE INTO clientes (nombre, apellido, dni, telefono, email, direccion) VALUES ('Carlos', 'Rodríguez', '20123456', '3519876543', 'carlos@email.com', 'Av. Colón 123')")
        cursor.execute("INSERT OR IGNORE INTO clientes (nombre, apellido, dni, telefono, email, direccion) VALUES ('Ana', 'Martínez', '25987654', '3516543210', 'ana@email.com', 'Bv. San Juan 456')")
       
        # --- ESTADOS VEHÍCULO ---
        estados = ['disponible', 'alquilado', 'mantenimiento', 'Baja', 'reservado']
        for estado in estados:
            cursor.execute("INSERT OR IGNORE INTO estados_vehiculo (nombre) VALUES (?)", (estado,))
       
        # --- VEHÍCULOS ---
        cursor.execute("INSERT OR IGNORE INTO vehiculos (patente, marca, modelo, anio, color, kilometraje, id_categoria, id_estado) VALUES ('AA123BB', 'Toyota', 'Etios', 2022, 'Blanco', 25000, 1, 1)")
        cursor.execute("INSERT OR IGNORE INTO vehiculos (patente, marca, modelo, anio, color, kilometraje, id_categoria, id_estado) VALUES ('AD456CC', 'Ford', 'Focus', 2023, 'Gris Plata', 10000, 2, 2)")
        cursor.execute("INSERT OR IGNORE INTO vehiculos (patente, marca, modelo, anio, color, kilometraje, id_categoria, id_estado) VALUES ('AF789DD', 'Toyota', 'SW4', 2024, 'Negro', 5000, 3, 3)")
        
        # --- ALQUILERES ---
        cursor.execute("INSERT OR IGNORE INTO alquileres (fecha_inicio, fecha_fin, costo_total, estado, id_cliente, id_vehiculo, id_empleado) VALUES (date('now'), date('now', '+3 days'), 24000, 'activo', 1, 1, 1)")
        
        # --- MULTAS ---
        cursor.execute("INSERT OR IGNORE INTO multas (monto, descripcion, id_alquiler, estado, id_tipo_multa) VALUES (12000, 'Entrega con 3 días de retraso', 1, 'pendiente', 1)")
        
        # --- MANTENIMIENTOS ---
        cursor.execute("INSERT OR IGNORE INTO mantenimientos (fecha_inicio, kilometraje, estado, id_vehiculo, id_empleado, id_servicio) VALUES (date('now', '-5 days'), 45000, 'finalizado', 1, 2, 1)")

        db.commit()
        print("> Datos de prueba insertados")
        
    except Exception as e:
        print(f"> Error al insertar datos de prueba: {e}")
        db.rollback()

if __name__ == "__main__":
    print("Creando base de datos...")
    crear_tablas()
    insertar_datos_prueba()
    print("¡Base de datos lista!")
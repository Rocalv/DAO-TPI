from backend.database.db_config import db

def crear_tablas():
    """ Crea todas las tablas necesarias para el sistema de alquiler """
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        # Tabla: clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                dni TEXT UNIQUE NOT NULL,
                telefono TEXT,
                email TEXT,
                direccion TEXT,
                fecha_registro DATE DEFAULT CURRENT_DATE,
                activo BOOLEAN DEFAULT 1
            )
        """)
        
        # Tabla: empleados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleados (
                id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                dni TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                cargo TEXT,
                telefono TEXT,
                email TEXT,
                activo BOOLEAN DEFAULT 1
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
                precio_dia REAL NOT NULL,
                estado TEXT DEFAULT 'disponible',
                kilometraje INTEGER DEFAULT 0,
                km_mantenimiento INTEGER DEFAULT 10000,
                activo BOOLEAN DEFAULT 1
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
            )
        """)
        
        # Tabla: multas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS multas (
                id_multa INTEGER PRIMARY KEY AUTOINCREMENT,
                motivo TEXT NOT NULL,
                monto REAL NOT NULL,
                fecha DATE DEFAULT CURRENT_DATE,
                pagada BOOLEAN DEFAULT 0,
                descripcion TEXT,
                id_alquiler INTEGER NOT NULL,
                FOREIGN KEY (id_alquiler) REFERENCES alquileres(id_alquiler)
            )
        """)
        
        db.commit()
        print("> Tablas creadas exitosamente")
        
    except Exception as e:
        print(f"> Error al crear tablas: {e}")
        db.rollback()
        raise


def insertar_datos_prueba():
    """ Inserta datos de prueba en las tablas """
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        # Empleados de prueba
        cursor.execute("""
            INSERT OR IGNORE INTO empleados (dni, nombre, apellido, cargo, telefono, email)
            VALUES ('12345678', 'Juan', 'Pérez', 'Gerente', '3511234567', 'juan@alquiler.com')
        """)
        
        cursor.execute("""
            INSERT OR IGNORE INTO empleados (dni, nombre, apellido, cargo, telefono, email)
            VALUES ('87654321', 'María', 'González', 'Vendedora', '3517654321', 'maria@alquiler.com')
        """)
        
        # Clientes de prueba
        cursor.execute("""
            INSERT OR IGNORE INTO clientes (nombre, apellido, dni, telefono, email, direccion)
            VALUES ('Carlos', 'Rodríguez', '20123456', '3519876543', 'carlos@email.com', 'Av. Colón 123')
        """)
        
        cursor.execute("""
            INSERT OR IGNORE INTO clientes (nombre, apellido, dni, telefono, email, direccion)
            VALUES ('Ana', 'Martínez', '25987654', '3516543210', 'ana@email.com', 'Bv. San Juan 456')
        """)
        
        # Vehículos de prueba
        cursor.execute("""
            INSERT OR IGNORE INTO vehiculos 
            (patente, marca, modelo, anio, color, precio_dia, kilometraje, km_mantenimiento)
            VALUES ('ABC123', 'Toyota', 'Corolla', 2020, 'Blanco', 8000, 45000, 50000)
        """)

        cursor.execute("""
            INSERT OR IGNORE INTO vehiculos 
            (patente, marca, modelo, anio, color, precio_dia, kilometraje, km_mantenimiento)
            VALUES ('XYZ789', 'Ford', 'Focus', 2019, 'Gris', 7500, 52000, 60000)
        """)

        cursor.execute("""
            INSERT OR IGNORE INTO vehiculos 
            (patente, marca, modelo, anio, color, precio_dia, kilometraje, km_mantenimiento)
            VALUES ('DEF456', 'Chevrolet', 'Cruze', 2021, 'Negro', 9000, 30000, 40000)
        """)
        
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
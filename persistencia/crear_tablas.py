# database/crear_tablas.py
from .db_config import db
import random
from datetime import date, timedelta

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

        # Tabla: reservas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_reserva_creada DATE DEFAULT CURRENT_DATE,
            fecha_inicio DATE NOT NULL,
            fecha_fin DATE NOT NULL,
            costo_total REAL NOT NULL,
            estado TEXT DEFAULT 'pendiente', -- (pendiente, completada, cancelada)
            id_cliente INTEGER NOT NULL,
            id_vehiculo INTEGER NOT NULL,
            id_empleado INTEGER NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
            FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo),
            FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
            )
        """)
        
        db.commit()
        print("> Tablas creadas y/o actualizadas exitosamente")
        
    except Exception as e:
        print(f"> Error al crear tablas: {e}")
        db.rollback()
        raise


def insertar_datos_prueba():
    """ Inserta una gran cantidad de datos de prueba realistas en las tablas """
    conn = db.get_connection()
    cursor = conn.cursor()
    
    print("> Insertando datos de prueba masivos...")

    try:
        # --- 1. DATOS BASE (CATEGORÍAS, SERVICIOS, ETC.) ---
        
        # (Se mantienen los datos base que ya tenías)
        cursor.execute("INSERT OR IGNORE INTO tipos_multa (motivo, descripcion, monto_sugerido) VALUES ('Retraso en entrega', 'Devolución fuera de término (por día)', 4000)")
        cursor.execute("INSERT OR IGNORE INTO tipos_multa (motivo, descripcion, monto_sugerido) VALUES ('Daño leve', 'Rayón o abolladura menor', 20000)")

        servicios = [
            ("Mantenimiento Preventivo", "Servicio estándar programado", 50000), ("Inspeccion Neumaticos", "Revisión y rotación de neumáticos", 15000),
            ("Cambio Liquidos", "Cambio de aceite, refrigerante y frenos", 30000), ("Reparacion Mecanica", "Reparación de motor, transmisión, etc.", 80000),
            ("Reparacion Electrica", "Reparación de sistema eléctrico", 70000), ("Limpieza", "Limpieza profunda de interior y exterior", 10000),
            ("Reparacion Colision", "Reparación de chapa y pintura", 150000)
        ]
        cursor.executemany("INSERT OR IGNORE INTO servicios (nombre, descripcion, costo_base) VALUES (?, ?, ?)", servicios)

        categorias = [
            ('Compactos-Económicos', 'Autos pequeños, bajo consumo', 55000), ('Intermedios-Medianos', 'Sedán 4 puertas, mayor confort', 69000),
            ('Premium-Sedán', 'Autos de alta gama', 150000), ('Premium-Plus', 'Lujo superior', 90000),
            ('SUV-Automática', 'Camioneta urbana, caja automática', 130000), ('SUV-Manual', 'Camioneta urbana, caja manual', 120000),
            ('Camioneta 4x4', 'Todo terreno', 190000), ('Deportivo', 'Alta performance', 250000)
        ]
        cursor.executemany("INSERT OR IGNORE INTO categorias (nombre, descripcion, precio_dia) VALUES (?, ?, ?)", categorias)
        
        cursor.execute("INSERT OR IGNORE INTO cargos_empleado (nombre, descripcion) VALUES ('Gerente', 'Responsable de sucursal')")
        cursor.execute("INSERT OR IGNORE INTO cargos_empleado (nombre, descripcion) VALUES ('Vendedor', 'Atención al público y alquileres')")
        cursor.execute("INSERT OR IGNORE INTO cargos_empleado (nombre, descripcion) VALUES ('Mecánico', 'Mantenimiento de flota')")
        cursor.execute("INSERT OR IGNORE INTO cargos_empleado (nombre, descripcion) VALUES ('Administrativo', 'Gestión de flotas y papelería')")

        estados = ['disponible', 'alquilado', 'mantenimiento', 'Baja', 'reservado']
        cursor.executemany("INSERT OR IGNORE INTO estados_vehiculo (nombre) VALUES (?)", [(e,) for e in estados])

        # --- 2. GENERACIÓN DE EMPLEADOS (10) ---
        empleados = [
            ('12345678', 'Juan', 'Pérez', 1, '3511234567', 'juan@alquiler.com', None),
            ('87654321', 'María', 'González', 2, '3517654321', 'maria@alquiler.com', None),
            ('30123456', 'Carlos', 'Gómez', 3, '3515551234', 'carlos@alquiler.com', None),
            ('45821252', 'Martín', 'Vélez', 3, '3515887425', 'martin@alquiler.com', None),
            ('31555888', 'Ana', 'López', 2, '351666777', 'ana@alquiler.com', None),
            ('32999000', 'Luis', 'Martínez', 2, '351222333', 'luis@alquiler.com', None),
            ('28111222', 'Sofía', 'Fernández', 4, '351999888', 'sofia@alquiler.com', None),
            ('34555666', 'Diego', 'Rodríguez', 3, '351444555', 'diego@alquiler.com', None),
            ('36888999', 'Valeria', 'Díaz', 2, '351777666', 'valeria@alquiler.com', None),
            ('27500100', 'Jorge', 'Sánchez', 1, '351333222', 'jorge@alquiler.com', None)
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO empleados (dni, nombre, apellido, id_cargo, telefono, email, foto_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, empleados)

        # --- 3. GENERACIÓN DE CLIENTES (50) ---
        nombres = ['Carlos', 'Ana', 'Miguel', 'Lucía', 'David', 'Elena', 'Pablo', 'Sara', 'Javier', 'Laura']
        apellidos = ['Rodríguez', 'Martínez', 'García', 'López', 'Sánchez', 'Pérez', 'Gómez', 'Díaz', 'Moreno', 'Jiménez']
        clientes = []
        for i in range(50):
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            dni = f"{20000000 + i * 1000 + i}" # DNI único
            telefono = f"351{random.randint(2000000, 8000000)}"
            email = f"{nombre.lower()}.{apellido.lower()}{i}@email.com"
            direccion = f"Calle Ficticia {random.randint(100, 2000)}"
            clientes.append((nombre, apellido, dni, telefono, email, direccion))
        
        cursor.executemany("""
            INSERT OR IGNORE INTO clientes (nombre, apellido, dni, telefono, email, direccion) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, clientes)

        # --- 4. GENERACIÓN DE VEHÍCULOS (100) ---
        marcas_modelos = [
            ('Ford', 'Focus', 2), ('Ford', 'Escape', 5), ('Hyundai', 'Elantra', 5), ('Ford', 'Fusion', 3),
            ('Kia', 'Soul', 6), ('Toyota', 'Corolla', 2), ('Kia', 'Niro ev', 5), ('Chevrolet', 'Spark', 1),
            ('Chevrolet', 'Malibu', 3), ('Jeep', 'Compass', 5), ('Nissan', 'Rogue', 5), ('Ford', 'Edge', 5),
            ('Chevrolet', 'Equinox', 5), ('Ford', 'Explorer', 7), ('Toyota', 'Hilux', 7), ('Volkswagen', 'Golf', 2),
            ('Volkswagen', 'T-Cross', 5), ('Renault', 'Duster', 6), ('Fiat', 'Cronos', 2), ('Peugeot', '208', 1),
            ('BMW', 'Serie 3', 3), ('Audi', 'A4', 3), ('Mercedes Benz', 'Clase C', 3), ('Jeep', 'Renegade', 6),
            ('Nissan', 'Kicks', 5), ('Toyota', 'Yaris', 1), ('Ford', 'Mustang', 8), ('Chevrolet', 'Camaro', 8)
        ]
        colores = ['Blanco', 'Rojo', 'Gris', 'Negro', 'Azul', 'Plata']
        
        vehiculos = []
        for i in range(100):
            # Patente única (formato simple 'AA-000-AA' + i)
            letra_final = chr(ord('A') + (i % 26))
            patente = f"PY{i:03d}{letra_final}K"
            
            base_vehiculo = random.choice(marcas_modelos)
            marca, modelo, id_categoria = base_vehiculo
            
            anio = random.randint(2018, 2025)
            color = random.choice(colores)
            kilometraje = random.randint(5000, 80000)
            id_estado = 1 # 1 = 'disponible'
            foto = f"frontend/assets/vehiculos/{marca.lower()}{modelo.replace(' ', '')}.png" # Foto genérica
            
            vehiculos.append((patente, marca, modelo, anio, color, kilometraje, id_categoria, id_estado, foto))

        cursor.executemany("""
            INSERT OR IGNORE INTO vehiculos (patente, marca, modelo, anio, color, kilometraje, id_categoria, id_estado, foto_path) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, vehiculos)


        # --- 5. GENERACIÓN DE ALQUILERES (REALISTAS) ---
        print("> Generando alquileres realistas para 2025...")

        cursor.execute("SELECT COUNT(*) FROM alquileres WHERE strftime('%Y', 'fecha_inicio')=?", ("2025",))
        if cursor.fetchone()[0] >= 500:
            print("> Ya existen alquileres de 2025. Se omite la inserción de alquileres.")
            db.commit()
            return

        # Obtenemos los IDs reales de la BD
        all_vehicles = cursor.execute("SELECT id_vehiculo, id_categoria FROM vehiculos").fetchall()
        all_clients = [row[0] for row in cursor.execute("SELECT id_cliente FROM clientes").fetchall()]
        all_employees = [row[0] for row in cursor.execute("SELECT id_empleado FROM empleados").fetchall()]
        precios_categoria = {id: p for id, p in cursor.execute("SELECT id_categoria, precio_dia FROM categorias").fetchall()}

        if not all_vehicles or not all_clients or not all_employees:
            print("ERROR: No se encontraron vehículos, clientes o empleados.")
            return

        # === INICIO DE LA NUEVA LÓGICA ===
        
        # Mezclamos los vehículos para que la selección sea aleatoria
        random.shuffle(all_vehicles)
        
        # ¡TU REQUISITO! Separamos los vehículos
        # Dejaremos ~20% de la flota (20 vehículos) sin alquilar NUNCA.
        # Solo los primeros 80 vehículos serán "alquilables".
        num_rentable = int(len(all_vehicles) * 0.8)
        rentable_vehicles = all_vehicles[:num_rentable]
        vehicles_kept_available = all_vehicles[num_rentable:]
        
        print(f"> Flota total: {len(all_vehicles)}. Alquilables: {len(rentable_vehicles)}. Reservados: {len(vehicles_kept_available)}.")

        # El "calendario" solo usará los vehículos alquilables
        vehicle_bookings = {v[0]: [] for v in rentable_vehicles}
        
        rentals_to_insert = []
        YEAR = 2025
        START_OF_YEAR = date(YEAR, 1, 1)
        END_OF_YEAR = date(YEAR, 12, 31)
        TOTAL_DAYS = (END_OF_YEAR - START_OF_YEAR).days
        
        # Asumimos que "hoy" es 17 de Noviembre de 2025 para el estado "activo"
        TODAY_SIMULATED = date(2025, 11, 17) 
        
        RENTALS_TO_CREATE = 1500
        
        for _ in range(RENTALS_TO_CREATE):
            # 1. Seleccionar participantes (SOLO de la lista de alquilables)
            vehicle_data = random.choice(rentable_vehicles) 
            id_vehiculo = vehicle_data[0]
            id_categoria = vehicle_data[1]
            
            id_cliente = random.choice(all_clients)
            id_empleado = random.choice(all_employees)
            
            # 2. Definir fechas aleatorias
            rental_duration = random.randint(2, 10)
            random_day_offset = random.randint(0, TOTAL_DAYS - rental_duration)
            
            start_date = START_OF_YEAR + timedelta(days=random_day_offset)
            end_date = start_date + timedelta(days=rental_duration)
            
            # 3. VERIFICAR CONFLICTO
            is_available = True
            for booked_start, booked_end in vehicle_bookings[id_vehiculo]:
                if (start_date <= booked_end) and (end_date >= booked_start):
                    is_available = False
                    break 
            
            # 4. Si está disponible, registrarlo
            if is_available:
                vehicle_bookings[id_vehiculo].append((start_date, end_date))
                
                precio_dia = precios_categoria.get(id_categoria, 60000)
                costo_total = precio_dia * rental_duration + random.randint(0, 5000)
                
                if end_date < TODAY_SIMULATED.replace(month=11, day=1):
                    estado = 'finalizado'
                elif start_date < TODAY_SIMULATED:
                    estado = 'activo'
                else:
                    estado = 'pendiente'

                rentals_to_insert.append((
                    start_date.isoformat(), end_date.isoformat(), 
                    costo_total, estado, id_cliente, id_vehiculo, id_empleado
                ))

        # 5. Insertar todos los alquileres
        if rentals_to_insert:
            cursor.executemany(
                "INSERT INTO alquileres (fecha_inicio, fecha_fin, costo_total, estado, id_cliente, id_vehiculo, id_empleado) VALUES (?, ?, ?, ?, ?, ?, ?)",
                rentals_to_insert
            )
            print(f"> {len(rentals_to_insert)} alquileres generados e insertados.")
        
        # === FIN DE LA NUEVA LÓGICA ===


        # --- 6. ACTUALIZAR ESTADOS DE VEHÍCULOS (NUEVO!) ---
        print("> Actualizando estados de la flota (alquilado, mantenimiento)...")
        
        # ID 1 = disponible, 2 = alquilado, 3 = mantenimiento
        updates_to_make = []
        
        # Poner vehículos "actualmente" alquilados en estado 2
        for id_vehiculo, bookings in vehicle_bookings.items():
            for start_date, end_date in bookings:
                # Si el alquiler se superpone con "hoy" (17/11/2025)
                if (start_date <= TODAY_SIMULATED) and (end_date >= TODAY_SIMULATED):
                    updates_to_make.append((2, id_vehiculo)) # 2 = 'alquilado'
                    break # Pasamos al siguiente vehículo
        
        # Poner algunos de los vehículos "reservados" en mantenimiento (estado 3)
        # Tomamos 5 vehículos de los que "guardamos"
        for i, (id_vehiculo, _) in enumerate(vehicles_kept_available):
            if i >= 5: # Solo 5 en mantenimiento
                break
            updates_to_make.append((3, id_vehiculo)) # 3 = 'mantenimiento'

        if updates_to_make:
            cursor.executemany(
                "UPDATE vehiculos SET id_estado = ? WHERE id_vehiculo = ?",
                updates_to_make
            )
            print(f"> {len(updates_to_make)} vehículos actualizados a 'alquilado' o 'mantenimiento'.")
            
        # El resto de vehículos (incluidos los "reservados" restantes)
        # permanecen con su estado original '1' (disponible).

        # --- 7. MANTENIMIENTOS Y MULTAS (Simples) ---
        cursor.execute("INSERT OR IGNORE INTO multas (monto, descripcion, id_alquiler, estado, id_tipo_multa) VALUES (12000, 'Entrega con 3 días de retraso', 1, 'pendiente', 1)")
        cursor.execute("INSERT OR IGNORE INTO mantenimientos (fecha_inicio, kilometraje, estado, id_vehiculo, id_empleado, id_servicio) VALUES (date('now', '-5 days'), 45000, 'finalizado', 1, 2, 1)")

        db.commit()
        print("> Todos los datos de prueba masivos han sido insertados.")
        
    except Exception as e:
        print(f"> Error al insertar datos de prueba masivos: {e}")
        db.rollback()
        raise

if __name__ == "__main__":
    print("Creando base de datos...")
    crear_tablas()
    insertar_datos_prueba()
    print("¡Base de datos lista!")
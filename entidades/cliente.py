from persistencia.db_config import db

class Cliente:
    def __init__(self, id_cliente=None, dni=None, nombre=None, apellido=None, telefono=None, email=None, direccion=None, fecha_registro=None, activo=1):
        self.id_cliente = id_cliente
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.fecha_registro = fecha_registro
        self.activo = activo
    
    # Metodos: registrar, modificar, eliminar, consultar, filtrar_por_id, filtrar_por_dni

    @staticmethod
    def registrar(dni, nombre, apellido, telefono, email, direccion):
        """Crea un nuevo cliente."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (dni, nombre, apellido, telefono, email, direccion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (dni, nombre, apellido, telefono, email, direccion,))
            db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear cliente: {e}")
            db.rollback()
            return None
        finally:
            db.close_connection()


    @staticmethod
    def modificar(id_cliente, dni, nombre, apellido, telefono, email, direccion, activo):
        """Actualiza o modifica un cliente existente."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE clientes
                SET dni = ?, nombre = ?, apellido = ?, telefono = ?, 
                    email = ?, direccion = ?, activo = ?
                WHERE id_cliente = ?
            """, (dni, nombre, apellido, telefono, email, direccion, activo, id_cliente,))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar cliente: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()

    @staticmethod
    def eliminar(id_cliente):
        """Realiza un 'soft delete' del cliente, marcándolo como inactivo (activo = 0)."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE clientes SET activo = 0 WHERE id_cliente = ?", (id_cliente,))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar (soft delete) cliente: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()

    @staticmethod
    def consultar(incluir_inactivos=False):
        """
        Obtiene todos los clientes.
        Por defecto, solo trae clientes activos.
        """
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM clientes"
            if not incluir_inactivos:
                query += " WHERE activo = 1"
                
            cursor.execute(query)
            clientes_data = cursor.fetchall()
            
            clientes = []
            if clientes_data:
                columnas = [desc[0] for desc in cursor.description]
                for c in clientes_data:
                    clientes.append(dict(zip(columnas, c)))
            return clientes
            
        except Exception as e:
            print(f"Error al obtener clientes: {e}")
            return []
        finally:
            db.close_connection()

    @staticmethod
    def filtrar_por_id(id_cliente):
        """Obtiene un cliente por su ID."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = ?", (id_cliente,))
            
            data = cursor.fetchone()
            if data:
                columnas = [desc[0] for desc in cursor.description]
                return dict(zip(columnas, data))
            return None
        except Exception as e:
            print(f"Error al obtener cliente por ID: {e}")
            return None
        finally:
            db.close_connection()

    @staticmethod
    def filtrar_por_dni(dni):
        """Obtiene un cliente por su DNI (útil para validación)."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE dni = ?", (dni))
            data = cursor.fetchone()
            if data:
                columnas = [desc[0] for desc in cursor.description]
                return dict(zip(columnas, data))
            return None
        except Exception as e:
            print(f"Error al obtener cliente por DNI: {e}")
            return None
        finally:
            db.close_connection()

    #Gettes y Setters
    def get_id_cliente(self):
        return self.id_cliente
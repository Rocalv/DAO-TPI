from sistema_alquiler.persistencia.database.db_config import db

class Servicio:
    
    def __init__(self, id_servicio=None, nombre=None, descripcion=None, costo_base=None):
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.descripcion = descripcion
        self.costo_base = costo_base

    @staticmethod
    def crear(nombre, descripcion, costo_base):
        """Crea un nuevo servicio de mantenimiento."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO servicios (nombre, descripcion, costo_base)
                VALUES (?, ?, ?)
            """, (nombre, descripcion, costo_base))
            db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear servicio: {e}")
            db.rollback()
            return None
        finally:
            db.close_connection()

    @staticmethod
    def obtener_todos():
        """Obtiene todos los servicios de la base de datos."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM servicios")
            servicios_data = cursor.fetchall()
            
            servicios = []
            if servicios_data:
                columnas = [desc[0] for desc in cursor.description]
                for serv in servicios_data:
                    servicios.append(dict(zip(columnas, serv)))
            return servicios
            
        except Exception as e:
            print(f"Error al obtener servicios: {e}")
            return []
        finally:
            db.close_connection()

    @staticmethod
    def obtener_por_id(id_servicio):
        """Obtiene un servicio por su ID."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM servicios WHERE id_servicio = ?", (id_servicio,))
            data = cursor.fetchone()
            if data:
                columnas = [desc[0] for desc in cursor.description]
                return dict(zip(columnas, data))
            return None
        except Exception as e:
            print(f"Error al obtener servicio por ID: {e}")
            return None
        finally:
            db.close_connection()

    @staticmethod
    def actualizar(id_servicio, nombre, descripcion, costo_base):
        """Actualiza un servicio existente."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE servicios
                SET nombre = ?, descripcion = ?, costo_base = ?
                WHERE id_servicio = ?
            """, (nombre, descripcion, costo_base, id_servicio))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar servicio: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()

    @staticmethod
    def eliminar(id_servicio):
        """Elimina un servicio."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM servicios WHERE id_servicio = ?", (id_servicio,))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar servicio: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()
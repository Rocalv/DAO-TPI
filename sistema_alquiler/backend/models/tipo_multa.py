from sistema_alquiler.persistencia.database.db_config import db

class TipoMulta:
    
    def __init__(self, id_tipo_multa=None, motivo=None, descripcion=None, monto_sugerido=None):
        self.id_tipo_multa = id_tipo_multa
        self.motivo = motivo
        self.descripcion = descripcion
        self.monto_sugerido = monto_sugerido

    @staticmethod
    def crear(motivo, descripcion, monto_sugerido):
        """Crea un nuevo tipo de multa."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tipos_multa (motivo, descripcion, monto_sugerido)
                VALUES (?, ?, ?)
            """, (motivo, descripcion, monto_sugerido))
            db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear tipo de multa: {e}")
            db.rollback()
            return None
        finally:
            db.close_connection()

    @staticmethod
    def obtener_todos():
        """Obtiene todos los tipos de multa de la base de datos."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tipos_multa")
            tipos_data = cursor.fetchall()
            
            tipos = []
            if tipos_data:
                columnas = [desc[0] for desc in cursor.description]
                for tipo in tipos_data:
                    tipos.append(dict(zip(columnas, tipo)))
            return tipos
            
        except Exception as e:
            print(f"Error al obtener tipos de multa: {e}")
            return []
        finally:
            db.close_connection()

    @staticmethod
    def obtener_por_id(id_tipo_multa):
        """Obtiene un tipo de multa por su ID."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tipos_multa WHERE id_tipo_multa = ?", (id_tipo_multa,))
            data = cursor.fetchone()
            if data:
                columnas = [desc[0] for desc in cursor.description]
                return dict(zip(columnas, data))
            return None
        except Exception as e:
            print(f"Error al obtener tipo de multa por ID: {e}")
            return None
        finally:
            db.close_connection()

    @staticmethod
    def actualizar(id_tipo_multa, motivo, descripcion, monto_sugerido):
        """Actualiza un tipo de multa existente."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tipos_multa
                SET motivo = ?, descripcion = ?, monto_sugerido = ?
                WHERE id_tipo_multa = ?
            """, (motivo, descripcion, monto_sugerido, id_tipo_multa))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar tipo de multa: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()

    @staticmethod
    def eliminar(id_tipo_multa):
        """Elimina un tipo de multa."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tipos_multa WHERE id_tipo_multa = ?", (id_tipo_multa,))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar tipo de multa: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()
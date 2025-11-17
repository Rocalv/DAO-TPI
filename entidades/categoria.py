from persistencia.db_config import db # CORRECCIÓN: Importar la instancia 'db'

class Categoria:
    def __init__(self, id_categoria=None, nombre=None, descripcion=None, precio_dia=None):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_dia = precio_dia
    
    # Metodos: registrar, modificar, eliminar, consultar, filtrar_por_id

    @staticmethod
    def registrar(nombre, descripcion, precio_dia):
        """Crea una nueva categoría de vehículo."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO categorias (nombre, descripcion, precio_dia)
                VALUES (?, ?, ?)
            """, (nombre, descripcion, precio_dia,))
            db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear categoría: {e}")
            db.rollback()
            return None
        finally:
            db.close_connection()

    @staticmethod
    def consultar():
        """Obtiene todas las categorías de la base de datos."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categorias")
            categorias_data = cursor.fetchall()
            
            categorias = []
            if categorias_data:
                columnas = [desc[0] for desc in cursor.description]
                for cat in categorias_data:
                    categorias.append(dict(zip(columnas, cat)))
            return categorias
            
        except Exception as e:
            print(f"Error al obtener categorías: {e}")
            return []
        finally:
            db.close_connection()

    @staticmethod
    def filtrar_por_id(self):
        """Obtiene una categoría por su ID."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            id_categoria = self.obtener_id()
            cursor.execute("SELECT * FROM categorias WHERE id_categoria = ?", (id_categoria,))
            data = cursor.fetchone()
            if data:
                columnas = [desc[0] for desc in cursor.description]
                return dict(zip(columnas, data))
            return None
        except Exception as e:
            print(f"Error al obtener categoría por ID: {e}")
            return None
        finally:
            db.close_connection()

    @staticmethod
    def modificar(id_categoria, nombre, descripcion, precio_dia):
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE categorias
                SET nombre = ?, descripcion = ?, precio_dia = ?
                WHERE id_categoria = ?
            """, (nombre, descripcion, precio_dia, id_categoria,))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar categoría: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()

    @staticmethod
    def eliminar(id_categoria):
        """Elimina una categoría (¡Cuidado con las dependencias!)."""
        # Nota: Esto fallará si un vehículo está usando esta categoría.
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categorias WHERE id_categoria = ?", (id_categoria,))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar categoría: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()
    
    @staticmethod
    def obtener_id(self) -> int:
        """Obtiene el ID de una categoría dada su instancia."""
        return self.id_categoria if self else None
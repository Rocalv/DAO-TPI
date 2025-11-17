from persistencia.db_config import db # CORRECCIÓN: Importar la instancia 'db'
from entidades.alquiler import Alquiler
from entidades.tipo_multa import TipoMulta
class Multa:
    
    def __init__(self, id_multa=None, monto=None, fecha=None, estado=None, descripcion=None, alquiler: Alquiler=None, tipo_multa: TipoMulta=None):
        self.id_multa = id_multa
        self.monto = monto
        self.fecha = fecha
        self.estado = estado
        self.descripcion = descripcion
        self.alquiler = alquiler
        self.tipo_multa = tipo_multa

    @staticmethod
    def registrar(alquiler: Alquiler, tipo_multa: TipoMulta, monto, descripcion=None):
        """Crea una nueva multa asociada a un alquiler."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            id_alquiler = alquiler.get_id_alquiler()
            id_tipo_multa= tipo_multa.get_id_tipo_multa()

            cursor.execute("""
                INSERT INTO multas (id_alquiler, id_tipo_multa, monto, descripcion, estado, fecha)
                VALUES (?, ?, ?, ?, 'pendiente', date('now'))
            """, (id_alquiler, id_tipo_multa, monto, descripcion)) # <--- CAMBIO
            db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear multa: {e}")
            db.rollback()
            return None
        finally:
            db.close_connection()

    @staticmethod
    def obtener_por_alquiler(alquiler: Alquiler):
        """Obtiene todas las multas de un alquiler específico."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()

            id_alquiler = alquiler.get_id_alquiler()

            cursor.execute("""
                SELECT m.*, tm.motivo, tm.monto_sugerido
                FROM multas m
                JOIN tipos_multa tm ON m.id_tipo_multa = tm.id_tipo_multa
                WHERE m.id_alquiler = ?
            """, (id_alquiler,))
            
            multas_data = cursor.fetchall()
            
            multas = []
            if multas_data:
                columnas = [desc[0] for desc in cursor.description]
                for m in multas_data:
                    multas.append(dict(zip(columnas, m)))
            return multas
            
        except Exception as e:
            print(f"Error al obtener multas por alquiler: {e}")
            return []
        finally:
            db.close_connection()

    @staticmethod
    def pagar_multa(id_multa):
        """Actualiza el estado de una multa a 'pagada'."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE multas SET estado = 'Pagada' WHERE id_multa = ?", (id_multa,))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al pagar multa: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()
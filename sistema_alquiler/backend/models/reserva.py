# backend/models/reserva.py
from ..database.db_config import db

class Reserva:

    @staticmethod
    def crear(id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total) -> bool:
        """Crea un nuevo registro de reserva."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reservas (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total, estado)
                VALUES (?, ?, ?, ?, ?, ?, 'pendiente')
            """, (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al crear reserva: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()
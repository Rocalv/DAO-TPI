from persistencia.db_config import db
class Reserva:
    @staticmethod
    def registrar(id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total) -> bool:
        """Crea un nuevo registro de reserva."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reservas (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total, estado)
                VALUES (?, ?, ?, ?, ?, ?, 'pendiente')
            """, (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total))
            from persistencia.Repository.repository_estados import RepositoryEstados 
            id_estado_disponible = RepositoryEstados.obtener_id("Reservado")
            cursor.execute("""
                UPDATE vehiculos 
                SET id_estado = ?
                WHERE id_vehiculo = ?
            """, (id_estado_disponible, id_vehiculo))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al crear reserva: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()
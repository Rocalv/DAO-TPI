from persistencia.db_config import db
class RepositoryEstados:

    MAPA_ESTADOS = {
        "Alquilado": 1,
        "Disponible": 2,
        "FueraServicio": 3,
        "Mantenimiento": 4,
        'Reservado': 5, 
        'ParaMantenimiento': 6
    }
    # estados = ['Alquilado', 'Disponible', 'FueraServicio', 'Mantenimiento', 'Reservado', 'ParaMantenimiento']

    @staticmethod
    def obtener_id(nombre_estado: str) -> int:
        try:
            return RepositoryEstados.MAPA_ESTADOS[nombre_estado]
        except KeyError:
            raise ValueError(f"Estado desconocido: {nombre_estado}")

    @staticmethod
    def cambiar_estado(id_estado: int, id_vehiculo: int):
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE vehiculos 
                SET id_estado = ?
                WHERE id_vehiculo = ?
            """, (id_estado, id_vehiculo))
            db.commit()
        except Exception as e:
            print("Error cambiando estado en BD:", e)
            db.rollback()
            return False
        finally:
            db.close_connection()
        return True
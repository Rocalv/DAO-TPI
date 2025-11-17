from persistencia.db_config import db
from entidades.vehiculo import Vehiculo
from entidades.cliente import Cliente
from entidades.empleado import Empleado
from persistencia.Repository.repository_estados import RepositoryEstados

class Alquiler:
    def __init__(self, id_alquiler: int, cliente: Cliente, vehiculo: Vehiculo, empleado: Empleado, 
                 fecha_inicio: str, fecha_fin: str, costo_total: float):
        self.id_alquiler = id_alquiler
        self.cliente = cliente
        self.vehiculo = vehiculo
        self.empleado = empleado
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.costo_total = costo_total

    @staticmethod
    def crear_transaccion(id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total) -> bool:
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO alquileres
                (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total, estado)
                VALUES (?, ?, ?, ?, ?, ?, 'activo')
            """, (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total))
            id_estado_alquilado = RepositoryEstados.obtener_id("Alquilado")
            cursor.execute("""
                UPDATE vehiculos 
                SET id_estado = ?
                WHERE id_vehiculo = ?
            """, (id_estado_alquilado, id_vehiculo))
            db.commit()
            return True

        except Exception as e:
            print(f"Error en la transacción de alquiler: {e}")
            db.rollback()
            return False

        finally:
            db.close_connection()

    def get_id_alquiler(self):
        return self.id_alquiler


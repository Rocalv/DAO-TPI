from persistencia.db_config import db
from entidades.vehiculo import Vehiculo
from entidades.cliente import Cliente
from entidades.empleado import Empleado

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
    def crear_transaccion(alquiler) -> bool:

        conn = db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO alquileres
                (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total, estado)
                VALUES (?, ?, ?, ?, ?, ?, 'activo')
            """, (
                alquiler.cliente.get_id_cliente(),
                alquiler.vehiculo.get_id_vehiculo(),
                alquiler.empleado.get_id_empleado(),
                alquiler.fecha_inicio,
                alquiler.fecha_fin,
                alquiler.costo_total
            ))

            alquiler.vehiculo.alquilar()

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


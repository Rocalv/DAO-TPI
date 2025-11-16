from datetime import date, datetime
from typing import Optional, List
from sistema_alquiler.persistencia.database.db_config import db
from .estado_vehiculo import FabricaEstados # <-- Importante

class Alquiler:
    @staticmethod
    def crear_transaccion(id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total) -> bool:
        """
        Inicia una transacción para:
        1. Registrar el nuevo alquiler.
        2. Cambiar el estado del vehículo a 'alquilado'.
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        id_estado_alquilado = FabricaEstados.obtener_id_estado("alquilado")
        if not id_estado_alquilado:
            print("Error: No se encontró el ID del estado 'alquilado'")
            return False
            
        try:
            # 1. Insertar el nuevo alquiler
            cursor.execute("""
                INSERT INTO alquileres (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total, estado)
                VALUES (?, ?, ?, ?, ?, ?, 'activo')
            """, (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total))
            
            # 2. Actualizar el estado del vehículo
            cursor.execute("""
                UPDATE vehiculos SET id_estado = ? WHERE id_vehiculo = ?
            """, (id_estado_alquilado, id_vehiculo))
            
            db.commit()
            return True
            
        except Exception as e:
            print(f"Error en la transacción de alquiler: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()
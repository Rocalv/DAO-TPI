# backend/models/cargo_empleado.py
import sqlite3
from sistema_alquiler.persistencia.database.db_config import db

class CargoEmpleado:

    @staticmethod
    def obtener_todos():
        """Obtiene todos los cargos de la base de datos."""
        try:
            conn = db.get_connection()
            conn.row_factory = sqlite3.Row # Para obtener resultados como diccionarios
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM cargos_empleado ORDER BY nombre")
            cargos_data = cursor.fetchall()
            
            # Convertir a lista de diccionarios estándar
            cargos = [dict(row) for row in cargos_data]
            return cargos
            
        except Exception as e:
            print(f"Error al obtener cargos: {e}")
            return []
        finally:
            db.close_connection()
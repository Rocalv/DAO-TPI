import sqlite3
from typing import Optional
from persistencia.db_config import db

class CargoEmpleado:
    def __init__(self, id_cargo: str, nombre_cargo: str):
        self.id_cargo = id_cargo
        self.nombre = nombre_cargo
        
# Clase que representa un cargo o ROL del empleado
    @staticmethod
    def obtener_todos():
        """Obtiene todos los cargos de la base de datos."""
        try:
            conn = db.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM cargos_empleado ORDER BY nombre")
            cargos_data = cursor.fetchall()
            
            cargos = [dict(row) for row in cargos_data]
            return cargos
            
        except Exception as e:
            print(f"Error al obtener cargos: {e}")
            return []
        finally:
            db.close_connection()

    def obtener_registro(id_cargo: int) -> Optional['CargoEmpleado']:
        """Obtiene una instancia de CargoEmpleado por id."""
        try:
            conn = db.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM cargos_empleado WHERE id_cargo = ?", (id_cargo,))
            row = cursor.fetchone()

            if not row:
                return None

            return CargoEmpleado(
                id_cargo=row["id_cargo"],
                nombre=row["nombre"]
            )

        except Exception as e:
            print(f"Error al obtener cargo: {e}")
            return None
        finally:
            db.close_connection()


    #Metodos Getters
    def get_id_cargo(self):
        return self.id_cargo
    
    def get_nombre_cargo(self):
        return self.nombre
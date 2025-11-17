from typing import Optional, List
import sqlite3
from persistencia.db_config import db
from entidades.cargo_empleado import CargoEmpleado

class Empleado:
    """ Clase que representa un empleado del sistema de alquiler """
    
    def __init__(self, dni: str, nombre: str, apellido: str,
                 cargo: Optional[CargoEmpleado] = None, 
                 telefono: str = "", email: str = "",
                 foto_path: Optional[str] = None,
                 id_empleado: Optional[int] = None, activo: bool = True):
        self.id_empleado = id_empleado
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.cargo = cargo
        self.telefono = telefono
        self.email = email
        self.foto_path = foto_path
        self.activo = activo

    # Métodos: registrar, modificar, eliminar, consultar, filtrar_por_id, filtrar_por_dni, filtrar_por_cargo    
    
    def registrar(self) -> bool:
        """Registra el empleado."""
        id_cargo = self.cargo.get_id_cargo()

        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO empleados (dni, nombre, apellido, id_cargo, telefono, email, foto_path, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.dni, self.nombre, self.apellido, id_cargo,
                    self.telefono, self.email, self.foto_path, self.activo))
            self.id_empleado = cursor.lastrowid
            db.commit()
            return True
        except Exception as e:
            print(f"Error al guardar empleado: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()
    
    def modificar(self) -> bool:
        """Modifica o actualiza el empleado."""
        id_cargo = self.cargo.get_id_cargo()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE empleados 
                SET dni=?, nombre=?, apellido=?, id_cargo=?, telefono=?, email=?, foto_path=?, activo=?
                WHERE id_empleado=?
            """, (self.dni, self.nombre, self.apellido, id_cargo,
                    self.telefono, self.email, self.foto_path, self.activo, self.id_empleado))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al guardar empleado: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()
    
    def eliminar(self) -> bool:
        """Desactiva (soft delete) un empleado en la base de datos."""
        if self.id_empleado is None: return False
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE empleados SET activo = 0 WHERE id_empleado = ?", (self.id_empleado,))
            db.commit()
            self.activo = False
            return True
        except Exception as e:
            print(f"Error al eliminar empleado: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()
    
    def _crear_objeto_empleado(row: sqlite3.Row) -> 'Empleado':
        if not row:
            return None
        cargo = CargoEmpleado.obtener_registro(row["id_cargo"])

        return Empleado(
            id_empleado=row["id_empleado"],
            dni=row["dni"],
            nombre=row["nombre"],
            apellido=row["apellido"],
            cargo=cargo,
            telefono=row["telefono"],
            email=row["email"],
            foto_path=row["foto_path"],
            activo=bool(row["activo"])
        )

    def consultar(solo_activos: bool = True) -> List['Empleado']:
        """Lista todos los empleados, uniendo el nombre del cargo."""
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT e.*, c.nombre as id_cargo 
            FROM empleados e
            LEFT JOIN cargos_empleado c ON e.id_cargo = c.id_cargo
        """
        params = []
        if solo_activos:
            query += " WHERE e.activo = 1"
        query += " ORDER BY e.apellido, e.nombre"
        
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        db.close_connection()
        return [Empleado._crear_objeto_empleado(row) for row in rows]

    def filtrar_por_dni(dni: str) -> Optional['Empleado']:
        """Busca un empleado por su DNI, uniendo el nombre del cargo."""
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.*, c.nombre as cargo_nombre 
            FROM empleados e
            LEFT JOIN cargos_empleado c ON e.id_cargo = c.id_cargo
            WHERE e.dni = ?
        """, (dni,))
        row = cursor.fetchone()
        db.close_connection()
        return Empleado._crear_objeto_empleado(row)
    
    def filtrar_por_id(id_empleado: int) -> Optional['Empleado']:  #RARO
        """Busca un empleado por su ID, uniendo el nombre del cargo."""
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.*, c.nombre as cargo_nombre 
            FROM empleados e
            LEFT JOIN cargos_empleado c ON e.id_cargo = c.id_cargo
            WHERE e.id_empleado = ?
        """, (id_empleado,))
        row = cursor.fetchone()
        db.close_connection()
        return Empleado._crear_objeto_empleado(row)
    
    def filtrar_por_cargo(cargo_nombre: str) -> List['Empleado']:  #RARO
        """
        Lista todos los empleados activos que tienen un cargo específico.
        """
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT e.*, c.nombre as cargo_nombre 
            FROM empleados e
            JOIN cargos_empleado c ON e.id_cargo = c.id_cargo
            WHERE c.nombre = ? AND e.activo = 1
            ORDER BY e.apellido, e.nombre
        """
        
        try:
            cursor.execute(query, (cargo_nombre))
            rows = cursor.fetchall()
            return [Empleado._crear_objeto_empleado(row) for row in rows]
        except Exception as e:
            print(f"Error al listar por cargo: {e}")
            return []
        finally:
            db.close_connection()
    
    def __str__(self) -> str:
        """Representación en string del empleado."""
        return f"{self.apellido}, {self.nombre} - {self.cargo_nombre}"
    
    #getters y setters
    def get_id_empleado(self):
        return self.id_empleado
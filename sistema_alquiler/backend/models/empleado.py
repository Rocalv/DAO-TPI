# backend/models/empleado.py
from typing import Optional, List
import sqlite3
from ..database.db_config import db

class Empleado:
    """ Clase que representa un empleado del sistema de alquiler """
    
    def __init__(self, dni: str, nombre: str, apellido: str,
                 id_cargo: Optional[int] = None,
                 cargo_nombre: Optional[str] = None,
                 telefono: str = "", email: str = "",
                 foto_path: Optional[str] = None,
                 id_empleado: Optional[int] = None, activo: bool = True):
        
        self.id_empleado = id_empleado
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.id_cargo = id_cargo
        self.cargo_nombre = cargo_nombre
        self.telefono = telefono
        self.email = email
        self.foto_path = foto_path
        self.activo = activo
    
    
    def guardar(self) -> bool:
        """Guarda (Inserta o Actualiza) el empleado en la base de datos."""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.id_empleado is None:
                cursor.execute("""
                    INSERT INTO empleados (dni, nombre, apellido, id_cargo, telefono, email, foto_path, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (self.dni, self.nombre, self.apellido, self.id_cargo,
                      self.telefono, self.email, self.foto_path, self.activo))
                
                self.id_empleado = cursor.lastrowid
                db.commit()
                return True
            else:
                cursor.execute("""
                    UPDATE empleados 
                    SET dni=?, nombre=?, apellido=?, id_cargo=?, telefono=?, email=?, foto_path=?, activo=?
                    WHERE id_empleado=?
                """, (self.dni, self.nombre, self.apellido, self.id_cargo,
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
        if self.id_empleado is None:
            return False
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
    
    
    @staticmethod
    def _crear_objeto_empleado(row: sqlite3.Row) -> 'Empleado':
        """Helper para crear un objeto Empleado desde una fila de BD."""
        return Empleado(
            id_empleado=row['id_empleado'],
            dni=row['dni'],
            nombre=row['nombre'],
            apellido=row['apellido'],
            id_cargo=row['id_cargo'],
            cargo_nombre=row['cargo_nombre'],
            telefono=row['telefono'],
            email=row['email'],
            foto_path=row['foto_path'],
            activo=bool(row['activo'])
        )

    @staticmethod
    def buscar_por_dni(dni: str) -> Optional['Empleado']:
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
        return Empleado._crear_objeto_empleado(row) if row else None
    
    @staticmethod
    def buscar_por_id(id_empleado: int) -> Optional['Empleado']:
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
        return Empleado._crear_objeto_empleado(row) if row else None
    
    @staticmethod
    def listar_todos(solo_activos: bool = True) -> List['Empleado']:
        """Lista todos los empleados, uniendo el nombre del cargo."""
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT e.*, c.nombre as cargo_nombre 
            FROM empleados e
            LEFT JOIN cargos_empleado c ON e.id_cargo = c.id_cargo
        """
        
        if solo_activos:
            query += " WHERE e.activo = 1"
        
        query += " ORDER BY e.apellido, e.nombre"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        db.close_connection()
        
        return [Empleado._crear_objeto_empleado(row) for row in rows]
    
    def __str__(self) -> str:
        """Representación en string del empleado."""
        return f"{self.apellido}, {self.nombre} - {self.cargo_nombre}"
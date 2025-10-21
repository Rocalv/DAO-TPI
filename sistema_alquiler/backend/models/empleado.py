from typing import Optional, List
from database.db_config import db


class Empleado:
    """ Clase que representa un empleado del sistema de alquiler """
    def __init__(self, dni: str, nombre: str, apellido: str,
                 cargo: str = "", telefono: str = "", email: str = "",
                 id_empleado: Optional[int] = None, activo: bool = True):
        
        self.id_empleado = id_empleado
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.cargo = cargo
        self.telefono = telefono
        self.email = email
        self.activo = activo
    
    
    def guardar(self) -> bool:    
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.id_empleado is None:
                # Insertar nuevo empleado
                cursor.execute("""
                    INSERT INTO empleados (dni, nombre, apellido, cargo, telefono, email, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (self.dni, self.nombre, self.apellido, self.cargo,
                      self.telefono, self.email, self.activo))
                
                self.id_empleado = cursor.lastrowid
                db.commit()
                print(f"\n> Empleado {self.nombre} {self.apellido} registrado con ID: {self.id_empleado}")
                return True
            else:
                # Actualizar empleado existente
                cursor.execute("""
                    UPDATE empleados 
                    SET dni=?, nombre=?, apellido=?, cargo=?, telefono=?, email=?, activo=?
                    WHERE id_empleado=?
                """, (self.dni, self.nombre, self.apellido, self.cargo,
                      self.telefono, self.email, self.activo, self.id_empleado))
                
                db.commit()
                print(f"\n> Empleado {self.nombre} {self.apellido} actualizado")
                return True
                
        except Exception as e:
            print(f"\n> Error al guardar empleado: {e}")
            db.rollback()
            return False
    
    def eliminar(self) -> bool:
        if self.id_empleado is None:
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE empleados SET activo = 0 WHERE id_empleado = ?
            """, (self.id_empleado,))
            
            db.commit()
            self.activo = False
            print(f"\n> Empleado {self.nombre} {self.apellido} desactivado")
            return True
            
        except Exception as e:
            print(f"\n> Error al eliminar empleado: {e}")
            db.rollback()
            return False
    
    
    @staticmethod
    def buscar_por_dni(dni: str) -> Optional['Empleado']:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM empleados WHERE dni = ?", (dni,))
        row = cursor.fetchone()
        
        if row:
            return Empleado(
                id_empleado=row['id_empleado'],
                dni=row['dni'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                cargo=row['cargo'],
                telefono=row['telefono'],
                email=row['email'],
                activo=bool(row['activo'])
            )
        return None
    
    @staticmethod
    def buscar_por_id(id_empleado: int) -> Optional['Empleado']:
        """
        Busca un empleado por su ID.
        
        Args:
            id_empleado: ID del empleado
            
        Returns:
            Empleado si se encuentra, None en caso contrario
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM empleados WHERE id_empleado = ?", (id_empleado,))
        row = cursor.fetchone()
        
        if row:
            return Empleado(
                id_empleado=row['id_empleado'],
                dni=row['dni'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                cargo=row['cargo'],
                telefono=row['telefono'],
                email=row['email'],
                activo=bool(row['activo'])
            )
        return None
    
    @staticmethod
    def listar_todos(solo_activos: bool = True) -> List['Empleado']:
        """
        Lista todos los empleados.
        
        Args:
            solo_activos: Si True, solo lista empleados activos
            
        Returns:
            Lista de empleados
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if solo_activos:
            cursor.execute("SELECT * FROM empleados WHERE activo = 1 ORDER BY apellido, nombre")
        else:
            cursor.execute("SELECT * FROM empleados ORDER BY apellido, nombre")
        
        rows = cursor.fetchall()
        
        return [
            Empleado(
                id_empleado=row['id_empleado'],
                dni=row['dni'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                cargo=row['cargo'],
                telefono=row['telefono'],
                email=row['email'],
                activo=bool(row['activo'])
            )
            for row in rows
        ]
    
    
    def __str__(self) -> str:
        """Representación en string del empleado."""
        return f"{self.apellido}, {self.nombre} - {self.cargo}"
    
    
    #!def __repr__(self) -> str:
    #!   """Representación para debugging."""
    #!   return f"<Empleado {self.id_empleado}: {self.nombre} {self.apellido}>"
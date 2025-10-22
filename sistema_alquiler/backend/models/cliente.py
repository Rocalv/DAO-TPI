from datetime import date
from typing import Optional, List
from backend.database import db

class Cliente:
    def __init__(self, nombre: str, apellido: str, dni: str, 
                 telefono: str = "", email: str = "", direccion: str = "",
                 id_cliente: Optional[int] = None, 
                 fecha_registro: date = None,
                 activo: bool = True):
        
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.fecha_registro = fecha_registro or date.today()
        self.activo = activo
    
    
    def guardar(self) -> bool:
        """ Guarda o actualiza el cliente en la base de datos.
        
        :return: True si se guardó correctamente, False en caso contrario
        :rtype: bool 
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.id_cliente is None:
                # Insertar nuevo cliente
                cursor.execute("""
                    INSERT INTO clientes (nombre, apellido, dni, telefono, email, direccion, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (self.nombre, self.apellido, self.dni, self.telefono, 
                      self.email, self.direccion, self.activo))
                
                self.id_cliente = cursor.lastrowid
                db.commit()
                print(f"\n> Cliente {self.nombre} {self.apellido} registrado con ID: {self.id_cliente}")
                return True
            
            else:
                # Actualizar cliente existente
                cursor.execute("""
                    UPDATE clientes 
                    SET nombre=?, apellido=?, dni=?, telefono=?, email=?, direccion=?, activo=?
                    WHERE id_cliente=?
                """, (self.nombre, self.apellido, self.dni, self.telefono, 
                      self.email, self.direccion, self.activo, self.id_cliente))
                
                db.commit()
                print(f"\n> Cliente {self.nombre} {self.apellido} actualizado")
                return True
                
        except Exception as e:
            print(f"\n> Error al guardar cliente: {e}")
            db.rollback()
            return False
    
    
    def eliminar(self) -> bool:
        """ Elimina (desactiva) el cliente de la base de datos.
        
        :return: True si se desactiva correctamente
        :rtype: bool 
        """
        if self.id_cliente is None:
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE clientes SET activo = 0 WHERE id_cliente = ?
            """, (self.id_cliente,))
            
            db.commit()
            self.activo = False
            print(f"\n> Cliente {self.nombre} {self.apellido} desactivado")
            return True
            
        except Exception as e:
            print(f"\n> Error al eliminar cliente: {e}")
            db.rollback()
            return False
    
    
    @staticmethod
    def buscar_por_dni(dni: str) -> Optional['Cliente']:
        """ Busca un cliente por su DNI.
        
        :param dni: DNI del cliente a buscar
        :type dni: str
            
        :return: Cliente si se encuentra, None en caso contrario
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM clientes WHERE dni = ?
        """, (dni,))
        
        row = cursor.fetchone()
        
        if row:
            return Cliente(
                id_cliente=row['id_cliente'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                dni=row['dni'],
                telefono=row['telefono'],
                email=row['email'],
                direccion=row['direccion'],
                fecha_registro=row['fecha_registro'],
                activo=bool(row['activo'])
            )
        return None
    
    
    @staticmethod
    def buscar_por_id(id_cliente: int) -> Optional['Cliente']:
        """ Busca un cliente por su ID.
        
        :param id_cliente: ID del cliente
        :type id_cliente: int
        :return: Cliente si se encuentra, None en caso contrario
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM clientes WHERE id_cliente = ?
        """, (id_cliente,))
        
        row = cursor.fetchone()
        
        if row:
            return Cliente(
                id_cliente=row['id_cliente'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                dni=row['dni'],
                telefono=row['telefono'],
                email=row['email'],
                direccion=row['direccion'],
                fecha_registro=row['fecha_registro'],
                activo=bool(row['activo'])
            )
        return None
    
    
    @staticmethod
    def listar_todos(solo_activos: bool = True) -> List['Cliente']:
        """ Lista todos los clientes.
        
        :param solo_activos: Si True, solo lista clientes activos
        :type solo_activos: bool
            
        :return: Lista de clientes
        :rtype: list
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if solo_activos:
            cursor.execute("SELECT * FROM clientes WHERE activo = 1 ORDER BY apellido, nombre")
        else:
            cursor.execute("SELECT * FROM clientes ORDER BY apellido, nombre")
        
        rows = cursor.fetchall()
        
        return [
            Cliente(
                id_cliente=row['id_cliente'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                dni=row['dni'],
                telefono=row['telefono'],
                email=row['email'],
                direccion=row['direccion'],
                fecha_registro=row['fecha_registro'],
                activo=bool(row['activo'])
            )
            for row in rows
        ]
    
    def __str__(self) -> str:
        """Representación en string del cliente."""
        return f"{self.apellido}, {self.nombre} (DNI: {self.dni})"
    
    
    #!def __repr__(self) -> str:
    #!    """Representación para debugging."""
    #!    return f"<Cliente {self.id_cliente}: {self.nombre} {self.apellido}>"
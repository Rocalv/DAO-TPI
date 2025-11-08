# backend/models/vehiculo.py
from typing import List, Optional
import sqlite3
from ..database.db_config import db
from .estado_vehiculo import EstadoVehiculo, FabricaEstados # <-- IMPORTANTE

class Vehiculo:

    def __init__(self, patente: str, marca: str, modelo: str, anio: int, 
                 id_categoria: int, id_estado: int, # <-- IDs OBLIGATORIOS
                 color: str = "", kilometraje: int = 0, km_mantenimiento: int = 10000, 
                 foto_path: Optional[str] = None,
                 id_vehiculo: Optional[int] = None,
                 # Campos de JOIN
                 categoria_nombre: Optional[str] = None, 
                 precio_dia: Optional[float] = None,
                 estado_nombre: Optional[str] = None):
        
        self.id_vehiculo = id_vehiculo
        self.patente = patente
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.color = color
        self.kilometraje = kilometraje
        self.km_mantenimiento = km_mantenimiento
        self.foto_path = foto_path
        self.id_categoria = id_categoria
        self.id_estado = id_estado
        
        # --- LÓGICA DEL PATRÓN STATE ---
        self.estado_obj: EstadoVehiculo = FabricaEstados.obtener_estado_por_id(self.id_estado)
        
        # Campos de JOIN (para vistas)
        self.categoria_nombre = categoria_nombre
        self.precio_dia = precio_dia
        self.estado_nombre = self.estado_obj.nombre_estado() # Usamos el del objeto

    def guardar(self) -> bool:
        """Guarda (Inserta o Actualiza) el vehículo en la BD."""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Actualizamos el ID del estado por si cambió
        self.id_estado = FabricaEstados.obtener_id_estado(self.estado_obj.nombre_estado())
        
        try:
            if self.id_vehiculo is None:
                cursor.execute("""
                    INSERT INTO vehiculos (patente, marca, modelo, anio, color, kilometraje, 
                                           km_mantenimiento, id_categoria, id_estado, foto_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (self.patente, self.marca, self.modelo, self.anio, self.color, 
                      self.kilometraje, self.km_mantenimiento, self.id_categoria, 
                      self.id_estado, self.foto_path))
                self.id_vehiculo = cursor.lastrowid
            else:
                cursor.execute("""
                    UPDATE vehiculos
                    SET patente=?, marca=?, modelo=?, anio=?, color=?, kilometraje=?, 
                        km_mantenimiento=?, id_categoria=?, id_estado=?, foto_path=?
                    WHERE id_vehiculo=?
                """, (self.patente, self.marca, self.modelo, self.anio, self.color, 
                      self.kilometraje, self.km_mantenimiento, self.id_categoria, 
                      self.id_estado, self.foto_path, self.id_vehiculo))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al guardar vehículo: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()

    def eliminar(self) -> bool:
        """Da de baja el vehículo (cambia el estado a 'Baja')."""
        if self.id_vehiculo is None: return False
        
        self.set_estado("Baja") # Usamos la fábrica
        return self.guardar() # Guardamos el cambio

    def set_estado(self, nuevo_estado_nombre: str):
        """Cambia el objeto de estado del vehículo."""
        self.estado_obj = FabricaEstados.obtener_estado_por_nombre(nuevo_estado_nombre)

    @staticmethod
    def _crear_objeto(row: sqlite3.Row) -> 'Vehiculo':
        """Helper para crear objetos Vehiculo desde filas de BD."""
        return Vehiculo(
            id_vehiculo=row['id_vehiculo'],
            patente=row['patente'],
            marca=row['marca'],
            modelo=row['modelo'],
            anio=row['anio'],
            color=row['color'],
            kilometraje=row['kilometraje'],
            km_mantenimiento=row['km_mantenimiento'],
            foto_path=row['foto_path'],
            id_categoria=row['id_categoria'],
            id_estado=row['id_estado'],
            # Campos de JOIN
            categoria_nombre=row['categoria_nombre'],
            precio_dia=row['precio_dia']
            # estado_nombre se genera en el __init__
        )

    @staticmethod
    def listar_todos(excluir_baja: bool = True) -> List['Vehiculo']:
        """Obtiene todos los vehículos, uniéndolos con categoría."""
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT v.*, c.nombre as categoria_nombre, c.precio_dia
            FROM vehiculos v
            JOIN categorias c ON v.id_categoria = c.id_categoria
            LEFT JOIN estados_vehiculo e ON v.id_estado = e.id_estado
        """
        params = []
        if excluir_baja:
            query += " WHERE e.nombre != ?"
            params.append('Baja')
        
        query += " ORDER BY v.marca, v.modelo"
        cursor.execute(query, tuple(params))
        
        rows = cursor.fetchall()
        db.close_connection()
        return [Vehiculo._crear_objeto(row) for row in rows]

    @staticmethod
    def buscar_por_id(id_vehiculo: int) -> Optional['Vehiculo']:
        """Obtiene un vehículo por su ID."""
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT v.*, c.nombre as categoria_nombre, c.precio_dia
            FROM vehiculos v
            JOIN categorias c ON v.id_categoria = c.id_categoria
            WHERE v.id_vehiculo = ?
        """, (id_vehiculo,))
        
        row = cursor.fetchone()
        db.close_connection()
        return Vehiculo._crear_objeto(row) if row else None
    
    @staticmethod
    def buscar_por_patente(patente: str) -> Optional['Vehiculo']:
        """Busca un vehículo por su Patente."""
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.*, c.nombre as categoria_nombre, c.precio_dia
            FROM vehiculos v
            JOIN categorias c ON v.id_categoria = c.id_categoria
            WHERE v.patente = ?
        """, (patente,))
        row = cursor.fetchone()
        db.close_connection()
        return Vehiculo._crear_objeto(row) if row else None
    
    # --- MÉTODO NUEVO (para Mantenimiento) ---
    @staticmethod
    def buscar_para_mantenimiento(patente: Optional[str] = None, id_categoria: Optional[int] = None) -> List['Vehiculo']:
        """
        Busca vehículos que puedan ir a mantenimiento (estado 'disponible').
        Filtra por patente y/o categoría si se proveen.
        """
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Comportamiento definido en el Patrón State:
        # Solo 'disponible' puede ir a mantenimiento.
        query = """
            SELECT v.*, c.nombre as categoria_nombre, c.precio_dia
            FROM vehiculos v
            JOIN categorias c ON v.id_categoria = c.id_categoria
            JOIN estados_vehiculo e ON v.id_estado = e.id_estado
            WHERE e.nombre = 'disponible'
        """
        params = []
        
        if patente:
            query += " AND v.patente LIKE ?"
            params.append(f"%{patente}%")
            
        if id_categoria:
            query += " AND v.id_categoria = ?"
            params.append(id_categoria)
            
        query += " ORDER BY v.marca, v.modelo"
        
        try:
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            return [Vehiculo._crear_objeto(row) for row in rows]
        except Exception as e:
            print(f"Error al buscar vehículos para mantenimiento: {e}")
            return []
        finally:
            db.close_connection()
    
    def __str__(self) -> str:
        return f"{self.marca} {self.modelo} ({self.patente}) - {self.estado_obj.nombre_estado()}"
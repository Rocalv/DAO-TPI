from typing import List, Optional
import sqlite3
from persistencia.db_config import db 
from persistencia.Repository.repository_estados import RepositoryEstados as RepositoryEstados
from entidades.categoria import Categoria
from entidades.patron_state.estado_vehiculo import EstadoVehiculo
from entidades.patron_state.disponible import Disponible

class Vehiculo:

    def __init__(self, patente: str, marca: str, modelo: str, anio: int, 
                 categoria: Categoria,
                 color: str = "", kilometraje: int = 0, km_mantenimiento: int = 10000, 
                 foto_path: Optional[str] = None,
                 precio_dia: Optional[float] = None,
                 estado: Optional[EstadoVehiculo] = None,
                 id_vehiculo: Optional[int] = None):
        
        self.patente = patente
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.color = color
        self.kilometraje = kilometraje
        self.km_mantenimiento = km_mantenimiento
        self.foto_path = foto_path
        self.categoria = categoria
        self.precio_dia = precio_dia
        self.estado = estado if estado is not None else Disponible()
        self.id_vehiculo = id_vehiculo
        
    # Metodos: 

    def registrar(self) -> bool:
        """Guarda (Inserta o Actualiza) el vehículo en la BD."""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            id_estado = RepositoryEstados.MAPA_ESTADOS.get(self.estado.nombre_estado()) 
            id_categoria = self.categoria.id_categoria

            cursor.execute("""
                INSERT INTO vehiculos (patente, marca, modelo, anio, color, kilometraje, 
                                        km_mantenimiento, foto_path, id_estado, id_categoria)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.patente, self.marca, self.modelo, self.anio, self.color, 
                    self.kilometraje, self.km_mantenimiento,
                    self.foto_path, id_estado, id_categoria))
            self.id_vehiculo = cursor.lastrowid
            db.commit()
            return True
        except Exception as e:
            print(f"Error al guardar vehículo: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()
    
    def modificar(self) -> bool:
        """Actualiza el vehículo en la BD."""
        conn = db.get_connection()
        cursor = conn.cursor()
        id_estado = RepositoryEstados.MAPA_ESTADOS.get(self.estado.nombre_estado()) 
        id_categoria = self.categoria.id_categoria
        
        if self.id_vehiculo is None:
            return False
        try:
            cursor.execute("""
                    UPDATE vehiculos
                    SET patente=?, marca=?, modelo=?, anio=?, color=?, kilometraje=?, 
                        km_mantenimiento=?, id_categoria=?, id_estado=?, foto_path=?
                    WHERE id_vehiculo=?
                """, (self.patente, self.marca, self.modelo, self.anio, self.color, 
                      self.kilometraje, self.km_mantenimiento, id_categoria, 
                      id_estado, self.foto_path, self.id_vehiculo))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al guardar vehículo: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()

    def eliminar(self) -> bool:
        """Da de baja el vehículo (cambia el estado a 'FueraServicio')."""
        if self.id_vehiculo is None: return False
        try:
            from entidades.patron_state.fuera_servicio import FueraServicio
            self.estado.fuera_servicio(self)
        except ValueError:
            RepositoryEstados.cambiar_estado(RepositoryEstados.obtener_id("Baja"), self.id_vehiculo)
            self.estado = FueraServicio() 
            
        return self.modificar()
    
    def alquilar(self):
        """Pide al estado que ejecute la transición a 'alquilado'."""
        self.estado.alquilar(self)

    def mantenimiento(self):
        """Pide al estado que ejecute la transición a 'mantenimiento'."""
        self.estado.mantenimiento(self)

    def disponibilizar(self):
        """Pide al estado que ejecute la transición a 'disponible'."""
        self.estado.disponibilizar(self)


    @staticmethod
    def consultar(excluir_baja: bool = True) -> List['Vehiculo']:
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

    def filtrar_por_id(id_vehiculo: int) -> Optional['Vehiculo']:
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
    
    def filtrar_por_patente(patente: str) -> Optional['Vehiculo']:
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
    
    def filtar_disponibles(fecha_inicio: str, fecha_fin: str, id_categoria: Optional[int] = None, marca: Optional[str] = None) -> List['Vehiculo']:
        """
        Busca vehículos que estén 'disponibles' Y que no tengan
        conflictos de fechas en las tablas 'alquileres' o 'reservas'.
        """
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT v.*, c.nombre as categoria_nombre, c.precio_dia
            FROM vehiculos v
            JOIN categorias c ON v.id_categoria = c.id_categoria
            JOIN estados_vehiculo e ON v.id_estado = e.id_estado
            WHERE
                e.nombre = 'disponible' 
                
                AND v.id_vehiculo NOT IN (
                    SELECT a.id_vehiculo FROM alquileres a
                    WHERE a.estado = 'activo'
                    AND a.fecha_inicio <= ? 
                    AND a.fecha_fin >= ? 
                )
                
                AND v.id_vehiculo NOT IN (
                    SELECT r.id_vehiculo FROM reservas r
                    WHERE r.estado = 'pendiente'
                    AND r.fecha_inicio <= ?
                    AND r.fecha_fin >= ?
                )
        """
        params = [fecha_fin, fecha_inicio, fecha_fin, fecha_inicio]
        
        if id_categoria:
            query += " AND v.id_categoria = ?"
            params.append(id_categoria)
        if marca:
            query += " AND v.marca LIKE ?"
            params.append(f"%{marca}%")
            
        query += " ORDER BY c.precio_dia, v.marca"
            
        try:
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            return [Vehiculo._crear_objeto(row) for row in rows]
        except Exception as e:
            print(f"Error al buscar disponibles: {e}")
            return []
        finally:
            db.close_connection()
    
    @staticmethod
    def _crear_objeto(row: sqlite3.Row) -> 'Vehiculo':
        from entidades.patron_state.disponible import Disponible
        from entidades.patron_state.alquilado import Alquilado
        from entidades.patron_state.mantenimiento import Mantenimiento
        from entidades.patron_state.fuera_servicio import FueraServicio
        mapa_estados = {
            1: Alquilado(),
            2: Disponible(),
            3: FueraServicio(),
            4: Mantenimiento()
        }

        estado = mapa_estados.get(row['id_estado'], Disponible())
        categoria = Categoria(row['id_categoria'], row['categoria_nombre'])

        return Vehiculo(
            patente=row['patente'],
            marca=row['marca'],
            modelo=row['modelo'],
            anio=row['anio'],
            categoria=categoria,
            color=row['color'],
            kilometraje=row['kilometraje'],
            km_mantenimiento=row['km_mantenimiento'],
            foto_path=row['foto_path'],
            precio_dia=row['precio_dia'], 
            estado=estado,
            id_vehiculo=row['id_vehiculo']
        )
    
    def __str__(self) -> str:
        return f"{self.marca} {self.modelo} ({self.patente}) - {self.estado.nombre_estado()}"
    
    #Gettes y Setters
    def get_id_vehiculo(self):
        return self.id_vehiculo
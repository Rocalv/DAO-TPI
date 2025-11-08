# backend/models/mantenimiento.py
import sqlite3
from ..database.db_config import db
from .estado_vehiculo import FabricaEstados

class Mantenimiento:

    def __init__(self, id_vehiculo: int, id_servicio: int, fecha_inicio: str, 
                 kilometraje: int, descripcion: str = None, 
                 proveedor: str = None, costo: float = 0.0, 
                 estado: str = 'pendiente', fecha_fin: str = None, 
                 id_mantenimiento: int = None, id_empleado: int = None):
        
        self.id_mantenimiento = id_mantenimiento
        self.id_vehiculo = id_vehiculo
        self.id_servicio = id_servicio
        self.fecha_inicio = fecha_inicio
        self.kilometraje = kilometraje
        self.descripcion = descripcion
        self.proveedor = proveedor
        self.costo = costo
        self.estado = estado
        self.fecha_fin = fecha_fin
        self.id_empleado = id_empleado

    @staticmethod
    def crear_mantenimiento_transaccion(id_vehiculo: int, id_servicio: int, kilometraje: int, descripcion: str, proveedor: str) -> bool:
        """
        Inicia una transacción para registrar un mantenimiento y 
        actualizar el estado del vehículo a 'mantenimiento'.
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        id_estado_mantenimiento = FabricaEstados.obtener_id_estado("mantenimiento")
        if not id_estado_mantenimiento:
            print("Error: No se encontró el ID del estado 'mantenimiento'")
            return False
            
        try:
            cursor.execute("""
                INSERT INTO mantenimientos (id_vehiculo, id_servicio, fecha_inicio, 
                                            kilometraje, descripcion, proveedor, estado)
                VALUES (?, ?, date('now'), ?, ?, ?, 'pendiente')
            """, (id_vehiculo, id_servicio, kilometraje, descripcion, proveedor))
            
            cursor.execute("""
                UPDATE vehiculos SET id_estado = ? WHERE id_vehiculo = ?
            """, (id_estado_mantenimiento, id_vehiculo))
            
            db.commit()
            return True
            
        except Exception as e:
            print(f"Error en la transacción de mantenimiento: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()

    @staticmethod
    def finalizar_mantenimiento_transaccion(id_mantenimiento: int, fecha_fin: str, costo: float) -> bool:
        """
        Finaliza un mantenimiento y revierte el estado del vehículo a 'disponible'.
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        id_estado_disponible = FabricaEstados.obtener_id_estado("disponible")
        
        try:
            cursor.execute("SELECT id_vehiculo FROM mantenimientos WHERE id_mantenimiento = ?", (id_mantenimiento,))
            row = cursor.fetchone()
            if not row:
                raise Exception("Mantenimiento no encontrado")
            id_vehiculo = row[0]

            cursor.execute("""
                UPDATE mantenimientos 
                SET estado = 'finalizado', fecha_fin = ?, costo = ?
                WHERE id_mantenimiento = ?
            """, (fecha_fin, costo, id_mantenimiento))
            
            cursor.execute("""
                UPDATE vehiculos SET id_estado = ? WHERE id_vehiculo = ?
            """, (id_estado_disponible, id_vehiculo))
            
            db.commit()
            return True
            
        except Exception as e:
            print(f"Error al finalizar mantenimiento: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()

    @staticmethod
    def listar_pendientes() -> list:
        """
        Lista todos los mantenimientos pendientes o en progreso.
        """
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT m.*, v.patente, v.marca, v.modelo, s.nombre as servicio_nombre
                FROM mantenimientos m
                JOIN vehiculos v ON m.id_vehiculo = v.id_vehiculo
                JOIN servicios s ON m.id_servicio = s.id_servicio
                WHERE m.estado = 'pendiente'
                ORDER BY m.fecha_inicio
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error al listar mantenimientos: {e}")
            return []
        finally:
            db.close_connection()
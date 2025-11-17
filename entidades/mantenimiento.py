import sqlite3
from persistencia.db_config import db
from entidades.vehiculo import Vehiculo
from entidades.servicio import Servicio
from entidades.empleado import Empleado

class Mantenimiento:
    def __init__(self, vehiculo: Vehiculo, servicio: Servicio, fecha_inicio: str, 
                 kilometraje: int, descripcion: str = None, 
                 proveedor: str = None, costo: float = 0.0, fecha_fin: str = None, 
                 estado: str = "Pendiente",
                 id_mantenimiento: int = None, empleado: Empleado = None):
        
        self.id_mantenimiento = id_mantenimiento
        self.vehiculo = vehiculo
        self.servicio = servicio
        self.fecha_inicio = fecha_inicio
        self.kilometraje = kilometraje
        self.descripcion = descripcion
        self.proveedor = proveedor
        self.costo = costo
        self.estado = estado
        self.fecha_fin = fecha_fin
        self.empleado = empleado

    @staticmethod
    def crear_mantenimiento_transaccion(vehiculo: Vehiculo, servicio: Servicio, kilometraje: int,
                                        descripcion: str, proveedor: str, 
                                        empleado: Empleado) -> bool:
        """
        Inicia una transacción para registrar un mantenimiento y 
        recordar que el vehiculo ya debe de estar en el estado 'ParaMantenimiento'.
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        id_vehiculo = vehiculo.get_id_vehiculo()
        id_servicio = servicio.id_servicio
        id_empleado = empleado.get_id_empleado()
        vehiculo.mantenimiento()
            
        try:
            cursor.execute("""
                INSERT INTO mantenimientos (id_vehiculo, id_servicio, fecha_inicio, 
                                            kilometraje, descripcion, proveedor, estado, 
                                            id_empleado) 
                VALUES (?, ?, date('now'), ?, ?, ?, 'Pendiente', ?) 
            """, (id_vehiculo, id_servicio, kilometraje, descripcion, proveedor, id_empleado))
            
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
        Finaliza un mantenimiento y revierte el estado del vehículo a 'Disponible'.
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id_vehiculo FROM mantenimientos WHERE id_mantenimiento = ?", (id_mantenimiento,))
            row = cursor.fetchone()
            if not row:
                raise Exception("Mantenimiento no encontrado")
            id_vehiculo = row[0]

            cursor.execute("""
                UPDATE mantenimientos 
                SET estado = 'Finalizado', fecha_fin = ?, costo = ?
                WHERE id_mantenimiento = ?
            """, (fecha_fin, costo, id_mantenimiento))
            
            instancia_vehiculo: Vehiculo = Vehiculo.filtrar_por_id(id_vehiculo)
            instancia_vehiculo.disponibilizar()
            
            db.commit()
            return True
            
        except Exception as e:
            print(f"Error al finalizar mantenimiento: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()

    @staticmethod
    def filtrar_pendientes() -> list:
        """
        Lista todos los mantenimientos pendientes o en progreso.
        """
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT m.*, v.patente, v.marca, v.modelo, s.nombre as servicio_nombre,
                       e.nombre as empleado_nombre, e.apellido as empleado_apellido
                FROM mantenimientos m
                JOIN vehiculos v ON m.id_vehiculo = v.id_vehiculo
                JOIN servicios s ON m.id_servicio = s.id_servicio
                LEFT JOIN empleados e ON m.id_empleado = e.id_empleado
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
    
    @staticmethod
    def filtrar_finalizados() -> list:
        """
        Lista todos los mantenimientos que ya han sido finalizados,
        ordenados por fecha de finalización (más recientes primero).
        """
        
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT m.*, 
                       v.patente, v.marca, v.modelo, 
                       s.nombre as servicio_nombre,
                       e.nombre as empleado_nombre, e.apellido as empleado_apellido
                FROM mantenimientos m
                JOIN vehiculos v ON m.id_vehiculo = v.id_vehiculo
                JOIN servicios s ON m.id_servicio = s.id_servicio
                LEFT JOIN empleados e ON m.id_empleado = e.id_empleado
                WHERE m.estado = 'finalizado'
                ORDER BY m.fecha_fin DESC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error al listar mantenimientos finalizados: {e}")
            return []
        finally:
            db.close_connection()
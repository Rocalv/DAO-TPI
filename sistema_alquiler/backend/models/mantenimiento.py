from datetime import date
from typing import Optional, List
from backend.database.db_config import db


class Mantenimiento:
    """Clase que representa el mantenimiento de un vehículo"""
    
    # Estados simples como las otras clases
    ESTADO_PENDIENTE = "pendiente"
    ESTADO_COMPLETADO = "completado"
    ESTADO_CANCELADO = "cancelado"
    
    ESTADOS_VALIDOS = [ESTADO_PENDIENTE, ESTADO_COMPLETADO, ESTADO_CANCELADO]
    
    def __init__(self, fecha_inicio: date, tipo: str, kilometraje: int, 
                 id_vehiculo: int, id_empleado: int,
                 fecha_fin: Optional[date] = None, descripcion: str = "",
                 costo: float = 0.0, proveedor: str = "",
                 estado: str = ESTADO_PENDIENTE,
                 id_mantenimiento: Optional[int] = None):
        
        self.id_mantenimiento = id_mantenimiento
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tipo = tipo
        self.descripcion = descripcion
        self.costo = costo
        self.kilometraje = kilometraje
        self.proveedor = proveedor
        self.estado = estado
        self.id_vehiculo = id_vehiculo
        self.id_empleado = id_empleado
    
    
    def validar_fechas(self) -> bool:
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            print("\n> Error: La fecha de fin no puede ser anterior a la fecha de inicio")
            return False
        return True
    
    
    def validar_estado(self) -> bool:
        if self.estado not in self.ESTADOS_VALIDOS:
            print(f"\n> Error: Estado '{self.estado}' no válido")
            return False
        return True
    
    
    def guardar(self) -> bool:
        if not self.validar_fechas() or not self.validar_estado():
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.id_mantenimiento is None:
                cursor.execute("""
                    INSERT INTO mantenimientos 
                    (fecha_inicio, fecha_fin, tipo, descripcion, costo, kilometraje, 
                     proveedor, estado, id_vehiculo, id_empleado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (self.fecha_inicio, self.fecha_fin, self.tipo, self.descripcion,
                      self.costo, self.kilometraje, self.proveedor, self.estado,
                      self.id_vehiculo, self.id_empleado))
                
                self.id_mantenimiento = cursor.lastrowid
                db.commit()
                print(f"\n> Mantenimiento registrado con ID: {self.id_mantenimiento}")
                return True
            
            else:
                cursor.execute("""
                    UPDATE mantenimientos 
                    SET fecha_inicio=?, fecha_fin=?, tipo=?, descripcion=?, costo=?,
                        kilometraje=?, proveedor=?, estado=?, id_vehiculo=?, id_empleado=?
                    WHERE id_mantenimiento=?
                """, (self.fecha_inicio, self.fecha_fin, self.tipo, self.descripcion,
                      self.costo, self.kilometraje, self.proveedor, self.estado,
                      self.id_vehiculo, self.id_empleado, self.id_mantenimiento))
                
                db.commit()
                print(f"\n> Mantenimiento actualizado")
                return True
                
        except Exception as e:
            print(f"\n> Error al guardar mantenimiento: {e}")
            db.rollback()
            return False
    
    
    def marcar_como_completado(self, fecha_fin: date, costo_final: float = None) -> bool:
        if self.id_mantenimiento is None:
            print("\n> Error: El mantenimiento no ha sido guardado")
            return False
        
        if self.estado == self.ESTADO_COMPLETADO:
            print(f"\n> El mantenimiento ya está completado")
            return True
            
        if self.estado == self.ESTADO_CANCELADO:
            print(f"\n> Error: No se puede completar un mantenimiento cancelado")
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            self.fecha_fin = fecha_fin
            if costo_final is not None:
                self.costo = costo_final
            
            cursor.execute("""
                UPDATE mantenimientos 
                SET estado = ?, fecha_fin = ?, costo = ?
                WHERE id_mantenimiento = ?
            """, (self.ESTADO_COMPLETADO, self.fecha_fin, self.costo, self.id_mantenimiento))
            
            from .vehiculo import Vehiculo
            vehiculo = Vehiculo.buscar_por_id(self.id_vehiculo)
            if vehiculo:
                vehiculo.cambiar_estado('disponible')  # Volver a disponible
                vehiculo.km_mantenimiento = self.kilometraje + 10000  # Próximo mantenimiento
                vehiculo.guardar()
            
            db.commit()
            self.estado = self.ESTADO_COMPLETADO
            print(f"\n> Mantenimiento #{self.id_mantenimiento} completado")
            return True
            
        except Exception as e:
            print(f"\n> Error al completar mantenimiento: {e}")
            db.rollback()
            return False
    
    
    def cancelar(self) -> bool:
        if self.id_mantenimiento is None:
            print("\n> Error: El mantenimiento no ha sido guardado")
            return False
        
        if self.estado == self.ESTADO_CANCELADO:
            print(f"\n> El mantenimiento ya está cancelado")
            return True
            
        if self.estado == self.ESTADO_COMPLETADO:
            print(f"\n> Error: No se puede cancelar un mantenimiento completado")
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE mantenimientos SET estado = ? WHERE id_mantenimiento = ?
            """, (self.ESTADO_CANCELADO, self.id_mantenimiento))
            
            db.commit()
            self.estado = self.ESTADO_CANCELADO
            print(f"\n> Mantenimiento #{self.id_mantenimiento} cancelado")
            return True
            
        except Exception as e:
            print(f"\n> Error al cancelar mantenimiento: {e}")
            db.rollback()
            return False
    
    
    def calcular_duracion(self) -> int:
        """ Calcula la duración en días del mantenimiento.
        
        :return: Número de días (0 si no está finalizado)
        :rtype: int
        """
        if not self.fecha_fin:
            return 0
        return (self.fecha_fin - self.fecha_inicio).days

    def es_mantenimiento_preventivo(self) -> bool:
        return self.tipo.lower() == "preventivo"

    @staticmethod
    def listar_activos() -> List['Mantenimiento']:
        """ Lista todos los mantenimientos pendientes o en proceso.
            
        :return: Lista de mantenimientos activos
        :rtype: list
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM mantenimientos 
            WHERE estado = ? 
            ORDER BY fecha_inicio ASC
            """, (Mantenimiento.ESTADO_PENDIENTE,))
        
        rows = cursor.fetchall()
        
        return [
            Mantenimiento(
                id_mantenimiento=row['id_mantenimiento'],
                fecha_inicio=date.fromisoformat(row['fecha_inicio']),
                fecha_fin=date.fromisoformat(row['fecha_fin']) if row['fecha_fin'] else None,
                tipo=row['tipo'],
                descripcion=row['descripcion'],
                costo=row['costo'],
                kilometraje=row['kilometraje'],
                proveedor=row['proveedor'],
                estado=row['estado'],
                id_vehiculo=row['id_vehiculo'],
                id_empleado=row['id_empleado']
            )
            for row in rows
        ]
    
    
    @staticmethod
    def buscar_por_id(id_mantenimiento: int) -> Optional['Mantenimiento']:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM mantenimientos WHERE id_mantenimiento = ?", (id_mantenimiento,))
        row = cursor.fetchone()
        
        if row:
            return Mantenimiento(
                id_mantenimiento=row['id_mantenimiento'],
                fecha_inicio=date.fromisoformat(row['fecha_inicio']),
                fecha_fin=date.fromisoformat(row['fecha_fin']) if row['fecha_fin'] else None,
                tipo=row['tipo'],
                descripcion=row['descripcion'],
                costo=row['costo'],
                kilometraje=row['kilometraje'],
                proveedor=row['proveedor'],
                estado=row['estado'],
                id_vehiculo=row['id_vehiculo'],
                id_empleado=row['id_empleado']
            )
        return None
    
    
    @staticmethod
    def listar_por_vehiculo(id_vehiculo: int) -> List['Mantenimiento']:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM mantenimientos 
            WHERE id_vehiculo = ? 
            ORDER BY fecha_inicio DESC
        """, (id_vehiculo,))
        
        rows = cursor.fetchall()
        
        return [
            Mantenimiento(
                id_mantenimiento=row['id_mantenimiento'],
                fecha_inicio=date.fromisoformat(row['fecha_inicio']),
                fecha_fin=date.fromisoformat(row['fecha_fin']) if row['fecha_fin'] else None,
                tipo=row['tipo'],
                descripcion=row['descripcion'],
                costo=row['costo'],
                kilometraje=row['kilometraje'],
                proveedor=row['proveedor'],
                estado=row['estado'],
                id_vehiculo=row['id_vehiculo'],
                id_empleado=row['id_empleado']
            )
            for row in rows
        ]
    
    
    def __str__(self) -> str:
        return f"Mantenimiento #{self.id_mantenimiento} - {self.tipo} - {self.estado}"
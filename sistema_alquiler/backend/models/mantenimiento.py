from datetime import date
from typing import Optional, List
from backend.database.db_config import db


class Mantenimiento:
    """Clase que representa el mantenimiento de un vehículo"""
    
    # Estados posibles de un mantenimiento
    ESTADO_PENDIENTE = "pendiente"
    ESTADO_EN_PROCESO = "en_proceso"
    ESTADO_COMPLETADO = "completado"
    ESTADO_CANCELADO = "cancelado"
    
    ESTADOS_VALIDOS = [ESTADO_PENDIENTE, ESTADO_EN_PROCESO, ESTADO_COMPLETADO, ESTADO_CANCELADO]
    
    # Tipos de mantenimiento
    TIPO_PREVENTIVO = "preventivo"
    TIPO_CORRECTIVO = "correctivo"
    TIPO_REVISION = "revision"
    
    TIPOS_VALIDOS = [TIPO_PREVENTIVO, TIPO_CORRECTIVO, TIPO_REVISION]
    
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
            print(f"\n> Error: Estado '{self.estado}' no válido. Estados permitidos: {', '.join(self.ESTADOS_VALIDOS)}")
            return False
        return True
    

    def esta_pendiente(self) -> bool:
        return self.estado == self.ESTADO_PENDIENTE

    
    def esta_en_proceso(self) -> bool:
        return self.estado == self.ESTADO_EN_PROCESO

    
    def esta_completado(self) -> bool:
        return self.estado == self.ESTADO_COMPLETADO

    
    def esta_cancelado(self) -> bool:
        return self.estado == self.ESTADO_CANCELADO

    
    def validar_tipo(self) -> bool:
        if self.tipo not in self.TIPOS_VALIDOS:
            print(f"\n> Error: Tipo '{self.tipo}' no válido. Tipos permitidos: {', '.join(self.TIPOS_VALIDOS)}")
            return False
        return True
    
    
    def es_preventivo(self) -> bool:
        return self.tipo == self.TIPO_PREVENTIVO
    
    
    def validar_costo(self) -> bool:
        if self.costo < 0:
            print("\n> Error: El costo no puede ser negativo")
            return False
        return True
    
    
    def guardar(self) -> bool:
        if not (self.validar_fechas() and self.validar_estado() and 
                self.validar_tipo() and self.validar_costo()):
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
                print(f"  - Tipo: {self.tipo}")
                print(f"  - Vehículo ID: {self.id_vehiculo}")
                print(f"  - Estado: {self.estado}")
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
    
    
    def iniciar_mantenimiento(self) -> bool:
        """Inicia el mantenimiento cambiando su estado a 'en_proceso'"""
        if self.id_mantenimiento is None:
            print("\n> Error: El mantenimiento no ha sido guardado en la base de datos")
            return False
        
        if self.estado != self.ESTADO_PENDIENTE:
            print(f"\n> Error: Solo se puede iniciar un mantenimiento pendiente (estado actual: {self.estado})")
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE mantenimientos SET estado = ? WHERE id_mantenimiento = ?
            """, (self.ESTADO_EN_PROCESO, self.id_mantenimiento))
            
            db.commit()
            self.estado = self.ESTADO_EN_PROCESO
            print(f"\n> Mantenimiento #{self.id_mantenimiento} iniciado")
            return True
            
        except Exception as e:
            print(f"\n> Error al iniciar mantenimiento: {e}")
            db.rollback()
            return False
    
    
    def finalizar_mantenimiento(self, fecha_fin: date, costo_final: float = None) -> bool:
        """Finaliza el mantenimiento registrando fecha de fin y costo final."""
        if self.id_mantenimiento is None:
            print("\n> Error: El mantenimiento no ha sido guardado en la base de datos")
            return False
        
        if self.estado != self.ESTADO_EN_PROCESO:
            print(f"\n> Error: Solo se puede finalizar un mantenimiento en proceso (estado actual: {self.estado})")
            return False
        
        if fecha_fin < self.fecha_inicio:
            print("\n> Error: La fecha de fin no puede ser anterior a la fecha de inicio")
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
            
            db.commit()
            self.estado = self.ESTADO_COMPLETADO
            print(f"\n> Mantenimiento #{self.id_mantenimiento} finalizado")
            print(f"  - Fecha fin: {fecha_fin}")
            print(f"  - Costo final: ${self.costo}")
            return True
            
        except Exception as e:
            print(f"\n> Error al finalizar mantenimiento: {e}")
            db.rollback()
            return False
    
    
    def cancelar_mantenimiento(self) -> bool:
        """Cancela el mantenimiento."""
        if self.id_mantenimiento is None:
            print("\n> Error: El mantenimiento no ha sido guardado en la base de datos")
            return False
        
        if self.estado in [self.ESTADO_COMPLETADO, self.ESTADO_CANCELADO]:
            print(f"\n> Error: No se puede cancelar un mantenimiento {self.estado}")
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
    
    
    def calcular_duracion(self) -> Optional[int]:
        if not self.fecha_fin:
            return None
        
        return (self.fecha_fin - self.fecha_inicio).days
    
    
    @staticmethod
    def buscar_por_id(id_mantenimiento: int) -> Optional['Mantenimiento']:
        """Busca un mantenimiento por su ID."""
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
        """Lista todos los mantenimientos de un vehículo."""
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
    
    
    @staticmethod
    def listar_por_estado(estado: str) -> List['Mantenimiento']:
        """Lista todos los mantenimientos con un estado específico."""
        if estado not in Mantenimiento.ESTADOS_VALIDOS:
            print(f"\n> Error: Estado '{estado}' no válido")
            return []
            
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM mantenimientos 
            WHERE estado = ? 
            ORDER BY fecha_inicio DESC
        """, (estado,))
        
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
    def listar_pendientes() -> List['Mantenimiento']:
        """Lista todos los mantenimientos pendientes."""
        return Mantenimiento.listar_por_estado(Mantenimiento.ESTADO_PENDIENTE)
    
    
    @staticmethod
    def listar_en_proceso() -> List['Mantenimiento']:
        """Lista todos los mantenimientos en proceso."""
        return Mantenimiento.listar_por_estado(Mantenimiento.ESTADO_EN_PROCESO)
    
    
    def __str__(self) -> str:
        duracion = self.calcular_duracion()
        duracion_str = f" - {duracion} días" if duracion else ""
        return f"Mantenimiento #{self.id_mantenimiento} - {self.tipo} - {self.estado}{duracion_str}"
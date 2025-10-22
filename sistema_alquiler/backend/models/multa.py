from datetime import date
from typing import Optional, List
from backend.database.db_config import db


class Multa:
    """ Clase que representa una multa asociada a un alquiler """
    
    # Estados posibles de una multa
    ESTADO_PENDIENTE = "pendiente"
    ESTADO_PAGADA = "pagada"
    ESTADO_CANCELADA = "cancelada"
    
    ESTADOS_VALIDOS = [ESTADO_PENDIENTE, ESTADO_PAGADA, ESTADO_CANCELADA]
    
    def __init__(self, motivo: str, monto: float, id_alquiler: int,
                 descripcion: str = "", fecha: Optional[date] = None,
                 estado: str = ESTADO_PENDIENTE, id_multa: Optional[int] = None):

        self.id_multa = id_multa
        self.motivo = motivo
        self.monto = monto
        self.fecha = fecha or date.today()
        self.estado = estado
        self.descripcion = descripcion
        self.id_alquiler = id_alquiler
    
    
    def validar_monto(self) -> bool:
        if self.monto <= 0:
            print(f"\n> Error: El monto de la multa debe ser mayor a 0")
            return False
        return True
    
    
    def validar_estado(self) -> bool:
        if self.estado not in self.ESTADOS_VALIDOS:
            print(f"\n> Error: Estado '{self.estado}' no válido. Estados permitidos: {', '.join(self.ESTADOS_VALIDOS)}")
            return False
        return True
    
    
    def esta_pagada(self) -> bool:
        return self.estado == self.ESTADO_PAGADA
    
    
    def esta_cancelada(self) -> bool:
        return self.estado == self.ESTADO_CANCELADA
    
    
    def esta_pendiente(self) -> bool:
        return self.estado == self.ESTADO_PENDIENTE
    
    
    def guardar(self) -> bool:
        if not self.validar_monto() or not self.validar_estado():
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.id_multa is None:
                cursor.execute("""
                    INSERT INTO multas (motivo, monto, fecha, estado, descripcion, id_alquiler)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (self.motivo, self.monto, self.fecha, self.estado, 
                      self.descripcion, self.id_alquiler))
                
                self.id_multa = cursor.lastrowid
                db.commit()
                print(f"\n> Multa registrada con ID: {self.id_multa}")
                print(f"  - Motivo: {self.motivo}")
                print(f"  - Monto: ${self.monto}")
                print(f"  - Estado: {self.estado}")
                return True
            
            else:
                cursor.execute("""
                    UPDATE multas 
                    SET motivo=?, monto=?, fecha=?, estado=?, descripcion=?
                    WHERE id_multa=?
                """, (self.motivo, self.monto, self.fecha, self.estado, 
                      self.descripcion, self.id_multa))
                
                db.commit()
                print(f"\n> Multa actualizada")
                return True
                
        except Exception as e:
            print(f"\n> Error al guardar multa: {e}")
            db.rollback()
            return False
    
    
    def marcar_como_pagada(self) -> bool:
        """ Marca la multa como pagada.
        
        :return: True si se pudo marcar como pagada, False en caso contrario
        :rtype: bool
        """
        if self.id_multa is None:
            print("\n> Error: La multa no ha sido guardada en la base de datos")
            return False
        
        if self.estado == self.ESTADO_PAGADA:
            print(f"\n> La multa ya está marcada como pagada")
            return True
            
        if self.estado == self.ESTADO_CANCELADA:
            print(f"\n> Error: No se puede marcar como pagada una multa cancelada")
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE multas SET estado = ? WHERE id_multa = ?
            """, (self.ESTADO_PAGADA, self.id_multa))
            
            db.commit()
            self.estado = self.ESTADO_PAGADA
            print(f"\n> Multa #{self.id_multa} marcada como pagada")
            return True
            
        except Exception as e:
            print(f"\n> Error al marcar multa como pagada: {e}")
            db.rollback()
            return False
    
    
    def cancelar(self) -> bool:
        """
        Cancela la multa sin eliminarla de la base de datos.
        
        :return: True si se pudo cancelar, False en caso contrario
        :rtype: bool
        """
        if self.id_multa is None:
            print("\n> Error: La multa no ha sido guardada en la base de datos")
            return False
        
        if self.estado == self.ESTADO_CANCELADA:
            print(f"\n> La multa ya está cancelada")
            return True
            
        if self.estado == self.ESTADO_PAGADA:
            print(f"\n> Error: No se puede cancelar una multa ya pagada")
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE multas SET estado = ? WHERE id_multa = ?
            """, (self.ESTADO_CANCELADA, self.id_multa))
            
            db.commit()
            self.estado = self.ESTADO_CANCELADA
            print(f"\n> Multa #{self.id_multa} cancelada")
            return True
            
        except Exception as e:
            print(f"\n> Error al cancelar multa: {e}")
            db.rollback()
            return False
    
    
    @staticmethod
    def buscar_por_id(id_multa: int) -> Optional['Multa']:
        """ Busca una multa por su ID.
        
        :param id_multa: ID de la multa
        :type id_multa: int
        :return: Multa si se encuentra, None en caso contrario
        :rtype: Multa or None
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM multas WHERE id_multa = ?", (id_multa,))
        row = cursor.fetchone()
        
        if row:
            return Multa(
                id_multa=row['id_multa'],
                motivo=row['motivo'],
                monto=row['monto'],
                fecha=date.fromisoformat(row['fecha']) if row['fecha'] else date.today(),
                estado=row['estado'],
                descripcion=row['descripcion'],
                id_alquiler=row['id_alquiler']
            )
        return None
    
    
    @staticmethod
    def listar_por_estado(estado: str) -> List['Multa']:
        """ Lista todas las multas con un estado específico.
        
        :param estado: Estado de las multas a listar
        :type estado: str
        :return: Lista de multas con el estado especificado
        :rtype: list
        """
        if estado not in Multa.ESTADOS_VALIDOS:
            print(f"\n> Error: Estado '{estado}' no válido")
            return []
            
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM multas 
            WHERE estado = ? 
            ORDER BY fecha DESC
        """, (estado,))
        
        rows = cursor.fetchall()
        
        return [
            Multa(
                id_multa=row['id_multa'],
                motivo=row['motivo'],
                monto=row['monto'],
                fecha=date.fromisoformat(row['fecha']) if row['fecha'] else date.today(),
                estado=row['estado'],
                descripcion=row['descripcion'],
                id_alquiler=row['id_alquiler']
            )
            for row in rows
        ]
    
    
    @staticmethod
    def calcular_total_por_estado(estado: str, id_alquiler: Optional[int] = None) -> float:
        """ Calcula el total de multas por estado.
        Si se proporciona id_alquiler, calcula solo para ese alquiler.
        
        :param estado: Estado de las multas a calcular
        :type estado: str
        :param id_alquiler: ID del alquiler (opcional)
        :type id_alquiler: int, optional
        :return: Monto total de multas con el estado especificado
        :rtype: float
        """
        if estado not in Multa.ESTADOS_VALIDOS:
            print(f"\n> Error: Estado '{estado}' no válido")
            return 0.0
            
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if id_alquiler:
            cursor.execute("""
                SELECT SUM(monto) as total FROM multas 
                WHERE estado = ? AND id_alquiler = ?
            """, (estado, id_alquiler))
        else:
            cursor.execute("""
                SELECT SUM(monto) as total FROM multas 
                WHERE estado = ?
            """, (estado,))
        
        result = cursor.fetchone()
        total = result['total'] if result['total'] else 0.0
        
        return round(total, 2)
    
    
    @staticmethod
    def calcular_total_pendiente(id_alquiler: Optional[int] = None) -> float:
        """ Calcula el total de multas pendientes.
        Si se proporciona id_alquiler, calcula solo para ese alquiler.
        
        :param id_alquiler: ID del alquiler (opcional)
        :type id_alquiler: int, optional
        :return: Monto total de multas pendientes
        :rtype: float
        """
        return Multa.calcular_total_por_estado(Multa.ESTADO_PENDIENTE, id_alquiler)
    
    
    def __str__(self) -> str:
        return f"Multa #{self.id_multa} - {self.motivo} - ${self.monto} - {self.estado.upper()}"
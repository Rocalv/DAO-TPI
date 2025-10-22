from datetime import date, datetime
from typing import Optional, List
from backend.database import db


class Alquiler:
    def __init__(self, fecha_inicio: date, fecha_fin: date, fecha_entrega_real: date, costo_total: float,
                 id_cliente: int, id_vehiculo: int, id_empleado: int,
                 estado: str = "pendiente",  observaciones: str = ""):
        
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.fecha_entrega_real = fecha_entrega_real
        self.costo_total = costo_total
        self.id_cliente = id_cliente
        self.id_empleado = id_empleado
        self.id_vehiculo = id_vehiculo
        self.estado = estado
        self.observaciones = observaciones
    
    
    def registrar_alquiler(self) -> bool:
        pass
    
    
    def calcular_costo(self) -> float:
        pass
    
    
    def finalizar_alquiler(self) -> bool:
        pass
    
    
    def extender_alquiler(self, nuevo_fin: date) -> bool:
        #! no seeee si este paja
        pass
    
    
    def verificar_disponibilidad_fecha(self, fecha_inicio: date, fecha_fin: date) -> bool:
        pass
    
    
    def calcular_multa(self) -> float:
        #! Clase multa por aca .......
        pass
    
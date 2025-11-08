# backend/models/estado_vehiculo.py
from abc import ABC, abstractmethod
from typing import Optional, List

class EstadoVehiculo(ABC):
    """ Interfaz base para los estados de un vehículo (Patrón STATE) """
    
    @abstractmethod
    def puede_alquilarse(self) -> bool:
        """ Verifica si el vehículo puede ser alquilado en este estado """
        pass
    
    @abstractmethod
    def puede_ir_a_mantenimiento(self) -> bool:
        """ Verifica si el vehículo puede ir a mantenimiento en este estado """
        pass
    
    @abstractmethod
    def nombre_estado(self) -> str:
        """ Retorna el nombre del estado (como se guarda en la BD) """
        pass
    
    def __str__(self) -> str:
        return self.nombre_estado()

class EstadoDisponible(EstadoVehiculo):
    def puede_alquilarse(self) -> bool: return True
    def puede_ir_a_mantenimiento(self) -> bool: return True
    def nombre_estado(self) -> str: return "disponible"

class EstadoAlquilado(EstadoVehiculo):
    def puede_alquilarse(self) -> bool: return False
    def puede_ir_a_mantenimiento(self) -> bool: return False
    def nombre_estado(self) -> str: return "alquilado"

class EstadoEnMantenimiento(EstadoVehiculo):
    def puede_alquilarse(self) -> bool: return False
    def puede_ir_a_mantenimiento(self) -> bool: return False
    def nombre_estado(self) -> str: return "mantenimiento"

class EstadoBaja(EstadoVehiculo):
    def puede_alquilarse(self) -> bool: return False
    def puede_ir_a_mantenimiento(self) -> bool: return False
    def nombre_estado(self) -> str: return "Baja"

class EstadoReservado(EstadoVehiculo):
    def puede_alquilarse(self) -> bool: return False
    def puede_ir_a_mantenimiento(self) -> bool: return False
    def nombre_estado(self) -> str: return "reservado"


class FabricaEstados:
    """ Fábrica para crear instancias de estados de vehículos """
    
    _estados = {
        "disponible": EstadoDisponible(),
        "alquilado": EstadoAlquilado(),
        "mantenimiento": EstadoEnMantenimiento(),
        "Baja": EstadoBaja(),
        "reservado": EstadoReservado()
    }
    
    # IDs de la BD
    _estados_map_bd = {
        "disponible": 1,
        "alquilado": 2,
        "mantenimiento": 3,
        "Baja": 4,
        "reservado": 5
    }

    @classmethod
    def obtener_estado_por_nombre(cls, nombre_estado: str) -> EstadoVehiculo:
        """ Obtiene una instancia del estado solicitado por su nombre (string) """
        return cls._estados.get(nombre_estado, EstadoBaja())
    
    @classmethod
    def obtener_estado_por_id(cls, id_estado: int) -> EstadoVehiculo:
        """ Obtiene una instancia del estado solicitado por su ID de BD """
        for nombre, id_est in cls._estados_map_bd.items():
            if id_est == id_estado:
                return cls._estados.get(nombre, EstadoBaja())
        return EstadoBaja()

    @classmethod
    def obtener_id_estado(cls, nombre_estado: str) -> Optional[int]:
        """ Obtiene el ID de un estado por su nombre """
        return cls._estados_map_bd.get(nombre_estado)

    @classmethod
    def listar_estados_para_ui(cls) -> dict:
        """ Lista todos los estados para mostrar en la interfaz (Combobox)."""
        return {n: i for n, i in cls._estados_map_bd.items() if n != "Baja"}
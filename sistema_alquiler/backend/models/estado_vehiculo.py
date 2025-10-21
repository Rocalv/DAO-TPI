from abc import ABC, abstractmethod
from typing import Optional


class EstadoVehiculo(ABC):
    """ Interfaz base para los estados de un vehículo (Patrón STATE) """
    
    @abstractmethod
    def puede_alquilarse(self) -> bool:
        """ Verifica si el vehículo puede ser alquilado en este estado
        
        :return: True si puede alquilarse, False en caso contrario
        :rtype: bool
        """
        pass
    
    
    @abstractmethod
    def puede_ir_a_mantenimiento(self) -> bool:
        """ Verifica si el vehículo puede ir a mantenimiento en este estado
        
        :return: True si puede ir a mantenimiento, False en caso contrario
        :rtype: bool
        """
        pass
    
    
    @abstractmethod
    def nombre_estado(self) -> str:
        """ Retorna el nombre del estado
        
        :return: Nombre del estado
        :rtype: str
        """
        pass
    
    def __str__(self) -> str:
        """Representación en string del estado"""
        return self.nombre_estado()


class EstadoDisponible(EstadoVehiculo):
    """ Estado: Vehículo disponible para alquiler """
    
    def puede_alquilarse(self) -> bool:
        return True    
    
    def puede_ir_a_mantenimiento(self) -> bool:
        return True
    
    def nombre_estado(self) -> str:
        return "disponible"


class EstadoAlquilado(EstadoVehiculo):
    """ Estado: Vehículo actualmente alquilado """
    
    def puede_alquilarse(self) -> bool:
        return False
    
    def puede_ir_a_mantenimiento(self) -> bool:
        return False
    
    def nombre_estado(self) -> str:
        return "alquilado"


class EstadoEnMantenimiento(EstadoVehiculo):
    """ Estado: Vehículo en mantenimiento """
    
    def puede_alquilarse(self) -> bool:
        return False
    
    def puede_ir_a_mantenimiento(self) -> bool:
        return False
    
    def nombre_estado(self) -> str:
        return "mantenimiento"


class EstadoFueraServicio(EstadoVehiculo):
    """ Estado: Vehículo fuera de servicio """
    
    def puede_alquilarse(self) -> bool:
        return False
    
    def puede_ir_a_mantenimiento(self) -> bool:
        return True
    
    def nombre_estado(self) -> str:
        return "fuera_servicio"
    

class FabricaEstados:
    """ Fábrica para crear instancias de estados de vehículos """
    _estados = {
        "disponible": EstadoDisponible(),
        "alquilado": EstadoAlquilado(),
        "mantenimiento": EstadoEnMantenimiento(),
        "fuera_servicio": EstadoFueraServicio()
    }
    
    
    @classmethod
    def obtener_estado(cls, nombre_estado: str) -> Optional[EstadoVehiculo]:
        """ Obtiene una instancia del estado solicitado
        
        :param nombre_estado: Nombre del estado a obtener
        :type nombre_estado: str
        :return: Instancia del estado o None si no existe
        :rtype: Optional[EstadoVehiculo]
        """
        return cls._estados.get(nombre_estado)
    
    
    @classmethod
    def listar_estados(cls) -> list:
        """ Lista todos los estados disponibles
        
        :return: Lista de nombres de estados
        :rtype: list
        """
        return list(cls._estados.keys())
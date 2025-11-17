from abc import ABC, abstractmethod

class EstadoVehiculo(ABC):
    @abstractmethod
    def nombre_estado(self) -> str:
        pass
    
    @abstractmethod
    def alquilar(self, vehiculo):
        pass
    @abstractmethod
    def disponibilizar(self, vehiculo):
        pass
    @abstractmethod
    def fuera_servicio(self, vehiculo):
        pass
    @abstractmethod
    def mantenimiento(self, vehiculo):
        pass
    @abstractmethod
    def para_mantenimiento(self, vehiculo):
        pass
    @abstractmethod
    def reservado(self, vehiculo):
        pass
    
    
    @abstractmethod
    def cambiar_estado(self, vehiculo):
        pass

    @abstractmethod
    def obtener_id(self) -> int:
        """Se obtiene el id del estado a partir del nombre."""
        pass
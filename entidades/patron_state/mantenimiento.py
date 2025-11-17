from entidades.patron_state.estado_vehiculo import EstadoVehiculo
from persistencia.Repository.repository_estados import RepositoryEstados
class Mantenimiento(EstadoVehiculo):
    def nombre_estado(self) -> str:
        return "Mantenimiento"

    def alquilar(self, vehiculo):
        raise ValueError("Un vehículo en mantenimiento no puede ir a alquilado")

    def disponibilizar(self, vehiculo):
        from entidades.patron_state.disponible import Disponible
        vehiculo.estado = Disponible()
        id_estado = RepositoryEstados.obtener_id("Disponible")
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def fuera_servicio(self, vehiculo):
        from entidades.patron_state.fuera_servicio import FueraServicio
        vehiculo.estado = FueraServicio()
        id_estado = RepositoryEstados.obtener_id("FueraServicio")
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def mantenimiento(self, vehiculo):
        raise ValueError("El vehiculo ya se encuentra en mantenimiento")
    
    def para_mantenimiento(self, vehiculo):
        raise ValueError("El vehiculo en mantenimiento no puede ir a para mantenimiento")
    
    def reservado(self, vehiculo):
        raise ValueError("El vehiculo en mantenimiento no puede ir a para reservado")

    def cambiar_estado(self, vehiculo):
        """Cambia el estado del vehículo en la BD al estado especificado."""
        id_estado = self.obtener_id()
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def obtener_id(self) -> int:
        """Obtiene el ID del estado especificado."""
        return RepositoryEstados.obtener_id(self.nombre_estado())
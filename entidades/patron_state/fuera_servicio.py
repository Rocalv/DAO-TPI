from entidades.patron_state.estado_vehiculo import EstadoVehiculo
from persistencia.Repository.repository_estados import RepositoryEstados

class FueraServicio(EstadoVehiculo):
    
    def nombre_estado(self) -> str: # CORRECCIÓN: Implementación correcta del abstracto
        return "FueraServicio"

    def alquilar(self, vehiculo):
        raise ValueError("Un vehículo fuera de servicio no puede alquilarse")

    def disponibilizar(self, vehiculo):   
        from entidades.patron_state.disponible import Disponible
        vehiculo.estado = Disponible()
        id_estado = RepositoryEstados.obtener_id("Disponible")
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def fuera_servicio(self, vehiculo):
        raise ValueError("El vehículo ya se encuentra fuera de servicio")

    def mantenimiento(self, vehiculo):
        raise ValueError("Un vehículo fuera de servicio no puede ir a mantenimiento")
    
    def para_mantenimiento(self, vehiculo):
        raise ValueError("El vehiculo en fuera de servicio no puede ir a para mantenimiento")

    def cambiar_estado(self, vehiculo): # CORRECCIÓN: Implementación del abstracto
        """Cambia el estado del vehículo en la BD al estado 'FueraServicio'."""
        id_estado = self.obtener_id()
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def obtener_id(self) -> int: # CORRECCIÓN: Implementación del abstracto
        """Obtiene el id del estado 'FueraServicio'."""
        return RepositoryEstados.obtener_id(self.nombre_estado())
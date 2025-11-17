from entidades.patron_state.estado_vehiculo import EstadoVehiculo
from persistencia.Repository.repository_estados import RepositoryEstados

class FueraServicio(EstadoVehiculo):
    
    def nombre_estado(self) -> str: # CORRECCIÓN: Implementación correcta del abstracto
        return "FueraServicio"

    def alquilar(self, vehiculo):
        raise ValueError("Un vehículo fuera de servicio no puede alquilarse")

    def disponibilizar(self, vehiculo):   
        raise ValueError("Un vehículo fuera de servicio no puede disponible")

    def fuera_servicio(self, vehiculo):
        raise ValueError("El vehículo ya se encuentra fuera de servicio")

    def mantenimiento(self, vehiculo):
        raise ValueError("Un vehículo fuera de servicio no puede ir a mantenimiento")
    
    def reserva(self, vehiculo):
        raise ValueError("Un vehículo fuera de servicio no puede ir a reserva")
    
    def para_mantenimiento(self, vehiculo):
        raise ValueError("El vehiculo en fuera de servicio no puede ir a para mantenimiento")

    def cambiar_estado(self, vehiculo):
        """Cambia el estado del vehículo en la BD al estado correspondiente."""
        id_estado = self.obtener_id()
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def obtener_id(self) -> int:
        """Obtiene el id del estado correspondiente."""
        return RepositoryEstados.obtener_id(self.nombre_estado())
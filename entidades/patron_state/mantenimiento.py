from entidades.patron_state.estado_vehiculo import EstadoVehiculo
from persistencia.Repository.repository_estados import RepositoryEstados
class Mantenimiento(EstadoVehiculo):
    def nombre_estado(self) -> str: # CORRECCIÓN: Implementación correcta del abstracto
        return "Mantenimiento"

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

    def alquilar(self, vehiculo):
        raise ValueError("Un vehículo en mantenimiento no puede ir a alquilado")

    def cambiar_estado(self, vehiculo): # CORRECCIÓN: Implementación del abstracto
        """Cambia el estado del vehículo en la BD al estado 'Mantenimiento'."""
        id_estado = self.obtener_id()
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def obtener_id(self) -> int: # CORRECCIÓN: Implementación del abstracto
        """Obtiene el ID del estado 'Mantenimiento'."""
        return RepositoryEstados.obtener_id(self.nombre_estado())
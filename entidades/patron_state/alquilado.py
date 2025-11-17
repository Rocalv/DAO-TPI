from entidades.patron_state.estado_vehiculo import EstadoVehiculo
from entidades.patron_state.disponible import Disponible
from entidades.patron_state.fuera_servicio import FueraServicio

from persistencia.Repository import repository_estados as RepositoryEstados

class Alquilado(EstadoVehiculo):

    def nombre_estado(self) -> str: # CORRECCIÓN: Implementa nombre_estado
        return "Alquilado"

    def disponibilizar(self, vehiculo):
        vehiculo.estado = Disponible()
        id_estado = RepositoryEstados.obtener_id("Disponible")
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def fuera_servicio(self, vehiculo):
        vehiculo.estado = FueraServicio()
        id_estado = RepositoryEstados.obtener_id("FueraServicio")
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def mantenimiento(self, vehiculo):
        raise ValueError("Un vehículo alquilado no puede ir a mantenimiento")

    def alquilar(self, vehiculo):
        raise ValueError("El vehículo ya está alquilado")

    def cambiar_estado(self, vehiculo):
        """Implementa el método abstracto: cambia el estado del vehículo en la BD al estado 'Alquilado'."""
        id_estado = self.obtener_id()
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)
        
    def obtener_id(self) -> int:
        """Implementa el método abstracto: Obtiene el ID del estado 'Alquilado'."""
        return RepositoryEstados.obtener_id(self.nombre_estado())
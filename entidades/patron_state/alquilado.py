from entidades.patron_state.estado_vehiculo import EstadoVehiculo
from entidades.patron_state.disponible import Disponible
from entidades.patron_state.fuera_servicio import FueraServicio

from persistencia.Repository import repository_estados as RepositoryEstados

class Alquilado(EstadoVehiculo):

    def nombre(self) -> str:
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

from entidades.patron_state.estado_vehiculo import EstadoVehiculo

from persistencia.Repository import repository_estados as RepositoryEstados

class FueraServicio(EstadoVehiculo):
    
    def nombre(self) -> str:
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

    def cambiar_estado(self, vehiculo, nuevo_estado: str):
        id_estado = RepositoryEstados.obtener_id(nuevo_estado)
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def obtener_id(self) -> int:
        return RepositoryEstados.obtener_id(self.nombre())
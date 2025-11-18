from entidades.patron_state.estado_vehiculo import EstadoVehiculo
from persistencia.Repository.repository_estados import RepositoryEstados

class Reservado(EstadoVehiculo):
    def nombre_estado(self) -> str:
        return "Reservado"

    def alquilar(self, vehiculo):
        raise ValueError("El vehículo reservado no puede pasar a alquilado")

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
        raise ValueError("Un vehículo reservado no puede ir a mantenimiento")

    def reservado(self, vehiculo):
        raise ValueError("El vehiculo ya se encuentra reservado")

    def cambiar_estado(self, vehiculo):
        """Implementa el método abstracto: cambia el estado del vehículo en la BD al estado correspondiente."""
        id_estado = self.obtener_id()
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)
        
    def obtener_id(self) -> int:
        """Implementa el método abstracto: Obtiene el ID del estado correspodiente."""
        return RepositoryEstados.obtener_id(self.nombre_estado())
from entidades.patron_state.estado_vehiculo import EstadoVehiculo
from persistencia.Repository import repository_estados as RepositoryEstados
class Disponible(EstadoVehiculo):

    def nombre_estado(self) -> str:
        return "Disponible"

    def _actualizar_estado_bd(self, vehiculo, nuevo_estado: str): 
        """Método auxiliar para la persistencia de la transición."""
        id_estado = RepositoryEstados.obtener_id(nuevo_estado)
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def alquilar(self, vehiculo):
        from entidades.patron_state.alquilado import Alquilado
        vehiculo.estado = Alquilado()
        self._actualizar_estado_bd(vehiculo, "Alquilado")

    def disponibilizar(self, vehiculo):
        pass

    def fuera_servicio(self, vehiculo):    
        from entidades.patron_state.fuera_servicio import FueraServicio
        vehiculo.estado = FueraServicio()
        self._actualizar_estado_bd(vehiculo, "FueraServicio")

    def mantenimiento(self, vehiculo):
        from entidades.patron_state.mantenimiento import Mantenimiento  
        vehiculo.estado = Mantenimiento()
        self._actualizar_estado_bd(vehiculo, "Mantenimiento")

    def cambiar_estado(self, vehiculo):
        """Implementa el método abstracto: cambia el estado del vehículo en la BD al estado 'Disponible'."""
        id_estado = self.obtener_id()
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def obtener_id(self) -> int: # CORRECCIÓN: Implementación del abstracto
        """Obtiene el ID del estado 'Disponible'."""
        return RepositoryEstados.obtener_id(self.nombre_estado())
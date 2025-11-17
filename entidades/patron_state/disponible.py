from entidades.patron_state.estado_vehiculo import EstadoVehiculo

from persistencia.Repository import repository_estados as RepositoryEstados
class Disponible(EstadoVehiculo):

    def nombre(self) -> str:
        return "Disponible"

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

    def cambiar_estado(self, vehiculo, nuevo_estado: str):
        id_estado = RepositoryEstados.obtener_id(nuevo_estado)
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def obtener_id(self) -> int:
        return RepositoryEstados.obtener_id(self.nombre())

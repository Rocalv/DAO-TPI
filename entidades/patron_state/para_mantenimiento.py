from entidades.patron_state.estado_vehiculo import EstadoVehiculo
from persistencia.Repository.repository_estados import RepositoryEstados
class ParaMantenimiento(EstadoVehiculo):
    def ParaMantenimiento(self) -> str:
        return "Para"

    def disponibilizar(self, vehiculo):
        raise ValueError("Un vehículo en para mantenimiento no puede ir a disponibilizar")

    def fuera_servicio(self, vehiculo):
        raise ValueError("Un vehículo en para mantenimiento no puede ir a fuera de servicio")

    def mantenimiento(self, vehiculo):
        from entidades.patron_state.mantenimiento import Mantenimiento  
        vehiculo.estado = Mantenimiento()
        self._actualizar_estado_bd(vehiculo, "Mantenimiento")

    def alquilar(self, vehiculo):
        raise ValueError("Un vehículo en para mantenimiento no puede ir a alquilado")
    
    def para_mantenimiento(self, vehiculo):
        raise ValueError("El vehiculo ya se encuentra en para mantenimiento")
    
    def reservado(self, vehiculo):
        raise ValueError("Un vehículo en para mantenimiento no puede ir a reservadi")

    def cambiar_estado(self, vehiculo):
        """Cambia el estado del vehículo en la BD al estado correspondiente."""
        id_estado = self.obtener_id()
        RepositoryEstados.cambiar_estado(id_estado, vehiculo.id_vehiculo)

    def obtener_id(self) -> int:
        """Obtiene el ID del estado correspondiente."""
        return RepositoryEstados.obtener_id(self.nombre_estado())
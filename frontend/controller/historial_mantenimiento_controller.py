from entidades.mantenimiento import Mantenimiento
from frontend.boundary.historial_mantenimiento_view import HistorialMantenimientoView

class HistorialMantenimientoController:
    def __init__(self, parent):
        """Inicializa la vista y carga los mantenimientos finalizados."""
        self.modelo = Mantenimiento
        self.view = HistorialMantenimientoView(
            parent,
            on_recargar=self.cargar_datos
        )

    def cargar_datos(self):
        """Carga la lista de mantenimientos finalizados en la vista."""
        try:
            mantenimientos = self.modelo.listar_finalizados()
            self.view.actualizar_tabla(mantenimientos)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar historial: {e}", error=True)

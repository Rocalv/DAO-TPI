# frontend/controllers/historial_mantenimiento_controller.py
from sistema_alquiler.backend.models.mantenimiento import Mantenimiento

class HistorialMantenimientoController:
    
    def __init__(self, view):
        self.view = view
        self.modelo = Mantenimiento
        
    def cargar_datos(self):
        """Carga la lista de mantenimientos finalizados."""
        try:
            mantenimientos = self.modelo.listar_finalizados()
            self.view.actualizar_tabla(mantenimientos)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar historial: {e}", error=True)
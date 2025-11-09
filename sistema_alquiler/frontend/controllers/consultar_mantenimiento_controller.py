# frontend/controllers/consultar_mantenimiento_controller.py
from tkinter import simpledialog
from datetime import date
from sistema_alquiler.backend.models.mantenimiento import Mantenimiento

class ConsultarMantenimientoController:
    
    def __init__(self, view):
        self.view = view
        self.modelo = Mantenimiento
        
    def cargar_datos(self):
        """Carga la lista de mantenimientos pendientes."""
        try:
            # Usamos el método que ya creamos en el modelo
            mantenimientos = self.modelo.listar_pendientes()
            self.view.actualizar_tabla(mantenimientos)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar mantenimientos: {e}", error=True)

    def finalizar_mantenimiento(self):
        """Maneja la acción del botón Finalizar."""
        id_mantenimiento = self.view.obtener_id_seleccionado()
        if not id_mantenimiento:
            self.view.mostrar_mensaje("Aviso", "Seleccione un mantenimiento de la tabla para finalizar.", error=True)
            return

        # 1. Pedir confirmación y Costo Final
        # Usamos un simpledialog para pedir el dato rápido sin crear otro formulario
        costo_final_str = simpledialog.askstring("Finalizar Mantenimiento", "Ingrese el COSTO FINAL del servicio:", parent=self.view)
        
        if costo_final_str is None: return # Usuario canceló
        
        try:
            costo_final = float(costo_final_str)
        except ValueError:
            self.view.mostrar_mensaje("Error", "El costo debe ser un número válido.", error=True)
            return

        if self.view.mostrar_mensaje("Confirmar", f"¿Finalizar este mantenimiento con costo ${costo_final:.2f}?\nEl vehículo volverá a estar 'disponible'.", confirm=True):
            try:
                # 2. Llamar a la transacción en el modelo
                fecha_hoy = date.today().isoformat()
                exito = self.modelo.finalizar_mantenimiento_transaccion(
                    id_mantenimiento=id_mantenimiento,
                    fecha_fin=fecha_hoy,
                    costo=costo_final
                )
                
                if exito:
                    self.view.mostrar_mensaje("Éxito", "Mantenimiento finalizado. Vehículo disponible.")
                    # 3. Actualizar la tabla (Requisito 3)
                    self.cargar_datos()
                else:
                    self.view.mostrar_mensaje("Error", "No se pudo finalizar el mantenimiento.", error=True)
                    
            except Exception as e:
                 self.view.mostrar_mensaje("Error", f"Error de base de datos: {e}", error=True)
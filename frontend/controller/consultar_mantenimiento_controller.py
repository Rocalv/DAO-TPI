from tkinter import simpledialog
from datetime import date
from entidades.mantenimiento import Mantenimiento
from frontend.boundary.consultar_mantenimiento_view import ConsultarMantenimientoView

class ConsultarMantenimientoController:
    def __init__(self, parent):
        """Inicializa la vista y conecta callbacks."""
        self.modelo = Mantenimiento
        self.view = ConsultarMantenimientoView(
            parent,
            on_finalizar=self.finalizar_mantenimiento
        )

    def inicializar_vista(self):
        """Carga la tabla con los mantenimientos pendientes al iniciar."""
        self.cargar_datos()

    def cargar_datos(self):
        """Carga la lista de mantenimientos pendientes en la vista."""
        try:
            mantenimientos = self.modelo.listar_pendientes()
            self.view.actualizar_tabla(mantenimientos)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar mantenimientos: {e}", error=True)

    def finalizar_mantenimiento(self):
        """Maneja la acción de finalizar un mantenimiento."""
        id_mantenimiento = self.view.obtener_id_seleccionado()
        if not id_mantenimiento:
            self.view.mostrar_mensaje(
                "Aviso",
                "Seleccione un mantenimiento de la tabla para finalizar.",
                error=True
            )
            return

        costo_str = simpledialog.askstring(
            "Finalizar Mantenimiento",
            "Ingrese el COSTO FINAL del servicio:",
            parent=self.view
        )
        if costo_str is None:
            return

        try:
            costo = float(costo_str)
        except ValueError:
            self.view.mostrar_mensaje("Error", "El costo debe ser un número válido.", error=True)
            return

        if self.view.mostrar_mensaje(
            "Confirmar",
            f"¿Finalizar este mantenimiento con costo ${costo:.2f}?\nEl vehículo volverá a estar 'disponible'.",
            confirm=True
        ):
            try:
                exito = self.modelo.finalizar_mantenimiento_transaccion(
                    id_mantenimiento=id_mantenimiento,
                    fecha_fin=date.today().isoformat(),
                    costo=costo
                )
                if exito:
                    self.view.mostrar_mensaje("Éxito", "Mantenimiento finalizado. Vehículo disponible.")
                    self.cargar_datos()
                else:
                    self.view.mostrar_mensaje("Error", "No se pudo finalizar el mantenimiento.", error=True)
            except Exception as e:
                self.view.mostrar_mensaje("Error", f"Error de base de datos: {e}", error=True)
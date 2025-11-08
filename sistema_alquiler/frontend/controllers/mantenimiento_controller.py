# frontend/controllers/mantenimiento_controller.py
from sistema_alquiler.backend.models.vehiculo import Vehiculo
from sistema_alquiler.backend.models.categoria import Categoria
from sistema_alquiler.backend.models.servicio import Servicio
from sistema_alquiler.backend.models.mantenimiento import Mantenimiento

class MantenimientoController:
    
    def __init__(self, view):
        """Inicializa el controlador para registrar mantenimiento."""
        self.view = view
        self.modelo_vehiculo = Vehiculo
        self.modelo_categoria = Categoria
        self.modelo_servicio = Servicio
        self.modelo_mantenimiento = Mantenimiento
        
    def inicializar_vista(self):
        """Carga los comboboxes iniciales."""
        self.cargar_categorias_filtro()
        self.cargar_servicios_form()
        # Limpia la tabla al inicio
        self.view.actualizar_tabla_vehiculos([])

    def cargar_categorias_filtro(self):
        """Carga el combobox de categorías para el filtro."""
        try:
            categorias = self.modelo_categoria.obtener_todas()
            if categorias:
                self.view.set_categorias_combobox(categorias)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar categorías: {e}", error=True)

    def cargar_servicios_form(self):
        """Carga el combobox de servicios para el formulario."""
        try:
            servicios = self.modelo_servicio.obtener_todos()
            if servicios:
                self.view.set_servicios_combobox(servicios)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar servicios: {e}", error=True)

    def buscar_vehiculos(self):
        """Filtra y muestra vehículos que pueden ir a mantenimiento."""
        filtros = self.view.obtener_datos_filtro()
        
        try:
            # Usamos el método que filtra vehículos 'disponibles'
            vehiculos = self.modelo_vehiculo.buscar_para_mantenimiento(
                patente=filtros['patente'],
                id_categoria=filtros['id_categoria']
            )
            
            if not vehiculos:
                self.view.mostrar_mensaje("Aviso", "No se encontraron vehículos disponibles con esos filtros.")
            
            self.view.actualizar_tabla_vehiculos(vehiculos)
            
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al buscar vehículos: {e}", error=True)

    def seleccionar_vehiculo(self, event):
        """Al seleccionar un vehículo, rellena el formulario de mantenimiento."""
        vehiculo_seleccionado = self.view.obtener_vehiculo_seleccionado()
        if not vehiculo_seleccionado:
            return
            
        # Obtenemos el objeto Vehiculo completo
        vehiculo_obj = self.modelo_vehiculo.buscar_por_id(vehiculo_seleccionado['id'])
        if vehiculo_obj:
            self.view.rellenar_formulario_vehiculo(vehiculo_obj)

    def registrar_mantenimiento(self):
        """Registra el mantenimiento (transacción)."""
        datos = self.view.obtener_datos_formulario()
        
        # --- Validaciones ---
        if not datos['id_vehiculo']:
            self.view.mostrar_mensaje("Error", "Debe seleccionar un vehículo de la tabla.", error=True)
            return
        
        if not datos['id_servicio']:
            self.view.mostrar_mensaje("Error", "Debe seleccionar un servicio.", error=True)
            return

        if self.view.mostrar_mensaje("Confirmar", "¿Registrar este mantenimiento? El estado del vehículo cambiará a 'mantenimiento'.", confirm=True):
            try:
                exito = self.modelo_mantenimiento.crear_mantenimiento_transaccion(
                    id_vehiculo=datos['id_vehiculo'],
                    id_servicio=datos['id_servicio'],
                    kilometraje=datos['kilometraje'],
                    descripcion=datos['descripcion'],
                    proveedor=datos['proveedor']
                )
                
                if exito:
                    self.view.mostrar_mensaje("Éxito", "Mantenimiento registrado. El vehículo ya no está disponible.")
                    self.limpiar_todo()
                else:
                    self.view.mostrar_mensaje("Error", "No se pudo completar la transacción.", error=True)

            except Exception as e:
                self.view.mostrar_mensaje("Error", f"Error de aplicación: {e}", error=True)

    def limpiar_todo(self):
        """Limpia la vista completa."""
        self.view.limpiar_filtro()
        self.view.limpiar_formulario()
        self.view.actualizar_tabla_vehiculos([])
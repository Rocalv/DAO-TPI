from frontend.boundary.mantenimiento_view import RegistrarMantenimientoView
from entidades.vehiculo import Vehiculo
from entidades.categoria import Categoria
from entidades.servicio import Servicio
from entidades.mantenimiento import Mantenimiento
from entidades.empleado import Empleado

class MantenimientoController:
    
    def __init__(self, parent):
        """Inicializa el controlador usando el nuevo modelo unidireccional MVC."""
        
        self.view = RegistrarMantenimientoView(
            parent,
            on_buscar=self.buscar_vehiculos,
            on_select=self.seleccionar_vehiculo,
            on_registrar=self.registrar_mantenimiento
        )

        self.modelo_vehiculo = Vehiculo
        self.modelo_categoria = Categoria
        self.modelo_servicio = Servicio
        self.modelo_mantenimiento = Mantenimiento
        self.modelo_empleado = Empleado

    def inicializar_vista(self):
        """Carga datos iniciales en los combos."""
        self.cargar_categorias_filtro()
        self.cargar_servicios_form()
        self.cargar_mecanicos_form()
        self.view.actualizar_tabla_vehiculos([])
    
    def cargar_categorias_filtro(self):
        try:
            categorias = self.modelo_categoria.consultar()
            self.view.set_categorias_combobox(categorias)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"No se pudieron cargar categorías:\n{e}", error=True)

    def cargar_servicios_form(self):
        try:
            servicios = self.modelo_servicio.consultar()
            self.view.set_servicios_combobox(servicios)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"No se pudieron cargar servicios:\n{e}", error=True)

    def cargar_mecanicos_form(self):
        try:
            mecanicos = self.modelo_empleado.filtrar_por_cargo("Mecánico")
            self.view.set_mecanicos_combobox(mecanicos)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"No se pudieron cargar mecánicos:\n{e}", error=True)

    def buscar_vehiculos(self): #buscar vehiculos con estado en mantenimiento
        filtros = self.view.obtener_datos_filtro()
        try:
            vehiculos = self.modelo_vehiculo.filtrar_mantenimiento(
                patente=filtros["patente"],
                id_categoria=filtros["id_categoria"]
            )
            if not vehiculos:
                self.view.mostrar_mensaje("Aviso", "No se encontraron vehículos.")

            self.view.actualizar_tabla_vehiculos(vehiculos)

        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al buscar vehículos:\n{e}", error=True)

    def seleccionar_vehiculo(self):
        seleccionado = self.view.obtener_vehiculo_seleccionado()
        if not seleccionado:
            return

        vehiculo = self.modelo_vehiculo.buscar_por_id(seleccionado["id"])
        if vehiculo:
            self.view.rellenar_formulario_vehiculo(vehiculo)

    def registrar_mantenimiento(self):
        datos = self.view.obtener_datos_formulario()

        if not datos["id_vehiculo"]:
            self.view.mostrar_mensaje("Error", "Debe seleccionar un vehículo.", error=True)
            return
        if not datos["id_servicio"]:
            self.view.mostrar_mensaje("Error", "Seleccione un servicio.", error=True)
            return
        if not datos["id_empleado"]:
            self.view.mostrar_mensaje("Error", "Seleccione un mecánico.", error=True)
            return

        if not self.view.mostrar_mensaje(
            "Confirmación",
            "¿Registrar este mantenimiento?",
            confirm=True
        ):
            return

        try:
            vehiculo_obj = self.modelo_vehiculo.filtrar_por_id(datos["id_vehiculo"])
            servicio_data = self.modelo_servicio.filtrar_por_id(datos["id_servicio"])
            servicio_obj = Servicio(**servicio_data) if servicio_data else None
            empleado_obj = self.modelo_empleado.filtrar_por_id(datos["id_empleado"])
            
            if not all([vehiculo_obj, servicio_obj, empleado_obj]):
                raise Exception("Error al obtener entidades: Vehículo, Servicio o Empleado no encontrado.")

            exito = self.modelo_mantenimiento.crear_mantenimiento_transaccion(
                vehiculo=vehiculo_obj,
                servicio=servicio_obj,
                empleado=empleado_obj,
                kilometraje=datos["kilometraje"],
                descripcion=datos["descripcion"],
                proveedor=datos["proveedor"]
            )

            if exito:
                self.view.mostrar_mensaje("Éxito", "Mantenimiento registrado.")
                self.limpiar_todo()
            else:
                self.view.mostrar_mensaje("Error", "No se pudo completar la transacción.", error=True)

        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al registrar:\n{e}", error=True)

    def limpiar_todo(self):
        self.view.limpiar_filtro()
        self.view.limpiar_formulario()
        self.view.actualizar_tabla_vehiculos([])

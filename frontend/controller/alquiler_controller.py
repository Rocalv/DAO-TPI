from datetime import date, datetime
import os 
from PIL import Image, ImageTk

from frontend.boundary.alquiler_view import AlquilerView
from entidades.vehiculo import Vehiculo
from entidades.categoria import Categoria
from entidades.cliente import Cliente
from entidades.alquiler import Alquiler
from entidades.reserva import Reserva

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOTO_PREVIEW_SIZE = (220, 220)

class AlquilerController:
    
    def __init__(self, parent, app):
        """
        Inicializa el controlador y crea la vista.
        parent: contenedor donde irá la vista
        app: referencia a la aplicación principal (para actualizar otras vistas)
        """

        self.app = app  
        self.modelo_vehiculo = Vehiculo
        self.modelo_categoria = Categoria
        self.modelo_cliente = Cliente
        self.modelo_alquiler = Alquiler
        self.modelo_reserva = Reserva

        self.vehiculos_filtrados = []
        self.vehiculo_seleccionado = None
        self.costo_total_calculado = 0.0

        self.view = AlquilerView(
            parent,
            on_buscar_disponibles=self.buscar_disponibles,
            on_vehiculo_select=self.on_vehiculo_select,
            on_confirmar_transaccion=self.confirmar_transaccion
        )

    def inicializar_vista(self):
        """Carga combos y oculta el panel derecho."""
        self.cargar_categorias()
        self.cargar_clientes()
        self.view.ocultar_panel_detalle()

    def cargar_categorias(self):
        try:
            categorias = self.modelo_categoria.consultar()
            if categorias:
                self.view.set_categorias_combobox(categorias)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar categorías: {e}", error=True)

    def cargar_clientes(self):
        try:
            clientes = self.modelo_cliente.consultar(incluir_inactivos=False)
            if clientes:
                self.view.set_clientes_combobox(clientes)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar clientes: {e}", error=True)

    def buscar_disponibles(self):
        filtros = self.view.obtener_datos_filtro()
        try:
            fecha_inicio = datetime.strptime(filtros['fecha_inicio'], '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(filtros['fecha_fin'], '%Y-%m-%d').date()

            if fecha_fin <= fecha_inicio:
                self.view.mostrar_mensaje("Error", "La Fecha Fin debe ser posterior a la Fecha Inicio.", error=True)
                return
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Formato de fecha inválido: {e}", error=True)
            return

        try:
            self.vehiculos_filtrados = self.modelo_vehiculo.filtar_disponibles(
                fecha_inicio=filtros['fecha_inicio'],
                fecha_fin=filtros['fecha_fin'],
                id_categoria=filtros['id_categoria'],
                marca=filtros['marca']
            )
            for v in self.vehiculos_filtrados:
                v.categoria_nombre = v.categoria.nombre if v.categoria else "N/A"
            print(f"Vehículos disponibles encontrados: {len(self.vehiculos_filtrados)}")

            self.view.actualizar_lista_vehiculos(self.vehiculos_filtrados)
            self.view.ocultar_panel_detalle()

            if not self.vehiculos_filtrados:
                self.view.mostrar_mensaje("Aviso", "No se encontraron vehículos disponibles.")
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al buscar vehículos: {e}", error=True)

    def on_vehiculo_select(self, event):
        id_vehiculo = self.view.obtener_vehiculo_seleccionado()
        if not id_vehiculo:
            return

        self.vehiculo_seleccionado = next(
            (v for v in self.vehiculos_filtrados if v.id_vehiculo == id_vehiculo),
            None
        )
        if not self.vehiculo_seleccionado:
            return

        filtros = self.view.obtener_datos_filtro()
        fecha_inicio = datetime.strptime(filtros['fecha_inicio'], '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(filtros['fecha_fin'], '%Y-%m-%d').date()

        dias = max(1, (fecha_fin - fecha_inicio).days)
        self.costo_total_calculado = dias * self.vehiculo_seleccionado.precio_dia
        foto_tk = None
        vehiculo_obj = self.vehiculo_seleccionado
        if vehiculo_obj.foto_path:
            try:
                ruta_absoluta = os.path.abspath(os.path.join(BASE_DIR, "..", "..", vehiculo_obj.foto_path)) 
                
                img = Image.open(ruta_absoluta)
                img.thumbnail(FOTO_PREVIEW_SIZE)
                foto_tk = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error al cargar la foto del vehículo {vehiculo_obj.patente}: {e}")

        self.view.mostrar_panel_detalle(
            self.vehiculo_seleccionado,
            self.costo_total_calculado,
            fecha_inicio == date.today(),
            foto_tk
        )

    def confirmar_transaccion(self):
        datos = self.view.obtener_datos_transaccion()
        filtros = self.view.obtener_datos_filtro()

        if not self.vehiculo_seleccionado or not datos['id_cliente']:
            self.view.mostrar_mensaje("Error", "Debe seleccionar un vehículo y un cliente.", error=True)
            return

        id_empleado_actual = 1 #CAMBIAR CUANDO EL LOGIN NO ESTE HARDCODEADO
        exito = False

        try:
            fecha_inicio = datetime.strptime(filtros['fecha_inicio'], '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(filtros['fecha_fin'], '%Y-%m-%d').date()

            es_alquiler_hoy = (fecha_inicio == date.today())

            if es_alquiler_hoy:
                if self.view.mostrar_mensaje(
                    "Confirmar Alquiler",
                    f"¿Confirmar ALQUILER INMEDIATO?\nVehículo: {self.vehiculo_seleccionado.patente}\nTotal: ${self.costo_total_calculado:,.2f}",
                    confirm=True
                ):
                    exito = self.modelo_alquiler.crear_transaccion(
                        id_cliente=datos['id_cliente'],
                        id_vehiculo=self.vehiculo_seleccionado.id_vehiculo,
                        id_empleado=id_empleado_actual,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        costo_total=self.costo_total_calculado
                    )

            else:
                if self.view.mostrar_mensaje(
                    "Confirmar Reserva",
                    f"¿Confirmar RESERVA?\nVehículo: {self.vehiculo_seleccionado.patente}\nFechas: {fecha_inicio} a {fecha_fin}\nTotal: ${self.costo_total_calculado:,.2f}",
                    confirm=True
                ):
                    exito = self.modelo_reserva.registrar(
                        id_cliente=datos['id_cliente'],
                        id_vehiculo=self.vehiculo_seleccionado.id_vehiculo,
                        id_empleado=id_empleado_actual,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        costo_total=self.costo_total_calculado
                    )

            if exito:
                self.view.mostrar_mensaje("Éxito", "Transacción registrada exitosamente.")
                self.view.limpiar_todo()

                if es_alquiler_hoy:
                    self.actualizar_vista_vehiculos()

        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al confirmar: {e}", error=True)

    def actualizar_vista_vehiculos(self):
        """
        Pide al controlador de Vehículos que actualice su vista.
        Ideal cuando se alquila un auto y debe desaparecer.
        """
        try:
            vehiculo_controller = self.app.get_controller("Vehiculos")
            if vehiculo_controller:
                vehiculo_controller.cargar_vehiculos()
        except Exception as e:
            print(f"Error al actualizar vista de Vehículos: {e}")

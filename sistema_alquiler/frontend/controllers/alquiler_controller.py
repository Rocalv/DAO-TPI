# frontend/controllers/alquiler_controller.py
import os
import shutil
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import date, datetime
from sistema_alquiler.backend.models.vehiculo import Vehiculo
from sistema_alquiler.backend.models.categoria import Categoria
from sistema_alquiler.backend.models.cliente import Cliente
from sistema_alquiler.backend.models.alquiler import Alquiler
from sistema_alquiler.backend.models.reserva import Reserva

class AlquilerController:
    
    def __init__(self, view, app): # <-- CAMBIO: Recibimos 'app'
        """Inicializa el controlador."""
        self.view = view
        self.app = app # <-- CAMBIO: Guardamos referencia a la App principal
        self.modelo_vehiculo = Vehiculo
        self.modelo_categoria = Categoria
        self.modelo_cliente = Cliente
        self.modelo_alquiler = Alquiler
        self.modelo_reserva = Reserva
        self.vehiculos_filtrados = []
        self.vehiculo_seleccionado = None
        self.costo_total_calculado = 0.0

    def inicializar_vista(self):
        """Carga los comboboxes iniciales."""
        self.cargar_categorias()
        self.cargar_clientes()
        self.view.ocultar_panel_detalle()

    def cargar_categorias(self):
        """Carga el combobox de categorías para el filtro."""
        try:
            categorias = self.modelo_categoria.obtener_todas()
            if categorias:
                self.view.set_categorias_combobox(categorias)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar categorías: {e}", error=True)
            
    def cargar_clientes(self):
        """Carga el combobox de clientes para el formulario."""
        try:
            clientes = self.modelo_cliente.obtener_todos(incluir_inactivos=False)
            if clientes:
                self.view.set_clientes_combobox(clientes)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar clientes: {e}", error=True)

    def buscar_disponibles(self):
        """Filtra y muestra vehículos disponibles según las fechas."""
        filtros = self.view.obtener_datos_filtro()
        try:
            fecha_inicio = datetime.strptime(filtros['fecha_inicio'], '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(filtros['fecha_fin'], '%Y-%m-%d').date()
            if fecha_fin <= fecha_inicio:
                self.view.mostrar_mensaje("Error", "La Fecha Fin debe ser posterior a la Fecha Inicio.", error=True); return
            # (Permitimos fechas pasadas para pruebas, pero idealmente se bloquearía)
            # if fecha_inicio < date.today():
            #     self.view.mostrar_mensaje("Error", "La Fecha Inicio no puede ser en el pasado.", error=True); return
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Formato de fecha inválido o error: {e}", error=True); return

        try:
            self.vehiculos_filtrados = self.modelo_vehiculo.buscar_disponibles(
                fecha_inicio=filtros['fecha_inicio'],
                fecha_fin=filtros['fecha_fin'],
                id_categoria=filtros['id_categoria'],
                marca=filtros['marca']
            )
            self.view.actualizar_lista_vehiculos(self.vehiculos_filtrados)
            self.view.ocultar_panel_detalle()
            if not self.vehiculos_filtrados:
                self.view.mostrar_mensaje("Aviso", "No se encontraron vehículos disponibles para esas fechas.")
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al buscar vehículos: {e}", error=True)

    def on_vehiculo_select(self, event):
        """Muestra el panel de detalle al seleccionar un vehículo."""
        id_vehiculo = self.view.obtener_vehiculo_seleccionado()
        if not id_vehiculo: return
        self.vehiculo_seleccionado = next((v for v in self.vehiculos_filtrados if v.id_vehiculo == id_vehiculo), None)
        if not self.vehiculo_seleccionado: return

        filtros = self.view.obtener_datos_filtro()
        fecha_inicio = datetime.strptime(filtros['fecha_inicio'], '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(filtros['fecha_fin'], '%Y-%m-%d').date()
        dias = max(1, (fecha_fin - fecha_inicio).days)
        self.costo_total_calculado = dias * self.vehiculo_seleccionado.precio_dia
        
        self.view.mostrar_panel_detalle(self.vehiculo_seleccionado, self.costo_total_calculado, fecha_inicio == date.today())

    def confirmar_transaccion(self):
        """Confirma el Alquiler o la Reserva."""
        datos = self.view.obtener_datos_transaccion()
        filtros = self.view.obtener_datos_filtro()

        if not self.vehiculo_seleccionado or not datos['id_cliente']:
            self.view.mostrar_mensaje("Error", "Debe seleccionar un vehículo y un cliente.", error=True); return
        
        id_empleado_actual = 1
        exito = False
        
        try:
            fecha_inicio = datetime.strptime(filtros['fecha_inicio'], '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(filtros['fecha_fin'], '%Y-%m-%d').date()
            es_alquiler_hoy = (fecha_inicio == date.today())

            if es_alquiler_hoy:
                if self.view.mostrar_mensaje("Confirmar Alquiler", f"¿Confirmar ALQUILER INMEDIATO?\nVehículo: {self.vehiculo_seleccionado.patente}\nTotal: ${self.costo_total_calculado:,.2f}", confirm=True):
                    exito = self.modelo_alquiler.crear_transaccion(
                        id_cliente=datos['id_cliente'], id_vehiculo=self.vehiculo_seleccionado.id_vehiculo,
                        id_empleado=id_empleado_actual, fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin, costo_total=self.costo_total_calculado
                    )
            else:
                if self.view.mostrar_mensaje("Confirmar Reserva", f"¿Confirmar RESERVA a futuro?\nVehículo: {self.vehiculo_seleccionado.patente}\nFechas: {fecha_inicio} al {fecha_fin}\nTotal: ${self.costo_total_calculado:,.2f}", confirm=True):
                    exito = self.modelo_reserva.crear(
                        id_cliente=datos['id_cliente'], id_vehiculo=self.vehiculo_seleccionado.id_vehiculo,
                        id_empleado=id_empleado_actual, fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin, costo_total=self.costo_total_calculado
                    )

            if exito:
                self.view.mostrar_mensaje("Éxito", "Transacción registrada exitosamente.")
                self.view.limpiar_todo()
                if es_alquiler_hoy:
                    self.actualizar_vista_vehiculos() # <-- SOLUCIÓN
                
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al confirmar: {e}", error=True)

    def actualizar_vista_vehiculos(self):
        """Busca el controlador de Vehiculos y le pide recargar sus datos."""
        try:
            vehiculo_controller = self.app.get_controller("Vehiculos")
            if vehiculo_controller:
                vehiculo_controller.cargar_vehiculos()
        except Exception as e:
            print(f"Error al intentar recargar la vista de Vehículos: {e}")
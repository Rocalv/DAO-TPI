from entidades.cliente import Cliente
from frontend.boundary.cliente_view import ClienteView

class ClienteController:
    
    def __init__(self, parent):
        """Inicializa el controlador y crea la vista sin acoplamiento."""
        self.modelo = Cliente
        self.view = ClienteView(
            parent,
            on_guardar=self.guardar_cliente,
            on_nuevo=self.limpiar_formulario,
            on_eliminar=self.eliminar_cliente,
            on_select_row=self.seleccionar_cliente
        )

    def cargar_clientes(self):
        """Obtiene todos los clientes del modelo y actualiza la vista."""
        clientes = self.modelo.consultar(incluir_inactivos=True)
        self.view.actualizar_lista(clientes)
        
    def guardar_cliente(self):
        """Obtiene datos de la vista y los envía al modelo para guardar o actualizar."""
        if not self.view.validar_formulario():
            return
        datos = self.view.obtener_datos_formulario()

        try:
            cliente_existente = self.modelo.filtrar_por_dni(datos['dni'])
            if datos['id_cliente'] is None:
                # REGISTRAR CLIENTE
                if cliente_existente:
                    self.view.mostrar_mensaje("Error de Validación", "El DNI ya existe.", error=True)
                    return
                
                self.modelo.registrar(datos['dni'], datos['nombre'], datos['apellido'], datos['telefono'], datos['email'], datos['direccion'])
                self.view.mostrar_mensaje("Éxito", "Cliente creado exitosamente.")
            else:
                # MODIFICAR CLIENTE
                if cliente_existente and str(cliente_existente['id_cliente']) != str(datos['id_cliente']):
                    self.view.mostrar_mensaje("Error de Validación", "El DNI ya pertenece a otro cliente.", error=True)
                    return

                self.modelo.modificar(datos['id_cliente'], datos['dni'], datos['nombre'], datos['apellido'], datos['telefono'], datos['email'], datos['direccion'], datos['activo'])
                self.view.mostrar_mensaje("Éxito", "Cliente actualizado exitosamente.")
                
            self.limpiar_formulario()
            self.cargar_clientes()
            
        except Exception as e:
            self.view.mostrar_mensaje("Error de Base de Datos", f"Error al guardar: {e}", error=True)

    def eliminar_cliente(self):
        """Obtiene el ID de la vista y pide al modelo que dé de baja al cliente."""
        datos = self.view.obtener_datos_formulario()
        id_cliente = datos.get('id_cliente')
        
        if id_cliente is None:
            self.view.mostrar_mensaje("Error", "Debe seleccionar un cliente para eliminar.", error=True)
            return

        try:
            if self.view.mostrar_mensaje("Confirmar", "¿Está seguro de que desea dar de baja a este cliente?", confirm=True):
                self.modelo.eliminar(id_cliente)
                self.view.mostrar_mensaje("Éxito", "Cliente dado de baja.")
                self.limpiar_formulario()
                self.cargar_clientes()
        except Exception as e:
             self.view.mostrar_mensaje("Error", f"No se pudo dar de baja al cliente: {e}", error=True)

    def seleccionar_cliente(self, event):
        """Se llama cuando el usuario hace clic en un item del Treeview."""
        selected = self.view.tree.selection()
        if not selected:
            return
        
        id_cliente = selected[0]
        cliente = self.modelo.filtrar_por_id(id_cliente)

        if cliente:
            self.view.seleccionar_item_en_formulario(cliente)

    def limpiar_formulario(self):
        """Pide a la vista que limpie sus campos."""
        self.view.limpiar_formulario()

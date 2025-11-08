# frontend/controllers/cliente_controller.py
from sistema_alquiler.backend.models.cliente import Cliente

class ClienteController:
    
    def __init__(self, view):
        """Inicializa el controlador."""
        self.view = view
        self.modelo = Cliente
        
    def cargar_clientes(self):
        """Obtiene todos los clientes del modelo y actualiza la vista."""
        clientes = self.modelo.obtener_todos(incluir_inactivos=True)
        self.view.actualizar_lista(clientes)
        
    def guardar_cliente(self):
        """Obtiene datos de la vista y los envía al modelo para guardar o actualizar."""
        datos = self.view.obtener_datos_formulario()
        
        if not datos['dni'] or not datos['nombre'] or not datos['apellido']:
            self.view.mostrar_mensaje("Error de Validación", "DNI, Nombre y Apellido son obligatorios.", error=True)
            return

        try:
            cliente_existente = self.modelo.obtener_por_dni(datos['dni'])
            if datos['id_cliente'] is None:
                # Es un cliente nuevo
                if cliente_existente:
                    self.view.mostrar_mensaje("Error de Validación", "El DNI ya existe.", error=True)
                    return
                
                self.modelo.crear(datos['dni'], datos['nombre'], datos['apellido'], datos['telefono'], datos['email'], datos['direccion'])
                self.view.mostrar_mensaje("Éxito", "Cliente creado exitosamente.")
            else:
                # Es un cliente existente
                if cliente_existente and str(cliente_existente['id_cliente']) != str(datos['id_cliente']):
                    self.view.mostrar_mensaje("Error de Validación", "El DNI ya pertenece a otro cliente.", error=True)
                    return

                self.modelo.actualizar(datos['id_cliente'], datos['dni'], datos['nombre'], datos['apellido'], datos['telefono'], datos['email'], datos['direccion'], datos['activo'])
                self.view.mostrar_mensaje("Éxito", "Cliente actualizado exitosamente.")
                
            self.limpiar_formulario()
            self.cargar_clientes()
            
        except Exception as e:
            self.view.mostrar_mensaje("Error de Base de Datos", f"Error al guardar: {e}", error=True)

    def eliminar_cliente(self):
        """Obtiene el ID de la vista y pide al modelo que 'elimine' (dar de baja) al cliente."""
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
        """Se llama cuando el usuario hace clic en un item de la grilla (Treeview)."""
        selected_item = self.view.tree.selection()
        if not selected_item:
            return
            
        # Obtenemos el ID desde el 'iid' de la fila, que es donde lo guardamos.
        id_cliente = selected_item[0] 
        
        cliente = self.modelo.obtener_por_id(id_cliente)
        
        if cliente:
            self.view.seleccionar_item_en_formulario(cliente)

    def limpiar_formulario(self):
        """Pide a la vista que limpie sus campos."""
        self.view.limpiar_formulario()
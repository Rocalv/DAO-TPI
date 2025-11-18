import os
import shutil
from tkinter import filedialog
from PIL import Image, ImageTk
from entidades.empleado import Empleado
from entidades.cargo_empleado import CargoEmpleado
from frontend.boundary.empleado_view import EmpleadoView

FOTO_PREVIEW_SIZE = (220, 220)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DESTINO_FOTOS = os.path.join(BASE_DIR, "..", "assets", "empleados")
os.makedirs(DESTINO_FOTOS, exist_ok=True)


class EmpleadoController:
    def __init__(self, parent):
        self.modelo = Empleado
        self.modelo_cargo = CargoEmpleado

        self.view = EmpleadoView(
            parent,
            on_guardar=self.guardar_empleado,
            on_nuevo=self.limpiar_formulario,
            on_eliminar=self.eliminar_empleado,
            on_seleccionar_foto=self.seleccionar_foto,
            on_select_row=self.seleccionar_empleado
        )

        
    def cargar_empleados(self):
        """Obtiene todos los empleados del modelo y actualiza la vista."""
        empleados = self.modelo.consultar(solo_activos=False)
        self.view.actualizar_lista(empleados)
        self.cargar_cargos()

    def cargar_cargos(self):
        """Obtiene los cargos y los carga en el combobox de la vista."""
        try:
            cargos = self.modelo_cargo.obtener_todos()
            if cargos:
                self.view.set_cargos_combobox(cargos)
            else:
                self.view.mostrar_mensaje("Aviso", "No hay cargos definidos en la base de datos.", error=True)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"No se pudo cargar la lista de cargos: {e}", error=True)

    def seleccionar_foto(self):
        """Abre un diálogo para que el usuario seleccione una foto."""
        ruta_origen = filedialog.askopenfilename(
            title="Seleccionar foto de empleado",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png")]
        )
        if not ruta_origen:
            return
        self.view.foto_path_var.set(ruta_origen)
        try:
            img = Image.open(ruta_origen)
            img.thumbnail(FOTO_PREVIEW_SIZE)
            foto_tk = ImageTk.PhotoImage(img)
            self.view.actualizar_preview_foto(foto_tk)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"No se pudo cargar la imagen: {e}", error=True)

    def guardar_empleado(self):
        """Guarda o actualiza un empleado, manejando la copia de la foto."""
        if not self.view.validar_formulario():
            return
        datos = self.view.obtener_datos_formulario()
                
        try:
            empleado_existente = self.modelo.filtrar_por_dni(datos['dni'])
            ruta_foto_guardada = None

            if datos['id_empleado'] is None:
                # REGISTREAR EMPLEADO
                if empleado_existente:
                    self.view.mostrar_mensaje("Error de Validación", "El DNI ya existe.", error=True)
                    return
                if not datos['foto_path_temporal']:
                    self.view.mostrar_mensaje("Error de Validación", "Debe seleccionar una foto para el nuevo empleado.", error=True)
                    return
                    
                ruta_foto_guardada = self._copiar_foto_a_assets(datos['foto_path_temporal'], datos['dni'])
                
                # OBTENER EL OBJETO CargoEmpleado
                cargo_obj = self.modelo_cargo.obtener_registro(datos['id_cargo'])

                emp = Empleado(
                    dni=datos['dni'],
                    nombre=datos['nombre'],
                    apellido=datos['apellido'],
                    cargo=cargo_obj,
                    telefono=datos['telefono'],
                    email=datos['email'],
                    foto_path=ruta_foto_guardada,
                    activo=datos['activo']
                )

            else:
                # MODIFICAR EMPLEADO
                if empleado_existente and str(empleado_existente.id_empleado) != str(datos['id_empleado']):
                    self.view.mostrar_mensaje("Error de Validación", "El DNI ya pertenece a otro empleado.", error=True)
                    return
                
                emp = self.modelo.filtrar_por_id(datos['id_empleado'])
                if not emp:
                    self.view.mostrar_mensaje("Error", "No se encontró el empleado a actualizar.", error=True)
                    return
                
                # Guardar la ruta de la foto vieja ANTES de actualizar el objeto
                ruta_foto_antigua = emp.foto_path

                emp.dni = datos['dni']
                emp.nombre = datos['nombre']
                emp.apellido = datos['apellido']
                emp.cargo = self.modelo_cargo.obtener_registro(datos['id_cargo']) # CORRECCIÓN: Actualizar el objeto Cargo
                emp.telefono = datos['telefono']
                emp.email = datos['email']
                emp.activo = datos['activo']
                
                if datos['foto_path_temporal']:
                    ruta_foto_guardada = self._copiar_foto_a_assets(datos['foto_path_temporal'], datos['dni'])
                    
                    # Llamar a la función de borrado
                    self._eliminar_foto_antigua(ruta_foto_antigua, ruta_foto_guardada)
                    emp.foto_path = ruta_foto_guardada
            
            if emp.registrar() if datos['id_empleado'] is None else emp.modificar(): 
                self.view.mostrar_mensaje("Éxito", "Empleado guardado exitosamente.")
                self.limpiar_formulario()
                self.cargar_empleados()
            else:
                self.view.mostrar_mensaje("Error", "No se pudo guardar el empleado en la base de datos.", error=True)
            
        except Exception as e:
            self.view.mostrar_mensaje("Error de Aplicación", f"Error al guardar: {e}", error=True)

    def _copiar_foto_a_assets(self, ruta_origen, dni):
        """Copia la foto seleccionada a la carpeta de assets del proyecto."""
        try:
            _, extension = os.path.splitext(ruta_origen)
            nombre_archivo = f"{dni}{extension}"
            ruta_destino = os.path.join(DESTINO_FOTOS, nombre_archivo)
            shutil.copy(ruta_origen, ruta_destino)
            return os.path.join("frontend", "assets", "empleados", nombre_archivo)
        except Exception as e:
            raise Exception(f"Error al copiar la foto: {e}")

    def _eliminar_foto_antigua(self, ruta_antigua, ruta_nueva):
        """Elimina la foto antigua si existe y es diferente a la nueva."""
        if not ruta_antigua: 
            return
        if ruta_antigua == ruta_nueva: 
            return
            
        try:
            ruta_completa_antigua = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ruta_antigua))
            if os.path.exists(ruta_completa_antigua):
                os.remove(ruta_completa_antigua)
                print(f"Foto antigua eliminada: {ruta_completa_antigua}")
        except Exception as e:
            print(f"Advertencia: No se pudo eliminar la foto antigua: {e}")

    def eliminar_empleado(self):
        """Obtiene el ID y pide al modelo que 'elimine' (dar de baja) al empleado."""
        datos = self.view.obtener_datos_formulario()
        id_empleado = datos.get('id_empleado')
        
        if id_empleado is None:
            self.view.mostrar_mensaje("Error", "Debe seleccionar un empleado para eliminar.", error=True)
            return

        try:
            if self.view.mostrar_mensaje("Confirmar", "¿Está seguro de que desea dar de baja a este empleado?", confirm=True):
                emp = self.modelo.filtrar_por_id(id_empleado)
                if emp and emp.eliminar():
                    self.view.mostrar_mensaje("Éxito", "Empleado dado de baja.")
                    self.limpiar_formulario()
                    self.cargar_empleados()
                else:
                    self.view.mostrar_mensaje("Error", "No se pudo dar de baja al empleado.", error=True)
        except Exception as e:
             self.view.mostrar_mensaje("Error", f"No se pudo dar de baja al empleado: {e}", error=True)

    def seleccionar_empleado(self, event):
        """Se llama cuando el usuario hace clic en un item de la grilla (Treeview)."""
        selected_item = self.view.tree.selection()
        if not selected_item:
            return
            
        id_empleado = selected_item[0] 
        emp = self.modelo.filtrar_por_id(id_empleado)
        
        if emp:
            foto_tk = None
            if emp.foto_path:
                try:
                    ruta_foto_completa = os.path.abspath(os.path.join(BASE_DIR, "..", "..", emp.foto_path))
                    
                    if os.path.exists(ruta_foto_completa):
                        img = Image.open(ruta_foto_completa)
                        img.thumbnail(FOTO_PREVIEW_SIZE)
                        foto_tk = ImageTk.PhotoImage(img)
                    else:
                        print(f"Advertencia: No se encontró la foto en {ruta_foto_completa}")
                        
                except Exception as e:
                    print(f"No se pudo cargar la imagen guardada: {e}")
                    foto_tk = None
                    
            self.view.seleccionar_item_en_formulario(emp, foto_tk)

    def limpiar_formulario(self):
        """Pide a la vista que limpie sus campos."""
        self.view.limpiar_formulario()
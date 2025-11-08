# frontend/controllers/vehiculo_controller.py
import os
import shutil
from tkinter import filedialog
from PIL import Image, ImageTk
from sistema_alquiler.backend.models.vehiculo import Vehiculo
from sistema_alquiler.backend.models.categoria import Categoria
from sistema_alquiler.backend.models.estado_vehiculo import FabricaEstados # <-- IMPORTANTE

FOTO_PREVIEW_SIZE = (220, 220)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DESTINO_FOTOS = os.path.join(BASE_DIR, "..", "assets", "vehiculos")
os.makedirs(DESTINO_FOTOS, exist_ok=True)

class VehiculoController:
    
    def __init__(self, view):
        self.view = view
        self.modelo = Vehiculo
        self.modelo_categoria = Categoria
        
    def cargar_vehiculos(self):
        """Carga vehículos (excluyendo 'Baja') y los comboboxes."""
        vehiculos = self.modelo.listar_todos(excluir_baja=True)
        self.view.actualizar_lista(vehiculos)
        self.cargar_categorias()
        self.cargar_estados()

    def cargar_categorias(self):
        """Carga el combobox de categorías."""
        try:
            categorias = self.modelo_categoria.obtener_todas()
            if categorias:
                self.view.set_categorias_combobox(categorias)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar categorías: {e}", error=True)
            
    def cargar_estados(self):
        """Carga el combobox de estados desde la Fábrica de Estados."""
        try:
            # Usamos el mapa {nombre: id} de la fábrica
            estados_map = FabricaEstados.listar_estados_para_ui()
            if estados_map:
                self.view.set_estados_combobox(estados_map)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar estados: {e}", error=True)

    def on_categoria_changed(self, event=None):
        """Se llama cuando el usuario cambia la selección del combobox de categoría."""
        nombre_cat = self.view.categoria_var.get()
        if nombre_cat in self.view.categorias_map:
            precio = self.view.categorias_map[nombre_cat]['precio_dia']
            self.view.actualizar_precio_label(precio)

    def seleccionar_foto(self):
        """Abre un diálogo para que el usuario seleccione una foto."""
        ruta_origen = filedialog.askopenfilename(title="Seleccionar foto", filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if not ruta_origen: return
        self.view.foto_path_var.set(ruta_origen)
        try:
            img = Image.open(ruta_origen)
            img.thumbnail(FOTO_PREVIEW_SIZE)
            self.view.actualizar_preview_foto(ImageTk.PhotoImage(img))
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar imagen: {e}", error=True)

    def guardar_vehiculo(self):
        """Guarda o actualiza un vehículo."""
        datos = self.view.obtener_datos_formulario()
        
        if not all([datos['patente'], datos['marca'], datos['modelo'], datos['anio'], datos['id_categoria'], datos['id_estado']]):
             self.view.mostrar_mensaje("Error", "Patente, Marca, Modelo, Año, Categoría y Estado son obligatorios.", error=True)
             return

        try:
            vehiculo_existente = self.modelo.buscar_por_patente(datos['patente'])
            ruta_foto_guardada = None

            if datos['id_vehiculo'] is None:
                # --- NUEVO VEHÍCULO ---
                if vehiculo_existente:
                     self.view.mostrar_mensaje("Error", "La patente ya existe.", error=True)
                     return
                
                if datos['foto_path_temporal']:
                    ruta_foto_guardada = self._copiar_foto(datos['foto_path_temporal'], datos['patente'])

                vehiculo = Vehiculo(
                    patente=datos['patente'], marca=datos['marca'], modelo=datos['modelo'],
                    anio=int(datos['anio']), color=datos['color'], 
                    kilometraje=int(datos['kilometraje'] or 0),
                    km_mantenimiento=int(datos['km_mantenimiento'] or 10000),
                    id_categoria=datos['id_categoria'], 
                    id_estado=datos['id_estado'], 
                    foto_path=ruta_foto_guardada
                )
            else:
                # --- ACTUALIZAR VEHÍCULO ---
                if vehiculo_existente and str(vehiculo_existente.id_vehiculo) != str(datos['id_vehiculo']):
                     self.view.mostrar_mensaje("Error", "La patente ya pertenece a otro vehículo.", error=True)
                     return

                vehiculo = self.modelo.buscar_por_id(datos['id_vehiculo'])
                if not vehiculo: return

                ruta_antigua = vehiculo.foto_path
                
                vehiculo.patente = datos['patente']
                vehiculo.marca = datos['marca']
                vehiculo.modelo = datos['modelo']
                vehiculo.anio = int(datos['anio'])
                vehiculo.color = datos['color']
                vehiculo.kilometraje = int(datos['kilometraje'] or 0)
                vehiculo.km_mantenimiento = int(datos['km_mantenimiento'] or 10000)
                vehiculo.id_categoria = datos['id_categoria']
                vehiculo.set_estado(FabricaEstados._estados[datos['estado_nombre']].nombre_estado()) # Actualizamos el objeto estado
                
                if datos['foto_path_temporal']:
                    ruta_nueva = self._copiar_foto(datos['foto_path_temporal'], datos['patente'])
                    self._eliminar_foto_antigua(ruta_antigua, ruta_nueva)
                    vehiculo.foto_path = ruta_nueva

            if vehiculo.guardar():
                self.view.mostrar_mensaje("Éxito", "Vehículo guardado.")
                self.limpiar_formulario()
                self.cargar_vehiculos()
            else:
                self.view.mostrar_mensaje("Error", "No se pudo guardar en la BD.", error=True)

        except ValueError:
             self.view.mostrar_mensaje("Error", "Año y Kilometrajes deben ser números.", error=True)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error de aplicación: {e}", error=True)

    def _copiar_foto(self, origen, patente):
        """Copia la foto seleccionada a la carpeta de assets del proyecto."""
        try:
            _, ext = os.path.splitext(origen)
            nombre = f"{patente.replace(' ', '_')}{ext}" # Limpiamos la patente
            destino = os.path.join(DESTINO_FOTOS, nombre)
            shutil.copy(origen, destino)
            return os.path.join("frontend", "assets", "vehiculos", nombre)
        except Exception as e:
            raise Exception(f"Error al copiar foto: {e}")

    def _eliminar_foto_antigua(self, ruta_antigua, ruta_nueva):
        """Elimina la foto antigua si existe y es diferente a la nueva."""
        if not ruta_antigua or ruta_antigua == ruta_nueva: return
        try:
            ruta_completa = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ruta_antigua))
            if os.path.exists(ruta_completa): os.remove(ruta_completa)
        except: pass

    def eliminar_vehiculo(self):
        """Cambia el estado del vehículo a 'Baja'."""
        datos = self.view.obtener_datos_formulario()
        id_vehiculo = datos.get('id_vehiculo')
        if not id_vehiculo:
             self.view.mostrar_mensaje("Error", "Seleccione un vehículo.", error=True)
             return

        if self.view.mostrar_mensaje("Confirmar", "¿Dar de baja este vehículo? Esta acción no se puede deshacer.", confirm=True):
            vehiculo = self.modelo.buscar_por_id(id_vehiculo)
            if vehiculo and vehiculo.eliminar(): # .eliminar() lo pone en 'Baja' y guarda
                self.view.mostrar_mensaje("Éxito", "Vehículo dado de baja.")
                self.limpiar_formulario()
                self.cargar_vehiculos()
            else:
                self.view.mostrar_mensaje("Error", "No se pudo dar de baja el vehículo.", error=True)

    def seleccionar_vehiculo(self, event):
        """Muestra los datos del vehículo seleccionado en el formulario."""
        selected = self.view.tree.selection()
        if not selected: return
        id_vehiculo = selected[0]
        vehiculo = self.modelo.buscar_por_id(id_vehiculo)
        if vehiculo:
            foto_tk = None
            if vehiculo.foto_path:
                try:
                    ruta_completa = os.path.abspath(os.path.join(BASE_DIR, "..", "..", vehiculo.foto_path))
                    if os.path.exists(ruta_completa):
                        img = Image.open(ruta_completa)
                        img.thumbnail(FOTO_PREVIEW_SIZE)
                        foto_tk = ImageTk.PhotoImage(img)
                except: pass
            self.view.seleccionar_item_en_formulario(vehiculo, foto_tk)

    def limpiar_formulario(self):
        """Limpia el formulario."""
        self.view.limpiar_formulario()
# frontend/controllers/vehiculo_controller.py
import os
import shutil
from tkinter import filedialog
from PIL import Image, ImageTk

from entidades.vehiculo import Vehiculo
from entidades.categoria import Categoria
from persistencia.Repository.repository_estados import RepositoryEstados

from frontend.boundary.vehiculo_view import VehiculoView

FOTO_PREVIEW_SIZE = (220, 220)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DESTINO_FOTOS = os.path.join(BASE_DIR, "..", "assets", "vehiculos")
os.makedirs(DESTINO_FOTOS, exist_ok=True)

class VehiculoController:

    def __init__(self, parent):

        self.modelo = Vehiculo
        self.modelo_categoria = Categoria

        self.view = VehiculoView(
            parent,
            on_guardar=self.guardar_vehiculo,
            on_nuevo=self.limpiar_formulario,
            on_eliminar=self.eliminar_vehiculo,
            on_seleccionar_foto=self.seleccionar_foto,
            on_categoria_changed=self.on_categoria_changed,
            on_select_row=self.seleccionar_vehiculo
        )

        self.view.create_widgets()
        self.cargar_vehiculos()
    
    def cargar_vehiculos(self):
        vehiculos = self.modelo.consultar(excluir_baja=True) 
        self.view.actualizar_lista(vehiculos)
        self.cargar_categorias()
        self.cargar_estados()

    def cargar_categorias(self):
        try:
            categorias = self.modelo_categoria.consultar()
            self.view.set_categorias_combobox(categorias)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar categorías: {e}", error=True)
    
    def cargar_categorias(self):
        try:
            categorias_data = self.modelo_categoria.consultar()
            self.categorias_map = {
                cat['nombre']: Categoria(
                    id_categoria=cat['id_categoria'], 
                    nombre=cat['nombre'], 
                    precio_dia=cat['precio_dia']
                ) for cat in categorias_data
            }
            self.view.set_categorias_combobox(list(self.categorias_map.values()))
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar categorías: {e}", error=True)

    def cargar_estados(self):
        try:
            estados = {"Alquilado": 1,
                       "Disponible": 2,
                        "FueraServicio": 3,
                        "Mantenimiento": 4
                        }
            self.view.set_estados_combobox(estados)
        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al cargar estados: {e}", error=True)
    
    def cargar_estados(self):
            try:
                estados_para_vista = {nombre: id_est for nombre, id_est in self.estado_vehiculo_map.items() if nombre != 'Baja'}
                self.view.set_estados_combobox(estados_para_vista)
            except Exception as e:
                self.view.mostrar_mensaje("Error", f"Error al cargar estados: {e}", error=True)
    
    def on_categoria_changed(self, event=None):
        nombre_cat = self.view.categoria_var.get()
        categoria_obj = self.categorias_map.get(nombre_cat)
        if categoria_obj:
            precio = categoria_obj.precio_dia
            self.view.actualizar_precio_label(precio)

    def seleccionar_foto(self):
        ruta_origen = filedialog.askopenfilename(
            title="Seleccionar foto",
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
            self.view.mostrar_mensaje("Error", f"Error al cargar imagen: {e}", error=True)

    # def guardar_vehiculo(self):
    #     datos = self.view.obtener_datos_formulario()

    #     if not all([datos["patente"], datos["marca"], datos["modelo"],
    #                 datos["anio"], datos["id_categoria"], datos["id_estado"]]):
    #         self.view.mostrar_mensaje("Error", "Faltan campos obligatorios.", error=True)
    #         return

    #     try:
    #         vehiculo_existente = self.modelo.filtrar_por_patente(datos["patente"])

    #         if datos["id_vehiculo"] is None:
    #             # NUEVO VEHÍCULO
    #             if vehiculo_existente:
    #                 self.view.mostrar_mensaje("Error", "La patente ya existe.", error=True)
    #                 return

    #             foto_path = None
    #             if datos["foto_path_temporal"]:
    #                 foto_path = self._copiar_foto(datos["foto_path_temporal"], datos["patente"])

    #             vehiculo = Vehiculo(
    #                 patente=datos["patente"],
    #                 marca=datos["marca"],
    #                 modelo=datos["modelo"],
    #                 anio=int(datos["anio"]),
    #                 color=datos["color"],
    #                 kilometraje=int(datos["kilometraje"] or 0),
    #                 km_mantenimiento=int(datos["km_mantenimiento"] or 10000),
    #                 id_categoria=datos["id_categoria"],
    #                 id_estado=datos["id_estado"],
    #                 foto_path=foto_path
    #             )

    #         else:
    #             # ACTUALIZAR VEHÍCULO
    #             if vehiculo_existente and str(vehiculo_existente.id_vehiculo) != str(datos["id_vehiculo"]):
    #                 self.view.mostrar_mensaje("Error", """La patente pertenece a otro vehículo.""", error=True)
    #                 return

    #             vehiculo = self.modelo.buscar_por_id(datos["id_vehiculo"])
    #             if not vehiculo:
    #                 return

    #             vehiculo.patente = datos["patente"]
    #             vehiculo.marca = datos["marca"]
    #             vehiculo.modelo = datos["modelo"]
    #             vehiculo.anio = int(datos["anio"])
    #             vehiculo.color = datos["color"]
    #             vehiculo.kilometraje = int(datos["kilometraje"] or 0)
    #             vehiculo.km_mantenimiento = int(datos["km_mantenimiento"] or 10000)
    #             vehiculo.categortia = Categoria

    #             vehiculo.set_estado(estado_obj)

    #             if datos["foto_path_temporal"]:
    #                 nueva = self._copiar_foto(datos["foto_path_temporal"], datos["patente"])
    #                 self._eliminar_foto_antigua(vehiculo.foto_path, nueva)
    #                 vehiculo.foto_path = nueva

    #         if vehiculo.guardar():
    #             self.view.mostrar_mensaje("Éxito", "Vehículo guardado.")
    #             self.limpiar_formulario()
    #             self.cargar_vehiculos()

    #     except Exception as e:
    #         self.view.mostrar_mensaje("Error", f"Error al guardar: {e}", error=True)
    def guardar_vehiculo(self):
        datos = self.view.obtener_datos_formulario()

        # Validación de campos obligatorios
        if not all([datos["patente"], datos["marca"], datos["modelo"],
                    datos["anio"], datos["nombre_categoria"], datos["nombre_estado"]]):
            self.view.mostrar_mensaje("Error", "Faltan campos obligatorios.", error=True)
            return

        try:
            # Obtener objetos necesarios
            categoria_obj = self.categorias_map.get(datos["nombre_categoria"])
            id_estado = self.estado_vehiculo_map.get(datos["nombre_estado"])

            if not categoria_obj:
                self.view.mostrar_mensaje("Error", "Categoría no válida.", error=True)
                return
            if not id_estado:
                self.view.mostrar_mensaje("Error", "Estado no válido.", error=True)
                return
            
            # La entidad Vehiculo.buscar_por_patente ahora se llama filtrar_por_patente
            vehiculo_existente = self.modelo.filtrar_por_patente(datos["patente"])
            
            if datos["id_vehiculo"] is None:
                # NUEVO VEHÍCULO
                if vehiculo_existente:
                    self.view.mostrar_mensaje("Error", "La patente ya existe.", error=True)
                    return

                foto_path = None
                if datos["foto_path_temporal"]:
                    foto_path = self._copiar_foto(datos["foto_path_temporal"], datos["patente"])

                # Se crea el objeto Vehiculo con el objeto Categoria (no solo id)
                vehiculo = Vehiculo(
                    patente=datos["patente"],
                    marca=datos["marca"],
                    modelo=datos["modelo"],
                    anio=int(datos["anio"]),
                    categoria=categoria_obj, # <--- OBJETO CATEGORIA
                    color=datos["color"],
                    kilometraje=int(datos["kilometraje"] or 0),
                    km_mantenimiento=int(datos["km_mantenimiento"] or 10000),
                    # El estado se inicializa por defecto en Disponible en el constructor de Vehiculo
                    # Si la entidad soporta pasar un estado inicial, podrías hacerlo aquí
                    # Si no, se usará Disponible. La entidad usa el patrón State.
                    foto_path=foto_path
                )
                
                # El Vehiculo usa el método registrar()
                if vehiculo.registrar():
                    self.view.mostrar_mensaje("Éxito", "Vehículo guardado.")
                    self.limpiar_formulario()
                    self.cargar_vehiculos()
                else:
                    self.view.mostrar_mensaje("Error", "Error al registrar el vehículo.", error=True)

            else:
                # ACTUALIZAR VEHÍCULO
                if vehiculo_existente and str(vehiculo_existente.id_vehiculo) != str(datos["id_vehiculo"]):
                    self.view.mostrar_mensaje("Error", "La patente pertenece a otro vehículo.", error=True)
                    return

                # La entidad Vehiculo.buscar_por_id ahora se llama filtrar_por_id
                vehiculo = self.modelo.filtrar_por_id(datos["id_vehiculo"])
                if not vehiculo:
                    self.view.mostrar_mensaje("Error", "Vehículo a actualizar no encontrado.", error=True)
                    return

                # Actualizar propiedades del objeto entidad
                vehiculo.patente = datos["patente"]
                vehiculo.marca = datos["marca"]
                vehiculo.modelo = datos["modelo"]
                vehiculo.anio = int(datos["anio"])
                vehiculo.color = datos["color"]
                vehiculo.kilometraje = int(datos["kilometraje"] or 0)
                vehiculo.km_mantenimiento = int(datos["km_mantenimiento"] or 10000)
                vehiculo.categoria = categoria_obj # <--- OBJETO CATEGORIA

                # Cambiar estado usando los métodos del patrón State
                nombre_estado_actual = vehiculo.estado.nombre_estado()
                nombre_estado_nuevo = datos["nombre_estado"]
                
                if nombre_estado_nuevo != nombre_estado_actual:
                    if nombre_estado_nuevo == "Disponible":
                        vehiculo.disponibilizar()
                    elif nombre_estado_nuevo == "Alquilado":
                        vehiculo.alquilar()
                    elif nombre_estado_nuevo == "Mantenimiento":
                        vehiculo.mantenimiento()
                    elif nombre_estado_nuevo == "FueraServicio":
                        vehiculo.fuera_servicio()
                    # El cambio de estado se guarda en BD dentro de esos métodos de estado
                
                if datos["foto_path_temporal"]:
                    nueva = self._copiar_foto(datos["foto_path_temporal"], datos["patente"])
                    self._eliminar_foto_antigua(vehiculo.foto_path, nueva)
                    vehiculo.foto_path = nueva
                
                # El Vehiculo usa el método modificar() para guardar el resto de los cambios
                if vehiculo.modificar():
                    self.view.mostrar_mensaje("Éxito", "Vehículo actualizado.")
                    self.limpiar_formulario()
                    self.cargar_vehiculos()
                else:
                    self.view.mostrar_mensaje("Error", "Error al actualizar el vehículo.", error=True)

        except Exception as e:
            self.view.mostrar_mensaje("Error", f"Error al guardar: {e}", error=True)

    # def eliminar_vehiculo(self):
    #     datos = self.view.obtener_datos_formulario()
    #     idv = datos["id_vehiculo"]
    #     if not idv:
    #         self.view.mostrar_mensaje("Error", "Seleccione un vehículo.", error=True)
    #         return

    #     if self.view.mostrar_mensaje("Confirmar", "¿Dar de baja este vehículo?", confirm=True):
    #         vehiculo = self.modelo.buscar_por_id(idv)
    #         if vehiculo and vehiculo.eliminar():
    #             self.view.mostrar_mensaje("Éxito", "Vehículo dado de baja.")
    #             self.limpiar_formulario()
    #             self.cargar_vehiculos()

    # def seleccionar_vehiculo(self, event=None):
    #     sel = self.view.tree.selection()
    #     if not sel:
    #         return

    #     vid = sel[0]
    #     vehiculo = self.modelo.buscar_por_id(vid)
    #     if not vehiculo:
    #         return

    #     foto_tk = None
    #     if vehiculo.foto_path:
    #         try:
    #             ruta_absoluta = os.path.abspath(os.path.join(BASE_DIR, "..", "..", vehiculo.foto_path))
    #             img = Image.open(ruta_absoluta)
    #             img.thumbnail(FOTO_PREVIEW_SIZE)
    #             foto_tk = ImageTk.PhotoImage(img)
    #         except:
    #             pass

    #     self.view.seleccionar_item_en_formulario(vehiculo, foto_tk)
    
    def eliminar_vehiculo(self):
        datos = self.view.obtener_datos_formulario()
        idv = datos["id_vehiculo"]
        if not idv:
            self.view.mostrar_mensaje("Error", "Seleccione un vehículo.", error=True)
            return

        if self.view.mostrar_mensaje("Confirmar", "¿Dar de baja este vehículo?", confirm=True):
            vehiculo = self.modelo.filtrar_por_id(idv)
            if vehiculo and vehiculo.eliminar():
                self.view.mostrar_mensaje("Éxito", "Vehículo dado de baja.")
                self.limpiar_formulario()
                self.cargar_vehiculos()
            else:
                self.view.mostrar_mensaje("Error", "Error al dar de baja el vehículo.", error=True)

    # def seleccionar_vehiculo(self, event=None):
    #     sel = self.view.tree.selection()
    #     if not sel:
    #         return
    #     vid = sel[0]
    #     vehiculo = self.modelo.filtrar_por_id(vid)
    #     if not vehiculo:
    #         return
    #     self.vehiculo_seleccionado = vehiculo 

    #     foto_tk = None
    #     if vehiculo.foto_path:
    #         try:
    #             ruta_absoluta = os.path.abspath(os.path.join(BASE_DIR, "..", "..", vehiculo.foto_path))
    #             img = Image.open(ruta_absoluta)
    #             img.thumbnail(FOTO_PREVIEW_SIZE)
    #             foto_tk = ImageTk.PhotoImage(img)
    #         except Exception:
    #             pass
    #     self.view.seleccionar_item_en_formulario(vehiculo, foto_tk) #VISTA
    def seleccionar_vehiculo(self, event=None):
        sel = self.view.tree.selection()
        if not sel:
            return
        vid = sel[0]
        vehiculo = self.modelo.filtrar_por_id(vid)
        if not vehiculo:
            return
        categoria_nombre = vehiculo.categoria.nombre if vehiculo.categoria else ""
        precio_dia = vehiculo.categoria.precio_dia if vehiculo.categoria else 0
        estado_nombre = vehiculo.estado.nombre_estado()
        vehiculo.categoria_nombre = categoria_nombre
        vehiculo.precio_dia = precio_dia
        vehiculo.estado_nombre = estado_nombre
        
        self.vehiculo_seleccionado = vehiculo

        foto_tk = None
        if vehiculo.foto_path:
            try:
                ruta_absoluta = os.path.abspath(os.path.join(BASE_DIR, "..", "..", vehiculo.foto_path))
                img = Image.open(ruta_absoluta)
                img.thumbnail(FOTO_PREVIEW_SIZE)
                foto_tk = ImageTk.PhotoImage(img)
            except Exception:
                pass

        self.view.seleccionar_item_en_formulario(vehiculo, foto_tk)

    def _copiar_foto(self, origen, patente):
        _, ext = os.path.splitext(origen)
        nombre = f"{patente.replace(' ', '_')}{ext}"
        destino = os.path.join(DESTINO_FOTOS, nombre)
        shutil.copy(origen, destino)
        return os.path.join("frontend", "assets", "vehiculos", nombre)

    def _eliminar_foto_antigua(self, antigua, nueva):
        if not antigua or antigua == nueva:
            return
        try:
            ruta = os.path.abspath(os.path.join(BASE_DIR, "..", "..", antigua))
            if os.path.exists(ruta):
                os.remove(ruta)
        except:
            pass

    def limpiar_formulario(self):
        self.view.limpiar_formulario()

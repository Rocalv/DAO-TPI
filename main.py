import tkinter as tk
from tkinter import ttk, font
import os
import glob

try:
    from PIL import Image, ImageTk
except ImportError:
    print("Error: Se necesita la librería Pillow. Ejecuta: py -m pip install pillow")
    exit()

# --- IMPORTS DE CONTROLADORES ---
from frontend.controller.empleado_controller import EmpleadoController
from frontend.controller.alquiler_controller import AlquilerController
from frontend.controller.cliente_controller import ClienteController
from frontend.controller.consultar_mantenimiento_controller import ConsultarMantenimientoController
from frontend.controller.historial_mantenimiento_controller import HistorialMantenimientoController
from frontend.controller.vehiculo_controller import VehiculoController

from persistencia.crear_tablas import crear_tablas, insertar_datos_prueba

BG_COLOR = "#212121"
FG_COLOR = "white"


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Alquiler de Vehículos")
        self.geometry("1200x800") 
        
        self.config(bg=BG_COLOR)
        
        base_path = os.path.dirname(__file__)
        self.image_path = os.path.join(base_path, "frontend", "assets", "images")
        self.all_images = [] 
        self.current_image_index = 0
        self.carousel_labels = []
        
        self.inicializar_db()
        
        self.main_container = tk.Frame(self, bg=BG_COLOR)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.frames = {}
        self.controllers = {}
        
        self.crear_menu()
        self.crear_vistas()
        self.mostrar_frame("Home")

    def get_controller(self, nombre_vista):
        """Permite a un controlador obtener acceso a otro."""
        return self.controllers.get(nombre_vista)

    def crear_menu(self):
        """Crea la barra de menú superior de la aplicación."""
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
        archivo_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Inicio", command=lambda: self.mostrar_frame("Home"))
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.quit)

        trans_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Transacciones", menu=trans_menu)
        trans_menu.add_command(label="Registrar Alquiler / Reserva", command=lambda: self.mostrar_frame("Alquiler"))

        gestion_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Gestión", menu=gestion_menu)
        gestion_menu.add_command(label="Gestionar Clientes", command=lambda: self.mostrar_frame("Clientes"))
        gestion_menu.add_command(label="Gestionar Empleados", command=lambda: self.mostrar_frame("Empleados"))
        gestion_menu.add_command(label="Gestionar Vehículos", command=lambda: self.mostrar_frame("Vehiculos"))

        mantenimiento_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Mantenimiento", menu=mantenimiento_menu)
        mantenimiento_menu.add_command(label="Registrar Mantenimiento", command=lambda: self.mostrar_frame("RegistrarMantenimiento"))
        mantenimiento_menu.add_command(label="Consultar Pendientes", command=lambda: self.mostrar_frame("ConsultarMantenimiento"))
        mantenimiento_menu.add_command(label="Historial Mantenimientos", command=lambda: self.mostrar_frame("HistorialMantenimiento"))


    def cargar_imagenes_carrusel(self, target_size=(300, 200)):
        """Carga, redimensiona y almacena todas las imágenes de la carpeta."""
        search_path = os.path.join(self.image_path, "*.*")
        image_files = [f for f in glob.glob(search_path) if f.endswith((".jpg", ".jpeg", ".png"))]
        if not image_files: print(f"No se encontraron imágenes en: {self.image_path}"); return
        for img_path in image_files:
            try:
                img = Image.open(img_path); img = img.resize(target_size, Image.Resampling.LANCZOS); photo_img = ImageTk.PhotoImage(img)
                self.all_images.append(photo_img)
            except Exception as e: print(f"Error al cargar la imagen {img_path}: {e}")

    def actualizar_carrusel(self):
        """Función recursiva que actualiza las 3 imágenes."""
        if not self.all_images: return
        total_images = len(self.all_images)
        for i in range(3): self.carousel_labels[i].config(image=self.all_images[(self.current_image_index + i) % total_images])
        self.current_image_index = (self.current_image_index + 1) % total_images; self.after(3000, self.actualizar_carrusel)

    def crear_vistas(self):
        # """Crea todas las vistas (frames) y las almacena en self.frames."""
        
        # # --- Vista HOME ---
        home_frame = tk.Frame(self.main_container, bg=BG_COLOR)
        tk.Label(home_frame, text="Gestion alquiler de autos - Grupo 47", font=("Helvetica", 24, "bold"), pady=20, bg=BG_COLOR, fg=FG_COLOR).pack(side="top")
        slogan_text = "Alquiler de autos fácil, a tu manera.\nConectándote con las mejores experiencias a los mejores precios"
        tk.Label(home_frame, text=slogan_text, font=("Helvetica", 14, "italic"), justify="center", bg=BG_COLOR, fg=FG_COLOR).pack(side="top", expand=True, pady=20)
        carousel_frame = tk.Frame(home_frame, pady=20, bg=BG_COLOR); self.cargar_imagenes_carrusel(target_size=(300, 200))
        for i in range(3): label = tk.Label(carousel_frame, borderwidth=2, relief="sunken", bg=BG_COLOR); label.pack(side="left", padx=10, pady=10); self.carousel_labels.append(label)
        if self.all_images: self.actualizar_carrusel()
        carousel_frame.pack(side="bottom"); self.frames["Home"] = home_frame
        
        # --- VISTA ALQUILER/RESERVA ---
        alquiler_container = tk.Frame(self.main_container, bg=BG_COLOR)
        alquiler_controller = AlquilerController(alquiler_container, self)
        alquiler_view = alquiler_controller.view
        alquiler_view.create_widgets()
        alquiler_controller.inicializar_vista()
        alquiler_view.pack(fill="both", expand=True)
        self.frames["Alquiler"] = alquiler_container
        self.controllers["Alquiler"] = alquiler_controller
        
        
        # # --- Vista GESTIÓN DE CLIENTES ---        
        cliente_container_frame = tk.Frame(self.main_container, bg=BG_COLOR)
        cliente_controller = ClienteController(cliente_container_frame)
        cliente_view = cliente_controller.view
        cliente_view.create_widgets()
        cliente_controller.cargar_empleados()
        cliente_view.pack(fill="both", expand=True)
        self.frames["Clientes"] = cliente_container_frame
        self.controllers["Clientes"] = cliente_controller

        # # --- VISTA CONSULTAR MANTENIMIENTO ---
        cons_manten_container = tk.Frame(self.main_container, bg=BG_COLOR)
        cons_manten_controller = ConsultarMantenimientoController(cons_manten_container, self)
        cons_manten_view = cons_manten_controller.view
        cons_manten_view.create_widgets()
        cons_manten_controller.inicializar_vista()
        cons_manten_view.pack(fill="both", expand=True)
        self.frames["ConsultarMantenimiento"] = cons_manten_container
        self.controllers["ConsultarMantenimiento"] = cons_manten_controller

        # --- GESTIÓN DE EMPLEADOS ---
        empleado_container_frame = tk.Frame(self.main_container, bg=BG_COLOR)
        empleado_controller = EmpleadoController(empleado_container_frame)
        empleado_view = empleado_controller.view
        empleado_view.create_widgets()
        empleado_controller.cargar_empleados()
        empleado_view.pack(fill="both", expand=True)
        self.frames["Empleados"] = empleado_container_frame
        self.controllers["Empleados"] = empleado_controller
        
        # # --- VISTA HISTORIAL MANTENIMIENTO ---
        hist_manten_container = tk.Frame(self.main_container, bg=BG_COLOR)
        hist_manten_controller = HistorialMantenimientoController(hist_manten_container, self)
        hist_manten_view = hist_manten_controller.view
        hist_manten_view.create_widgets()
        hist_manten_controller.inicializar_vista()
        hist_manten_view.pack(fill="both", expand=True)
        self.frames["HistorialMantenimiento"] = hist_manten_container
        self.controllers["HistorialMantenimiento"] = hist_manten_controller

        
        # # --- VISTA REGISTRAR MANTENIMIENTO ---        
        reg_manten_container = tk.Frame(self.main_container, bg=BG_COLOR)
        mantenimiento_controller = HistorialMantenimientoController(reg_manten_container, self)
        mantenimiento_view = mantenimiento_controller.view
        mantenimiento_view.create_widgets()
        mantenimiento_controller.inicializar_vista()
        mantenimiento_view.pack(fill="both", expand=True)
        self.frames["RegistrarMantenimiento"] = reg_manten_container
        self.controllers["RegistrarMantenimiento"] = mantenimiento_controller
        
        # # --- VISTA VEHÍCULOS ---        
        vehiculo_container_frame = tk.Frame(self.main_container, bg=BG_COLOR)
        vehiculo_controller = HistorialMantenimientoController(vehiculo_container_frame, self)
        vehiculo_view = vehiculo_controller.view
        vehiculo_view.create_widgets()
        vehiculo_controller.inicializar_vista()
        vehiculo_view.pack(fill="both", expand=True)
        self.frames["Vehiculos"] = vehiculo_container_frame
        self.controllers["Vehiculos"] = vehiculo_controller
        

    def mostrar_frame(self, nombre_frame):
        """Oculta todas las ventanas y muestra solo la solicitada."""
        for frame in self.frames.values():
            frame.pack_forget()
        frame = self.frames[nombre_frame]
        frame.pack(fill="both", expand=True)
        
        # --- LÓGICA DE RECARGA DE DATOS (SOLUCIÓN AL BUG) ---
        try:
            # Buscamos el controlador asociado a la vista que queremos mostrar
            if nombre_frame in self.controllers:
                controller = self.controllers[nombre_frame]
                
                # Definimos qué función 'recargar' llamar para cada vista
                if nombre_frame == "Alquiler":
                    controller.inicializar_vista()
                elif nombre_frame == "Clientes":
                    controller.cargar_clientes()
                elif nombre_frame == "Empleados":
                    controller.cargar_empleados()
                elif nombre_frame == "Vehiculos":
                    controller.cargar_vehiculos()
                elif nombre_frame == "RegistrarMantenimiento":
                    controller.inicializar_vista()
                elif nombre_frame in ("ConsultarMantenimiento", "HistorialMantenimiento"):
                    controller.cargar_datos()
                    
        except Exception as e:
            print(f"Error al recargar vista {nombre_frame}: {e}")

    def inicializar_db(self):
        """Asegura que las tablas estén creadas."""
        try:
            print("Inicializando base de datos...")
            crear_tablas()
            #insertar_datos_prueba() 
            print("Base de datos lista.")
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
            self.destroy() 

if __name__ == "__main__":
    app = Application()
    app.mainloop()
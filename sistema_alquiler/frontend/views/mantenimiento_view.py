# frontend/views/mantenimiento_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk 
from typing import List 
from sistema_alquiler.backend.models.vehiculo import Vehiculo

BG_COLOR, FG_COLOR = "#212121", "white"
ENTRY_BG, ENTRY_FG = "#333333", "white"
BTN_BG, BTN_FG = "#424242", "white"
TREE_BG, TREE_FG, TREE_SEL = "#2a2a2a", "white", "#0078d4"

class RegistrarMantenimientoView(tk.Frame):
    
    def __init__(self, parent, controller):
        """Inicializa la vista para Registrar Mantenimiento."""
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        
        self.categorias_map = {}
        self.servicios_map = {}
        self.id_vehiculo_seleccionado = tk.StringVar()

        self._configurar_estilos()
        # ¡self.create_widgets() NO se llama aquí! Se llama desde main.py
        
    def _configurar_estilos(self):
        """Configura los estilos oscuros para el Treeview."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=TREE_BG, foreground=TREE_FG, fieldbackground=TREE_BG, borderwidth=0)
        style.map('Treeview', background=[('selected', TREE_SEL)])
        style.configure("Treeview.Heading", background="#555555", foreground="white", font=('Helvetica', 9, 'bold'))
        # Este estilo ya no es necesario
        # style.configure("Seccion.TLabel", font=('Helvetica', 12, 'bold'), background=BG_COLOR, foreground=FG_COLOR)
        
    def create_widgets(self):
        """Crea todos los widgets de la interfaz de cliente."""
        
        # --- 1. Frame de FILTRO ---
        filtro_frame = tk.Frame(self, bg=BG_COLOR, pady=10)
        filtro_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.filtro_patente_var = tk.StringVar()
        self.filtro_categoria_var = tk.StringVar()

        tk.Label(filtro_frame, text="Patente:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e", padx=5)
        tk.Entry(filtro_frame, textvariable=self.filtro_patente_var, width=15, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR).grid(row=0, column=1, padx=5)
        
        tk.Label(filtro_frame, text="Categoría:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, sticky="e", padx=5)
        self.combo_cat_filtro = ttk.Combobox(filtro_frame, textvariable=self.filtro_categoria_var, state="readonly", width=25)
        self.combo_cat_filtro.grid(row=0, column=3, padx=5)
        
        tk.Button(filtro_frame, text="Filtrar", command=self.controller.buscar_vehiculos, bg=BTN_BG, fg=BTN_FG).grid(row=0, column=4, padx=20)
        
        # --- 2. Frame de TABLA DE VEHÍCULOS ---
        tabla_frame = tk.Frame(self, bg=BG_COLOR)
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=0)
        
        scrollbar = ttk.Scrollbar(tabla_frame)
        scrollbar.pack(side="right", fill="y")
        
        cols = ("Patente", "Marca", "Modelo", "Categoría", "Kilometraje")
        self.tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8, yscrollcommand=scrollbar.set)
        for col in cols: self.tree.heading(col, text=col)
        self.tree.column("Patente", width=100); self.tree.column("Marca", width=120); self.tree.column("Modelo", width=120)
        self.tree.column("Categoría", width=150); self.tree.column("Kilometraje", width=100, anchor="e")
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.bind("<<TreeviewSelect>>", self.controller.seleccionar_vehiculo)

        # --- 3. Frame de FORMULARIO DE MANTENIMIENTO ---
        self.form_frame = tk.Frame(self, bg=BG_COLOR, pady=10)
        # Se empaqueta (pack) cuando el usuario selecciona un item
        
        self.form_patente_var = tk.StringVar(value="N/A")
        self.form_modelo_var = tk.StringVar()
        self.form_km_var = tk.StringVar()
        self.form_estado_var = tk.StringVar()
        self.form_servicio_var = tk.StringVar()
        self.form_proveedor_var = tk.StringVar()

        tk.Label(self.form_frame, text="Vehículo:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e", padx=5, pady=2)
        tk.Entry(self.form_frame, textvariable=self.form_patente_var, width=20, state="disabled", disabledbackground=ENTRY_BG, disabledforeground=ENTRY_FG).grid(row=0, column=1, padx=5, pady=2)
        tk.Entry(self.form_frame, textvariable=self.form_modelo_var, width=30, state="disabled", disabledbackground=ENTRY_BG, disabledforeground=ENTRY_FG).grid(row=0, column=2, padx=5, pady=2)
        
        tk.Label(self.form_frame, text="Kilometraje Actual:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e", padx=5, pady=2)
        tk.Entry(self.form_frame, textvariable=self.form_km_var, width=20, state="disabled", disabledbackground=ENTRY_BG, disabledforeground=ENTRY_FG).grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(self.form_frame, text="Servicio a Realizar:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=3, sticky="e", padx=5, pady=2)
        self.combo_servicios = ttk.Combobox(self.form_frame, textvariable=self.form_servicio_var, state="readonly", width=30)
        self.combo_servicios.grid(row=0, column=4, padx=5, pady=2)

        tk.Label(self.form_frame, text="Proveedor:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=3, sticky="e", padx=5, pady=2)
        tk.Entry(self.form_frame, textvariable=self.form_proveedor_var, width=32, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR).grid(row=1, column=4, padx=5, pady=2)
        
        tk.Label(self.form_frame, text="Descripción:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.form_desc_entry = tk.Entry(self.form_frame, width=54, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR)
        self.form_desc_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=2)
        
        tk.Button(self.form_frame, text="Registrar Mantenimiento", command=self.controller.registrar_mantenimiento, bg=BTN_BG, fg=BTN_FG, height=2).grid(row=0, column=5, rowspan=3, padx=20, sticky="ns")
        
        self.form_frame.grid_columnconfigure(0, weight=1)
        self.form_frame.grid_columnconfigure(5, weight=1)


    def set_categorias_combobox(self, categorias: list):
        """Carga el combobox de filtro de categorías."""
        self.categorias_map = {c['nombre']: c['id_categoria'] for c in categorias}
        self.combo_cat_filtro['values'] = ["Todas"] + list(self.categorias_map.keys())
        self.combo_cat_filtro.set("Todas")

    def set_servicios_combobox(self, servicios: list):
        """Carga el combobox de formulario de servicios."""
        self.servicios_map = {s['nombre']: s['id_servicio'] for s in servicios}
        self.combo_servicios['values'] = list(self.servicios_map.keys())

    def actualizar_tabla_vehiculos(self, vehiculos: List[Vehiculo]):
        """Limpia y recarga la grilla de vehículos."""
        for row in self.tree.get_children(): self.tree.delete(row)
        for v in vehiculos:
            self.tree.insert("", "end", iid=v.id_vehiculo, values=(
                v.patente, v.marca, v.modelo, v.categoria_nombre, v.kilometraje
            ))

    def obtener_datos_filtro(self) -> dict:
        """Obtiene los datos del formulario de filtro."""
        nombre_cat = self.filtro_categoria_var.get()
        return {
            "patente": self.filtro_patente_var.get(),
            "id_categoria": self.categorias_map.get(nombre_cat) if nombre_cat != "Todas" else None
        }

    def obtener_vehiculo_seleccionado(self) -> dict:
        """Obtiene el ID del vehículo seleccionado en la tabla."""
        selected = self.tree.selection()
        if not selected:
            return None
        return {"id": selected[0]}

    def rellenar_formulario_vehiculo(self, vehiculo: Vehiculo):
        """Rellena el formulario inferior con los datos del vehículo y MUESTRA el formulario."""
        self.id_vehiculo_seleccionado.set(vehiculo.id_vehiculo)
        self.form_patente_var.set(vehiculo.patente)
        self.form_modelo_var.set(f"{vehiculo.marca} {vehiculo.modelo} ({vehiculo.anio})")
        self.form_km_var.set(vehiculo.kilometraje)
        
        self.form_frame.pack(fill="x", padx=10, pady=10)

    def obtener_datos_formulario(self) -> dict:
        """Obtiene los datos del formulario de registro de mantenimiento."""
        nombre_servicio = self.form_servicio_var.get()
        return {
            "id_vehiculo": self.id_vehiculo_seleccionado.get() or None,
            "id_servicio": self.servicios_map.get(nombre_servicio),
            "kilometraje": self.form_km_var.get(),
            "proveedor": self.form_proveedor_var.get(),
            "descripcion": self.form_desc_entry.get()
        }

    def limpiar_filtro(self):
        """Limpia los campos del filtro superior."""
        self.filtro_patente_var.set("")
        self.filtro_categoria_var.set("Todas")
        
    def limpiar_formulario(self):
        """Limpia el formulario inferior y lo OCULTA."""
        self.id_vehiculo_seleccionado.set("")
        self.form_patente_var.set("N/A")
        self.form_modelo_var.set("")
        self.form_km_var.set("")
        self.form_servicio_var.set("")
        self.form_proveedor_var.set("")
        self.form_desc_entry.delete(0, 'end')
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
        
        self.form_frame.pack_forget()

    def mostrar_mensaje(self, t, m, error=False, confirm=False):
        """Mestra un popup de mensaje."""
        if error: messagebox.showerror(t, m)
        elif confirm: return messagebox.askyesno(t, m)
        else: messagebox.showinfo(t, m)
# frontend/views/vehiculo_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from sistema_alquiler.backend.models.vehiculo import Vehiculo
from sistema_alquiler.backend.models.estado_vehiculo import FabricaEstados

BG_COLOR, FG_COLOR = "#212121", "white"
ENTRY_BG, ENTRY_FG = "#333333", "white"
BTN_BG, BTN_FG = "#424242", "white"
TREE_BG, TREE_FG, TREE_SEL = "#2a2a2a", "white", "#0078d4"

class VehiculoView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self._configurar_estilos()
        self.categorias_map = {}
        self.estados_map = {}

    def _configurar_estilos(self):
        """Configura los estilos oscuros para el Treeview."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=TREE_BG, foreground=TREE_FG, fieldbackground=TREE_BG, borderwidth=0)
        style.map('Treeview', background=[('selected', TREE_SEL)])
        style.configure("Treeview.Heading", background="#555555", foreground="white", font=('Helvetica', 9, 'bold'))

    def create_widgets(self):
        """Crea los widgets de la interfaz de vehículos."""
        form_frame = tk.Frame(self, padx=10, pady=10, bg=BG_COLOR)
        form_frame.pack()

        self.id_var = tk.StringVar()
        self.patente_var = tk.StringVar()
        self.marca_var = tk.StringVar()
        self.modelo_var = tk.StringVar()
        self.anio_var = tk.StringVar()
        self.color_var = tk.StringVar()
        self.km_var = tk.StringVar()
        self.km_mant_var = tk.StringVar(value="10000")
        self.categoria_var = tk.StringVar()
        self.estado_var = tk.StringVar()
        self.foto_path_var = tk.StringVar()
        self.precio_dia_var = tk.StringVar()

        tk.Label(form_frame, text="Patente:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.patente_var, width=30, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Marca:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.marca_var, width=30, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR).grid(row=1, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Modelo:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.modelo_var, width=30, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR).grid(row=2, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Año:", bg=BG_COLOR, fg=FG_COLOR).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.anio_var, width=30, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR).grid(row=3, column=1, padx=5, pady=5)

        form_frame.grid_columnconfigure(2, pad=20)
        tk.Label(form_frame, text="Color:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.color_var, width=30, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR).grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Categoría:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.combo_cat = ttk.Combobox(form_frame, textvariable=self.categoria_var, state="readonly", width=28)
        self.combo_cat.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.combo_cat.bind("<<ComboboxSelected>>", self.controller.on_categoria_changed)

        tk.Label(form_frame, text="Estado:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=2, sticky="e", padx=5, pady=5)
        self.combo_estado = ttk.Combobox(form_frame, textvariable=self.estado_var, state="readonly", width=28)
        self.combo_estado.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Kilometraje:", bg=BG_COLOR, fg=FG_COLOR).grid(row=3, column=2, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.km_var, width=30, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR).grid(row=3, column=3, padx=5, pady=5)

        form_frame.grid_columnconfigure(4, pad=20)
        tk.Label(form_frame, text="Próx. Mant. (Km):", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=4, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.km_mant_var, width=30, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR).grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(form_frame, text="Precio por Día:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=4, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.precio_dia_var, width=30, bg=ENTRY_BG, fg=ENTRY_FG, state="disabled").grid(row=1, column=5, padx=5, pady=5)

        form_frame.grid_columnconfigure(6, pad=30)
        self.preview_lbl = tk.Label(form_frame, bg=ENTRY_BG, text="Sin foto", fg=FG_COLOR, relief="sunken")
        self.preview_lbl.grid(row=0, column=7, rowspan=4, padx=5, pady=5, sticky="ns")
        tk.Button(form_frame, text="Seleccionar Foto...", command=self.controller.seleccionar_foto, bg=BTN_BG, fg=BTN_FG).grid(row=4, column=7, padx=5, pady=5, sticky="ew")

        btn_frame = tk.Frame(self, pady=10, bg=BG_COLOR)
        btn_frame.pack()
        tk.Button(btn_frame, text="Guardar", command=self.controller.guardar_vehiculo, bg=BTN_BG, fg=BTN_FG).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Nuevo", command=self.controller.limpiar_formulario, bg=BTN_BG, fg=BTN_FG).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar (Dar de Baja)", command=self.controller.eliminar_vehiculo, bg=BTN_BG, fg=BTN_FG).pack(side="left", padx=5)

        tree_frame = tk.Frame(self, pady=10)
        tree_frame.pack(fill="both", expand=True, padx=10)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        cols = ("Patente", "Marca", "Modelo", "Año", "Categoría", "Estado", "KM")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", yscrollcommand=scrollbar.set)
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.column("Patente", width=90); self.tree.column("Marca", width=100); self.tree.column("Modelo", width=100); self.tree.column("Año", width=60, anchor="center"); self.tree.column("Categoría", width=150); self.tree.column("Estado", width=90); self.tree.column("KM", width=80, anchor="e")
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        self.tree.bind("<<TreeviewSelect>>", self.controller.seleccionar_vehiculo)

    def actualizar_lista(self, vehiculos):
        """Limpia y recarga la grilla de vehículos."""
        for row in self.tree.get_children(): self.tree.delete(row)
        for v in vehiculos:
            self.tree.insert("", "end", iid=v.id_vehiculo, values=(
                v.patente, v.marca, v.modelo, v.anio, 
                v.categoria_nombre, v.estado_nombre, v.kilometraje
            ))
        min_h, max_h, current_h = 5, 10, len(vehiculos)
        self.tree.config(height=max(min_h, min(current_h, max_h)))

    def set_categorias_combobox(self, categorias: list):
        """Carga el combobox de categorías."""
        self.categorias_map = {c['nombre']: c for c in categorias}
        self.combo_cat['values'] = list(self.categorias_map.keys())

    def set_estados_combobox(self, estados_map: dict):
        """Carga el combobox de estados."""
        self.estados_map = estados_map
        self.combo_estado['values'] = list(self.estados_map.keys())

    def get_estados_map(self) -> dict:
        """Devuelve el mapa de estados al controlador."""
        return FabricaEstados._estados_map_bd

    def obtener_datos_formulario(self):
        """Obtiene los datos del formulario y los devuelve como diccionario."""
        nombre_cat = self.categoria_var.get()
        id_categoria = self.categorias_map.get(nombre_cat, {}).get('id_categoria')
        
        nombre_estado = self.estado_var.get()
        id_estado = FabricaEstados.obtener_id_estado(nombre_estado)
        
        return {
            "id_vehiculo": self.id_var.get() or None,
            "patente": self.patente_var.get(),
            "marca": self.marca_var.get(),
            "modelo": self.modelo_var.get(),
            "anio": self.anio_var.get(),
            "color": self.color_var.get(),
            "kilometraje": self.km_var.get(),
            "km_mantenimiento": self.km_mant_var.get(),
            "id_categoria": id_categoria,
            "id_estado": id_estado,
            "estado_nombre": nombre_estado,
            "foto_path_temporal": self.foto_path_var.get() or None
        }

    def seleccionar_item_en_formulario(self, v: Vehiculo, foto_tk):
        """Rellena el formulario con los datos del vehículo seleccionado."""
        self.id_var.set(v.id_vehiculo)
        self.patente_var.set(v.patente)
        self.marca_var.set(v.marca)
        self.modelo_var.set(v.modelo)
        self.anio_var.set(v.anio)
        self.color_var.set(v.color or "")
        self.km_var.set(v.kilometraje)
        self.km_mant_var.set(v.km_mantenimiento)
        self.categoria_var.set(v.categoria_nombre or "")
        self.estado_var.set(v.estado_nombre or "")
        self.foto_path_var.set("")
        self.actualizar_preview_foto(foto_tk)
        self.actualizar_precio_label(v.precio_dia or 0.0)

    def actualizar_preview_foto(self, foto_tk):
        """Muestra la foto seleccionada en el widget de previsualización."""
        if foto_tk:
            self.preview_lbl.config(image=foto_tk, text="")
            self.preview_lbl.image = foto_tk
        else:
            self.preview_lbl.config(image="", text="Sin foto")
            self.preview_lbl.image = None

    def actualizar_precio_label(self, precio):
        """Actualiza el campo de texto (Entry) del precio."""
        self.precio_dia_var.set(f"${precio:,.2f}")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        for var in [self.id_var, self.patente_var, self.marca_var, self.modelo_var, self.anio_var, self.color_var, self.km_var, self.categoria_var, self.estado_var, self.foto_path_var, self.precio_dia_var]:
            var.set("")
        self.km_mant_var.set("10000")
        self.estado_var.set("disponible")
        self.actualizar_preview_foto(None)
        if self.tree.selection(): self.tree.selection_remove(self.tree.selection())
    
    def mostrar_mensaje(self, t, m, error=False, confirm=False):
        """Muestra un popup de mensaje."""
        if error: messagebox.showerror(t, m)
        elif confirm: return messagebox.askyesno(t, m)
        else: messagebox.showinfo(t, m)
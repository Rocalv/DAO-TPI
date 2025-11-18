import tkinter as tk
from tkinter import ttk, messagebox

BG_COLOR, FG_COLOR = "#212121", "white"
ENTRY_BG, ENTRY_FG = "#333333", "white"
BTN_BG, BTN_FG = "#424242", "white"
TREE_BG, TREE_FG, TREE_SEL = "#2a2a2a", "white", "#0078d4"

class VehiculoView(tk.Frame):

    def __init__(self, parent,
                 on_guardar,
                 on_nuevo,
                 on_eliminar,
                 on_seleccionar_foto,
                 on_categoria_changed,
                 on_select_row):
        
        super().__init__(parent, bg=BG_COLOR)

        self.on_guardar = on_guardar
        self.on_nuevo = on_nuevo
        self.on_eliminar = on_eliminar
        self.on_seleccionar_foto = on_seleccionar_foto
        self.on_categoria_changed = on_categoria_changed
        self.on_select_row = on_select_row

        self._configurar_estilos()
        self.categorias_map = {}
        self.estados_map = {}

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=TREE_BG, foreground=TREE_FG, fieldbackground=TREE_BG, borderwidth=0)
        style.map("Treeview", background=[("selected", TREE_SEL)])
        style.configure("Treeview.Heading", background="#555555", foreground="white",
                        font=("Helvetica", 9, "bold"))

    def create_widgets(self):
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



        # Columna 1
        tk.Label(form_frame, text="Patente:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e", pady=5)
        tk.Entry(form_frame, textvariable=self.patente_var, width=30,
                 bg=ENTRY_BG, fg=ENTRY_FG).grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Marca:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e", pady=5)
        tk.Entry(form_frame, textvariable=self.marca_var, width=30,
                 bg=ENTRY_BG, fg=ENTRY_FG).grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Modelo:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="e", pady=5)
        tk.Entry(form_frame, textvariable=self.modelo_var, width=30,
                 bg=ENTRY_BG, fg=ENTRY_FG).grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Año:", bg=BG_COLOR, fg=FG_COLOR).grid(row=3, column=0, sticky="e", pady=5)
        tk.Entry(form_frame, textvariable=self.anio_var, width=30,
                 bg=ENTRY_BG, fg=ENTRY_FG).grid(row=3, column=1, pady=5)

        # Columna 2
        form_frame.grid_columnconfigure(2, pad=30)

        tk.Label(form_frame, text="Color:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, sticky="e")
        tk.Entry(form_frame, textvariable=self.color_var, width=30,
                 bg=ENTRY_BG, fg=ENTRY_FG).grid(row=0, column=3)

        tk.Label(form_frame, text="Categoría:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=2, sticky="e")
        self.combo_cat = ttk.Combobox(form_frame, textvariable=self.categoria_var, state="readonly", width=28)
        self.combo_cat.grid(row=1, column=3)
        self.combo_cat.bind("<<ComboboxSelected>>", self.on_categoria_changed)

        tk.Label(form_frame, text="Estado:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=2, sticky="e")
        self.combo_estado = ttk.Combobox(form_frame, textvariable=self.estado_var, state="readonly", width=28)
        self.combo_estado.grid(row=2, column=3)

        tk.Label(form_frame, text="Kilometraje:", bg=BG_COLOR, fg=FG_COLOR).grid(row=3, column=2, sticky="e")
        tk.Entry(form_frame, textvariable=self.km_var, width=30,
                 bg=ENTRY_BG, fg=ENTRY_FG).grid(row=3, column=3)

        # Columna 3
        form_frame.grid_columnconfigure(4, pad=30)

        tk.Label(form_frame, text="Próx. Mant. (Km):", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=4, sticky="e")
        tk.Entry(form_frame, textvariable=self.km_mant_var, width=30,
                 bg=ENTRY_BG, fg=ENTRY_FG).grid(row=0, column=5)

        tk.Label(form_frame, text="Precio por Día:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=4, sticky="e")
        tk.Entry(form_frame, textvariable=self.precio_dia_var, width=30,
                 bg=ENTRY_BG, fg=ENTRY_FG, state="disabled").grid(row=1, column=5)

        form_frame.grid_columnconfigure(6, pad=30)

        self.preview_lbl = tk.Label(form_frame, bg=ENTRY_BG, text="Sin foto", fg=FG_COLOR, relief="sunken", width=20, height=6)
        self.preview_lbl.grid(row=0, column=7, rowspan=4, padx=20, pady=10, sticky="nsew")

        tk.Button(form_frame, text="Seleccionar Foto...",
                  command=self.on_seleccionar_foto,
                  bg=BTN_BG, fg=BTN_FG).grid(row=4, column=7, padx=20, pady=5, sticky="nsew")

        form_frame.grid_columnconfigure(7, minsize=230)

        btn_frame = tk.Frame(self, pady=10, bg=BG_COLOR)
        btn_frame.pack()

        tk.Button(btn_frame, text="Guardar", command=self.on_guardar,
                  bg=BTN_BG, fg=BTN_FG).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Nuevo", command=self.on_nuevo,
                  bg=BTN_BG, fg=BTN_FG).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Eliminar (Dar de Baja)", command=self.on_eliminar,
                  bg=BTN_BG, fg=BTN_FG).pack(side="left", padx=5)

        tree_frame = tk.Frame(self, pady=10)
        tree_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        cols = ("Patente", "Marca", "Modelo", "Año", "Categoría", "Estado", "KM")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                                 yscrollcommand=scrollbar.set)

        for col in cols:
            self.tree.heading(col, text=col)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        self.tree.bind("<<TreeviewSelect>>", self.on_select_row)

    def actualizar_lista(self, vehiculos):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for v in vehiculos:
            self.tree.insert("", "end", iid=v.id_vehiculo,
                             values=(v.patente, v.marca, v.modelo, v.anio,
                                     v.categoria_nombre, v.estado_nombre, v.kilometraje))

    def set_categorias_combobox(self, categorias):
        self.categorias_map = {c.nombre: c for c in categorias}
        self.combo_cat["values"] = list(self.categorias_map.keys())

    def set_estados_combobox(self, estados_map):
        self.estados_map = estados_map
        self.combo_estado["values"] = list(estados_map.keys())

    def obtener_datos_formulario(self):
        nombre_cat = self.categoria_var.get()
        
        categoria_obj = self.categorias_map.get(nombre_cat)
        id_categoria = categoria_obj.id_categoria if categoria_obj else None

        estados = {
            "Alquilado": 1,
            "Disponible": 2,
            "FueraServicio": 3,
            "Mantenimiento": 4,
            'Reservado': 5, 
            'ParaMantenimiento': 6
        }

        nombre_estado = self.estado_var.get()
        id_estado = estados.get(nombre_estado)
        def safe_int(valor):
            try:
                return int(valor)
            except (TypeError, ValueError):
                return None
            
        return {
            "id_vehiculo": self.id_var.get() or None,
            "patente": self.patente_var.get(),
            "marca": self.marca_var.get(),
            "modelo": self.modelo_var.get(),
            "anio": self.anio_var.get(),
            "color": self.color_var.get(),
            "kilometraje": self.km_var.get(),
            "km_mantenimiento": self.km_mant_var.get(),
            "nombre_categoria": nombre_cat,
            "id_categoria": id_categoria,
            "id_estado": id_estado,
            "nombre_estado": nombre_estado,
            "foto_path_temporal": self.foto_path_var.get() or None,
        }

    def seleccionar_item_en_formulario(self, v, foto_tk):
        self.id_var.set(v.id_vehiculo)
        self.patente_var.set(v.patente)
        self.marca_var.set(v.marca)
        self.modelo_var.set(v.modelo)
        self.anio_var.set(v.anio)
        self.color_var.set(v.color)
        self.km_var.set(v.kilometraje)
        
        try:
            manteniento = v.km_mantenimiento - v.kilometraje
            if manteniento < 0:
                manteniento = 10000 # Por defecto
            self.km_mant_var.set(str(manteniento))
        except (TypeError, ValueError):
            self.km_mant_var.set("10000")
        
        self.categoria_var.set(v.categoria_nombre)
        self.estado_var.set(v.estado_nombre)
        self.foto_path_var.set("")
        self.actualizar_preview_foto(foto_tk)
        self.actualizar_precio_label(v.precio_dia or 0)

    def actualizar_preview_foto(self, foto_tk):
        if foto_tk:
            self.preview_lbl.config(image=foto_tk, text="")
            self.preview_lbl.image = foto_tk
        else:
            self.preview_lbl.config(image="", text="Sin foto")
            self.preview_lbl.image = None

    def actualizar_precio_label(self, precio):
        self.precio_dia_var.set(f"${precio:,.2f}")

    def limpiar_formulario(self):
        for var in [
            self.id_var, self.patente_var, self.marca_var, self.modelo_var,
            self.anio_var, self.color_var, self.km_var,
            self.categoria_var, self.estado_var,
            self.foto_path_var, self.precio_dia_var
        ]:
            var.set("")
        self.km_mant_var.set("10000")

        self.actualizar_preview_foto(None)

    def validar_formulario(self):
        """Validaciones básicas al intentar guardar"""
        datos = self.obtener_datos_formulario()
        
        # Validar campos obligatorios
        campos_obligatorios = ["patente", "marca", "modelo", "anio", "color", "nombre_categoria", "nombre_estado", "kilometraje"]
        for campo in campos_obligatorios:
            if not datos[campo]:
                self.mostrar_mensaje("Error", f"El campo {campo.replace('_', ' ').title()} es obligatorio", error=True)
                return False
        
        # Validar patente 
        if len(datos["patente"].strip()) < 6:
            self.mostrar_mensaje("Error", "La patente debe tener al menos 6 caracteres", error=True)
            return False
        
        # Validar año (debe ser número y entre valores validos)
        try:
            anio = int(datos["anio"])
            if anio < 2000 or anio > 2030:
                self.mostrar_mensaje("Error", "El año debe ser entre 2000 y 2030", error=True)
                return False
        except ValueError:
            self.mostrar_mensaje("Error", "El año debe ser un número válido", error=True)
            return False
        
        # Validar kilometraje (si se ingresó)
        try:
            kilometraje = int(datos["kilometraje"] or 0)
            if kilometraje < 0:
                self.mostrar_mensaje("Error", "El kilometraje no puede ser negativo", error=True)
                return False
        except ValueError:
            self.mostrar_mensaje("Error", "El kilometraje debe ser un número válido", error=True)
            return False
        
        # Validacion KM mantenimiento
        try:
            km_mantenimiento = int(datos["km_mantenimiento"] or 10000)
            if km_mantenimiento < 0:
                self.mostrar_mensaje("Error", "Los km de mantenimiento debe ser al menos 0", error=True)
                return False

        
        except ValueError:
            self.mostrar_mensaje("Error", "El km de mantenimiento debe ser un número válido", error=True)
            return False
        
                
        # Validar marca y modelo (solo letras, números y espacios)
        def es_texto_valido(texto):
            caracteres_permitidos = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑ0123456789 "
            return all(c in caracteres_permitidos for c in texto)
        
        if not es_texto_valido(datos["marca"]):
            self.mostrar_mensaje("Error", "La marca solo puede contener letras, números y espacios", error=True)
            return False
            
        if not es_texto_valido(datos["modelo"]):
            self.mostrar_mensaje("Error", "El modelo solo puede contener letras, números y espacios", error=True)
            return False
        
        return True    
    
    def mostrar_mensaje(self, t, m, error=False, confirm=False):
        if error:
            messagebox.showerror(t, m)
        elif confirm:
            return messagebox.askyesno(t, m)
        else:
            messagebox.showinfo(t, m)
# frontend/views/mantenimiento_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk
from typing import List

BG_COLOR, FG_COLOR = "#212121", "white"
ENTRY_BG, ENTRY_FG = "#333333", "white"
BTN_BG, BTN_FG = "#424242", "white"
TREE_BG, TREE_FG, TREE_SEL = "#2a2a2a", "white", "#0078d4"

class RegistrarMantenimientoView(tk.Frame):
    
    def __init__(self, parent, on_buscar, on_select, on_registrar):
        super().__init__(parent, bg=BG_COLOR)

        self.on_buscar = on_buscar
        self.on_select = on_select
        self.on_registrar = on_registrar

        self.categorias_map = {}
        self.servicios_map = {}
        self.mecanicos_map = {}

        self.id_vehiculo_seleccionado = tk.StringVar()
        self._configurar_estilos()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=TREE_BG, foreground=TREE_FG, fieldbackground=TREE_BG)
        style.map("Treeview", background=[("selected", TREE_SEL)])
        style.configure("Treeview.Heading", background="#555", foreground="white", font=("Helvetica", 9, "bold"))

    def create_widgets(self):

        filtro = tk.Frame(self, bg=BG_COLOR)
        filtro.pack(fill="x", padx=10, pady=10)

        self.filtro_patente_var = tk.StringVar()
        self.filtro_categoria_var = tk.StringVar()

        tk.Label(filtro, text="Patente:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0)
        tk.Entry(filtro, textvariable=self.filtro_patente_var, bg=ENTRY_BG, fg=ENTRY_FG).grid(row=0, column=1)

        tk.Label(filtro, text="Categoría:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2)
        self.combo_cat_filtro = ttk.Combobox(filtro, textvariable=self.filtro_categoria_var, state="readonly", width=25)
        self.combo_cat_filtro.grid(row=0, column=3, padx=5)

        tk.Button(filtro, text="Filtrar", bg=BTN_BG, fg=BTN_FG, command=self.on_buscar).grid(row=0, column=4, padx=20)

        tabla_frame = tk.Frame(self, bg=BG_COLOR)
        tabla_frame.pack(fill="both", expand=True, padx=10)

        scrollbar = ttk.Scrollbar(tabla_frame)
        scrollbar.pack(side="right", fill="y")

        cols = ("Patente", "Marca", "Modelo", "Categoría", "Kilometraje")
        self.tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", yscrollcommand=scrollbar.set, height=8)

        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.tree.yview)

        self.tree.bind("<<TreeviewSelect>>", lambda e: self.on_select())

        self.form_frame = tk.Frame(self, bg=BG_COLOR, pady=10)

        self.form_patente_var = tk.StringVar(value="N/A")
        self.form_modelo_var = tk.StringVar()
        self.form_km_var = tk.StringVar()
        self.form_proveedor_var = tk.StringVar()
        self.form_servicio_var = tk.StringVar()
        self.form_mecanico_var = tk.StringVar()

        tk.Label(self.form_frame, text="Vehículo:", bg=BG_COLOR, fg=FG_COLOR)\
            .grid(row=0, column=0, sticky="e")
        tk.Entry(self.form_frame, textvariable=self.form_patente_var, width=15,
                 state="disabled", disabledbackground=ENTRY_BG,
                 disabledforeground=ENTRY_FG).grid(row=0, column=1, padx=5)

        tk.Entry(self.form_frame, textvariable=self.form_modelo_var, width=25,
                 state="disabled", disabledbackground=ENTRY_BG,
                 disabledforeground=ENTRY_FG).grid(row=0, column=2, padx=5)

        tk.Label(self.form_frame, text="Kilometraje:", bg=BG_COLOR, fg=FG_COLOR)\
            .grid(row=1, column=0, sticky="e")
        tk.Entry(self.form_frame, textvariable=self.form_km_var, width=15,
                 state="disabled", disabledbackground=ENTRY_BG,
                 disabledforeground=ENTRY_FG).grid(row=1, column=1, padx=5)

        tk.Label(self.form_frame, text="Mecánico:", bg=BG_COLOR, fg=FG_COLOR)\
            .grid(row=2, column=0, sticky="e")
        self.combo_mecanicos = ttk.Combobox(self.form_frame, textvariable=self.form_mecanico_var, state="readonly", width=40)
        self.combo_mecanicos.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        tk.Label(self.form_frame, text="Servicio:", bg=BG_COLOR, fg=FG_COLOR)\
            .grid(row=0, column=3, sticky="e")
        self.combo_servicios = ttk.Combobox(self.form_frame, textvariable=self.form_servicio_var, state="readonly", width=25)
        self.combo_servicios.grid(row=0, column=4, padx=5)

        tk.Label(self.form_frame, text="Proveedor:", bg=BG_COLOR, fg=FG_COLOR)\
            .grid(row=1, column=3, sticky="e")
        tk.Entry(self.form_frame, textvariable=self.form_proveedor_var, bg=ENTRY_BG, fg=ENTRY_FG)\
            .grid(row=1, column=4, padx=5)

        tk.Label(self.form_frame, text="Descripción:", bg=BG_COLOR, fg=FG_COLOR)\
            .grid(row=3, column=0, sticky="e")
        self.form_desc_entry = tk.Entry(self.form_frame, bg=ENTRY_BG, fg=ENTRY_FG)
        self.form_desc_entry.grid(row=3, column=1, columnspan=4, sticky="ew", padx=5)

        tk.Button(self.form_frame, text="Registrar Mantenimiento",
                  command=self.on_registrar, bg=BTN_BG, fg=BTN_FG, height=2)\
            .grid(row=0, column=5, rowspan=4, padx=20, sticky="ns")

    def set_categorias_combobox(self, categorias):
        self.categorias_map = {c["nombre"]: c["id_categoria"] for c in categorias}
        self.combo_cat_filtro["values"] = ["Todas"] + list(self.categorias_map.keys())
        self.combo_cat_filtro.set("Todas")

    def set_servicios_combobox(self, servicios):
        self.servicios_map = {s["nombre"]: s["id_servicio"] for s in servicios}
        self.combo_servicios["values"] = list(self.servicios_map.keys())

    def set_mecanicos_combobox(self, mecanicos):
        self.mecanicos_map = {f"{m.apellido}, {m.nombre}": m.id_empleado for m in mecanicos}
        self.combo_mecanicos["values"] = list(self.mecanicos_map.keys())

    def actualizar_tabla_vehiculos(self, vehiculos):
        self.tree.delete(*self.tree.get_children())
        for v in vehiculos:
            self.tree.insert("", "end", iid=v.id_vehiculo,
                             values=(v.patente, v.marca, v.modelo, v.categoria_nombre, v.kilometraje))

    def obtener_datos_filtro(self):
        nombre_cat = self.filtro_categoria_var.get()
        return {
            "patente": self.filtro_patente_var.get(),
            "id_categoria": self.categorias_map.get(nombre_cat) if nombre_cat != "Todas" else None
        }

    def obtener_vehiculo_seleccionado(self):
        selected = self.tree.selection()
        if not selected:
            return None
        return {"id": selected[0]}

    def rellenar_formulario_vehiculo(self, vehiculo):
        self.id_vehiculo_seleccionado.set(vehiculo.id_vehiculo)
        self.form_patente_var.set(vehiculo.patente)
        self.form_modelo_var.set(f"{vehiculo.marca} {vehiculo.modelo} ({vehiculo.anio})")
        self.form_km_var.set(vehiculo.kilometraje)

        self.form_frame.pack(pady=10)

    def obtener_datos_formulario(self):
        return {
            "id_vehiculo": self.id_vehiculo_seleccionado.get(),
            "id_servicio": self.servicios_map.get(self.form_servicio_var.get()),
            "id_empleado": self.mecanicos_map.get(self.form_mecanico_var.get()),
            "kilometraje": self.form_km_var.get(),
            "proveedor": self.form_proveedor_var.get(),
            "descripcion": self.form_desc_entry.get()
        }

    def limpiar_filtro(self):
        self.filtro_patente_var.set("")
        self.filtro_categoria_var.set("Todas")

    def limpiar_formulario(self):
        self.id_vehiculo_seleccionado.set("")
        self.form_patente_var.set("N/A")
        self.form_modelo_var.set("")
        self.form_km_var.set("")
        self.form_servicio_var.set("")
        self.form_proveedor_var.set("")
        self.form_mecanico_var.set("")
        self.form_desc_entry.delete(0, tk.END)

        self.form_frame.pack_forget()

    def mostrar_mensaje(self, t, m, error=False, confirm=False):
        if error:
            messagebox.showerror(t, m)
        elif confirm:
            return messagebox.askyesno(t, m)
        else:
            messagebox.showinfo(t, m)

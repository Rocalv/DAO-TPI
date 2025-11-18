import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date, datetime, timedelta

BG_COLOR, FG_COLOR = "#212121", "white"
ENTRY_BG, ENTRY_FG = "#333333", "white"
BTN_BG, BTN_FG = "#424242", "white"
TREE_BG, TREE_FG, TREE_SEL = "#2a2a2a", "white", "#0078d4"

class AlquilerView(tk.Frame):
    
    def __init__(
        self,
        parent,
        on_buscar_disponibles,
        on_vehiculo_select,
        on_confirmar_transaccion
    ):
        """Vista de Alquiler/Reserva sin referencia al controlador."""
        super().__init__(parent, bg=BG_COLOR)

        # Guardamos solo los callbacks
        self.on_buscar_disponibles = on_buscar_disponibles
        self.on_vehiculo_select = on_vehiculo_select
        self.on_confirmar_transaccion = on_confirmar_transaccion

        self.categorias_map = {}
        self.clientes_map = {}
        self._configurar_estilos()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=TREE_BG, foreground=TREE_FG,
                        fieldbackground=TREE_BG, borderwidth=0)
        style.map('Treeview', background=[('selected', TREE_SEL)])
        style.configure("Treeview.Heading", background="#555555",
                        foreground="white", font=('Helvetica', 9, 'bold'))

    def create_widgets(self):
        self.main_pane = tk.PanedWindow(self, orient="horizontal",
                                        sashrelief="sunken", bg=BG_COLOR)
        self.main_pane.pack(fill="both", expand=True)

        self.left_pane = tk.Frame(self.main_pane, bg=BG_COLOR)
        self.main_pane.add(self.left_pane, width=450, stretch="never")

        self.right_pane = tk.Frame(self.main_pane, bg=BG_COLOR,
                                   relief="sunken", borderwidth=1)
        self.main_pane.add(self.right_pane, stretch="always")
        
        self._crear_panel_izquierdo()
        self._crear_panel_derecho()

    def _crear_panel_izquierdo(self):
        filtro_frame = tk.Frame(self.left_pane, bg=BG_COLOR, pady=10)
        filtro_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        fecha_inicio = date.today()
        fecha_fin = fecha_inicio + timedelta(days=1)
        
        self.filtro_fecha_inicio_var = tk.StringVar()
        self.filtro_fecha_fin_var = tk.StringVar()
        self.filtro_categoria_var = tk.StringVar()
        self.filtro_marca_var = tk.StringVar()
        
        # Campos de filtro
        tk.Label(filtro_frame, text="Fecha Inicio:", bg=BG_COLOR, fg=FG_COLOR)\
          .grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.date_inicio = DateEntry(filtro_frame,
                                     textvariable=self.filtro_fecha_inicio_var,
                                     date_pattern='yyyy-mm-dd',
                                     width=12, state="readonly")
        self.date_inicio.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(filtro_frame, text="Fecha Fin:", bg=BG_COLOR, fg=FG_COLOR)\
          .grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.date_fin = DateEntry(filtro_frame,
                                  textvariable=self.filtro_fecha_fin_var,
                                  date_pattern='yyyy-mm-dd',
                                  width=12, state="readonly")
        self.date_fin.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(filtro_frame, text="Categoría:", bg=BG_COLOR, fg=FG_COLOR)\
          .grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.combo_cat_filtro = ttk.Combobox(
            filtro_frame, textvariable=self.filtro_categoria_var,
            state="readonly", width=20
        )
        self.combo_cat_filtro.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.date_inicio.set_date(fecha_inicio)
        self.date_fin.set_date(fecha_fin)

        tk.Label(filtro_frame, text="Marca:", bg=BG_COLOR, fg=FG_COLOR)\
          .grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.combo_marca_filtro = ttk.Combobox(
            filtro_frame, 
            textvariable=self.filtro_marca_var,
            state="readonly",  # Hace que sea solo seleccionable
            width=12
        )
        self.combo_marca_filtro.grid(row=1, column=3, padx=5, pady=5)
        
        # Botón buscar
        tk.Button(
            filtro_frame,
            text="Buscar Disponibles",
            command=self.on_buscar_disponibles,
            bg=BTN_BG, fg=BTN_FG
        ).grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")

        # Lista de vehículos
        lista_frame = tk.Frame(self.left_pane, bg=BG_COLOR)
        lista_frame.pack(fill="both", expand=True, padx=10, pady=0)
        
        scrollbar = ttk.Scrollbar(lista_frame)
        scrollbar.pack(side="right", fill="y")
        
        cols = ("Vehículo", "Categoría", "Precio/Día")
        self.tree = ttk.Treeview(lista_frame, columns=cols, show="headings",
                                 height=15, yscrollcommand=scrollbar.set)
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.column("Vehículo", width=200)
        self.tree.column("Categoría", width=150)
        self.tree.column("Precio/Día", width=80, anchor="e")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.tree.yview)

        # Evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.on_vehiculo_select)

    def set_marcas_combobox(self, marcas):
        self.marcas_map = {m: m for m in marcas}  # Simple mapeo de marca a marca
        self.combo_marca_filtro["values"] = ["Todas"] + list(self.marcas_map.keys())
        self.combo_marca_filtro.set("Todas")
    
    def _crear_panel_derecho(self):
        self.detalle_frame = tk.Frame(self.right_pane, bg=BG_COLOR)
        
        self.detalle_cliente_var = tk.StringVar()
        self.detalle_costo_var = tk.StringVar(value="$ 0.00")
        self.detalle_titulo_var = tk.StringVar(value="Seleccione un vehículo")
        self.detalle_subtitulo_var = tk.StringVar()
        self.detalle_tipo_trans_var = tk.StringVar()

        tk.Label(self.detalle_frame, textvariable=self.detalle_titulo_var,
                 bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 16, "bold"))\
            .pack(pady=(10, 0))
        tk.Label(self.detalle_frame, textvariable=self.detalle_subtitulo_var,
                 bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 11)).pack()

        self.preview_lbl = tk.Label(self.detalle_frame, bg=ENTRY_BG,
                                    text="Sin foto", fg=FG_COLOR, relief="sunken")
        self.preview_lbl.pack(pady=10, padx=10, fill="both", expand=True)

        trans_frame = tk.Frame(self.detalle_frame, bg=BG_COLOR)
        trans_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(trans_frame, text="Cliente:", bg=BG_COLOR, fg=FG_COLOR)\
          .grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.combo_cliente = ttk.Combobox(
            trans_frame, textvariable=self.detalle_cliente_var,
            state="readonly", width=40
        )
        self.combo_cliente.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(
            trans_frame, text="COSTO TOTAL (Aprox.):",
            bg=BG_COLOR, fg="#00FF00", font=("Helvetica", 12)
        ).grid(row=1, column=0, sticky="e", padx=5, pady=10)
        tk.Label(
            trans_frame, textvariable=self.detalle_costo_var,
            bg=BG_COLOR, fg="#00FF00", font=("Helvetica", 16, "bold")
        ).grid(row=1, column=1, sticky="w", padx=5, pady=10)
        
        trans_frame.grid_columnconfigure(1, weight=1)

        # Botón confirmar
        self.btn_confirmar = tk.Button(
            self.detalle_frame,
            textvariable=self.detalle_tipo_trans_var,
            command=self.on_confirmar_transaccion,
            bg="#2e7d32", fg="white",
            font=("Helvetica", 12, "bold"), height=2
        )
        self.btn_confirmar.pack(fill="x", padx=10, pady=10, side="bottom")

    def mostrar_mensaje(self, t, m, error=False, confirm=False):
        """Muestra un popup de información, error o confirmación."""
        if error:
            messagebox.showerror(t, m)
        elif confirm:
            return messagebox.askyesno(t, m)
        else:
            messagebox.showinfo(t, m)

    def ocultar_panel_detalle(self):
        """Oculta el frame de detalle y acción del lado derecho."""
        self.detalle_frame.pack_forget()
        self.right_pane.pack_forget()
        self.right_pane.pack(side="right", fill="both", expand=True)
        self.left_pane.pack(side="left", fill="both", expand=True)

    def set_categorias_combobox(self, categorias):
        """Recibe la lista de categorías y configura el combobox."""
        self.categorias_map = {c["nombre"]: c["id_categoria"] for c in categorias}
        self.combo_cat_filtro["values"] = ["Todas"] + list(self.categorias_map.keys())
        self.combo_cat_filtro.set("Todas")

    def set_clientes_combobox(self, clientes):
        """Recibe la lista de clientes y configura el combobox."""
        self.clientes_map = {f"{c['apellido']}, {c['nombre']} ({c['dni']})": c["id_cliente"] for c in clientes}
        self.combo_cliente["values"] = list(self.clientes_map.keys())
        if self.clientes_map:
            self.combo_cliente.set(list(self.clientes_map.keys())[0])

    def obtener_datos_filtro(self):
        nombre_cat = self.filtro_categoria_var.get()
        nombre_marca = self.filtro_marca_var.get()
        return {
            "fecha_inicio": self.filtro_fecha_inicio_var.get(),
            "fecha_fin": self.filtro_fecha_fin_var.get(),
            "id_categoria": self.categorias_map.get(nombre_cat) if nombre_cat != "Todas" else None,
            "marca": nombre_marca if nombre_marca != "Todas" else None
        }

    def actualizar_lista_vehiculos(self, vehiculos):
        """Limpia y rellena la tabla de vehículos disponibles."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for v in vehiculos:
            # Asumiendo que las propiedades categoria_nombre y precio_dia son añadidas por la entidad Vehiculo al crearse.
            # Si no, esto podría fallar, pero se basa en el código del controlador.
            self.tree.insert("", "end", iid=v.id_vehiculo,
                             values=(f"{v.marca} {v.modelo} ({v.patente})",
                                     v.categoria_nombre,
                                     f"${v.precio_dia:,.2f}"))

    def obtener_vehiculo_seleccionado(self):
        """Devuelve el ID del vehículo seleccionado en la tabla."""
        selected = self.tree.selection()
        if not selected: return None
        return int(selected[0])

    def mostrar_panel_detalle(self, vehiculo_obj, costo_total, es_alquiler_hoy, foto_tk):
        """Rellena el panel derecho con los detalles del vehículo y habilita la acción."""
        self.detalle_titulo_var.set(f"{vehiculo_obj.marca} {vehiculo_obj.modelo}")
        # Aseguramos que haya al menos 1 día para evitar división por cero
        dias = max(1, int(costo_total / vehiculo_obj.precio_dia)) if vehiculo_obj.precio_dia else 1
        self.detalle_subtitulo_var.set(f"Patente: {vehiculo_obj.patente} | Días: {dias} | Kilometraje: {vehiculo_obj.kilometraje}")
        self.detalle_costo_var.set(f"${costo_total:,.2f}")
        
        if es_alquiler_hoy:
            self.detalle_tipo_trans_var.set("Confirmar ALQUILER")
        else:
            self.detalle_tipo_trans_var.set("Confirmar RESERVA")
        if foto_tk:
            self.preview_lbl.config(image=foto_tk, text="")
            self.preview_lbl.image = foto_tk
        else:
            self.preview_lbl.config(image="", text="Sin foto")
            self.preview_lbl.image = None

        self.detalle_frame.pack(fill="both", expand=True)
        # Aseguramos que el frame derecho esté visible para que detalle_frame se empaquete dentro.
        self.right_pane.pack(side="right", fill="both", expand=True)

    def obtener_datos_transaccion(self):
        """Devuelve los datos del cliente y costo para la transacción."""
        nombre_cliente_seleccionado = self.detalle_cliente_var.get()
        id_cliente = self.clientes_map.get(nombre_cliente_seleccionado)
        
        return {
            "id_cliente": id_cliente,
        }

    def limpiar_todo(self):
        """Limpia todos los campos y oculta el panel de detalle."""
        fecha_inicio = date.today()
        fecha_fin = fecha_inicio + timedelta(days=1)
        
        self.filtro_fecha_inicio_var.set(fecha_inicio.isoformat())
        self.filtro_fecha_fin_var.set(fecha_fin.isoformat())
        self.filtro_marca_var.set("")
        
        # El combo de categoría debe reestablecerse
        if "Todas" in self.combo_cat_filtro["values"]:
             self.filtro_categoria_var.set("Todas") 
        
        # Limpiar marca
        if hasattr(self, 'combo_marca_filtro') and "Todas" in self.combo_marca_filtro["values"]:
            self.filtro_marca_var.set("Todas")
                
        # Limpiar tabla
        self.tree.delete(*self.tree.get_children())
        
        # Limpiar detalle
        if self.clientes_map:
            self.detalle_cliente_var.set(list(self.clientes_map.keys())[0])
        else:
            self.detalle_cliente_var.set("")
            
        self.detalle_costo_var.set("$ 0.00")
        self.detalle_titulo_var.set("Seleccione un vehículo")
        self.detalle_subtitulo_var.set("")
        self.detalle_tipo_trans_var.set("")
        
        self.ocultar_panel_detalle()
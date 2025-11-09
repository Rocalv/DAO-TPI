# frontend/views/alquiler_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import date
from typing import List, Optional
from sistema_alquiler.backend.models.vehiculo import Vehiculo
from sistema_alquiler.backend.models.cliente import Cliente
from sistema_alquiler.backend.models.categoria import Categoria

BG_COLOR, FG_COLOR = "#212121", "white"
ENTRY_BG, ENTRY_FG = "#333333", "white"
BTN_BG, BTN_FG = "#424242", "white"
TREE_BG, TREE_FG, TREE_SEL = "#2a2a2a", "white", "#0078d4"

class AlquilerView(tk.Frame):
    
    def __init__(self, parent, controller):
        """Inicializa la vista principal de Alquiler/Reserva."""
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        
        self.categorias_map = {}
        self.clientes_map = {}
        self._configurar_estilos()
        
    def _configurar_estilos(self):
        """Configura los estilos oscuros para el Treeview."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=TREE_BG, foreground=TREE_FG, fieldbackground=TREE_BG, borderwidth=0)
        style.map('Treeview', background=[('selected', TREE_SEL)])
        style.configure("Treeview.Heading", background="#555555", foreground="white", font=('Helvetica', 9, 'bold'))

    def create_widgets(self):
        """Crea el layout de 2 paneles (Filtro/Lista y Detalle)."""
        self.main_pane = tk.PanedWindow(self, orient="horizontal", sashrelief="sunken", bg=BG_COLOR)
        self.main_pane.pack(fill="both", expand=True)

        self.left_pane = tk.Frame(self.main_pane, bg=BG_COLOR)
        self.main_pane.add(self.left_pane, width=450, stretch="never")

        self.right_pane = tk.Frame(self.main_pane, bg=BG_COLOR, relief="sunken", borderwidth=1)
        self.main_pane.add(self.right_pane, stretch="always")
        
        self._crear_panel_izquierdo()
        self._crear_panel_derecho()

    def _crear_panel_izquierdo(self):
        """Crea los widgets para el panel de filtros y lista."""
        filtro_frame = tk.Frame(self.left_pane, bg=BG_COLOR, pady=10)
        filtro_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.filtro_fecha_inicio_var = tk.StringVar(value=date.today().isoformat())
        self.filtro_fecha_fin_var = tk.StringVar()
        self.filtro_categoria_var = tk.StringVar()
        self.filtro_marca_var = tk.StringVar()
        
        tk.Label(filtro_frame, text="Fecha Inicio:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.date_inicio = DateEntry(filtro_frame, textvariable=self.filtro_fecha_inicio_var, date_pattern='yyyy-mm-dd', width=12, state="readonly")
        self.date_inicio.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(filtro_frame, text="Fecha Fin:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.date_fin = DateEntry(filtro_frame, textvariable=self.filtro_fecha_fin_var, date_pattern='yyyy-mm-dd', width=12, state="readonly")
        self.date_fin.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(filtro_frame, text="Categoría:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.combo_cat_filtro = ttk.Combobox(filtro_frame, textvariable=self.filtro_categoria_var, state="readonly", width=20)
        self.combo_cat_filtro.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(filtro_frame, text="Marca:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=2, sticky="e", padx=5, pady=5)
        tk.Entry(filtro_frame, textvariable=self.filtro_marca_var, width=14, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR).grid(row=1, column=3, padx=5, pady=5)
        
        tk.Button(filtro_frame, text="Buscar Disponibles", command=self.controller.buscar_disponibles, bg=BTN_BG, fg=BTN_FG).grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")

        lista_frame = tk.Frame(self.left_pane, bg=BG_COLOR)
        lista_frame.pack(fill="both", expand=True, padx=10, pady=0)
        
        scrollbar = ttk.Scrollbar(lista_frame)
        scrollbar.pack(side="right", fill="y")
        
        cols = ("Vehículo", "Categoría", "Precio/Día")
        self.tree = ttk.Treeview(lista_frame, columns=cols, show="headings", height=15, yscrollcommand=scrollbar.set)
        for col in cols: self.tree.heading(col, text=col)
        self.tree.column("Vehículo", width=200); self.tree.column("Categoría", width=150); self.tree.column("Precio/Día", width=80, anchor="e")
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.bind("<<TreeviewSelect>>", self.controller.on_vehiculo_select)

    def _crear_panel_derecho(self):
        """Crea los widgets para el panel de detalle de transacción."""
        self.detalle_frame = tk.Frame(self.right_pane, bg=BG_COLOR)
        
        self.detalle_cliente_var = tk.StringVar()
        self.detalle_costo_var = tk.StringVar(value="$ 0.00")
        self.detalle_titulo_var = tk.StringVar(value="Seleccione un vehículo")
        self.detalle_subtitulo_var = tk.StringVar()
        self.detalle_tipo_trans_var = tk.StringVar()

        tk.Label(self.detalle_frame, textvariable=self.detalle_titulo_var, bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 16, "bold")).pack(pady=(10, 0))
        tk.Label(self.detalle_frame, textvariable=self.detalle_subtitulo_var, bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 11)).pack()

        self.preview_lbl = tk.Label(self.detalle_frame, bg=ENTRY_BG, text="Sin foto", fg=FG_COLOR, relief="sunken")
        self.preview_lbl.pack(pady=10, padx=10, fill="both", expand=True)

        trans_frame = tk.Frame(self.detalle_frame, bg=BG_COLOR)
        trans_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(trans_frame, text="Cliente:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.combo_cliente = ttk.Combobox(trans_frame, textvariable=self.detalle_cliente_var, state="readonly", width=40)
        self.combo_cliente.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(trans_frame, text="COSTO TOTAL (Aprox.):", bg=BG_COLOR, fg="#00FF00", font=("Helvetica", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=10)
        tk.Label(trans_frame, textvariable=self.detalle_costo_var, bg=BG_COLOR, fg="#00FF00", font=("Helvetica", 16, "bold")).grid(row=1, column=1, sticky="w", padx=5, pady=10)
        
        trans_frame.grid_columnconfigure(1, weight=1)

        self.btn_confirmar = tk.Button(self.detalle_frame, textvariable=self.detalle_tipo_trans_var, 
                                       command=self.controller.confirmar_transaccion, 
                                       bg="#2e7d32", fg="white", font=("Helvetica", 12, "bold"), height=2)
        self.btn_confirmar.pack(fill="x", padx=10, pady=10, side="bottom")

    def set_categorias_combobox(self, categorias: list):
        """Carga el combobox de filtro de categorías."""
        self.categorias_map = {c['nombre']: c['id_categoria'] for c in categorias}
        self.combo_cat_filtro['values'] = ["Todas"] + list(self.categorias_map.keys())
        self.combo_cat_filtro.set("Todas")

    def set_clientes_combobox(self, clientes: list):
        """Carga el combobox de formulario de clientes."""
        self.clientes_map = {f"{c['apellido']}, {c['nombre']} (DNI: {c['dni']})": c['id_cliente'] for c in clientes}
        self.combo_cliente['values'] = list(self.clientes_map.keys())

    def actualizar_lista_vehiculos(self, vehiculos: List[Vehiculo]):
        """Limpia y recarga la grilla de vehículos."""
        for row in self.tree.get_children(): self.tree.delete(row)
        for v in vehiculos:
            self.tree.insert("", "end", iid=v.id_vehiculo, values=(
                f"{v.marca} {v.modelo} ({v.patente})", 
                v.categoria_nombre, 
                f"${v.precio_dia:,.2f}"
            ))

    def mostrar_panel_detalle(self, vehiculo: Vehiculo, costo_total: float, es_alquiler_hoy: bool):
        """Rellena y muestra el panel de la derecha."""
        self.detalle_titulo_var.set(f"{vehiculo.marca} {vehiculo.modelo} ({vehiculo.patente})")
        self.detalle_subtitulo_var.set(f"{vehiculo.categoria_nombre} - ${vehiculo.precio_dia:,.2f}/día")
        self.detalle_costo_var.set(f"${costo_total:,.2f}")
        
        if es_alquiler_hoy:
            self.detalle_tipo_trans_var.set("Confirmar ALQUILER INMEDIATO")
        else:
            self.detalle_tipo_trans_var.set("Confirmar RESERVA")
            
        foto_tk = self.cargar_foto_preview(vehiculo.foto_path)
        self.actualizar_preview_foto(foto_tk)
        
        self.detalle_frame.pack(fill="both", expand=True)

    def ocultar_panel_detalle(self):
        """Oculta el panel de la derecha."""
        self.detalle_frame.pack_forget()
        self.limpiar_formulario_detalle()
        
    def limpiar_formulario_detalle(self):
        """Limpia solo el panel de detalle."""
        self.detalle_cliente_var.set("")
        self.detalle_costo_var.set("$ 0.00")
        self.detalle_titulo_var.set("Seleccione un vehículo")
        self.detalle_subtitulo_var.set("")
        self.actualizar_preview_foto(None)

    def limpiar_todo(self):
        """Limpia solo los resultados (lista y panel), NO los filtros."""
        self.actualizar_lista_vehiculos([])
        self.ocultar_panel_detalle()
        
    def actualizar_preview_foto(self, foto_tk):
        """Muestra la foto en el panel de detalle."""
        if foto_tk:
            self.preview_lbl.config(image=foto_tk, text="")
            self.preview_lbl.image = foto_tk
        else:
            self.preview_lbl.config(image="", text="Sin foto")
            self.preview_lbl.image = None
            
    def cargar_foto_preview(self, foto_path):
        """Carga una imagen desde un path y la prepara para la preview."""
        if not foto_path: return None
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__)) 
            base_dir = os.path.dirname(base_dir) 
            ruta_completa = os.path.abspath(os.path.join(base_dir, foto_path))
            
            if os.path.exists(ruta_completa):
                img = Image.open(ruta_completa)
                img_resized = img.resize((350, 250), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img_resized)
        except Exception as e:
            print(f"Error al cargar foto de preview: {e}")
            return None

    def obtener_datos_filtro(self) -> dict:
        """Obtiene los datos del formulario de filtro."""
        nombre_cat = self.filtro_categoria_var.get()
        return {
            "fecha_inicio": self.filtro_fecha_inicio_var.get(),
            "fecha_fin": self.filtro_fecha_fin_var.get(),
            "marca": self.filtro_marca_var.get() or None,
            "id_categoria": self.categorias_map.get(nombre_cat)
        }
        
    def obtener_vehiculo_seleccionado(self) -> Optional[int]:
        """Obtiene el ID del vehículo seleccionado en la tabla."""
        selected = self.tree.selection()
        if not selected:
            return None
        return int(selected[0])

    def obtener_datos_transaccion(self) -> dict:
        """Obtiene los datos del panel de transacción."""
        nombre_cliente = self.detalle_cliente_var.get()
        return {
            "id_cliente": self.clientes_map.get(nombre_cliente),
            "nombre_cliente": nombre_cliente
        }

    def mostrar_mensaje(self, t, m, error=False, confirm=False):
        """Mestra un popup de mensaje."""
        if error: messagebox.showerror(t, m)
        elif confirm: return messagebox.askyesno(t, m)
        else: messagebox.showinfo(t, m)
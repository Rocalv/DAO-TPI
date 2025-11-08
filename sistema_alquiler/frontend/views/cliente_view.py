# frontend/views/cliente_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from sistema_alquiler.frontend.controllers.cliente_controller import ClienteController

# Definición de colores
BG_COLOR = "#212121"
FG_COLOR = "white"
ENTRY_BG_COLOR = "#333333"
ENTRY_FG_COLOR = "white"
BTN_BG_COLOR = "#424242"
BTN_FG_COLOR = "white"

# --- Colores para el Treeview (Modo Oscuro) ---
TREE_BG = "#2a2a2a"
TREE_FG = "white"
TREE_SELECTED = "#0078d4" # Azul para la selección
TREE_HEADING_BG = "#555555"
TREE_HEADING_FG = "white"
TREE_HEADING_ACTIVE = "#6a6a6a"

class ClienteView(tk.Frame):
    
    def __init__(self, parent, controller):
        """Inicializa la vista y aplica el tema oscuro al Treeview."""
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        # --- CAMBIO: Aplicar Estilo Oscuro al Treeview (Grilla) ---
        style = ttk.Style()
        
        # Usar un tema base que podamos sobreescribir
        style.theme_use("default") 
        
        # Configurar colores del cuerpo del Treeview
        style.configure("Treeview", 
                        background=TREE_BG, 
                        foreground=TREE_FG, 
                        fieldbackground=TREE_BG, 
                        bordercolor="#555555",
                        borderwidth=1)
        # Configurar color de la fila seleccionada
        style.map('Treeview', background=[('selected', TREE_SELECTED)])
        
        # Configurar colores de la cabecera (Títulos)
        style.configure("Treeview.Heading", 
                        background=TREE_HEADING_BG, 
                        foreground=TREE_HEADING_FG, 
                        font=('Helvetica', 10, 'bold'))
        # Configurar color de la cabecera al pasar el mouse
        style.map("Treeview.Heading",
            background=[('active', TREE_HEADING_ACTIVE)])
        # --- FIN CAMBIO ---

        
    def create_widgets(self):
        """Crea todos los widgets de la interfaz de cliente."""
        
        # --- Frame del Formulario (Centrado) ---
        form_frame = tk.Frame(self, padx=10, pady=10, bg=BG_COLOR)
        # Usamos .pack() sin 'fill' para que se centre automáticamente
        form_frame.pack() 

        self.id_var = tk.StringVar()
        self.dni_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.activo_var = tk.BooleanVar(value=True)

        # --- Columna 1 ---
        tk.Label(form_frame, text="DNI:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.dni_var, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Nombre:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.nombre_var, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Apellido:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.apellido_var, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=2, column=1, padx=5, pady=5)

        # --- Columna 2 ---
        form_frame.grid_columnconfigure(2, pad=30) 

        tk.Label(form_frame, text="Teléfono:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.telefono_var, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Email:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.email_var, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=1, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Dirección:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.direccion_var, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=2, column=3, padx=5, pady=5)
        
        tk.Checkbutton(form_frame, text="Activo", variable=self.activo_var, bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR, activebackground=BG_COLOR, activeforeground=FG_COLOR).grid(row=3, column=3, padx=5, pady=5, sticky="w")
        
        # --- CAMBIO: Esta línea se eliminó para permitir el centrado ---
        # self.grid_columnconfigure(0, weight=1) 

        # --- Frame de Botones (Centrado) ---
        button_frame = tk.Frame(self, pady=10, bg=BG_COLOR)
        button_frame.pack()

        tk.Button(button_frame, text="Guardar", command=self.controller.guardar_cliente, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(side="left", padx=5)
        tk.Button(button_frame, text="Nuevo", command=self.controller.limpiar_formulario, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(side="left", padx=5)
        tk.Button(button_frame, text="Eliminar (Dar de Baja)", command=self.controller.eliminar_cliente, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(side="left", padx=5)

        # --- CAMBIO: Frame de la grilla AHORA CON SCROLLBAR ---
        tree_container = tk.Frame(self)
        tree_container.pack(fill="both", expand=True, padx=10, pady=(5,10))

        # Crear el Scrollbar
        scrollbar = ttk.Scrollbar(tree_container)
        scrollbar.pack(side="right", fill="y")

        # El alto inicial (min_height) se configura en actualizar_lista
        self.tree = ttk.Treeview(tree_container, 
                                 columns=("DNI", "Nombre", "Apellido", "Teléfono", "Email", "Activo"), 
                                 show="headings", 
                                 yscrollcommand=scrollbar.set) # Conectar al scrollbar
        
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Activo", text="Activo")
        
        self.tree.column("DNI", width=80, anchor="center")
        self.tree.column("Nombre", width=120)
        self.tree.column("Apellido", width=120)
        self.tree.column("Teléfono", width=100)
        self.tree.column("Email", width=150)
        self.tree.column("Activo", width=50, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)
        
        # Configurar el scrollbar para que controle el treeview
        scrollbar.config(command=self.tree.yview)
        # --- FIN CAMBIO SCROLLBAR ---
        
        self.tree.bind("<<TreeviewSelect>>", self.controller.seleccionar_cliente)

    
    def actualizar_lista(self, clientes):
        """Limpia y recarga la grilla (Treeview) con datos y ajusta su altura."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for cli in clientes:
            estado = "Sí" if cli['activo'] else "No"
            self.tree.insert("", "end", 
                             iid=cli['id_cliente'], 
                             values=(cli['dni'], cli['nombre'], cli['apellido'], cli['telefono'], cli['email'], estado))

        # --- CAMBIO: Ajustar altura de la tabla dinámicamente ---
        min_height = 5  # Alto mínimo (en filas)
        max_height = 10 # Alto máximo (en filas)
        
        current_height = len(clientes)
        
        if current_height < min_height:
            display_height = min_height
        elif current_height > max_height:
            display_height = max_height
        else:
            display_height = current_height
            
        self.tree.config(height=display_height)
        # --- FIN CAMBIO ---

    def limpiar_formulario(self):
        """Limpia los campos del formulario."""
        self.id_var.set("")
        self.dni_var.set("")
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.telefono_var.set("")
        self.email_var.set("")
        self.direccion_var.set("")
        self.activo_var.set(True)
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

    def mostrar_mensaje(self, titulo, mensaje, error=False, confirm=False):
        """Muestra un popup de información, error o confirmación."""
        if error:
            messagebox.showerror(titulo, mensaje)
        elif confirm:
            return messagebox.askyesno(titulo, mensaje)
        else:
            messagebox.showinfo(titulo, mensaje)

    def obtener_datos_formulario(self):
        """Devuelve los datos del formulario como un diccionario."""
        return {
            "id_cliente": self.id_var.get() or None,
            "dni": self.dni_var.get(),
            "nombre": self.nombre_var.get(),
            "apellido": self.apellido_var.get(),
            "telefono": self.telefono_var.get(),
            "email": self.email_var.get(),
            "direccion": self.direccion_var.get(),
            "activo": self.activo_var.get()
        }
    
    def seleccionar_item_en_formulario(self, item):
        """Rellena el formulario con los datos del item seleccionado en la grilla."""
        self.id_var.set(item['id_cliente'])
        self.dni_var.set(item['dni'])
        self.nombre_var.set(item['nombre'])
        self.apellido_var.set(item['apellido'])
        self.telefono_var.set(item['telefono'])
        self.email_var.set(item['email'])
        self.direccion_var.set(item['direccion'])
        self.activo_var.set(item['activo'])
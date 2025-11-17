# frontend/views/empleado_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# (Definición de Colores... sin cambios)
BG_COLOR = "#212121"
FG_COLOR = "white"
ENTRY_BG_COLOR = "#333333"
ENTRY_FG_COLOR = "white"
BTN_BG_COLOR = "#424242"
BTN_FG_COLOR = "white"
TREE_BG = "#2a2a2a"
TREE_FG = "white"
TREE_SELECTED = "#0078d4"
TREE_HEADING_BG = "#555555"
TREE_HEADING_FG = "white"
TREE_HEADING_ACTIVE = "#6a6a6a"

class EmpleadoView(tk.Frame):
    
    def __init__(self, parent, on_guardar, on_nuevo, on_eliminar, on_seleccionar_foto, on_select_row):
        super().__init__(parent, bg=BG_COLOR)

        self.on_guardar = on_guardar
        self.on_nuevo = on_nuevo
        self.on_eliminar = on_eliminar
        self.on_seleccionar_foto = on_seleccionar_foto
        self.on_select_row = on_select_row

        style = ttk.Style()
        style.theme_use("default") 
        style.configure("Treeview", 
                        background=TREE_BG, foreground=TREE_FG, 
                        fieldbackground=TREE_BG, bordercolor="#555555",
                        borderwidth=1)
        style.map('Treeview', background=[('selected', TREE_SELECTED)])
        style.configure("Treeview.Heading", 
                        background=TREE_HEADING_BG, foreground=TREE_HEADING_FG, 
                        font=('Helvetica', 10, 'bold'))
        style.map("Treeview.Heading", background=[('active', TREE_HEADING_ACTIVE)])
        
        self.cargos_map = {}
        
    def create_widgets(self):
        """Crea todos los widgets de la interfaz de empleado."""
        form_frame = tk.Frame(self, padx=10, pady=10, bg=BG_COLOR)
        form_frame.pack() 

        self.id_var = tk.StringVar()
        self.dni_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.cargo_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.activo_var = tk.BooleanVar(value=True)
        self.foto_path_var = tk.StringVar()
        
        # Columna 1
        tk.Label(form_frame, text="DNI:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.dni_var, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Nombre:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.nombre_var, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Apellido:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.apellido_var, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=2, column=1, padx=5, pady=5)

        # Columna 2
        form_frame.grid_columnconfigure(2, pad=30) 

        tk.Label(form_frame, text="Cargo:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.cargo_combobox = ttk.Combobox(form_frame, textvariable=self.cargo_var, width=28, state="readonly")
        self.cargo_combobox.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Teléfono:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.telefono_var, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=1, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Email:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.email_var, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=2, column=3, padx=5, pady=5)
        
        tk.Checkbutton(form_frame, text="Activo", variable=self.activo_var, bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR, activebackground=BG_COLOR, activeforeground=FG_COLOR).grid(row=3, column=3, padx=5, pady=5, sticky="w")
        
        # Columna 3 (Foto Preview)
        form_frame.grid_columnconfigure(4, pad=30)
        
        # --- CAMBIO: Se eliminó width=25, height=10 ---
        self.foto_preview_label = tk.Label(form_frame, bg=ENTRY_BG_COLOR, text="Sin foto", fg=FG_COLOR, relief="sunken")
        self.foto_preview_label.grid(row=0, column=5, rowspan=3, padx=5, pady=5)
        
        tk.Button(form_frame, text="Seleccionar Foto...", command=self.on_seleccionar_foto, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).grid(row=3, column=5, padx=5, pady=5, sticky="nsew")

        # Frame de Botones
        button_frame = tk.Frame(self, pady=10, bg=BG_COLOR)
        button_frame.pack()

        tk.Button(button_frame, text="Guardar", command=self.on_guardar, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(side="left", padx=5)
        tk.Button(button_frame, text="Nuevo",  command=self.on_nuevo, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(side="left", padx=5)
        tk.Button(button_frame, text="Eliminar (Dar de Baja)", command=self.on_eliminar, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(side="left", padx=5)

        # Frame de la grilla
        tree_container = tk.Frame(self)
        tree_container.pack(fill="both", expand=True, padx=10, pady=(5,10))
        
        scrollbar = ttk.Scrollbar(tree_container)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(tree_container, 
                                 columns=("DNI", "Nombre", "Apellido", "Cargo", "Teléfono", "Email", "Activo"), 
                                 show="headings", 
                                 yscrollcommand=scrollbar.set)
        
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Activo", text="Activo")
        
        self.tree.column("DNI", width=80, anchor="center")
        self.tree.column("Nombre", width=120)
        self.tree.column("Apellido", width=120)
        self.tree.column("Cargo", width=100)
        self.tree.column("Teléfono", width=100)
        self.tree.column("Email", width=150)
        self.tree.column("Activo", width=50, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select_row)
    
    def actualizar_lista(self, empleados):
        """Limpia y recarga la grilla (Treeview) con datos y ajusta su altura."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for emp in empleados:
            estado = "Sí" if emp.activo else "No"
            self.tree.insert("", "end", 
                             iid=emp.id_empleado, 
                             values=(emp.dni, emp.nombre, emp.apellido, 
                                     emp.cargo.nombre if emp.cargo else "N/A",
                                     emp.telefono, emp.email, estado))
        
        min_height = 5
        max_height = 10
        current_height = len(empleados)
        display_height = max(min_height, min(current_height, max_height))
        self.tree.config(height=display_height)

    def limpiar_formulario(self):
        """Limpia los campos del formulario y la preview de la foto."""
        self.id_var.set("")
        self.dni_var.set("")
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.cargo_var.set("")
        self.telefono_var.set("")
        self.email_var.set("")
        self.activo_var.set(True)
        self.foto_path_var.set("")
        self.foto_preview_label.config(image="", text="Sin foto")
        self.foto_preview_label.image = None
        
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

    def set_cargos_combobox(self, cargos_lista):
        """Recibe la lista de cargos y configura el combobox y el mapa."""
        self.cargos_map = {cargo['nombre']: cargo['id_cargo'] for cargo in cargos_lista}
        self.cargo_combobox['values'] = list(self.cargos_map.keys())

    def obtener_datos_formulario(self):
        """Devuelve los datos del formulario como un diccionario."""
        nombre_cargo = self.cargo_var.get()
        id_cargo = self.cargos_map.get(nombre_cargo)
        
        return {
            "id_empleado": self.id_var.get() or None,
            "dni": self.dni_var.get(),
            "nombre": self.nombre_var.get(),
            "apellido": self.apellido_var.get(),
            "id_cargo": id_cargo,
            "telefono": self.telefono_var.get(),
            "email": self.email_var.get(),
            "activo": self.activo_var.get(),
            "foto_path_temporal": self.foto_path_var.get() or None
        }
    
    def seleccionar_item_en_formulario(self, empleado_obj, foto_tk):
        """Rellena el formulario con los datos del empleado seleccionado."""
        self.id_var.set(empleado_obj.id_empleado)
        self.dni_var.set(empleado_obj.dni)
        self.nombre_var.set(empleado_obj.nombre)
        self.apellido_var.set(empleado_obj.apellido)
        self.cargo_var.set(empleado_obj.cargo.nombre if empleado_obj.cargo else "")
        self.telefono_var.set(empleado_obj.telefono)
        self.email_var.set(empleado_obj.email)
        self.activo_var.set(empleado_obj.activo)
        self.foto_path_var.set("")
        
        if foto_tk:
            self.foto_preview_label.config(image=foto_tk, text="")
            self.foto_preview_label.image = foto_tk
        else:
            self.foto_preview_label.config(image="", text="Sin foto")
            self.foto_preview_label.image = None

    def actualizar_preview_foto(self, foto_tk):
        """Muestra en la vista la foto que el usuario acaba de seleccionar."""
        self.foto_preview_label.config(image=foto_tk, text="")
        self.foto_preview_label.image = foto_tk
import tkinter as tk
from tkinter import ttk, messagebox

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


class ClienteView(tk.Frame):
    
    def __init__(self, parent, on_guardar, on_nuevo, on_eliminar, on_select_row):
        """Inicializa la vista sin referencia al controlador."""
        super().__init__(parent, bg=BG_COLOR)

        self.on_guardar = on_guardar
        self.on_nuevo = on_nuevo
        self.on_eliminar = on_eliminar
        self.on_select_row = on_select_row

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background=TREE_BG,
                        foreground=TREE_FG,
                        fieldbackground=TREE_BG,
                        bordercolor="#555",
                        borderwidth=1)

        style.map('Treeview', background=[('selected', TREE_SELECTED)])

        style.configure("Treeview.Heading",
                        background=TREE_HEADING_BG,
                        foreground=TREE_HEADING_FG,
                        font=('Helvetica', 10, 'bold'))

        style.map("Treeview.Heading",
                  background=[('active', TREE_HEADING_ACTIVE)])

    def create_widgets(self):
        """Crea los widgets de cliente."""

        form_frame = tk.Frame(self, padx=10, pady=10, bg=BG_COLOR)
        form_frame.pack()

        self.id_var = tk.StringVar()
        self.dni_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.activo_var = tk.BooleanVar(value=True)

        tk.Label(form_frame, text="DNI:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.dni_var, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR,
                 insertbackground=FG_COLOR, width=30).grid(row=0, column=1)

        tk.Label(form_frame, text="Nombre:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.nombre_var, width=30, bg=ENTRY_BG_COLOR,
                 fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=1, column=1)

        tk.Label(form_frame, text="Apellido:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.apellido_var, width=30, bg=ENTRY_BG_COLOR,
                 fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=2, column=1)

        tk.Label(form_frame, text="Teléfono:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, sticky="e")
        tk.Entry(form_frame, textvariable=self.telefono_var, width=30, bg=ENTRY_BG_COLOR,
                 fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=0, column=3)

        tk.Label(form_frame, text="Email:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=2, sticky="e")
        tk.Entry(form_frame, textvariable=self.email_var, width=30, bg=ENTRY_BG_COLOR,
                 fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=1, column=3)

        tk.Label(form_frame, text="Dirección:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=2, sticky="e")
        tk.Entry(form_frame, textvariable=self.direccion_var, width=30, bg=ENTRY_BG_COLOR,
                 fg=ENTRY_FG_COLOR, insertbackground=FG_COLOR).grid(row=2, column=3)

        tk.Checkbutton(form_frame, text="Activo", variable=self.activo_var,
                       bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR).grid(row=3, column=3, sticky="w")

        button_frame = tk.Frame(self, pady=10, bg=BG_COLOR)
        button_frame.pack()

        tk.Button(button_frame, text="Guardar", command=self.on_guardar, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(side="left", padx=5)
        tk.Button(button_frame, text="Nuevo", command=self.on_nuevo, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(side="left", padx=5)
        tk.Button(button_frame, text="Eliminar (Dar de Baja)", command=self.on_eliminar, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(side="left", padx=5)

        tree_container = tk.Frame(self)
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(tree_container)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            tree_container,
            columns=("DNI", "Nombre", "Apellido", "Teléfono", "Email", "Activo"),
            show="headings",
            yscrollcommand=scrollbar.set
        )

        headers = ["DNI", "Nombre", "Apellido", "Teléfono", "Email", "Activo"]
        for h in headers:
            self.tree.heading(h, text=h)

        scrollbar.config(command=self.tree.yview)

        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_select_row)

    def actualizar_lista(self, clientes):
        """Actualiza la tabla."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for cli in clientes:
            self.tree.insert("", "end",
                             iid=cli['id_cliente'],
                             values=(cli['dni'], cli['nombre'], cli['apellido'],
                                     cli['telefono'], cli['email'],
                                     "Sí" if cli['activo'] else "No"))

    def limpiar_formulario(self):
        self.id_var.set("")
        self.dni_var.set("")
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.telefono_var.set("")
        self.email_var.set("")
        self.direccion_var.set("")
        self.activo_var.set(True)

    def validar_formulario(self):
        """Validaciones básicas  antes de enviar al controlador"""
        datos = self.obtener_datos_formulario()
        
        # Validar campos obligatorios
        if not datos['dni'].strip():
            self.mostrar_mensaje("Error", "El DNI es obligatorio", error=True)
            return False
            
        if not datos['nombre'].strip():
            self.mostrar_mensaje("Error", "El nombre es obligatorio", error=True)
            return False
            
        if not datos['apellido'].strip():
            self.mostrar_mensaje("Error", "El apellido es obligatorio", error=True)
            return False
        
        # Validar formato DNI (solo números, 7-8 dígitos)
        if not datos['dni'].isdigit() or len(datos['dni']) not in [7, 8]:
            self.mostrar_mensaje("Error", "DNI debe contener solo números (7 u 8 dígitos)", error=True)
            return False
        
        # Validar formato email si se ingresó
        if datos['email'] and "@" not in datos['email']:
            self.mostrar_mensaje("Error", "Formato de email inválido", error=True)
            return False
            
        # Validar teléfono si se ingresó (solo números)
        if datos['telefono'] and not datos['telefono'].isdigit():
            self.mostrar_mensaje("Error", "Teléfono debe contener solo números", error=True)
            return False
        
        return True
    
    def mostrar_mensaje(self, titulo, mensaje, error=False, confirm=False):
        if error:
            messagebox.showerror(titulo, mensaje)
        elif confirm:
            return messagebox.askyesno(titulo, mensaje)
        else:
            messagebox.showinfo(titulo, mensaje)

    def obtener_datos_formulario(self):
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
        self.id_var.set(item['id_cliente'])
        self.dni_var.set(item['dni'])
        self.nombre_var.set(item['nombre'])
        self.apellido_var.set(item['apellido'])
        self.telefono_var.set(item['telefono'])
        self.email_var.set(item['email'])
        self.direccion_var.set(item['direccion'])
        self.activo_var.set(item['activo'])

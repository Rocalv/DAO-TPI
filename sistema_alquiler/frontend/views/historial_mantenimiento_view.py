# frontend/views/historial_mantenimiento_view.py
import tkinter as tk
from tkinter import ttk, messagebox

BG_COLOR, FG_COLOR = "#212121", "white"
BTN_BG, BTN_FG = "#424242", "white"
TREE_BG, TREE_FG, TREE_SEL = "#2a2a2a", "white", "#0078d4"

class HistorialMantenimientoView(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self._configurar_estilos()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=TREE_BG, foreground=TREE_FG, fieldbackground=TREE_BG, borderwidth=0)
        style.map('Treeview', background=[('selected', TREE_SEL)])
        style.configure("Treeview.Heading", background="#555555", foreground="white", font=('Helvetica', 9, 'bold'))

    def create_widgets(self):
        # Título
        tk.Label(self, text="Historial de Mantenimientos (Finalizados)", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 16, "bold")).pack(pady=(20, 10))

        # Frame de la Grilla
        tree_frame = tk.Frame(self, bg=BG_COLOR)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Columnas solicitadas: Vehículo, Servicio, Fecha Inicio, Fecha Fin, Costo
        cols = ("Vehículo", "Servicio", "Fecha Inicio", "Fecha Fin", "Costo", "Técnico")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", yscrollcommand=scrollbar.set)
        
        for col in cols: self.tree.heading(col, text=col)
        self.tree.column("Vehículo", width=200)
        self.tree.column("Servicio", width=200)
        self.tree.column("Fecha Inicio", width=100, anchor="center")
        self.tree.column("Fecha Fin", width=100, anchor="center")
        self.tree.column("Costo", width=100, anchor="e")
        self.tree.column("Técnico", width=150)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        # Botón de Acción
        btn_frame = tk.Frame(self, bg=BG_COLOR, pady=20)
        btn_frame.pack()
        
        tk.Button(btn_frame, text="Recargar Historial", 
                  command=self.controller.cargar_datos, 
                  bg=BTN_BG, fg=BTN_FG, font=("Helvetica", 10), padx=10, pady=5).pack()

    def actualizar_tabla(self, mantenimientos):
        """Recarga la tabla con los datos recibidos."""
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        for m in mantenimientos:
            vehiculo_str = f"{m['patente']} - {m['marca']} {m['modelo']}"
            tecnico_str = f"{m.get('empleado_apellido', 'N/A')}, {m.get('empleado_nombre', '')}"
            costo_str = f"${m['costo'] or 0:,.2f}"
            
            self.tree.insert("", "end", values=(
                vehiculo_str,
                m['servicio_nombre'],
                m['fecha_inicio'],
                m['fecha_fin'],
                costo_str,
                tecnico_str
            ))

    def mostrar_mensaje(self, t, m, error=False, confirm=False):
        if error: messagebox.showerror(t, m)
        elif confirm: return messagebox.askyesno(t, m)
        else: messagebox.showinfo(t, m)
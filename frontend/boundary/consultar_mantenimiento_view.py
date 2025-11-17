import tkinter as tk
from tkinter import ttk, messagebox

BG_COLOR, FG_COLOR = "#212121", "white"
TREE_BG, TREE_FG, TREE_SEL = "#2a2a2a", "white", "#0078d4"
BTN_BG, BTN_FG = "#2e7d32", "white"

class ConsultarMantenimientoView(tk.Frame):
    def __init__(self, parent, on_finalizar):
        super().__init__(parent, bg=BG_COLOR)
        self.on_finalizar = on_finalizar

        self._configurar_estilos()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=TREE_BG, foreground=TREE_FG, fieldbackground=TREE_BG)
        style.map('Treeview', background=[('selected', TREE_SEL)])
        style.configure("Treeview.Heading", background="#555555", foreground="white", font=('Helvetica', 9, 'bold'))
        style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=('Helvetica', 14, 'bold'))

    def create_widgets(self):
        tk.Label(
            self, text="Mantenimientos en Curso (Pendientes)",
            bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 16, "bold")
        ).pack(pady=(20, 10))

        tree_frame = tk.Frame(self, bg=BG_COLOR)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        cols = ("ID", "Vehículo", "Servicio", "Fecha Inicio", "Proveedor")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", yscrollcommand=scrollbar.set)
        for col in cols: self.tree.heading(col, text=col)
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Vehículo", width=200)
        self.tree.column("Servicio", width=200)
        self.tree.column("Fecha Inicio", width=100, anchor="center")
        self.tree.column("Proveedor", width=150)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        btn_frame = tk.Frame(self, bg=BG_COLOR, pady=20)
        btn_frame.pack()
        tk.Button(
            btn_frame,
            text="Finalizar Mantenimiento Seleccionado",
            command=self.on_finalizar,
            bg=BTN_BG, fg=BTN_FG,
            font=("Helvetica", 12, "bold"), padx=20, pady=10
        ).pack()

    def actualizar_tabla(self, mantenimientos):
        self.tree.delete(*self.tree.get_children())
        for m in mantenimientos:
            vehiculo_str = f"{m['patente']} - {m['marca']} {m['modelo']}"
            self.tree.insert("", "end", values=(
                m['id_mantenimiento'],
                vehiculo_str,
                m['servicio_nombre'],
                m['fecha_inicio'],
                m['proveedor'] or "N/A"
            ))

    def obtener_id_seleccionado(self):
        selected = self.tree.selection()
        if not selected: return None
        return self.tree.item(selected[0])['values'][0]

    def mostrar_mensaje(self, t, m, error=False, confirm=False):
        if error:
            messagebox.showerror(t, m)
        elif confirm:
            return messagebox.askyesno(t, m)
        else:
            messagebox.showinfo(t, m)

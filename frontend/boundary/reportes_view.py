import tkinter as tk
from tkinter import ttk

# --- Consistencia de Colores (Importados o definidos globalmente) ---
BG_COLOR, FG_COLOR = "#212121", "white"
BTN_BG, BTN_FG = "#424242", "white" 

class ReportesView(tk.Frame):
    """
    Vista principal para la generación de reportes.
    Presenta los botones que disparan la lógica del ReportesController.
    """
    
    def __init__(self, parent, controller_callbacks):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller_callbacks

        self.reportes = [
            ("Listado alquileres por cliente", self.controller.generar_listado_alquileres_por_cliente),
            ("Vehículos más alquilados", self.controller.generar_vehiculos_mas_alquilados),
            ("Alquileres por período", self.controller.generar_alquileres_por_periodo),
            ("Estadística facturación mensual (gráfico)", self.controller.generar_estadistica_facturacion_mensual)
        ]
        
        # Se elimina _configurar_estilos ya que no se usará ttk.Button con estilos personalizados.

    # Se elimina el método _configurar_estilos.

    def create_widgets(self):
        # Título principal de la vista (Consistente con otras vistas)
        tk.Label(
            self, 
            text="Generación de Reportes y Estadísticas",
            bg=BG_COLOR, fg=FG_COLOR, 
            font=("Helvetica", 16, "bold")
        ).pack(pady=(20, 30))

        # Marco principal centrado
        main_frame = tk.Frame(self, bg=BG_COLOR, padx=40, pady=20)
        main_frame.pack(expand=True, fill="both")
        
        # Subtítulo (Consistente con otras etiquetas)
        tk.Label(
            main_frame, 
            text="Seleccione un reporte para generar el PDF:", 
            bg=BG_COLOR, 
            fg=FG_COLOR, 
            font=("Helvetica", 12, "bold")
        ).pack(pady=(10, 15))

        # Creación de Botones (USANDO tk.Button PARA EVITAR EL ERROR DE LAYOUT)
        for name, callback in self.reportes:
            btn = tk.Button( # CAMBIO CLAVE: Usar tk.Button en lugar de ttk.Button
                main_frame,
                text=name,
                command=callback, 
                bg=BTN_BG, 
                fg=BTN_FG, 
                font=("Helvetica", 10, "bold"), # Aplicación directa de la fuente/colores
                padx=10, # Añadir padding para simular el estilo
                pady=5,
                relief="raised" # Estilo consistente
            )
            btn.pack(pady=8, padx=10, fill="x")

        # Nota explicativa
        tk.Label(
            main_frame,
            text="Nota: Los reportes solicitarán los parámetros necesarios (ej. Cliente, Fechas o Año) mediante diálogos emergentes, y luego pedirán la ubicación para guardar el archivo PDF.",
            bg=BG_COLOR, fg="#AAAAAA", 
            font=("Helvetica", 9, "italic"),
            wraplength=450,
            justify="center"
        ).pack(pady=(30, 10))
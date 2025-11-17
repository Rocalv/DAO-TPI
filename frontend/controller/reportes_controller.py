import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from entidades.cliente import Cliente
from entidades import reporte as reports


class ReportesController:
    def __init__(self, app):
        self.app = app

    def _ask_save_path(self, default_name):
        path = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF Files', '*.pdf')], initialfile=default_name)
        return path

    def generar_listado_alquileres_por_cliente(self):
        try:
            clientes = Cliente.consultar()
            if not clientes:
                messagebox.showinfo('Reportes', 'No hay clientes registrados.')
                return

            # Mostrar selector simple
            win = tk.Toplevel()
            win.title('Seleccionar cliente')
            win.geometry('400x120')
            win.transient(self.app)
            win.grab_set()

            ttk.Label(win, text='Cliente:').pack(pady=(10, 0))
            items = [f"{c['id_cliente']} - {c['nombre']} {c['apellido']}" for c in clientes]
            cmb = ttk.Combobox(win, values=items, state='readonly')
            cmb.pack(padx=10, pady=6, fill='x')

            def on_ok():
                sel = cmb.get()
                if not sel:
                    messagebox.showwarning('Reportes', 'Seleccione un cliente.'); return
                id_cliente = int(sel.split(' - ')[0])
                win.destroy()
                save_path = self._ask_save_path(f'listado_alquileres_cliente_{id_cliente}.pdf')
                if not save_path: return
                reports.generar_listado_alquileres_por_cliente(id_cliente, save_path)
                messagebox.showinfo('Reportes', f'Reporte generado:\n{save_path}')

            btn = ttk.Button(win, text='Generar PDF', command=on_ok)
            btn.pack(pady=8)

        except Exception as e:
            messagebox.showerror('Error', f'Error al generar reporte: {e}')

    def generar_vehiculos_mas_alquilados(self):
        try:
            limit = simpledialog.askinteger('Vehículos más alquilados', 'Cantidad a listar (máx 50):', initialvalue=10, minvalue=1, maxvalue=50, parent=self.app)
            if limit is None: return
            save_path = self._ask_save_path('vehiculos_mas_alquilados.pdf')
            if not save_path: return
            reports.generar_vehiculos_mas_alquilados(save_path, limit=limit)
            messagebox.showinfo('Reportes', f'Reporte generado:\n{save_path}')
        except Exception as e:
            messagebox.showerror('Error', f'Error al generar reporte: {e}')

    def generar_alquileres_por_periodo(self):
        try:
            # Reemplazamos la entrada por texto por una pequeña ventana con controles
            win = tk.Toplevel()
            win.title('Alquileres por período')
            win.geometry('360x160')
            win.transient(self.app)
            win.grab_set()

            ttk.Label(win, text='Tipo de período:').grid(row=0, column=0, padx=8, pady=(12, 4), sticky='w')
            tipo_cb = ttk.Combobox(win, values=['mes', 'trimestre'], state='readonly', width=12)
            tipo_cb.current(0)
            tipo_cb.grid(row=0, column=1, padx=8, pady=(12, 4), sticky='w')

            ttk.Label(win, text='Valor:').grid(row=1, column=0, padx=8, pady=4, sticky='w')
            value_cb = ttk.Combobox(win, values=[str(i) for i in range(1, 13)], state='readonly', width=12)
            value_cb.current(0)
            value_cb.grid(row=1, column=1, padx=8, pady=4, sticky='w')

            ttk.Label(win, text='Año:').grid(row=2, column=0, padx=8, pady=4, sticky='w')
            year_sb = tk.Spinbox(win, from_=2000, to=2100, width=10)
            year_sb.delete(0, 'end')
            year_sb.insert(0, str(datetime_now_year()))
            year_sb.grid(row=2, column=1, padx=8, pady=4, sticky='w')

            def on_tipo_change(event=None):
                t = tipo_cb.get()
                if t == 'mes':
                    value_cb['values'] = [str(i) for i in range(1, 13)]
                    value_cb.current(0)
                else:
                    value_cb['values'] = [str(i) for i in range(1, 5)]
                    value_cb.current(0)

            tipo_cb.bind('<<ComboboxSelected>>', on_tipo_change)

            def on_ok():
                t = tipo_cb.get()
                v = value_cb.get()
                y = year_sb.get()
                if not (t and v and y):
                    messagebox.showwarning('Reportes', 'Complete todos los campos.'); return
                try:
                    yi = int(y)
                    vi = int(v)
                except:
                    messagebox.showwarning('Reportes', 'Año o valor inválido.'); return
                win.destroy()
                save_path = self._ask_save_path(f'alquileres_{t}_{vi}_{yi}.pdf')
                if not save_path: return
                reports.generar_alquileres_por_periodo(yi, t, vi, save_path)
                messagebox.showinfo('Reportes', f'Reporte generado:\n{save_path}')

            btn_ok = ttk.Button(win, text='Generar PDF', command=on_ok)
            btn_ok.grid(row=3, column=0, columnspan=2, pady=(10, 12))

        except Exception as e:
            messagebox.showerror('Error', f'Error al generar reporte: {e}')

    def generar_estadistica_facturacion_mensual(self):
        try:
            year = simpledialog.askinteger('Año', 'Año (ej. 2025):', parent=self.app, initialvalue=datetime_now_year())
            if year is None: return
            save_path = self._ask_save_path(f'facturacion_mensual_{year}.pdf')
            if not save_path: return
            reports.generar_estadistica_facturacion_mensual(year, save_path)
            messagebox.showinfo('Reportes', f'Reporte generado:\n{save_path}')
        except Exception as e:
            messagebox.showerror('Error', f'Error al generar reporte: {e}')


def datetime_now_year():
    try:
        from datetime import datetime
        return datetime.now().year
    except:
        return 2025

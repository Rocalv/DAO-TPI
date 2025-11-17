import os
import tempfile
from datetime import datetime
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import matplotlib.pyplot as plt

from persistencia.db_config import db

styles = getSampleStyleSheet()


def _fetchall(query, params=()):
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description] if cur.description else []
    db.close_connection()
    return cols, rows


def generar_listado_alquileres_por_cliente(id_cliente, output_path):
    """Genera un PDF con el listado detallado de alquileres para un cliente."""
    cols, rows = _fetchall(
        """
        SELECT a.id_alquiler, a.fecha_inicio, a.fecha_fin, a.costo_total, a.estado, v.patente, v.marca || ' ' || v.modelo AS vehiculo
        FROM alquileres a
        JOIN vehiculos v ON a.id_vehiculo = v.id_vehiculo
        WHERE a.id_cliente = ?
        ORDER BY a.fecha_inicio DESC
        """,
        (id_cliente,)
    )

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    story.append(Paragraph(f"Listado de alquileres - Cliente ID: {id_cliente}", styles['Title']))
    story.append(Spacer(1, 12))

    if not rows:
        story.append(Paragraph("No se encontraron alquileres para este cliente.", styles['BodyText']))
    else:
        table_data = [cols]
        for r in rows:
            row = [str(x) if x is not None else "" for x in r]
            table_data.append(row)

        t = Table(table_data, hAlign='LEFT')
        t.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dddddd')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ])
        story.append(t)

    doc.build(story)


def generar_vehiculos_mas_alquilados(output_path, limit=10):
    """Genera un PDF listando los vehículos más alquilados por cantidad."""
    cols, rows = _fetchall(
        """
        SELECT v.id_vehiculo, v.patente, v.marca || ' ' || v.modelo AS vehiculo, COUNT(a.id_alquiler) AS veces_alquilado
        FROM vehiculos v
        LEFT JOIN alquileres a ON v.id_vehiculo = a.id_vehiculo
        GROUP BY v.id_vehiculo
        ORDER BY veces_alquilado DESC
        LIMIT ?
        """,
        (limit,)
    )

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = [Paragraph("Vehículos más alquilados", styles['Title']), Spacer(1, 12)]
    table_data = [cols]
    for r in rows:
        table_data.append([str(x) if x is not None else "" for x in r])

    t = Table(table_data, hAlign='LEFT')
    t.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dddddd')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ])
    story.append(t)
    doc.build(story)


def generar_alquileres_por_periodo(year, periodo_type, value, output_path):
    """Genera un PDF con los alquileres para un período dado.
    periodo_type: 'mes' or 'trimestre'
    value: month (1-12) or quarter (1-4)
    """
    if periodo_type == 'mes':
        q = "SELECT a.id_alquiler, a.fecha_inicio, a.fecha_fin, a.costo_total, a.estado, a.id_cliente, v.patente FROM alquileres a JOIN vehiculos v ON a.id_vehiculo=v.id_vehiculo WHERE strftime('%Y', a.fecha_inicio)=? AND strftime('%m', a.fecha_inicio)=? ORDER BY a.fecha_inicio"
        params = (str(year), f"{int(value):02d}")
    else:
        # trimestre 1 -> meses 01-03, 2->04-06, etc.
        start = 1 + (int(value) - 1) * 3
        months = [f"{m:02d}" for m in range(start, start + 3)]
        q = f"SELECT a.id_alquiler, a.fecha_inicio, a.fecha_fin, a.costo_total, a.estado, a.id_cliente, v.patente FROM alquileres a JOIN vehiculos v ON a.id_vehiculo=v.id_vehiculo WHERE strftime('%Y', a.fecha_inicio)=? AND strftime('%m', a.fecha_inicio) IN ({', '.join(['?']*3)}) ORDER BY a.fecha_inicio"
        params = tuple([str(year)] + months)

    cols, rows = _fetchall(q, params)

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    title = f"Alquileres - {periodo_type.capitalize()}: {value} / {year}"
    story = [Paragraph(title, styles['Title']), Spacer(1, 12)]

    if not rows:
        story.append(Paragraph("No se encontraron alquileres para este período.", styles['BodyText']))
    else:
        table_data = [cols]
        for r in rows:
            table_data.append([str(x) if x is not None else "" for x in r])
        t = Table(table_data, hAlign='LEFT')
        t.setStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dddddd')), ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)])
        story.append(t)

    doc.build(story)


def generar_estadistica_facturacion_mensual(year, output_path):
    """Genera un PDF con un gráfico de barras de la facturación mensual del año dado."""
    # Obtener totales por mes
    q = "SELECT strftime('%m', fecha_inicio) as mes, SUM(costo_total) as total FROM alquileres WHERE strftime('%Y', fecha_inicio)=? GROUP BY mes ORDER BY mes"
    cols, rows = _fetchall(q, (str(year),))

    meses = [f"{i:02d}" for i in range(1, 13)]
    valores = {r[0]: (r[1] or 0) for r in rows}
    totals = [float(valores.get(m, 0)) for m in meses]

    # Crear gráfico
    plt.figure(figsize=(10, 4))
    x = range(1, 13)
    plt.bar(x, totals, color='#4c72b0')
    plt.xticks(x, [str(i) for i in range(1, 13)])
    plt.xlabel('Mes')
    plt.ylabel('Facturación')
    plt.title(f'Facturación mensual - {year}')
    plt.tight_layout()

    tmpdir = tempfile.gettempdir()
    chart_path = os.path.join(tmpdir, f'fact_mes_{year}.png')
    plt.savefig(chart_path)
    plt.close()

    # Generar PDF e incluir imagen
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = [Paragraph(f"Estadística de facturación mensual - {year}", styles['Title']), Spacer(1, 12)]
    story.append(RLImage(chart_path, width=450, height=200))
    story.append(Spacer(1, 12))

    # Añadir tabla con valores
    table_data = [['Mes', 'Total']]
    for i, tval in enumerate(totals, start=1):
        table_data.append([str(i), f"{tval:.2f}"])
    t = Table(table_data, hAlign='LEFT')
    t.setStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dddddd')), ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)])
    story.append(t)

    doc.build(story)

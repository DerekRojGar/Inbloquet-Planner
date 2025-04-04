# models/export_model.py
import locale
from datetime import datetime
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.drawing.image import Image

def crear_excel_con_diseño(df, filename, semana, año, img_width=120, img_height=120):
    # Configurar el idioma a español para los nombres de los meses
    try:
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")  # Linux/Mac
    except locale.Error:
        locale.setlocale(locale.LC_TIME, "Spanish_Spain.1252")  # Windows

    wb = Workbook()
    ws = wb.active
    ws.title = f"Semana {semana}"
    
    ws.insert_rows(1, 3)  # Insertamos 3 filas para el encabezado

    # COMBINAR CELDAS ===
    ws.merge_cells("A1:B3")  # Logo de la empresa
    ws.merge_cells("D1:I1")  # Información de la semana
    ws.merge_cells("D2:I2")
    ws.merge_cells("D3:I3")
    ws.merge_cells("J1:J3")
    ws.merge_cells("A4:K4")

    # INSERTAR LOGOS Y AJUSTAR TAMAÑO ===
    max_img_height = 0  # Variable para rastrear la imagen más grande en altura

    try:
        img1 = Image("InbloquetD.png")  # Cargar imagen del archivo
        img1.width = img_width        # Usar el parámetro img_width
        img1.height = img_height      # Usar el parámetro img_height
        ws.add_image(img1, "A1")
        max_img_height = max(max_img_height, img1.height)
    except FileNotFoundError:
        ws["A1"] = "LOGO NO ENCONTRADO"
        ws["A1"].font = Font(bold=True, size=14)
        ws["A1"].alignment = Alignment(horizontal="center", vertical="center")

    try:
        img2 = Image("rocket.png")  # Cargar imagen del archivo
        # Para la segunda imagen se puede usar una relación distinta, por ejemplo el 60% del ancho de la primera
        img2.width = int(img_width * 0.6)
        img2.height = img_height
        ws.add_image(img2, "J1")
        max_img_height = max(max_img_height, img2.height)
    except FileNotFoundError:
        ws["K1"] = "IMAGEN NO ENCONTRADA"
        ws["K1"].font = Font(bold=True, size=14)
        ws["K1"].alignment = Alignment(horizontal="center", vertical="center")

    # Ajustar la altura de las filas combinadas según la imagen más alta
    row_height = max_img_height / 4  # Ajuste proporcional
    ws.row_dimensions[1].height = row_height
    ws.row_dimensions[2].height = row_height
    ws.row_dimensions[3].height = row_height

    # INSERTAR ENCABEZADO PRINCIPAL ===
    ws["D1"] = "Programación de Actividades Semanal"
    ws["D1"].font = Font(bold=True, size=20)
    ws["D1"].alignment = Alignment(horizontal="center", vertical="center")

    ws["D2"] = f"SEMANA {semana} - AÑO {año}"
    ws["D2"].font = Font(bold=True, size=16)
    ws["D2"].alignment = Alignment(horizontal="center", vertical="center")

    ws["D3"] = "¡Intenta, Explora y Conquista!"
    ws["D3"].font = Font(bold=True, size=14)
    ws["D3"].alignment = Alignment(horizontal="center", vertical="center")

    # REFORMATEAR COLUMNA FECHA ===
    df["Fecha"] = df.apply(lambda row: f"{row['Día']} {int(row['Fecha'][:2])} de {datetime.strptime(row['Fecha'], '%d/%m').strftime('%B')} del {row['Año']}", axis=1)
    
    # Convertir el mes a minúsculas y capitalizar la primera letra
    df["Fecha"] = df["Fecha"].apply(lambda x: x.replace(x.split()[3], x.split()[3].capitalize()))

    # Eliminar las columnas antiguas
    df = df.drop(columns=["Día", "Año"])

    # Reorganizar las columnas para que Fecha esté al inicio
    column_order = ["Semana", "Fecha", "Horario", "Alumnos", "Escuelas", "Grupos", "Maestro", "Tema", "Encargado", "Notas"]
    df = df[column_order]

    # INSERTAR ENCABEZADOS ===
    ws.append(df.columns.tolist())

    # INSERTAR DATOS ===
    for item in df.to_dict('records'):
        ws.append(list(item.values()))

    # FORMATEAR TABLA ===
    tabla_ref = f"A5:J{ws.max_row}"  # Tabla desde la fila 5 hasta la última con datos
    tabla = Table(displayName="TablaActividades", ref=tabla_ref)

    estilo_tabla = TableStyleInfo(
        name="TableStyleMedium9",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,  
        showColumnStripes=False
    )
    tabla.tableStyleInfo = estilo_tabla
    ws.add_table(tabla)

    # AJUSTE AUTOMÁTICO DE COLUMNAS ===
    for col in ws.iter_cols(min_row=5, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        col_letter = col[0].column_letter
        max_length = max((len(str(celda.value)) if celda.value else 0) for celda in col) + 2
        ws.column_dimensions[col_letter].width = max_length

    # AJUSTAR TEXTO EN LA COLUMNA "TEMA" ===
    for celda in ws["H"]:  # Columna "Tema"
        celda.alignment = Alignment(wrap_text=True)

    # GUARDAR ARCHIVO EXCEL ===
    wb.save(filename)

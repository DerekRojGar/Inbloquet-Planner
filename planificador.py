import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import base64
import os
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
from openpyxl.cell.cell import MergedCell

# ==================================================
# CONFIGURACIÓN INICIAL
# ==================================================
st.set_page_config(
    page_title="Planificador INBLOQUET",
    page_icon="📅",
    layout="wide"
)

# ==================================================
# ESTILOS CSS
# ==================================================
st.markdown("""
    <style>
    .logo-sidebar {
        max-width: 200px;
        margin: 20px auto;
        padding: 10px;
    }
    .frase-dia {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #003366;
        margin: 20px 0;
        color: #333;
    }
    .actividad-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
        color: #333; /* Color de texto oscuro para mejor legibilidad */
    }
    .actividad-card b {
        color: #003366; /* Color para los títulos */
    }
    .st-expander {
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .st-expander .stMarkdown {
        color: #333; /* Color de texto oscuro para mejor legibilidad */
    }
    </style>
    """, unsafe_allow_html=True)

# ==================================================
# FUNCIONES BASE
# ==================================================
def generar_semana(año, semana):
    fecha_inicio = datetime(año, 1, 4)
    fecha_inicio = fecha_inicio - timedelta(days=fecha_inicio.weekday())
    fecha_inicio += timedelta(weeks=semana-1)
    return [fecha_inicio + timedelta(days=i) for i in range(6)]  # Lunes a Sábado

DIAS_ESPAÑOL = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]

# ==================================================
# CARGAR DATOS DESDE CSV
# ==================================================
def cargar_datos():
    if os.path.exists("actividades.csv"):
        try:
            df = pd.read_csv("actividades.csv")
            if df.empty:  # Verificar si el DataFrame está vacío
                return {}
            actividades = {}
            for _, row in df.iterrows():
                semana_key = f"{row['Año']}-S{row['Semana']}"
                fecha = row['Fecha']
                actividad = {
                    "Escuelas": row['Escuelas'],
                    "Horario": row ['Horario'],
                    "Grupos": row['Grupos'],
                    "Tema": row['Tema'],
                    "Maestro": row ['Maestro'],
                    "Alumnos": row['Alumnos'],
                    "Notas": row['Notas']
                }
                if semana_key not in actividades:
                    actividades[semana_key] = {
                        "fechas": [dia.strftime("%d/%m") for dia in generar_semana(int(row['Año']), int(row['Semana']))],
                        "actividades": {dia.strftime("%d/%m"): [] for dia in generar_semana(int(row['Año']), int(row['Semana']))}
                    }
                if fecha not in actividades[semana_key]["actividades"]:
                    actividades[semana_key]["actividades"][fecha] = []
                actividades[semana_key]["actividades"][fecha].append(actividad)
            return actividades
        except pd.errors.EmptyDataError:  # Manejar archivos vacíos
            return {}
    return {}

# ==================================================
# GUARDAR DATOS EN CSV
# ==================================================
def guardar_datos(actividades):
    all_data = []
    for semana_key, semana_data in actividades.items():
        año, semana = semana_key.split("-S")
        año = int(año)
        semana = int(semana)
        for fecha, actividades_dia in semana_data["actividades"].items():
            for act in actividades_dia:
                registro = {
                    "Semana": semana,
                    "Año": año,
                    "Fecha": fecha,
                    **act
                }
                all_data.append(registro)
    df = pd.DataFrame(all_data)
    df.to_csv("actividades.csv", index=False, encoding='utf-8-sig')

# ==================================================
# INICIALIZACIÓN DE DATOS
# ==================================================
if 'actividades' not in st.session_state:
    st.session_state.actividades = cargar_datos()

# ==================================================
# BARRA LATERAL (LOGO Y CONFIGURACIÓN)
# ==================================================
with st.sidebar:
    # Logo (reemplazar 'logo.png' con tu archivo)
    st.image("Inbloquet.png",  # 🖼️ Coloca tu archivo aquí
            use_container_width=True,  # Cambiado a use_container_width
            output_format='PNG',
            caption="",
            width=150,
            clamp=False)
    
    # Configuración de semana
    st.header("⚙️ Configuración")
    semana = st.number_input("Número de Semana", 1, 52, 9)
    año = st.number_input("Año", 2024, 2030, 2025)
    
    # Editor de frase
    st.markdown("---")
    frase_actual = st.session_state.get('frase_global', '')
    nueva_frase = st.text_area("✍️ Frase inspiradora del día:", value=frase_actual)
    if st.button("💾 Guardar Frase"):
        st.session_state.frase_global = nueva_frase
        st.rerun()

# ==================================================
# CONTENIDO PRINCIPAL
# ==================================================
st.title("📅 Planificación Semanal INBLOQUET")
st.markdown("---")

# Frase del día debajo del título
if 'frase_global' in st.session_state and st.session_state.frase_global:
    st.markdown(f'<div class="frase-dia">📌 {st.session_state.frase_global}</div>', 
               unsafe_allow_html=True)

# ==================================================
# FORMULARIO DE ACTIVIDADES
# ==================================================
with st.form(key='form_actividad'):
    st.subheader("📝 Nueva Actividad")
    
    cols = st.columns(2)
    with cols[0]:
        dia_seleccionado = st.selectbox("Selecciona el día:", DIAS_ESPAÑOL)
        
        escuelas = st.multiselect(
            "Selecciona escuelas:",
            ["INBLOQUET", "AEC", "RW", "AB"],
            key='escuelas'
        )
        
        grupos = st.multiselect(
            "Selecciona grupos:",
            ["RINOS", "PRESCO", "PA", "PB", "LOBOS", "PANDAS/BUFALOS", "PUMAS/DELFINES", "S DUPLO", "S NORMAL", "M", "L"],
            key='grupos'
        )
        
        # Campo para Horario
        horario = st.text_input(
            "Horario de la actividad:",
            placeholder="Ej: 8:00 a.m. - 2:00 p.m."
        )
    
    with cols[1]:
        tema = st.text_area(
            "Descripción detallada:",
            placeholder="Ej: Taller de programación con robots",
            height=100
        )
        
        maestro = st.text_input(
            "Maestro",
            placeholder="Ej: Caleb, Angie, Emma"
        )
        
        alumnos = st.text_input(
            "Alumnos:",
            placeholder="Ej: Dereck, Alberto, Emma"
        )
        
        notas = st.text_input(
            "Información adicional:",
            placeholder="Ej: Materiales especiales requeridos"
        )
    
    # Botón de guardado
    if st.form_submit_button("💾 Guardar Actividad"):
        if escuelas:
            nueva_actividad = {
                "Escuelas": ", ".join(escuelas),
                "Horario": horario if horario else "-",
                "Grupos": ", ".join(grupos) if grupos else "-",
                "Tema": tema if tema else "-",
                "Maestro": maestro if maestro else "-",
                "Alumnos": alumnos if alumnos else "-",
                "Notas": notas if notas else "-"
            }
            semana_key = f"{año}-S{semana}"
            if semana_key not in st.session_state.actividades:
                st.session_state.actividades[semana_key] = {
                    "fechas": [dia.strftime("%d/%m") for dia in generar_semana(año, semana)],
                    "actividades": {dia.strftime("%d/%m"): [] for dia in generar_semana(año, semana)}
                }
            fecha_key = st.session_state.actividades[semana_key]["fechas"][DIAS_ESPAÑOL.index(dia_seleccionado)]
            st.session_state.actividades[semana_key]["actividades"][fecha_key].append(nueva_actividad)
            guardar_datos(st.session_state.actividades)
            st.success("✅ Actividad registrada exitosamente!")
            st.rerun()
        else:
            st.error("❌ Debes seleccionar al menos una escuela")

# ==================================================
# VISTA DE CALENDARIO
# ==================================================
st.markdown("---")
st.subheader("🗓️ Vista Semanal")

semana_key = f"{año}-S{semana}"
if semana_key not in st.session_state.actividades:
    st.session_state.actividades[semana_key] = {
        "fechas": [dia.strftime("%d/%m") for dia in generar_semana(año, semana)],
        "actividades": {dia.strftime("%d/%m"): [] for dia in generar_semana(año, semana)}
    }

cols_calendario = st.columns(6)
for i, col in enumerate(cols_calendario):
    with col:
        dia_str = st.session_state.actividades[semana_key]["fechas"][i]
        actividades = st.session_state.actividades[semana_key]["actividades"][dia_str]
        
        st.markdown(f"**{DIAS_ESPAÑOL[i]}**")
        st.caption(dia_str)
        
        if actividades:
            for idx, act in enumerate(actividades):
                with st.expander(act['Escuelas'], expanded=False):
                    st.markdown(f"""
                    - **Horario:** {act['Horario']}
                    - **Grupos:** {act['Grupos']}
                    - **Tema:** {act['Tema']}
                    - **Maestro** {act['Maestro']}
                    - **Alumnos:** {act['Alumnos']}
                    - **Notas:** {act['Notas']}
                    """)
                    if st.button(f"Detalles", key=f"btn_expand_{dia_str}_{idx}"):
                        st.session_state.selected_activity = {
                            "semana_key": semana_key,
                            "dia_str": dia_str,
                            "index": idx,
                            "datos": act
                        }
                        st.rerun()
        else:
            st.info("Sin actividades")

# ==================================================
# DETALLE DE ACTIVIDAD (DESPLAZAMIENTO AUTOMÁTICO)
# ==================================================
if "selected_activity" in st.session_state:
    selected = st.session_state.selected_activity
    act = selected["datos"]
    
    st.subheader("📋 Detalle de Actividad")
    st.markdown(f"""
    - **Escuelas:** {act['Escuelas']}
    - **Horario** {act['Horario']}
    - **Grupos:** {act['Grupos']}
    - **Tema:** {act['Tema']}
    - **Maestro** {act['Maestro']}
    - **Alumnos:** {act['Alumnos']}
    - **Notas:** {act['Notas']}
    """)
    
    col1, col2 = st.columns([1, 6])
    
    with col1:
        if st.button("✏️ Editar"):
            st.session_state.editando = selected
            st.rerun()
    
    with col2:
        if st.button("🗑️ Eliminar"):
            del st.session_state.actividades[selected["semana_key"]]["actividades"][selected["dia_str"]][selected["index"]]
            st.success("✅ Actividad eliminada!")
            del st.session_state.selected_activity
            st.rerun()

# ==================================================
# MÓDULO DE EDICIÓN
# ==================================================
if 'editando' in st.session_state:
    st.markdown("---")
    st.subheader("✏️ Editor de Actividad")
    
    edit = st.session_state.editando
    with st.form(key='form_edicion'):
        cols = st.columns([2, 3, 2])
        
        with cols[0]:
            escuelas_edit = st.multiselect(
                "Escuelas",
                ["INBLOQUET", "AEC", "RW", "AB"],
                default=edit["datos"]["Escuelas"].split(", ")
            )
            grupos_edit = st.multiselect(
                "Grupos",
                ["RINOS", "PRESCO", "PA", "PB", "LOBOS", "PANDAS/BUFALOS", "PUMAS/DELFINES", "S DUPLO", "S NORMAL", "M", "L"],
                default=edit["datos"]["Grupos"].split(", ") if edit["datos"]["Grupos"] != "-" else []
            )
            
            maestro_edit = st.text_input(
                "Maestro",
                value=edit["datos"]["Maestro"] if edit["datos"]["Maestro"] != "-" else ""
            )
        
        with cols[1]:
            tema_edit = st.text_area(
                "Tema",
                value=edit["datos"]["Tema"] if edit["datos"]["Tema"] != "-" else ""
            )
        
        with cols[2]:
            alumnos_edit = st.text_input(
                "Alumnos",
                value=edit["datos"]["Alumnos"] if edit["datos"]["Alumnos"] != "-" else ""
            )
            notas_edit = st.text_input(
                "Notas",
                value=edit["datos"]["Notas"] if edit["datos"]["Notas"] != "-" else ""
            )
            horario_edit = st.text_input(
                "Horario",
                value=edit["datos"]["Horario"] if edit["datos"]["Horario"] != "-" else ""
            )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.form_submit_button("💾 Guardar Cambios"):
                if escuelas_edit:
                    nueva_actividad = {
                        "Escuelas": ", ".join(escuelas_edit),
                        "Horario": horario_edit.strip() if horario_edit else "-",
                        "Grupos": ", ".join(grupos_edit) if grupos_edit else "-",
                        "Tema": tema_edit.strip(),
                        "Maestro" : maestro_edit.strip() if horario_edit else "-",
                        "Alumnos": alumnos_edit.strip(),
                        "Notas": notas_edit.strip()
                    }
                    st.session_state.actividades[edit["semana_key"]]["actividades"][edit["dia_str"]][edit["index"]] = nueva_actividad
                    guardar_datos(st.session_state.actividades)
                    del st.session_state.editando
                    st.success("✅ Cambios guardados!")
                    st.rerun()
                else:
                    st.error("❌ Debes seleccionar al menos una escuela")
        
        with col2:
            if st.form_submit_button("❌ Cancelar Edición"):
                del st.session_state.editando
                st.rerun()

# ==================================================
# EXPORTACIÓN DE DATOS
# ==================================================

def crear_excel_con_diseño(df, filename, semana, año, img_width=120, img_height=120):
    wb = Workbook()
    ws = wb.active
    ws.title = f"Semana {semana}"
    
    ws.insert_rows(1, 3)  # Insertamos 3 filas para el encabezado

    # === 1) COMBINAR CELDAS ===
    ws.merge_cells("A1:C2")  # Logo de la empresa
    ws.merge_cells("D1:I1")  # Información de la semana
    ws.merge_cells("D2:I2")
    ws.merge_cells("D3:I3")
    ws.merge_cells("K1:K3")
    ws.merge_cells("A3:C3")
    ws.merge_cells("A4:K4")

    # === 2) INSERTAR LOGO Y AJUSTAR TAMAÑO ===
    try:
        img = Image("logo.png")  # Cargar imagen del archivo
        img.width = 266  # Tamaño personalizado
        img.height = 165

        # Ajustar tamaño de las celdas al tamaño de la imagen
        ws.row_dimensions[1].height = img.height / 3  
        ws.row_dimensions[2].height = img.height / 3  

        col_width = img.width / 7  # Ajuste proporcional
        for col in range(1, 4):  # Columnas A-C (1 a 3)
            ws.column_dimensions[get_column_letter(col)].width = col_width

        # Insertar la imagen en la celda combinada
        ws.add_image(img, "A1")
    except FileNotFoundError:
        ws["A1"] = "LOGO NO ENCONTRADO"
        ws["A1"].font = Font(bold=True, size=14)
        ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    try:
        img = Image("juguete.png")  # Cargar imagen del archivo
        img.width = 578  # Tamaño personalizado
        img.height = 165

        # Ajustar tamaño de las celdas al tamaño de la imagen
        ws.row_dimensions[1].height = img.height / 3  
        ws.row_dimensions[2].height = img.height / 3  

        col_width = img.width / 7  # Ajuste proporcional
        for col in range(1, 4):  # 
            ws.column_dimensions[get_column_letter(col)].width = col_width

        # Insertar la imagen en la celda combinada
        ws.add_image(img, "J1")
    except FileNotFoundError:
        ws["K1"] = "IMAGEN NO ENCONTRADA"
        ws["K1"].font = Font(bold=True, size=14)
        ws["K1"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws["D1"] = "Programación de Actividades Semanal"
    ws["D1"].font = Font(bold=True, size=20)
    ws["D1"].alignment = Alignment(horizontal="center", vertical="center")

    # === 3) INSERTAR TEXTO DE SEMANA Y AÑO ===
    ws["D2"] = f"SEMANA {semana} - AÑO {año}"
    ws["D2"].font = Font(bold=True, size=16)
    ws["D2"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws["D3"] = "¡Intenta, Explora y Conquista!"
    ws["D3"].font = Font(bold=True, size=14)
    ws["D3"].alignment = Alignment(horizontal="center", vertical="center")

    # === 4) INSERTAR ENCABEZADOS ===
    columns = ["Semana", "Año", "Fecha", "Día", "Escuelas", "Horario", "Grupos", "Tema", "Maestro", "Alumnos", "Notas"]
    ws.append(columns)

    # === 5) INSERTAR DATOS ===
    for item in df.to_dict('records'):
        ws.append([
            item["Semana"], item["Año"], item["Fecha"], item["Día"], 
            item["Escuelas"], item["Horario"], item["Grupos"], 
            item["Tema"], item["Maestro"], item["Alumnos"], item["Notas"]
        ])

    # === 6) FORMATEAR TABLA ===
    tabla_ref = f"A5:K{ws.max_row}"  # Tabla desde la fila 5 hasta la última con datos
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

    # === 7) AJUSTE AUTOMÁTICO DE COLUMNAS (EVITANDO CELDAS COMBINADAS) ===
    for col in ws.iter_cols(min_row=5, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        col_letter = col[0].column_letter  # Obtener la letra de la columna
        max_length = max((len(str(celda.value)) if celda.value else 0) for celda in col if not isinstance(celda, MergedCell)) + 2
        ws.column_dimensions[col_letter].width = max_length

    # === 8) AJUSTAR TEXTO EN LA COLUMNA "TEMA" ===
    for celda in ws["H"]:  # Columna "Tema"
        celda.alignment = Alignment(wrap_text=True)

    # === 9) GUARDAR ARCHIVO EXCEL ===
    wb.save(filename)

# ==============================
# SECCIÓN DE EXPORTACIÓN
# ==============================

st.markdown("---")
if st.button("📤 Exportar a Excel y CSV"):
    all_data = []
    semana_data = st.session_state.actividades[semana_key]
    
    for fecha in semana_data["fechas"]:
        dia_nombre = DIAS_ESPAÑOL[semana_data["fechas"].index(fecha)]
        for act in semana_data["actividades"][fecha]:
            registro = {
                "Semana": semana,
                "Año": año,
                "Fecha": fecha,
                "Día": dia_nombre,
                **act
            }
            all_data.append(registro)
    
    df = pd.DataFrame(all_data)
    
    # Nombres de archivo
    excel_file = f"Planificacion_S{semana}_{año}.xlsx"
    csv_file = f"Planificacion_S{semana}_{año}.csv"
    
    # Guardar
    crear_excel_con_diseño(df, excel_file, semana, año, img_width=100, img_height=100)  # Aquí puedes cambiar el tamaño
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    
    # Descargas
    st.markdown("### 📥 Descargas")
    st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{base64.b64encode(open(excel_file, "rb").read()).decode()}" download="{excel_file}">Descargar Excel</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="data:text/csv;base64,{base64.b64encode(open(csv_file, "rb").read()).decode()}" download="{csv_file}">Descargar CSV</a>', unsafe_allow_html=True)
    st.success("✅ Exportación completada")

# ==================================================
# INSTRUCCIONES FINALES
# ==================================================
st.markdown("---")
st.info("""
**Guía Rápida:**
1. **Configuración:** Selecciona semana y año en la barra lateral
2. **Frase Diaria:** Edítala en el área inferior del panel lateral
3. **Actividades:** Completa el formulario principal y guarda
4. **Editar/Eliminar:** Usa los botones en la vista detallada
5. **Exportar:** Genera archivos Excel/CSV con el botón inferior
""")

# Ejecutar con:
# streamlit run planificador_final.py
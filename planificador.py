import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import base64
import os
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

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
                    "Grupos": row['Grupos'],
                    "Tema": row['Tema'],
                    "Participantes": row['Participantes'],
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
    
    # Selección de día
    dia_seleccionado = st.selectbox("Selecciona el día:", DIAS_ESPAÑOL)
    
    cols = st.columns(2)
    with cols[0]:
        escuelas = st.multiselect(
            "Selecciona escuelas:",
            ["INBLOQUET", "AEC", "RW", "AB"],
            key='escuelas'
        )
        
        grupos = st.multiselect(
            "Selecciona grupos:",
            ["RINOS", "PRESCO", "PA", "PB", "LOBOS", "PANDAS/BUFALOS", "PUMAS/DELFINES"],
            key='grupos'
        )
    
    with cols[1]:
        tema = st.text_area(
            "Descripción detallada:",
            placeholder="Ej: Taller de programación con robots",
            height=100
        )
        
        alumnos = st.text_input(
            "Nombres de asistentes:",
            placeholder="Ej: María, Carlos, Luisa"
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
                "Grupos": ", ".join(grupos) if grupos else "-",
                "Tema": tema if tema else "-",
                "Participantes": alumnos if alumnos else "-",
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
            for act in actividades:
                with st.expander("Ver detalles", expanded=False):
                    st.markdown(f"""
                    - **Escuelas:** {act['Escuelas']}
                    - **Grupos:** {act['Grupos']}
                    - **Tema:** {act['Tema']}
                    - **Participantes:** {act['Participantes']}
                    - **Notas:** {act['Notas']}
                    """)
        else:
            st.info("Sin actividades")

# ==================================================
# VISTA DETALLADA CON EDICIÓN
# ==================================================
st.markdown("---")
st.subheader("📋 Detalle Completo")

for i, dia_str in enumerate(st.session_state.actividades[semana_key]["fechas"]):
    actividades = st.session_state.actividades[semana_key]["actividades"][dia_str]
    st.markdown(f"### {DIAS_ESPAÑOL[i]} - {dia_str}")
    
    if actividades:
        for j, act in enumerate(actividades, 1):
            cols = st.columns([4, 1, 1])
            with cols[0]:
                st.markdown(f"""
                <div class="actividad-card">
                    <b>Actividad {j}</b><br>
                    ▸ Escuelas: {act['Escuelas']}<br>
                    ▸ Grupos: {act['Grupos']}<br>
                    ▸ Tema: {act['Tema']}<br>
                    ▸ Participantes: {act['Participantes']}<br>
                    ▸ Notas: {act['Notas']}
                </div>
                """, unsafe_allow_html=True)
            
            with cols[1]:
                if st.button(f"✏️ Editar", key=f"editar_{dia_str}_{j}"):
                    st.session_state.editando = {
                        "semana_key": semana_key,
                        "dia_str": dia_str,
                        "index": j-1,
                        "datos": act
                    }
            
            with cols[2]:
                if st.button(f"🗑️ Eliminar", key=f"eliminar_{dia_str}_{j}"):
                    del st.session_state.actividades[semana_key]["actividades"][dia_str][j-1]
                    guardar_datos(st.session_state.actividades)
                    st.success("✅ Actividad eliminada!")
                    st.rerun()
    else:
        st.info("No hay actividades registradas")

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
                ["RINOS", "PRESCO", "PA", "PB", "LOBOS", "PANDAS/BUFALOS", "PUMAS/DELFINES"],
                default=edit["datos"]["Grupos"].split(", ") if edit["datos"]["Grupos"] != "-" else []
            )
        
        with cols[1]:
            tema_edit = st.text_area(
                "Tema",
                value=edit["datos"]["Tema"] if edit["datos"]["Tema"] != "-" else ""
            )
        
        with cols[2]:
            alumnos_edit = st.text_input(
                "Participantes",
                value=edit["datos"]["Participantes"] if edit["datos"]["Participantes"] != "-" else ""
            )
            notas_edit = st.text_input(
                "Notas",
                value=edit["datos"]["Notas"] if edit["datos"]["Notas"] != "-" else ""
            )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.form_submit_button("💾 Guardar Cambios"):
                if escuelas_edit:
                    nueva_actividad = {
                        "Escuelas": ", ".join(escuelas_edit),
                        "Grupos": ", ".join(grupos_edit) if grupos_edit else "-",
                        "Tema": tema_edit.strip(),
                        "Participantes": alumnos_edit.strip(),
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
def crear_excel_con_diseño(df, filename):
    wb = Workbook()
    ws = wb.active
    ws.title = f"Semana {semana}"
    
    # Estilos
    header_fill = PatternFill(start_color="003366", end_color="003366", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    border = Border(left=Side(style='thin'), 
                  right=Side(style='thin'), 
                  top=Side(style='thin'), 
                  bottom=Side(style='thin'))
    
    # Encabezados
    columns = ["Semana", "Año", "Fecha", "Escuelas", "Grupos", "Tema", "Participantes", "Notas"]
    for col_num, column_title in enumerate(columns, 1):
        cell = ws.cell(row=1, column=col_num, value=column_title)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
    
    # Datos
    for row_num, item in enumerate(df.to_dict('records'), 2):
        ws.cell(row=row_num, column=1, value=item["Semana"]).border = border
        ws.cell(row=row_num, column=2, value=item["Año"]).border = border
        ws.cell(row=row_num, column=3, value=item["Fecha"]).border = border
        ws.cell(row=row_num, column=4, value=item["Escuelas"]).border = border
        ws.cell(row=row_num, column=5, value=item["Grupos"]).border = border
        ws.cell(row=row_num, column=6, value=item["Tema"]).alignment = Alignment(wrap_text=True)
        ws.cell(row=row_num, column=6).border = border
        ws.cell(row=row_num, column=7, value=item["Participantes"]).border = border
        ws.cell(row=row_num, column=8, value=item["Notas"]).border = border
    
    # Ajustar columnas
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column].width = adjusted_width
    
    wb.save(filename)

st.markdown("---")
if st.button("📤 Exportar a Excel y CSV"):
    all_data = []
    semana_data = st.session_state.actividades[semana_key]
    
    for fecha in semana_data["fechas"]:
        for act in semana_data["actividades"][fecha]:
            registro = {
                "Semana": semana,
                "Año": año,
                "Fecha": fecha,
                **act
            }
            all_data.append(registro)
    
    df = pd.DataFrame(all_data)
    
    # Nombres de archivo
    excel_file = f"Planificacion_S{semana}_{año}.xlsx"
    csv_file = f"Planificacion_S{semana}_{año}.csv"
    
    # Guardar
    crear_excel_con_diseño(df, excel_file)
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
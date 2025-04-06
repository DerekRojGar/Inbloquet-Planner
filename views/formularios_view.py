import streamlit as st
from models.actividades_model import ESCUELAS, GRUPOS_POR_ESCUELA, DIAS_ESPAÑOL
from datetime import datetime
from openpyxl.styles import Font, Alignment  # <--- Corrección de errores Pylance
from openpyxl.drawing.image import Image

def render_new_activity_form():
    st.markdown("---")
    st.subheader("📝 Nueva Actividad")
    new_activity = None
    with st.form(key='form_nueva_actividad'):
        cols = st.columns(2)
        with cols[0]:
            dia_seleccionado = st.selectbox("Selecciona el día:", DIAS_ESPAÑOL)
            # Guardamos el índice del día seleccionado para ubicar la actividad
            dia_index = DIAS_ESPAÑOL.index(dia_seleccionado)
            horario = st.text_input("Horario de la actividad:", placeholder="Ej: 8:00 a.m. - 2:00 p.m.")
            alumnos = st.text_input("Alumnos:", placeholder="Ej: Dereck, Alberto, Emma")
            escuelas_seleccionadas = st.multiselect("Selecciona escuelas:", ESCUELAS, key='nuevas_escuelas')
            if st.form_submit_button("🔍 Buscar grupos"):
                grupos_disponibles = set()
                for escuela in escuelas_seleccionadas:
                    grupos_disponibles.update(GRUPOS_POR_ESCUELA.get(escuela, []))
                st.session_state.grupos_disponibles = sorted(grupos_disponibles)
                if not st.session_state.grupos_disponibles:
                    st.warning("⚠️ No hay grupos disponibles para las escuelas seleccionadas.")
                st.rerun()
            grupos_seleccionados = st.multiselect("Selecciona grupos:", st.session_state.get("grupos_disponibles", []), key='nuevos_grupos')
        with cols[1]:
            encargado = st.text_input("Encargado", placeholder="Ej: Ivan, Gus, Caleb")
            tema = st.text_area("Descripción detallada:", placeholder="Ej: Taller de programación con robots", height=100)
            maestro = st.text_input("Maestro", placeholder="Ej: Joss, Angie, Kevin")
            notas = st.text_area("Información adicional:", placeholder="Ej: Materiales especiales requeridos")
        if st.form_submit_button("💾 Guardar Actividad"):
            if escuelas_seleccionadas:
                new_activity = {
                    "Horario": horario if horario else "-",
                    "Alumnos": alumnos if alumnos else "-",
                    "Escuelas": ", ".join(escuelas_seleccionadas),
                    "Grupos": ", ".join(grupos_seleccionados) if grupos_seleccionados else "-",
                    "Maestro": maestro if maestro else "-",
                    "Tema": tema if tema else "-",
                    "Encargado": encargado if encargado else "-",
                    "Notas": notas if notas else "-",
                    "dia_index": dia_index
                }
            else:
                st.error("❌ Debes seleccionar al menos una escuela")
    return new_activity

from models.actividades_model import (
    ESCUELAS,
    GRUPOS_POR_ESCUELA,
    DIAS_ESPAÑOL,
    guardar_datos  # Import agregado
)

# =============================================
# FORMULARIO DE EDICIÓN (VERSIÓN COMPLETA)
# =============================================
def render_edit_activity_form():
    from models.actividades_model import guardar_datos  # Import local para evitar errores
    
    st.markdown("---")
    st.subheader("✏️ Editor de Actividad")
    
    # Validar si hay una actividad seleccionada
    if "editando" not in st.session_state:
        st.error("⚠️ No hay actividad seleccionada para editar")
        return
    
    edit = st.session_state.editando
    actividad = edit["datos"]

    with st.form(key='form_edicion_actividad'):
        cols = st.columns(2)
        
        # Columna Izquierda
        with cols[0]:
            # 1. Selección de día
            dia_actual = actividad.get("Día", DIAS_ESPAÑOL[0])
            dia_index = DIAS_ESPAÑOL.index(dia_actual) if dia_actual in DIAS_ESPAÑOL else 0
            dia_seleccionado = st.selectbox(
                "Día:", 
                DIAS_ESPAÑOL, 
                index=dia_index,
                key="edit_dia"
            )
            
            # 2. Horario y alumnos
            horario = st.text_input(
                "Horario:", 
                value=str(actividad.get("Horario", "-")).replace("-", "").strip(),
                key="edit_horario"
            )
            
            # 3. Escuelas y grupos
            escuelas_actuales = [e.strip() for e in str(actividad.get("Escuelas", "")).split(",") if e.strip() in ESCUELAS]
            escuelas_edit = st.multiselect(
                "Escuelas:", 
                ESCUELAS, 
                default=escuelas_actuales,
                key="edit_escuelas"
            )
            
            # Actualizar grupos disponibles
            if st.form_submit_button("🔄 Actualizar grupos"):
                grupos_disponibles = set()
                for escuela in escuelas_edit:
                    grupos_disponibles.update(GRUPOS_POR_ESCUELA.get(escuela, []))
                st.session_state.grupos_edit_disponibles = sorted(grupos_disponibles)
                st.rerun()
            
            # Selección de grupos
            grupos_disponibles = st.session_state.get("grupos_edit_disponibles", [])
            grupos_actuales = [g.strip() for g in str(actividad.get("Grupos", "")).split(",") if g.strip() in grupos_disponibles]
            grupos_edit = st.multiselect(
                "Grupos:", 
                grupos_disponibles,
                default=grupos_actuales,
                key="edit_grupos"
            )
            
            # 4. Alumnos
            alumnos_edit = st.text_input(
                "Alumnos:", 
                value=str(actividad.get("Alumnos", "-")).replace("-", "").strip(),
                key="edit_alumnos"
            )

        # Columna Derecha
        with cols[1]:
            # 5. Responsables
            encargado_edit = st.text_input(
                "Encargado:", 
                value=str(actividad.get("Encargado", "-")).replace("-", "").strip(),
                key="edit_encargado"
            )
            maestro_edit = st.text_input(
                "Maestro:", 
                value=str(actividad.get("Maestro", "-")).replace("-", "").strip(),
                key="edit_maestro"
            )
            
            # 6. Detalles de contenido
            tema_edit = st.text_area(
                "Tema:", 
                value=str(actividad.get("Tema", "-")).replace("-", "").strip(),
                height=100,
                key="edit_tema"
            )
            
            # 7. Notas adicionales
            notas_edit = st.text_area(
                "Notas:", 
                value=str(actividad.get("Notas", "-")).replace("-", "").strip(),
                height=100,
                key="edit_notas"
            )

        # Botones de acción
        submit_cols = st.columns([1, 1, 3])
        with submit_cols[0]:
            submit = st.form_submit_button("💾 Guardar Cambios")
        with submit_cols[1]:
            cancelar = st.form_submit_button("❌ Cancelar")

    if submit:
        if escuelas_edit:
            nueva_actividad = {
                "Día": dia_seleccionado,
                "Horario": horario.strip() or "-",
                "Escuelas": ", ".join(escuelas_edit),
                "Grupos": ", ".join(grupos_edit) if grupos_edit else "-",
                "Alumnos": alumnos_edit.strip() or "-",
                "Encargado": encargado_edit.strip() or "-",
                "Maestro": maestro_edit.strip() or "-",
                "Tema": tema_edit.strip() or "-",
                "Notas": notas_edit.strip() or "-"
            }
            
            # Actualizar datos
            st.session_state.actividades[edit["semana_key"]]["actividades"][edit["dia_str"]][edit["index"]] = nueva_actividad
            
            # Guardar cambios persistentes
            guardar_datos(st.session_state.actividades)
            
            # Cerrar todos los modales
            for key in ['editando', 'selected_activity']:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.rerun()  # Recarga completa
        else:
            st.error("❌ Debes seleccionar al menos una escuela")

    if cancelar:
        del st.session_state.editando
        st.rerun()

def render_export_view(semana_key, semana, año):
    import base64
    import streamlit as st
    from models.export_model import crear_excel_con_diseño
    import pandas as pd
    from datetime import datetime

    st.markdown("---")
    if st.button("📤 Exportar a Excel y CSV", key="export_excel_csv"):
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
        excel_file = f"Planificacion_S{semana}_{año}.xlsx"
        csv_file = f"Planificacion_S{semana}_{año}.csv"
        crear_excel_con_diseño(df, excel_file, semana, año)
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        excel_base64 = base64.b64encode(open(excel_file, "rb").read()).decode()
        csv_base64 = base64.b64encode(open(csv_file, "rb").read()).decode()
        st.markdown("### 📥 Descargas")
        st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_base64}" download="{excel_file}">Descargar Excel</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="data:text/csv;base64,{csv_base64}" download="{csv_file}">Descargar CSV</a>', unsafe_allow_html=True)
        st.success("✅ Exportación completada")
    if st.button("📤 Exportar Semanas Totales", key="export_all_weeks"):
        from openpyxl import Workbook
        wb = Workbook()
        if "Sheet" in wb.sheetnames:
            wb.remove(wb["Sheet"])
        semanas_ordenadas = sorted(
            st.session_state.actividades.keys(),
            key=lambda k: (int(k.split("-S")[0]), int(k.split("-S")[1]))
        )
        total_semanas = len(semanas_ordenadas)
        progreso = st.progress(0)
        for idx, s_key in enumerate(semanas_ordenadas):
            año_str, semana_str = s_key.split("-S")
            anio_int = int(año_str)
            semana_int = int(semana_str)
            semana_data = st.session_state.actividades[s_key]
            all_data = []
            for fecha in semana_data["fechas"]:
                dia_nombre = DIAS_ESPAÑOL[semana_data["fechas"].index(fecha)]
                for act in semana_data["actividades"][fecha]:
                    registro = {
                        "Semana": semana_int,
                        "Año": anio_int,
                        "Fecha": fecha,
                        "Día": dia_nombre,
                        **act
                    }
                    all_data.append(registro)
            if all_data:
                df = pd.DataFrame(all_data)
                sheet_name = f"S{semana_int}_{anio_int}"
                ws = wb.create_sheet(title=sheet_name)
                ws.insert_rows(1, 3)
                ws.merge_cells("A1:B3")
                ws.merge_cells("D1:I1")
                ws.merge_cells("D2:I2")
                ws.merge_cells("D3:I3")
                ws.merge_cells("J1:J3")
                ws.merge_cells("A4:K4")
                try:
                    from openpyxl.drawing.image import Image
                    img1 = Image("InbloquetD.png")
                    img1.width = 150
                    img1.height = 140
                    ws.add_image(img1, "A1")
                except FileNotFoundError:
                    ws["A1"] = "LOGO NO ENCONTRADO"
                    ws["A1"].font = Font(bold=True, size=14)
                    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
                try:
                    img2 = Image("rocket.png")
                    img2.width = 90
                    img2.height = 140
                    ws.add_image(img2, "J1")
                except FileNotFoundError:
                    ws["K1"] = "IMAGEN NO ENCONTRADA"
                    ws["K1"].font = Font(bold=True, size=14)
                    ws["K1"].alignment = Alignment(horizontal="center", vertical="center")
                ws["D1"] = "Programación de Actividades Semanal"
                ws["D1"].font = Font(bold=True, size=20)
                ws["D1"].alignment = Alignment(horizontal="center", vertical="center")
                ws["D2"] = f"SEMANA {semana_int} - AÑO {anio_int}"
                ws["D2"].font = Font(bold=True, size=16)
                ws["D2"].alignment = Alignment(horizontal="center", vertical="center")
                ws["D3"] = "¡Intenta, Explora y Conquista!"
                ws["D3"].font = Font(bold=True, size=14)
                ws["D3"].alignment = Alignment(horizontal="center", vertical="center")
                df["Fecha"] = df.apply(lambda row: f"{row['Día']} {int(row['Fecha'][:2])} de {datetime.strptime(row['Fecha'], '%d/%m').strftime('%B')} del {row['Año']}", axis=1)
                df["Fecha"] = df["Fecha"].apply(lambda x: x.replace(x.split()[3], x.split()[3].capitalize()))
                df = df.drop(columns=["Día", "Año"])
                column_order = ["Semana", "Fecha", "Horario", "Alumnos", "Escuelas", "Grupos", "Maestro", "Tema", "Encargado", "Notas"]
                df = df[column_order]
                ws.append(df.columns.tolist())
                for item in df.to_dict('records'):
                    ws.append(list(item.values()))
                from openpyxl.worksheet.table import Table, TableStyleInfo
                last_row = ws.max_row
                tabla_ref = f"A5:J{last_row}"
                tabla = Table(displayName=f"TablaActividades_{sheet_name}", ref=tabla_ref)
                estilo_tabla = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
                tabla.tableStyleInfo = estilo_tabla
                ws.add_table(tabla)
                for col in ws.iter_cols(min_row=5, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
                    col_letter = col[0].column_letter
                    max_length = max((len(str(celda.value)) if celda.value else 0) for celda in col) + 2
                    ws.column_dimensions[col_letter].width = max_length
            progreso.progress((idx + 1) / total_semanas)
        excel_file = "Planificacion General de Semanas.xlsx"
        wb.save(excel_file)
        progreso.empty()
        with open(excel_file, "rb") as f:
            excel_bytes = f.read()
        excel_base64 = base64.b64encode(excel_bytes).decode()
        st.markdown("### 📥 Descargas")
        st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_base64}" download="{excel_file}">Descargar Excel</a>', unsafe_allow_html=True)
        st.success("✅ Exportación completada")

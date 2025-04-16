import streamlit as st
from views.alumnos.detalle import render_detalle_alumno
from views.alumnos.formulario import render_formulario_alumno
from models.export_alumnos import exportar_alumno_inbloquet, exportar_todos_los_alumnos_inbloquet
import pandas as pd
import base64
import os

def render_lista_alumnos(alumnos, busqueda):
    """
    Renderiza la lista de alumnos filtrados, con filtros de ordenamiento y botones para:
      - Ver detalles individualmente
      - Editar o eliminar alumnos
      - Exportar la ficha del alumno a Excel (con el diseño Inbloquet, en formato tabla con colores corporativos)
      - Exportar TODOS los alumnos a Excel, cada uno en una hoja, con el mismo diseño.
    """
    # Filtro de ordenamiento
    col_sort, _ = st.columns([2, 2])
    # Por defecto, selecciona "ID"
    criterio = col_sort.selectbox("📋 Ordenar alumnos por:", ["A-Z", "Estado de pago", "ID"], key="ordenamiento", index=2)

    if criterio == "A-Z":
        alumnos = sorted(alumnos, key=lambda x: x.get("Nombre", "").lower())
    elif criterio == "Estado de pago":
        # Se asume que el estado de pago está en la llave "Inscripción"
        alumnos = sorted(alumnos, key=lambda x: x.get("Inscripción", ""))
    elif criterio == "ID":
        alumnos = sorted(alumnos, key=lambda x: int(x.get("Matricula", 0)))

    # Filtrado según búsqueda
    alumnos_filtrados = [
        a for a in alumnos
        if busqueda.lower() in str(a.get("Nombre", "")).lower() or busqueda in str(a.get("Matricula", ""))
    ]

    with st.expander("📋 Listado de Alumnos", expanded=True):
        for alumno in alumnos_filtrados:
            matricula = alumno.get("Matricula", "")
            # Se crean 7 columnas:
            # [0]: ID, [1]: Nombre, [2]: Estado de pago, [3]: Ver detalles, [4]: Editar, [5]: Eliminar, [6]: Exportar individual
            cols = st.columns([1, 3, 2, 2, 1, 1, 1, 1])
            cols[0].markdown(f"**{matricula}**")
            cols[1].markdown(f"**{alumno.get('Nombre', '')}**")
            
            # Estado de inscripción (status de pago) con indicador de color
            estado_insc = alumno.get("Inscripción", "Pagada")
            if estado_insc == "Pagada":
                color_insc = "#4BB1E0"
            elif estado_insc == "Condonada":
                color_insc = "#FFD700"
            elif estado_insc == "Pendiente":
                color_insc = "#FF4B4B"
            else:
                color_insc = "#4BB1E0"
            cols[2].markdown(f"<span style='color: {color_insc};'>●</span> {estado_insc}",
                              unsafe_allow_html=True)

            # Estado activo/inactivo
            vigente = alumno.get("Vigente", "activo")
            color_vigente = "#4BB543" if vigente == "activo" else "#FF4B4B"
            cols[3].markdown(f"<span style='color: {color_vigente};'>●</span> {vigente.capitalize()}", unsafe_allow_html=True)

            # Botón para ver detalles (si se pulsa, guarda el alumno en sesión)
            if cols[4].button("👁️", key=f"ver_{matricula}"):
                st.session_state.alumno_detalle = alumno
                st.session_state.modo_edicion = None

            # Botón para editar (pone en modo edición)
            if cols[5].button("✏️", key=f"editar_{matricula}"):
                st.session_state.modo_edicion = "editar"
                st.session_state.alumno_editando = alumno
                st.session_state.alumno_detalle = None
                st.rerun()

            # Botón para eliminar el alumno (se elimina de la lista y se recarga la app)
            if cols[6].button("🗑️", key=f"eliminar_{matricula}"):
                nuevos_alumnos = [a for a in st.session_state.alumnos if a.get("Matricula") != matricula]
                st.session_state.alumnos = nuevos_alumnos
                st.success(f"Alumno {matricula} eliminado.")
                st.rerun()

            # Botón para exportar individualmente la ficha del alumno a Excel
            if cols[7].button("📤 Exportar", key=f"exportar_{matricula}"):
                filename = f"Ficha_{matricula}.xlsx"
                exportar_alumno_inbloquet(alumno, filename)
                with open(filename, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                st.markdown(
                    f"⬇️ [Descargar Excel](data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64})",
                    unsafe_allow_html=True
                )
                os.remove(filename)

            # Mostrar la ficha de detalles si el alumno está seleccionado y no se está editando
            if st.session_state.get("alumno_detalle") == alumno and not st.session_state.get("modo_edicion"):
                render_detalle_alumno(alumno)

    st.markdown("---")
    # Botón global: exportar todos los alumnos a Excel (cada alumno en una hoja, con formato de tabla y diseño Inbloquet)
    if st.button("📥 Exportar TODOS los alumnos a Excel"):
        filename = "Alumnos_Inbloquet.xlsx"
        exportar_todos_los_alumnos_inbloquet(alumnos, filename)
        with open(filename, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f"⬇️ [Descargar Excel](data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64})",
            unsafe_allow_html=True
        )
        os.remove(filename)
        st.success("✅ Exportación completada")

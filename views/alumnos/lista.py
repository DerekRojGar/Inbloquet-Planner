import streamlit as st
from views.alumnos.detalle import render_detalle_alumno  # Asegurarse de tener esta importación

def render_lista_alumnos(alumnos, busqueda):
    """
    Renderiza la lista de alumnos filtrados según la búsqueda.
    Cada alumno se muestra con sus botones para ver/ocultar detalles, editar y eliminar.
    """
    # Filtrar alumnos según el término de búsqueda
    alumnos_filtrados = [
        a for a in alumnos 
        if busqueda.lower() in str(a.get('Nombre', '')).lower() or 
           busqueda in str(a.get('Matricula', ''))
    ]

    with st.expander("📋 Listado de Alumnos", expanded=True):
        for alumno in alumnos_filtrados:
            matricula = alumno.get('Matricula', '')
            cols = st.columns([1, 3, 2, 2, 2, 3])
            cols[0].markdown(f"**{matricula}**")
            cols[1].markdown(f"**{alumno.get('Nombre', '')}**")

            # Estado de inscripción
            estado_insc = alumno.get('Inscripción', 'Pagada')
            color_insc = "#4BB1E0" if estado_insc == "Pagada" else "#FF4B4B"
            cols[2].markdown(f"<span style='color: {color_insc};'>●</span> {estado_insc}", unsafe_allow_html=True)
            
            # Botón para alternar detalles
            detalles_key = f"detalles_{matricula}"
            if detalles_key not in st.session_state:
                st.session_state[detalles_key] = False

            toggle_label = "Ver detalles" if not st.session_state[detalles_key] else "Ocultar detalles"
            if cols[3].button(toggle_label, key=f"toggle_{matricula}"):
                st.session_state[detalles_key] = not st.session_state[detalles_key]
            
            # Botón para editar
            if cols[4].button("✏️", key=f"editar_{matricula}"):
                st.session_state.modo_edicion = 'editar'
                st.session_state.alumno_editando = alumno

            # Botón para eliminar
            if cols[5].button("🗑️", key=f"eliminar_{matricula}"):
                # Confirma y elimina; por simplicidad, se elimina de st.session_state.alumnos
                nuevos_alumnos = [a for a in st.session_state.alumnos if a.get('Matricula', '') != matricula]
                st.session_state.alumnos = nuevos_alumnos
                st.success(f"Alumno {matricula} eliminado.")
                st.rerun()
            
            # Si los detalles están activados, los desplegamos debajo
            if st.session_state[detalles_key]:
                with st.container():
                    st.markdown("---")
                    render_detalle_alumno(alumno)
                    st.markdown("---")

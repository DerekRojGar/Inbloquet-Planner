import streamlit as st
from models.actividades_model import DIAS_ESPAÑOL

def render_calendar(semana_key):
    actividades = st.session_state.actividades[semana_key]
    st.subheader("🗓️ Vista Semanal")
    col1, col2, col3 = st.columns([6, 1, 1])
    with col1:
        st.markdown("****")
    with col2:
        if st.button("📂 Expandir Todo"):
            st.session_state.expanded_state = True
            st.rerun()
    with col3:
        if st.button("📂 Contraer Todo"):
            st.session_state.expanded_state = False
            st.rerun()

    # Crear columnas con contenedores para cada día
    cols = st.columns(6)
    for i, col in enumerate(cols):
        with col:
            with st.container():
                st.markdown(f"<div class='calendar-column'><strong>{DIAS_ESPAÑOL[i]}</strong><br><small>{actividades['fechas'][i]}</small></div>", unsafe_allow_html=True)
                day_acts = actividades["actividades"][actividades["fechas"][i]]
                if day_acts:
                    for idx, act in enumerate(day_acts):
                        with st.expander(label=f"{act['Escuelas']}: {act['Grupos']}", expanded=st.session_state.get("expanded_state", False)):
                            st.markdown(f"""
                            - **Horario:** {act['Horario']}
                            - **Alumnos:** {act['Alumnos']}
                            - **Maestro:** {act['Maestro']}
                            - **Tema:** {act['Tema']}
                            - **Encargado:** {act['Encargado']}
                            """)
                            if st.button("Detalles", key=f"det_{actividades['fechas'][i]}_{idx}"):
                                st.session_state.selected_activity = {
                                    "semana_key": semana_key,
                                    "dia_str": actividades["fechas"][i],
                                    "index": idx,
                                    "datos": act
                                }
                                st.rerun()
                else:
                    st.info("Sin actividades")
    
def render_activity_detail():
    if "selected_activity" not in st.session_state:
        return
    
    selected = st.session_state.selected_activity
    act = selected["datos"]
    
    with st.expander("📋 Detalle de Actividad", expanded=True):
        cols = st.columns([4, 1])
        with cols[0]:
            st.markdown(f"### {act['Horario']}")
        with cols[1]:
            if st.button("❌"):
                del st.session_state.selected_activity
                st.rerun()
        
        st.markdown(f"""
        - **Alumnos:** {act['Alumnos']}
        - **Escuelas:** {act['Escuelas']}
        - **Grupos:** {act['Grupos']}
        - **Maestro:** {act['Maestro']}
        - **Tema:** {act['Tema']}
        - **Encargado:** {act['Encargado']}
        - **Notas:** {act['Notas']}
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Editar"):
                st.session_state.editando = {
                    "semana_key": selected["semana_key"],
                    "dia_str": selected["dia_str"],
                    "index": selected["index"],
                    "datos": act
                }
                del st.session_state.selected_activity  # Cerrar detalle al editar
                st.rerun()
        with col2:
            if st.button("🗑️ Eliminar"):
                semana_key = selected["semana_key"]
                dia_str = selected["dia_str"]
                index = selected["index"]
                del st.session_state.actividades[semana_key]["actividades"][dia_str][index]
                from models.actividades_model import guardar_datos
                guardar_datos(st.session_state.actividades)
                del st.session_state.selected_activity
                st.rerun()
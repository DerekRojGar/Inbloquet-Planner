import streamlit as st
import base64

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception as e:
        st.error(f"Error al cargar la imagen: {e}")
        return ""

def run_app():
    from views.global_styles import render_css
    render_css()
    
    # Navegación principal
    with st.sidebar:
        opcion = st.radio(
            "Módulos INBLOQUET",
            ["📅 Planificación", "👥 Gestión de Alumnos"],
            key="nav_principal"
        )
    
    # Cargar módulo de alumnos si está seleccionado
    if opcion == "👥 Gestión de Alumnos":
        from controllers.alumnos_controller import inicializar_estado_alumnos
        from views.alumnos_view import render_alumnos_view
        
        inicializar_estado_alumnos()
        render_alumnos_view()
        return  # Salir temprano para evitar cargar lógica de planificación

    # ==============================================
    # LÓGICA ORIGINAL DE PLANIFICACIÓN (solo si no estamos en alumnos)
    # ==============================================
    
    from controllers.actividades_controller import initialize_state
    initialize_state()
    
    from views.sidebar_view import render_sidebar
    semana, año = render_sidebar(st.session_state.get("frase_global", ""))
    
    from models.actividades_model import generar_semana
    semana_key = f"{año}-S{semana}"
    if semana_key not in st.session_state.actividades:
        fechas = [dia.strftime("%d/%m") for dia in generar_semana(año, semana)]
        st.session_state.actividades[semana_key] = {"fechas": fechas, "actividades": {fecha: [] for fecha in fechas}}
    
    # Cabecera principal
    logo_base64 = get_base64_image("Inbloquet.png")
    st.markdown(f"""
    <div class="header-container">
        <h1 class="main-title">Planificación Semanal</h1>
        <img src="data:image/png;base64,{logo_base64}" class="inbloquet-logo" alt="Logo Inbloquet" />
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if "frase_global" in st.session_state and st.session_state.frase_global:
        st.markdown(f'<div class="frase-dia">📌 {st.session_state.frase_global}</div>', unsafe_allow_html=True)
    
    from views.calendario_view import render_calendar, render_activity_detail
    render_calendar(semana_key)
    
    if "selected_activity" in st.session_state:
        render_activity_detail()
    
    from views.formularios_view import render_new_activity_form, render_edit_activity_form, render_export_view
    if "editando" in st.session_state:
        render_edit_activity_form()
    
    nueva_actividad = render_new_activity_form()
    if nueva_actividad:
        dia_index = nueva_actividad.pop("dia_index")
        fecha_key = st.session_state.actividades[semana_key]["fechas"][dia_index]
        st.session_state.actividades[semana_key]["actividades"][fecha_key].append(nueva_actividad)
        from models.actividades_model import guardar_datos
        guardar_datos(st.session_state.actividades)
        st.success("✅ Actividad registrada exitosamente!")
        st.rerun()
    
    render_export_view(semana_key, semana, año)

if __name__ == "__main__":
    run_app()
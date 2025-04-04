# controllers/ui_controller.py
import streamlit as st
from views.global_styles import render_css
from views.sidebar_view import render_sidebar
from views.calendario_view import render_calendar, render_activity_detail
from views.formularios_view import render_new_activity_form, render_edit_activity_form, render_export_view
from controllers.actividades_controller import initialize_state
from models.actividades_model import generar_semana

def run_app():
    # Renderizar los estilos globales
    render_css()
    
    # Inicializar el estado de la aplicación
    initialize_state()
    
    # Obtener la configuración (usando la semana actual ya configurada)
    semana, año = render_sidebar(st.session_state.get("frase_global", ""))
    
    # Crear o inicializar la estructura de actividades para la semana actual
    semana_key = f"{año}-S{semana}"
    if semana_key not in st.session_state.actividades:
        fechas = [dia.strftime("%d/%m") for dia in generar_semana(año, semana)]
        st.session_state.actividades[semana_key] = {"fechas": fechas, "actividades": {fecha: [] for fecha in fechas}}
    
    # Título principal y visualización de la frase inspiradora
    st.image("inb_logo.png", width=75)
    st.title("Planificación Semanal")

    st.markdown("---")
    if "frase_global" in st.session_state and st.session_state.frase_global:
        st.markdown(f'<div class="frase-dia">📌 {st.session_state.frase_global}</div>', unsafe_allow_html=True)
    
    # Renderizar la vista del calendario
    render_calendar(semana_key)
    
    # Mostrar detalles de la actividad si se seleccionó alguna
    if "selected_activity" in st.session_state:
        render_activity_detail()
    
    # Renderizar el formulario de edición si se está editando
    if "editando" in st.session_state:
        render_edit_activity_form()
    
    # Renderizar el formulario para crear una nueva actividad
    nueva_actividad = render_new_activity_form()
    if nueva_actividad:
        dia_index = nueva_actividad.pop("dia_index")
        fecha_key = st.session_state.actividades[semana_key]["fechas"][dia_index]
        st.session_state.actividades[semana_key]["actividades"][fecha_key].append(nueva_actividad)
        from models.actividades_model import guardar_datos
        guardar_datos(st.session_state.actividades)
        st.success("✅ Actividad registrada exitosamente!")
        st.rerun()
    
    # Renderizar la sección de exportación (descarga de Excel y CSV)
    render_export_view(semana_key, semana, año)

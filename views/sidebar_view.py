import streamlit as st
from datetime import datetime

def render_css():
    """
    Puedes dejar esta función si la usas en otro lado;
    de lo contrario, podrías eliminarla si no la llamas.
    """
    st.markdown("""
    <style>
    .logo-sidebar {
        max-width: 200px;
        max-height: 100px;
        margin: 20px;
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
    </style>
    """, unsafe_allow_html=True)

# Obtener la semana y año actual a partir de la fecha del sistema
current_week = datetime.today().isocalendar()[1]
current_year = datetime.today().year

def render_sidebar(frase_actual):
    with st.sidebar:
        # Imagen rocket (foto de perfil) - si quieres usar la clase .rocket-logo, utiliza la API de st.markdown
        st.image("rocket.png", width=80)
        st.header("⚙️ Configuración")
        
        # Inputs para seleccionar semana y año
        semana = st.number_input("Número de Semana", min_value=1, max_value=53, value=current_week, key="num_semana")
        año = st.number_input("Año", min_value=current_year-1, max_value=current_year+5, value=current_year, key="num_año")
        st.markdown("---")
        
        # Frase inspiradora
        nueva_frase = st.text_area("✍️ Frase inspiradora del día:", value=frase_actual)
        if st.button("💾 Guardar Frase"):
            st.session_state.frase_global = nueva_frase
            st.rerun()
        
        # Botones para Expandir y Contraer Todo, ubicados debajo de "Guardar Frase"
        if st.button("📂 Expandir Todo", key="expandir_todo"):
            st.session_state.expanded_state = True
            st.rerun()
        if st.button("📂 Contraer Todo", key="contraer_todo"):
            st.session_state.expanded_state = False
            st.rerun()
    return semana, año

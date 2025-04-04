import streamlit as st
from datetime import datetime

def render_css():
    st.markdown("""
    <style>
    .logo-sidebar {
        max-width: 200px;
        max-hight: 100px;
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
        st.image("rocket.png", width=250)
        st.header("⚙️ Configuración")
        # Se actualizan los valores por defecto para usar la semana y año actuales
        semana = st.number_input("Número de Semana", min_value=1, max_value=53, value=current_week, key="num_semana")
        año = st.number_input("Año", min_value=current_year-1, max_value=current_year+5, value=current_year, key="num_año")
        st.markdown("---")
        nueva_frase = st.text_area("✍️ Frase inspiradora del día:", value=frase_actual)
        if st.button("💾 Guardar Frase"):
            st.session_state.frase_global = nueva_frase
            st.rerun()
    return semana, año


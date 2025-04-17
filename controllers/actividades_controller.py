import streamlit as st
from models.actividades_model import cargar_datos, guardar_datos
from datetime import datetime

def initialize_state():
    if 'actividades' not in st.session_state:
        st.session_state.actividades = cargar_datos()
    if "expanded_state" not in st.session_state:
        st.session_state.expanded_state = False
    # Inicializar año y semana si no existen
    if "num_año" not in st.session_state:
        st.session_state.num_año = datetime.now().year
    if "num_semana" not in st.session_state:
        st.session_state.num_semana = datetime.now().isocalendar()[1]

def save_data(actividades):
    guardar_datos(actividades)

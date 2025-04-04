import streamlit as st
from models.actividades_model import cargar_datos, guardar_datos

def initialize_state():
    if 'actividades' not in st.session_state:
        st.session_state.actividades = cargar_datos()
    if "expanded_state" not in st.session_state:
        st.session_state.expanded_state = False

def save_data(actividades):
    guardar_datos(actividades)

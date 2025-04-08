import streamlit as st
from models.alumnos_model import cargar_alumnos, guardar_alumnos

def inicializar_estado_alumnos():
    if 'alumnos' not in st.session_state:
        st.session_state.alumnos = cargar_alumnos()
    if 'alumno_editando' not in st.session_state:
        st.session_state.alumno_editando = None

def eliminar_alumno(matricula):
    st.session_state.alumnos = [a for a in st.session_state.alumnos if a['matricula'] != matricula]
    guardar_alumnos(st.session_state.alumnos)
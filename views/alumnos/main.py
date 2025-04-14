import streamlit as st
from views.alumnos.lista import render_lista_alumnos
from views.alumnos.detalle import render_detalle_alumno
from views.alumnos.formulario import render_formulario_alumno

def render_alumnos_view():
    """Vista principal de gestión de alumnos, compuesta de sus diferentes componentes"""
    st.subheader("👥 Gestión de Alumnos")
    
    # Si estamos en modo de edición o creación, mostrar el formulario por encima
    if st.session_state.get('modo_edicion'):
        render_formulario_alumno()
    
    # Mostrar el botón y la búsqueda siempre (para agregar o buscar)
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("➕ Nuevo Alumno"):
            st.session_state.modo_edicion = 'crear'
            st.session_state.alumno_detalle = None
            st.rerun()
  # Refrescar para mostrar el formulario
    with col2:
        busqueda = st.text_input("Buscar alumno:")
    
    # Renderizar la lista de alumnos debajo del formulario (o de la cabecera, en caso de que no se esté editando)
    render_lista_alumnos(st.session_state.alumnos, busqueda)
    
    # Si se ha seleccionado un alumno para ver los detalles, mostrarlos al final
    if st.session_state.get('alumno_detalle'):
        render_detalle_alumno(st.session_state.alumno_detalle)

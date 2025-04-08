import streamlit as st
from datetime import datetime
import pandas as pd

CAMPOS_ALUMNO = [
    'matricula', 'nombre', 'sexo', 'fecha_inscripcion', 
    'id_grado', 'id_nivel_educativo', 'estado_matricula', 
    'curso', 'paquete', 'metodo_pago', 'fecha_nacimiento',
    'fecha_pago', 'monto_pago', 'saldo_pendiente'
]

def render_alumnos_view():
    st.subheader("👥 Gestión de Alumnos")
    
    # Botones principales
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("➕ Nuevo Alumno"):
            st.session_state.modo_edicion = 'crear'
            st.session_state.alumno_detalle = None
    
    # Búsqueda
    with col2:
        busqueda = st.text_input("Buscar alumno:")
    
    # Filtrado
    alumnos_filtrados = [
        a for a in st.session_state.alumnos 
        if busqueda.lower() in str(a['nombre']).lower() or 
           busqueda in str(a['matricula'])
    ]
    
    # Tabla de alumnos mejorada
    with st.expander("📋 Listado de Alumnos", expanded=True):
        for alumno in alumnos_filtrados:
            cols = st.columns([1, 3, 2, 2, 2, 2])
            cols[0].markdown(f"**{alumno.get('matricula', '')}**")
            cols[1].markdown(f"**{alumno.get('nombre', '')}**")
            cols[2].markdown(f"**{alumno.get('curso', '')}**")
            estado_color = "#4BB1E0" if alumno.get('estado_matricula') == 'activo' else "#FF4B4B"
            cols[3].markdown(f"<span style='color: {estado_color};'>●</span> {alumno.get('estado_matricula', '')}", unsafe_allow_html=True)
            
            if cols[4].button("👁️", key=f"ver_{alumno['matricula']}"):
                st.session_state.alumno_detalle = alumno
            if cols[5].button("✏️", key=f"editar_{alumno['matricula']}"):
                st.session_state.modo_edicion = 'editar'
                st.session_state.alumno_editando = alumno

    # Detalle del alumno
    if st.session_state.get('alumno_detalle'):
        render_detalle_alumno(st.session_state.alumno_detalle)

    # Formulario de edición/creación
    if st.session_state.get('modo_edicion'):
        render_formulario_alumno()

def render_detalle_alumno(alumno):
    with st.expander(f"📄 Detalle completo de {alumno.get('nombre', '')}", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            st.markdown("### Información Básica")
            st.markdown(f"**Matrícula:** {alumno.get('matricula', '')}")
            st.markdown(f"**Nombre:** {alumno.get('nombre', '')}")
            st.markdown(f"**Sexo:** {alumno.get('sexo', '')}")
            st.markdown(f"**Fecha Nacimiento:** {alumno.get('fecha_nacimiento', '')}")
        
        with cols[1]:
            st.markdown("### Datos Académicos")
            st.markdown(f"**Grado:** {alumno.get('id_grado', '')}")
            st.markdown(f"**Nivel:** {alumno.get('id_nivel_educativo', '')}")
            st.markdown(f"**Curso:** {alumno.get('curso', '')}")
            st.markdown(f"**Paquete:** {alumno.get('paquete', '')}")
        
        st.markdown("### Información Financiera")
        cols_fin = st.columns(3)
        cols_fin[0].markdown(f"**Método Pago:** {alumno.get('metodo_pago', '')}")
        cols_fin[1].markdown(f"**Último Pago:** {alumno.get('fecha_pago', '')}")
        cols_fin[2].markdown(f"**Saldo Pendiente:** ${alumno.get('saldo_pendiente', '')}")

def render_formulario_alumno():
    with st.form(key='form_alumno'):
        alumno = st.session_state.alumno_editando if st.session_state.modo_edicion == 'editar' else {}
        
        # Campos en 2 columnas
        col1, col2 = st.columns(2)
        
        with col1:
            matricula = st.text_input("Matrícula*", value=alumno.get('matricula', ''))
            nombre = st.text_input("Nombre completo*", value=alumno.get('nombre', ''))
            sexo = st.selectbox("Sexo", ['', 'h', 'm'], index=['', 'h', 'm'].index(alumno.get('sexo', '')))
            id_grado = st.text_input("ID Grado", value=alumno.get('id_grado', ''))
            id_nivel = st.text_input("ID Nivel Educativo", value=alumno.get('id_nivel_educativo', ''))
        
        with col2:
            estado = st.selectbox("Estado*", ['activo', 'inactivo'], index=0 if alumno.get('estado_matricula') == 'activo' else 1)
            curso = st.text_input("Curso", value=alumno.get('curso', ''))
            paquete = st.text_input("Paquete", value=alumno.get('paquete', ''))
            metodo_pago = st.selectbox("Método Pago", ['', 'Efectivo', 'Transferencia', 'Depósito'], 
                                      index=['', 'Efectivo', 'Transferencia', 'Depósito'].index(alumno.get('metodo_pago', '')))
        
        # Campos adicionales
        fecha_inscripcion = st.date_input("Fecha Inscripción", 
                                        value=pd.to_datetime(alumno.get('fecha_inscripcion')) if alumno.get('fecha_inscripcion') else None)
        fecha_nacimiento = st.date_input("Fecha Nacimiento", 
                                       value=pd.to_datetime(alumno.get('fecha_nacimiento')) if alumno.get('fecha_nacimiento') else None)
        fecha_pago = st.date_input("Última Fecha Pago", 
                                 value=pd.to_datetime(alumno.get('fecha_pago')) if alumno.get('fecha_pago') else None)
        
        # Campos numéricos corregidos
        monto_pago = st.number_input(
            "Monto Último Pago",
            value=float(alumno.get('monto_pago', 0)) if alumno.get('monto_pago') else 0.0
        )
        
        saldo_pendiente = st.number_input(
            "Saldo Pendiente",
            value=float(alumno.get('saldo_pendiente', 0)) if alumno.get('saldo_pendiente') else 0.0
        )

        # Validación y guardado
        if st.form_submit_button("💾 Guardar"):
            if not matricula or not nombre:
                st.error("Matrícula y Nombre son campos obligatorios")
                return
            
            nuevo_alumno = {
                'matricula': matricula,
                'nombre': nombre,
                'sexo': sexo,
                'id_grado': id_grado,
                'id_nivel_educativo': id_nivel,
                'estado_matricula': estado,
                'curso': curso,
                'paquete': paquete,
                'metodo_pago': metodo_pago,
                'fecha_inscripcion': fecha_inscripcion.strftime("%d/%m/%Y") if fecha_inscripcion else '',
                'fecha_nacimiento': fecha_nacimiento.strftime("%d/%m/%Y") if fecha_nacimiento else '',
                'fecha_pago': fecha_pago.strftime("%d/%m/%Y") if fecha_pago else '',
                'monto_pago': monto_pago,
                'saldo_pendiente': saldo_pendiente
            }
            
            # Lógica de guardado
            if st.session_state.modo_edicion == 'crear':
                st.session_state.alumnos.append(nuevo_alumno)
            else:
                index = next(i for i, a in enumerate(st.session_state.alumnos) 
                          if a['matricula'] == alumno['matricula'])
                st.session_state.alumnos[index] = nuevo_alumno
            
            guardar_alumnos(st.session_state.alumnos)
            st.session_state.modo_edicion = None
            st.session_state.alumno_editando = None
            st.rerun()
        
        if st.form_submit_button("❌ Cancelar"):
            st.session_state.modo_edicion = None
            st.session_state.alumno_editando = None
            st.rerun()
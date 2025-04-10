import streamlit as st
from datetime import datetime
import pandas as pd
from models.alumnos_model import guardar_alumnos, obtener_proxima_matricula

OPCIONES_GRADO = ['Preescolar', 'Primaria']
OPCIONES_NIVEL = ['preescolar', 'elemental']
OPCIONES_CURSO = ['Clases', 'Verano']
OPCIONES_PAQUETE = ['paquete sencillo', 'paquete completo']
METODOS_PAGO = ['Efectivo', 'Transferencia', 'Depósito']

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
        if busqueda.lower() in str(a.get('nombre', '')).lower() or 
           busqueda in str(a.get('matricula', ''))
    ]
    
    # Tabla de alumnos
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
    alumno = st.session_state.alumno_editando if st.session_state.modo_edicion == 'editar' else {}
    
    with st.form(key='form_alumno'):
        # Generar matrícula automática
        if st.session_state.modo_edicion == 'crear':
            matricula = obtener_proxima_matricula()
        else:
            matricula = alumno.get('matricula', '')
        
        # Campos en 2 columnas
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Matrícula*", value=matricula, disabled=True)
            nombre = st.text_input("Nombre completo*", value=alumno.get('nombre', ''))
            sexo = st.selectbox(
                "Sexo*", 
                ['h', 'm'], 
                index=0 if alumno.get('sexo', 'h') == 'h' else 1
            )
            
            id_grado = st.selectbox(
                "Grado*", 
                OPCIONES_GRADO, 
                index=OPCIONES_GRADO.index(alumno.get('id_grado', OPCIONES_GRADO[0]))
            )
            
            id_nivel = st.selectbox(
                "Nivel Educativo*", 
                OPCIONES_NIVEL, 
                index=OPCIONES_NIVEL.index(alumno.get('id_nivel_educativo', OPCIONES_NIVEL[0]))
            )

                

        with col2:
            estado = st.selectbox(
                "Estado*", 
                ['activo', 'inactivo'], 
                index=0 if alumno.get('estado_matricula', 'activo') == 'activo' else 1
            )
            
            curso = st.selectbox(
                "Curso*", 
                OPCIONES_CURSO, 
                index=OPCIONES_CURSO.index(alumno.get('curso', OPCIONES_CURSO[0])))
            
            paquete = st.selectbox(
                "Paquete*", 
                OPCIONES_PAQUETE, 
                index=OPCIONES_PAQUETE.index(alumno.get('paquete', OPCIONES_PAQUETE[0])))
            
            metodo_pago = st.selectbox(
                "Método Pago", 
                [''] + METODOS_PAGO, 
                index=([''] + METODOS_PAGO).index(alumno.get('metodo_pago', '')))

        # Campos de fechas
        col_fechas = st.columns(3)
        with col_fechas[0]:
            fecha_inscripcion = st.date_input(
                "Fecha Inscripción",
                value=pd.to_datetime(alumno.get('fecha_inscripcion')) if alumno.get('fecha_inscripcion') else datetime.today()
            )
        with col_fechas[1]:
            fecha_nacimiento = st.date_input(
                "Fecha Nacimiento",
                value=pd.to_datetime(alumno.get('fecha_nacimiento')) if alumno.get('fecha_nacimiento') else None
            )
        with col_fechas[2]:
            fecha_pago = st.date_input(
                "Última Fecha Pago",
                value=pd.to_datetime(alumno.get('fecha_pago')) if alumno.get('fecha_pago') else None
            )

        # Campos numéricos
        monto_pago = st.number_input(
            "Monto Último Pago (MXN)",
            value=float(alumno.get('monto_pago', 0)) if alumno.get('monto_pago') else 0.0,
            min_value=0.0
        )
        
        saldo_pendiente = st.number_input(
            "Saldo Pendiente (MXN)",
            value=float(alumno.get('saldo_pendiente', 0)) if alumno.get('saldo_pendiente') else 0.0,
            min_value=0.0
        )

        # Validación y guardado
        if st.form_submit_button("💾 Guardar"):
            campos_requeridos = {
                'Nombre': nombre,
                'Grado': id_grado,
                'Nivel Educativo': id_nivel,
                'Estado': estado,
                'Curso': curso,
                'Paquete': paquete
            }
            
            faltantes = [k for k, v in campos_requeridos.items() if not v]
            if faltantes:
                st.error(f"Campos obligatorios faltantes: {', '.join(faltantes)}")
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
                'metodo_pago': metodo_pago if metodo_pago else '',
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
import streamlit as st
from datetime import datetime, date
import pandas as pd
from models.alumnos_model import guardar_alumnos, obtener_proxima_matricula

# Constantes del sistema
OPCIONES_GRADO = ['Preescolar', 'Primaria', 'Secundaria', 'Bachillerato']
OPCIONES_NIVEL = ['Preescolar', 'Elemental', 'Intermedio', 'Avanzado']
OPCIONES_TIPO_CURSO = ["Clase", "Verano", "Intensivo"]
METODOS_PAGO = ['Efectivo', 'Transferencia', 'Tarjeta']
COSTO_PAQUETE = 500.0
COSTO_INSCRIPCION = 150.0

def calcular_clases_restantes(fecha_inicio):
    """Calcula las clases restantes en el mes basado en la fecha de inicio"""
    if not fecha_inicio:
        return 0
    hoy = datetime.today().date()
    diferencia = hoy - fecha_inicio
    semanas_transcurridas = diferencia.days // 7
    clases_transcurridas = semanas_transcurridas % 4
    return 4 - clases_transcurridas if clases_transcurridas < 4 else 0

def render_alumnos_view():
    """Vista principal de gestión de alumnos"""
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
        if busqueda.lower() in str(a.get('Nombre', '')).lower() or 
           busqueda in str(a.get('Matricula', ''))
    ]
    
    # Tabla de alumnos
    with st.expander("📋 Listado de Alumnos", expanded=True):
        for alumno in alumnos_filtrados:
            cols = st.columns([1, 3, 2, 2, 2, 2])
            cols[0].markdown(f"**{alumno.get('Matricula', '')}**")
            cols[1].markdown(f"**{alumno.get('Nombre', '')}**")
            
            # Estado de inscripción
            estado_insc = alumno.get('Inscripción', 'Pagada')
            color_insc = "#4BB1E0" if estado_insc == "Pagada" else "#FF4B4B"
            cols[2].markdown(f"<span style='color: {color_insc};'>●</span> {estado_insc}", unsafe_allow_html=True)
            
            if cols[4].button("👁️", key=f"ver_{alumno['Matricula']}"):
                st.session_state.alumno_detalle = alumno
            if cols[5].button("✏️", key=f"editar_{alumno['Matricula']}"):
                st.session_state.modo_edicion = 'editar'
                st.session_state.alumno_editando = alumno

    # Detalle del alumno
    if st.session_state.get('alumno_detalle'):
        render_detalle_alumno(st.session_state.alumno_detalle)

    # Formulario de edición/creación
    if st.session_state.get('modo_edicion'):
        render_formulario_alumno()

def render_detalle_alumno(alumno):
    """Muestra el detalle completo de un alumno"""
    with st.expander(f"📄 Detalle completo de {alumno.get('Nombre', '')}", expanded=True):
        cols = st.columns(2)
        
        # Información Básica
        with cols[0]:
            st.markdown("### Información Básica")
            st.markdown(f"**Matrícula:** {alumno.get('Matricula', '')}")
            st.markdown(f"**Nombre:** {alumno.get('Nombre', '')}")
            st.markdown(f"**Sexo:** {alumno.get('Sexo', '').upper()}")
            st.markdown(f"**Fecha Nacimiento:** {alumno.get('Cumpleaños', '')}")
            st.markdown(f"**Estado Inscripción:** {alumno.get('Inscripción', '')}")
            st.markdown(f"**Escuela Procedencia:** {alumno.get('Escuela de provinencia', '')}")
        
        # Datos Académicos
        with cols[1]:
            st.markdown("### Datos Académicos")
            st.markdown(f"**Grado:** {alumno.get('Grado', '')}")
            st.markdown(f"**Nivel:** {alumno.get('Nivel', '')}")
            st.markdown(f"**Curso:** {alumno.get('Tipo de Curso', '')}")
            st.markdown(f"**Fecha Inscripción:** {alumno.get('Fecha Inscripción', '')}")
            st.markdown(f"**Fecha Inicio Clases:** {alumno.get('Fecha Inicio Clases', '')}")
            
            # Calcular clases restantes
            if alumno.get('Fecha Inicio Clases'):
                fecha_inicio = pd.to_datetime(alumno['Fecha Inicio Clases']).date()
                clases_restantes = calcular_clases_restantes(fecha_inicio)
                st.markdown(f"**Clases restantes en el mes:** {clases_restantes}")
                if clases_restantes == 1:
                    st.warning("⚠️ ¡Última clase! Realizar próximo pago")
        
        # Información de Contacto
        st.markdown("### Información de Contacto")
        cols_contacto = st.columns(2)
        with cols_contacto[0]:
            st.markdown(f"**Email:** {alumno.get('Dirección de correo electrónico', '')}")
            st.markdown(f"**Familiar:** {alumno.get('Nombre Completo del Familiar', '')}")
            st.markdown(f"**Parentesco:** {alumno.get('Parentesco', '')}")
        
        with cols_contacto[1]:
            st.markdown(f"**Tel. Familiar:** {alumno.get('Número de teléfono del familiar', '')}")
            st.markdown(f"**Contacto Emergencia:** {alumno.get('Nombre completo de contacto de emergencia', '')}")
            st.markdown(f"**Tel. Emergencia:** {alumno.get('Número de teléfono de contacto de emergencia', '')}")
        
        # Información Médica
        st.markdown("### Información Médica")
        st.markdown(f"**Alergias:** {alumno.get('Alergias', 'Ninguna')}")
        st.markdown(f"**Observaciones:** {alumno.get('Observaciones', 'Ninguna')}")
        
        # Información Financiera
        st.markdown("### Información Financiera")
        monto_abonado = alumno.get('monto_abonado', 0.0)
        saldo_pendiente = COSTO_PAQUETE - monto_abonado
        cols_fin = st.columns(2)
        cols_fin[0].markdown(f"**Total Pagado:** ${monto_abonado:.2f} MXN")
        cols_fin[1].markdown(f"**Saldo Pendiente:** ${saldo_pendiente:.2f} MXN", 
                            help="Costo total del paquete: $500.00 MXN")

def render_formulario_alumno():
    """Formulario para crear/editar alumnos"""
    alumno = st.session_state.alumno_editando if st.session_state.modo_edicion == 'editar' else {}
    
    with st.form(key='form_alumno'):
        # Generar matrícula automática
        if st.session_state.modo_edicion == 'crear':
            matricula = obtener_proxima_matricula()
        else:
            matricula = alumno.get('Matricula', '')
        
        # Sección 1: Información Básica
        st.subheader("📝 Información Básica")
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Matrícula*", value=matricula, disabled=True)
            nombre = st.text_input("Nombre completo*", value=alumno.get('Nombre', ''))
            sexo = st.selectbox(
                "Sexo*", 
                ['H', 'M'], 
                index=0 if alumno.get('Sexo', 'H') == 'H' else 1
            )
            
        with col2:
            id_grado = st.selectbox(
                "Grado*", 
                OPCIONES_GRADO, 
                index=OPCIONES_GRADO.index(alumno.get('Grado', OPCIONES_GRADO[0])))
            
            escuela_procedencia = st.text_input(
                "Escuela de Procedencia*",
                value=alumno.get('Escuela de provinencia', '')
            )

        # Sección 2: Datos del Curso
        st.subheader("📚 Datos del Curso")
        col_curso, col_estado = st.columns([3, 1])
        
        with col_curso:
            # Sistema de curso dividido
            curso_actual = alumno.get('Tipo de Curso', '')
            tipo_actual = 'Clase'
            año_actual = datetime.today().year
            
            if ' - ' in curso_actual:
                partes = curso_actual.split(' - ')
                tipo_actual = partes[0].strip()
                año_actual = partes[1].strip() if len(partes) > 1 else str(datetime.today().year)
            
            col_tipo, col_año = st.columns([2, 1])
            with col_tipo:
                tipo_curso = st.selectbox(
                    "Tipo de Curso*",
                    OPCIONES_TIPO_CURSO,
                    index=OPCIONES_TIPO_CURSO.index(tipo_actual) if tipo_actual in OPCIONES_TIPO_CURSO else 0
                )
            with col_año:
                año_curso = st.number_input(
                    "Año del Curso*",
                    min_value=1900,
                    max_value=2100,
                    value=int(año_actual) if str(año_actual).isdigit() else datetime.today().year,
                    step=1
                )
            
            curso_completo = f"{tipo_curso} - {año_curso}"
        
        with col_estado:
            estado_matricula = st.selectbox(
                "Estado Matrícula*", 
                ['activo', 'inactivo'], 
                index=0 if alumno.get('Vigente', 'activo') == 'activo' else 1
            )
            estado_inscripcion = st.selectbox(
                "Estado Inscripción*",
                ["Pagada", "Condonada"],
                index=0 if alumno.get('Inscripción', 'Pagada') == 'Pagada' else 1
            )

        # Sección 3: Fechas Importantes
        st.subheader("📅 Fechas Importantes")
        col_fechas = st.columns(3)
        with col_fechas[0]:
            fecha_inscripcion = st.date_input(
                "Fecha de Inscripción*",
                value=pd.to_datetime(alumno.get('Fecha Inscripción')) if alumno.get('Fecha Inscripción') else datetime.today()
            )
        with col_fechas[1]:
            fecha_inicio_clases = st.date_input(
                "Fecha Inicio Clases*",
                value=pd.to_datetime(alumno.get('Fecha Inicio Clases')) if alumno.get('Fecha Inicio Clases') else datetime.today()
            )
        with col_fechas[2]:
            fecha_nacimiento = st.date_input(
                "Fecha Nacimiento*",
                value=pd.to_datetime(alumno.get('Cumpleaños')) if alumno.get('Cumpleaños') else None,
                min_value=date(1900, 1, 1),
                max_value=date.today()
            )

        # Sección 4: Información de Contacto
        st.subheader("📞 Información de Contacto")
        col_contacto = st.columns(2)
        with col_contacto[0]:
            email = st.text_input(
                "Correo Electrónico", 
                value=alumno.get('Dirección de correo electrónico', '')
            )
            nombre_familiar = st.text_input(
                "Nombre del Familiar*", 
                value=alumno.get('Nombre Completo del Familiar', '')
            )
            parentesco = st.text_input(
                "Parentesco*", 
                value=alumno.get('Parentesco', '')
            )
        
        with col_contacto[1]:
            tel_familiar = st.text_input(
                "Teléfono Familiar*", 
                value=alumno.get('Número de teléfono del familiar', '')
            )
            contacto_emergencia = st.text_input(
                "Contacto Emergencia*", 
                value=alumno.get('Nombre completo de contacto de emergencia', '')
            )
            tel_emergencia = st.text_input(
                "Teléfono Emergencia*", 
                value=alumno.get('Número de teléfono de contacto de emergencia', '')
            )

        # Sección 5: Información Médica
        st.subheader("🏥 Información Médica")
        col_medica = st.columns(2)
        with col_medica[0]:
            alergias = st.text_area(
                "Alergias", 
                value=alumno.get('Alergias', 'Ninguna'),
                placeholder="Ej: Alergia al polen, medicamentos, etc."
            )
        with col_medica[1]:
            observaciones = st.text_area(
                "Observaciones Médicas", 
                value=alumno.get('Observaciones', 'Ninguna'),
                placeholder="Ej: Uso de lentes, condiciones especiales, etc."
            )

        # Sección 6: Información de Pagos
        st.subheader("💰 Información de Pagos")
        monto_actual = float(alumno.get('monto_abonado', 0.0))
        col_pagos = st.columns(2)
        
        with col_pagos[0]:
            monto_abonado = st.number_input(
                "Monto Abonado (MXN)",
                value=monto_actual,
                min_value=0.0,
                max_value=COSTO_PAQUETE,
                step=50.0,
                key="monto_abonado"
            )
            st.info(f"Costo total del paquete: ${COSTO_PAQUETE:.2f} MXN")
        
        with col_pagos[1]:
            saldo_pendiente = COSTO_PAQUETE - monto_abonado
            st.metric(
                "Saldo Pendiente", 
                f"${saldo_pendiente:.2f} MXN",
                delta=f"-${saldo_pendiente:.2f}" if saldo_pendiente > 0 else "",
                delta_color="inverse"
            )

        # Botones de acción
        submit_cols = st.columns([1, 1, 3])
        with submit_cols[0]:
            submitted = st.form_submit_button("💾 Guardar")
        with submit_cols[1]:
            cancelled = st.form_submit_button("❌ Cancelar")

        if submitted:
            # Validación de campos obligatorios
            campos_requeridos = {
                'Nombre': nombre,
                'Grado': id_grado,
                'Escuela Procedencia': escuela_procedencia,
                'Tipo de Curso': tipo_curso,
                'Año del Curso': año_curso,
                'Nombre Familiar': nombre_familiar,
                'Parentesco': parentesco,
                'Teléfono Familiar': tel_familiar,
                'Contacto Emergencia': contacto_emergencia,
                'Teléfono Emergencia': tel_emergencia
            }
            
            faltantes = [k for k, v in campos_requeridos.items() if not v]
            if faltantes:
                st.error(f"❌ Campos obligatorios faltantes: {', '.join(faltantes)}")
                return

            # Construir registro del alumno
            nuevo_alumno = {
                'Matricula': matricula,
                'Nombre': nombre,
                'Sexo': sexo,
                'Grado': id_grado,
                'Nivel': 'Elemental',
                'Escuela de provinencia': escuela_procedencia,
                'Alergias': alergias,
                'Observaciones': observaciones,
                'Nombre Completo del Familiar': nombre_familiar,
                'Parentesco': parentesco,
                'Número de teléfono del familiar': tel_familiar,
                'Nombre completo de contacto de emergencia': contacto_emergencia,
                'Número de teléfono de contacto de emergencia': tel_emergencia,
                'Fecha Inscripción': fecha_inscripcion.strftime("%d/%m/%Y"),
                'Fecha Inicio Clases': fecha_inicio_clases.strftime("%d/%m/%Y"),
                'Cumpleaños': fecha_nacimiento.strftime("%d/%m/%Y") if fecha_nacimiento else '',
                'Inscripción': estado_inscripcion,
                'Tipo de Curso': curso_completo,
                'Vigente': 'Si' if estado_matricula == 'activo' else 'No',
                'monto_abonado': monto_abonado,
                'Dirección de correo electrónico': email
            }

            # Guardar cambios
            if st.session_state.modo_edicion == 'crear':
                st.session_state.alumnos.append(nuevo_alumno)
            else:
                index = next(i for i, a in enumerate(st.session_state.alumnos) 
                          if a['Matricula'] == alumno['Matricula'])
                st.session_state.alumnos[index] = nuevo_alumno
            
            guardar_alumnos(st.session_state.alumnos)
            st.session_state.modo_edicion = None
            st.session_state.alumno_editando = None
            st.rerun()
        
        if cancelled:
            st.session_state.modo_edicion = None
            st.session_state.alumno_editando = None
            st.rerun()
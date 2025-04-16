import streamlit as st
from datetime import datetime, date
import pandas as pd
from models.alumnos_model import guardar_alumnos, obtener_proxima_matricula

# Opciones de grado general simplificadas
OPCIONES_GRADO = [
    'Preescolar', 'Primaria', 'Secundaria', 'Bachillerato', 'Universidad'
]
# Cambiar "Intensivo" por "Taller"
OPCIONES_TIPO_CURSO = ["Clase", "Verano", "Taller"]
# Agregar "Pendiente" a métodos de pago
METODOS_PAGO = ['Efectivo', 'Transferencia', 'Tarjeta', 'Pendiente']
COSTO_PAQUETE = 500.0
OPCIONES_GRADO_INBLOQUET = [
    'Inbloquet: Elemental',
    'Inbloquet: Preescolar'
]


def render_formulario_alumno():
    """Formulario para crear/editar alumnos, renderizado inline con un contenedor único."""
    # Si estamos editando, obtenemos el alumno; si no, se usa un dict vacío.
    alumno = st.session_state.alumno_editando if st.session_state.modo_edicion == 'editar' else {}
    
    # Se define un identificador único para el formulario. Si es edición, se usa la matrícula; de lo contrario se usa 'nuevo'
    form_id = f"form_alumno_{alumno.get('Matricula', 'nuevo')}"
    
    # Cada formulario debe tener un único st.form_submit_button, por eso le asignamos un key único.
    with st.form(key=form_id):
        # Generar matrícula automática si es creación, o usar la existente en edición
        if st.session_state.modo_edicion == 'crear':
            matricula = obtener_proxima_matricula()
            matricula_disabled = True
        else:
            matricula = alumno.get('Matricula', '')
            matricula_disabled = True  # Siempre inhabilitado
        
        # Sección 1: Información Básica
        st.subheader("📝 Información Básica")
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Matrícula*", value=matricula, disabled=matricula_disabled)
            nombre = st.text_input("Nombre completo*", value=alumno.get('Nombre', ''))
            sexo = st.selectbox(
                "Sexo*", 
                ['H', 'M'], 
                index=0 if alumno.get('Sexo', 'H') == 'H' else 1
            )
            
        with col2:
    # Lista de grados internos de Inbloquet
            OPCIONES_GRADO_INBLOQUET = ['Inbloquet: Elemental', 'Inbloquet: Preescolar']

            # Selectbox del grado general del alumno
            grado_actual = alumno.get('Grado', OPCIONES_GRADO[0])
            default_index_grado = OPCIONES_GRADO.index(grado_actual) if grado_actual in OPCIONES_GRADO else 0
            id_grado = st.selectbox("Grado escolar*", OPCIONES_GRADO, index=default_index_grado)

            # Nuevo selectbox del grado Inbloquet
            grado_inbloquet_actual = alumno.get('Grado Inbloquet', OPCIONES_GRADO_INBLOQUET[0])
            default_index_inbloquet = OPCIONES_GRADO_INBLOQUET.index(grado_inbloquet_actual) if grado_inbloquet_actual in OPCIONES_GRADO_INBLOQUET else 0
            grado_inbloquet = st.selectbox("Grado en Inbloquet*", OPCIONES_GRADO_INBLOQUET, index=default_index_inbloquet)

            # Escuela de procedencia
            escuela_procedencia = st.text_input(
                "Escuela de Procedencia*",
                value=alumno.get('Escuela de provinencia', '')
            )

        # Sección 2: Datos del Curso
        st.subheader("📚 Datos del Curso")
        col_curso, col_estado = st.columns([3, 1])
        
        with col_curso:
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
            # Agregar "Pendiente" a estado de inscripción
            estado_inscripcion = st.selectbox(
                "Estado Inscripción*",
                ["Pagada", "Condonada", "Pendiente"],
                index=["Pagada", "Condonada", "Pendiente"].index(alumno.get('Inscripción', 'Pagada')) if alumno.get('Inscripción', 'Pagada') in ["Pagada", "Condonada", "Pendiente"] else 0
            )

        # Sección 3: Fechas Importantes
        st.subheader("📅 Fechas Importantes")
        col_fechas = st.columns(3)
        with col_fechas[0]:
            # Inhabilitar edición de fecha de inscripción si es edición
            if st.session_state.modo_edicion == 'editar':
                fecha_inscripcion = pd.to_datetime(alumno.get('Fecha Inscripción'), dayfirst=True).date() if alumno.get('Fecha Inscripción') else date.today()
                st.date_input(
                    "Fecha de Inscripción*",
                    value=fecha_inscripcion,
                    min_value=date(1900, 1, 1),
                    max_value=date(2100, 12, 31),
                    disabled=True
                )
            else:
                fecha_inscripcion = st.date_input(
                    "Fecha de Inscripción*",
                    value=pd.to_datetime(alumno.get('Fecha Inscripción'), dayfirst=True).date() if alumno.get('Fecha Inscripción') else date.today(),
                    min_value=date(1900, 1, 1),
                    max_value=date(2100, 12, 31)
                )
        with col_fechas[1]:
            fecha_inicio_clases = st.date_input(
                "Fecha Inicio Clases*",
                value=pd.to_datetime(alumno.get('Fecha Inicio Clases'), dayfirst=True).date() if alumno.get('Fecha Inicio Clases') else date.today(),
                min_value=date(1900, 1, 1),
                max_value=date(2100, 12, 31)
            )
        with col_fechas[2]:
            fecha_nacimiento = st.date_input(
                "Fecha Nacimiento*",
                value=pd.to_datetime(alumno.get('Cumpleaños'), dayfirst=True).date() if alumno.get('Cumpleaños') else None,
                min_value=date(1900, 1, 1),
                max_value=date.today()
            )

        # Sección 4: Información de Contacto
        st.subheader("📞 Información de Contacto")
        col_contacto = st.columns(2)
        with col_contacto[0]:
            email = st.text_input("Correo Electrónico", value=alumno.get('Dirección de correo electrónico', ''))
            nombre_familiar = st.text_input("Nombre del Familiar*", value=alumno.get('Nombre Completo del Familiar', ''))
            parentesco = st.text_input("Parentesco*", value=alumno.get('Parentesco', ''))
        with col_contacto[1]:
            tel_familiar = st.text_input("Teléfono Familiar*", value=alumno.get('Número de teléfono del familiar', ''))
            contacto_emergencia = st.text_input("Contacto Emergencia", value=alumno.get('Nombre completo de contacto de emergencia', ''))
            tel_emergencia = st.text_input("Teléfono Emergencia", value=alumno.get('Número de teléfono de contacto de emergencia', ''))

        # Sección 5: Información Médica
        st.subheader("🏥 Información Médica")
        col_medica = st.columns(2)
        with col_medica[0]:
            alergias = st.text_area("Alergias", value=alumno.get('Alergias', 'Ninguna'),
                                    placeholder="Ej: Alergia al polen, medicamentos, etc.")
        with col_medica[1]:
            observaciones = st.text_area("Observaciones Médicas", value=alumno.get('Observaciones', 'Ninguna'),
                                         placeholder="Ej: Uso de lentes, condiciones especiales, etc.")

        # Sección 6: Información de Pagos
        st.subheader("💰 Información de Pagos")
        total_pagado = sum(p['monto'] for p in alumno.get('pagos', []))
        col_pagos = st.columns(2)
        with col_pagos[0]:
            monto_abonado = st.number_input(
                "Monto a Abonar (MXN)",
                value=0.0,
                min_value=0.0,
                max_value=COSTO_PAQUETE - total_pagado,
                step=50.0,
                key=f"monto_abonado_{matricula}"
            )
            metodo_pago = st.selectbox("Método de Pago", METODOS_PAGO, key=f"metodo_pago_{matricula}")
            st.info(f"Costo total del paquete: ${COSTO_PAQUETE:.2f} MXN")
        with col_pagos[1]:
            saldo_pendiente = COSTO_PAQUETE - (total_pagado + monto_abonado)
            st.metric("Saldo Pendiente", f"${saldo_pendiente:.2f} MXN",
                      delta=f"-${monto_abonado:.2f}" if monto_abonado > 0 else "",
                      delta_color="inverse")

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
                'Grado Inbloquet': grado_inbloquet,
                'Escuela Procedencia': escuela_procedencia,
                'Tipo de Curso': tipo_curso,
                'Año del Curso': año_curso,
                'Nombre Familiar': nombre_familiar,
            }
            # Construir registro del alumno
            nuevo_alumno = {
                'Matricula': matricula,
                'Nombre': nombre,
                'Sexo': sexo,
                'Grado': id_grado,
                'Grado Inbloquet': grado_inbloquet,
                'Escuela de provinencia': escuela_procedencia,
                'Tipo de Curso': curso_completo,
                'Vigente': estado_matricula,
                'Inscripción': estado_inscripcion,
                'Fecha Inscripción': fecha_inscripcion,
                'Fecha Inicio Clases': fecha_inicio_clases,
                'Cumpleaños': fecha_nacimiento,
                'Dirección de correo electrónico': email,
                'Nombre Completo del Familiar': nombre_familiar,
                'Parentesco': parentesco,
                'Número de teléfono del familiar': tel_familiar,
                'Nombre completo de contacto de emergencia': contacto_emergencia,
                'Número de teléfono de contacto de emergencia': tel_emergencia,
                'Alergias': alergias,
                'Observaciones': observaciones,
                'pagos': alumno.get('pagos', []) + [{'monto': monto_abonado, 'metodo': metodo_pago}] if monto_abonado > 0 else alumno.get('pagos', [])
            }

            # Guardar cambios según si es creación o edición
            if st.session_state.modo_edicion == 'crear':
                if 'alumnos' not in st.session_state:
                    st.session_state.alumnos = []
                st.session_state.alumnos.append(nuevo_alumno)
            else:
                # Buscar el índice del alumno a editar
                index = next((i for i, a in enumerate(st.session_state.alumnos)
                              if a['Matricula'] == alumno['Matricula']), None)
                if index is not None:
                    st.session_state.alumnos[index] = nuevo_alumno

            guardar_alumnos(st.session_state.alumnos)
            st.session_state.modo_edicion = None
            st.session_state.alumno_editando = None
            st.session_state.alumno_detalle = None
            st.rerun()

        if cancelled:
            st.session_state.modo_edicion = None
            st.session_state.alumno_editando = None
            st.session_state.alumno_detalle = None
            st.rerun()
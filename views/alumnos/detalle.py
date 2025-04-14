import streamlit as st
import pandas as pd
from datetime import date
from views.alumnos.calculos import calcular_clases_restantes, generar_calendario_clases

def render_detalle_alumno(alumno):
    """Muestra el detalle completo de un alumno sin usar un expander anidado"""
    # Usamos un contenedor para evitar expanders anidados y para agrupar los detalles
    with st.container():
        st.markdown(f"**Detalle completo de {alumno.get('Nombre', '')}:**")
        cols = st.columns(2)
        
        # Información Básica
        with cols[0]:
            st.markdown("##### Información Básica")
            st.markdown(f"**Matrícula:** {alumno.get('Matricula', '')}")
            st.markdown(f"**Nombre:** {alumno.get('Nombre', '')}")
            st.markdown(f"**Sexo:** {alumno.get('Sexo', '').upper()}")
            st.markdown(f"**Fecha Nacimiento:** {alumno.get('Cumpleaños', '')}")
            st.markdown(f"**Estado Inscripción:** {alumno.get('Inscripción', '')}")
            st.markdown(f"**Escuela Procedencia:** {alumno.get('Escuela de provinencia', '')}")
        
        # Datos Académicos
        with cols[1]:
            st.markdown("##### Datos Académicos")
            st.markdown(f"**Grado:** {alumno.get('Grado', '')}")
            st.markdown(f"**Nivel:** {alumno.get('Nivel', '')}")
            st.markdown(f"**Grado Inbloquet:** {alumno.get('Grado Inbloquet', '')}")
            st.markdown(f"**Curso:** {alumno.get('Tipo de Curso', '')}")
            st.markdown(f"**Fecha Inscripción:** {alumno.get('Fecha Inscripción', '')}")
            st.markdown(f"**Fecha Inicio Clases:** {alumno.get('Fecha Inicio Clases', '')}")
            
            # Calcular clases restantes
            if alumno.get('Fecha Inicio Clases'):
                fecha_inicio = pd.to_datetime(alumno['Fecha Inicio Clases'], dayfirst=True).date()
                clases_restantes = calcular_clases_restantes(fecha_inicio)
                st.markdown(f"**Clases restantes en el mes:** {clases_restantes}")
                if clases_restantes == 1:
                    st.warning("⚠️ ¡Última clase! Realizar próximo pago")
        
        st.markdown("##### Información de Contacto")
        cols_contacto = st.columns(2)
        with cols_contacto[0]:
            st.markdown(f"**Email:** {alumno.get('Dirección de correo electrónico', '')}")
            st.markdown(f"**Familiar:** {alumno.get('Nombre Completo del Familiar', '')}")
            st.markdown(f"**Parentesco:** {alumno.get('Parentesco', '')}")
        with cols_contacto[1]:
            st.markdown(f"**Tel. Familiar:** {alumno.get('Número de teléfono del familiar', '')}")
            st.markdown(f"**Contacto Emergencia:** {alumno.get('Nombre completo de contacto de emergencia', '')}")
            st.markdown(f"**Tel. Emergencia:** {alumno.get('Número de teléfono de contacto de emergencia', '')}")
        
        st.markdown("##### Información Médica")
        st.markdown(f"**Alergias:** {alumno.get('Alergias', 'Ninguna')}")
        st.markdown(f"**Observaciones:** {alumno.get('Observaciones', 'Ninguna')}")
        
        st.markdown("##### Información Financiera")
        COSTO_PAQUETE = 500.0
        total_pagado = sum(p['monto'] for p in alumno.get('pagos', []))
        saldo_pendiente = COSTO_PAQUETE - total_pagado
        
        cols_fin = st.columns(2)
        cols_fin[0].markdown(f"**Total Pagado:** ${total_pagado:.2f} MXN")
        cols_fin[1].markdown(f"**Saldo Pendiente:** ${saldo_pendiente:.2f} MXN", 
                             help="Costo total del paquete: $500.00 MXN")
        
        st.markdown("###### Historial de Pagos")
        if alumno.get('pagos'):
            for pago in alumno['pagos']:
                st.write(f"{pago['fecha']}: ${pago['monto']:.2f} MXN ({pago['metodo']})")
        else:
            st.info("No hay registros de pago")
        
        st.markdown("###### Seguimiento de Clases")
        if 'clases' not in alumno:
            alumno['clases'] = []
        
        # Generar clases si no existen
        if not alumno['clases'] and alumno.get('Fecha Inicio Clases'):
            fecha_inicio = pd.to_datetime(alumno['Fecha Inicio Clases'], dayfirst=True).date()
            alumno['clases'] = generar_calendario_clases(fecha_inicio)
        
        # Renderización de cada clase con claves únicas usando el índice o matrícula
        for i, clase in enumerate(alumno['clases']):
            cols_clase = st.columns([2, 2, 3, 1])
            fecha = cols_clase[0].date_input(
                "Fecha", 
                value=pd.to_datetime(clase['fecha'], dayfirst=True).date(),
                key=f"fecha_{alumno.get('Matricula','')}_{i}"
            )
            estado = cols_clase[1].selectbox(
                "Estado",
                options=['Programada', 'Tomada', 'PosPuesta', 'Vista'],
                index=['Programada', 'Tomada', 'PosPuesta', 'Vista'].index(clase.get('estado', 'Programada')),
                key=f"estado_{alumno.get('Matricula','')}_{i}"
            )
            comentario = cols_clase[2].text_input(
                "Comentario",
                value=clase.get('comentario', ''),
                key=f"comentario_{alumno.get('Matricula','')}_{i}"
            )
            if cols_clase[3].button("✖️", key=f"eliminar_clase_{alumno.get('Matricula','')}_{i}"):
                del alumno['clases'][i]
                st.experimental_rerun()
            
            # Actualizar valores
            alumno['clases'][i] = {
                'fecha': fecha.strftime("%d/%m/%Y"),
                'estado': estado,
                'comentario': comentario
            }
        
        # Actualizamos la clave del botón para que sea única por alumno
        if st.button("➕ Agregar clase manualmente", key=f"agregar_clase_{alumno.get('Matricula','')}"):
            alumno['clases'].append({
                'fecha': date.today().strftime("%d/%m/%Y"),
                'estado': 'Programada',
                'comentario': ''
            })
            st.experimental_rerun()

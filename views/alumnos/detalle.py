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
            # Mostrar estado activo/inactivo con color
            vigente = alumno.get("Vigente", "activo")
            color_vigente = "#4BB543" if vigente == "activo" else "#FF4B4B"
            st.markdown(
                f"**Estado Matrícula:** <span style='color: {color_vigente};'>●</span> {vigente.capitalize()}",
                unsafe_allow_html=True
            )
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
        # --- Asegurar que pagos y clases sean listas ---
        pagos = alumno.get('pagos') or []
        clases = alumno.get('clases') or []
        total_pagado = sum(p.get('monto', 0.0) for p in pagos)
        saldo_pendiente = COSTO_PAQUETE - total_pagado
        
        cols_fin = st.columns(2)
        cols_fin[0].markdown(f"**Total Pagado:** ${total_pagado:.2f} MXN")
        cols_fin[1].markdown(f"**Saldo Pendiente:** ${saldo_pendiente:.2f} MXN", 
                             help="Costo total del paquete: $500.00 MXN")
        
        st.markdown("###### Historial de Pagos")
        if alumno.get('pagos'):
            for pago in alumno['pagos']:
                # Usar .get para evitar KeyError si falta 'fecha'
                fecha = pago.get('fecha', '-')
                monto = pago.get('monto', 0.0)
                metodo = pago.get('metodo', '-')
                st.write(f"{fecha}: ${monto:.2f} MXN ({metodo})")
        else:
            st.info("No hay registros de pago")
        
        st.markdown("###### Seguimiento de Clases")
        if not clases and alumno.get('Fecha Inicio Clases'):
            fecha_inicio = pd.to_datetime(alumno['Fecha Inicio Clases'], dayfirst=True).date()
            clases = generar_calendario_clases(fecha_inicio)
            alumno['clases'] = clases
        
        # --- ADVERTENCIAS DE CLASES Y PAGOS ---
        clases = alumno.get('clases', [])
        clases_restantes = len([c for c in clases if c.get('estado', 'Programada') in ['Programada']])
        clases_tomadas = len([c for c in clases if c.get('estado', 'Programada') not in ['Programada']])
        # Si no hay clases, intentar generarlas
        if not clases and alumno.get('Fecha Inicio Clases'):
            fecha_inicio = pd.to_datetime(alumno['Fecha Inicio Clases'], dayfirst=True).date()
            clases = generar_calendario_clases(fecha_inicio)
            alumno['clases'] = clases

        # --- Nueva tanda de clases si las últimas 4 son Tomada/Vista ---
        if len(clases) >= 4:
            ultimas_4 = clases[-4:]
            if all(c.get('estado') in ['Tomada', 'Vista'] for c in ultimas_4):
                # Solo agregar si no se ha agregado ya la siguiente tanda
                if not any(c.get('estado') == 'Programada' for c in clases[-4:]):
                    # Generar nuevas 4 clases a partir de la última fecha
                    ultima_fecha = pd.to_datetime(clases[-1]['fecha'], dayfirst=True).date()
                    nuevas_clases = generar_calendario_clases(ultima_fecha, cantidad=4)
                    # Evitar duplicados
                    for nc in nuevas_clases:
                        if nc['fecha'] not in [c['fecha'] for c in clases]:
                            clases.append(nc)
                    alumno['clases'] = clases

        # --- Advertencias de pago y clases ---
        clases_programadas = [c for c in clases if c.get('estado', 'Programada') == 'Programada']
        clases_restantes = len(clases_programadas)
        if clases_restantes == 3:
            if saldo_pendiente > 0:
                st.warning("⚠️ Quedan 3 clases programadas. Realiza el pago pronto para evitar interrupciones.")
            else:
                st.info("ℹ️ Quedan 3 clases. Pronto terminarán sus clases, considera realizar el siguiente pago.")
        elif clases_restantes == 1:
            if saldo_pendiente > 0:
                st.error("🚨 ¡Última clase! Es urgente realizar el pago para continuar el siguiente ciclo.")
            else:
                st.warning("⚠️ Última clase. Se requiere pago para continuar después de esta clase.")
        elif clases_restantes == 0 and all(c.get('estado') in ['Tomada', 'Vista'] for c in clases):
            if saldo_pendiente <= 0:
                st.success("✅ Paquete finalizado. El contador de abonos se reinicia, pero el historial de pagos se conserva.")

        # --- Reinicio de abonos y saldo cuando termina el paquete ---
        if saldo_pendiente <= 0 and all(c.get('estado') in ['Tomada', 'Vista'] for c in clases):
            # Guardar historial de pagos si no existe
            if 'pagos_historial' not in alumno:
                alumno['pagos_historial'] = []
            alumno['pagos_historial'].extend(pagos)
            alumno['pagos'] = []
            saldo_pendiente = COSTO_PAQUETE  # Reinicia saldo pendiente para el siguiente ciclo
            st.info("ℹ️ Paquete finalizado. El contador de abonos se reinicia, pero el historial de pagos se conserva.")

        # Renderización de cada clase con claves únicas usando el índice o matrícula
        for i, clase in enumerate(alumno['clases'] or []):
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
                st.rerun()
            
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
            st.rerun()

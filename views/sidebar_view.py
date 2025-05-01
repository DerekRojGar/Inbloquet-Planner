import streamlit as st
from datetime import datetime
import base64

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception as e:
        st.error(f"Error al cargar la imagen: {e}")
        return ""

def render_sidebar(frase_actual):
    # Convertir imagen a base64
    rocket_base64 = get_base64_image("rocket-face.png")
    
    with st.sidebar:
        # Logo más grande (160px) con borde circular
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: center;
                margin-bottom: 30px;
                padding: 15px;
            ">
                <img src="data:image/png;base64,{rocket_base64}" 
                     width="160" 
                     style="border-radius: 50%; 
                            border: 3px solid #4BB1E0;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Configuración principal
        st.header("⚙️ Configuración")
        
        # Selectores en 2 columnas
        col1, col2 = st.columns(2)
        with col1:
            semana = st.number_input(
                "Número de Semana", 
                min_value=1, 
                max_value=53, 
                value=st.session_state.get("num_semana", datetime.today().isocalendar()[1]),
                key="sidebar_semana"
            )
        with col2:
            año = st.number_input(
                "Año", 
                min_value=2023, 
                max_value=2030, 
                value=st.session_state.get("num_año", datetime.today().year),
                key="sidebar_año"
            )
        # Actualizar session_state global para que los formularios usen estos valores
        st.session_state.num_semana = semana
        st.session_state.num_año = año
        
        st.markdown("---")
        
        # Frase inspiradora (diseño original)
        nueva_frase = st.text_area(
            "✍️ Frase inspiradora del día:", 
            value=frase_actual,
            height=100
        )
        
        # Botones en disposición vertical original
        if st.button("💾 Guardar Frase", key="guardar_frase"):
            st.session_state.frase_global = nueva_frase
            st.rerun()
            
        st.markdown("---")
        
        # Botones de expansión en línea horizontal
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            if st.button("📂 Expandir Todo", key="expandir_todo"):
                st.session_state.expanded_state = True
                st.rerun()
        with exp_col2:
            if st.button("📂 Contraer Todo", key="contraer_todo"):
                st.session_state.expanded_state = False
                st.rerun()
                
    return semana, año
import streamlit as st

def render_css():
    st.markdown("""
    <style>
    /* ================================
       RESET Y TIPOGRAFÍA
       ================================ */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    html, body, [class*="css"] {
        font-family: 'Gotham', Arial, sans-serif;
    }

    /* ================================
       CONTENEDOR PRINCIPAL (FONDO NEGRO)
       ================================ */
    [data-testid="stAppViewContainer"] {
        background-color: #000000 !important; /* FONDO NEGRO */
        padding: 1rem;
        color: #ffffff; /* Texto blanco por defecto */
    }
    
    /* ================================
       SIDEBAR
       ================================ */
    [data-testid="stSidebar"] {
        background-color: #003891 !important;
        border-right: 2px solid #4bb1e0;
        padding: 1rem;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] input, 
    [data-testid="stSidebar"] textarea, 
    [data-testid="stSidebar"] select {
        color: #003891 !important;
        background-color: #ffffff !important;
        border: 2px solid #4bb1e0 !important;
        border-radius: 6px;
        padding: 0.3em 0.5em;
        margin-bottom: 0.5rem;
    }

    /* Logo Rocket en el Sidebar (tipo foto de perfil) */
    .rocket-logo {
        width: 80px !important;
        height: 80px !important;
        object-fit: cover;
        border-radius: 50%;
        margin-bottom: 1rem;
        border: 2px solid #ffffff;
    }

        /* ================================
       CABECERA PRINCIPAL
       ================================ */
    .header-container {
        display: inline-flex;
        align-items: center;
        gap: 10px; /* Espacio entre el título y el logo */
        margin-bottom: 1rem;
    }
    .main-title {
        font-size: 2.2em;
        color: #ffffff; /* Texto blanco */
        margin: 0;
    }
    .inbloquet-logo {
        width: 75px;
        height: auto;
    }

    /* ================================
       CALENDARIO
       ================================ */
    .calendar-column {
        background-color: #222222; /* Fondo oscuro para cada recuadro */
        color: #ffffff;           /* Texto blanco */
        border: 1px solid #4bb1e0;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.3rem;
        text-align: center;
    }

    /* ================================
       EXPANDERS (Actividades)
       ================================ */
    .st-expander {
        background-color: #222222 !important; /* Fondo oscuro */
        border: 2px solid #4bb1e0;
        border-radius: 10px;
        margin: 10px 0;
    }
    /* Texto interno de los expanders */
    .st-expander .stMarkdown, .st-expander p, .st-expander li {
        color: #ffffff !important;
    }

    /* ================================
       BOTONES DEL SIDEBAR
       (Expandir Todo y Contraer Todo)
       ================================ */
    .sidebar-button {
        background-color: #f6c500;
        color: #003891;
        border: 2px solid #4bb1e0;
        border-radius: 6px;
        padding: 0.5em 1.2em;
        font-weight: bold;
        width: 100%;
        margin-top: 0.5rem;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    .sidebar-button:hover {
        background-color: #d1dd00;
        color: #003891;
        cursor: pointer;
    }

    /* ================================
       BOTONES GENERALES
       ================================ */
    div.stButton > button, 
    div.stDownloadButton > button {
        background-color: #f6c500;
        color: #003891;
        border: 2px solid #4bb1e0;
        border-radius: 6px;
        padding: 0.5em 1.2em;
        font-weight: bold;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    div.stButton > button:hover, 
    div.stDownloadButton > button:hover {
        background-color: #d1dd00;
        color: #003891;
        cursor: pointer;
    }

    /* ================================
       FORMULARIOS (Inputs, Textareas, etc.)
       ================================ */
    .stTextInput input, 
    .stNumberInput input, 
    .stTextArea textarea, 
    .stDateInput input,
    .stSelectbox select {
        border: 2px solid #4bb1e0;
        border-radius: 6px;
        padding: 0.5em;
        color: #003891;
        background-color: #ffffff;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 0.5em;
    }
    /* Mejora para la visibilidad de los placeholders */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #555 !important;
}

    .stTextInput input:focus, 
    .stNumberInput input:focus, 
    .stTextArea textarea:focus, 
    .stDateInput input:focus,
    .stSelectbox select:focus {
        outline: none !important;
        border: 2px solid #003891;
        box-shadow: 0 0 5px rgba(0,56,145,0.5);
    }

    /* ================================
       FRASE INSPIRADORA
       ================================ */
    .frase-dia {
        background: #4bb1e0;
        color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #003891;
        margin: 20px 0;
    }

    /* ================================
       SCROLLBARS PERSONALIZADOS (OPCIONAL)
       ================================ */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #000000;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #4bb1e0;
        border-radius: 4px;
    }
                /* Detalle de alumno */
.detalle-alumno {
    background: #222222;
    border: 2px solid #4BB1E0;
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.detalle-alumno h3 {
    color: #4BB1E0;
    border-bottom: 2px solid;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

/* Campos requeridos */
[class*="stTextInput"] label span::after {
    content: "*";
    color: #FF4B4B;
    margin-left: 0.2rem;
}
                
                
    </style>
    """, unsafe_allow_html=True)


# Añadir al CSS:
st.markdown("""
<style>
    /* Estilos para estado de pago */
    .estado-pago {
        padding: 0.8rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .pagado {
        background-color: #4BB1E022;
        border-left: 5px solid #4BB1E0;
    }
    
    .pendiente {
        background-color: #FF4B4B22;
        border-left: 5px solid #FF4B4B;
    }
    
    /* Scroll automático al formulario */
    [data-testid="stExpander"] {
        scroll-margin-top: 80px;
    }
</style>
""", unsafe_allow_html=True)

import streamlit as st

def render_css():
    st.markdown("""
    <style>
    /* =========================================
       TIPOGRAFÍA LOCAL
       ========================================= */
    html, body, [class*="css"] {
        font-family: 'Gotham', Arial, sans-serif;
        
    }
    
    /* =========================================
       COLORES CORPORATIVOS
       =========================================
       #003891 (Azul oscuro)  661 C
       #4bb1e0 (Azul claro)   306 C
       #f6c500 (Amarillo)     7548 C
       #d1dd00 (Verde lima)   389 C
    */

    /* =========================================
       FONDO PRINCIPAL Y CONTENEDORES
       ========================================= */
    [data-testid="stAppViewContainer"] {
        background-color: #00000 !important;
        color: #00000;
        padding: 1rem;
    }
    
    /* Contenedor global para el contenido principal */
    .main {
        padding: 1rem;
    }
    
    /* =========================================
       SIDEBAR
       ========================================= */
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

    /* =========================================
       TÍTULOS PRINCIPALES
       ========================================= */
    .main h1 {
        color: #003891;
        font-size: 2.2em;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .main h2, .main h3, .main h4 {
        color: #00000;
    }

    /* =========================================
       FRASE INSPIRADORA
       ========================================= */
    .frase-dia {
        background: #4bb1e0;
        color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #003891;
        margin: 20px 0;
    }

    /* =========================================
       CALENDARIO - CONTAINERS
       ========================================= */
    .calendar-column {
        border: 1px solid #4bb1e0;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.3rem;
        background-color: #f8f9fa;
    }
    
    /* =========================================
       FORMULARIOS (Inputs, Textareas, Selects)
       ========================================= */
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
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #999999;
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
    
    /* =========================================
       EXPANDERS Y TARJETAS
       ========================================= */
    .st-expander {
        background: #ffffff;
        border: 2px solid #4bb1e0;
        border-radius: 10px;
        margin: 10px 0;
        padding: 10px;
    }
    .st-expander .stMarkdown {
        color: #003891;
    }
    .actividad-card {
        background: #ffffff;
        color: #003891;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #4bb1e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .actividad-card b {
        color: #003891;
    }

    /* =========================================
       BOTONES
       ========================================= */
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
    
    /* =========================================
       MENSAJES
       ========================================= */
    .stAlert {
        border: 2px solid #4bb1e0;
        border-radius: 6px;
    }
    .stAlert[data-baseweb="alert"] p {
        margin: 0;
        font-weight: 600;
    }
    .element-container .stAlert[data-baseweb="alert"][style*="background-color: rgb(232, 244, 253)"] {
        background-color: #4bb1e0 !important;
        color: #ffffff !important;
        border-left: 5px solid #003891;
    }
    .element-container .stAlert[data-baseweb="alert"][style*="background-color: rgb(237, 247, 237)"] {
        background-color: #d1dd00 !important;
        color: #003891 !important;
        border-left: 5px solid #003891;
    }
    .element-container .stAlert[data-baseweb="alert"][style*="background-color: rgb(248, 215, 218)"] {
        background-color: #f6c500 !important;
        color: #003891 !important;
        border-left: 5px solid #003891;
    }
    
    /* =========================================
       SCROLLBARS PERSONALIZADOS (OPCIONAL)
       ========================================= */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #ffffff;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #003891;
        border-radius: 4px;
    }
    
    </style>
    """, unsafe_allow_html=True)

import pandas as pd
import os
import streamlit as st
from datetime import datetime

DATA_PATH = os.path.join("data", "MatriculaGeneral.csv")

def cargar_alumnos():
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_csv(DATA_PATH, dtype={'matricula': str})
            date_cols = ['fecha_inscripcion', 'fecha_nacimiento', 'fecha_pago']
            for col in date_cols:
                df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce').dt.strftime('%d/%m/%Y')
            return df.replace({pd.NaT: None}).to_dict('records')
        except Exception as e:
            st.error(f"Error cargando alumnos: {str(e)}")
            return []
    return []

def guardar_alumnos(alumnos):
    df = pd.DataFrame(alumnos)
    column_order = [
        'matricula', 'nombre', 'sexo', 'fecha_inscripcion', 
        'id_grado', 'id_nivel_educativo', 'estado_matricula', 
        'curso', 'paquete', 'metodo_pago', 'fecha_nacimiento',
        'fecha_pago', 'monto_pago', 'saldo_pendiente'
    ]
    df = df[column_order]
    df.to_csv(DATA_PATH, index=False, encoding='utf-8-sig')

def obtener_proxima_matricula():
    try:
        df = pd.read_csv(DATA_PATH, dtype={'matricula': str})
        if df.empty or 'matricula' not in df.columns:
            return "1"
        
        df['matricula_num'] = pd.to_numeric(df['matricula'], errors='coerce')
        if df['matricula_num'].isnull().all():
            return "1"
            
        max_matricula = int(df['matricula_num'].max())
        return str(max_matricula + 1)
    except Exception as e:
        st.error(f"Error calculando matrícula: {str(e)}")
        return "1"
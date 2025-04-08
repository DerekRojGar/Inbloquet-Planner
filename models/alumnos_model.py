import streamlit as st
import pandas as pd
import os
from datetime import datetime

DATA_PATH = os.path.join("data", "MatriculaGeneral.csv")

def cargar_alumnos():
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_csv(DATA_PATH, dtype={'matricula': str})
            # Convertir fechas
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
    # Ordenar columnas como en el CSV original
    df = df[['matricula', 'nombre', 'sexo', 'fecha_inscripcion', 'id_grado', 
             'id_nivel_educativo', 'estado_matricula', 'curso', 'paquete', 
             'metodo_pago', 'fecha_nacimiento', 'fecha_pago', 'monto_pago', 
             'saldo_pendiente']]
    df.to_csv(DATA_PATH, index=False, encoding='utf-8-sig')
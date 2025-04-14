import os
import pandas as pd
import streamlit as st
from datetime import datetime
import ast

DATA_PATH = os.path.join("data", "MatriculaFinal.csv")

def cargar_alumnos():
    """Carga los datos de alumnos desde el CSV manteniendo la estructura original"""
    if not os.path.exists(DATA_PATH):
        return []
    
    try:
        df = pd.read_csv(DATA_PATH, dtype={'Matricula': str})
        
        # Convertir campos de fecha
        date_columns = ['Fecha Inscripción', 'Cumpleaños', 'Fecha Inicio Clases']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce').dt.strftime('%d/%m/%Y')
        
        # Manejar campos especiales
        for list_column in ['pagos', 'clases']:
            if list_column not in df.columns:
                df[list_column] = '[]'
            try:
                df[list_column] = df[list_column].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            except:
                df[list_column] = []
        
        # Manejar monto abonado histórico
        if 'monto_abonado' not in df.columns:
            df['monto_abonado'] = 0.0
        
        return df.replace({pd.NaT: None}).to_dict('records')
    
    except Exception as e:
        st.error(f"Error cargando alumnos: {str(e)}")
        return []

def guardar_alumnos(alumnos):
    """Guarda los datos manteniendo la estructura del CSV original"""
    if not alumnos:
        return
    
    try:
        df = pd.DataFrame(alumnos)
        
        # Orden de columnas
        column_order = [
            'Matricula', 'Nombre', 'Dirección de correo electrónico', 
            'Escuela de provinencia', 'Alergias', 'Observaciones',
            'Nombre Completo del Familiar', 'Parentesco', 
            'Número de teléfono del familiar', 
            'Nombre completo de contacto de emergencia',
            'Número de teléfono de contacto de emergencia', 'Sexo', 
            'Fecha Inscripción', 'Grado', 'Nivel', 'Inscripción', 
            'Cumpleaños', 'Tipo de Curso', 'Vigente', 'Fecha Inicio Clases',
            'monto_abonado', 'pagos', 'clases'
        ]
        
        # Asegurar todas las columnas
        for col in column_order:
            if col not in df.columns:
                df[col] = None
        
        # Convertir listas a strings
        for list_column in ['pagos', 'clases']:
            df[list_column] = df[list_column].apply(str)
        
        # Ordenar y guardar
        df = df[column_order]
        df.to_csv(DATA_PATH, index=False, encoding='utf-8-sig')
    
    except Exception as e:
        st.error(f"Error guardando alumnos: {str(e)}")

def obtener_proxima_matricula():
    """Calcula la siguiente matrícula disponible"""
    try:
        if not os.path.exists(DATA_PATH):
            return "1"
        
        df = pd.read_csv(DATA_PATH, dtype={'Matricula': str})
        
        if df.empty or 'Matricula' not in df.columns:
            return "1"
        
        # Convertir a numérico y encontrar máximo
        df['matricula_num'] = pd.to_numeric(df['Matricula'], errors='coerce')
        max_matricula = df['matricula_num'].max()
        
        return str(int(max_matricula) + 1) if not pd.isnull(max_matricula) else "1"
    
    except Exception as e:
        st.error(f"Error calculando matrícula: {str(e)}")
        return "1"

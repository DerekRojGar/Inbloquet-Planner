import os
import pandas as pd
from datetime import datetime, timedelta

# Constantes para la aplicación
DIAS_ESPAÑOL = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
ESCUELAS = ["INBLOQUET", "AEC", "RW Core", "RW Plus", "AB"]
GRUPOS_POR_ESCUELA = {
    "INBLOQUET": ["Dario", "Emi/Regi", "Roro Mine", "Santi", "Dani", "Romi", "Iker", "Hermanos"],
    "AEC": ["Taller 1", "Taller 2"],
    "RW Core": ["LOBOS", "RINOS", "PANDAS/BUFALOS", "PUMAS/DELFINES"],
    "RW Plus": ["S DUPLO", "S NORMAL", "M", "L"],
    "AB": ["PRESCO", "PA", "PB"]
}

DATA_PATH = os.path.join("data", "actividades.csv")

def generar_semana(año, semana):
    fecha_inicio = datetime(año, 1, 4)
    fecha_inicio = fecha_inicio - timedelta(days=fecha_inicio.weekday())
    fecha_inicio += timedelta(weeks=semana-1)
    return [fecha_inicio + timedelta(days=i) for i in range(6)]  # Lunes a Sábado

def cargar_datos():
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_csv(DATA_PATH)
            if df.empty:
                return {}
            actividades = {}
            for _, row in df.iterrows():
                semana_key = f"{row['Año']}-S{row['Semana']}"
                fecha = row['Fecha']
                actividad = {
                    "Horario": row["Horario"],
                    "Alumnos": row["Alumnos"],
                    "Escuelas": row["Escuelas"],
                    "Grupos": row["Grupos"],
                    "Maestro": row["Maestro"],
                    "Tema": row["Tema"],
                    "Encargado": row["Encargado"],
                    "Notas": row["Notas"]
                }
                if semana_key not in actividades:
                    fechas = [dia.strftime("%d/%m") for dia in generar_semana(int(row['Año']), int(row['Semana']))]
                    actividades[semana_key] = {"fechas": fechas, "actividades": {fecha: [] for fecha in fechas}}
                actividades[semana_key]["actividades"][fecha].append(actividad)
            return actividades
        except pd.errors.EmptyDataError:
            return {}
    return {}

def guardar_datos(actividades):
    all_data = []
    for semana_key, semana_data in actividades.items():
        año_str, semana_num = semana_key.split("-S")
        año = int(año_str)
        semana = int(semana_num)
        for fecha, actividades_dia in semana_data["actividades"].items():
            for act in actividades_dia:
                registro = {"Semana": semana, "Año": año, "Fecha": fecha}
                registro.update(act)
                all_data.append(registro)
    df = pd.DataFrame(all_data)
    # Asegurarse de que exista el directorio de datos
    data_dir = os.path.dirname(DATA_PATH)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    df.to_csv(DATA_PATH, index=False, encoding='utf-8-sig')

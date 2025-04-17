import os
import pandas as pd
from datetime import datetime, timedelta

# Nuevos archivos para escuelas y grupos
ESCUELAS_PATH = os.path.join("data", "escuelas.csv")
GRUPOS_PATH = os.path.join("data", "grupos.csv")
MATRICULA_PATH = os.path.join("data", "matricula_final.csv")
DATA_PATH = os.path.join("data", "actividades.csv")

DIAS_ESPAÑOL = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]

def cargar_escuelas():
    if os.path.exists(ESCUELAS_PATH):
        df = pd.read_csv(ESCUELAS_PATH)
        return df["Escuela"].tolist()
    # Valor por defecto si no existe el archivo
    return ["INBLOQUET", "AEC", "RW", "AB"]

def agregar_escuela(nombre):
    escuelas = cargar_escuelas()
    if nombre not in escuelas:
        escuelas.append(nombre)
        pd.DataFrame({"Escuela": escuelas}).to_csv(ESCUELAS_PATH, index=False)

def cargar_grupos():
    if os.path.exists(GRUPOS_PATH):
        df = pd.read_csv(GRUPOS_PATH)
        grupos = {}
        for _, row in df.iterrows():
            escuela = row["Escuela"]
            grupo = row["Grupo"]
            if escuela not in grupos:
                grupos[escuela] = []
            grupos[escuela].append(grupo)
        return grupos
    # Estructura por defecto
    return {
        "INBLOQUET": ["Dario", "Emi/Regi", "Roro Mine", "Santi", "Dani", "Romi", "Iker", "Hermanos"],
        "AEC": ["Taller 1", "Taller 2"],
        "RW": ["LOBOS", "RINOS", "PANDAS", "BUFALOS", "PUMAS", "DELFINES"],
        "AB": ["DUPLO ALPHA", "DUPLO BETA", "DUPLO GAMA", "DUPLO OMEGA", "ELEMENTAL ALPHA", "ELEMENTAL BETA", "ELEMENTAL GAMA", "ELEMENTAL OMEGA"]
    }

def agregar_grupo(escuela, grupo):
    grupos = cargar_grupos()
    if escuela not in grupos:
        grupos[escuela] = []
    if grupo not in grupos[escuela]:
        grupos[escuela].append(grupo)
        # Guardar en CSV
        rows = []
        for esc, gs in grupos.items():
            for g in gs:
                rows.append({"Escuela": esc, "Grupo": g})
        pd.DataFrame(rows).to_csv(GRUPOS_PATH, index=False)

def cargar_alumnos_activos():
    if os.path.exists(MATRICULA_PATH):
        df = pd.read_csv(MATRICULA_PATH)
        # Suponiendo que hay una columna 'Activo' y 'Nombre'
        activos = df[df["Activo"] == 1]["Nombre"].tolist()
        return activos
    return []

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

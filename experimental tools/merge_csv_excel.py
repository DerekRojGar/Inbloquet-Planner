import pandas as pd

# Cargar los archivos
df_inscripciones = pd.read_csv('InscripcionesCSV.csv', encoding='utf-8')
df_matricula = pd.read_csv('MatriculaGeneral.csv', encoding='utf-8')

# Normalizar nombres para hacer el match
df_inscripciones['nombre_normalizado'] = df_inscripciones['Nombre Completo Alumno'].str.strip().str.lower()
df_matricula['nombre_normalizado'] = df_matricula['nombre'].str.strip().str.lower()

# Combinar los dataframes
df_combinado = pd.merge(
    df_matricula,
    df_inscripciones,
    how='left',
    on='nombre_normalizado',
    suffixes=('_matricula', '_inscripcion')
)

# Eliminar la columna temporal de nombre normalizado
df_combinado.drop('nombre_normalizado', axis=1, inplace=True)

# Guardar el resultado
df_combinado.to_csv('MatriculaCompleta.csv', index=False, encoding='utf-8-sig')
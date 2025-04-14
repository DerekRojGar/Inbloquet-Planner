from datetime import datetime, timedelta
import pandas as pd

def calcular_clases_restantes(fecha_inicio):
    """Calcula las clases restantes considerando solo días hábiles (lunes a sábado)"""
    if not fecha_inicio:
        return 0

    hoy = datetime.today().date()
    clases_restantes = 0
    current_date = fecha_inicio

    # Calcular las próximas 4 clases
    for _ in range(4):
        # Saltar domingos
        while current_date.weekday() == 6:
            current_date += timedelta(days=1)

        if current_date >= hoy:
            clases_restantes += 1

        current_date += timedelta(days=7)

    return clases_restantes

def generar_calendario_clases(fecha_inicio):
    """Genera 4 clases semanales a partir de la fecha de inicio omitiendo domingos"""
    clases = []
    current_date = fecha_inicio
    clases_generadas = 0

    while clases_generadas < 4:
        # Saltar domingos
        if current_date.weekday() == 6:
            current_date += timedelta(days=1)
            continue

        clases.append({
            'fecha': current_date.strftime("%d/%m/%Y"),
            'estado': 'Programada',
            'comentario': ''
        })

        current_date += timedelta(days=7)
        clases_generadas += 1

    return clases

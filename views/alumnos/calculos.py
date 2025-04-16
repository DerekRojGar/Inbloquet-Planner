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

def generar_calendario_clases(fecha_inicio, cantidad=4):
    """
    Genera una lista de dicts de clases a partir de una fecha de inicio.
    Cada clase es semanal (cada 7 días).
    """
    clases = []
    for i in range(cantidad):
        clase = {
            'fecha': (fecha_inicio + timedelta(days=7 * i)).strftime("%d/%m/%Y"),
            'estado': 'Programada',
            'comentario': ''
        }
        clases.append(clase)
    return clases

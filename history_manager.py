# history_manager.py

HISTORY = []

def add_exercise(exercise_type, details):
    global HISTORY
    # Agregar el ejercicio al historial
    HISTORY.append({'type': exercise_type, 'details': details})
    # Limitar el historial a los últimos 8 ejercicios
    if len(HISTORY) > 8:
        HISTORY = HISTORY[-8:]

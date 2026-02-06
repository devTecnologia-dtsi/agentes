"""Tools utilitarias de tiempo/fecha."""

from datetime import datetime
from langchain.tools import tool


@tool
def obtener_tiempo_actual() -> str:
    """Obtiene la fecha y hora actual del sistema en formato legible en español.

    Returns:
        Fecha y hora actual formateada en español.
    """
    tiempo_actual = datetime.now()

    dias = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo",
    ]
    dia_semana = dias[tiempo_actual.weekday()]

    meses = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]
    mes = meses[tiempo_actual.month - 1]

    fecha_hora_str = (
        f"{dia_semana}, {tiempo_actual.day} de {mes} de {tiempo_actual.year}, "
        f"{tiempo_actual.hour:02d}:{tiempo_actual.minute:02d}:{tiempo_actual.second:02d}"
    )
    return fecha_hora_str

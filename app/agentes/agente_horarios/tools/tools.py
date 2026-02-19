"""Herramientas del agente de horarios."""

from datetime import datetime, timedelta
import json
from contextvars import ContextVar

from langchain.tools import tool
from ..services.horario_actual import cargar_datos_horario

# Contexto por request (thread-safe / async-safe)
_usuario_id_ctx: ContextVar = ContextVar("usuario_id", default=None)


def set_usuario_id(usuario_id: str) -> None:
    """Guarda el ID del usuario en el contexto actual."""
    _usuario_id_ctx.set(usuario_id)


TEXTO_SIN_DEFINIR = "No definida"


def _parsear_hora(valor: str) -> tuple[int, int] | None:
    """Convierte HHMM o HH:MM a (hora, minuto)."""
    if valor is None:
        return None

    texto = str(valor).strip()
    if ":" in texto:
        partes = texto.split(":")
        if len(partes) != 2:
            return None
        if not partes[0].isdigit() or not partes[1].isdigit():
            return None
        hora = int(partes[0])
        minuto = int(partes[1])
    else:
        if not texto.isdigit() or len(texto) != 4:
            return None
        hora = int(texto[:2])
        minuto = int(texto[2:])

    if hora < 0 or hora > 23 or minuto < 0 or minuto > 59:
        return None

    return hora, minuto


def _calcular_diferencia_horas(
    hora_desde: str,
    hora_hasta: str,
    dias_hasta: int = 0,
) -> dict | str:
    """Calcula diferencia entre dos horas considerando offset de días."""
    inicio = _parsear_hora(hora_desde)
    fin = _parsear_hora(hora_hasta)

    if inicio is None:
        return (
            "Hora inicial inválida. Usa formato HHMM o HH:MM "
            "(ej: 0957 o 09:57)."
        )
    if fin is None:
        return (
            "Hora final inválida. Usa formato HHMM o HH:MM "
            "(ej: 1645 o 16:45)."
        )
    if dias_hasta < 0:
        return "El parámetro dias_hasta no puede ser negativo."

    base = datetime(2000, 1, 1, inicio[0], inicio[1], 0)
    objetivo = datetime(2000, 1, 1, fin[0], fin[1], 0) + timedelta(
        days=dias_hasta
    )

    diferencia = objetivo - base
    total_minutos = int(diferencia.total_seconds() // 60)

    if total_minutos < 0:
        return (
            "La hora final queda antes de la inicial para el mismo rango de "
            "días. Ajusta dias_hasta o verifica las horas."
        )

    horas = total_minutos // 60
    minutos = total_minutos % 60

    return {
        "hora_desde": f"{inicio[0]:02d}:{inicio[1]:02d}",
        "hora_hasta": f"{fin[0]:02d}:{fin[1]:02d}",
        "dias_hasta": dias_hasta,
        "horas": horas,
        "minutos": minutos,
        "total_minutos": total_minutos,
    }


def _normalizar_registro(d: dict) -> dict:
    """Normaliza null en un registro del horario para uso en tools."""
    return {k: (TEXTO_SIN_DEFINIR if v is None else v) for k, v in d.items()}


@tool
def obtener_datos_horario(dia: str = None) -> str:
    """Consulta el horario del estudiante y devuelve las clases encontradas.

    El servicio entrega los datos sin duplicados, ordenados por día y por
    horaInicio dentro de cada día (entradas sin hora quedan al final).
    horaInicio/horaFin vienen en formato HHMM (ej: 1815 = 18:15).

    Args:
        dia: (Opcional) Día en español ('Lunes', 'Martes', etc.). Si no se pasa,
             se devuelve el horario completo de la semana.
    """
    # id_usuario validado en el endpoint; el contexto se configura antes de invocar al agente
    usuario_id = _usuario_id_ctx.get()
    datos = cargar_datos_horario(usuario_id)

    if datos is None:
        return "Error al consultar el servicio de horarios."

    if not datos:
        return "[]"

    # Filtrar por día si se proporciona
    if dia:
        dia_buscado = dia.strip().capitalize()
        datos = [d for d in datos if (d.get("dia") or "").strip().capitalize() == dia_buscado]
        if not datos:
            return f"No se encontraron clases para el día {dia_buscado}."

    # Normalizar null para que el agente no invente datos
    datos_para_agente = [_normalizar_registro(d) for d in datos]

    try:
        return json.dumps(datos_para_agente, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error al procesar los datos: {str(e)}"


@tool
def obtener_info_profesor() -> str:
    """Obtiene el listado de profesores y sus materias asignadas.

    No requiere parámetros. Devuelve un resumen de los docentes encontrados en el horario del estudiante.
    """
    # id_usuario validado en el endpoint; el contexto se configura antes de invocar al agente
    usuario_id = _usuario_id_ctx.get()
    datos = cargar_datos_horario(usuario_id)
    if datos is None:
        return "Error al consultar el servicio de horarios."
    if not datos:
        return "No se encontró información de profesores en el horario."

    horario = [_normalizar_registro(d) for d in datos]
    info_profesor = {}
    sin_docente = []

    for clase in horario:
        docente = clase.get("docente")
        materia = clase.get("materia", "Desconocida")
        nrc = clase.get("nrc", "N/A")
        if not docente or docente == TEXTO_SIN_DEFINIR:
            # Agrupar materias sin docente para reportarlas
            # Usamos un set de tuplas (materia, nrc) para evitar duplicados si la materia tiene varios horarios
            sin_docente.append((materia, nrc))
            continue
            
        # Inicializar estructura
        if docente not in info_profesor:
            info_profesor[docente] = {"materias": set(), "clases": 0}
        # Contar materia única
        info_profesor[docente]["materias"].add(
            (materia, nrc)
        )
        # Contar cada horario
        info_profesor[docente]["clases"] += 1

    if not info_profesor and not sin_docente:
        return "No se encontró información de profesores en el horario."

    resultado = []
    
    # 1. Reportar docentes encontrados
    if info_profesor:
        for docente, datos in info_profesor.items():
            materias_texto = ", ".join(
                [f"{m} (NRC {nrc})" for m, nrc in datos["materias"]]
            )
            texto = (
                f"- **{docente}**: Dicta {len(datos['materias'])} "
                f"materia(s): {materias_texto}. "
                f"({datos['clases']} sesiones de clase)"
            )
            resultado.append(texto)
    
    # 2. Reportar materias sin docente asignado (IMPORTANTE para no mentir)
    if sin_docente:
        # Eliminar duplicados
        sin_docente_unicas = sorted(list(set(sin_docente)))
        materias_sin_docente_texto = ", ".join(
            [f"{m} (NRC {nrc})" for m, nrc in sin_docente_unicas]
        )
        texto_sin_docente = (
            f"\n**Materias sin docente asignado en el sistema**:\n"
            f"El sistema no reporta profesor para las siguientes {len(sin_docente_unicas)} materias: "
            f"{materias_sin_docente_texto}."
        )
        resultado.append(texto_sin_docente)

    return "\n".join(resultado)


import pytz  

@tool
def obtener_tiempo_actual():
    """Obtiene la fecha y hora actual del sistema (zona America/Bogota).
    
    No requiere parámetros. 
    
    IMPORTANTE: Usa esta herramienta SIEMPRE que el usuario pregunte por "hoy", "mañana", "ahora", "próxima clase", etc.
    
    Devuelve un diccionario con:
    - 'dia_semana': El nombre del día de la semana en español (Lunes, Martes, etc.) - USA ESTE CAMPO para consultas por día
    - 'legible': Fecha y hora completa en formato legible para humanos
    - 'iso': Fecha/hora en formato ISO 8601 para cálculos
    - 'timezone': Zona horaria (America/Bogota)
    
    Después de llamar esta herramienta, DEBES llamar a obtener_datos_horario(dia=...) usando el valor de 'dia_semana'."""
    bogota_tz = pytz.timezone('America/Bogota')
    tiempo_actual = datetime.now(bogota_tz)

    # Nombres de los días en español
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

    # Nombres de los meses en español
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

    # Formato legible en español
    fecha_hora_str = (
        f"{dia_semana}, {tiempo_actual.day} de {mes} de {tiempo_actual.year}, "
        f"{tiempo_actual.hour:02d}:{tiempo_actual.minute:02d}:"
        f"{tiempo_actual.second:02d}"
    )
    
    # Formato ISO 8601 para operaciones IA
    iso_str = tiempo_actual.isoformat()
    
    return {
        'dia_semana': dia_semana,  # Día de la semana extraído explícitamente
        'legible': fecha_hora_str,
        'iso': iso_str,
        'timezone': str(tiempo_actual.tzinfo)
    }


@tool
def calcular_diferencia_horas(
    hora_desde: str,
    hora_hasta: str,
    dias_hasta: int = 0,
):
    """Calcula la diferencia exacta entre dos horas.

    Acepta horas en formato HHMM o HH:MM.

    Args:
        hora_desde: Hora inicial (ej: 0957 o 09:57).
        hora_hasta: Hora final (ej: 1645 o 16:45).
        dias_hasta: Días entre hora_desde y hora_hasta. Usa 1 para "mañana".

    Retorna:
        Diccionario con horas, minutos y total_minutos.
    """
    return _calcular_diferencia_horas(hora_desde, hora_hasta, dias_hasta)

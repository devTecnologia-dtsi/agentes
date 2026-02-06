"""Herramientas del agente de horarios."""

from datetime import datetime
import json
from contextvars import ContextVar

from langchain.tools import tool
from ..services.horario_actual import cargar_datos_horario

# Contexto por request (thread-safe / async-safe)
_usuario_id_ctx: ContextVar = ContextVar("usuario_id", default=None)


def set_usuario_id(usuario_id: str) -> None:
    """Guarda el ID del usuario en el contexto actual."""
    _usuario_id_ctx.set(usuario_id)


@tool
def obtener_datos_horario() -> str:
    """Obtiene el horario completo del estudiante con todas sus clases y materias.
    
    Consulta el servicio externo bajo demanda.
    Devuelve un JSON con la información del horario incluyendo materias, horarios, profesores, días, etc.
    """
    usuario_id = _usuario_id_ctx.get()
    if usuario_id is None:
        return "Error: No se ha establecido el ID del usuario."
        
    datos = cargar_datos_horario(usuario_id)
    
    if datos is None:
        return "Error al consultar el servicio de horarios."
        
    try:
        resultado = json.dumps(datos, indent=2, ensure_ascii=False)
        if not isinstance(resultado, str):
            resultado = str(resultado)
        return resultado
    except Exception as e:
        error_msg = f"Error al procesar los datos: {str(e)}"
        return str(error_msg)


@tool
def obtener_info_profesor() -> str:
    """Obtiene el listado de profesores, sus materias y clases asignadas.
    
    Úsala SIEMPRE que pregunten:
    - "¿Quién es el profesor de [materia]?"
    - "¿Qué profesores tengo?"
    - Información de contacto o detalles de los docentes.
    
    Devuelve un resumen texto con:
    - Nombre del docente.
    - Materias que dicta (con NRC).
    - Cantidad de clases.
    """
    horario_str = obtener_datos_horario.invoke({})
    if horario_str is None or horario_str == "No hay datos cargados":
        return "No hay datos cargados"

    try:
        horario = json.loads(horario_str)
    except json.JSONDecodeError:
        return "Error al procesar los datos del horario"

    info_profesor = {}
    for clase in horario:
        docente = clase.get("docente")
        if not docente:
            continue
        # Inicializar estructura
        if docente not in info_profesor:
            info_profesor[docente] = {"materias": set(), "clases": 0}
        # Contar materia única
        info_profesor[docente]["materias"].add(
            (clase["materia"], clase["nrc"])
        )
        # Contar cada horario
        info_profesor[docente]["clases"] += 1

    if not info_profesor:
        return "No se encontró información de profesores en el horario."

    resultado = []
    for docente, datos in info_profesor.items():
        materias_texto = ", ".join(
            [f"{m} (NRC {nrc})" for m, nrc in datos["materias"]]
        )
        texto = (
            f"{docente} dicta {len(datos['materias'])} "
            f"materia(s): {materias_texto}. "
            f"Tiene {datos['clases']} clase(s)."
        )
        resultado.append(texto)

    return "\n".join(resultado)


@tool
def obtener_tiempo_actual():
    """Obtiene la fecha y hora actual del sistema en formato legible."""
    tiempoActual = datetime.now()

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
    dia_semana = dias[tiempoActual.weekday()]

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
    mes = meses[tiempoActual.month - 1]

    # Formato de fecha en español
    fecha_hora_str = (
        f"{dia_semana}, {tiempoActual.day} de {mes} de {tiempoActual.year}, "
        f"{tiempoActual.hour:02d}:{tiempoActual.minute:02d}:"
        f"{tiempoActual.second:02d}"
    )
    return str(fecha_hora_str)

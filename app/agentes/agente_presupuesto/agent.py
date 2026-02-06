
from app.services.ai import instanciar_agente
from .prompt.system_prompt import SYSTEM_PROMPT

from .clase import get_tools as clase_tools
from .componente import get_tools as componente_tools
from .contrato import get_tools as contrato_tools
from .dtsi import get_tools as dtsi_tools
from .cuenta import get_tools as cuenta_tools
from .estado import get_tools as estado_tools
from .negociacion import get_tools as negociacion_tools
from .orden import get_tools as orden_tools
from .origen import get_tools as origen_tools
from .otro_si import get_tools as otro_si_tools
from .presupuesto import get_tools as presupuesto_tools
from .proveedor import get_tools as proveedor_tools
from .responsable import get_tools as responsable_tools
from .tipo import get_tools as tipo_tools

herramientas = (
    clase_tools()
    + componente_tools()
    + contrato_tools()
    + dtsi_tools()
    + cuenta_tools()
    + estado_tools()
    + negociacion_tools()
    + orden_tools()
    + origen_tools()
    + otro_si_tools()
    + presupuesto_tools()
    + proveedor_tools()
    + responsable_tools()
    + tipo_tools()
)

def construir_agente_presupuesto(modelo_ia: str = "gemini"):
    """Construye el agente de presupuesto y lo instancia con el modelo especificado.
   
    Parámetros:
        modelo_ia: Nombre del modelo ("gemini", "openai")
   
    Retorna:
        Agente de presupuesto inicializado
    """
    return instanciar_agente(herramientas, SYSTEM_PROMPT, modelo_ia)

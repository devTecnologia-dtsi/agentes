
import datetime
import requests
from .config import get_base_url, get_headers
from app.core.logging import get_logger

logger = get_logger(__name__)

class CalificacionesService:

    suffixes = [
        "84","69","55","44","43","42","62",
        "41","40","38","27","25","21","64",
        "15","12","11","10","07","05","61",
        "00","97","95","93","91","90","86",
        "85","80","71","67","65","60"
    ]

    def get_current_year(self) -> str:
        return str(datetime.datetime.now().year)

    def build_period_list(self):
        year = self.get_current_year()
        return [f"{year}{suffix}" for suffix in self.suffixes]

    def fetch_notas(self, estudiante_id: str):
        """Busca calificaciones en todos los periodos del año actual."""

        headers = get_headers()

        periodos = self.build_period_list()
        resultados = []

        for periodo in periodos:

            params = {
                "id": estudiante_id,
                "periodo": periodo
            }

            try:
                resp = requests.get(
                    url = f"{get_base_url()}/servicios-banner/calificacionActual",
                    params=params,
                    headers=headers,
                    timeout=60
                )

                try:
                    data = resp.json()
                except ValueError:
                    continue

                if resp.status_code == 200 and data.get("calificaciones"):
                    logger.info(f"Calificaciones encontradas para {periodo}")
                    resultados.append({
                        "periodo": periodo,
                        "calificaciones": data["calificaciones"]
                    })

            except requests.exceptions.RequestException as e:
                logger.warning(f"Error consultando periodo {periodo}: {e}")
                continue

        if resultados:
            return resultados
        
        return {"error": f"No se encontraron calificaciones para {estudiante_id}"}

    def extraer_calificaciones(self, data):
        """Normaliza las materias para que el agente las entienda bien."""

        if "calificaciones" not in data:
            return []

        materias = []

        for m in data["calificaciones"]:

            # Definir definitiva
            if m.get("PARCIAL_ACUM"):
                definitiva = float(m["PARCIAL_ACUM"])
            elif m.get("NOTA_UNICA"):
                definitiva = float(m["NOTA_UNICA"])
            else:
                definitiva = None

            materias.append({
                "codigo": m.get("COD_MAT"),
                "materia": m.get("DESC_MAT"),
                "parcial1": float(m["PARCIAL1"]) if m.get("PARCIAL1") else None,
                "parcial2": float(m["PARCIAL2"]) if m.get("PARCIAL2") else None,
                "examen": float(m["EXAMEN"]) if m.get("EXAMEN") else None,
                "notaUnica": float(m["NOTA_UNICA"]) if m.get("NOTA_UNICA") else None,
                "definitiva": definitiva,
                "nrc": m.get("NRC"),
                "periodo": m.get("PERIODO")
            })

        return materias

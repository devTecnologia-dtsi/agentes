
import datetime
from datetime import datetime as dt
import requests
import unicodedata
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

    def obtener_anio_actual(self) -> str:
        return str(datetime.datetime.now().year)

    def lista_periodos(self):
        year = self.obtener_anio_actual()
        return [f"{year}{suffix}" for suffix in self.suffixes]
    
    def consultar_periodo(self, estudiante_id: str, periodo: str) -> dict | None:
        """
        Consulta la API para un SOLO periodo.
        Retorna el payload crudo o None si no hay datos.
        """
        try:
            resp = requests.get(
                url=f"{get_base_url()}/servicios-banner/calificacionActual",
                params={"id": estudiante_id, "periodo": periodo},
                headers=get_headers(),
                timeout=60
            )

            if resp.status_code != 200:
                return None

            data = resp.json()
            if not data.get("calificaciones"):
                return None

            return data

        except requests.exceptions.RequestException as e:
            logger.warning(f"Error consultando periodo {periodo}: {e}")
            return None

    def buscar_notas(self, estudiante_id: str)-> list[dict]:
        """
        Devuelve todas las calificaciones encontradas por periodo
        sin interpretación semántica.
        """
        resultados = []

        for periodo in self.lista_periodos():
            data = self.consultar_periodo(estudiante_id, periodo)
            if not data:
                continue

            resultados.append({
                "periodo": periodo,
                "calificaciones": data["calificaciones"]
            })

        return resultados
    
    def _parse_fecha(self, fecha: str | None):
        if not fecha:
            return None
        try:
            return dt.strptime(fecha, "%d-%b-%y").date()
        except Exception:
            return None
        
    def _normalizar_texto(self, texto: str) -> str:
        """
        Normaliza texto:
        - Quita tildes
        - Minúsculas
        - Elimina espacios extra
        """
        if not texto:
            return ""

        texto = texto.strip().lower()
        texto = unicodedata.normalize("NFD", texto)
        texto = texto.encode("ascii", "ignore").decode("utf-8")

        return " ".join(texto.split())



    def extraer_calificaciones(self, data) -> list[dict]:
        """Normaliza las materias para que el agente las entienda bien.""" 
        
        materias = []

        for m in data.get("calificaciones", []):

            definitiva = (
                float(m["PARCIAL_ACUM"])
                if m.get("PARCIAL_ACUM") is not None
                else float(m["NOTA_UNICA"])
                if m.get("NOTA_UNICA") is not None
                else None
            )

            materias.append({
                "codigo": m.get("COD_MAT"),
                "materia": m.get("DESC_MAT"),
                "materia_normalizada": self._normalizar_texto( m.get("DESC_MAT")),
                "parcial1": float(m["PARCIAL1"]) if m.get("PARCIAL1") else None,
                "parcial2": float(m["PARCIAL2"]) if m.get("PARCIAL2") else None,
                "examen": float(m["EXAMEN"]) if m.get("EXAMEN") else None,
                "nota_unica": float(m["NOTA_UNICA"]) if m.get("NOTA_UNICA") else None,
                "definitiva": definitiva,
                "periodo": m.get("PERIODO"),
                "nrc": m.get("NRC"),
            })

        return materias
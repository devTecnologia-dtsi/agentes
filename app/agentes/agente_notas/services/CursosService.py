import requests
from datetime import datetime
import unicodedata
from .config import get_base_url, get_headers

class CursosService:

    def _normalizar_texto(self, texto: str) -> str:
        if not texto:
            return ""

        texto = texto.strip().lower()
        texto = unicodedata.normalize("NFD", texto)
        texto = texto.encode("ascii", "ignore").decode("utf-8")

        return " ".join(texto.split())
    
    def fetch_cursos(self, id_estudiante: str):
        """
        Llama a la API de cursos actuales del estudiante.
        """

        try:
            params = {"id": id_estudiante}

            headers = get_headers()

            resp = requests.get(
                url = f"{get_base_url()}/servicios-banner/consultaCursos",
                params=params,
                headers=headers,
                timeout=60
            )

            if resp.status_code != 200:
                return {
                    "error": True,
                    "message": f"No se pudo obtener la información del estudiante. URL: {resp.url} Status: {resp.status_code}, Response: {resp.text}"
                }

            data = resp.json()

            return {
                "error": False,
                "informacion": data.get("informacion", {}),
                "cursos": data.get("cursos", [])
            }

        except requests.RequestException as e:
            return {
                "error": True,
                "message": f"Error en solicitud HTTP: {str(e)}"
            }


    def obtener_cursos(self, id_estudiante: str):
        """
        Obtiene y limpia la lista de cursos actuales del estudiante.
        """
        data = self.fetch_cursos(id_estudiante)

        if data.get("error"):
            return data

        cursos_raw = data.get("cursos", [])

        cursos_limpios = []

        for c in cursos_raw:
            nombre = c.get("nombre")

            cursos_limpios.append({
                "codigo": c.get("codigo"),
                "materia": c.get("nombre"),
                "materia_normalizada": self._normalizar_texto(nombre),
                "inicio": c.get("inicio"),     
                "fin": c.get("final"), 
                "periodo": c.get("periodo")
            })

        return {
            "error": False,
            "cursos": cursos_limpios
        }

    def obtener_informacion_estudiante(self, id_estudiante: str):
        """
        Obtiene la información académica básica del estudiante (programa, facultad, etc.).
        """
        data = self.fetch_cursos(id_estudiante)

        if data.get("error"):
            return data

        info = data.get("informacion", {})

        return {
            "codigoLargo": info.get("Programa", {}).get("codigoLargo"),
            "programa": info.get("Programa", {}).get("nombre"),
            "nivel": info.get("Nivel", {}).get("nombre"),
            "facultad": info.get("Facultad", {}).get("nombre"),
            "sede": info.get("Sede", {}).get("nombre"),
            "modalidad": info.get("Modalidad", {}).get("nombre"),
            "periodo": info.get("Periodo", {}).get("nombre"),
        }
    
    
    def formatear_fecha_es(self, fecha_str: str):
        try:
            fecha = datetime.strptime(fecha_str, "%d-%b-%y")

            dias_es = {
                "Monday": "lunes",
                "Tuesday": "martes",
                "Wednesday": "miércoles",
                "Thursday": "jueves",
                "Friday": "viernes",
                "Saturday": "sábado",
                "Sunday": "domingo",
            }

            meses_es = {
                1: "enero", 2: "febrero", 3: "marzo",
                4: "abril", 5: "mayo", 6: "junio",
                7: "julio", 8: "agosto", 9: "septiembre",
                10: "octubre", 11: "noviembre", 12: "diciembre",
            }

            dia_semana = dias_es.get(fecha.strftime("%A"), "")
            mes = meses_es.get(fecha.month, "")

            return f"{dia_semana} {fecha.day} de {mes} de {fecha.year}"

        except Exception:
            return fecha_str

    def calcular_contexto_fecha(self, fecha_str: str):
        try:
            fecha = datetime.strptime(fecha_str, "%d-%b-%y")
            hoy = datetime.now()

            diferencia = (fecha.date() - hoy.date()).days

            if diferencia == 0:
                return "es hoy"
            elif diferencia == 1:
                return "es mañana"
            elif diferencia > 1:
                return f"es en {diferencia} días"
            elif diferencia == -1:
                return "fue ayer"
            else:
                return f"fue hace {abs(diferencia)} días"

        except Exception:
            return ""

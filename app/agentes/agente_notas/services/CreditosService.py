import requests
from .CursosService import CursosService
from .config import get_base_url, get_headers
import unicodedata
class CreditosService:
    """
    Servicio encargado de consultar y procesar
    el cumplimiento académico y créditos del estudiante.
    """

    def normalizar_texto(self, texto: str) -> str:
        texto = texto.lower().strip()
        texto = unicodedata.normalize("NFD", texto)
        texto = texto.encode("ascii", "ignore").decode("utf-8")
        return texto

    def fetch_cumplimiento(self, id_estudiante: str, programa: str):
        """Llama a la API de cumplimiento académico."""
        try:
            params = {
                "id": id_estudiante,
                "programa": programa
            }

            headers = get_headers()

            resp = requests.get(
                url=f"{get_base_url()}/servicios-banner-dos/cumplimientoCursos",
                params=params,
                headers=headers,
                timeout=60
            )

            if resp.status_code != 200:
                return {"error": True, "message": f"No se pudo obtener cumplimiento académico. Status: {resp.status_code}, Response: {resp.text}"}

            data = resp.json()

            return {
                "error": False,
                "cursadas": data.get("rutaAcademica", {}).get("cursadas", []),
                "perdidas": data.get("rutaAcademica", {}).get("perdidas", []),
                "pendientes": data.get("rutaAcademica", {}).get("pendientes", [])
            }

        except requests.RequestException as e:
            return {"error": True, "message": f"Error en solicitud HTTP: {str(e)}"}
        

    def _obtener_cumplimiento_base(self, id_estudiante: str):
        
        cursos_service = CursosService()
        info_cursos = cursos_service.fetch_cursos(id_estudiante)

        if info_cursos.get("error"):
            return info_cursos

        programa = (
            info_cursos
            .get("informacion", {})
            .get("Programa", {})
            .get("codigoLargo")
        )

        if not programa:
            return {"error": True, "message": "No se encontró el código largo del programa."}

        raw = self.fetch_cumplimiento(id_estudiante, programa)

        if raw.get("error"):
            return raw

        return {
            "error": False,
            "cursadas": raw.get("cursadas", []),
            "perdidas": raw.get("perdidas", []),
            "pendientes": raw.get("pendientes", []),
        }

    def normalizar_cursadas(self, data):
        return [
            {
                "materia": m.get("NOMBRE_CURSO"),
                "creditos": int(m.get("CRED_CURSO", 0)),
                "sem_terminado": m.get("SEM_TERMINADO"),
            }
            for m in data
        ]
    
    def normalizar_perdidas(self, data):
        return [
            {
                "materia": m.get("NOMBRE_CURSO"),
                "creditos": int(m.get("CRED_CURSO", 0)),
                "nota": m.get("NOTA_CURSO"),
                "periodo": m.get("PERIODO"),
            }
            for m in data
        ]

    def normalizar_pendientes(self, data):
        return [
            {
                "materia": m.get("NOMBRE_CURSO")
            }
            for m in data
        ]

    def obtener_resumen_creditos(self, id_estudiante: str):
        """
        Retorna únicamente el resumen de créditos.
        """
        data = self._obtener_cumplimiento_base(id_estudiante)

        if data.get("error"):
            return data

        return {
            "error": False,
            "aprobados": sum(int(m.get("CRED_CURSO", 0)) for m in data["cursadas"]),
            "perdidos": sum(int(m.get("CRED_CURSO", 0)) for m in data["perdidas"]),
            "pendientes": sum(int(m.get("CRED_CURSO", 0)) for m in data["pendientes"]),
        }

    def obtener_materias_por_estado(self, id_estudiante: str):

        data = self._obtener_cumplimiento_base(id_estudiante)

        if not data:
            return {"error": "No se obtuvo respuesta de la API"}

        if isinstance(data, dict) and data.get("error"):
            return data

        return {
            "error": False,
            "cursadas": self.normalizar_cursadas(data["cursadas"]),
            "perdidas": self.normalizar_perdidas(data["perdidas"]),
            "pendientes": self.normalizar_pendientes(data["pendientes"]),
        }

    def buscar_creditos_materia(self, id_estudiante: str, nombre_materia: str):

        data = self._obtener_cumplimiento_base(id_estudiante)

        if data.get("error"):
            return data

        nombre_materia = self.normalizar_texto(nombre_materia)

        for grupo in ["cursadas", "perdidas", "pendientes"]:
            for m in data[grupo]:
                nombre_api = self.normalizar_texto(m.get("NOMBRE_CURSO", ""))

                if nombre_materia in nombre_api:
                    return {
                        "error": False,
                        "materia": m.get("NOMBRE_CURSO"),
                        "creditos": int(m.get("CRED_CURSO", 0))
                    }

        return {"error": True, "message": "No se encontró la materia"}

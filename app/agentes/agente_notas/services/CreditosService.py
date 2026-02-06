import requests
from .CursosService import CursosService
from .config import get_base_url, get_headers

class CreditosService:
    """
    Servicio encargado de consultar y procesar
    el cumplimiento académico y créditos del estudiante.
    """

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

            try:
                data = resp.json()
            except ValueError:
                return {"error": True, "message": "Respuesta inválida de API de cumplimiento"}

            return {
                "error": False,
                "cursadas": data.get("rutaAcademica", {}).get("cursadas", []),
                "perdidas": data.get("rutaAcademica", {}).get("perdidas", []),
                "pendientes": data.get("rutaAcademica", {}).get("pendientes", [])
            }

        except requests.RequestException as e:
            return {"error": True, "message": f"Error en solicitud HTTP: {str(e)}"}

    def normalizar_cursadas(self, data):
        materias = []
        for m in data:
            materias.append({
                "curso": m.get("CURSO"),
                "nombre": m.get("NOMBRE_CURSO"),
                "creditosCurso": int(m["CRED_CURSO"]) if m.get("CRED_CURSO") else 0,
                "area": m.get("AREA_DESC"),
                "semestre": m.get("SEMESTRE"),
                "periodoTerminado": m.get("SEM_TERMINADO"),
            })
        return materias

    def normalizar_listado_simple(self, data):
        materias = []
        for m in data:
            materias.append({
                "curso": m.get("CURSO"),
                "nombre": m.get("NOMBRE_CURSO"),
                "creditosCurso": int(m["CRED_CURSO"]) if m.get("CRED_CURSO") else 0,
                "area": m.get("AREA_DESC"),
                "semestre": m.get("SEMESTRE"),
            })
        return materias

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
            "cursadas": self.normalizar_cursadas(raw["cursadas"]),
            "perdidas": self.normalizar_listado_simple(raw["perdidas"]),
            "pendientes": self.normalizar_listado_simple(raw["pendientes"]),
        }

    def obtener_resumen_creditos(self, id_estudiante: str):
        """
        Retorna únicamente el resumen de créditos.
        """
        data = self._obtener_cumplimiento_base(id_estudiante)

        if data.get("error"):
            return data

        return {
            "error": False,
            "aprobados": sum(m["creditosCurso"] for m in data["cursadas"]),
            "perdidos": sum(m["creditosCurso"] for m in data["perdidas"]),
            "pendientes": sum(m["creditosCurso"] for m in data["pendientes"]),
        }

    def obtener_detalle_materias(self, id_estudiante: str):
        """
        Retorna el listado completo de materias por estado.
        """
        data = self._obtener_cumplimiento_base(id_estudiante)

        if data.get("error"):
            return data

        return {
            "error": False,
            "cursadas": data["cursadas"],
            "perdidas": data["perdidas"],
            "pendientes": data["pendientes"],
        }

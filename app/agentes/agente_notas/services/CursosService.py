import requests
from .config import get_base_url, get_headers

class CursosService:

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

            try:
                data = resp.json()
            except ValueError:
                return {
                    "error": True,
                    "message": "Respuesta inválida de la API de cursos."
                }

            return {
                "error": False,
                "informacion": data.get("informacion", {}),
                "cursos": data.get("cursos", [])
            }

        except Exception as e:
            return {"error": True, "message": f"Error interno: {e}"}


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
            cursos_limpios.append({
                "codigo": c.get("codigo"),
                "materia": c.get("nombre"),
                "codigoMateria": c.get("codigoMateria"),
                "inicio": c.get("inicio"),
                "final": c.get("final"),
                "periodo": c.get("periodo"),
                "descripcion": c.get("descripcion"),
            })

        return cursos_limpios

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

import requests
from .config import get_historial_url
import unicodedata

# Tabla de sufijos y descripciones
suffixes = {
    '84': '-3',
    '69': '-1',
    '55': '-3',
    '44': '-1',
    '43': '-1',
    '42': 'Op Grado Dis Ene-Abr',
    '41': '-1',
    '40': '-1',
    '38': '-1',
    '27': '-3',
    '25': '-1',
    '21': '-1',
    '15': '-1',
    '12': '-1',
    '11': '-1',
    '10': '-1',
    '07': '-3',
    '05': '-1',
    '00': 'Cumplimiento plan estudios 26',
    '97': '-11',
    '95': '-9',
    '93': '-7',
    '91': '-5',
    '90': 'Educación Continua',
    '86': 'Op Grado Presenci Jul-Dic',
    '85': 'Op Grado Sem Ene-Jun',
    '80': 'Intersemestral Dic-Ene',
    '71': '-2',
    '67': '-11',
    '65': '-2',
    '64': '-9',
    '62': '-2',
    '61': '-2',
    '60': '-2',
}
 
class HistorialService:

    def _formatear_periodo(self, term_code: str) -> str:
        """
        Convierte 202660 → 2026-2
        """
        if not term_code or len(term_code) < 6:
            return "Periodo desconocido"

        year = term_code[:4]
        suffix = term_code[-2:]

        suffix_desc = suffixes.get(suffix)

        if not suffix_desc:
            return f"{year}-?"

        # Si es formato tipo -1, -2, -3
        if suffix_desc.startswith("-"):
            return f"{year}{suffix_desc}"

        # Si es descripción especial (Educación Continua, etc)
        return f"{year} ({suffix_desc})"
    
    def _normalizar_texto(self, texto: str) -> str:
        """
        Normaliza texto:
        - Quita tildes
        - Pasa a minúsculas
        - Elimina espacios extra
        """
        if not texto:
            return ""

        texto = texto.strip().lower()
        texto = unicodedata.normalize("NFD", texto)
        texto = texto.encode("ascii", "ignore").decode("utf-8")

        return " ".join(texto.split())

    def buscar_historial(self, id_estudiante: str):
        try:
            resp = requests.get(
                get_historial_url(),
                params={"V_ID": id_estudiante},
                timeout=60
            )

            if resp.status_code != 200:
                return {"error": True, "message": "No se pudo obtener la información del estudiante."}

            data = resp.json()

            if isinstance(data, list):
                return {"error": False, "historial": data}

            return {"error": False, "historial": data.get("historial", [])}

        except requests.RequestException as e:
            return {"error": True, "message": f"Error interno: {e}"}

    def obtener_historial(self, id_estudiante: str):
        response = self.buscar_historial(id_estudiante)

        if response.get("error"):
            return response

        historial_limpio = []

        for curso in response.get("historial", []):
            term_code = curso.get("V_TERM_CODE", "")

            historial_limpio.append({
                "codigo": curso.get("V_CRN"),
                "materia": curso.get("V_CRSE_TITLE"),
                "materia_normalizada": self._normalizar_texto(curso.get("V_CRSE_TITLE")),
                "periodo": self._formatear_periodo(term_code),
                "nota": curso.get("V_GRDE_CODE_MID"),
                "termCode": term_code
            })

        return {
            "error": False,
            "historial": historial_limpio
        }
    
    def _buscar_coincidencias(self, historial, nombre_materia):
        nombre_normalizado = self._normalizar_texto(nombre_materia)

        return [
            curso for curso in historial
            if nombre_normalizado in curso["materia_normalizada"]
        ]
    

    def obtener_nota_materia(self, id_estudiante: str, nombre_materia: str):
        response = self.obtener_historial(id_estudiante)

        if response.get("error"):
            return response

        coincidencias = self._buscar_coincidencias(
                response["historial"],
                nombre_materia
            )
        
        if not coincidencias:
            return {"error": True, "message": "No se encontró la materia"}

        return {
            "error": False,
            "tipo_nota": "Parcial",
            "advertencia": "La nota corresponde a un registro parcial del sistema académico. Se recomienda validar la nota definitiva en la plataforma oficial de la universidad.",
            "total_veces_cursada": len(coincidencias),
            "resultados": [
                {
                    "materia": c["materia"],
                    "nota": c["nota"],
                    "periodo": c["periodo"]
                }
                for c in coincidencias
            ]
        }


    def obtener_semestre_materia(self, id_estudiante: str, nombre_materia: str):
        response = self.obtener_historial(id_estudiante)

        if response.get("error"):
            return response

        coincidencias = self._buscar_coincidencias(
            response["historial"],
            nombre_materia
        )

        if not coincidencias:
            return {"error": True, "message": "No se encontró la materia"}

        return {
            "error": False,
            "total_veces_cursada": len(coincidencias),
            "resultados": [
                {
                    "materia": c["materia"],
                    "semestre": c["periodo"],
                    "nota": c["nota"]
                }
                for c in coincidencias
            ]
        }

    def contar_veces_materia(self, id_estudiante: str, nombre_materia: str):
        response = self.obtener_historial(id_estudiante)

        if response.get("error"):
            return response

        coincidencias = self._buscar_coincidencias(
            response["historial"],
            nombre_materia
        )

        return {
            "error": False,
            "materia_consultada": nombre_materia,
            "total_veces_cursada": len(coincidencias)
        }
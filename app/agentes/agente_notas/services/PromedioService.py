import requests
from .config import get_promedio_url


class PromedioService:

    def obtener_promedio_estudiante(self, id_estudiante: str):
        try:
            base_url = get_promedio_url().rstrip("/")
            url = f"{base_url}/{id_estudiante}"

            resp = requests.get(
                url=url,
                timeout=60
            )

            if resp.status_code != 200:
                return {
                    "error": True,
                    "message": "No se pudo obtener el promedio del estudiante."
                }

            data = resp.json()

            if not isinstance(data, list) or not data:
                return {
                    "error": True,
                    "message": "No se encontró información del estudiante."
                }

            promedio = data[0].get("PROM_ESTU")

            return {
                "error": False,
                "promedio_acumulado": round(float(promedio), 2) if promedio else None
            }

        except requests.RequestException as e:
            return {
                "error": True,
                "message": f"Error interno: {e}"
            }

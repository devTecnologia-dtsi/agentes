import requests
from ..config_pre import API_PRESUPUESTO

class ClaseService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar clases.
    """

    def listar_clases(self):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/clases", timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_clase(self, id: int):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/clases/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def crear_clase(self, cod: str, clase: str):
        try:
            payload = {
                "cod": cod,
                "clase": clase
            }
            resp = requests.post(
                f"{API_PRESUPUESTO}/clases",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def actualizar_clase(self, id: int, cod: str | None = None, clase: str | None = None):
        try:
            payload = {"id": id}

            # Solo se envía lo que el usuario quiere modificar
            if cod is not None:
                payload["cod"] = cod

            if clase is not None:
                payload["clase"] = clase

            resp = requests.put(
                f"{API_PRESUPUESTO}/clases/{id}",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()

        except requests.RequestException as e:
            return {"error": True, "message": str(e)}


    def eliminar_clase(self, id: int):
        try:
            resp = requests.delete(
                f"{API_PRESUPUESTO}/clases/{id}",
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
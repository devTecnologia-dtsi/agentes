import requests
from ..config_pre import API_PRESUPUESTO

class TipoService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar tipos.
    """

    def listar_tipos(self):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/tipo", timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_tipo(self, id: int):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/tipo/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def crear_tipo(self, cod: str, tipo: str):
        try:
            payload = {
                "cod": cod,
                "tipo": tipo
            }
            resp = requests.post(
                f"{API_PRESUPUESTO}/tipo",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def actualizar_tipo(self, id: int, cod: str | None = None, tipo: str | None = None):
        try:
            payload = {"id": id}

            # Solo se envía lo que el usuario quiere modificar
            if cod is not None:
                payload["cod"] = cod

            if tipo is not None:
                payload["tipo"] = tipo

            resp = requests.put(
                f"{API_PRESUPUESTO}/tipo/{id}",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()

        except requests.RequestException as e:
            return {"error": True, "message": str(e)}


    def eliminar_tipo(self, id: int):
        try:
            resp = requests.delete(
                f"{API_PRESUPUESTO}/tipo/{id}",
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
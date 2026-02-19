import requests
from ..config_pre import API_PRESUPUESTO


class ComponenteService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar componentes.
    """

    def listar_componentes(self):
        try:
            resp = requests.get(
                f"{API_PRESUPUESTO}/componente",
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_componente(self, id: int):
        try:
            resp = requests.get(
                f"{API_PRESUPUESTO}/componente/{id}",
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def crear_componente(self, nombre: str, tipo: str):
        try:
            payload = {
                "nombre": nombre,
                "tipo": tipo
            }

            resp = requests.post(
                f"{API_PRESUPUESTO}/componente",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()

        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def actualizar_componente(self, id: int, nombre: str | None = None, tipo: str | None = None):
        try:
            payload = {}

            # Solo se envía lo que venga
            if nombre is not None:
                payload["nombre"] = nombre

            if tipo is not None:
                payload["tipo"] = tipo
        
            if not payload:
                return {
                    "error": True,
                    "message": "Debe enviar al menos un campo para actualizar"
                }

            resp = requests.put(
                f"{API_PRESUPUESTO}/componente/{id}",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()

        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def eliminar_componente(self, id: int):
        try:
            resp = requests.delete(
                f"{API_PRESUPUESTO}/componente/{id}",
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
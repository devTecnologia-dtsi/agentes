import requests
from ..config_pre import API_PRESUPUESTO

class DtsiService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar DTSI.
    """

    def listar_dtsi(self):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/dtsi", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_dtsi(self, id: int):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/dtsi/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def crear_dtsi(self, id_clase: int, id_tipo: int, id_responsble: int):
        try:
            payload = {
                "id_clase": id_clase,
                "id_tipo": id_tipo,
                "id_responsble": id_responsble
            }
            resp = requests.post(
                f"{API_PRESUPUESTO}/dtsi",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def actualizar_dtsi(self, id: int, id_clase: int | None = None, id_tipo: int | None = None, id_responsble: int | None = None):
        try:
            payload = {"id": id}

            # Solo se envía lo que el usuario quiere modificar
            if id_clase is not None:
                payload["id_clase"] = id_clase

            if id_tipo is not None:
                payload["id_tipo"] = id_tipo

            if id_responsble is not None:
                payload["id_responsble"] = id_responsble

            resp = requests.put(
                f"{API_PRESUPUESTO}/dtsi/{id}",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
    
    def eliminar_dtsi(self, id: int):
        try:
            resp = requests.delete(f"{API_PRESUPUESTO}/dtsi/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
import requests
from ..config_pre import API_PRESUPUESTO

class EstadoService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar estados.
    """

    def listar_estados(self):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/estados", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_estado(self, id: int):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/estados/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
    
    def crear_estado(self, cod: str, estado:str):
        try:
            payload = {
                "cod": cod,
                "estado": estado
            }
            resp = requests.post(
                f"{API_PRESUPUESTO}/estados",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
    def actualizar_estado(self, id: int, cod: str | None = None, estado: str | None = None):
        try:
            payload = {"id": id}

            # Solo se envía lo que venga
            if cod is not None:
                payload["cod"] = cod
            
            if estado is not None:
                payload["estado"] = estado

            resp = requests.put(
                f"{API_PRESUPUESTO}/estados/{id}",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
    
    def eliminar_estado(self, id: int):
        try:
            resp = requests.delete(f"{API_PRESUPUESTO}/estados/{id}", timeout=10)
            resp.raise_for_status()
            return {"message": "Estado eliminado correctamente"}
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
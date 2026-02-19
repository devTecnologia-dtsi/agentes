import requests
from ..config_pre import API_PRESUPUESTO

class OrigenService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar orígenes.
    """

    def listar_origenes(self):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/origen", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_origen(self, id: int):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/origen/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
    def crear_origen(self, cod: str, origen:str):
        try:
            payload = {
                "cod": cod,
                "origen": origen
            }
            resp = requests.post(
                f"{API_PRESUPUESTO}/origen",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
    
    def actualizar_origen(self, id: int, cod: str | None = None, origen: str | None = None):
        try:
            payload = {"id": id}

            # Solo se envía lo que venga
            if cod is not None:
                payload["cod"] = cod
            
            if origen is not None:
                payload["origen"] = origen
            
            resp = requests.put(
                f"{API_PRESUPUESTO}/origen/{id}",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
    
    def eliminar_origen(self, id: int):
        try:
            resp = requests.delete(f"{API_PRESUPUESTO}/origen/{id}", timeout=10)
            resp.raise_for_status()
            return {"message": "Origen eliminado correctamente"}
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
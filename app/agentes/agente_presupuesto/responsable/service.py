import requests
from ..config_pre import API_PRESUPUESTO

class ResponsableService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar responsables.
    """

    def listar_responsables(self):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/responsables", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_responsable(self, id: int):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/responsables/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
    
    def crear_responsable(self, responsable: str, cargo: str, area: str, correo: str ):
        try:
            payload = {
                "responsable": responsable,
                "cargo": cargo,
                "area": area,
                "correo": correo
            }

            resp = requests.post(
                f"{API_PRESUPUESTO}/responsables",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
    def actualizar_responsable(self, id: int, responsable: str | None = None, cargo: str | None = None, area: str | None = None, correo: str | None = None):
        try:
            payload = {"id": id}

            # Solo se envía lo que venga
            if responsable is not None:
                payload["nombre"] = responsable

            if cargo is not None:
                payload["cargo"] = cargo

            if area is not None:
                payload["area"] = area

            if correo is not None:
                payload["correo"] = correo


            resp = requests.put(
                f"{API_PRESUPUESTO}/responsables/{id}",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
    def eliminar_responsable(self, id: int):
        try:
            resp = requests.delete(f"{API_PRESUPUESTO}/responsables/{id}", timeout=10)
            resp.raise_for_status()
            return {"success": True, "message": "Responsable eliminado correctamente."}
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
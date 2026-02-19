import requests
from ..config_pre import API_PRESUPUESTO

class ProveedorService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar proveedores.
    """

    def listar_proveedores(self):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/proveedor", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_proveedor(self, id: int):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/proveedor/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
    def crear_proveedor(self, nombre: str):
        try:
            payload = {
                "nombre": nombre,
            }

            resp = requests.post(
                f"{API_PRESUPUESTO}/proveedor",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
    
    def actualizar_proveedor(self, id: int, nombre: str | None = None):
        try:
            payload = {"id": id}

            # Solo se envía lo que venga
            if nombre is not None:
                payload["nombre"] = nombre

            resp = requests.put(
                f"{API_PRESUPUESTO}/proveedor/{id}",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
    
    def eliminar_proveedor(self, id: int):
        try:
            resp = requests.delete(f"{API_PRESUPUESTO}/proveedor/{id}", timeout=10)
            resp.raise_for_status()
            return {"message": "Proveedor eliminado correctamente"}
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
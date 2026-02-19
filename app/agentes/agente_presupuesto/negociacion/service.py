import requests
from datetime import date
from ..config_pre import API_PRESUPUESTO

class NegociacionService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar negociaciones.
    """

    def listar_negociaciones(self):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/negociacion", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_negociacion(self, id: int):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/negociacion/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
    
    def crear_negociacion(self, fecha_inicio: date, fecha_fin: date, id_contrato:int):
        try:
            payload = {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "id_contrato": id_contrato
            }
            resp = requests.post(
                f"{API_PRESUPUESTO}/negociacion",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
    
    def actualizar_negociacion(self, id: int, fecha_inicio: date | None = None, fecha_fin: date | None = None, id_contrato: int | None = None):
        try:
            payload = {"id": id}

            # Solo se envía lo que venga
            if fecha_inicio is not None:
                payload["fecha_inicio"] = fecha_inicio
            
            if fecha_fin is not None:
                payload["fecha_fin"] = fecha_fin

            if id_contrato is not None:
                payload["id_contrato"] = id_contrato

            resp = requests.put(
                f"{API_PRESUPUESTO}/negociacion/{id}",
                json=payload,
                timeout=10
            )

            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
    
    def eliminar_negociacion(self, id: int):
        try:
            resp = requests.delete(f"{API_PRESUPUESTO}/negociacion/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
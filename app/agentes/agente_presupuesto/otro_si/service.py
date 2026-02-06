import  requests
from datetime import date
from ..config_pre import API_PRESUPUESTO


class OtroSIService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar otros sí.
    """

    def listar_otro_si(self):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/otro_si", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_otro_si(self, id: int):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/otro_si/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
    def crear_otro_si(self, fecha_inicio: date, fecha_fin: date,id_estado:int, id_contrato:int):
        try:
            payload = {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "id_estado": id_estado,
                "id_contrato": id_contrato
            }
            resp = requests.post(
                f"{API_PRESUPUESTO}/otro_si",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
    def actualizar_otro_si(self, id: int, fecha_inicio: date | None = None, fecha_fin: date | None = None, id_estado: int | None = None, id_contrato: int | None = None):

        try:
            payload = {"id": id}

            # Solo se envía lo que venga
            if fecha_inicio is not None:
                payload["fecha_inicio"] = fecha_inicio
            
            if fecha_fin is not None:
                payload["fecha_fin"] = fecha_fin

            if id_estado is not None:
                payload["id_estado"] = id_estado
                
            if id_contrato is not None:
                payload["id_contrato"] = id_contrato
            
            resp = requests.put(
                f"{API_PRESUPUESTO}/otro_si/{id}",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
    def eliminar_otro_si(self, id: int):
        try:
            resp = requests.delete(f"{API_PRESUPUESTO}/otro_si/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
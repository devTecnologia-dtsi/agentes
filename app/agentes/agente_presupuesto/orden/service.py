import requests
from datetime import date
from decimal import Decimal
from ..config_pre import API_PRESUPUESTO

class OrdenService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar ordenes.
    """

    def listar_ordenes(self):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/orden", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_orden(self, id: int):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/orden/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
    def crear_orden(self, valor: Decimal, iva: Decimal, fecha_inicio: date, fecha_fin: date, id_presupuesto:int, id_proveedor:int):
        try:
            payload = {
                "valor": valor,
                "iva": iva,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "id_presupuesto": id_presupuesto,
                "id_proveedor": id_proveedor
            }
            resp = requests.post(
                f"{API_PRESUPUESTO}/orden",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
    
    def actualizar_orden(self, id: int, valor: Decimal | None = None, iva: Decimal | None = None, fecha_inicio: date | None = None, fecha_fin: date | None = None, id_presupuesto:int | None = None, id_proveedor:int | None = None):
        try:
            payload = {"id": id}

            # Solo se envía lo que venga
            if valor is not None:
                payload["valor"] = valor
            
            if iva is not None:
                payload["iva"] = iva
            
            if fecha_inicio is not None:
                payload["fecha_inicio"] = fecha_inicio
            
            if fecha_fin is not None:
                payload["fecha_fin"] = fecha_fin

            if id_presupuesto is not None:
                payload["id_presupuesto"] = id_presupuesto

            if id_proveedor is not None:
                payload["id_proveedor"] = id_proveedor

            resp = requests.put(
                f"{API_PRESUPUESTO}/orden/{id}",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
    def eliminar_orden(self, id: int):
        try:
            resp = requests.delete(f"{API_PRESUPUESTO}/orden/{id}", timeout=10)
            resp.raise_for_status()
            return {"message": "Negociación eliminada correctamente"}
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
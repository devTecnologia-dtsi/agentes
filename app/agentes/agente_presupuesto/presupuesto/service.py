import requests
from datetime import date
from ..config_pre import API_PRESUPUESTO

class PresupuestoService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar presupuestos.
    """

    def listar_presupuestos(self):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/presupuestos", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_presupuesto(self, id: int):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/presupuestos/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
    def crear_presupuesto(self, presupuesto: float, aprobado:float, gasto:float, anio:date, id_cuenta: int):
        try:
            payload = {
                "presupuesto": presupuesto,
                "aprobado": aprobado,
                "gasto": gasto, 
                "anio": anio,
                "id_cuenta": id_cuenta
            }
            resp = requests.post(
                f"{API_PRESUPUESTO}/presupuestos",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
    def actualizar_presupuesto(self, id: int, presupuesto: float | None = None, aprobado:float | None = None, gasto:float | None = None, anio:date | None = None, id_cuenta: int | None = None):
        try:
            payload = {"id": id}

            # Solo se envía lo que venga
            if presupuesto is not None:
                payload["presupuesto"] = presupuesto

            if aprobado is not None:
                payload["aprobado"] = aprobado

            if gasto is not None:
                payload["gasto"] = gasto

            if anio is not None:
                payload["anio"] = anio

            if id_cuenta is not None:
                payload["id_cuenta"] = id_cuenta

            resp = requests.put(
                f"{API_PRESUPUESTO}/presupuestos/{id}",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
        
    def eliminar_presupuesto(self, id: int):
        try:
            resp = requests.delete(f"{API_PRESUPUESTO}/presupuestos/{id}", timeout=10)
            resp.raise_for_status()
            return {"message": "Presupuesto eliminado correctamente"}
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
import requests
from ..config_pre import API_PRESUPUESTO

class CuentaService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar cuentas.
    """

    def listar_cuentas(self):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/cuenta", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_cuenta(self, id: int):
        try:
            resp = requests.get(f"{API_PRESUPUESTO}/cuenta/{id}", timeout=10)
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def crear_cuenta(self, numero: int, cuenta: str, id_dtsi:int, id_tipo:int, id_componente: int):
        try:
            payload = {
                "numero": numero,
                "cuenta": cuenta,
                "id_dtsi": id_dtsi,
                "id_tipo": id_tipo,
                "id_componente": id_componente
            }
            resp = requests.post(
                f"{API_PRESUPUESTO}/cuenta",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def actualizar_cuenta(self, id: int, numero: int | None = None, cuenta: str | None = None, id_dtsi:int | None = None, id_tipo:int | None = None, id_componente: int | None = None):
        try:
            payload = {"id": id}

            # Solo se envía lo que el usuario quiere modificar
            if numero is not None:
                payload["numero"] = numero
            
            if cuenta is not None:
                payload["cuenta"] = cuenta

            if id_dtsi is not None:
                payload["id_dtsi"] = id_dtsi
            
            if id_tipo is not None:
                payload["id_tipo"] = id_tipo
            
            if id_componente is not None:
                payload["id_componente"] = id_componente

            resp = requests.put(
                f"{API_PRESUPUESTO}/cuenta/{id}",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def eliminar_cuenta(self, id: int):
        try:
            resp = requests.delete(
                f"{API_PRESUPUESTO}/cuenta/{id}",
                timeout=10
            )
            resp.raise_for_status()
            return {"message": "Cuenta eliminada exitosamente."}
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
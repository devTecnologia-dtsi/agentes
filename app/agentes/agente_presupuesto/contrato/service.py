import requests
from datetime import date
from decimal import Decimal
from ..config_pre import API_PRESUPUESTO


class ContratoService:
    """
    Servicio que se comunica con la API de presupuesto
    para gestionar Contratos.
    """

    def listar_Contratos(self):
        try:
            resp = requests.get(
                f"{API_PRESUPUESTO}/contrato",
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def obtener_Contrato(self, id: int):
        try:
            resp = requests.get(
                f"{API_PRESUPUESTO}/contrato/{id}",
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def crear_Contrato(self, id_origen: int, id_proveedor: int, fecha_inicio: date, fecha_fin: date, valor_real: Decimal, negociado: Decimal):
        try:
            payload = {
                "id_origen": id_origen,
                "id_proveedor": id_proveedor,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "valor_real": valor_real,
                "negociado": negociado
            }

            resp = requests.post(
                f"{API_PRESUPUESTO}/contrato",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()

        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def actualizar_Contrato(self, id: int, id_origen: int | None = None, id_proveedor: int | None = None, fecha_inicio: date | None = None, fecha_fin: date | None = None, valor_real: Decimal | None = None, negociado: Decimal| None = None):
        try:
            payload = {}

            # Solo se envía lo que venga
            if id_origen is not None:
                payload["id_origen"] = id_origen

            if id_proveedor is not None:
                payload["id_proveedor"] = id_proveedor

            if fecha_inicio is not None:
                payload["fecha_inicio"] = fecha_inicio

            if fecha_fin is not None:
                payload["fecha_fin"] = fecha_fin

            if valor_real is not None:
                payload["valor_real"] = valor_real

            if negociado is not None:
                payload["negociado"] = negociado

            if not payload:
                return {
                    "error": True,
                    "message": "Debe enviar al menos un campo para actualizar"
                }

            resp = requests.put(
                f"{API_PRESUPUESTO}/contrato/{id}",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()

        except requests.RequestException as e:
            return {"error": True, "message": str(e)}

    def eliminar_Contrato(self, id: int):
        try:
            resp = requests.delete(
                f"{API_PRESUPUESTO}/contrato/{id}",
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"error": True, "message": str(e)}
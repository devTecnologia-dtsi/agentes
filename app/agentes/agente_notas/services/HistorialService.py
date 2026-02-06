import requests
from .config import get_historial_url
 
# Tabla de sufijos y descripciones
suffixes = {
    '84': 'Posgrado Sem Virt.2026-3',
    '69': 'Posgrado Sem Virt.2026-1',
    '55': 'Pregrado Sem Virt.2026-3',
    '44': 'Posg Presencia Cua 2026-1',
    '43': 'Preg Presencia Cua 2026-1',
    '42': 'Op Grado Dis Ene-Abr 2026',
    '41': 'Posgrado Distancia Cuat 2026-1',
    '40': 'Pregrado Distancia Cua 2026-1',
    '38': 'Pregrado Sem Virt.2026-1',
    '27': 'Posgrado Cua Virt.2026-3',
    '25': 'Posgrado Cua Virt.2026-1',
    '21': 'Posgrado Distancia 2026-1',
    '15': 'Pregrado Distancia 2026-1',
    '12': 'Formacion Trabajo 2026-1',
    '11': 'Posgrado Presencial 2026-1',
    '10': 'Pregrado Presencial 2026-1',
    '07': 'Pregrado Cua Virt.2026-3',
    '05': 'Pregrado Cua Virt.2026-1',
    '00': 'Cumplimiento plan estudios 26',
    '97': 'Posgrado Sem Virt.2025-11',
    '95': 'Posgrado Sem Virt.2025-9',
    '93': 'Posgrado Sem Virt.2025-7',
    '91': 'Posgrado Sem Virt.2025-5',
    '90': 'Educación Continua 2025',
    '86': 'Op Grado Presenci Jul-Dic 2025',
    '85': 'Op Grado Sem Ene-Jun 2025',
    '80': 'Intersemestral 2025-2 Dic-Ene',
    '71': 'Posgrado Distancia 2025-2',
    '67': 'Pregrado Sem Virt.2025-11',
    '65': 'Pregrado Distancia 2025-2',
    '64': 'Pregrado Sem Virt.2025-9',
    '62': 'Formación Trabajo 2025-2',
    '61': 'Posgrado Presencial 2025-2',
    '60': 'Pregrado Presencial 2025-2',
}
 
class HistorialService:
 
    def fetch_historial(self, id_estudiante: str):
        try:
            resp = requests.get(
                get_historial_url(),
                params={"V_ID": id_estudiante},
                timeout=60
            )
 
            if resp.status_code != 200:
                return {"error": True, "message": f"No se pudo obtener el historial. Status: {resp.status_code}, Response: {resp.text}"}
 
            try:
                data = resp.json()
            except ValueError:
                return {"error": True, "message": "La API devolvió un JSON inválido."}
 
            if isinstance(data, list):
                return {"error": False, "historial": data}
 
            return {"error": False, "historial": data.get("historial", [])}
 
        except (requests.RequestException, ValueError) as e:
            return {"error": True, "message": f"Error interno: {e}"}
 
 
    def obtener_historial(self, id_estudiante: str):
        response = self.fetch_historial(id_estudiante)
 
        if response.get("error"):
            return response
 
        historial_raw = response.get("historial", [])
        historial_limpio = []
 
        for curso in historial_raw:
            term_code = curso.get("V_TERM_CODE", "")
 
            # Últimos dos dígitos = sufijo del período
            suffix = term_code[-2:] if len(term_code) >= 2 else ""
 
            # Descripción del período desde la tabla de sufijos
            periodo_desc = suffixes.get(suffix, "Periodo no identificado")
 
            historial_limpio.append({
                "codigo": curso.get("V_CRN"),
                "materia": curso.get("V_CRSE_TITLE"),
                "periodo": periodo_desc,
                "nota": curso.get("V_GRDE_CODE_MID"),
                "termCode": term_code
            })
 
        return {
            "error": False,
            "historial": historial_limpio
        }
 
    def obtener_historial_por_nota(self, id_estudiante: str, nota_buscada: str = None, operador: str = "=="):
        """
        Obtiene el historial filtrado por nota específica o rango.
       
        Parámetros:
            id_estudiante: ID del estudiante
            nota_buscada: Nota a buscar (ej: "5.0", "4", "3")
            operador: Tipo de comparación: "==" (exacta), "<", ">", "<=", ">=" (default: "==")
       
        Retorna: Historial con solo los cursos que cumplen la condición
       
        Ejemplos:
            - obtener_historial_por_nota(id, "5", "==") → materias con nota exacta 5
            - obtener_historial_por_nota(id, "3", "<") → materias con nota menor a 3
            - obtener_historial_por_nota(id, "4", ">=") → materias con nota mayor o igual a 4
        """
        response = self.obtener_historial(id_estudiante)
       
        if response.get("error"):
            return response
       
        if not nota_buscada:
            return response
       
        historial_completo = response.get("historial", [])
        historial_filtrado = []
       
        try:
            nota_valor = float(nota_buscada)
        except (ValueError, TypeError):
            return {
                "error": True,
                "message": f"La nota '{nota_buscada}' no es un valor numérico válido",
                "historial": []
            }
       
        for curso in historial_completo:
            nota_curso = curso.get("nota")
            if not nota_curso:
                continue
           
            try:
                nota_curso_valor = float(nota_curso)
            except (ValueError, TypeError):
                continue
           
            # Aplicar la comparación según el operador
            cumple = False
            if operador == "==":
                cumple = abs(nota_curso_valor - nota_valor) < 0.001  # Comparación con tolerancia
            elif operador == "<":
                cumple = nota_curso_valor < nota_valor
            elif operador == ">":
                cumple = nota_curso_valor > nota_valor
            elif operador == "<=":
                cumple = nota_curso_valor <= nota_valor
            elif operador == ">=":
                cumple = nota_curso_valor >= nota_valor
            else:
                return {
                    "error": True,
                    "message": f"Operador '{operador}' no válido. Use: ==, <, >, <=, >=",
                    "historial": []
                }
           
            if cumple:
                historial_filtrado.append(curso)
       
        return {
            "error": False,
            "historial": historial_filtrado,
            "nota_buscada": nota_buscada,
            "operador": operador,
            "total_encontrados": len(historial_filtrado)
        }
 
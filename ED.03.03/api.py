"""Cliente del DataMart de la evaluación."""
from urllib.parse import urlparse
import requests

DIAS = ("Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo")

def consultar(base):
    url = urlparse(base)
    if url.scheme not in ("http", "https") or not url.hostname or url.username or url.password:
        raise ValueError("Configura una URL HTTP o HTTPS válida para el DataMart.")
    respuesta = requests.get(base.rstrip("/") + "/resultados", timeout=(3, 8))
    respuesta.raise_for_status()
    filas = respuesta.json()
    if not isinstance(filas, list):
        raise ValueError("La API debe devolver una lista de resultados.")
    claves = set()
    for fila in filas:
        if not isinstance(fila, dict):
            raise ValueError("La API devolvió una fila inválida.")
        metodo = fila.get("metodo_pago")
        dia = fila.get("dia_semana")
        unidades = fila.get("unidades")
        if (not isinstance(metodo, str) or not metodo.strip()
                or dia not in DIAS or type(unidades) is not int or unidades < 0):
            raise ValueError("La respuesta contiene un método, día o conteo inválido.")
        clave = (metodo, dia)
        if clave in claves:
            raise ValueError("La API devolvió grupos duplicados.")
        claves.add(clave)
    return filas

"""Serie FIX publicada por el portal web del SIE de Banco de México."""
import pandas as pd
import requests

URL_PUBLICA = ("https://www.banxico.org.mx/SieInternet/consultaSerieGrafica.do"
               "?s=SF43718,CF102,3&versionSerie=LA-MAS-RECIENTE&l=es")

def consultar_fix(inicio, fin):
    respuesta = requests.get(URL_PUBLICA, timeout=(5, 20))
    respuesta.raise_for_status()
    datos = respuesta.json()
    if datos.get("serie") != "SF43718" or not isinstance(datos.get("valores"), list):
        raise ValueError("El portal del SIE devolvió un formato inesperado.")
    df = pd.DataFrame(datos["valores"], columns=["Fecha", "Valor"])
    df["Fecha"] = pd.to_datetime(df["Fecha"], format="%Y-%m-%d")
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
    df = df.loc[df.Fecha.between(pd.Timestamp(inicio), pd.Timestamp(fin))].copy()
    df["Clave"] = "SF43718"
    df["Serie"] = datos["titulo"]
    df["Anio"] = df.Fecha.dt.year
    df["Mes"] = df.Fecha.dt.month
    return df, {"SF43718": int(df.Valor.isna().sum())}

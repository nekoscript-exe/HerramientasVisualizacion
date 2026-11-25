"""Ventas agregadas por día de la semana y medio de pago."""
from os import getenv

import altair as alt
import pandas as pd
import requests
import streamlit as st

from api import DIAS, consultar

st.set_page_config(page_title="Ventas por medio de pago", layout="wide")
st.title("Ventas por medio de pago")
st.caption("DataMart de la evaluación · Unidades acumuladas por día de la semana")

base = getenv("DATAMART_API_URL", "http://127.0.0.1:9001")
if st.sidebar.button("Actualizar datos"):
    st.session_state.pop("filas_datamart", None)
try:
    if "filas_datamart" not in st.session_state:
        st.session_state.filas_datamart = consultar(base)
    filas = st.session_state.filas_datamart
except requests.RequestException:
    st.error("Sin conexión con el DataMart. Verifica el servicio y pulsa Actualizar datos.")
    st.stop()
except ValueError as exc:
    st.error(str(exc))
    st.stop()

st.sidebar.success("Datos recibidos del DataMart")
st.sidebar.caption("GET /resultados · Pulsa Actualizar datos para volver a consultar")
if not filas:
    st.info("La API respondió sin registros.")
    st.stop()

datos = pd.DataFrame(filas, columns=["metodo_pago", "dia_semana", "unidades"])
metodos = sorted(datos["metodo_pago"].unique())
dias_disponibles = [d for d in DIAS if d in set(datos["dia_semana"])]
elegidos = st.sidebar.multiselect("Métodos de pago", metodos, default=metodos)
dias = st.sidebar.multiselect("Días de la semana", dias_disponibles, default=dias_disponibles)
muestra = datos[datos.metodo_pago.isin(elegidos) & datos.dia_semana.isin(dias)]
if muestra.empty:
    st.info("No hay resultados con estos filtros.")
    st.stop()

totales = muestra.groupby("metodo_pago")["unidades"].sum()
lideres = " · ".join(totales.index[totales.eq(totales.max())])
indicadores = st.columns(3)
indicadores[0].metric("Unidades", f"{muestra.unidades.sum():,}")
indicadores[1].metric("Grupos día × pago", len(muestra))
indicadores[2].metric("Mayor volumen", lideres)

st.subheader("Volumen por día y método")
st.caption("Cada barra corresponde a un agregado de la API. Pasa el cursor para ver el valor exacto.")
grafico = alt.Chart(muestra).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
    x=alt.X("dia_semana:N", sort=list(DIAS), title="Día", axis=alt.Axis(labelAngle=0)),
    xOffset=alt.XOffset("metodo_pago:N", sort=metodos),
    y=alt.Y("unidades:Q", title="Unidades", axis=alt.Axis(format="~s")),
    color=alt.Color("metodo_pago:N", sort=metodos, title="Pago",
                    scale=alt.Scale(scheme="tableau10")),
    tooltip=[alt.Tooltip("dia_semana:N", title="Día"),
             alt.Tooltip("metodo_pago:N", title="Pago"),
             alt.Tooltip("unidades:Q", title="Unidades", format=",")],
).properties(height=330)
st.altair_chart(grafico, width="stretch")

with st.expander("Ver tabla y descargar CSV"):
    tabla = muestra.assign(orden=muestra.dia_semana.map({d:i for i,d in enumerate(DIAS)}))
    tabla = tabla.sort_values(["orden", "metodo_pago"]).drop(columns="orden")
    st.dataframe(tabla.rename(columns={"metodo_pago":"Método", "dia_semana":"Día",
                                       "unidades":"Unidades"}), hide_index=True)
    st.download_button("Descargar CSV", tabla.to_csv(index=False), "ventas_filtradas.csv")

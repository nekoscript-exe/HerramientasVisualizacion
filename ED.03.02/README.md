# ED.03.02 · Tablero de Banco de México

La copia parte de [BOWadapter/HerramientasVisualizacion](https://github.com/BOWadapter/HerramientasVisualizacion/tree/1be2c58519955f032a1ca116e3b5844e8fd45b8b). El original se llama `dashboard_banxico.py`.

## Antes y después

Retiré **Promedio por mes y año**. La celda de color resume cada mes con un promedio, pero no muestra cuánto varió la serie dentro del mes. La nueva gráfica **Rango y mediana por mes** muestra mínimo y máximo diarios como banda y la mediana como línea. El cursor permite leer las tres cifras y el número de observaciones. Cada estadístico usa valores válidos del rango seleccionado. Los meses sin datos quedan fuera. Conservé tendencia, comparación en base 100, cambios de cierre, distribución anual y tabla con descarga.

## Ejecutar

Desde la raíz de la rama `ed-03-02`, con Python 3.14:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r ED.03.02/requirements.txt
cd ED.03.02
../.venv/bin/streamlit run dashboard_banxico.py --server.address 127.0.0.1 --server.port 8508
```

El modo **Portal público · FIX** consulta al [SIE público](https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CF102&locale=es) para obtener la serie `SF43718`. El control de fechas funciona en ese modo. Para consultar otras series selecciona **API REST del SIE** y configura localmente `BANXICO_TOKEN` o crea `ED.03.02/.streamlit/secrets.toml` a partir de la plantilla. El archivo de secretos está ignorado por Git. En Lifelya se reutilizó el entorno Python de ED.03.03.

Para abrir la aplicación original, ejecuta `streamlit run dashboard_banxico.py` desde la raíz del repositorio. Requiere un token. Para reproducir el **antes** con la misma serie pública y los gráficos originales, genera el archivo local con `python ED.03.02/preparar_original.py` y ejecuta `streamlit run ED.03.02/original_comparacion.local.py --server.port 8507` desde la raíz con el entorno activado. Esa copia temporal está ignorada por Git.

Desde la raíz, ejecuta `python -m unittest discover -s ED.03.02 -v` con el entorno activado.

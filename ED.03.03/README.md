# ED.03.03 · Ventas por medio de pago

El tablero lee agregados de unidades por método de pago y día de la semana de la API FastAPI de [la evaluación P2](https://github.com/nekoscript-exe/examen-p2-125054864). Usa `GET /resultados` (JSON con `metodo_pago`, `dia_semana` y `unidades`). `GET /salud` confirma la conexión a PostgreSQL y `GET /resultados/{clave}` permite verificar un método. Los GET utilizados en Lifelya funcionan sin autenticación. El tablero solo lee datos.

## Ejecución

Con Python 3.14, desde la raíz del repositorio:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r ED.03.03/requirements.txt
curl -fsS http://127.0.0.1:9001/salud
.venv/bin/streamlit run ED.03.03/app.py --server.address 127.0.0.1 --server.port 8505
```

Abre http://127.0.0.1:8505. Cambia los filtros de método y día para actualizar los indicadores, gráfico y CSV. Pulsa **Actualizar datos** para hacer una nueva consulta.

Si la API está detenida, sigue el README del repositorio de la evaluación para iniciar su Compose y poblar la base con el pipeline original. En Lifelya ya estaba disponible en 9001. Si la evaluación publica otro puerto, exporta `DATAMART_API_URL` con su URL base antes de iniciar Streamlit. `.env.example` documenta esa variable.

Con la API de Lifelya activa, ejecuta `.venv/bin/python -m unittest discover -s ED.03.03 -v`.

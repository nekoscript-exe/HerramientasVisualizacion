import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import Mock, patch

import requests
from streamlit.testing.v1 import AppTest

from api import consultar

URL = "http://127.0.0.1:9001"
APP = Path(__file__).with_name("app.py")

class Dashboard(unittest.TestCase):
    def test_api_real(self):
        filas = consultar(URL)
        control = requests.get(URL + "/resultados/Tarjeta", timeout=5)
        control.raise_for_status()
        self.assertEqual([r for r in filas if r["metodo_pago"] == "Tarjeta"], control.json())

    def test_filtros_grafica_y_metricas(self):
        filas = consultar(URL)
        app = AppTest.from_file(APP).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, f"{sum(r['unidades'] for r in filas):,}")
        self.assertEqual(len(app.dataframe[0].value), len(filas))
        self.assertEqual(len(app.get("vega_lite_chart")), 1)
        app.multiselect[0].set_value(["Tarjeta"]).run()
        esperadas = Counter({r["dia_semana"]:r["unidades"] for r in filas
                             if r["metodo_pago"] == "Tarjeta"})
        self.assertEqual(app.metric[0].value, f"{sum(esperadas.values()):,}")
        app.multiselect[1].set_value(["Lunes"]).run()
        self.assertEqual(app.metric[0].value, f"{esperadas['Lunes']:,}")
        self.assertEqual(len(app.dataframe[0].value), 1)
        app.multiselect[0].set_value([]).run()
        self.assertIn("estos filtros", app.info[0].value)

    @patch("api.requests.get")
    def test_api_vacia(self, get):
        get.return_value = Mock()
        get.return_value.json.return_value = []
        app = AppTest.from_file(APP).run()
        self.assertIn("sin registros", app.info[0].value)

    @patch("api.requests.get", side_effect=requests.ConnectionError)
    def test_fallo_red(self, _):
        app = AppTest.from_file(APP).run()
        self.assertIn("Sin conexión", app.error[0].value)
        self.assertFalse(app.exception)

    @patch("api.requests.get")
    def test_formato_invalido(self, get):
        get.return_value.json.return_value = {"error":"estructura inválida"}
        with self.assertRaisesRegex(ValueError, "lista"):
            consultar(URL)

import statistics
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from analisis import rango_mensual
from fuente_publica import consultar_fix

RAIZ = Path(__file__).parent

class Banxico(unittest.TestCase):
    def test_datos_publicos_y_agregacion(self):
        df, _ = consultar_fix("2024-01-01", "2024-03-31")
        self.assertTrue((df["Clave"] == "SF43718").all())
        mensual = rango_mensual(df)
        self.assertEqual(len(mensual), 3)
        for fecha, fila in mensual.iterrows():
            valores = df.loc[df.Fecha.dt.month.eq(fecha.month), "Valor"].dropna().tolist()
            self.assertEqual(list(fila), [min(valores), statistics.median(valores),
                                          max(valores), len(valores)])

    def test_aplicacion_modificada(self):
        with patch.dict("os.environ", {"BANXICO_TOKEN": ""}):
            app = AppTest.from_file(RAIZ/"dashboard_banxico.py", default_timeout=25).run()
        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        self.assertIn("Rango y mediana por mes", [e.value for e in app.subheader])
        self.assertNotIn("Promedio por mes y año", [e.value for e in app.subheader])
        self.assertEqual(len(app.get("vega_lite_chart")), 1)
        self.assertTrue({"La serie y su tendencia", "Cambio de un mes a otro",
                         "Qué tan movido estuvo cada año"}.issubset(
                             {e.value for e in app.subheader}))
        app.radio[0].set_value("API REST del SIE").run()
        self.assertIn("BANXICO_TOKEN", app.info[0].value)

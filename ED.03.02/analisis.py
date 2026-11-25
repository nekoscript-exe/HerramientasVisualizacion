"""Resumen mensual de las observaciones diarias."""
def rango_mensual(principal):
    diario = principal.sort_values("Fecha").set_index("Fecha")["Valor"]
    return (diario.resample("MS").agg(["min", "median", "max", "count"])
            .rename(columns={"min":"Mínimo", "median":"Mediana",
                             "max":"Máximo", "count":"Observaciones"})
            .query("Observaciones > 0"))

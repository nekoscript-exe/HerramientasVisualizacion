"""Genera una copia comparativa con gráficos intactos y la serie oficial pública."""
from pathlib import Path

raiz = Path(__file__).resolve().parent
original = (raiz.parent / "dashboard_banxico.py").read_text(encoding="utf-8")
original = original.replace("import streamlit as st", "import streamlit as st\nfrom fuente_publica import consultar_fix")
inicio = original.index("TOKEN = leer_token()")
fin = original.index("@st.cache_data", inicio)
original = original[:inicio] + 'TOKEN = None\n\n' + original[fin:]
original = original.replace("consultar(tuple(claves), str(inicio), str(fin), TOKEN)",
                            "consultar_fix(inicio, fin)")
original = original.replace('st.title("Tablero de series del SIE")',
                            'st.title("Tablero de series del SIE")\n'
                            'st.info("Diseño original · Comparación con la serie pública FIX")')
destino = raiz / "original_comparacion.local.py"
destino.write_text(original, encoding="utf-8")
print(destino)

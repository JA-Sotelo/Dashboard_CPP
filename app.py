"""
Streamlit generator — PAP & Biopsias Dashboard
Procesa un Excel con pandas, inyecta los datos en index.html y entrega
un HTML autocontenido listo para distribuir.
"""

import json
import re
import streamlit as st
import pandas as pd
from pathlib import Path

# ── CONFIG ──────────────────────────────────────────────────────────────────
TEMPLATE_PATH = Path(__file__).parent / "index.html"
MO_MAP = {1:"Ene",2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",
          7:"Jul",8:"Ago",9:"Sep",10:"Oct",11:"Nov",12:"Dic"}

# ── HELPERS ──────────────────────────────────────────────────────────────────
def clean(v) -> str:
    """Elimina NaN/None/nat que pandas convierte a string."""
    if v is None:
        return ""
    s = str(v).strip()
    if s.lower() in ("nan", "none", "nat", ""):
        return ""
    return s

def to_float(v) -> float:
    try:
        if pd.isna(v):
            return 0.0
    except Exception:
        pass
    try:
        return float(str(v).replace(",", "."))
    except Exception:
        return 0.0

def normalizar_col(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFD", str(s))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower().replace(" ", "").replace("_", "")


# ── PROCESAMIENTO EXCEL ──────────────────────────────────────────────────────
def procesar_excel(archivo) -> list[dict]:
    df = pd.read_excel(archivo, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]

    # Detectar columna de fecha (primera que matchea patrones)
    col_fecha = None
    for c in df.columns:
        n = normalizar_col(c)
        if any(p in n for p in ["fecha", "date", "fec", "ingreso"]):
            col_fecha = c
            break

    rows = []
    for _, row in df.iterrows():
        obj = {}
        for col in df.columns:
            obj[col] = clean(row[col])

        # Campo FECHA tipado + campos calculados
        if col_fecha and obj.get(col_fecha):
            try:
                dt = pd.to_datetime(obj[col_fecha], dayfirst=True, errors="coerce")
                if pd.notna(dt):
                    obj[col_fecha] = dt.strftime("%Y-%m-%d")
                    obj["__PERIODO__"] = f"{MO_MAP[dt.month]}-{str(dt.year)[2:]}"
                    obj["__ANIO__"]    = str(dt.year)
                else:
                    obj["__PERIODO__"] = ""
                    obj["__ANIO__"]    = ""
            except Exception:
                obj["__PERIODO__"] = ""
                obj["__ANIO__"]    = ""
        else:
            obj["__PERIODO__"] = ""
            obj["__ANIO__"]    = ""

        rows.append(obj)

    return rows


# ── GENERACIÓN HTML ──────────────────────────────────────────────────────────
def generar_html(rows: list[dict], password: str, filename: str) -> str:
    if not TEMPLATE_PATH.exists():
        st.error(f"No se encontró {TEMPLATE_PATH}. Asegurate de que index.html esté en la misma carpeta que app.py.")
        st.stop()

    html_base = TEMPLATE_PATH.read_text(encoding="utf-8")

    # Serializar con ensure_ascii=True — OBLIGATORIO para evitar SyntaxError JS
    json_data = json.dumps(rows, ensure_ascii=True, separators=(",", ":"))

    # 1 ── Inyectar datos en RAW
    html_base = html_base.replace(
        "let RAW = [], COLS = [], CHARTS = {}, PAGE = 1;",
        f"let RAW = {json_data}, COLS = [], CHARTS = {{}}, PAGE = 1;"
    )

    # 2 ── Cambiar contraseña
    html_base = html_base.replace(
        "const DASHBOARD_PASSWORD = 'pap2025';",
        f"const DASHBOARD_PASSWORD = {json.dumps(password)};"
    )

    # 3 ── Conectar initDashboard() al cierre del login
    #      Reemplaza el timeout del overlay para que llame a initDashboard()
    html_base = html_base.replace(
        "setTimeout(() => { overlay.style.display = 'none'; }, 460);",
        "setTimeout(() => { overlay.style.display = 'none'; initDashboard(); }, 460);"
    )

    # 4 ── Inyectar badge de origen en el statusText inicial
    html_base = html_base.replace(
        "Sin datos · cargá un archivo para comenzar",
        f"Datos de: {filename}"
    )

    return html_base


# ── STREAMLIT UI ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Generador Dashboard PAP & Biopsias",
    page_icon="🧬",
    layout="centered"
)

st.title("🧬 Generador Dashboard PAP & Biopsias")
st.markdown(
    "Subí tu archivo Excel, configurá la contraseña y descargá el HTML listo para distribuir."
)

with st.form("config"):
    archivo = st.file_uploader(
        "Archivo Excel (.xlsx / .xls)",
        type=["xlsx", "xls"],
        help="Todos los datos se procesan localmente, no se suben a ningún servidor externo."
    )
    password = st.text_input(
        "Contraseña del dashboard",
        value="pap2025",
        type="password",
        help="Los usuarios finales deberán ingresar esta contraseña para ver el dashboard."
    )
    submitted = st.form_submit_button("⚡ Generar HTML", type="primary")

if submitted:
    if not archivo:
        st.warning("Por favor seleccioná un archivo Excel.")
        st.stop()
    if not password:
        st.warning("La contraseña no puede estar vacía.")
        st.stop()

    with st.spinner("Procesando datos y generando HTML…"):
        try:
            rows = procesar_excel(archivo)
            html_out = generar_html(rows, password, archivo.name)

            st.success(
                f"✅ Dashboard generado con **{len(rows):,} registros** "
                f"desde `{archivo.name}`."
            )

            st.download_button(
                label="⬇️ Descargar dashboard.html",
                data=html_out.encode("utf-8"),
                file_name="dashboard.html",
                mime="text/html",
                use_container_width=True
            )

            with st.expander("Vista previa de datos (primeras 5 filas)"):
                st.json(rows[:5])

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
            st.exception(e)

st.divider()
st.caption("Dashboard Anatomía Patológica · app.py para Streamlit Cloud")

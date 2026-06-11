# Dashboard PAP & Biopsias

Dashboard interactivo de Anatomía Patológica para visualizar y analizar protocolos de PAP y Biopsias. Funciona como un único archivo HTML autocontenido que puede abrirse directamente en el navegador **o** generarse con datos pre-cargados mediante el generador Streamlit.

---

## Estructura del proyecto

```
.
├── index.html        # Dashboard completo (HTML + JS autocontenido)
├── app.py            # Generador Streamlit — procesa Excel e inyecta datos
├── requirements.txt  # Dependencias Python
├── logo 4.jpg        # Logo embebido en el dashboard (base64)
└── README.md
```

---

## Funcionalidades

| Función | Detalle |
|---|---|
| **Login con contraseña** | Overlay con máx. 5 intentos y bloqueo de 30 s. Contraseña configurable en `const DASHBOARD_PASSWORD` |
| **Carga de archivos** | Drag & drop o selector — `.xlsx`, `.xls`, `.csv` |
| **Detección de columnas** | Auto-mapea fecha, material, diagnóstico, procedencia, médico, sexo, estudio, período, año |
| **Segmentadores** | Dropdowns con checkboxes: Año · Período (mmm-aa) · Estudio · Sexo · Procedencia |
| **KPIs** | Total protocolos · PAP · Biopsias |
| **Gráficos interactivos** | 10 gráficos con cross-filtering entre secciones (Material, Diagnóstico, Procedencia, Médicos) |
| **Cross-filter** | Click en un gráfico filtra las demás secciones; badge con `✕` para limpiar |
| **Toggle tema** | Modo oscuro / claro con botón en el header |
| **Tabla de detalle** | Paginada, búsqueda libre, exportación a CSV |
| **Logo** | Embebido en base64 — funciona sin conexión y sin archivos externos |

---

## Uso directo (sin servidor)

Abrí `index.html` directamente en cualquier navegador moderno (Chrome, Edge, Firefox).
No requiere instalación ni conexión a internet: todas las dependencias se cargan por CDN y el logo está embebido.

**Contraseña por defecto:** `pap2025`
Para cambiarla, editá la línea en `index.html`:
```js
const DASHBOARD_PASSWORD = 'pap2025'; // ← cambiar aquí
```

---

## Generador Streamlit

El `app.py` permite a usuarios finales subir su propio Excel y descargar un `dashboard.html` con los datos ya embebidos — listo para distribuir como un único archivo.

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Ejecutar

```bash
streamlit run app.py
```

Abrí el navegador en `http://localhost:8501`.

### Flujo del generador

```
Usuario sube Excel
       ↓
pandas procesa con dtype=str + clean() elimina 'nan'/'none'
       ↓
Calcula PERIODO y ANIO desde columna de fecha detectada automáticamente
       ↓
json.dumps(ensure_ascii=True) — evita SyntaxError JS con caracteres latinos
       ↓
Inyecta en index.html:
  • let RAW = [...datos...]
  • DASHBOARD_PASSWORD = "contraseña elegida"
  • initDashboard() conectado al cierre del login
       ↓
Botón de descarga → dashboard.html autocontenido
```

### Deploy en Streamlit Cloud

1. Subí este repositorio a GitHub
2. En [share.streamlit.io](https://share.streamlit.io) → New app → seleccioná `app.py`
3. Listo — los usuarios acceden por URL, suben su Excel y descargan su dashboard

---

## Gráficos y cross-filtering

Cada sección tiene gráficos interactivos entre sí:

| Sección | Gráficos |
|---|---|
| **Material** | Línea de tiempo · Barras · Anillo |
| **Diagnóstico** | Línea de tiempo · Barras · Anillo |
| **Procedencia** | Anillo · Barras |
| **Médicos** | Anillo · Barras |

**Cómo funciona el cross-filter:**
- Click en un segmento/barra → filtra las demás secciones para mostrar solo los registros de esa categoría
- Un badge aparece junto al título de la sección activa — hacé click en `✕` para limpiar
- Segundo click en el mismo elemento → deselecciona
- "Limpiar todo" en los segmentadores resetea también todos los cross-filters

---

## Columnas detectadas automáticamente

| Columna | Palabras clave detectadas |
|---|---|
| Fecha | `fecha`, `date`, `fec`, `ingreso` |
| Material | `material`, `tipo`, `mat` |
| Diagnóstico | `diagnostico`, `diag`, `resultado`, `dx` |
| Procedencia | `procedencia`, `origen`, `servicio` |
| Médico | `medico`, `doctor`, `solicitante` |
| Sexo | `sexo`, `genero` |
| Estudio | `estudio`, `tipoestudio` |
| Período | `periodo`, `mes` |
| Año | `anio`, `año`, `year` |

---

## Dependencias frontend (CDN)

| Librería | Versión | Uso |
|---|---|---|
| [Tailwind CSS](https://tailwindcss.com) | latest | Estilos y diseño responsive |
| [Chart.js](https://www.chartjs.org) | 4.4.0 | Gráficos interactivos |
| [chartjs-adapter-date-fns](https://github.com/chartjs/chartjs-adapter-date-fns) | 3.0.0 | Eje de tiempo en gráficos de línea |
| [SheetJS / xlsx](https://sheetjs.com) | 0.18.5 | Lectura de archivos Excel y CSV |

> El dashboard no sube ningún dato a servidores externos. Todo el procesamiento ocurre en el navegador del usuario.

---

## Licencia

MIT — libre para uso personal y comercial.

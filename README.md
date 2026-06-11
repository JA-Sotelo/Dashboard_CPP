# Dashboard PAP & Biopsias

Dashboard interactivo de Anatomía Patológica para visualizar y analizar protocolos de PAP y Biopsias.

Funciona de dos maneras:
- **Uso directo** — abrís `index.html` en el navegador, arrastrás tu Excel y el dashboard se arma al instante, sin servidor ni instalación.
- **Generador Streamlit** — `app.py` procesa el Excel con Python, inyecta los datos en el HTML y genera un único archivo `dashboard.html` listo para distribuir o publicar.

---

## Estructura del proyecto

```
.
├── index.html        # Dashboard completo (HTML + JS autocontenido)
├── app.py            # Generador Streamlit con HTML embebido en base64
├── requirements.txt  # Dependencias Python
└── README.md
```

> El logo de la empresa está embebido en base64 dentro de `index.html` — no hace falta incluirlo en el repositorio.

---

## Funcionalidades

| Función | Detalle |
|---|---|
| **Login con contraseña** | Overlay con máx. 5 intentos y bloqueo de 30 s |
| **Carga de archivos** | Drag & drop o selector — `.xlsx`, `.xls`, `.csv` |
| **Detección automática de columnas** | Auto-mapea fecha, material, diagnóstico, procedencia, médico, sexo, estudio, período, año |
| **Filtros en sidebar lateral** | Panel fijo a la izquierda — los dropdowns no tapan los gráficos |
| **Segmentadores** | Dropdowns con checkboxes — Año · Período · Estudio · Sexo · Procedencia |
| **KPIs** | Total protocolos · PAP · Biopsias |
| **10 gráficos interactivos** | Líneas de tiempo, barras y anillos en 4 secciones |
| **Cross-filtering** | Click en cualquier gráfico filtra las demás secciones; badge `✕` para limpiar |
| **Toggle tema** | Modo oscuro / claro con paleta basada en el logo institucional |
| **Tabla de detalle** | Paginada, búsqueda libre, exportación a CSV |

---

## Uso directo (sin servidor)

1. Descargá `index.html`
2. Abrilo en Chrome, Edge o Firefox
3. Ingresá la contraseña (`pap2025` por defecto)
4. Arrastrá tu archivo Excel

No requiere instalación ni conexión a internet. Todas las librerías se cargan desde CDN y el logo está embebido en el propio HTML.

**Cambiar la contraseña:** editá esta línea en `index.html`:
```js
const DASHBOARD_PASSWORD = 'pap2025';
```

---

## Generador Streamlit

`app.py` permite a cualquier usuario subir su Excel desde el navegador y descargarse un `dashboard.html` con los datos ya cargados.

### Instalación local

```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
streamlit run app.py
```

Abrí `http://localhost:8501` en el navegador.

### Deploy en Streamlit Cloud

1. Subí este repositorio a GitHub (solo necesitás `app.py` y `requirements.txt`)
2. Ingresá a [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Seleccioná el repo y apuntá a `app.py`
4. Deployá — el HTML está embebido en `app.py`, no hace falta commitear `index.html`

### Flujo del generador

```
Usuario sube Excel (.xlsx / .xls)
        ↓
pandas lee con dtype=str → clean() elimina valores 'nan'/'none' de pandas
        ↓
Detecta columna de fecha → calcula PERIODO (ej. "Mar-25") y ANIO
        ↓
json.dumps con ensure_ascii=True → evita errores JS con caracteres latinos
        ↓
Inyecta en el template HTML:
  · let RAW = [...datos...]
  · DASHBOARD_PASSWORD = "contraseña configurada"
  · initDashboard() conectado al cierre del login
        ↓
Botón de descarga → dashboard.html autocontenido
```

---

## Cross-filtering entre gráficos

Cada sección (Material, Diagnóstico, Procedencia, Médicos) tiene sus propios gráficos interactivos. Al hacer click en un elemento:

- Las **demás secciones** se filtran para mostrar solo los registros asociados a esa selección
- La **sección propia** mantiene su vista completa con el elemento seleccionado resaltado
- Aparece un **badge** junto al título — click en `✕` para limpiar ese filtro
- Segundo click en el mismo elemento → deselecciona
- **"Limpiar filtros"** en el sidebar resetea también todos los cross-filters

| Sección | Gráficos |
|---|---|
| **Material** | Línea de tiempo · Barras · Anillo |
| **Diagnóstico** | Línea de tiempo · Barras · Anillo |
| **Procedencia** | Anillo · Barras |
| **Médicos** | Anillo · Barras |

---

## Columnas detectadas automáticamente

| Columna lógica | Palabras clave en el encabezado del Excel |
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

La detección es insensible a mayúsculas, tildes y espacios.

---

## Dependencias

### Python (generador)

| Paquete | Uso |
|---|---|
| `streamlit` | Interfaz web del generador |
| `pandas` | Procesamiento del Excel |
| `openpyxl` | Lectura de archivos `.xlsx` |
| `xlrd` | Lectura de archivos `.xls` legacy |

### Frontend (CDN — sin instalación)

| Librería | Uso |
|---|---|
| [Tailwind CSS](https://tailwindcss.com) | Estilos y diseño responsive |
| [Chart.js 4.4](https://www.chartjs.org) | Gráficos interactivos |
| [chartjs-adapter-date-fns](https://github.com/chartjs/chartjs-adapter-date-fns) | Eje de tiempo en gráficos de línea |
| [SheetJS / xlsx](https://sheetjs.com) | Lectura de Excel y CSV en el navegador |

> Ningún dato sale del navegador del usuario. El procesamiento del Excel es 100 % local (tanto en el modo directo como en el generador Streamlit).

---

## Licencia

MIT — libre para uso personal y comercial.

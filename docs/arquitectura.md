# Arquitectura del proyecto

## Estructura de archivos

```
reporter-ia-atom-3.0/
├── index.html          ← toda la aplicación en un solo archivo
├── README.md
└── docs/
    ├── arquitectura.md         (este archivo)
    ├── estandar-reportes.md
    ├── asistente-ia.md
    └── configuracion-metricas.md
```

---

## Estructura interna de index.html

El archivo está organizado en 5 bloques en orden:

```
<head>
  styles CSS (inline)
</head>
<body>
  1. NAV        — barra superior fija
  2. SIDEBAR    — navegación lateral fija
  3. PANELS     — doc panels y chat panel (posición fixed)
  4. MAIN WRAP  — contenido de cada página (display:none / active)
  5. SCRIPT     — datos, lógica y funciones de render
</body>
```

---

## Sistema de datos

Todos los datos son sintéticos y generados en el bloque `<script>` al cargar la página.

### RNG determinístico

```js
let seed = 42;
function ri(min, max) { /* LCG seeded */ }   // random int
function pick(arr) { /* pick random element */ }
```

El seed fijo garantiza que los datos sean siempre los mismos, lo que hace que la demo sea reproducible.

### Conjuntos de datos

| Variable | Registros | Descripción |
|---|---|---|
| `DATA` | 200 | Conversaciones del período actual (mes base) |
| `PREV` | 160 | Conversaciones del período anterior (para deltas) |
| `DB.conversations` | — | Alias de DATA en algunos contextos |
| `DB.contacts` | — | Contactos únicos derivados de DATA |
| `DB.agent_interactions` | — | Interacciones de agentes |
| `DB.agent_status` | — | Historial de estados de agentes |
| `DB.agent_calls` | — | Llamadas realizadas |
| `DB.smarton_calls` | — | Llamadas del agente de voz |
| `DB.campaigns` | — | Campañas masivas |
| `DB.billing` | — | Datos de facturación |
| `DB.paid_ads_meta` | — | Anuncios y métricas de Meta |
| `DB.paid_ads_google` | — | Anuncios de Google |
| `DB.paid_ads_web` | — | Tráfico web |
| `DB.contact_custom_fields` | — | Campos custom por contacto |

### Estructura de cada registro (`DATA`/`PREV`)

```js
{
  id: string,
  fecha: Date,
  origen: 'inbound organico' | 'click to wa' | 'campañas' | 'webhooks' | 'plantillas individuales',
  bot: 'Flujo Financiamiento' | 'Flujo Tasación' | 'Flujo Soporte',
  botTipif: string | null,       // tipificación del bot (si aplica)
  escalado: boolean,             // si fue escalada a un agente
  grupo: string | null,          // grupo de agentes asignado
  agentTipif: string | null,     // tipificación del agente
  maxStage: 'stage_1' | ... | 'stage_4',
  respSecs: number | null,       // segundos hasta primera respuesta del agente
  // campos custom automotrices:
  marca_auto: string,
  modelo_auto: string,
  tipo_financiamiento: string,
  patente: string | null,
  presupuesto_usd: number | null,
  anio_vehiculo: number | null,
  pais: string
}
```

---

## Sistema de navegación

### Páginas principales

Cada reporte es un `<div class="page" id="page-{nombre}">`. Solo uno tiene la clase `active` a la vez.

```js
function goTo(id, btn, group, name) {
  // oculta todas las .page
  // muestra page-{id}
  // actualiza el nav breadcrumb
  // actualiza el botón activo del sidebar
}
```

### Sub-tabs (Pauta inbound)

La página de pauta tiene tabs internos (stab-meta, stab-google, stab-web):

```js
function goToPautaTab(tabId, navBtn, group, name) {
  goTo('pauta', navBtn, group, name);
  showStab(tabId, tabBtn);
  // actualiza título y descripción del header dinámicamente
}
```

El objeto `PAUTA_TAB_INFO` contiene título y descripción de cada sub-tab:

```js
const PAUTA_TAB_INFO = {
  'stab-meta':   { title: 'Click to WA · Meta',   desc: '...' },
  'stab-google': { title: 'Click to WA · Google', desc: '...' },
  'stab-web':    { title: 'Tráfico web',           desc: '...' }
};
```

### Tabs internos de tablas

```js
function showTab(tabId, btn)   // tabs dentro de un card (ej: Por origen / Por flujo)
function showStab(stabId, btn) // sub-tabs de páginas completas (ej: Pauta)
```

---

## Sistema de render

Cada reporte tiene su propio conjunto de funciones de render:

```js
// Conversaciones
function render() {
  renderKPIs();
  renderDaily();
  renderFunnel();
  renderTipif();
  renderTableOrigen();
  renderTableBot();
  renderTableGrupo();
}

// Contactos
function renderContactos() { ... }

// Pauta Meta
function renderMetaCtwa() { ... }
```

Las funciones leen el array `filtered` (subconjunto de `DATA` según los filtros activos) y regeneran los DOM/charts.

### Patrón de charts (Chart.js)

Antes de crear un chart nuevo, siempre destruir el anterior:

```js
function dc(id) {
  if (charts[id]) { charts[id].destroy(); delete charts[id]; }
}

// Uso:
dc('daily');
charts['daily'] = new Chart(document.getElementById('chart-daily'), { ... });
```

---

## Sistema de filtros

Cada reporte mantiene su propio estado de período y filtros en variables globales:

```js
// Conversaciones
let period = 30;      // días del período activo
let filtered = [];    // subconjunto de DATA según filtros

function applyFilters() {
  // lee los selects del filter-bar
  // recalcula filtered
  // llama render()
}

function resetFilters() { ... }
```

---

## Constantes automotrices

```js
const BOTS    = ['Flujo Financiamiento', 'Flujo Tasación', 'Flujo Soporte'];
const GRUPOS  = ['Equipo Ventas', 'Equipo Financiamiento', 'Equipo Soporte'];
const ORIGENES = ['inbound organico', 'click to wa', 'campañas', 'webhooks', 'plantillas individuales'];
const AGENT_TIPIFS = ['venta', 'sin respuesta', 'reagendar', 'no califica', 'pendiente docs'];
const COLORS  = ['#E8590C', '#2E7D32', '#1565C0', '#6A1B9A', '#E65100'];
```

---

## Variables CSS clave

```css
:root {
  --orange: #E8590C;       /* color principal */
  --orange-light: #FFF3EC;
  --green: #2E7D32;
  --blue: #1565C0;
  --sidebar-w: 236px;
  --nav-h: 52px;
  --radius: 10px;
}
```

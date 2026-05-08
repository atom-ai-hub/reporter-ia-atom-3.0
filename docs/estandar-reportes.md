# Estándar base de reportes

Todo reporte activo (con datos reales) debe implementar esta estructura de forma obligatoria y en este orden. No omitir ninguna sección.

---

## Estructura HTML completa

```html
<div class="page" id="page-{nombre}">

  <!-- 1. HEADER -->
  <div class="page-header">
    <div class="ph-row">
      <div class="ph-left">
        <div class="page-title">{Nombre igual al item del sidebar}</div>
        <div class="page-updated">Última actualización de datos: <span>hoy 9:30 AM</span></div>
      </div>
      <div class="ph-right page-desc">{Descripción detallada del reporte}</div>
    </div>
  </div>

  <!-- 2. SEARCH BAR + DOC BUTTON -->
  <div class="ai-search-wrap">
    <div class="ai-search-inner">
      <input class="ai-search-input" id="ai-search-{nombre}"
        type="text"
        placeholder="Pregunta lo que quieras sobre {nombre en minúsculas}..."
        onkeydown="if(event.key==='Enter')sendFromSearch('ai-search-{nombre}')">
      <button class="ai-search-submit" onclick="sendFromSearch('ai-search-{nombre}')">↑</button>
    </div>
    <button class="ai-search-doc-btn" onclick="toggleDocPanel('doc-{nombre}')">
      📖 Ver documentación del reporte
    </button>
  </div>

  <!-- 3. FILTER BAR -->
  <div class="filter-bar">
    <span class="filter-label">Período</span><div class="filter-divider"></div>
    <div class="preset-group">
      <button class="preset-btn" onclick="set{Nombre}Period(7,this)">7d</button>
      <button class="preset-btn active" onclick="set{Nombre}Period(30,this)">30d</button>
      <button class="preset-btn" onclick="set{Nombre}Period(90,this)">90d</button>
    </div>
    <div class="filter-divider"></div>
    <span class="filter-label">Filtros</span><div class="filter-divider"></div>
    <!-- selects contextuales del reporte -->
    <button class="reset-btn" onclick="reset{Nombre}Filters()">Limpiar</button>
    <button class="apply-btn" onclick="apply{Nombre}Filters()">Aplicar</button>
  </div>

  <!-- 4. KPIs -->
  <div class="sh"><span class="sh-title">KPIs principales</span><div class="sh-line"></div></div>
  <div class="kpi-grid" id="{nombre}-kpi-grid"></div>

  <!-- 5. GRÁFICO PRINCIPAL (ancho completo) -->
  <div class="sh"><span class="sh-title">{Título del gráfico principal}</span><div class="sh-line"></div></div>
  <div class="card" style="margin-bottom:14px">
    <div class="legend">...</div>
    <div style="position:relative;width:100%;height:240px">
      <canvas id="chart-{nombre}-daily"></canvas>
    </div>
  </div>

  <!-- 6. GRÁFICOS SECUNDARIOS (split 50/50) -->
  <div class="g2" style="margin-bottom:14px">
    <div class="card"><!-- gráfico izquierdo --></div>
    <div class="card"><!-- gráfico derecho --></div>
  </div>

  <!-- 7. TABLA DE PERFORMANCE -->
  <div class="sh" style="margin-top:1.5rem">
    <span class="sh-title">Performance detallado</span><div class="sh-line"></div>
  </div>
  <div class="card">
    <div class="tabs">
      <button class="tab-btn active" onclick="showTab('tab-{a}',this)">Agrupación A</button>
      <button class="tab-btn" onclick="showTab('tab-{b}',this)">Agrupación B</button>
    </div>
    <div class="tab-panel active" id="tab-{a}">
      <div class="table-wrap"><table>
        <thead><tr>
          <th>{Dimensión}</th>
          <th>Cantidad</th>
          <th>% Total</th>  <!-- OBLIGATORIO en todas las tablas -->
          <!-- resto de columnas métricas -->
        </tr></thead>
        <tbody id="tbody-{a}"></tbody>
      </table></div>
    </div>
  </div>

</div>
```

---

## Reglas del header

| Campo | Regla |
|---|---|
| `page-title` | **Debe coincidir exactamente** con el texto del item del sidebar. Sin subtítulos ni variaciones. |
| `page-updated` | Siempre visible, siempre con formato "hoy HH:MM AM/PM". En producción, leer el timestamp real de la última ejecución del SP. |
| `page-desc` | Descripción en prosa de 1-2 líneas. Mencionar qué mide el reporte, la unidad de análisis y el contexto de comparación. |

---

## Reglas de KPIs

```js
// Estructura de cada KPI
{
  label: string,          // nombre del KPI
  tip: string,            // texto del tooltip (?)
  val: string,            // valor formateado (ej: "108 (54%)")
  delta: number,          // diferencia vs período anterior (número puro)
  sfx: string,            // sufijo del delta (ej: 'pp' para puntos porcentuales)
  g: boolean,             // true = verde cuando sube, false = rojo cuando sube (lowerBetter)
}
```

- Siempre mostrar delta vs período anterior con flecha ↑↓
- Para métricas de volumen (ventas, asignadas): mostrar `valor (% del total)` entre paréntesis en gris
- Usar `lowerBetter: true` para métricas como tiempo de respuesta o costo por conversión

---

## Reglas de gráfico principal

- **Ancho completo** (no en columnas, directamente en `.card` sin grid)
- **Altura mínima: 240px**
- Solo dos series como máximo: volumen principal + conversión/venta
- Conversaciones → barras naranjas (`rgba(232,89,12,0.75)`)
- Ventas/conversión → línea verde con puntos (`#2E7D32`, `pointRadius:4`)
- **Sin período anterior** en el gráfico principal

---

## Reglas de gráficos secundarios

- Layout **50/50** con clase `.g2`
- Izquierda: funnel o embudo de conversión
- Derecha: distribución de tipificaciones u otra dimensión categórica
- El funnel debe ser **HTML** (no canvas) con `.fh-row` para poder mostrar cantidad + tasa de caída dentro de cada barra
- Las tipificaciones siempre ordenadas de **mayor a menor**

---

## Reglas de tablas

- Siempre incluir columna `% Total` después de la columna de cantidad principal
- El `% Total` se calcula sobre el total de `filtered` (el universo actual con filtros aplicados)
- La columna `% Total` va en gris (`color:var(--gray-500)`) para que sea discreta
- Sin barras de progreso en las celdas, solo el porcentaje en texto
- Siempre ofrecer al menos 2 tabs de agrupación diferente

---

## Doc panel obligatorio

Cada reporte activo necesita su doc panel con este ID y estructura:

```html
<!-- fuera del main-wrap, junto a los demás panels -->
<div class="doc-overlay" id="doc-{nombre}-overlay" onclick="toggleDocPanel('doc-{nombre}')"></div>
<div class="doc-panel" id="doc-{nombre}-panel">
  <div class="doc-ph">
    <div>
      <div class="doc-ph-title">📖 Documentación del reporte</div>
      <div class="doc-ph-sub">{Nombre} · referencia rápida</div>
    </div>
    <button class="doc-close" onclick="toggleDocPanel('doc-{nombre}')">✕</button>
  </div>
  <div class="doc-body">

    <!-- SECCIÓN 1: Descripción (obligatoria) -->
    <div class="doc-sec">
      <div class="doc-sec-title">Descripción del reporte</div>
      <div class="doc-sec-body">
        <!-- Explicar la UNIDAD ÚNICA del reporte. Ejemplos:
             - Conversaciones: "cada conversación empieza con el primer mensaje y termina con una tipificación"
             - Contactos: "un contacto único = un número de teléfono"
             - Pauta Meta: "cada registro = una conversación originada desde un anuncio de Meta"
        -->
      </div>
    </div>

    <!-- SECCIÓN 2: KPIs (uno por .doc-item) -->
    <div class="doc-sec">
      <div class="doc-sec-title">KPIs principales</div>
      <div class="doc-item">
        <div class="doc-item-name">{Nombre del KPI}</div>
        <div class="doc-item-desc">{Qué mide, cómo se calcula, a qué subconjunto aplica}</div>
      </div>
      <!-- repetir por cada KPI -->
    </div>

    <!-- SECCIÓN 3: Gráficos (uno por .doc-item) -->
    <div class="doc-sec">
      <div class="doc-sec-title">Gráficos</div>
      <!-- ... -->
    </div>

    <!-- SECCIÓN 4: Tabla de performance (uno por tab) -->
    <div class="doc-sec">
      <div class="doc-sec-title">Tabla de performance</div>
      <!-- ... -->
    </div>

    <!-- SECCIÓN 5: Filtros (uno por .doc-item) -->
    <div class="doc-sec">
      <div class="doc-sec-title">Filtros</div>
      <!-- ... -->
    </div>

  </div>
</div>
```

---

## Checklist para activar un reporte nuevo

Al convertir un reporte de `nav-soon` a activo:

- [ ] Quitar clase `nav-soon` del botón del sidebar
- [ ] Reemplazar el bloque `coming-soon` con el HTML del reporte siguiendo este estándar
- [ ] Implementar funciones: `render{Nombre}()`, `set{Nombre}Period()`, `apply{Nombre}Filters()`, `reset{Nombre}Filters()`
- [ ] Agregar el doc panel con las 5 secciones completas
- [ ] Verificar que el título coincide con el sidebar
- [ ] Verificar que `% Total` aparece en todas las tablas
- [ ] Agregar el reporte a la sección "Activos" del README

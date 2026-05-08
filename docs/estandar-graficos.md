# Estándar de diseño de gráficos

Prácticas acordadas para todos los reportes activos. Aplicar siempre al crear o modificar gráficos.

---

## Gráfico principal diario (barras + línea)

### Estructura
- Barras naranjas: volumen principal (`rgba(232,89,12,0.62)`, `borderRadius:3`)
- Línea verde con puntos: conversión/venta (`#2E7D32`, `borderWidth:2`, `tension:.35`)
- **Línea siempre al frente** de las barras: `order:1` en línea, `order:2` en barras
- **Puntos pequeños** en la línea: `pointRadius` array — valor 3 en puntos clave, 0 en el resto
- **Sin período anterior** en el gráfico principal

### Eje X — fechas reales
- Siempre mostrar fechas reales en formato `"abr 9"`, `"may 8"` (no números de día)
- El rango va desde `hoy - N días` hasta `hoy` (usar constante `TODAY_DEMO` para demo)
- Máximo **45 días** de rango; si el filtro pide más, truncar y aclararlo en el título
- `maxTicksLimit`: máximo 12 ticks visibles

### Labels en puntos clave
Mostrar el valor numérico encima del punto, usando un plugin inline `afterDatasetsDraw`:
- Puntos clave: máximo global, mínimo global (no-cero), primer día, último día, e intermedios equidistantes (~cada N/4 días)
- Label de conversaciones: arriba del bar correspondiente, color `rgba(180,60,0,0.85)`, 10px
- Label de ventas: arriba del punto de la línea, color `#2E7D32`, 10px
- `ctx.font = '500 10px "DM Sans",sans-serif'`

### Título del card
- Incluir siempre `card-title` dentro del card
- Si hay límite de días, agregar nota discreta: `<span style="font-size:10px;color:var(--gray-300)">máx. 45 días</span>`
- Leyenda al lado derecho del título (no abajo)
- **Sin `card-sub`** (descripción debajo del título) — el título es suficiente

---

## Gráficos de barras horizontales (tipificaciones, distribuciones)

### Colores
Usar paleta suave con transparencia (~0.55 alpha), NO los COLORS[] vibrantes:
```js
const SOFT_COLORS = [
  'rgba(232,89,12,0.55)',
  'rgba(46,125,50,0.55)',
  'rgba(21,101,192,0.55)',
  'rgba(106,27,154,0.55)',
  'rgba(230,81,0,0.55)'
];
```

### Labels inline
Mostrar `valor  %` directamente sobre las barras mediante plugin `afterDatasetsDraw`:
- Si la barra tiene espacio (ancho > 72px): label dentro, blanco `rgba(255,255,255,0.92)`, alineado a la izquierda desde `bar.base + 10`
- Si la barra es corta: label afuera a la derecha, gris `#555`, desde `bar.x + 6`
- Para barras horizontales: `bar.x` = borde derecho, `bar.base` = borde izquierdo (cero), ancho real = `bar.x - bar.base`

### Etiquetas Y
- **Sin sufijos de rol** como "(de agente)", "(de bot)": el contexto lo da el título del card
- Siempre ordenadas de mayor a menor

### Títulos
- Solo `card-title`, **sin `card-sub`**
- Agregar `margin-top:12px` al canvas después del título

---

## Gráficos de embudo (funnel HTML)

- Implementar como **HTML** (no canvas): clase `.fh-row`, `.fh-bar`, `.fh-drop`
- Dentro de cada barra: valor absoluto + porcentaje del total
- A la derecha de cada barra: tasa de caída respecto a la etapa anterior (`▼ N%`)
- Ancho de barra proporcional al valor vs el máximo (mínimo 8% para visibilidad)
- Último step (venta/conversión): color verde `#2E7D32`
- **Sin `card-sub`**, solo `card-title`

---

## Filter bar

Orden estándar de elementos:
1. `<span class="filter-label">Filtros</span><div class="filter-divider"></div>` — siempre primero
2. Date picker (`.dp-wrap`) con quick options + rango personalizado
3. `<div class="filter-divider"></div>`
4. Selects de filtro contextual
5. Botón **Limpiar** (reset-btn)
6. Botón **Aplicar** (apply-btn) — siempre `margin-left:auto` para quedar a la derecha

---

## Reglas generales

- Todos los plugins de charts se definen **inline** en el array `plugins:[]` del chart (no registrar globalmente salvo necesidad)
- Nunca usar `card-sub` en gráficos — el título debe ser autoexplicativo
- Tooltips: siempre `mode:'index', intersect:false` en charts de serie temporal para mostrar todos los valores al hovear
- Escalas Y: siempre `beginAtZero:true`, grid `rgba(0,0,0,0.04)`
- Escala X temporal: grid oculto (`display:false`)

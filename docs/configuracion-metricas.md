# Configuración de métricas

Las métricas clave del dashboard son configurables desde la página **⚙ Configuración** del sidebar, sin necesidad de tocar el código.

---

## El objeto CONFIG

```js
const CONFIG = {
  sla_target_min: 3,          // objetivo de SLA en minutos
  stages: [                   // etapas del funnel (editables)
    { id: 'stage_1', name: 'Awareness' },
    { id: 'stage_2', name: 'Lead' },
    { id: 'stage_3', name: 'MQL' },
    { id: 'stage_4', name: 'SQL' }
  ],
  calificado_stage: 'stage_3',  // cuál etapa = "Calificado" (para % calificados en Contactos)
  conversion: {
    type: 'typification',       // 'typification' | 'stage'
    values: ['venta']           // tipificaciones o etapas que cuentan como conversión
  }
};
```

Cuando el usuario modifica algo en la UI de Configuración y presiona **Aplicar**, se ejecuta `applyConfig()`:

```js
function applyConfig() {
  // lee todos los inputs de la página de Configuración
  // actualiza el objeto CONFIG
  // llama render() para recalcular todos los KPIs y gráficos
}
```

---

## SLA de primera respuesta

### Definición

El SLA mide el tiempo entre que el contacto escribe el primer mensaje y el agente responde por primera vez. Solo aplica a conversaciones que fueron **escaladas y asignadas** a un agente.

### Configuración

```js
CONFIG.sla_target_min = 3; // objetivo en minutos
```

En la UI: input numérico en la página de Configuración.

### Cálculo

```js
function withinSLA(d) {
  if (!d.escalado || !d.respSecs) return null;
  return d.respSecs <= CONFIG.sla_target_min * 60;
}
```

Retorna `true` (dentro del objetivo), `false` (fuera), o `null` (no aplica).

### Dónde afecta

- KPI "Cumplimiento SLA" en Conversaciones
- Columna "% SLA" en las tablas de performance (Por origen, Por grupo)
- Columna "SLA OK" en tabla Por grupo de agentes

---

## Etapas del funnel

### Definición

El funnel tiene 4 etapas configurables que representan el progreso de una conversación desde el contacto inicial hasta la venta.

### Configuración

```js
CONFIG.stages = [
  { id: 'stage_1', name: 'Awareness' },
  { id: 'stage_2', name: 'Lead' },
  { id: 'stage_3', name: 'MQL' },
  { id: 'stage_4', name: 'SQL' }
];
```

En la UI: 4 inputs de texto, uno por etapa.

### Cómo se asigna una etapa a una conversación

Cada conversación tiene un campo `maxStage` que indica la etapa más avanzada que alcanzó:

```js
record.maxStage = pick(['stage_1','stage_2','stage_3','stage_4']);
```

En producción, este campo vendría de los eventos de cambio de etapa en el CRM.

### Dónde afecta

- Gráfico "Funnel de conversión" en Conversaciones
- Filtro "Todas las etapas" en el filter bar
- KPI "% Calificados" en Contactos (usa `CONFIG.calificado_stage`)
- Tabla "Campos completados" en Contactos (columna Calificado)

---

## Métrica de conversión

### Definición

Una "conversión" (venta) se puede definir de dos formas distintas:

| Tipo | Descripción |
|---|---|
| `typification` | Cuenta como venta toda conversación donde el agente asignó una de las tipificaciones configuradas (ej: "venta") |
| `stage` | Cuenta como venta toda conversación que alcanzó una de las etapas configuradas del funnel |

### Configuración

```js
// Por tipificación (default)
CONFIG.conversion = {
  type: 'typification',
  values: ['venta']            // tipificaciones que = conversión
};

// Por etapa
CONFIG.conversion = {
  type: 'stage',
  values: ['stage_4']          // etapas que = conversión
};
```

En la UI: radio buttons (tipificación / etapa) + checkboxes con los valores disponibles.

### Función de evaluación

```js
function isConversion(d, conv) {
  const c = conv || CONFIG.conversion;
  if (c.type === 'typification') return c.values.includes(d.agentTipif);
  if (c.type === 'stage') return c.values.includes(d.maxStage);
  return false;
}
```

### Dónde afecta

- KPI "Ventas cerradas" en Conversaciones
- KPI "Tasa de conversión" en Conversaciones
- Línea de ventas en el gráfico diario
- Embudo (etapa final "Venta")
- Columna "Ventas" y "% Conv." en todas las tablas de performance
- KPIs de conversión en Pauta inbound

---

## Etapa "Calificado" (Contactos)

### Definición

En el reporte de Contactos, un contacto se considera "calificado" cuando alcanzó la etapa configurada como `calificado_stage`.

### Configuración

```js
CONFIG.calificado_stage = 'stage_3'; // etapa que = calificado
```

En la UI: selector desplegable con las etapas del funnel.

### Dónde afecta

- KPI "% Calificados" en Contactos
- Columna "Calificado" en la tabla de análisis de campos custom

---

## Página de Configuración (UI)

La página `page-config` renderiza la UI de configuración con `renderConfigPage()`:

```js
function renderConfigPage() {
  // Lee CONFIG y rellena los inputs
  // Al presionar Aplicar → applyConfig()
}

function applyConfig() {
  // Lee los valores actuales de la UI
  CONFIG.sla_target_min = parseInt(document.getElementById('cfg-sla').value);
  // ... resto de campos
  render();           // recalcula Conversaciones
  renderContactos();  // recalcula Contactos (si aplica)
}
```

### Inputs disponibles

| Input ID | Campo | Tipo |
|---|---|---|
| `cfg-sla` | `sla_target_min` | Número |
| `cfg-stage-1` ... `cfg-stage-4` | `stages[].name` | Texto |
| `cfg-calificado` | `calificado_stage` | Select |
| `cfg-conv-type` | `conversion.type` | Radio |
| `cfg-conv-values` | `conversion.values` | Checkboxes |

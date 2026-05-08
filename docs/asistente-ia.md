# Asistente IA

El dashboard tiene dos componentes de IA distintos pero relacionados: el **buscador por reporte** y el **chat panel global**.

---

## 1. Buscador por reporte (search bar)

Cada reporte activo tiene su propio search bar en el header:

```html
<div class="ai-search-wrap">
  <div class="ai-search-inner">
    <input id="ai-search-{nombre}" placeholder="Pregunta lo que quieras sobre {nombre}...">
    <button onclick="sendFromSearch('ai-search-{nombre}')">↑</button>
  </div>
  <button onclick="toggleDocPanel('doc-{nombre}')">📖 Ver documentación del reporte</button>
</div>
```

### Flujo actual (simulado)

```
Usuario escribe en el buscador
        ↓
sendFromSearch('ai-search-{nombre}')
        ↓
Abre el chat panel global
        ↓
Envía la pregunta al chat como si el usuario la hubiera escrito
        ↓
sendChat() → respuesta simulada con timeout
```

La función `sendFromSearch`:

```js
function sendFromSearch(inputId) {
  const inp = document.getElementById(inputId);
  const q = inp.value.trim();
  if (!q) return;
  inp.value = '';
  // abre el chat panel
  document.getElementById('chat-panel').classList.add('open');
  document.getElementById('chat-overlay').classList.add('open');
  // inyecta la pregunta y dispara el chat
  document.getElementById('chat-input').value = q;
  sendChat();
}
```

### Integración futura con LLM real

En producción, `sendChat()` deberá hacer un `fetch()` a un endpoint que:
1. Reciba la pregunta + el contexto del reporte activo (nombre del reporte, filtros aplicados, período)
2. Consulte la base de conocimiento correspondiente (ver sección 3)
3. Devuelva una respuesta en lenguaje natural con los datos reales

---

## 2. Chat panel global

El chat panel es un panel lateral derecho accesible desde cualquier página.

### Estructura HTML

```html
<div class="chat-overlay" id="chat-overlay" onclick="toggleChat()"></div>
<div class="chat-panel" id="chat-panel">
  <div class="chat-header">...</div>
  <div class="chat-messages" id="chat-messages">
    <!-- mensajes se agregan dinámicamente -->
  </div>
  <div class="chat-input-wrap">
    <input id="chat-input" onkeydown="if(event.key==='Enter')sendChat()">
    <button onclick="sendChat()">↑</button>
  </div>
</div>
```

### Comportamiento actual (mock)

```js
function sendChat() {
  const q = input.value.trim();
  // 1. Agrega el mensaje del usuario al DOM
  // 2. Muestra animación de "escribiendo..."
  // 3. Después de 1.2s, reemplaza con una respuesta hardcodeada aleatoria
  // 4. Scroll al último mensaje
}
```

Las respuestas actuales son genéricas y no consultan los datos reales. Son una simulación visual del flujo.

### Sugerencias rápidas (chips)

El mensaje inicial del bot incluye chips de sugerencias:

```js
const suggestions = [
  '¿Cuántas ventas hubo este mes?',
  '¿Qué campaña convierte mejor?',
  '¿Cuál es la tasa de asignación?',
  '¿Qué flujo genera más leads?'
];
```

Al hacer click en un chip, llama `askSuggestion(btn)` que inyecta el texto en el input y dispara `sendChat()`.

---

## 3. Base de conocimiento por reporte (doc panels)

Cada reporte activo tiene su propio **doc panel** que funciona como base de conocimiento estructurada. Este panel sirve dos propósitos:

1. **Para el usuario**: documentación accesible en el momento en que analiza el reporte
2. **Para la IA (futuro)**: contexto inyectable en el prompt del LLM para que las respuestas sean precisas sobre ese reporte específico

### Cómo abrir un doc panel

```js
function toggleDocPanel(id) {
  document.getElementById(id + '-panel').classList.toggle('open');
  document.getElementById(id + '-overlay').classList.toggle('open');
}

// Ejemplos:
toggleDocPanel('doc')            // panel de Conversaciones
toggleDocPanel('doc-contactos')  // panel de Contactos
toggleDocPanel('doc-meta')       // panel de Click to WA · Meta
```

### Estructura del doc panel (5 secciones)

Cada doc panel tiene 5 secciones fijas que representan todo lo que un analista (o un LLM) necesita para interpretar el reporte:

| Sección | Contenido |
|---|---|
| **Descripción del reporte** | Unidad única de análisis, ciclo de vida del dato, qué incluye y qué excluye |
| **KPIs principales** | Nombre, definición, fórmula de cálculo y subconjunto al que aplica |
| **Gráficos** | Qué muestra cada gráfico, qué representan los colores/ejes |
| **Tabla de performance** | Qué agrupación hace cada tab, qué significa cada columna |
| **Filtros** | Qué filtra cada selector, cómo afecta el universo de datos |

### Uso futuro como contexto de LLM

En la integración con LLM real, el doc panel de cada reporte se usará como system prompt contextual:

```js
// Pseudocódigo de integración futura
async function sendChat() {
  const activeReport = getCurrentActiveReport(); // ej: 'conversaciones'
  const docContent = extractDocPanelContent(activeReport); // texto del doc panel
  const filtersState = getCurrentFilters(); // filtros activos
  
  const response = await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
      question: userQuestion,
      context: {
        report: activeReport,
        documentation: docContent,  // ← base de conocimiento
        filters: filtersState,
        period: currentPeriod
      }
    })
  });
}
```

---

## 4. Panel de documentación vs. chat: diferencias

| | Chat panel | Doc panel |
|---|---|---|
| Propósito | Responder preguntas sobre datos | Explicar cómo funciona el reporte |
| Trigger | Botón "Preguntá lo que quieras" o search bar | Botón "Ver documentación del reporte" |
| Contenido | Dinámico (respuestas del LLM) | Estático (documentación del reporte) |
| Scope | Global (aplica a cualquier reporte) | Específico por reporte |
| ID | `#chat-panel` | `#doc-{nombre}-panel` |

---

## 5. Extensión a nuevos reportes

Al activar un reporte nuevo:

1. Crear el doc panel con las 5 secciones (ver [estándar de reportes](estandar-reportes.md))
2. Agregar el search bar al header del reporte con el `inputId` correcto
3. Las sugerencias del chat inicial pueden actualizarse para que sean contextuales al reporte activo (mejora futura)

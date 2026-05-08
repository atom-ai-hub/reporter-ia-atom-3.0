# Reporter IA · Atom 3.0

Dashboard de analytics de WhatsApp para empresas automotrices de financiamiento. Construido como una aplicación de un solo archivo HTML, sin dependencias de servidor ni base de datos. Diseñado para iterar rápido y compartir demos sin infraestructura.

🔗 **[Ver demo en vivo](https://atom-ai-hub.github.io/reporter-ia-atom-3.0)**

---

## ¿Qué es esto?

Reporter IA Atom 3.0 es un mockup de dashboard interactivo que simula el producto final de reportería de Atom. Está pensado para:

- Validar ideas de UI/UX con stakeholders antes de conectar datos reales
- Demostrar el valor del producto a clientes potenciales
- Definir el estándar visual y funcional de cada reporte antes de desarrollarlo en producción

Todos los datos son **sintéticos y determinísticos** (generados con seed fijo), por lo que la demo siempre muestra los mismos números independientemente de cuándo se abra.

---

## Reportes disponibles

### ✅ Activos (con datos)

| Reporte | Ruta | Descripción |
|---|---|---|
| Conversaciones | `/` → sidebar: Conversaciones | Volumen, funnel, tipificaciones, SLA y performance por origen/flujo/grupo |
| Contactos | sidebar: Contactos | Base de contactos únicos, completitud de campos, segmentación |
| Click to WA · Meta | sidebar: Click to WA · Meta | ROI de pauta de Facebook/Instagram: conversaciones, costo, embudo y performance por anuncio |

### 🔜 En construcción

| Reporte | Grupo |
|---|---|
| Flujos | Automatizaciones |
| Smarton de voz | Automatizaciones |
| Rendimiento de agentes | Asesores |
| Llamadas de agentes | Asesores |
| Estatus de agentes | Asesores |
| Rendimiento de campañas | Campañas outbound |
| Click to WA · Google | Pauta inbound |
| Tráfico web | Pauta inbound |
| Facturación | Negocio |

---

## Stack técnico

- **HTML + CSS + JS vanilla** — sin frameworks, sin build step
- **Chart.js 4.4.1** — gráficos de barras, líneas y donut
- **Google Fonts** — DM Sans + DM Mono
- **Un solo archivo** — `index.html` autocontenido, se puede abrir directo en el browser

---

## Cómo correr localmente

```bash
# Opción 1: abrir directo
open index.html

# Opción 2: servidor local (evita problemas de CORS en algunos browsers)
python3 -m http.server 3000
# luego abrir http://localhost:3000
```

---

## Documentación técnica

| Documento | Descripción |
|---|---|
| [Arquitectura](docs/arquitectura.md) | Estructura interna del archivo, sistema de datos y navegación |
| [Estándar de reportes](docs/estandar-reportes.md) | Template base obligatorio para todos los reportes activos |
| [Asistente IA](docs/asistente-ia.md) | Cómo funciona el chat, documentación por reporte y base de conocimiento |
| [Configuración de métricas](docs/configuracion-metricas.md) | Objeto CONFIG, etapas del funnel, conversión y SLA |

---

## Contexto de negocio

Los reportes están diseñados para una empresa automotriz de financiamiento. Los campos custom relevantes son:

- `marca_auto`, `modelo_auto`, `anio_vehiculo`
- `tipo_financiamiento`, `presupuesto_usd`, `patente`

Los flujos automatizados son: **Flujo Financiamiento**, **Flujo Tasación**, **Flujo Soporte**.

---

## Roadmap

- [ ] Conectar datos reales desde BigQuery vía atom_brain
- [ ] Integrar LLM real en el asistente IA (reemplazar simulación)
- [ ] Activar reportes de Asesores (rendimiento, llamadas, estatus)
- [ ] Activar reporte de Campañas outbound
- [ ] Activar pauta Google y Tráfico web
- [ ] Agregar exportación a PDF/CSV por reporte
- [ ] Multi-tenant: selector de empresa en el header

# ⚡ Sistema de Enfoque

**Dashboard personal de alto rendimiento.**  
Un terminal de control para atletas del conocimiento: trackeá deep work, visualizá tu consistencia en 30 días y mantené el rumbo hacia tus metas financieras — todo con una estética naval + oro que convierte datos en logros.

---

## ✦ Features

| Feature | Descripción |
|---|---|
| **Hero del día** | Banner central con progreso diario, racha de días consecutivos y estado de cada hábito. |
| **Check-in rápido** | Toggle de hábitos con feedback visual inmediato (border-top gold = completado). |
| **Matriz de consistencia** | Heatmap 30+ días con escala navy→gold. Cada celda es un hábito completado. |
| **Donuts semanales** | 7 anillos de progreso. Hoy es más grande (spotlight effect). Colores por rango de cumplimiento. |
| **Racha (streak)** | Cálculo automático de días consecutivos con todos los hábitos completados. |
| **Tracker financiero** | Línea diaria de urgencia: cuánto necesitás generar por día para llegar a tu meta. |
| **Sidebar de gestión** | Agregá nuevos hábitos sin recargar la página. |

---

## ✦ Tech Stack

- **Python** 3.14
- **Streamlit** 1.58 — interfaz reactiva sin HTML/JS manual
- **SQLite** — base de datos local, zero config
- **Plotly** 6.8 — heatmaps, donuts, gráficos interactivos
- **Pandas** 3.0 — manipulación de datos
- **Google Fonts** — DM Sans (tipografía general) + JetBrains Mono (números y métricas)

---

## ✦ Design System

### Paleta Navy + Gold

```
Fondos       → #0D1B2A (navy profundo) · #1A2D45 (surface) · #243B55 (raised)
Bordes       → #1E3050 (sep) · #8B6914 (goldDim)
Tipografía   → #F0E6CC (texto) · #9BA8B5 (muted)
Acento       → #C9A84C (gold) · #E8C97A (goldLight)
Estados      → #E07070 (danger) · #4A1A2D (dangerBg)
```

El oro reemplaza al verde como color de «éxito»: en este contexto representa valor generado, no solo finalización.

### Tipografía

- **DM Sans** — títulos, cuerpo, botones (sans-serif moderna, legible)
- **JetBrains Mono** — porcentajes, métricas, montos, fechas (monospace técnica)

### Componentes visuales

| Componente | Firma visual |
|---|---|
| Hero card | Fondo degradado, borde izquierdo gold 3px, progreso 3x grande |
| Habit card | Border-top 3px: gold (completado), goldLight (progreso), gris (pendiente) |
| Botón primario | Fondo navyLight, borde goldDim, hover con glow gold |
| Donut | Hoy 140px, resto 90px, color por rango, porcentaje centrado |
| Heatmap | Escala navy→gold, gap 4px, eje X arriba, 45° |

---

## ✦ Roadmap

### Fase 1 · MVP actual ✅

- [x] Check-in diario con toggle
- [x] Matriz de consistencia (heatmap)
- [x] Donuts de consistencia semanal
- [x] Racha de días consecutivos
- [x] Tracker financiero (metas)
- [x] Diseño Navy + Gold
- [x] Sidebar de gestión de hábitos

### Fase 2 · Próximo lanzamiento 🚧

- [ ] Exportación de datos a PDF / CSV
- [ ] Múltiples metas activas simultáneas
- [ ] Notificaciones por scheduler (cron local)
- [ ] Temas claro/oscuro toggle
- [ ] Logs de hábitos con notas diarias

### Fase 3 · Visión 🚀

- [ ] Autenticación multi-usuario
- [ ] API REST para integración externa
- [ ] App mobile (PWA o React Native)
- [ ] IA predictiva de consistencia
- [ ] Sincronización con Google Calendar / Notion
- [ ] Despliegue en Railway / Fly.io

---

## ✦ Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Mauricio-bb/sistema-enfoque.git
cd sistema-enfoque

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Inicializar la base de datos
python enfoque.py

# 5. Ejecutar
streamlit run app.py
```

> La base de datos se crea automáticamente al primer `streamlit run app.py` si no existe. Cada usuario tiene su propia DB local — no se sincroniza con el repo.

---

## ✦ Estructura del proyecto

```
sistema-enfoque/
├── app.py              # Dashboard principal (Streamlit)
├── enfoque.py          # Inicializador de base de datos
├── diario.py           # CLI para check-in diario
├── gestion.py          # CLI para gestión de hábitos
├── grafico.py          # CLI para gráfico de barras (matplotlib)
├── requirements.txt    # Dependencias
├── .gitignore          # Ignorar DB, caches, etc.
└── README.md           # Este archivo
```

---

## ✦ Licencia

**MIT** — hacé lo que quieras con esto. Si te sirve, regalale una estrella al repo ⭐

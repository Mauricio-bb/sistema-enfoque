# ⚡ Sistema de Enfoque

**Dashboard personal de alto rendimiento.**  
Terminal de control para atletas del conocimiento: trackeá deep work, visualizá tu consistencia y mantené el rumbo hacia tus metas — con estética naval + oro.

---

## ✦ Features

| Feature | Descripción |
|---|---|
| **Hero del día** | Banner con progreso diario, racha de días consecutivos y estado de cada hábito. |
| **Habit Tracker** | Cards individuales por hábito con icono, nombre y racha. Columna completa sirve como card (sin HTML partido). |
| **Per-habit streak** | Cada card muestra su racha individual de días consecutivos. |
| **Matriz de consistencia** | Heatmap con escala navy→gold. Celdas ordenadas cronológicamente. |
| **Donuts semanales** | 7 anillos de progreso. Hoy 140px (spotlight), resto 90px. Colores por rango. |
| **Racha global** | Días consecutivos con todos los hábitos completados. |
| **Tracker financiero** | Línea diaria de urgencia para llegar a tu meta. |
| **Sidebar de gestión** | Agregá nuevos hábitos al instante. |

---

## ✦ Tech Stack

- **Python** 3.14
- **Streamlit** 1.58 — interfaz reactiva
- **SQLite** — base local, zero config
- **Plotly** 6.8 — heatmaps, donuts
- **Pandas** 3.0 — manipulación de datos
- **Caché** — `@st.cache_data(ttl=60)` + `@st.cache_resource` para conexión DB
- **Google Fonts** — DM Sans + JetBrains Mono

---

## ✦ Design System

### Paleta Navy + Gold

```
Fondos       → #0D1B2A · #1A2D45 · #243B55
Bordes       → #1E3050 · #8B6914
Tipografía   → #F0E6CC · #9BA8B5
Acento       → #C9A84C · #E8C97A
Estados      → #E07070 · #4A1A2D
```

### Componentes

| Componente | Firma visual |
|---|---|
| Hero card | Degradado, borde izquierdo gold 3px, progreso 56px |
| Habit card | Columna = card. Border-top gold/completado. Footer con botón integrado |
| Botón | NavyLight, goldDim, hover con glow gold |
| Donut | Hoy 140px, resto 90px, color por rango, % centrado |
| Heatmap | Escala navy→gold, gap 4px, eje X arriba |

---

## ✦ Roadmap

### Fase 1 · MVP ✅

- [x] Check-in diario con toggle
- [x] Matriz de consistencia (heatmap)
- [x] Donuts de consistencia semanal
- [x] Racha de días consecutivos
- [x] Tracker financiero (metas)
- [x] Diseño Navy + Gold
- [x] Sidebar de gestión de hábitos
- [x] Per-habit streak individual
- [x] Cards integradas (columna = card, sin HTML partido)
- [x] Caché optimizado (ttl=60, conexión persistente)

### Fase 2 · Próximo 🚧

- [ ] Exportación a PDF / CSV
- [ ] Múltiples metas activas
- [ ] Notificaciones por scheduler
- [ ] Tema claro/oscuro
- [ ] Notas diarias por hábito

### Fase 3 · Visión 🚀

- [ ] Autenticación multi-usuario
- [ ] API REST
- [ ] App mobile (PWA)
- [ ] IA predictiva de consistencia
- [ ] Sincronización Google Calendar / Notion
- [ ] Despliegue Railway / Fly.io

---

## ✦ Instalación

```bash
git clone https://github.com/Mauricio-bb/sistema-enfoque.git
cd sistema-enfoque
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python enfoque.py          # crear DB
streamlit run app.py       # arrancar dashboard
```

> Cada usuario tiene su propia DB local — no se sincroniza con el repo.

---

## ✦ Estructura

```
├── app.py              # Dashboard (Streamlit) — ~390 líneas
├── enfoque.py          # Inicializador de DB
├── diario.py           # CLI check-in
├── gestion.py          # CLI gestión de hábitos
├── grafico.py          # CLI gráfico matplotlib
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ✦ Licencia

**MIT** — si te sirve, regalale una estrella ⭐

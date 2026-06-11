import streamlit as st
import sqlite3
import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Sistema de Enfoque", page_icon="🎯", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
* { font-family: 'DM Sans', system-ui, sans-serif; }
.stApp {
    background-color: #0D1B2A;
    color: #F0E6CC;
}
.stApp > header { display: none; }
.main > div { padding: 24px 32px; }
h1, h2, h3, h4, h5, h6 {
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    color: #F0E6CC;
}
p, li, span, div { color: #F0E6CC; }

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0D1B2A; }
::-webkit-scrollbar-thumb { background: #1E3050; border-radius: 3px; }

/* ─── SIDEBAR ─── */
section[data-testid="stSidebar"] {
    background-color: #0D1B2A;
    border-right: 1px solid #1E3050;
}
section[data-testid="stSidebar"] .stTextInput input {
    background-color: #1A2D45;
    border: 1px solid #1E3050;
    color: #F0E6CC;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
}
section[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: #8B6914;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.15);
}
.sidebar-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #F0E6CC;
    margin-bottom: 16px;
    letter-spacing: 0.3px;
}

/* ─── HERO CARD ─── */
.hero-card {
    background: linear-gradient(135deg, #0D1B2A 0%, #1A2D45 100%);
    border: 1px solid #1E3050;
    border-left: 3px solid #C9A84C;
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 32px;
}
.hero-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}
.hero-date {
    font-family: 'DM Sans', sans-serif;
    font-size: 18px;
    font-weight: 500;
    color: #9BA8B5;
}
.hero-streak {
    font-family: 'JetBrains Mono', monospace;
    font-size: 15px;
    font-weight: 600;
    color: #E8C97A;
    background: rgba(201,168,76,0.1);
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(201,168,76,0.2);
}
.hero-body { text-align: center; }
.hero-progress-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 56px;
    font-weight: 700;
    color: #C9A84C;
    line-height: 1;
    margin-bottom: 12px;
}
.hero-progress-bar-bg {
    width: 100%;
    height: 10px;
    background: #1A2D45;
    border-radius: 5px;
    overflow: hidden;
    margin-bottom: 12px;
}
.hero-progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #8B6914, #C9A84C);
    border-radius: 5px;
    transition: width 0.5s ease;
}
.hero-subtext {
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    color: #9BA8B5;
    margin-bottom: 20px;
}
.hero-habits {
    display: flex;
    justify-content: center;
    gap: 24px;
    flex-wrap: wrap;
}
.hero-habit {
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    font-weight: 500;
    color: #F0E6CC;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #1A2D45;
    padding: 6px 14px;
    border-radius: 8px;
    border: 1px solid #1E3050;
}
.hero-habit-icon { font-size: 16px; }

/* ─── SECTION TITLES ─── */
.section-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 20px;
    font-weight: 600;
    color: #F0E6CC;
    margin-bottom: 16px;
    letter-spacing: 0.2px;
}

/* ─── CHECK-IN CARDS ─── */
.checkin-card {
    background: #1A2D45;
    border-radius: 10px 10px 0 0;
    padding: 16px;
    text-align: center;
    border-top: 3px solid #1E3050;
    border-left: 1px solid #1E3050;
    border-right: 1px solid #1E3050;
    min-height: 100px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
}
.checkin-card.completed {
    border-top-color: #C9A84C;
    border-left-color: rgba(201,168,76,0.2);
    border-right-color: rgba(201,168,76,0.2);
}
.checkin-card.in-progress {
    border-top-color: #E8C97A;
    border-left-color: rgba(232,201,122,0.2);
    border-right-color: rgba(232,201,122,0.2);
}
.checkin-card.failed {
    border-top-color: #E07070;
    border-left-color: rgba(224,112,112,0.2);
    border-right-color: rgba(224,112,112,0.2);
}
.checkin-icon { font-size: 28px; }
.checkin-name {
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    font-weight: 500;
    color: #F0E6CC;
}

/* ─── BUTTONS ─── */
div.stButton > button {
    background: #243B55;
    border-radius: 0 0 10px 10px;
    border: 1px solid #8B6914;
    border-top: none;
    color: #E8C97A;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 13px;
    transition: all 0.2s ease;
    width: 100%;
}
div.stButton > button:hover {
    background: #1A2D45;
    border-color: #C9A84C;
    box-shadow: 0 0 12px rgba(201,168,76,0.2);
    color: #C9A84C;
}
div.stButton > button:active {
    background: #243B55;
    border-color: #C9A84C;
    color: #C9A84C;
}

/* ─── DONUT LABELS ─── */
.donut-label {
    text-align: center;
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    color: #9BA8B5;
    margin-top: 4px;
}

/* ─── FINANCE CARD ─── */
.finance-card {
    background: linear-gradient(135deg, #0D1B2A 0%, #1A2D45 100%);
    border: 1px solid #1E3050;
    border-left: 3px solid #C9A84C;
    border-radius: 12px;
    padding: 20px 32px;
    margin-bottom: 32px;
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}
.finance-emoji { font-size: 28px; }
.finance-text {
    font-family: 'DM Sans', sans-serif;
    font-size: 16px;
    color: #9BA8B5;
}
.finance-amount {
    font-family: 'JetBrains Mono', monospace;
    font-size: 28px;
    font-weight: 700;
    color: #C9A84C;
}

/* ─── SIDEBAR BUTTON ─── */
section[data-testid="stSidebar"] div.stButton > button {
    background: #243B55;
    border: 1px solid #8B6914;
    color: #E8C97A;
    border-radius: 10px;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
    transition: all 0.2s ease;
}
section[data-testid="stSidebar"] div.stButton > button:hover {
    background: #1A2D45;
    border-color: #C9A84C;
    box-shadow: 0 0 12px rgba(201,168,76,0.2);
}

/* ─── INFO BOX ─── */
.stAlert {
    background-color: #1A2D45 !important;
    border: 1px solid #1E3050 !important;
    border-left: 3px solid #8B6914 !important;
    color: #F0E6CC !important;
    border-radius: 8px !important;
}
.stAlert p { color: #F0E6CC !important; }

/* ─── RESPONSIVE ─── */
@media (max-width: 768px) {
    .hero-progress-label { font-size: 36px; }
    .hero-habits { gap: 12px; }
    .hero-habit { font-size: 12px; padding: 4px 10px; }
}
</style>
""", unsafe_allow_html=True)

# ─── DB ──────────────────────────────────────────────────────────────────────

def conectar():
    conn = sqlite3.connect('sistema_enfoque.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@st.cache_data(ttl=3)
def obtener_datos():
    conn = conectar()
    habitos = pd.read_sql_query("SELECT * FROM habitos", conn)
    registros = pd.read_sql_query("SELECT * FROM registros", conn)
    conn.close()
    return habitos, registros

habitos, registros = obtener_datos()

# ─── CONSTANTS ───────────────────────────────────────────────────────────────

hoy = datetime.date.today()
dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
fecha_label = f"{dias_semana[hoy.weekday()]} {hoy.day} de {meses[hoy.month - 1]}"

total_h = len(habitos) if not habitos.empty else 0
fecha_hoy_str = str(hoy)

completados_ids = []
pct_hoy = 0
completados_hoy = 0

if not registros.empty:
    completados_hoy = registros[registros['fecha'] == fecha_hoy_str]['completado'].sum()
    completados_ids = registros[registros['fecha'] == fecha_hoy_str]['habito_id'].tolist()

if total_h > 0:
    pct_hoy = int(completados_hoy / total_h * 100)

streak = 0
if total_h > 0 and not registros.empty:
    check_date = hoy - datetime.timedelta(days=1)
    while True:
        day_data = registros[registros['fecha'] == str(check_date)]
        if not day_data.empty and day_data['completado'].sum() == total_h:
            streak += 1
            check_date -= datetime.timedelta(days=1)
        else:
            break

# ─── EMOJI MAP ───────────────────────────────────────────────────────────────

def get_emoji(nombre):
    name = nombre.lower()
    emojis = {
        'programación': '💻', 'programacion': '💻', 'coding': '💻',
        'michishop': '🛍️', 'shop': '🛍️',
        'ejercicio': '🏋️', 'gym': '🏋️', 'entrenamiento': '🏋️', 'running': '🏃',
        'lectura': '📚', 'leer': '📚', 'reading': '📚', 'libro': '📚',
        'meditación': '🧘', 'meditacion': '🧘', 'meditate': '🧘',
        'agua': '💧', 'water': '💧',
        'diario': '📝', 'journal': '📝',
        'ingles': '🇬🇧', 'english': '🇬🇧', 'inglés': '🇬🇧',
        'guitarra': '🎸', 'music': '🎸', 'música': '🎸',
    }
    for key, icon in emojis.items():
        if key in name:
            return icon
    return '📌'

# ─── HERO ─────────────────────────────────────────────────────────────────────

if total_h > 0:
    hero_habits_html = ""
    for _, row in habitos.iterrows():
        completed = row['id'] in completados_ids
        icon = get_emoji(row['nombre'])
        status_icon = "✅" if completed else "⬜"
        hero_habits_html += (
            f'<span class="hero-habit">'
            f'<span class="hero-habit-icon">{icon}</span>'
            f'{row["nombre"]} {status_icon}'
            f'</span>'
        )

    streak_html = f'🔥 {streak} días consecutivos' if streak > 0 else ''
    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-top">
            <span class="hero-date">{fecha_label}</span>
            {'<span class="hero-streak">' + streak_html + '</span>' if streak_html else ''}
        </div>
        <div class="hero-body">
            <div class="hero-progress-label">{pct_hoy}%</div>
            <div class="hero-progress-bar-bg">
                <div class="hero-progress-bar-fill" style="width: {pct_hoy}%"></div>
            </div>
            <div class="hero-subtext">{completados_hoy} de {total_h} hábitos completados hoy</div>
            <div class="hero-habits">{hero_habits_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-top">
            <span class="hero-date">{fecha_label}</span>
        </div>
        <div class="hero-body">
            <div class="hero-subtext">Agregá tu primer hábito desde el panel lateral →</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── CHECK-IN ────────────────────────────────────────────────────────────────

st.markdown("<h2 class='section-title'>✅ Registro de hoy</h2>", unsafe_allow_html=True)

if not habitos.empty:
    cols_check = st.columns(len(habitos))
    for i, (idx, row) in enumerate(habitos.iterrows()):
        with cols_check[i]:
            ya_completado = row['id'] in completados_ids
            status_class = "completed" if ya_completado else "in-progress"
            icon = get_emoji(row['nombre'])
            label = "✓ Completado" if ya_completado else "Marcar completado"

            st.markdown(f"""
            <div class="checkin-card {status_class}">
                <div class="checkin-icon">{icon}</div>
                <div class="checkin-name">{row['nombre']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(label, key=f"check_{row['id']}", use_container_width=True):
                conn = conectar()
                if ya_completado:
                    conn.execute(
                        "DELETE FROM registros WHERE habito_id = ? AND fecha = ?",
                        (row['id'], fecha_hoy_str)
                    )
                else:
                    conn.execute(
                        "INSERT INTO registros (habito_id, completado, fecha) VALUES (?, 1, ?)",
                        (row['id'], fecha_hoy_str)
                    )
                conn.commit()
                conn.close()
                st.cache_data.clear()
                st.rerun()
else:
    st.markdown(
        '<div class="stAlert"><p>No hay hábitos todavía. Agregá uno desde el panel lateral.</p></div>',
        unsafe_allow_html=True
    )

# ─── DONUTS ──────────────────────────────────────────────────────────────────

st.markdown("<h2 class='section-title'>🗓️ Consistencia semanal</h2>", unsafe_allow_html=True)

cols_donuts = st.columns(7)
ultimos_7_dias = [(hoy - datetime.timedelta(days=i)) for i in range(6, -1, -1)]

for i, col in enumerate(cols_donuts):
    fecha_target = ultimos_7_dias[i]
    fecha_str = str(fecha_target)

    completados = 0
    if not registros.empty:
        datos_dia = registros[registros['fecha'] == fecha_str]
        completados = datos_dia['completado'].sum() if not datos_dia.empty else 0

    valor_pct = int((completados / total_h * 100) if total_h > 0 else 0)

    if valor_pct == 100:
        donut_colors = ['#C9A84C', '#1A2D45']
    elif valor_pct >= 50:
        donut_colors = ['#E8C97A', '#1A2D45']
    elif valor_pct > 0:
        donut_colors = ['#243B55', '#1A2D45']
    else:
        donut_colors = ['#1A2D45', '#1A2D45']

    is_today = (i == 6)
    height = 140 if is_today else 90

    with col:
        fig_donut = go.Figure(go.Pie(
            hole=.7,
            values=[valor_pct, 100 - valor_pct],
            marker=dict(colors=donut_colors, line=dict(
                color='rgba(0,0,0,0)', width=0
            )),
            showlegend=False,
            textinfo='none',
            direction='clockwise',
            sort=False,
        ))
        annotations = []
        if valor_pct > 0:
            annotations.append(dict(
                text=f"{valor_pct}%",
                x=0.5, y=0.5,
                font=dict(
                    size=16 if is_today else 12,
                    color='#F0E6CC',
                    family='JetBrains Mono',
                    weight=600,
                ),
                showarrow=False,
            ))
        fig_donut.update_layout(
            margin=dict(l=4, r=4, t=4, b=4),
            height=height,
            paper_bgcolor='rgba(0,0,0,0)',
            annotations=annotations,
        )
        st.plotly_chart(fig_donut, use_container_width=True, key=f"donut_{i}")
        st.markdown(
            f"<p class='donut-label'>{fecha_target.strftime('%a %d')}</p>",
            unsafe_allow_html=True
        )

# ─── HEATMAP ─────────────────────────────────────────────────────────────────

st.markdown("<h2 class='section-title'>📋 Matriz de consistencia</h2>", unsafe_allow_html=True)

if not registros.empty and not habitos.empty:
    registros_full = registros.merge(habitos, left_on='habito_id', right_on='id')
    matrix = registros_full.pivot_table(
        index='nombre', columns='fecha', values='completado', aggfunc='max'
    ).fillna(0)

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=matrix.values,
        x=list(matrix.columns),
        y=list(matrix.index),
        colorscale=[
            [0.0, "#0D1B2A"],
            [0.01, "#1A2D45"],
            [0.5, "#8B6914"],
            [1.0, "#C9A84C"],
        ],
        showscale=False,
        xgap=4,
        ygap=4,
        hoverongaps=False,
        hovertemplate='%{y}<br>%{x}<br>%{z}<extra></extra>',
    ))

    n_dates = len(matrix.columns)
    height = max(160, 40 * len(matrix.index))

    fig_heatmap.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=height,
        xaxis=dict(
            showgrid=False,
            side='top',
            tickfont=dict(size=10, color='#9BA8B5', family='JetBrains Mono'),
            tickangle=-45,
            dtick=1 if n_dates <= 31 else max(1, n_dates // 30),
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=12, color='#F0E6CC'),
            autorange='reversed',
        ),
    )
    st.plotly_chart(fig_heatmap, use_container_width=True, key="heatmap")
else:
    st.markdown(
        '<div class="stAlert"><p>Completá algunos hábitos para ver tu matriz de consistencia.</p></div>',
        unsafe_allow_html=True
    )

# ─── FINANCE TRACKER ─────────────────────────────────────────────────────────

try:
    conn_fin = conectar()
    metas_df = pd.read_sql_query(
        "SELECT * FROM metas WHERE completada = 0 ORDER BY fecha_fin LIMIT 1",
        conn_fin
    )
    conn_fin.close()
    if not metas_df.empty:
        meta = metas_df.iloc[0]
        restante = float(meta['monto_meta']) - float(meta['monto_actual'])
        hoy_ts = pd.Timestamp.today()
        fecha_fin = pd.to_datetime(meta['fecha_fin'])
        dias_restantes = (fecha_fin - hoy_ts).days
        if dias_restantes > 0:
            diario = restante / dias_restantes
            st.markdown(f"""
            <div class="finance-card">
                <span class="finance-emoji">💰</span>
                <span class="finance-text">Necesitás </span>
                <span class="finance-amount">${diario:.2f}</span>
                <span class="finance-text">/día para llegar a tu meta — {meta['nombre']}</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:13px;color:#9BA8B5;margin-left:auto;">
                    {restante:.0f} restantes · {dias_restantes}d
                </span>
            </div>
            """, unsafe_allow_html=True)
except Exception:
    pass

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("<div style='font-size:22px;font-weight:700;color:#C9A84C;margin-bottom:24px;letter-spacing:0.5px;'>⚡ ENFOQUE</div>", unsafe_allow_html=True)
    st.markdown("<h2 class='sidebar-title'>⚙️ Gestión</h2>", unsafe_allow_html=True)
    nuevo = st.text_input("Añadir nuevo reto:", placeholder="Nombre del hábito")
    if st.button("Guardar", use_container_width=True):
        if nuevo:
            conn = conectar()
            conn.execute("INSERT INTO habitos (nombre) VALUES (?)", (nuevo,))
            conn.commit()
            conn.close()
            st.cache_data.clear()
            st.rerun()

    st.markdown("<hr style='border-color:#1E3050;margin:24px 0;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-family:DM Sans;font-size:12px;color:#9BA8B5;text-align:center;'>"
        "Sistema de Enfoque v2 · Navy + Gold</p>",
        unsafe_allow_html=True
    )

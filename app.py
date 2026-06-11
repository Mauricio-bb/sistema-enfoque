import streamlit as st
import sqlite3
import pandas as pd
import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="Sistema de Enfoque", page_icon="🎯", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{font-family:'DM Sans',system-ui,sans-serif}
.stApp{background-color:#0D1B2A;color:#F0E6CC}
.stApp>header{display:none}
.main>div{padding:24px 32px}
h1,h2,h3,h4,h5,h6{font-family:'DM Sans',sans-serif;font-weight:700;color:#F0E6CC;margin:0}
p,li,span,div,label{color:#F0E6CC}
a{color:#C9A84C;text-decoration:none}

::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:#0D1B2A}
::-webkit-scrollbar-thumb{background:#1E3050;border-radius:3px}

/* ─── SIDEBAR ─── */
section[data-testid="stSidebar"]{background-color:#0D1B2A;border-right:1px solid #1E3050;padding-top:0}
section[data-testid="stSidebar"] .stTextInput input{background-color:#1A2D45;border:1px solid #1E3050;color:#F0E6CC;border-radius:8px;font-family:'DM Sans',sans-serif}
section[data-testid="stSidebar"] .stTextInput input:focus{border-color:#8B6914;box-shadow:0 0 0 2px rgba(201,168,76,0.15)}
.sidebar-title{font-size:18px;font-weight:700;margin-bottom:16px;letter-spacing:0.3px}
section[data-testid="stSidebar"] div.stButton>button{background:#243B55;border:1px solid #8B6914;color:#E8C97A;border-radius:10px;font-weight:600;transition:all .2s}
section[data-testid="stSidebar"] div.stButton>button:hover{background:#1A2D45;border-color:#C9A84C;box-shadow:0 0 12px rgba(201,168,76,0.2)}

/* ─── HERO ─── */
.hero-card{background:linear-gradient(135deg,#0D1B2A 0%,#1A2D45 100%);border:1px solid #1E3050;border-left:3px solid #C9A84C;border-radius:12px;padding:24px 32px;margin-bottom:32px}
.hero-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}
.hero-date{font-size:18px;font-weight:500;color:#9BA8B5}
.hero-streak{font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:600;color:#E8C97A;background:rgba(201,168,76,0.1);padding:4px 14px;border-radius:20px;border:1px solid rgba(201,168,76,0.2)}
.hero-body{text-align:center}
.hero-progress-label{font-family:'JetBrains Mono',monospace;font-size:56px;font-weight:700;color:#C9A84C;line-height:1;margin-bottom:12px}
.hero-progress-bar-bg{max-width:480px;margin:0 auto 12px;height:10px;background:#1A2D45;border-radius:5px;overflow:hidden}
.hero-progress-bar-fill{height:100%;background:linear-gradient(90deg,#8B6914,#C9A84C);border-radius:5px;transition:width .6s ease}
.hero-subtext{font-size:15px;color:#9BA8B5;margin-bottom:20px}
.hero-habits{display:flex;justify-content:center;gap:12px;flex-wrap:wrap}
.hero-habit{font-size:13px;font-weight:500;display:inline-flex;align-items:center;gap:6px;background:#1A2D45;padding:6px 14px;border-radius:8px;border:1px solid #1E3050}
.hero-habit-icon{font-size:15px}

/* ─── SECTION TITLES ─── */
.section-title{font-size:20px;font-weight:600;margin-bottom:16px;letter-spacing:0.2px}

/* ─── HABIT CARDS (column-as-card) ─── */
div[data-testid="column"]{
    background:#1A2D45;
    border-radius:12px;
    border:1px solid #1E3050;
    border-top:3px solid #1E3050;
    overflow:hidden;
    transition:border-color .25s,border-top-color .35s;
}
div[data-testid="column"]:has(.hc.completed){
    border-top-color:#C9A84C;
    border-color:rgba(201,168,76,0.2);
}
div[data-testid="column"]:has(.hc.pending){
    border-top-color:#1E3050;
}
.hc{padding:16px 12px 10px;text-align:center}
.hc-icon{font-size:28px;display:block;margin-bottom:2px}
.hc-name{font-size:14px;font-weight:600;margin-bottom:2px}
.hc-streak{font-size:11px;color:#9BA8B5;font-family:'JetBrains Mono',monospace}
.hc-streak.active{color:#E8C97A}

div[data-testid="column"]>div:last-child button{
    background:transparent;
    border:none;
    border-top:1px solid rgba(255,255,255,0.06);
    border-radius:0;
    color:#9BA8B5;
    font-family:'DM Sans',sans-serif;
    font-size:13px;
    font-weight:600;
    padding:10px;
    width:100%;
    cursor:pointer;
    transition:background .2s,color .2s;
}
div[data-testid="column"]:has(.hc.completed)>div:last-child button{color:#C9A84C}
div[data-testid="column"]>div:last-child button:hover{background:rgba(201,168,76,0.08);color:#E8C97A}

/* ─── DONUTS ─── */
.donut-label{text-align:center;font-size:11px;color:#9BA8B5;margin-top:2px;font-family:'JetBrains Mono',monospace}

/* ─── FINANCE ─── */
.finance-card{background:linear-gradient(135deg,#0D1B2A 0%,#1A2D45 100%);border:1px solid #1E3050;border-left:3px solid #C9A84C;border-radius:12px;padding:20px 32px;margin-bottom:32px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.finance-emoji{font-size:28px}
.finance-text{font-size:16px;color:#9BA8B5}
.finance-amount{font-family:'JetBrains Mono',monospace;font-size:28px;font-weight:700;color:#C9A84C}

/* ─── INFO BOX ─── */
.stAlert{background-color:#1A2D45!important;border:1px solid #1E3050!important;border-left:3px solid #8B6914!important;color:#F0E6CC!important;border-radius:8px!important}
.stAlert p{color:#F0E6CC!important}

@media(max-width:768px){
.main>div{padding:16px}
.hero-card{padding:16px 20px}
.hero-progress-label{font-size:36px}
.hero-habits{gap:8px}
.hero-habit{font-size:12px;padding:4px 10px}
.hc{padding:12px 8px 8px}
.hc-icon{font-size:22px}
.hc-name{font-size:12px}
}
</style>
""", unsafe_allow_html=True)

# ─── DB ──────────────────────────────────────────────────────────────────────

@st.cache_resource
def get_conn():
    conn = sqlite3.connect('sistema_enfoque.db', check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@st.cache_data(ttl=60)
def obtener_datos(_conn):
    habitos = pd.read_sql_query("SELECT * FROM habitos", _conn)
    registros = pd.read_sql_query("SELECT * FROM registros", _conn)
    return habitos, registros

conn = get_conn()
habitos, registros = obtener_datos(conn)

if 'rev' not in st.session_state:
    st.session_state.rev = 0

# ─── CONSTANTS ───────────────────────────────────────────────────────────────

hoy = datetime.date.today()
dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
fecha_label = f"{dias[hoy.weekday()]} {hoy.day} de {meses[hoy.month - 1]}"

total_h = len(habitos) if not habitos.empty else 0
fhs = str(hoy)

completados_ids = []
pct_hoy = 0
completados_hoy = 0

if not registros.empty:
    hd = registros[registros['fecha'] == fhs]
    completados_hoy = int(hd['completado'].sum())
    completados_ids = hd['habito_id'].tolist()

if total_h > 0:
    pct_hoy = int(completados_hoy / total_h * 100)

# ─── STREAKS ─────────────────────────────────────────────────────────────────

streak = 0
if total_h > 0 and not registros.empty:
    fd = registros.groupby('fecha')['completado'].sum().reset_index()
    fd = fd[fd['completado'] == total_h]
    fs = set(fd['fecha'].tolist())
    c = hoy - datetime.timedelta(days=1)
    while str(c) in fs:
        streak += 1
        c -= datetime.timedelta(days=1)

def habit_streak(hid):
    if registros.empty:
        return 0
    hr = registros[(registros['habito_id'] == hid) & (registros['completado'] == 1)]
    f = set(hr['fecha'].tolist())
    s = 0
    d = hoy - datetime.timedelta(days=1)
    while str(d) in f:
        s += 1
        d -= datetime.timedelta(days=1)
    return s

# ─── EMOJI ───────────────────────────────────────────────────────────────────

def emoji(n):
    n = n.lower()
    m = {
        'programación': '💻', 'programacion': '💻', 'coding': '💻',
        'michishop': '🛍️', 'shop': '🛍️',
        'ejercicio': '🏋️', 'gym': '🏋️', 'entrenamiento': '🏋️', 'running': '🏃',
        'lectura': '📚', 'leer': '📚', 'reading': '📚', 'libro': '📚',
        'meditación': '🧘', 'meditacion': '🧘', 'meditate': '🧘',
        'agua': '💧', 'water': '💧',
        'diario': '📝', 'journal': '📝',
        'ingles': '🇬🇧', 'english': '🇬🇧', 'inglés': '🇬🇧',
        'guitarra': '🎸', 'music': '🎸', 'música': '🎸',
        'dios': '🙏', 'biblia': '📖',
        'facultad': '🎓', 'uni': '🎓', 'estudio': '📖',
        'dropshipping': '📦', 'negocio': '💼',
        'recreativo': '🎮', 'ocio': '🎮',
    }
    for k, v in m.items():
        if k in n:
            return v
    return '📌'

# ─── TOGGLE ──────────────────────────────────────────────────────────────────

def toggle(hid):
    if hid in completados_ids:
        conn.execute("DELETE FROM registros WHERE habito_id=? AND fecha=?", (hid, fhs))
    else:
        conn.execute("INSERT INTO registros (habito_id,completado,fecha) VALUES (?,1,?)", (hid, fhs))
    conn.commit()
    st.cache_data.clear()
    st.session_state.rev += 1
    st.rerun()

# ─── HERO ─────────────────────────────────────────────────────────────────────

if total_h > 0:
    hh = "".join(
        f'<span class="hero-habit"><span class="hero-habit-icon">{emoji(r["nombre"])}</span>'
        f'{r["nombre"]} {"✅" if r["id"] in completados_ids else "⬜"}</span>'
        for _, r in habitos.iterrows()
    )
    sh = f'🔥 {streak} días consecutivos' if streak > 0 else ''
    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-top">
            <span class="hero-date">{fecha_label}</span>
            {f'<span class="hero-streak">{sh}</span>' if sh else ''}
        </div>
        <div class="hero-body">
            <div class="hero-progress-label">{pct_hoy}%</div>
            <div class="hero-progress-bar-bg"><div class="hero-progress-bar-fill" style="width:{pct_hoy}%"></div></div>
            <div class="hero-subtext">{completados_hoy} de {total_h} hábitos completados hoy</div>
            <div class="hero-habits">{hh}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-top"><span class="hero-date">{fecha_label}</span></div>
        <div class="hero-body"><div class="hero-subtext">Agregá tu primer hábito desde el panel lateral →</div></div>
    </div>
    """, unsafe_allow_html=True)

# ─── HABIT TRACKER ───────────────────────────────────────────────────────────

st.markdown("<h2 class='section-title'>✅ Registro de hoy</h2>", unsafe_allow_html=True)

if not habitos.empty:
    cols = st.columns(len(habitos))
    for i, (_, r) in enumerate(habitos.iterrows()):
        with cols[i]:
            hid = r['id']
            ya = hid in completados_ids
            status = "completed" if ya else "pending"
            hs = habit_streak(hid)

            st.markdown(f"""
            <div class="hc {status}">
                <span class="hc-icon">{emoji(r['nombre'])}</span>
                <div class="hc-name">{r['nombre']}</div>
                <div class="hc-streak{' active' if hs > 0 else ''}">{'🔥 '+str(hs)+'d' if hs > 0 else '—'}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("✓ Hecho" if ya else "Marcar", key=f"h_{hid}", width='stretch'):
                toggle(hid)
else:
    st.markdown('<div class="stAlert"><p>No hay hábitos todavía. Agregá uno desde el panel lateral.</p></div>', unsafe_allow_html=True)

# ─── DONUTS ──────────────────────────────────────────────────────────────────

st.markdown("<h2 class='section-title'>🗓️ Consistencia semanal</h2>", unsafe_allow_html=True)

cols_d = st.columns(7)
ult7 = [(hoy - datetime.timedelta(days=i)) for i in range(6, -1, -1)]

for i, col in enumerate(cols_d):
    ft = ult7[i]
    fs = str(ft)
    c = 0
    if not registros.empty:
        dd = registros[registros['fecha'] == fs]
        c = int(dd['completado'].sum()) if not dd.empty else 0

    v = int((c / total_h * 100) if total_h > 0 else 0)

    if v == 100:
        dc = ['#C9A84C', '#1A2D45']
    elif v >= 50:
        dc = ['#E8C97A', '#1A2D45']
    elif v > 0:
        dc = ['#243B55', '#1A2D45']
    else:
        dc = ['#1A2D45', '#1A2D45']

    today = (i == 6)
    h = 140 if today else 90

    with col:
        fig = go.Figure(go.Pie(
            hole=.7, values=[v, 100 - v],
            marker=dict(colors=dc, line=dict(color='rgba(0,0,0,0)', width=0)),
            showlegend=False, textinfo='none', direction='clockwise', sort=False,
        ))
        ann = []
        if v > 0:
            ann.append(dict(
                text=f"{v}%", x=0.5, y=0.5,
                font=dict(size=16 if today else 12, color='#F0E6CC', family='JetBrains Mono', weight=600),
                showarrow=False,
            ))
        fig.update_layout(
            margin=dict(l=2, r=2, t=2, b=2),
            height=h, paper_bgcolor='rgba(0,0,0,0)', annotations=ann,
        )
        st.plotly_chart(fig, width='stretch', key=f"d_{st.session_state.rev}_{i}")
        st.markdown(f"<p class='donut-label'>{ft.strftime('%a %d')}</p>", unsafe_allow_html=True)

# ─── HEATMAP ─────────────────────────────────────────────────────────────────

st.markdown("<h2 class='section-title'>📋 Matriz de consistencia</h2>", unsafe_allow_html=True)

if not registros.empty and not habitos.empty:
    rf = registros.merge(habitos, left_on='habito_id', right_on='id')
    mat = rf.pivot_table(index='nombre', columns='fecha', values='completado', aggfunc='max').fillna(0)
    mat = mat[sorted(mat.columns)]

    fig = go.Figure(data=go.Heatmap(
        z=mat.values, x=list(mat.columns), y=list(mat.index),
        colorscale=[[0.0, "#0D1B2A"], [0.01, "#1A2D45"], [0.5, "#8B6914"], [1.0, "#C9A84C"]],
        showscale=False, xgap=4, ygap=4, hoverongaps=False,
        hovertemplate='%{y}<br>%{x}<br>%{z}<extra></extra>',
    ))
    nd = len(mat.columns)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=max(160, 44 * len(mat.index)),
        xaxis=dict(
            showgrid=False, side='top',
            tickfont=dict(size=10, color='#9BA8B5', family='JetBrains Mono'),
            tickangle=-45,
            dtick=1 if nd <= 31 else max(1, nd // 30),
        ),
        yaxis=dict(showgrid=False, tickfont=dict(size=12, color='#F0E6CC'), autorange='reversed'),
    )
    st.plotly_chart(fig, width='stretch', key=f"hm_{st.session_state.rev}")
else:
    st.markdown('<div class="stAlert"><p>Completá algunos hábitos para ver tu matriz de consistencia.</p></div>', unsafe_allow_html=True)

# ─── FINANCE ─────────────────────────────────────────────────────────────────

try:
    metas = pd.read_sql_query(
        "SELECT * FROM metas WHERE completada = 0 ORDER BY fecha_fin LIMIT 1", conn
    )
    if not metas.empty:
        m = metas.iloc[0]
        rest = float(m['monto_meta']) - float(m['monto_actual'])
        ff = pd.to_datetime(m['fecha_fin'])
        dr = (ff - pd.Timestamp.today()).days
        if dr > 0:
            d = rest / dr
            st.markdown(f"""
            <div class="finance-card">
                <span class="finance-emoji">💰</span>
                <span class="finance-text">Necesitás </span>
                <span class="finance-amount">${d:.2f}</span>
                <span class="finance-text">/día — {m['nombre']}</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:13px;color:#9BA8B5;margin-left:auto;">{rest:.0f} rest · {dr}d</span>
            </div>
            """, unsafe_allow_html=True)
except Exception:
    pass

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("<div style='font-size:22px;font-weight:700;color:#C9A84C;margin-bottom:24px;letter-spacing:0.5px;'>⚡ ENFOQUE</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-title'>⚙️ Gestión</div>", unsafe_allow_html=True)
    nuevo = st.text_input("", placeholder="Nombre del hábito", label_visibility="collapsed")
    if st.button("Guardar", width='stretch'):
        if nuevo:
            conn.execute("INSERT INTO habitos (nombre) VALUES (?)", (nuevo,))
            conn.commit()
            st.cache_data.clear()
            st.session_state.rev += 1
            st.rerun()
    st.markdown("<hr style='border-color:#1E3050;margin:24px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px;color:#9BA8B5;text-align:center;'>Sistema de Enfoque v3 · Navy + Gold</p>", unsafe_allow_html=True)

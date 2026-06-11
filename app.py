import streamlit as st
import sqlite3
import pandas as pd
import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="Sistema de Enfoque", page_icon="⚡", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
--color-bg-base:#0d1b2a;
--color-bg-surface:#1a2d45;
--color-bg-raised:#243b55;
--color-border:#1e3050;
--color-border-acc:#8b6914;
--color-text-main:#f0e6cc;
--color-text-muted:#9ba8b5;
--color-accent:#c9a84c;
--color-accent-light:#e8c97a;
--color-accent-dim:#8b6914;
--color-danger:#e07070;
--color-danger-bg:#4a1a2d;
--color-success:#5FB57A;
--font-display:'DM Sans',system-ui,sans-serif;
--font-data:'JetBrains Mono',monospace;
--space-1:8px;--space-2:16px;--space-3:24px;--space-4:32px;--space-6:48px;
--radius-sm:6px;--radius-md:10px;--radius-lg:14px;--radius-pill:20px;
--btn-bg:#243b55;--btn-border:#8b6914;--btn-text:#e8c97a;
--btn-hover-bg:#1a2d45;--btn-hover-border:#c9a84c;
--btn-hover-shadow:0 0 12px rgba(201,168,76,0.2);
--card-bg:#1a2d45;--card-border:#1e3050;--card-radius:var(--radius-md);
--transition-fast:0.15s ease;--transition-base:0.25s ease;
--glow-accent:0 0 20px rgba(201,168,76,0.15);
}
*{font-family:var(--font-display);border-color:var(--color-border)}
.stApp{background-color:var(--color-bg-base);color:var(--color-text-main)}
.stApp>header{display:none}
.main>div{padding:var(--space-3) var(--space-4)}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--color-bg-base)}
::-webkit-scrollbar-thumb{background:var(--color-bg-raised);border-radius:8px}
::-webkit-scrollbar-thumb:hover{background:var(--color-accent-dim)}

/* ─── SIDEBAR ─── */
section[data-testid="stSidebar"]{background-color:var(--color-bg-base);border-right:1px solid var(--color-border);padding-top:0}
section[data-testid="stSidebar"] .stTextInput input{background-color:var(--color-bg-surface);border:1px solid var(--color-border);color:var(--color-text-main);border-radius:var(--radius-sm);font-family:var(--font-display)}
section[data-testid="stSidebar"] .stTextInput input:focus{border-color:var(--color-accent-dim);box-shadow:0 0 0 2px rgba(201,168,76,0.15)}
section[data-testid="stSidebar"] div.stButton>button{background:var(--btn-bg);border:1px solid var(--btn-border);color:var(--btn-text);border-radius:var(--radius-md);font-weight:600;transition:all var(--transition-fast)}
section[data-testid="stSidebar"] div.stButton>button:hover{background:var(--btn-hover-bg);border-color:var(--btn-hover-border);box-shadow:var(--btn-hover-shadow)}

/* ─── HEADER ─── */
.app-header{display:flex;align-items:center;justify-content:space-between;padding:var(--space-2) 0;border-bottom:1px solid var(--color-border);margin-bottom:var(--space-3)}
.app-brand{display:flex;align-items:center;gap:8px}
.app-brand svg{color:var(--color-accent)}
.app-brand span{font-size:20px;font-weight:700;letter-spacing:-0.3px;color:var(--color-text-main)}
.app-actions{display:flex;align-items:center;gap:12px}
.app-date{font-size:13px;color:var(--color-text-muted)}
.app-streak{display:flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:var(--color-accent);font-family:var(--font-data)}

/* ─── HERO ─── */
.hero-card{background:linear-gradient(135deg,var(--color-bg-base) 0%,var(--color-bg-surface) 100%);border:1px solid var(--color-border);border-radius:var(--radius-md);padding:var(--space-3)}.hero-card.with-accent{border-left:3px solid var(--color-accent)}
.hero-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:var(--space-2)}
.hero-title{font-size:14px;font-weight:600;display:flex;align-items:center;gap:8px;color:var(--color-text-main)}
.hero-badge{display:flex;align-items:center;gap:6px;padding:3px 10px;border-radius:var(--radius-pill);font-size:11px;border:1px solid rgba(201,168,76,0.3);color:var(--color-accent);background:var(--color-bg-base)}
.hero-badge-dot{width:6px;height:6px;border-radius:50%;background:var(--color-accent);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}
.hero-body{text-align:center;padding:var(--space-2) 0}
.hero-pct{font-family:var(--font-data);font-size:48px;font-weight:700;color:var(--color-accent);line-height:1;margin-bottom:var(--space-1)}
.hero-bar{max-width:400px;margin:0 auto var(--space-1);height:10px;background:var(--color-bg-base);border-radius:5px;overflow:hidden;border:1px solid var(--color-border)}
.hero-bar-fill{height:100%;background:linear-gradient(90deg,var(--color-accent-dim),var(--color-accent));border-radius:5px;transition:width .6s ease}
.hero-meta{font-size:13px;color:var(--color-text-muted);margin-bottom:var(--space-2)}
.hero-habits{display:flex;justify-content:center;gap:8px;flex-wrap:wrap}
.hero-habit{font-size:12px;display:inline-flex;align-items:center;gap:4px;background:var(--color-bg-surface);padding:4px 10px;border-radius:var(--radius-sm);border:1px solid var(--color-border)}

/* ─── HABIT CARD ─── */
.hc{background:var(--color-bg-surface);border:1px solid var(--color-border);border-radius:var(--radius-md);padding:var(--space-2);border-top:3px solid var(--color-border);transition:background var(--transition-fast);cursor:default}
.hc:hover{background:var(--color-bg-raised)}
.hc.completado{border-top-color:var(--color-accent)}
.hc.en-camino{border-top-color:var(--color-accent-light)}
.hc.sin-registrar{border-top-color:var(--color-border)}
.hc.fallido{border-top-color:var(--color-danger)}
.hc-top{display:flex;align-items:center;gap:8px;margin-bottom:8px}
.hc-icon-box{width:36px;height:36px;display:flex;align-items:center;justify-content:center;border-radius:var(--radius-sm);background:rgba(201,168,76,0.12);font-size:18px}
.hc-name{font-size:13px;font-weight:600;color:var(--color-text-main);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hc-badge{display:inline-block;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;padding:2px 8px;border-radius:var(--radius-pill);white-space:nowrap;margin-bottom:8px}
.hc-metric{display:flex;align-items:baseline;gap:4px;font-family:var(--font-data);margin-bottom:8px}
.hc-metric-val{font-size:22px;font-weight:600;color:var(--color-accent)}
.hc-metric-label{font-size:12px;color:var(--color-text-muted)}
.hc-bar{height:6px;border-radius:3px;overflow:hidden;background:rgba(255,255,255,0.06);margin-bottom:4px}
.hc-bar-fill{height:100%;border-radius:3px;transition:width .5s ease}
.hc-bar-label{font-size:11px;color:var(--color-text-muted);font-family:var(--font-data)}
.hc-footer{border-top:1px solid rgba(255,255,255,0.06);margin:8px -12px -12px;padding:8px 12px 0;margin-top:10px}
.hc-footer button{width:100%;padding:7px;background:transparent;border:none;color:var(--color-text-muted);font-size:12px;font-weight:600;cursor:pointer;transition:all var(--transition-fast);font-family:var(--font-display);border-radius:var(--radius-sm)}
.hc-footer button:hover{background:rgba(201,168,76,0.08);color:var(--color-accent-light)}
.hc.completado .hc-footer button{color:var(--color-accent)}
.hc.completado .hc-footer button:hover{background:rgba(201,168,76,0.1)}

/* ─── STREAK CARD ─── */
.streak-card{background:var(--color-bg-surface);border:1px solid var(--color-border);border-radius:var(--radius-md);padding:var(--space-3);text-align:center;margin-bottom:var(--space-3)}
.streak-label{font-size:11px;color:var(--color-text-muted);font-family:var(--font-data);letter-spacing:0.5px;margin-bottom:var(--space-1)}
.streak-number{display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:4px}
.streak-number span{font-size:48px;font-weight:600;font-family:var(--font-data);color:var(--color-accent);line-height:1}
.streak-sub{font-size:13px;color:var(--color-text-muted);margin-bottom:var(--space-2)}
.streak-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.streak-stat{background:var(--color-bg-base);border-radius:var(--radius-sm);padding:10px;border:1px solid var(--color-border)}
.streak-stat-label{font-size:11px;color:var(--color-text-muted);margin-bottom:4px}
.streak-stat-val{font-size:14px;font-family:var(--font-data);color:var(--color-text-main)}
.streak-stat-val.gold{color:var(--color-accent)}

/* ─── QUICK REGISTER ─── */
.qr-card{background:var(--color-bg-surface);border:1px solid var(--color-border);border-radius:var(--radius-md);padding:var(--space-3);margin-bottom:var(--space-3)}
.qr-title{font-size:14px;font-weight:600;display:flex;align-items:center;gap:8px;color:var(--color-text-main);margin-bottom:var(--space-2)}
.qr-field{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:10px}
.qr-field label{font-size:12px;color:var(--color-text-muted);min-width:60px}
.qr-field input,.qr-field select{flex:1;background:var(--color-bg-base);border:1px solid var(--color-border);color:var(--color-text-main);border-radius:var(--radius-sm);padding:8px 10px;font-size:13px;font-family:var(--font-display)}
.qr-field input:focus,.qr-field select:focus{border-color:var(--color-accent-dim);outline:none;box-shadow:0 0 0 2px rgba(201,168,76,0.15)}
.qr-btn{width:100%;padding:8px;border-radius:var(--radius-sm);border:1px solid var(--btn-border);background:var(--btn-bg);color:var(--btn-text);font-size:13px;font-weight:600;cursor:pointer;transition:all var(--transition-fast);font-family:var(--font-display)}
.qr-btn:hover{border-color:var(--btn-hover-border);box-shadow:var(--btn-hover-shadow);background:var(--btn-hover-bg)}

/* ─── FINANCE CARDS ─── */
.finance-card{background:var(--color-bg-surface);border:1px solid var(--color-border);border-radius:var(--radius-md);padding:var(--space-3)}
.finance-title{font-size:14px;font-weight:600;display:flex;align-items:center;gap:8px;color:var(--color-text-main);margin-bottom:var(--space-2)}
.finance-bar{height:8px;border-radius:4px;overflow:hidden;background:var(--color-bg-base);border:1px solid var(--color-border);margin-bottom:4px}
.finance-bar-fill{height:100%;border-radius:4px;background:var(--color-accent)}
.finance-labels{display:flex;justify-content:space-between;font-size:11px;color:var(--color-text-muted);font-family:var(--font-data);margin-bottom:4px}
.finance-amount{font-size:24px;font-weight:600;font-family:var(--font-data);color:var(--color-accent);margin-bottom:var(--space-2)}
.finance-row{display:flex;justify-content:space-between;font-size:13px;padding:4px 0}
.finance-row-label{color:var(--color-text-muted)}
.finance-row-val{font-family:var(--font-data)}
.finance-row-val.positive{color:var(--color-success)}
.finance-row-val.negative{color:var(--color-danger)}
.finance-urgent{display:flex;align-items:flex-start;gap:8px;margin-top:var(--space-2);padding-top:var(--space-2);border-top:1px solid var(--color-border)}
.finance-urgent-text{font-family:var(--font-data);font-size:15px;color:var(--color-accent);line-height:1.3}

/* ─── DONUTS ─── */
.donuts-wrap{display:flex;align-items:flex-end;justify-content:space-between;gap:8px;flex-wrap:wrap;padding:var(--space-2) 0}

/* ─── HEATMAP ─── */
.heat-wrap{display:flex;gap:12px;padding:var(--space-2);overflow-x:auto}
.heat-days{display:flex;flex-direction:column;gap:4px;padding-top:2px}
.heat-day{height:16px;font-size:10px;line-height:16px;color:var(--color-text-muted)}
.heat-weeks{display:flex;gap:4px}
.heat-week{display:flex;flex-direction:column;gap:4px}
.heat-cell{width:16px;height:16px;border-radius:3px;border:1px solid var(--color-border);cursor:pointer;transition:transform .15s}
.heat-cell:hover{transform:scale(1.25)}
.heat-legend{display:flex;align-items:flex-end;gap:6px;margin-left:auto;align-self:flex-end;padding-bottom:1px}
.heat-legend-text{font-size:10px;color:var(--color-text-muted)}

/* ─── ACTIONS ─── */
.actions-card{background:var(--color-bg-surface);border:1px solid var(--color-border);border-radius:var(--radius-md);padding:var(--space-3)}
.actions-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.action-btn{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:12px 8px;background:var(--color-bg-base);border:1px solid var(--color-border);border-radius:var(--radius-sm);cursor:pointer;transition:all var(--transition-fast);color:var(--color-text-main);font-size:11px;text-align:center;line-height:1.2}
.action-btn:hover{background:var(--color-bg-raised);border-color:rgba(201,168,76,0.3)}
.action-btn-icon{font-size:20px}

/* ─── LOADING SPINNER ─── */
.loading-overlay{position:fixed;inset:0;background:rgba(13,27,42,0.95);display:flex;align-items:center;justify-content:center;z-index:9999}
.loading-inner{display:flex;flex-direction:column;align-items:center}
.spinner-outer{position:relative;width:80px;height:80px}
.spinner-ring{position:absolute;inset:0;border:4px solid rgba(201,168,76,0.2);border-radius:50%}
.spinner-ring-anim{position:absolute;inset:8px;border:4px solid transparent;border-top-color:var(--color-accent);border-radius:50%;animation:spin 1s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.ping-ring{position:absolute;inset:0;border:4px solid var(--color-accent);border-radius:50%;animation:ping 2s cubic-bezier(0,0,0.2,1) infinite;opacity:0}
@keyframes ping{0%{transform:scale(1);opacity:0.5}100%{transform:scale(1.5);opacity:0}}
.loading-text{margin-top:16px;color:var(--color-accent);font-family:var(--font-data);font-size:12px;letter-spacing:2px}

/* ─── SECTION TITLE ─── */
.section-title{font-size:20px;font-weight:600;margin-bottom:16px;display:flex;align-items:center;gap:8px;color:var(--color-text-main)}

/* ─── MOVEMENTS ─── */
.mov-item{display:flex;align-items:center;justify-content:space-between;padding:8px;border-radius:var(--radius-sm);transition:background var(--transition-fast)}
.mov-item:hover{background:var(--color-bg-raised)}
.mov-left{display:flex;align-items:center;gap:8px}
.mov-icon{font-size:16px}
.mov-desc{font-size:13px;color:var(--color-text-main)}
.mov-right{text-align:right}
.mov-amount{font-size:13px;font-family:var(--font-data)}
.mov-amount.positive{color:var(--color-success)}
.mov-amount.negative{color:var(--color-danger)}
.mov-when{font-size:10px;color:var(--color-text-muted)}

/* ─── TABS ─── */
.stTabs [data-baseweb="tab-list"]{background:var(--color-bg-base);padding:4px;border-radius:var(--radius-sm);gap:4px;border:1px solid var(--color-border)}
.stTabs [data-baseweb="tab"]{font-size:13px;font-weight:500;color:var(--color-text-muted);border-radius:4px;padding:6px 16px;transition:all var(--transition-fast)}
.stTabs [data-baseweb="tab"][aria-selected="true"]{background:var(--color-bg-raised);color:var(--color-accent)}
.stTabs [data-baseweb="tab"]:hover{color:var(--color-text-main)}
.stTabs [data-baseweb="tab-border"]{display:none}

/* ─── MISC ─── */
.stAlert{background:var(--color-bg-surface)!important;border:1px solid var(--color-border)!important;border-left:3px solid var(--color-accent-dim)!important;color:var(--color-text-main)!important;border-radius:var(--radius-sm)!important}
.stAlert p{color:var(--color-text-main)!important}

@media(max-width:768px){
.main>div{padding:12px}
.hero-pct{font-size:36px}
}
</style>
""", unsafe_allow_html=True)

# ─── LOADING ─────────────────────────────────────────────────────────────────

if 'loaded' not in st.session_state:
    st.markdown("""
    <div class="loading-overlay" id="loading-overlay">
        <div class="loading-inner">
            <div class="spinner-outer">
                <div class="spinner-ring"></div>
                <div class="ping-ring"></div>
                <div class="spinner-ring-anim"></div>
                <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;">
                    <span style="font-size:28px;">⚡</span>
                </div>
            </div>
            <div class="loading-text">CARGANDO SISTEMA</div>
        </div>
    </div>
    <script>
    setTimeout(function(){
        var el = document.getElementById('loading-overlay');
        if(el) el.style.display = 'none';
    }, 1200);
    </script>
    """, unsafe_allow_html=True)
    st.session_state.loaded = True

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
fecha_corta = hoy.strftime('%d/%m/%Y')

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

# ─── STREAK ──────────────────────────────────────────────────────────────────

streak = 0
if total_h > 0 and not registros.empty:
    fd = registros.groupby('fecha')['completado'].sum().reset_index()
    fd = fd[fd['completado'] == total_h]
    fs = set(fd['fecha'].tolist())
    c = hoy - datetime.timedelta(days=1)
    while str(c) in fs:
        streak += 1
        c -= datetime.timedelta(days=1)

def best_streak():
    if registros.empty:
        return 0
    best = cur = 0
    for d in sorted(registros['fecha'].unique()):
        day = registros[registros['fecha'] == d]
        if int(day['completado'].sum()) == total_h:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best

def avg_7d():
    if registros.empty:
        return 0
    vals = []
    for i in range(7):
        d = str(hoy - datetime.timedelta(days=i))
        day = registros[registros['fecha'] == d]
        vals.append(int(day['completado'].sum()) / total_h if total_h > 0 and not day.empty else 0)
    return int(sum(vals) / len(vals) * 100)

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
        'ejercicio': '🏋️', 'gym': '🏋️', 'gimnasio': '🏋️', 'entrenamiento': '🏋️', 'running': '🏃',
        'lectura': '📚', 'leer': '📚', 'reading': '📚', 'libro': '📚',
        'meditación': '🧘', 'meditacion': '🧘', 'meditate': '🧘',
        'agua': '💧', 'water': '💧',
        'diario': '📝', 'journal': '📝',
        'ingles': '🇬🇧', 'english': '🇬🇧', 'inglés': '🇬🇧',
        'guitarra': '🎸', 'music': '🎸', 'música': '🎸',
        'dios': '🙏', 'biblia': '📖',
        'facultad': '🎓', 'uni': '🎓', 'estudio': '📖', 'universidad': '🎓',
        'dropshipping': '📦', 'negocio': '💼',
        'recreativo': '🎮', 'ocio': '🎮', 'recreacion': '🎮',
        'programar': '💻', 'codigo': '💻',
    }
    for k, v in m.items():
        if k in n:
            return v
    return '📌'

# ─── SVG BUILDERS ────────────────────────────────────────────────────────────

def svg_donut(pct, size, label, is_today=False):
    stroke = 5 if size < 70 else 7
    r = (size - stroke) / 2
    c = 2 * 3.14159 * r
    offset = c - (min(pct, 100) / 100) * c
    if pct >= 100:
        color = "#C9A84C"
    elif pct > 0:
        color = "#E8C97A"
    else:
        color = "#243B55"
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
        <div style="width:{size}px;height:{size}px;position:relative;">
            <svg width="{size}" height="{size}" style="transform:rotate(-90deg);">
                <circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="#1E3050" stroke-width="{stroke}"/>
                <circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke}"
                    stroke-dasharray="{c}" stroke-dashoffset="{offset}" stroke-linecap="round"
                    style="transition:stroke-dashoffset 0.6s ease;"/>
            </svg>
            <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;">
                <span style="font-family:'JetBrains Mono',monospace;font-weight:600;color:#F0E6CC;font-size:{14 if not is_today else 11}px;">{pct}%</span>
            </div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:11px;color:#9BA8B5;">{label}</div>
            {f'<div style="font-size:9px;color:#C9A84C;font-family:JetBrains Mono;margin-top:2px;">HOY</div>' if is_today else ''}
        </div>
    </div>"""

def heat_color(pct):
    if pct <= 0: return "#0D1B2A"
    if pct < 40: return "#1A2D45"
    if pct < 75: return "#8B6914"
    return "#C9A84C"

def render_heatmap_html(cells):
    weeks = [cells[i:i+7] for i in range(0, len(cells), 7)]
    day_labels = ["L", "M", "M", "J", "V", "S", "D"]
    html = '<div class="heat-wrap">'
    html += '<div class="heat-days">' + "".join(f'<div class="heat-day">{d}</div>' for d in day_labels) + '</div>'
    html += '<div class="heat-weeks">'
    for week in weeks:
        html += '<div class="heat-week">'
        for cell in week:
            title = f"{cell['date']} · {cell['pct']}%"
            if cell.get('detalle'):
                title += f" · {cell['detalle']}"
            html += f'<div class="heat-cell" title="{title}" style="background:{heat_color(cell["pct"])};"></div>'
        html += '</div>'
    html += '</div>'
    html += '<div class="heat-legend">'
    html += '<span class="heat-legend-text">menos</span>'
    for c in ["#0D1B2A", "#1A2D45", "#8B6914", "#C9A84C"]:
        html += f'<div style="width:12px;height:12px;border-radius:3px;border:1px solid #1E3050;background:{c};"></div>'
    html += '<span class="heat-legend-text">más</span>'
    html += '</div></div>'
    return html

# ─── HEADER ──────────────────────────────────────────────────────────────────

streak_icon = "🔥"
st.markdown(f"""
<div class="app-header">
    <div class="app-brand">
        <span style="font-size:22px;">⚡</span>
        <span>SISTEMA DE ENFOQUE</span>
    </div>
    <div class="app-actions">
        <span class="app-date">{fecha_label}</span>
        {'<span class="app-streak">🔥 '+str(streak)+' días de racha</span>' if streak > 0 else ''}
    </div>
</div>
""", unsafe_allow_html=True)

# ─── LAYOUT ──────────────────────────────────────────────────────────────────

col_main, col_right = st.columns([7, 3])

with col_main:

    # ─── HERO ─────────────────────────────────────────────────────────────────

    if total_h > 0:
        hh = "".join(
            f'<span class="hero-habit">{emoji(r["nombre"])} {r["nombre"]} {"✅" if r["id"] in completados_ids else "⬜"}</span>'
            for _, r in habitos.iterrows()
        )
        st.markdown(f"""
        <div class="hero-card with-accent">
            <div class="hero-header">
                <div class="hero-title">📊 Estado del Día</div>
                <div class="hero-badge"><div class="hero-badge-dot"></div>LIVE</div>
            </div>
            <div class="hero-body">
                <div class="hero-pct">{pct_hoy}%</div>
                <div class="hero-bar"><div class="hero-bar-fill" style="width:{pct_hoy}%"></div></div>
                <div class="hero-meta">{completados_hoy} de {total_h} hábitos · {completados_hoy} completados · <span style="color:#C9A84C;">{streak} días</span></div>
                <div class="hero-habits">{hh}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="hero-card with-accent">
            <div class="hero-header">
                <div class="hero-title">📊 Estado del Día</div>
            </div>
            <div class="hero-body">
                <div class="hero-meta">Agregá tu primer hábito desde el panel lateral →</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ─── HABIT CARDS ─────────────────────────────────────────────────────────

    st.markdown("<div class='section-title'>✅ Registro de hoy</div>", unsafe_allow_html=True)

    if not habitos.empty:
        ncols = min(4, len(habitos))
        extra = len(habitos) % ncols if len(habitos) > ncols else 0
        cols = st.columns(ncols)
        for i, (_, r) in enumerate(habitos.iterrows()):
            with cols[i % ncols]:
                hid = r['id']
                ya = hid in completados_ids
                hs = habit_streak(hid)
                status = "completado" if ya else "sin-registrar"
                badge_label = "COMPLETADO" if ya else "PENDIENTE"
                badge_color = "#5FB57A" if ya else "#9BA8B5"
                badge_bg = "rgba(95,181,122,0.15)" if ya else "rgba(155,168,181,0.12)"
                bar_color = "#C9A84C" if ya else "#243B55"
                bar_pct = 100 if ya else 0
                metric_val = "🔥 " + str(hs) + "d" if hs > 0 else "—"

                st.markdown(f"""
                <div class="hc {status}">
                    <div class="hc-top">
                        <div class="hc-icon-box">{emoji(r['nombre'])}</div>
                        <div class="hc-name">{r['nombre']}</div>
                    </div>
                    <div class="hc-badge" style="color:{badge_color};background:{badge_bg};">{badge_label}</div>
                    <div class="hc-metric">
                        <span class="hc-metric-val">{metric_val}</span>
                        <span class="hc-metric-label">racha</span>
                    </div>
                    <div class="hc-bar"><div class="hc-bar-fill" style="width:{bar_pct}%;background:{bar_color};"></div></div>
                    <div class="hc-bar-label">{bar_pct}%</div>
                    <div class="hc-footer">
                """, unsafe_allow_html=True)

                if st.button("✓ Completado" if ya else "Marcar", key=f"h_{hid}", width='stretch'):
                    if hid in completados_ids:
                        conn.execute("DELETE FROM registros WHERE habito_id=? AND fecha=?", (hid, fhs))
                    else:
                        conn.execute("INSERT INTO registros (habito_id,completado,fecha) VALUES (?,1,?)", (hid, fhs))
                    conn.commit()
                    st.cache_data.clear()
                    st.session_state.rev += 1
                    st.rerun()

                st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="stAlert"><p>No hay hábitos todavía. Agregá uno desde el panel lateral.</p></div>', unsafe_allow_html=True)

    # ─── TABS ─────────────────────────────────────────────────────────────────

    st.markdown("<div class='section-title'>📈 Visualizaciones</div>", unsafe_allow_html=True)

    tab_semana, tab_matriz, tab_tendencia = st.tabs(["Semana", "Matriz 30 días", "Tendencia"])

    with tab_semana:
        ult7 = [(hoy - datetime.timedelta(days=i)) for i in range(6, -1, -1)]
        donuts_html = '<div class="donuts-wrap">'
        for i, ft in enumerate(ult7):
            fs = str(ft)
            c = 0
            if not registros.empty:
                dd = registros[registros['fecha'] == fs]
                c = int(dd['completado'].sum()) if not dd.empty else 0
            v = int((c / total_h * 100) if total_h > 0 else 0)
            today = (i == 6)
            dia_es = ['Vie', 'Sáb', 'Dom', 'Lun', 'Mar', 'Mié', 'Jue'][ft.weekday()]
            donuts_html += svg_donut(v, 96 if today else 56, dia_es, today)
        donuts_html += '</div>'
        if total_h > 0:
            st.markdown(donuts_html, unsafe_allow_html=True)
        else:
            st.markdown('<div class="stAlert"><p>Registrá hábitos para ver tu consistencia semanal.</p></div>', unsafe_allow_html=True)

    with tab_matriz:
        if not registros.empty and not habitos.empty:
            dates = sorted(registros['fecha'].unique())
            cells = []
            for dt in dates:
                day = registros[registros['fecha'] == dt]
                c = int(day['completado'].sum())
                pct = int(c / total_h * 100) if total_h > 0 else 0
                detalle = " · ".join(
                    f'{habitos[habitos["id"]==hid]["nombre"].values[0]}'
                    for hid in day['habito_id'].tolist()
                )
                cells.append({"date": dt, "pct": pct, "detalle": detalle})
            if cells:
                st.markdown(f'<div style="background:var(--color-bg-base);border-radius:var(--radius-md);border:1px solid var(--color-border);">{render_heatmap_html(cells)}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="stAlert"><p>Completá algunos hábitos para ver tu matriz.</p></div>', unsafe_allow_html=True)

    with tab_tendencia:
        if not registros.empty and total_h > 0:
            trend = registros.groupby('fecha')['completado'].mean().reset_index()
            trend['pct'] = (trend['completado'] * 100).astype(int)
            fig = go.Figure(go.Scatter(
                x=trend['fecha'], y=trend['pct'], mode='lines',
                line=dict(color='#C9A84C', width=2),
                fill='tozeroy', fillcolor='rgba(201,168,76,0.15)',
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=0, b=0), height=250,
                xaxis=dict(showgrid=False, tickfont=dict(size=10, color='#9BA8B5', family='JetBrains Mono')),
                yaxis=dict(showgrid=False, range=[0, 100], tickfont=dict(size=10, color='#9BA8B5', family='JetBrains Mono'), tickvals=[0, 25, 50, 75, 100]),
                hovermode='x unified',
            )
            fig.update_traces(hovertemplate='%{y}%<extra></extra>')
            st.plotly_chart(fig, width='stretch', key=f"trend_{st.session_state.rev}")
        else:
            st.markdown('<div class="stAlert"><p>Completá hábitos para ver tu tendencia.</p></div>', unsafe_allow_html=True)

    # ─── FINANCE ─────────────────────────────────────────────────────────────

    try:
        metas = pd.read_sql_query("SELECT * FROM metas WHERE completada=0 ORDER BY fecha_fin LIMIT 1", conn)
        if not metas.empty:
            m = metas.iloc[0]
            rest = float(m['monto_meta']) - float(m['monto_actual'])
            ff = pd.to_datetime(m['fecha_fin'])
            dr = (ff - pd.Timestamp.today()).days
            if dr > 0:
                d = rest / dr
                meta_pct = min(float(m['monto_actual']) / float(m['monto_meta']) * 100, 100)
                st.markdown(f"""
                <div class="finance-card" style="margin-top:20px;">
                    <div class="finance-title">💰 Meta ${float(m['monto_meta']):.0f} USD</div>
                    <div class="finance-labels"><span>$0</span><span>${float(m['monto_meta']):.0f}</span></div>
                    <div class="finance-bar"><div class="finance-bar-fill" style="width:{meta_pct}%;"></div></div>
                    <div class="finance-amount">${float(m['monto_actual']):.2f}</div>
                    <div class="finance-row"><span class="finance-row-label">Ingresos este mes</span><span class="finance-row-val positive">—</span></div>
                    <div class="finance-row"><span class="finance-row-label">Gastos este mes</span><span class="finance-row-val negative">—</span></div>
                    <div class="finance-urgent">
                        <span style="font-size:20px;">⚡</span>
                        <span class="finance-urgent-text">Necesitás ${d:.2f}/día para llegar en tiempo</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    except Exception:
        pass

with col_right:

    # ─── STREAK CARD ─────────────────────────────────────────────────────────

    st.markdown(f"""
    <div class="streak-card">
        <div class="streak-label">RACHA ACTUAL</div>
        <div class="streak-number">
            <span style="font-size:24px;">🔥</span>
            <span>{streak}</span>
        </div>
        <div class="streak-sub">días consecutivos</div>
        <div class="streak-grid">
            <div class="streak-stat">
                <div class="streak-stat-label">Mejor racha</div>
                <div class="streak-stat-val">{best_streak()} días</div>
            </div>
            <div class="streak-stat">
                <div class="streak-stat-label">Promedio 7d</div>
                <div class="streak-stat-val gold">{avg_7d()}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── QUICK REGISTER ─────────────────────────────────────────────────────

    st.markdown("""
    <div class="qr-card">
        <div class="qr-title">📝 Registro Rápido</div>
        <form id="quick-form" onsubmit="return false;">
            <div class="qr-field">
                <label>Hábito</label>
                <select>
                    <option>Seleccionar...</option>
                </select>
            </div>
            <div class="qr-field">
                <label>Horas</label>
                <input type="number" step="0.25" min="0" value="0.5">
            </div>
            <div class="qr-field">
                <label>Nota</label>
                <input placeholder="Opcional">
            </div>
            <button type="submit" class="qr-btn">Registrar</button>
        </form>
    </div>
    """, unsafe_allow_html=True)

    # ─── ACTIONS ─────────────────────────────────────────────────────────────

    st.markdown(f"""
    <div class="actions-card">
        <div class="qr-title" style="margin-bottom:12px;">⚡ Acciones</div>
        <div class="actions-grid">
            <div class="action-btn" onclick="alert('Registrar hábitos desde las cards principales')"><span class="action-btn-icon">✅</span>Registrar hoy</div>
            <div class="action-btn" onclick="alert('Agregar desde el panel lateral')"><span class="action-btn-icon">💰</span>Agregar ingreso</div>
            <div class="action-btn" onclick="document.querySelector('[data-baseweb=\\'tab\\']:nth-child(2)')?.click()"><span class="action-btn-icon">📊</span>Ver matriz</div>
            <div class="action-btn" onclick="alert('Usar el panel lateral')"><span class="action-btn-icon">⚙️</span>Editar hábitos</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("<div style='font-size:20px;font-weight:700;color:#C9A84C;margin-bottom:20px;letter-spacing:0.3px;display:flex;align-items:center;gap:8px;'>⚡ ENFOQUE</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:14px;font-weight:600;margin-bottom:12px;color:#F0E6CC;'>⚙️ Gestión</div>", unsafe_allow_html=True)
    nuevo = st.text_input("Nuevo hábito", placeholder="Nombre del hábito", label_visibility="collapsed")
    if st.button("Guardar", width='stretch'):
        if nuevo:
            conn.execute("INSERT INTO habitos (nombre) VALUES (?)", (nuevo,))
            conn.commit()
            st.cache_data.clear()
            st.session_state.rev += 1
            st.rerun()

    st.markdown("<hr style='border-color:#1E3050;margin:20px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px;color:#9BA8B5;text-align:center;'>Sistema de Enfoque v4 · Navy + Gold</p>", unsafe_allow_html=True)

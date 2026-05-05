import streamlit as st
import sqlite3
import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px

# 1. Configuración de la página (Fuerza el layout ancho)
st.set_page_config(page_title="Sistema de Enfoque", page_icon="🎯", layout="wide")

# 2. CSS INYECTADO: Aquí es donde sucede la magia visual
st.markdown("""
    <style>
    /* Fondo con degradado para dar profundidad */
    .stApp {
        background: radial-gradient(circle at 20% 20%, #1a1c24 0%, #0e1117 100%);
        color: #c9d1d9;
    }

    /* Títulos con gradiente */
    h1, h2, h3 {
        background: linear-gradient(90deg, #39d353, #2ea043);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }

    /* TARJETAS DE MÉTRICAS: El cambio más grande */
    div[data-testid="stMetric"] {
        background-color: #1c2128 !important;
        border: 1px solid #30363d !important;
        padding: 15px !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #39d353 !important;
        transform: translateY(-5px);
    }

    div[data-testid="stMetricValue"] {
        color: #39d353 !important;
    }

    /* Barra de progreso personalizada */
    .stProgress > div > div > div > div {
        background-color: #39d353 !important;
    }

    /* Estilo para los botones */
    div.stButton > button {
        background-color: #21262d !important;
        border-radius: 8px !important;
        border: 1px solid #30363d;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #39d353 !important;
        color: #39d353 !important;
    }

    /* Matriz de Hábitos / Dataframes */
    .stDataFrame {
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def conectar():
    conn = sqlite3.connect('sistema_enfoque.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# --- DATA ---
def obtener_datos():
    conn = conectar()
    habitos = pd.read_sql_query("SELECT * FROM habitos", conn)
    registros = pd.read_sql_query("SELECT * FROM registros", conn)
    conn.close()
    return habitos, registros

habitos, registros = obtener_datos()

# --- LAYOUT ---
st.title("🚀 Panel de Alto Rendimiento")

# Row 1: Metricas
if not habitos.empty:
    c1, c2, c3 = st.columns(3)
    total_h = len(habitos)
    # Hoy (simplificado para el ejemplo)
    completados_hoy = registros[registros['fecha'] == str(datetime.date.today())]['completado'].sum()
    pct_hoy = int((completados_hoy / total_h * 100) if total_h > 0 else 0)

    c1.metric("Hábitos Totales", total_h)
    c2.metric("Completados Hoy", completados_hoy)
    with c3:
        st.write("Avance Diario")
        st.progress(pct_hoy / 100)
        st.caption(f"{pct_hoy}% del objetivo")

st.markdown("---")

# --- SECCIÓN DE REGISTRO DIARIO (CHECK-IN) ---
st.subheader("✅ Registro de hoy")
if not habitos.empty:
    # Creamos una columna para cada hábito
    cols_check = st.columns(len(habitos))
    fecha_hoy = str(datetime.date.today())
    
    # Obtenemos los IDs de los hábitos ya completados hoy
    completados_ids = registros[registros['fecha'] == fecha_hoy]['habito_id'].tolist()

    for i, (idx, row) in enumerate(habitos.iterrows()):
        with cols_check[i]:
            ya_completado = row['id'] in completados_ids
            label = f"✓ {row['nombre']}" if ya_completado else row['nombre']
            
            if st.button(label, key=f"check_{row['id']}", width="stretch"):
                conn = conectar()
                if ya_completado:
                    # Si ya estaba, lo quitamos (Toggle)
                    conn.execute("DELETE FROM registros WHERE habito_id = ? AND fecha = ?", (row['id'], fecha_hoy))
                else:
                    # Si no estaba, lo registramos
                    conn.execute("INSERT INTO registros (habito_id, completado, fecha) VALUES (?, 1, ?)", (row['id'], fecha_hoy))
                conn.commit()
                conn.close()
                st.rerun()

# Row 2: Graficos Avanzados
col_l, col_r = st.columns([2, 1])

with col_l:
    st.subheader("📈 Tendencia de Cumplimiento")
    if not registros.empty:
        df_trend = registros.groupby('fecha')['completado'].mean().reset_index()
        fig = px.area(df_trend, x='fecha', y='completado', line_shape='spline',
                      color_discrete_sequence=['#39d353'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          margin=dict(l=0, r=0, t=0, b=0), height=300,
                          xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        st.plotly_chart(fig, width="stretch", key="trend_chart")

with col_r:
    st.subheader("📊 Progreso Semanal")
    if not registros.empty:
        # Mostramos los últimos 7 días con datos
        df_semanal = registros.groupby('fecha')['completado'].sum().reset_index().tail(7)
        fig_bar = px.bar(df_semanal, x='fecha', y='completado', color_discrete_sequence=['#2ea043'])
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig_bar, width="stretch", key="weekly_bar_chart")

# Row 3: Donuts para días de la semana
st.subheader("🗓️ Consistencia Últimos 7 Días")
cols_donuts = st.columns(7)

# Calculamos fechas de los últimos 7 días
hoy = datetime.date.today()
ultimos_7_dias = [(hoy - datetime.timedelta(days=i)) for i in range(6, -1, -1)]

for i, col in enumerate(cols_donuts):
    fecha_target = ultimos_7_dias[i]
    fecha_str = str(fecha_target)
    
    # Calcular valor real para el donut
    datos_dia = registros[registros['fecha'] == fecha_str]
    completados = datos_dia['completado'].sum() if not datos_dia.empty else 0
    valor_pct = int((completados / total_h * 100) if total_h > 0 else 0)
    
    with col:
        fig_donut = go.Figure(go.Pie(hole=.7, values=[valor_pct, 100 - valor_pct], 
                                     marker=dict(colors=['#39d353', '#1c2128']),
                                     showlegend=False, textinfo='none'))
        fig_donut.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=120, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_donut, width="stretch", key=f"donut_chart_{i}")
        st.markdown(f"<p style='text-align:center; font-size:0.8rem;'>{fecha_target.strftime('%a %d')}</p>", unsafe_allow_html=True)

# Row 4: Matriz de Hábitos
st.subheader("📋 Matriz de Consistencia")
if not registros.empty:
    # Pivotar datos: Filas (Hábito), Columnas (Fecha)
    registros_full = registros.merge(habitos, left_on='habito_id', right_on='id')
    matrix = registros_full.pivot_table(index='nombre', columns='fecha', values='completado', aggfunc='max').fillna(0)
    
    # Estilo visual para la matriz
    def color_celdas(val):
        color = '#238636' if val == 1 else '#161b22'
        return f'background-color: {color}; color: {color}'

    st.dataframe(matrix.style.map(color_celdas), width="stretch")

# Sidebar para gestión
with st.sidebar:
    st.header("⚙️ Gestión")
    nuevo = st.text_input("Añadir nuevo reto:")
    if st.button("Guardar"):
        if nuevo:
            conn = conectar()
            conn.execute("INSERT INTO habitos (nombre) VALUES (?)", (nuevo,))
            conn.commit()
            conn.close()
            st.rerun()
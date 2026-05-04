import streamlit as st
import sqlite3
import pandas as pd
import datetime

# Configuración de la página
st.set_page_config(page_title="Sistema de Enfoque", page_icon="🎯", layout="wide")

def conectar():
    conn = sqlite3.connect('sistema_enfoque.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# --- TÍTULO Y ESTÉTICA ---
st.title("🎯 Mi Sistema de Enfoque")
st.markdown("---")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Configuración")
    nuevo_habito = st.text_input("Agregar nuevo hábito:")
    if st.button("Guardar Hábito"):
        if nuevo_habito:
            conn = conectar()
            try:
                conn.execute("INSERT INTO habitos (nombre) VALUES (?)", (nuevo_habito,))
                conn.commit()
                st.success(f"Añadido: {nuevo_habito}")
                st.rerun() # Recarga la app para mostrar el nuevo botón
            except:
                st.error("Ese hábito ya existe")
            finally:
                conn.close()

# --- CUERPO PRINCIPAL: REGISTRO DEL DÍA ---
st.subheader(f"📅 Registro para hoy: {datetime.date.today()}")
conn = conectar()
habitos = pd.read_sql_query("SELECT * FROM habitos", conn)

if not habitos.empty:
    cols = st.columns(len(habitos))
    for i, row in habitos.iterrows():
        with cols[i]:
            if st.button(f"✅ {row['nombre']}", key=f"btn_{row['id']}"):
                cursor = conn.cursor()
                cursor.execute("INSERT INTO registros (habito_id, completado) VALUES (?, 1)", (row['id'],))
                conn.commit()
                st.toast(f"¡{row['nombre']} marcado!")
                st.rerun()
else:
    st.info("Agregá hábitos en la barra lateral para empezar.")

# --- VISUALIZACIÓN ---
st.markdown("---")
st.subheader("📊 Progreso General")

query_stats = '''
    SELECT h.nombre, 
           SUM(r.completado) as cumplidos,
           COUNT(r.id) as total
    FROM habitos h
    LEFT JOIN registros r ON h.id = r.habito_id
    GROUP BY h.id
'''
stats = pd.read_sql_query(query_stats, conn)
conn.close()

if not stats.empty:
    # Calculamos porcentaje evitando división por cero
    stats['porcentaje'] = (stats['cumplidos'] / stats['total'].replace(0, 1)) * 100
    
    # --- EL PARCHE DE SEGURIDAD (Manejo de NaN) ---
    promedio_val = stats['porcentaje'].mean()
    if pd.isna(promedio_val):
        promedio_val = 0
        
    m1, m2, m3 = st.columns(3)
    
    # Métrica 1: Promedio
    m1.metric("Promedio de Enfoque", f"{int(promedio_val)}%")
    
    # Métrica 2: Hábito más constante (Manejo de error si no hay cumplidos)
    try:
        if stats['cumplidos'].sum() > 0:
            constante = stats.loc[stats['cumplidos'].idxmax(), 'nombre']
        else:
            constante = "Sin registros"
    except:
        constante = "Sin datos"
    m2.metric("Hábito más constante", constante)
    
    # Métrica 3: Días Registrados (Máximo de registros en un hábito)
    total_dias = stats['total'].max()
    m3.metric("Días Registrados", int(total_dias) if not pd.isna(total_dias) else 0)

    # Gráfico de barras
    st.bar_chart(data=stats, x='nombre', y='porcentaje', color='#4CAF50')
else:
    st.warning("Aún no hay estadísticas disponibles.")
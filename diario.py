import sqlite3
from datetime import date

def conectar():
    conexion = sqlite3.connect('sistema_enfoque.db')
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion

def registrar_dia():
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Buscamos qué hábitos tenés configurados
    cursor.execute("SELECT id, nombre FROM habitos")
    habitos = cursor.fetchall()
    
    if not habitos:
        print("No hay hábitos cargados. Usá el script 'gestionar_habitos.py' primero.")
        return

    print(f"\n=== CHECK-IN DIARIO: {date.today()} ===")
    
    # 2. Recorremos cada hábito y te preguntamos
    for habito in habitos:
        habito_id = habito[0]  # El número de ID
        nombre = habito[1]     # El texto del hábito
        
        respuesta = input(f"¿Completaste '{nombre}' hoy? (s/n): ").strip().lower()
        
        # Transformamos tu 's' o 'n' en un 1 o 0 (Booleanos en SQLite)
        completado = 1 if respuesta == 's' else 0
        
        # 3. Guardamos tu respuesta en la tabla 'registros'
        cursor.execute('''
            INSERT INTO registros (habito_id, completado) 
            VALUES (?, ?)
        ''', (habito_id, completado))
        
    # Guardamos todos los cambios juntos al final
    conn.commit()
    conn.close()
    
    print("-----------------------------------")
    print("¡Día registrado con éxito! A descansar.")

if __name__ == "__main__":
    registrar_dia()
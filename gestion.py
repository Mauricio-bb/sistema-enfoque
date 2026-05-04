import sqlite3

def conectar():
    conexion = sqlite3.connect('sistema_enfoque.db')
    # Recordá siempre activar las FK en SQLite
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion

def agregar_habito(nombre):
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Usamos parámetros (?) para evitar Inyección SQL (¡Ojo con esto para el examen!)
        cursor.execute("INSERT INTO habitos (nombre) VALUES (?)", (nombre,))
        
        conn.commit()
        print(f"✅ Hábito '{nombre}' agregado con éxito.")
    except sqlite3.IntegrityError:
        print(f"⚠️ El hábito '{nombre}' ya existe.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

def listar_habitos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habitos")
    habitos = cursor.fetchall()
    
    print("\n--- TUS HÁBITOS ACTUALES ---")
    for h in habitos:
        print(f"ID: {h[0]} | Nombre: {h[1]}")
    print("----------------------------\n")
    conn.close()

if __name__ == "__main__":
    while True:
        print("1. Agregar Hábito")
        print("2. Ver mis Hábitos")
        print("3. Salir")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            nuevo = input("Nombre del nuevo hábito: ")
            agregar_habito(nuevo)
        elif opcion == "2":
            listar_habitos()
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")
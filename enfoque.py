import sqlite3

def inicializar_db():
    conexion = None
    try:
        conexion = sqlite3.connect('sistema_enfoque.db')
        cursor = conexion.cursor()

        # 1. Fundamental en SQLite: Activar el soporte para Foreign Keys
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Creamos la tabla de hábitos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habitos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            )
        ''')

        # Creamos la tabla de registros diarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habito_id INTEGER,
                fecha DATE DEFAULT (DATE('now', 'localtime')),
                completado INTEGER DEFAULT 0,
                FOREIGN KEY (habito_id) REFERENCES habitos (id)
            )
        ''')

        conexion.commit()
        print("¡Base de datos y tablas creadas con éxito!")

    # 2. Manejo de Errores
    except sqlite3.Error as error:
        print(f"Ocurrió un error al crear la base de datos: {error}")

    # 3. Cierre seguro
    finally:
        if conexion:
            conexion.close()

if __name__ == "__main__":
    inicializar_db()

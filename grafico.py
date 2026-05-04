import sqlite3
import matplotlib.pyplot as plt

def mostrar_grafico():
    conn = sqlite3.connect('sistema_enfoque.db')
    cursor = conn.cursor()

    # Traemos el nombre y el porcentaje de cumplimiento
    query = '''
        SELECT h.nombre, 
               (CAST(SUM(r.completado) AS FLOAT) / COUNT(r.id)) * 100
        FROM habitos h
        LEFT JOIN registros r ON h.id = r.habito_id
        GROUP BY h.id
    '''
    cursor.execute(query)
    datos = cursor.fetchall()
    conn.close()

    nombres = [d[0] for d in datos]
    porcentajes = [d[1] if d[1] is not None else 0 for d in datos]

    # Configuramos el gráfico estilo "Sistema de Enfoque"
    plt.figure(figsize=(10, 6))
    barras = plt.bar(nombres, porcentajes, color='#4CAF50') # Verde como la foto
    plt.axhline(0, color='black', linewidth=0.8)
    plt.ylim(0, 100)
    plt.ylabel('Porcentaje de Éxito (%)')
    plt.title('Mi Panel de Control de Hábitos')

    # Añadimos el número sobre la barra
    for barra in barras:
        yval = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, yval + 1, f'{int(yval)}%', ha='center')

    plt.show()

if __name__ == "__main__":
    mostrar_grafico()
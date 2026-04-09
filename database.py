import sqlite3
import pandas as pd

# Base de datos para almacenar los activos y sus datos de confiabilidad
def crear_tabla():
    """Crea la tabla de activos si no existe."""
    conn = sqlite3.connect("confiabilidad.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT NOT NULL,
            nombre TEXT NOT NULL,
            frecuencia INTEGER,
            consecuencia INTEGER,
            criticidad INTEGER,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Llamar a la función para crear la tabla al iniciar el programa
def guardar_activo(tag, nombre, frecuencia, consecuencia):
    """Inserta un nuevo activo en la base de datos."""
    criticidad = frecuencia * consecuencia
    conn = sqlite3.connect("confiabilidad.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO activos (tag, nombre, frecuencia, consecuencia, criticidad)
        VALUES (?, ?, ?, ?, ?)
    """, (tag, nombre, frecuencia, consecuencia))
    conn.commit()
    conn.close()

# Función para cargar todos los activos desde la base de datos
def cargar_activos():
    """Retorna todos los activos como un DataFrame de Pandas."""
    conn = sqlite3.connect("confiabilidad.db")
    df = pd.read_sql_query("SELECT * FROM activos", conn)
    conn.close()
    return df
import sqlite3
import pandas as pd

# Base de datos para almacenar los activos y sus datos de confiabilidad
def crear_tabla():
    """Crea las tablas de activos y AMEF si no existen."""
    conn = sqlite3.connect("confiabilidad.db")
    cursor = conn.cursor()
    
    # Tabla 1: Activos (La que ya tenías)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            frecuencia INTEGER,
            consecuencia INTEGER,
            criticidad INTEGER,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla 2: AMEF (¡Nueva!)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS amef (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_activo TEXT NOT NULL,
            funcion TEXT NOT NULL,
            falla_funcional TEXT NOT NULL,
            modo_falla TEXT NOT NULL,
            efecto TEXT NOT NULL,
            FOREIGN KEY (tag_activo) REFERENCES activos(tag) 
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
    """, (tag, nombre, frecuencia, consecuencia, criticidad))
    conn.commit()
    conn.close()

# Función para cargar todos los activos desde la base de datos
def cargar_activos():
    """Retorna todos los activos como un DataFrame de Pandas."""
    conn = sqlite3.connect("confiabilidad.db")
    df = pd.read_sql_query("SELECT * FROM activos", conn)
    conn.close()
    return df

#
def guardar_amef(tag_activo, funcion, falla_funcional, modo_falla, efecto):
    """Inserta un nuevo modo de falla asociado a un activo."""
    conn = sqlite3.connect("confiabilidad.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO amef (tag_activo, funcion, falla_funcional, modo_falla, efecto)
        VALUES (?, ?, ?, ?, ?)
    """, (tag_activo, funcion, falla_funcional, modo_falla, efecto))
    conn.commit()
    conn.close()

def cargar_amef_por_equipo(tag_activo):
    """Retorna el AMEF de un equipo específico como DataFrame."""
    conn = sqlite3.connect("confiabilidad.db")
    df = pd.read_sql_query(f"SELECT funcion, falla_funcional, modo_falla, efecto FROM amef WHERE tag_activo = '{tag_activo}'", conn)
    conn.close()
    return df
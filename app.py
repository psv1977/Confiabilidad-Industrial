import streamlit as st
from database import crear_tabla, guardar_activo, cargar_activos

# Iniciamos la base de datos al arrancar
crear_tabla()

st.title("🛡️ Confiabilidad Industrial - Registro de Activos")

# Formulario de entrada
with st.form("nuevo_activo"):
    st.subheader("Registrar Nuevo Análisis de Criticidad")
    col1, col2 = st.columns(2)
    with col1:
        tag = st.text_input("TAG del Equipo (Ej: P-101)")
        nombre = st.text_input("Nombre del Equipo")
    with col2:
        frec_falla = st.slider("Frecuencia de Falla (1-10)", 1, 10, 5)
        cons_falla = st.slider("Consecuencia (1-10)", 1, 10, 5)
    
    submit = st.form_submit_button("Guardar en Base de Datos")

if submit:
    guardar_activo(tag, nombre, frec_falla, cons_falla)
    st.success(f"✅ Activo {tag} guardado correctamente.")

# Mostrar la tabla de lo que llevamos guardado
st.divider()
st.subheader("📋 Inventario de Criticidad")
df_activos = cargar_activos()

if not df_activos.empty:
    st.dataframe(df_activos, use_container_width=True)
else:
    st.write("Aún no hay activos registrados.")
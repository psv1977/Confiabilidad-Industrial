import streamlit as st
from database import crear_tabla, guardar_activo, cargar_activos, guardar_amef, cargar_amef_por_equipo

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
st.set_page_config(page_title="Confiabilidad Industrial", layout="wide")
crear_tabla()

st.title("🛡️ Confiabilidad Industrial - Registro de Activos")

# ==========================================
# 2. INGRESO DE ACTIVOS
# ==========================================
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

# Cargamos los datos una sola vez para usarlos en toda la app
df_activos = cargar_activos()

# ==========================================
# 3. INVENTARIO Y EXPORTACIÓN
# ==========================================
st.divider()
st.subheader("📋 Inventario de Equipos Analizados")

if not df_activos.empty:
    st.dataframe(df_activos, use_container_width=True)
    
    # Botón de exportación mágica
    st.markdown("### Exportar Reporte")
    csv = df_activos.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Descargar Inventario (CSV para Excel)",
        data=csv,
        file_name="inventario_criticidad_rcm.csv",
        mime="text/csv",
    )
else:
    st.info("No hay activos registrados aún.")

# ==========================================
# 4. MATRIZ DE CRITICIDAD
# ==========================================
st.divider()
st.subheader("📊 Matriz de Riesgo / Criticidad")

if not df_activos.empty:
    tab1, tab2 = st.tabs(["Gráfico de Dispersión", "Resumen Estadístico"])
    
    with tab1:
        st.write("Visualización de activos según su Frecuencia y Consecuencia")
        st.scatter_chart(
            data=df_activos,
            x="consecuencia",
            y="frecuencia",
            color="#FF4B4B", 
            size="criticidad" 
        )
        
    with tab2:
        st.write("Métricas clave de tus activos registrados:")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Total Activos", len(df_activos))
        col_m2.metric("Criticidad Promedio", round(df_activos['criticidad'].mean(), 1))
        col_m3.metric("Criticidad Máxima", df_activos['criticidad'].max())
else:
    st.info("Agrega más activos para visualizar la matriz.")

# ==========================================
# 5. MÓDULO AMEF
# ==========================================
st.divider()
st.header("⚙️ Análisis de Modos y Efectos de Falla (AMEF)")

if not df_activos.empty:
    # Selector de equipo
    lista_tags = df_activos['tag'].tolist()
    tag_seleccionado = st.selectbox("Seleccione un equipo para analizar:", lista_tags)
    
    nombre_equipo = df_activos[df_activos['tag'] == tag_seleccionado]['nombre'].iloc[0]
    st.info(f"Analizando Activo: **{nombre_equipo}**")

    # Formulario AMEF
    with st.form("formulario_amef"):
        st.subheader("Registrar nuevo Modo de Falla")
        
        funcion = st.text_area("Función del Sistema", placeholder="Ej: Bombear agua a 50 GPM a la caldera.")
        falla_funcional = st.text_area("Falla Funcional", placeholder="Ej: No bombea agua / Bombea menos de 50 GPM.")
        
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            modo_falla = st.text_input("Modo de Falla (Causa Raíz)", placeholder="Ej: Rodamiento lado acople desgastado")
        with col_a2:
            efecto = st.text_input("Efecto de la Falla", placeholder="Ej: Parada de caldera, vibración excesiva")
            
        btn_amef = st.form_submit_button("Guardar Modo de Falla")
        
    if btn_amef:
        if funcion and falla_funcional and modo_falla and efecto:
            guardar_amef(tag_seleccionado, funcion, falla_funcional, modo_falla, efecto)
            st.success("✅ Modo de falla registrado correctamente.")
        else:
            st.warning("⚠️ Por favor, complete todos los campos del AMEF.")

    # Tabla AMEF del equipo
    st.subheader(f"📋 Registros AMEF para {tag_seleccionado}")
    df_amef = cargar_amef_por_equipo(tag_seleccionado)
    
    if not df_amef.empty:
        st.dataframe(df_amef, use_container_width=True)
    else:
        st.write("Aún no hay modos de falla registrados para este equipo.")
        
else:
    st.warning("⚠️ Debe registrar al menos un activo en la sección superior para comenzar el AMEF.")
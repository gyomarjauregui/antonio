# streamlit_app_inventario.py

import streamlit as st
import pandas as pd

# Cargar dataset
@st.cache_data
def cargar_datos():
    return pd.read_csv("dataset_inventario_consumomax.csv", parse_dates=["Fecha_Ingreso"])

df = cargar_datos()

# Configurar página
st.set_page_config(page_title="Sistema de Inventario ConsumoMax", page_icon="📦", layout="wide")

# Título principal
st.title("🧠 Sistema Inteligente de Control de Inventario - ConsumoMax")

# Filtros laterales
st.sidebar.header("🔍 Filtros de búsqueda")
almacen = st.sidebar.multiselect("Seleccionar almacén:", options=df["Almacén"].unique(), default=df["Almacén"].unique())
categoria = st.sidebar.multiselect("Seleccionar categoría:", options=df["Categoría"].unique(), default=df["Categoría"].unique())

# Aplicar filtros
df_filtrado = df[(df["Almacén"].isin(almacen)) & (df["Categoría"].isin(categoria))]

# Mostrar datos filtrados
st.subheader("📋 Inventario actual")
st.dataframe(df_filtrado, use_container_width=True)

# KPIs principales
st.subheader("📈 Indicadores rápidos")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Productos registrados", value=len(df_filtrado))
with col2:
    st.metric(label="Total de stock disponible", value=int(df_filtrado["Cantidad_Actual"].sum()))
with col3:
    st.metric(label="Productos bajo umbral mínimo", value=(df_filtrado["Cantidad_Actual"] < df_filtrado["Umbral_Mínimo"]).sum())

# Gráficos
st.subheader("📊 Distribución de Stock por Categoría")
stock_categoria = df_filtrado.groupby("Categoría")["Cantidad_Actual"].sum()
st.bar_chart(stock_categoria)

st.subheader("🏢 Distribución por Almacén")
stock_almacen = df_filtrado.groupby("Almacén")["Cantidad_Actual"].sum()
st.bar_chart(stock_almacen)

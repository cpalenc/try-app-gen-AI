#!/usr/bin/env python3
"""
Aplicación muy simplificada para consultar el histórico de la TRM en Colombia.
Esta versión es extremadamente básica para garantizar la compatibilidad.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "trm_data.csv")

# Configuración de la página
st.set_page_config(
    page_title="TRM Colombia - Histórico",
    page_icon="📈",
    layout="wide"
)

# Título de la aplicación
st.title("📊 Histórico TRM Colombia")
st.markdown("Aplicación para consultar y analizar el histórico de la Tasa Representativa del Mercado (TRM) en Colombia")

# Cargar datos
@st.cache_data
def load_data():
    try:
        data = pd.read_csv(DATA_FILE)
        # Renombrar columnas para facilitar su uso
        data.columns = ['fecha', 'trm']
        
        # Convertir la columna de fecha a datetime
        data['fecha'] = pd.to_datetime(data['fecha'], format='%Y/%m/%d')
        
        # Ordenar por fecha
        data = data.sort_values('fecha')
        
        return data
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None

data = load_data()

if data is not None:
    # Obtener rango de fechas disponibles
    min_date = data['fecha'].min().date()
    max_date = data['fecha'].max().date()
    
    # Sidebar para filtros
    st.sidebar.header("Filtros")
    
    # Filtro de fechas
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Fecha inicial", min_date, min_value=min_date, max_value=max_date)
    with col2:
        end_date = st.date_input("Fecha final", max_date, min_value=min_date, max_value=max_date)
    
    # Filtrar datos
    filtered_data = data[(data['fecha'].dt.date >= start_date) & (data['fecha'].dt.date <= end_date)]
    
    # Mostrar estadísticas
    st.header("📝 Estadísticas")
    
    if not filtered_data.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("TRM Mínima", f"${filtered_data['trm'].min():.2f}")
            st.metric("TRM Promedio", f"${filtered_data['trm'].mean():.2f}")
        
        with col2:
            st.metric("TRM Máxima", f"${filtered_data['trm'].max():.2f}")
            st.metric("TRM Mediana", f"${filtered_data['trm'].median():.2f}")
        
        with col3:
            st.metric("Valor Inicial", f"${filtered_data.iloc[0]['trm']:.2f}")
            st.metric("Desviación Estándar", f"${filtered_data['trm'].std():.2f}")
        
        with col4:
            st.metric("Valor Final", f"${filtered_data.iloc[-1]['trm']:.2f}")
            change = filtered_data.iloc[-1]['trm'] - filtered_data.iloc[0]['trm']
            change_pct = (filtered_data.iloc[-1]['trm'] / filtered_data.iloc[0]['trm'] - 1) * 100
            st.metric("Variación", f"{change_pct:.2f}%", delta=f"{change:.2f}")
    
        # Gráfico principal
        st.header("📈 Gráfico de la TRM")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(filtered_data['fecha'], filtered_data['trm'])
        ax.set_title('Histórico TRM Colombia')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('TRM (COP/USD)')
        ax.grid(True)
        
        # Mostrar el gráfico
        st.pyplot(fig)
        
        # Tabla de datos
        st.header("📋 Datos")
        st.dataframe(filtered_data)
    else:
        st.warning("No hay datos disponibles para el rango de fechas seleccionado.")
else:
    st.error("No se pudieron cargar los datos. Por favor, verifica que el archivo de datos exista.")

# Información adicional
st.sidebar.markdown("---")
st.sidebar.markdown("### Acerca de")
st.sidebar.info("""
Esta aplicación permite consultar y analizar el histórico de la Tasa Representativa del Mercado (TRM) en Colombia.

La TRM es la cantidad de pesos colombianos por un dólar de los Estados Unidos.
""")

# Footer
st.markdown("---")
st.markdown("Desarrollado con ❤️ usando Python y Streamlit")
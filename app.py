import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from trm_data_loader import TRMDataLoader
import numpy as np
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="TRM Colombia - Histórico",
    page_icon="📈",
    layout="wide"
)

# Inicializar el cargador de datos
@st.cache_resource
def get_data_loader():
    return TRMDataLoader()

trm_loader = get_data_loader()

# Título de la aplicación
st.title("📊 Histórico TRM Colombia")
st.markdown("Aplicación para consultar y analizar el histórico de la Tasa Representativa del Mercado (TRM) en Colombia")

# Sidebar para filtros
st.sidebar.header("Filtros")

# Obtener rango de fechas disponibles
min_date = trm_loader.data['fecha'].min().date()
max_date = trm_loader.data['fecha'].max().date()

# Filtro de fechas
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Fecha inicial", min_date, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("Fecha final", max_date, min_value=min_date, max_value=max_date)

# Botones de acceso rápido para rangos de fechas
st.sidebar.markdown("### Rangos predefinidos")
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("Último mes"):
        end_date = max_date
        start_date = end_date - timedelta(days=30)
        st.experimental_rerun()
    
    if st.button("Último año"):
        end_date = max_date
        start_date = datetime(end_date.year - 1, end_date.month, end_date.day).date()
        st.experimental_rerun()

with col2:
    if st.button("Últimos 3 meses"):
        end_date = max_date
        start_date = end_date - timedelta(days=90)
        st.experimental_rerun()
    
    if st.button("Últimos 5 años"):
        end_date = max_date
        start_date = datetime(end_date.year - 5, end_date.month, end_date.day).date()
        st.experimental_rerun()

# Obtener datos filtrados
filtered_data = trm_loader.get_data_range(start_date, end_date)

# Mostrar estadísticas
st.header("📝 Estadísticas")
stats = trm_loader.get_statistics(start_date, end_date)

if stats:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("TRM Mínima", f"${stats['min']:.2f}")
        st.metric("TRM Promedio", f"${stats['avg']:.2f}")
    
    with col2:
        st.metric("TRM Máxima", f"${stats['max']:.2f}")
        st.metric("TRM Mediana", f"${stats['median']:.2f}")
    
    with col3:
        st.metric("Valor Inicial", f"${stats['start_value']:.2f}")
        st.metric("Desviación Estándar", f"${stats['std']:.2f}")
    
    with col4:
        st.metric("Valor Final", f"${stats['end_value']:.2f}")
        st.metric("Variación", f"{stats['change_pct']:.2f}%", 
                 delta=f"{stats['change']:.2f}")

# Gráfico principal
st.header("📈 Gráfico de la TRM")

# Opciones de visualización
chart_options = st.expander("Opciones de visualización")
with chart_options:
    col1, col2 = st.columns(2)
    
    with col1:
        show_ma = st.checkbox("Mostrar promedio móvil", value=True)
        ma_window = st.slider("Ventana del promedio móvil", 5, 100, 30)
    
    with col2:
        show_trend = st.checkbox("Mostrar línea de tendencia", value=False)
        log_scale = st.checkbox("Escala logarítmica", value=False)

# Preparar datos para el gráfico
if show_ma:
    ma_data = trm_loader.calculate_moving_average(ma_window, start_date, end_date)
else:
    ma_data = filtered_data

# Crear gráfico
fig, ax = plt.subplots(figsize=(12, 6))

# Gráfico principal
sns.lineplot(x='fecha', y='trm', data=filtered_data, ax=ax, color='blue', label='TRM')

# Añadir promedio móvil si está seleccionado
if show_ma and ma_data is not None:
    sns.lineplot(x='fecha', y=f'ma_{ma_window}', data=ma_data, ax=ax, color='red', 
                label=f'Promedio Móvil ({ma_window} días)')

# Añadir línea de tendencia si está seleccionada
if show_trend and filtered_data is not None:
    # Crear variable numérica para la regresión
    x = np.arange(len(filtered_data))
    y = filtered_data['trm'].values
    
    # Calcular la línea de tendencia
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    
    # Añadir al gráfico
    ax.plot(filtered_data['fecha'], p(x), "g--", label=f'Tendencia: {z[0]:.2f}x + {z[1]:.2f}')

# Configurar escala logarítmica si está seleccionada
if log_scale:
    ax.set_yscale('log')

# Configurar el gráfico
ax.set_title('Histórico TRM Colombia')
ax.set_xlabel('Fecha')
ax.set_ylabel('TRM (COP/USD)')
ax.grid(True)
ax.legend()

# Mostrar el gráfico
st.pyplot(fig)

# Tabla de datos
st.header("📋 Datos")
st.dataframe(filtered_data)

# Análisis de variaciones
st.header("🔍 Análisis de Variaciones")

threshold = st.slider("Umbral de variación (%)", 0.5, 5.0, 1.0, 0.1)
variations = trm_loader.find_extreme_variations(threshold, start_date, end_date)

if variations is not None and not variations.empty:
    st.write(f"Se encontraron {len(variations)} días con variaciones superiores al {threshold}%")
    
    # Crear gráfico de variaciones
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Barras para variaciones
    sns.barplot(x='fecha', y='var_pct', data=variations, ax=ax, palette='coolwarm')
    
    # Configurar el gráfico
    ax.set_title(f'Variaciones diarias superiores al {threshold}%')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Variación (%)')
    ax.grid(True, axis='y')
    
    # Rotar etiquetas del eje x
    plt.xticks(rotation=45)
    
    # Mostrar el gráfico
    st.pyplot(fig)
    
    # Mostrar tabla de variaciones
    st.dataframe(variations[['fecha', 'trm', 'var_pct']].sort_values('var_pct', ascending=False))
else:
    st.write(f"No se encontraron variaciones superiores al {threshold}%")

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
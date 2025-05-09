#!/usr/bin/env python3
"""
Aplicación simplificada para consultar el histórico de la TRM en Colombia.
Esta versión integra todas las funcionalidades en un solo archivo para facilitar la ejecución.
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date, timedelta
import streamlit as st
from typing import List, Dict, Any, Optional, Tuple

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "trm_data.csv")

# Clase para cargar y procesar datos de TRM
class TRMDataLoader:
    def __init__(self, data_path=None):
        """
        Inicializa el cargador de datos de TRM
        
        Args:
            data_path (str): Ruta al archivo CSV con datos de TRM
        """
        self.data_path = data_path or DATA_FILE
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Carga los datos desde el archivo CSV"""
        try:
            self.data = pd.read_csv(self.data_path)
            # Renombrar columnas para facilitar su uso
            self.data.columns = ['fecha', 'trm']
            
            # Convertir la columna de fecha a datetime
            self.data['fecha'] = pd.to_datetime(self.data['fecha'], format='%Y/%m/%d')
            
            # Ordenar por fecha
            self.data = self.data.sort_values('fecha')
            
            print(f"Datos cargados correctamente: {len(self.data)} registros")
            return True
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            return False
    
    def get_data_range(self, start_date=None, end_date=None):
        """
        Obtiene datos de TRM en un rango de fechas
        
        Args:
            start_date (str): Fecha inicial en formato YYYY-MM-DD
            end_date (str): Fecha final en formato YYYY-MM-DD
            
        Returns:
            DataFrame: Datos filtrados por el rango de fechas
        """
        if self.data is None:
            return None
        
        filtered_data = self.data.copy()
        
        if start_date:
            try:
                start_date = pd.to_datetime(start_date)
                filtered_data = filtered_data[filtered_data['fecha'] >= start_date]
            except:
                pass
            
        if end_date:
            try:
                end_date = pd.to_datetime(end_date)
                filtered_data = filtered_data[filtered_data['fecha'] <= end_date]
            except:
                pass
            
        return filtered_data
    
    def get_statistics(self, start_date=None, end_date=None):
        """
        Calcula estadísticas básicas para un rango de fechas
        
        Args:
            start_date (str): Fecha inicial en formato YYYY-MM-DD
            end_date (str): Fecha final en formato YYYY-MM-DD
            
        Returns:
            dict: Estadísticas calculadas
        """
        filtered_data = self.get_data_range(start_date, end_date)
        
        if filtered_data is None or filtered_data.empty:
            return None
        
        stats = {
            'min': filtered_data['trm'].min(),
            'max': filtered_data['trm'].max(),
            'avg': filtered_data['trm'].mean(),
            'median': filtered_data['trm'].median(),
            'std': filtered_data['trm'].std(),
            'count': len(filtered_data),
            'start_date': filtered_data['fecha'].min().strftime('%Y-%m-%d'),
            'end_date': filtered_data['fecha'].max().strftime('%Y-%m-%d'),
            'start_value': filtered_data.iloc[0]['trm'],
            'end_value': filtered_data.iloc[-1]['trm'],
            'change': filtered_data.iloc[-1]['trm'] - filtered_data.iloc[0]['trm'],
            'change_pct': (filtered_data.iloc[-1]['trm'] / filtered_data.iloc[0]['trm'] - 1) * 100
        }
        
        return stats
    
    def plot_trm(self, start_date=None, end_date=None, save_path=None):
        """
        Genera un gráfico de la TRM en un rango de fechas
        
        Args:
            start_date (str): Fecha inicial en formato YYYY-MM-DD
            end_date (str): Fecha final en formato YYYY-MM-DD
            save_path (str): Ruta para guardar el gráfico
            
        Returns:
            matplotlib.figure.Figure: Figura generada
        """
        filtered_data = self.get_data_range(start_date, end_date)
        
        if filtered_data is None or filtered_data.empty:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(filtered_data['fecha'], filtered_data['trm'])
        ax.set_title('Histórico TRM Colombia')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('TRM (COP/USD)')
        ax.grid(True)
        
        # Añadir anotaciones de valores mínimos y máximos
        min_idx = filtered_data['trm'].idxmin()
        max_idx = filtered_data['trm'].idxmax()
        
        ax.annotate(f'Min: {filtered_data.loc[min_idx, "trm"]:.2f}',
                    xy=(filtered_data.loc[min_idx, 'fecha'], filtered_data.loc[min_idx, 'trm']),
                    xytext=(10, -30), textcoords='offset points',
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
        
        ax.annotate(f'Max: {filtered_data.loc[max_idx, "trm"]:.2f}',
                    xy=(filtered_data.loc[max_idx, 'fecha'], filtered_data.loc[max_idx, 'trm']),
                    xytext=(10, 30), textcoords='offset points',
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
        
        if save_path:
            plt.savefig(save_path)
            
        return fig
    
    def calculate_moving_average(self, window=30, start_date=None, end_date=None):
        """
        Calcula el promedio móvil de la TRM
        
        Args:
            window (int): Tamaño de la ventana para el promedio móvil
            start_date (str): Fecha inicial en formato YYYY-MM-DD
            end_date (str): Fecha final en formato YYYY-MM-DD
            
        Returns:
            DataFrame: Datos con el promedio móvil calculado
        """
        filtered_data = self.get_data_range(start_date, end_date)
        
        if filtered_data is None or filtered_data.empty:
            return None
        
        filtered_data[f'ma_{window}'] = filtered_data['trm'].rolling(window=window).mean()
        
        return filtered_data
    
    def find_extreme_variations(self, threshold_pct=1.0, start_date=None, end_date=None):
        """
        Encuentra variaciones extremas en la TRM
        
        Args:
            threshold_pct (float): Umbral de variación porcentual
            start_date (str): Fecha inicial en formato YYYY-MM-DD
            end_date (str): Fecha final en formato YYYY-MM-DD
            
        Returns:
            DataFrame: Datos con variaciones que superan el umbral
        """
        filtered_data = self.get_data_range(start_date, end_date)
        
        if filtered_data is None or filtered_data.empty:
            return None
        
        # Calcular variación diaria
        filtered_data['var_pct'] = filtered_data['trm'].pct_change() * 100
        
        # Filtrar por umbral
        extreme_variations = filtered_data[abs(filtered_data['var_pct']) > threshold_pct].copy()
        
        return extreme_variations
    
    def get_date_range(self):
        """
        Obtiene el rango de fechas disponibles
        
        Returns:
            tuple: (fecha_minima, fecha_maxima)
        """
        if self.data is None or self.data.empty:
            return (datetime.now().date(), datetime.now().date())
        
        min_date = self.data['fecha'].min().date()
        max_date = self.data['fecha'].max().date()
        
        return (min_date, max_date)

# Función para ejecutar la aplicación web con Streamlit
def run_streamlit_app():
    """Ejecuta la aplicación web con Streamlit"""
    # Inicializar el cargador de datos
    trm_loader = TRMDataLoader()
    
    # Configuración de la página
    st.set_page_config(
        page_title="TRM Colombia - Histórico",
        page_icon="📈",
        layout="wide"
    )
    
    # Título de la aplicación
    st.title("📊 Histórico TRM Colombia")
    st.markdown("Aplicación para consultar y analizar el histórico de la Tasa Representativa del Mercado (TRM) en Colombia")
    
    # Sidebar para filtros
    st.sidebar.header("Filtros")
    
    # Obtener rango de fechas disponibles
    min_date, max_date = trm_loader.get_date_range()
    
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
            st.rerun()  # Usar st.rerun() en lugar de st.experimental_rerun()
        
        if st.button("Último año"):
            end_date = max_date
            start_date = datetime(end_date.year - 1, end_date.month, end_date.day).date()
            st.rerun()  # Usar st.rerun() en lugar de st.experimental_rerun()
    
    with col2:
        if st.button("Últimos 3 meses"):
            end_date = max_date
            start_date = end_date - timedelta(days=90)
            st.rerun()  # Usar st.rerun() en lugar de st.experimental_rerun()
        
        if st.button("Últimos 5 años"):
            end_date = max_date
            start_date = datetime(end_date.year - 5, end_date.month, end_date.day).date()
            st.rerun()  # Usar st.rerun() en lugar de st.experimental_rerun()
    
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
        ma_col = f'ma_{ma_window}'
        if ma_col in ma_data.columns:
            sns.lineplot(x='fecha', y=ma_col, data=ma_data, ax=ax, color='red', 
                        label=f'Promedio Móvil ({ma_window} días)')
    
    # Añadir línea de tendencia si está seleccionada
    if show_trend and filtered_data is not None and not filtered_data.empty:
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

# Punto de entrada principal
if __name__ == "__main__":
    run_streamlit_app()
"""
Servicios de dominio para la TRM.
"""
from datetime import date
from typing import List, Optional, Dict, Any, Tuple
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from ..models.trm import TRMData, TRMStatistics, TRMVariation, TRMMovingAverage


class TRMService:
    """
    Servicio de dominio para operaciones con datos de TRM.
    """
    
    def calculate_statistics(self, data: List[TRMData]) -> Optional[TRMStatistics]:
        """
        Calcula estadísticas sobre los datos de TRM.
        
        Args:
            data (List[TRMData]): Lista de datos de TRM
            
        Returns:
            Optional[TRMStatistics]: Estadísticas calculadas o None si no hay datos
        """
        if not data:
            return None
        
        # Convertir a DataFrame para facilitar cálculos
        df = pd.DataFrame([item.to_dict() for item in data])
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Ordenar por fecha
        df = df.sort_values('fecha')
        
        # Calcular estadísticas
        stats = TRMStatistics(
            min_value=df['trm'].min(),
            max_value=df['trm'].max(),
            avg_value=df['trm'].mean(),
            median_value=df['trm'].median(),
            std_dev=df['trm'].std(),
            count=len(df),
            start_date=df['fecha'].min().date(),
            end_date=df['fecha'].max().date(),
            start_value=df.iloc[0]['trm'],
            end_value=df.iloc[-1]['trm'],
            change=df.iloc[-1]['trm'] - df.iloc[0]['trm'],
            change_pct=(df.iloc[-1]['trm'] / df.iloc[0]['trm'] - 1) * 100
        )
        
        return stats
    
    def calculate_moving_average(self, data: List[TRMData], window: int = 30) -> List[TRMMovingAverage]:
        """
        Calcula el promedio móvil de los datos de TRM.
        
        Args:
            data (List[TRMData]): Lista de datos de TRM
            window (int): Tamaño de la ventana para el promedio móvil
            
        Returns:
            List[TRMMovingAverage]: Lista de datos con promedio móvil
        """
        if not data:
            return []
        
        # Convertir a DataFrame para facilitar cálculos
        df = pd.DataFrame([item.to_dict() for item in data])
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Ordenar por fecha
        df = df.sort_values('fecha')
        
        # Calcular promedio móvil
        df[f'ma_{window}'] = df['trm'].rolling(window=window).mean()
        
        # Convertir de nuevo a objetos de dominio
        result = []
        for _, row in df.iterrows():
            ma_value = row[f'ma_{window}'] if not pd.isna(row[f'ma_{window}']) else None
            result.append(TRMMovingAverage(
                fecha=row['fecha'].date(),
                valor=row['trm'],
                promedio_movil=ma_value,
                window=window
            ))
        
        return result
    
    def find_extreme_variations(self, data: List[TRMData], threshold_pct: float = 1.0) -> List[TRMVariation]:
        """
        Encuentra variaciones extremas en los datos de TRM.
        
        Args:
            data (List[TRMData]): Lista de datos de TRM
            threshold_pct (float): Umbral de variación porcentual
            
        Returns:
            List[TRMVariation]: Lista de variaciones extremas
        """
        if not data:
            return []
        
        # Convertir a DataFrame para facilitar cálculos
        df = pd.DataFrame([item.to_dict() for item in data])
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Ordenar por fecha
        df = df.sort_values('fecha')
        
        # Calcular variación diaria
        df['var_pct'] = df['trm'].pct_change() * 100
        
        # Filtrar por umbral
        extreme_df = df[abs(df['var_pct']) > threshold_pct].copy()
        
        # Convertir de nuevo a objetos de dominio
        result = []
        for _, row in extreme_df.iterrows():
            if not pd.isna(row['var_pct']):
                result.append(TRMVariation(
                    fecha=row['fecha'].date(),
                    valor=row['trm'],
                    variacion_pct=row['var_pct']
                ))
        
        return result
    
    def generate_plot(self, data: List[TRMData]) -> Optional[Figure]:
        """
        Genera un gráfico con los datos de TRM.
        
        Args:
            data (List[TRMData]): Lista de datos de TRM
            
        Returns:
            Optional[Figure]: Figura generada o None si no hay datos
        """
        if not data:
            return None
        
        # Convertir a DataFrame para facilitar la visualización
        df = pd.DataFrame([item.to_dict() for item in data])
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Ordenar por fecha
        df = df.sort_values('fecha')
        
        # Crear gráfico
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['fecha'], df['trm'])
        ax.set_title('Histórico TRM Colombia')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('TRM (COP/USD)')
        ax.grid(True)
        
        # Añadir anotaciones de valores mínimos y máximos
        min_idx = df['trm'].idxmin()
        max_idx = df['trm'].idxmax()
        
        ax.annotate(f'Min: {df.loc[min_idx, "trm"]:.2f}',
                    xy=(df.loc[min_idx, 'fecha'], df.loc[min_idx, 'trm']),
                    xytext=(10, -30), textcoords='offset points',
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
        
        ax.annotate(f'Max: {df.loc[max_idx, "trm"]:.2f}',
                    xy=(df.loc[max_idx, 'fecha'], df.loc[max_idx, 'trm']),
                    xytext=(10, 30), textcoords='offset points',
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
        
        return fig
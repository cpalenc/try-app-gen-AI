"""
Repositorio para acceder a los datos de la TRM.
"""
import os
import pandas as pd
from datetime import date, datetime
from typing import List, Optional, Tuple

from ...domain.models.trm import TRMData


class TRMRepository:
    """
    Repositorio para acceder a los datos de la TRM desde un archivo CSV.
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Inicializa el repositorio.
        
        Args:
            data_path (Optional[str]): Ruta al archivo CSV con datos de TRM
        """
        if data_path is None:
            # Ruta por defecto relativa a la raíz del proyecto
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))
            self.data_path = os.path.join(base_dir, 'data', 'trm_data.csv')
        else:
            self.data_path = data_path
        
        self._data_df = None
    
    def _load_data(self) -> bool:
        """
        Carga los datos desde el archivo CSV.
        
        Returns:
            bool: True si se cargaron correctamente, False en caso contrario
        """
        try:
            self._data_df = pd.read_csv(self.data_path)
            
            # Renombrar columnas para facilitar su uso
            self._data_df.columns = ['fecha', 'trm']
            
            # Convertir la columna de fecha a datetime
            self._data_df['fecha'] = pd.to_datetime(self._data_df['fecha'], format='%Y/%m/%d')
            
            # Ordenar por fecha
            self._data_df = self._data_df.sort_values('fecha')
            
            return True
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            return False
    
    def get_all(self) -> List[TRMData]:
        """
        Obtiene todos los datos de TRM.
        
        Returns:
            List[TRMData]: Lista de datos de TRM
        """
        if self._data_df is None:
            if not self._load_data():
                return []
        
        result = []
        for _, row in self._data_df.iterrows():
            result.append(TRMData(
                fecha=row['fecha'].date(),
                valor=row['trm']
            ))
        
        return result
    
    def get_by_date_range(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[TRMData]:
        """
        Obtiene datos de TRM en un rango de fechas.
        
        Args:
            start_date (Optional[date]): Fecha inicial
            end_date (Optional[date]): Fecha final
            
        Returns:
            List[TRMData]: Lista de datos de TRM filtrados por el rango de fechas
        """
        if self._data_df is None:
            if not self._load_data():
                return []
        
        filtered_df = self._data_df.copy()
        
        if start_date:
            start_date_dt = pd.Timestamp(start_date)
            filtered_df = filtered_df[filtered_df['fecha'] >= start_date_dt]
            
        if end_date:
            end_date_dt = pd.Timestamp(end_date)
            filtered_df = filtered_df[filtered_df['fecha'] <= end_date_dt]
        
        result = []
        for _, row in filtered_df.iterrows():
            result.append(TRMData(
                fecha=row['fecha'].date(),
                valor=row['trm']
            ))
        
        return result
    
    def get_date_range(self) -> Tuple[date, date]:
        """
        Obtiene el rango de fechas disponibles.
        
        Returns:
            Tuple[date, date]: Fecha mínima y máxima disponibles
        """
        if self._data_df is None:
            if not self._load_data():
                return (date.today(), date.today())
        
        min_date = self._data_df['fecha'].min().date()
        max_date = self._data_df['fecha'].max().date()
        
        return (min_date, max_date)
    
    def save(self, data: List[TRMData]) -> bool:
        """
        Guarda datos de TRM en el archivo CSV.
        
        Args:
            data (List[TRMData]): Lista de datos de TRM a guardar
            
        Returns:
            bool: True si se guardaron correctamente, False en caso contrario
        """
        try:
            # Convertir a DataFrame
            new_df = pd.DataFrame([item.to_dict() for item in data])
            new_df['fecha'] = pd.to_datetime(new_df['fecha'])
            
            # Si ya hay datos cargados, combinarlos
            if self._data_df is not None:
                combined_df = pd.concat([self._data_df, new_df])
                # Eliminar duplicados
                combined_df = combined_df.drop_duplicates(subset=['fecha'])
                # Ordenar por fecha
                combined_df = combined_df.sort_values('fecha')
                self._data_df = combined_df
            else:
                self._data_df = new_df
            
            # Guardar en formato CSV
            self._data_df.to_csv(self.data_path, index=False, date_format='%Y/%m/%d')
            
            return True
        except Exception as e:
            print(f"Error al guardar los datos: {e}")
            return False
"""
Servicio de aplicación para la TRM.
"""
from datetime import date
from typing import List, Optional, Dict, Any, Tuple
import io
from matplotlib.figure import Figure
import pandas as pd

# Importación simplificada para evitar problemas de dependencias circulares
# Usaremos importación dinámica cuando sea necesario


class TRMApplicationService:
    """
    Servicio de aplicación que coordina las operaciones con datos de TRM.
    """
    
    def __init__(self, repository=None, service=None):
        """
        Inicializa el servicio de aplicación.
        
        Args:
            repository: Repositorio de TRM
            service: Servicio de dominio de TRM
        """
        # Importación dinámica para evitar problemas de dependencias circulares
        from ...infrastructure.repositories.trm_repository import TRMRepository
        from ...domain.services.trm_service import TRMService
        
        self.repository = repository or TRMRepository()
        self.service = service or TRMService()
    
    def get_trm_data(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtiene datos de TRM en un rango de fechas.
        
        Args:
            start_date (Optional[str]): Fecha inicial en formato YYYY-MM-DD
            end_date (Optional[str]): Fecha final en formato YYYY-MM-DD
            
        Returns:
            List[Dict[str, Any]]: Lista de datos de TRM en formato diccionario
        """
        try:
            start_date_obj = date.fromisoformat(start_date) if start_date else None
            end_date_obj = date.fromisoformat(end_date) if end_date else None
        except ValueError:
            # Si hay un error en el formato de fecha, intentamos con otro formato
            try:
                if start_date:
                    start_date_obj = pd.to_datetime(start_date).date()
                else:
                    start_date_obj = None
                
                if end_date:
                    end_date_obj = pd.to_datetime(end_date).date()
                else:
                    end_date_obj = None
            except:
                # Si sigue fallando, usamos None
                start_date_obj = None
                end_date_obj = None
        
        data = self.repository.get_by_date_range(start_date_obj, end_date_obj)
        
        return [item.to_dict() for item in data]
    
    def get_statistics(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Calcula estadísticas sobre los datos de TRM.
        
        Args:
            start_date (Optional[str]): Fecha inicial en formato YYYY-MM-DD
            end_date (Optional[str]): Fecha final en formato YYYY-MM-DD
            
        Returns:
            Optional[Dict[str, Any]]: Estadísticas calculadas o None si no hay datos
        """
        try:
            start_date_obj = date.fromisoformat(start_date) if start_date else None
            end_date_obj = date.fromisoformat(end_date) if end_date else None
        except ValueError:
            # Si hay un error en el formato de fecha, intentamos con otro formato
            try:
                if start_date:
                    start_date_obj = pd.to_datetime(start_date).date()
                else:
                    start_date_obj = None
                
                if end_date:
                    end_date_obj = pd.to_datetime(end_date).date()
                else:
                    end_date_obj = None
            except:
                # Si sigue fallando, usamos None
                start_date_obj = None
                end_date_obj = None
        
        data = self.repository.get_by_date_range(start_date_obj, end_date_obj)
        stats = self.service.calculate_statistics(data)
        
        return stats.to_dict() if stats else None
    
    def get_moving_average(self, window: int = 30, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Calcula el promedio móvil de los datos de TRM.
        
        Args:
            window (int): Tamaño de la ventana para el promedio móvil
            start_date (Optional[str]): Fecha inicial en formato YYYY-MM-DD
            end_date (Optional[str]): Fecha final en formato YYYY-MM-DD
            
        Returns:
            List[Dict[str, Any]]: Lista de datos con promedio móvil en formato diccionario
        """
        try:
            start_date_obj = date.fromisoformat(start_date) if start_date else None
            end_date_obj = date.fromisoformat(end_date) if end_date else None
        except ValueError:
            # Si hay un error en el formato de fecha, intentamos con otro formato
            try:
                if start_date:
                    start_date_obj = pd.to_datetime(start_date).date()
                else:
                    start_date_obj = None
                
                if end_date:
                    end_date_obj = pd.to_datetime(end_date).date()
                else:
                    end_date_obj = None
            except:
                # Si sigue fallando, usamos None
                start_date_obj = None
                end_date_obj = None
        
        data = self.repository.get_by_date_range(start_date_obj, end_date_obj)
        ma_data = self.service.calculate_moving_average(data, window)
        
        return [item.to_dict() for item in ma_data]
    
    def get_extreme_variations(self, threshold_pct: float = 1.0, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Encuentra variaciones extremas en los datos de TRM.
        
        Args:
            threshold_pct (float): Umbral de variación porcentual
            start_date (Optional[str]): Fecha inicial en formato YYYY-MM-DD
            end_date (Optional[str]): Fecha final en formato YYYY-MM-DD
            
        Returns:
            List[Dict[str, Any]]: Lista de variaciones extremas en formato diccionario
        """
        try:
            start_date_obj = date.fromisoformat(start_date) if start_date else None
            end_date_obj = date.fromisoformat(end_date) if end_date else None
        except ValueError:
            # Si hay un error en el formato de fecha, intentamos con otro formato
            try:
                if start_date:
                    start_date_obj = pd.to_datetime(start_date).date()
                else:
                    start_date_obj = None
                
                if end_date:
                    end_date_obj = pd.to_datetime(end_date).date()
                else:
                    end_date_obj = None
            except:
                # Si sigue fallando, usamos None
                start_date_obj = None
                end_date_obj = None
        
        data = self.repository.get_by_date_range(start_date_obj, end_date_obj)
        variations = self.service.find_extreme_variations(data, threshold_pct)
        
        return [item.to_dict() for item in variations]
    
    def generate_plot(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Optional[Figure]:
        """
        Genera un gráfico con los datos de TRM.
        
        Args:
            start_date (Optional[str]): Fecha inicial en formato YYYY-MM-DD
            end_date (Optional[str]): Fecha final en formato YYYY-MM-DD
            
        Returns:
            Optional[Figure]: Figura generada o None si no hay datos
        """
        try:
            start_date_obj = date.fromisoformat(start_date) if start_date else None
            end_date_obj = date.fromisoformat(end_date) if end_date else None
        except ValueError:
            # Si hay un error en el formato de fecha, intentamos con otro formato
            try:
                if start_date:
                    start_date_obj = pd.to_datetime(start_date).date()
                else:
                    start_date_obj = None
                
                if end_date:
                    end_date_obj = pd.to_datetime(end_date).date()
                else:
                    end_date_obj = None
            except:
                # Si sigue fallando, usamos None
                start_date_obj = None
                end_date_obj = None
        
        data = self.repository.get_by_date_range(start_date_obj, end_date_obj)
        return self.service.generate_plot(data)
    
    def get_date_range(self) -> Tuple[date, date]:
        """
        Obtiene el rango de fechas disponibles.
        
        Returns:
            Tuple[date, date]: Fecha mínima y máxima disponibles
        """
        return self.repository.get_date_range()
    
    def update_data(self, new_data: List[Dict[str, Any]]) -> bool:
        """
        Actualiza los datos de TRM.
        
        Args:
            new_data (List[Dict[str, Any]]): Nuevos datos de TRM
            
        Returns:
            bool: True si se actualizaron correctamente, False en caso contrario
        """
        # Importación dinámica para evitar problemas de dependencias circulares
        from ...domain.models.trm import TRMData
        
        trm_data = []
        for item in new_data:
            try:
                fecha = date.fromisoformat(item['fecha']) if isinstance(item['fecha'], str) else item['fecha']
            except ValueError:
                # Si hay un error en el formato de fecha, intentamos con otro formato
                try:
                    fecha = pd.to_datetime(item['fecha']).date()
                except:
                    # Si sigue fallando, saltamos este registro
                    continue
            
            trm_data.append(TRMData(
                fecha=fecha,
                valor=item['trm']
            ))
        
        return self.repository.save(trm_data)
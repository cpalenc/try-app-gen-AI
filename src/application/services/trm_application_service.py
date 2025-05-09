"""
Servicio de aplicación para la TRM.
"""
from datetime import date
from typing import List, Optional, Dict, Any, Tuple
import io
from matplotlib.figure import Figure

from ...domain.models.trm import TRMData, TRMStatistics, TRMVariation, TRMMovingAverage
from ...domain.services.trm_service import TRMService
from ...infrastructure.repositories.trm_repository import TRMRepository


class TRMApplicationService:
    """
    Servicio de aplicación que coordina las operaciones con datos de TRM.
    """
    
    def __init__(self, repository: Optional[TRMRepository] = None, service: Optional[TRMService] = None):
        """
        Inicializa el servicio de aplicación.
        
        Args:
            repository (Optional[TRMRepository]): Repositorio de TRM
            service (Optional[TRMService]): Servicio de dominio de TRM
        """
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
        start_date_obj = date.fromisoformat(start_date) if start_date else None
        end_date_obj = date.fromisoformat(end_date) if end_date else None
        
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
        start_date_obj = date.fromisoformat(start_date) if start_date else None
        end_date_obj = date.fromisoformat(end_date) if end_date else None
        
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
        start_date_obj = date.fromisoformat(start_date) if start_date else None
        end_date_obj = date.fromisoformat(end_date) if end_date else None
        
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
        start_date_obj = date.fromisoformat(start_date) if start_date else None
        end_date_obj = date.fromisoformat(end_date) if end_date else None
        
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
        start_date_obj = date.fromisoformat(start_date) if start_date else None
        end_date_obj = date.fromisoformat(end_date) if end_date else None
        
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
        trm_data = []
        for item in new_data:
            fecha = date.fromisoformat(item['fecha']) if isinstance(item['fecha'], str) else item['fecha']
            trm_data.append(TRMData(
                fecha=fecha,
                valor=item['trm']
            ))
        
        return self.repository.save(trm_data)
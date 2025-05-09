"""
Módulo que define los modelos de dominio para la TRM.
"""
from dataclasses import dataclass
from datetime import date
from typing import List, Dict, Any, Optional


@dataclass
class TRMData:
    """
    Clase que representa un registro de TRM para una fecha específica.
    """
    fecha: date
    valor: float

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto a un diccionario.
        
        Returns:
            Dict[str, Any]: Diccionario con los datos del objeto
        """
        return {
            'fecha': self.fecha.strftime('%Y-%m-%d'),
            'trm': self.valor
        }


@dataclass
class TRMStatistics:
    """
    Clase que representa estadísticas calculadas sobre datos de TRM.
    """
    min_value: float
    max_value: float
    avg_value: float
    median_value: float
    std_dev: float
    count: int
    start_date: date
    end_date: date
    start_value: float
    end_value: float
    change: float
    change_pct: float

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto a un diccionario.
        
        Returns:
            Dict[str, Any]: Diccionario con los datos del objeto
        """
        return {
            'min': self.min_value,
            'max': self.max_value,
            'avg': self.avg_value,
            'median': self.median_value,
            'std': self.std_dev,
            'count': self.count,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'start_value': self.start_value,
            'end_value': self.end_value,
            'change': self.change,
            'change_pct': self.change_pct
        }


@dataclass
class TRMVariation:
    """
    Clase que representa una variación significativa en la TRM.
    """
    fecha: date
    valor: float
    variacion_pct: float

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto a un diccionario.
        
        Returns:
            Dict[str, Any]: Diccionario con los datos del objeto
        """
        return {
            'fecha': self.fecha.strftime('%Y-%m-%d'),
            'trm': self.valor,
            'variacion_pct': self.variacion_pct
        }


@dataclass
class TRMMovingAverage:
    """
    Clase que representa un registro de TRM con su promedio móvil.
    """
    fecha: date
    valor: float
    promedio_movil: Optional[float] = None
    window: int = 30

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto a un diccionario.
        
        Returns:
            Dict[str, Any]: Diccionario con los datos del objeto
        """
        return {
            'fecha': self.fecha.strftime('%Y-%m-%d'),
            'trm': self.valor,
            f'ma_{self.window}': self.promedio_movil
        }
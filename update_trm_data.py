#!/usr/bin/env python3
"""
Script para actualizar los datos de la TRM desde la API del Banco de la República
"""

import requests
import pandas as pd
import os
from datetime import datetime, timedelta
import argparse
import sys

# URL de la API del Banco de la República
API_URL = "https://www.banrep.gov.co/estadisticas/trm"

def parse_args():
    """Parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description='Actualiza los datos de la TRM desde la API del Banco de la República')
    parser.add_argument('--output', '-o', default='../data/trm_data.csv', help='Archivo de salida (CSV)')
    parser.add_argument('--days', '-d', type=int, default=30, help='Número de días a consultar')
    parser.add_argument('--append', '-a', action='store_true', help='Añadir a datos existentes')
    return parser.parse_args()

def get_trm_data(days=30):
    """
    Obtiene los datos de la TRM desde la API del Banco de la República
    
    Args:
        days (int): Número de días a consultar
        
    Returns:
        DataFrame: Datos de la TRM
    """
    try:
        # Nota: Esta es una implementación simulada ya que la API real requiere autenticación
        # o tiene una estructura diferente. En una implementación real, se debería usar la API
        # oficial del Banco de la República o una fuente de datos confiable.
        
        # En este ejemplo, generamos datos aleatorios para simular la consulta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Crear un rango de fechas
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Crear un DataFrame con fechas y valores aleatorios
        data = pd.DataFrame({
            'fecha': date_range,
            'trm': [4000 + i * 10 for i in range(len(date_range))]  # Valores simulados
        })
        
        print(f"Datos obtenidos: {len(data)} registros")
        return data
        
        # En una implementación real, se haría algo como:
        # response = requests.get(f"{API_URL}?start_date={start_date}&end_date={end_date}")
        # if response.status_code == 200:
        #     data = response.json()
        #     return pd.DataFrame(data)
        # else:
        #     print(f"Error al obtener datos: {response.status_code}")
        #     return None
        
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return None

def update_trm_data(output_file, days=30, append=False):
    """
    Actualiza los datos de la TRM
    
    Args:
        output_file (str): Archivo de salida
        days (int): Número de días a consultar
        append (bool): Añadir a datos existentes
        
    Returns:
        bool: True si se actualizaron los datos, False en caso contrario
    """
    # Obtener nuevos datos
    new_data = get_trm_data(days)
    
    if new_data is None:
        return False
    
    if append and os.path.exists(output_file):
        try:
            # Cargar datos existentes
            existing_data = pd.read_csv(output_file)
            
            # Convertir columna de fecha a datetime
            existing_data['fecha'] = pd.to_datetime(existing_data['fecha'])
            
            # Combinar datos
            combined_data = pd.concat([existing_data, new_data])
            
            # Eliminar duplicados
            combined_data = combined_data.drop_duplicates(subset=['fecha'])
            
            # Ordenar por fecha
            combined_data = combined_data.sort_values('fecha')
            
            # Guardar datos combinados
            combined_data.to_csv(output_file, index=False)
            
            print(f"Datos actualizados: {len(combined_data)} registros totales")
            return True
            
        except Exception as e:
            print(f"Error al combinar datos: {e}")
            return False
    else:
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Guardar nuevos datos
            new_data.to_csv(output_file, index=False)
            
            print(f"Datos guardados: {len(new_data)} registros")
            return True
            
        except Exception as e:
            print(f"Error al guardar datos: {e}")
            return False

def main():
    """Función principal"""
    args = parse_args()
    
    if update_trm_data(args.output, args.days, args.append):
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
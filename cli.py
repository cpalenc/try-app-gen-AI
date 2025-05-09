#!/usr/bin/env python3
"""
CLI para consultar el histórico de la TRM en Colombia
"""

import argparse
import sys
from trm_data_loader import TRMDataLoader
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def parse_args():
    """Parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description='Consulta el histórico de la TRM en Colombia')
    
    # Comandos principales
    subparsers = parser.add_subparsers(dest='command', help='Comando a ejecutar')
    
    # Comando para obtener datos
    get_parser = subparsers.add_parser('get', help='Obtener datos de la TRM')
    get_parser.add_argument('--start', '-s', help='Fecha inicial (YYYY-MM-DD)')
    get_parser.add_argument('--end', '-e', help='Fecha final (YYYY-MM-DD)')
    get_parser.add_argument('--output', '-o', help='Archivo de salida (CSV)')
    
    # Comando para obtener estadísticas
    stats_parser = subparsers.add_parser('stats', help='Obtener estadísticas de la TRM')
    stats_parser.add_argument('--start', '-s', help='Fecha inicial (YYYY-MM-DD)')
    stats_parser.add_argument('--end', '-e', help='Fecha final (YYYY-MM-DD)')
    
    # Comando para generar gráfico
    plot_parser = subparsers.add_parser('plot', help='Generar gráfico de la TRM')
    plot_parser.add_argument('--start', '-s', help='Fecha inicial (YYYY-MM-DD)')
    plot_parser.add_argument('--end', '-e', help='Fecha final (YYYY-MM-DD)')
    plot_parser.add_argument('--output', '-o', help='Archivo de salida (PNG)')
    plot_parser.add_argument('--show', action='store_true', help='Mostrar gráfico')
    
    # Comando para calcular promedio móvil
    ma_parser = subparsers.add_parser('ma', help='Calcular promedio móvil de la TRM')
    ma_parser.add_argument('--window', '-w', type=int, default=30, help='Ventana del promedio móvil')
    ma_parser.add_argument('--start', '-s', help='Fecha inicial (YYYY-MM-DD)')
    ma_parser.add_argument('--end', '-e', help='Fecha final (YYYY-MM-DD)')
    ma_parser.add_argument('--output', '-o', help='Archivo de salida (CSV)')
    
    # Comando para encontrar variaciones extremas
    var_parser = subparsers.add_parser('var', help='Encontrar variaciones extremas de la TRM')
    var_parser.add_argument('--threshold', '-t', type=float, default=1.0, help='Umbral de variación (%)')
    var_parser.add_argument('--start', '-s', help='Fecha inicial (YYYY-MM-DD)')
    var_parser.add_argument('--end', '-e', help='Fecha final (YYYY-MM-DD)')
    var_parser.add_argument('--output', '-o', help='Archivo de salida (CSV)')
    
    return parser.parse_args()

def main():
    """Función principal"""
    args = parse_args()
    
    # Inicializar el cargador de datos
    loader = TRMDataLoader()
    
    if args.command == 'get':
        # Obtener datos
        data = loader.get_data_range(args.start, args.end)
        
        if data is None:
            print("Error: No se pudieron cargar los datos")
            return 1
        
        if args.output:
            data.to_csv(args.output, index=False)
            print(f"Datos guardados en {args.output}")
        else:
            pd.set_option('display.max_rows', None)
            print(data)
    
    elif args.command == 'stats':
        # Obtener estadísticas
        stats = loader.get_statistics(args.start, args.end)
        
        if stats is None:
            print("Error: No se pudieron calcular las estadísticas")
            return 1
        
        print("\n=== Estadísticas de la TRM ===")
        print(f"Periodo: {stats['start_date']} a {stats['end_date']}")
        print(f"Registros: {stats['count']}")
        print(f"Mínimo: ${stats['min']:.2f}")
        print(f"Máximo: ${stats['max']:.2f}")
        print(f"Promedio: ${stats['avg']:.2f}")
        print(f"Mediana: ${stats['median']:.2f}")
        print(f"Desviación estándar: ${stats['std']:.2f}")
        print(f"Valor inicial: ${stats['start_value']:.2f}")
        print(f"Valor final: ${stats['end_value']:.2f}")
        print(f"Cambio absoluto: ${stats['change']:.2f}")
        print(f"Cambio porcentual: {stats['change_pct']:.2f}%")
    
    elif args.command == 'plot':
        # Generar gráfico
        fig = loader.plot_trm(args.start, args.end, args.output)
        
        if fig is None:
            print("Error: No se pudo generar el gráfico")
            return 1
        
        if args.output:
            print(f"Gráfico guardado en {args.output}")
        
        if args.show:
            plt.show()
    
    elif args.command == 'ma':
        # Calcular promedio móvil
        data = loader.calculate_moving_average(args.window, args.start, args.end)
        
        if data is None:
            print("Error: No se pudo calcular el promedio móvil")
            return 1
        
        if args.output:
            data.to_csv(args.output, index=False)
            print(f"Datos guardados en {args.output}")
        else:
            pd.set_option('display.max_rows', None)
            print(data)
    
    elif args.command == 'var':
        # Encontrar variaciones extremas
        data = loader.find_extreme_variations(args.threshold, args.start, args.end)
        
        if data is None:
            print("Error: No se pudieron calcular las variaciones")
            return 1
        
        if data.empty:
            print(f"No se encontraron variaciones superiores al {args.threshold}%")
            return 0
        
        if args.output:
            data.to_csv(args.output, index=False)
            print(f"Datos guardados en {args.output}")
        else:
            pd.set_option('display.max_rows', None)
            print(data)
    
    else:
        print("Error: Comando no reconocido")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
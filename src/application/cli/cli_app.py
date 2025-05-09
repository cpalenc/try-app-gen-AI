"""
Interfaz de línea de comandos para la TRM.
"""
import argparse
import sys
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from ...application.services.trm_application_service import TRMApplicationService


def parse_args():
    """
    Parsea los argumentos de línea de comandos.
    
    Returns:
        argparse.Namespace: Argumentos parseados
    """
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


def run_cli():
    """
    Ejecuta la interfaz de línea de comandos.
    
    Returns:
        int: Código de salida
    """
    args = parse_args()
    
    # Inicializar el servicio de aplicación
    trm_app_service = TRMApplicationService()
    
    if args.command == 'get':
        # Obtener datos
        data = trm_app_service.get_trm_data(args.start, args.end)
        
        if not data:
            print("Error: No se pudieron cargar los datos")
            return 1
        
        df = pd.DataFrame(data)
        
        if args.output:
            df.to_csv(args.output, index=False)
            print(f"Datos guardados en {args.output}")
        else:
            pd.set_option('display.max_rows', None)
            print(df)
    
    elif args.command == 'stats':
        # Obtener estadísticas
        stats = trm_app_service.get_statistics(args.start, args.end)
        
        if not stats:
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
        fig = trm_app_service.generate_plot(args.start, args.end)
        
        if fig is None:
            print("Error: No se pudo generar el gráfico")
            return 1
        
        if args.output:
            fig.savefig(args.output)
            print(f"Gráfico guardado en {args.output}")
        
        if args.show:
            plt.show()
    
    elif args.command == 'ma':
        # Calcular promedio móvil
        data = trm_app_service.get_moving_average(args.window, args.start, args.end)
        
        if not data:
            print("Error: No se pudo calcular el promedio móvil")
            return 1
        
        df = pd.DataFrame(data)
        
        if args.output:
            df.to_csv(args.output, index=False)
            print(f"Datos guardados en {args.output}")
        else:
            pd.set_option('display.max_rows', None)
            print(df)
    
    elif args.command == 'var':
        # Encontrar variaciones extremas
        data = trm_app_service.get_extreme_variations(args.threshold, args.start, args.end)
        
        if not data:
            print(f"No se encontraron variaciones superiores al {args.threshold}%")
            return 0
        
        df = pd.DataFrame(data)
        
        if args.output:
            df.to_csv(args.output, index=False)
            print(f"Datos guardados en {args.output}")
        else:
            pd.set_option('display.max_rows', None)
            print(df)
    
    else:
        print("Error: Comando no reconocido")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(run_cli())
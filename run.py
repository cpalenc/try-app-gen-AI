#!/usr/bin/env python3
"""
Script principal para ejecutar la aplicación TRM Colombia
"""

import argparse
import sys
import os
import subprocess

def parse_args():
    """Parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description='Ejecuta la aplicación TRM Colombia')
    
    # Comandos principales
    subparsers = parser.add_subparsers(dest='command', help='Comando a ejecutar')
    
    # Comando para ejecutar la aplicación web
    web_parser = subparsers.add_parser('web', help='Ejecuta la aplicación web con Streamlit')
    web_parser.add_argument('--port', '-p', type=int, default=8501, help='Puerto para la aplicación web')
    
    # Comando para ejecutar la API
    api_parser = subparsers.add_parser('api', help='Ejecuta la API REST con Flask')
    api_parser.add_argument('--port', '-p', type=int, default=5000, help='Puerto para la API')
    
    # Comando para actualizar los datos
    update_parser = subparsers.add_parser('update', help='Actualiza los datos de la TRM')
    update_parser.add_argument('--days', '-d', type=int, default=30, help='Número de días a consultar')
    update_parser.add_argument('--append', '-a', action='store_true', help='Añadir a datos existentes')
    
    # Comando para ejecutar la CLI
    cli_parser = subparsers.add_parser('cli', help='Ejecuta la interfaz de línea de comandos')
    cli_parser.add_argument('cli_args', nargs='*', help='Argumentos para la CLI')
    
    return parser.parse_args()

def main():
    """Función principal"""
    args = parse_args()
    
    # Obtener el directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.command == 'web':
        # Ejecutar la aplicación web con Streamlit
        cmd = ['streamlit', 'run', os.path.join(current_dir, 'app.py'), '--server.port', str(args.port)]
        print(f"Ejecutando aplicación web en http://localhost:{args.port}")
        subprocess.run(cmd)
    
    elif args.command == 'api':
        # Ejecutar la API REST con Flask
        os.environ['PORT'] = str(args.port)
        print(f"Ejecutando API REST en http://localhost:{args.port}")
        subprocess.run(['python', os.path.join(current_dir, 'api.py')])
    
    elif args.command == 'update':
        # Actualizar los datos de la TRM
        cmd = ['python', os.path.join(current_dir, 'update_trm_data.py')]
        if args.days:
            cmd.extend(['--days', str(args.days)])
        if args.append:
            cmd.append('--append')
        subprocess.run(cmd)
    
    elif args.command == 'cli':
        # Ejecutar la interfaz de línea de comandos
        cmd = ['python', os.path.join(current_dir, 'cli.py')]
        if args.cli_args:
            cmd.extend(args.cli_args)
        subprocess.run(cmd)
    
    else:
        print("Uso: python run.py [web|api|update|cli] [opciones]")
        print("Ejecute 'python run.py --help' para más información")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
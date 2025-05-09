#!/usr/bin/env python3
"""
Script principal para ejecutar la aplicación TRM Colombia.
"""
import argparse
import sys
import os

# Asegurarse de que el directorio actual esté en el PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Importar después de configurar el PYTHONPATH
from src.utils.logger import app_logger
from src.utils.config import API_HOST, API_PORT, API_DEBUG, STREAMLIT_PORT


def parse_args():
    """
    Parsea los argumentos de línea de comandos.
    
    Returns:
        argparse.Namespace: Argumentos parseados
    """
    parser = argparse.ArgumentParser(description='Ejecuta la aplicación TRM Colombia')
    
    # Comandos principales
    subparsers = parser.add_subparsers(dest='command', help='Comando a ejecutar')
    
    # Comando para ejecutar la aplicación web
    web_parser = subparsers.add_parser('web', help='Ejecuta la aplicación web con Streamlit')
    web_parser.add_argument('--port', '-p', type=int, default=STREAMLIT_PORT, help='Puerto para la aplicación web')
    
    # Comando para ejecutar la API
    api_parser = subparsers.add_parser('api', help='Ejecuta la API REST con Flask')
    api_parser.add_argument('--host', type=str, default=API_HOST, help='Host para la API')
    api_parser.add_argument('--port', '-p', type=int, default=API_PORT, help='Puerto para la API')
    api_parser.add_argument('--debug', '-d', action='store_true', default=API_DEBUG, help='Modo debug')
    
    # Comando para actualizar los datos
    update_parser = subparsers.add_parser('update', help='Actualiza los datos de la TRM')
    update_parser.add_argument('--days', '-d', type=int, default=30, help='Número de días a consultar')
    update_parser.add_argument('--append', '-a', action='store_true', help='Añadir a datos existentes')
    
    # Comando para ejecutar la CLI
    cli_parser = subparsers.add_parser('cli', help='Ejecuta la interfaz de línea de comandos')
    cli_parser.add_argument('cli_args', nargs='*', help='Argumentos para la CLI')
    
    return parser.parse_args()


def main():
    """
    Función principal.
    
    Returns:
        int: Código de salida
    """
    args = parse_args()
    
    if args.command == 'web':
        # Ejecutar la aplicación web con Streamlit
        app_logger.info(f"Ejecutando aplicación web en puerto {args.port}")
        
        try:
            # Importar aquí para evitar cargar Streamlit innecesariamente
            import streamlit.web.cli as stcli
            import streamlit as st
            
            # Configurar variables de entorno para Streamlit
            os.environ['STREAMLIT_SERVER_PORT'] = str(args.port)
            
            # Ruta al archivo de la aplicación Streamlit
            streamlit_app_path = os.path.join(current_dir, 'src', 'application', 'web', 'streamlit_app.py')
            
            # Ejecutar la aplicación
            sys.argv = ["streamlit", "run", streamlit_app_path]
            stcli.main()
            
        except ImportError:
            app_logger.error("No se pudo importar Streamlit. Asegúrate de que esté instalado.")
            return 1
        except Exception as e:
            app_logger.error(f"Error al ejecutar la aplicación web: {e}")
            return 1
    
    elif args.command == 'api':
        # Ejecutar la API REST con Flask
        app_logger.info(f"Ejecutando API REST en {args.host}:{args.port} (debug={args.debug})")
        
        try:
            # Importar aquí para evitar cargar Flask innecesariamente
            from src.infrastructure.api.flask_api import run_api
            
            # Ejecutar la API
            run_api(host=args.host, port=args.port, debug=args.debug)
            
        except ImportError:
            app_logger.error("No se pudo importar Flask. Asegúrate de que esté instalado.")
            return 1
        except Exception as e:
            app_logger.error(f"Error al ejecutar la API REST: {e}")
            return 1
    
    elif args.command == 'update':
        # Actualizar los datos de la TRM
        app_logger.info(f"Actualizando datos de la TRM (días={args.days}, append={args.append})")
        
        try:
            # Importar aquí para evitar cargar dependencias innecesariamente
            from src.infrastructure.data.trm_data_updater import TRMDataUpdater
            
            # Crear actualizador de datos
            updater = TRMDataUpdater()
            
            # Actualizar datos
            if updater.update_data(args.days, args.append):
                app_logger.info("Datos actualizados correctamente")
                return 0
            else:
                app_logger.error("Error al actualizar los datos")
                return 1
                
        except ImportError:
            app_logger.error("No se pudieron importar las dependencias necesarias.")
            return 1
        except Exception as e:
            app_logger.error(f"Error al actualizar los datos: {e}")
            return 1
    
    elif args.command == 'cli':
        # Ejecutar la interfaz de línea de comandos
        app_logger.info(f"Ejecutando CLI con argumentos: {args.cli_args}")
        
        try:
            # Importar aquí para evitar cargar la CLI innecesariamente
            from src.application.cli.cli_app import run_cli
            
            # Configurar argumentos para la CLI
            sys.argv = [sys.argv[0]] + args.cli_args
            
            # Ejecutar la CLI
            return run_cli()
            
        except ImportError:
            app_logger.error("No se pudieron importar las dependencias necesarias.")
            return 1
        except Exception as e:
            app_logger.error(f"Error al ejecutar la CLI: {e}")
            return 1
    
    else:
        print("Uso: python main.py [web|api|update|cli] [opciones]")
        print("Ejecute 'python main.py --help' para más información")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
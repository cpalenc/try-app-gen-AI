"""
Configuración de logging para la aplicación.
"""
import logging
import os
import sys
from datetime import datetime

# Configuración básica de logging
def setup_logger(name=None, level=logging.INFO):
    """
    Configura y devuelve un logger.
    
    Args:
        name (str): Nombre del logger
        level (int): Nivel de logging
        
    Returns:
        logging.Logger: Logger configurado
    """
    # Crear directorio de logs si no existe
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Nombre del archivo de log
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")
    
    # Configurar logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar duplicación de handlers
    if not logger.handlers:
        # Handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        # Handler para archivo
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger

# Logger principal de la aplicación
app_logger = setup_logger("trm_app")
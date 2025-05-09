"""
Configuración de la aplicación.
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()

# Configuración general
APP_NAME = "TRM Colombia"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Aplicación para consultar y analizar el histórico de la TRM en Colombia"

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "trm_data.csv")

# Configuración de la API
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 5000))
API_DEBUG = os.getenv("API_DEBUG", "True").lower() in ("true", "1", "t")

# Configuración de Streamlit
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8501))

# Configuración de la base de datos (para futuras extensiones)
DB_TYPE = os.getenv("DB_TYPE", "csv")  # csv, sqlite, postgresql, etc.
DB_PATH = os.getenv("DB_PATH", DATA_FILE)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "trm_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Configuración de la API externa
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "https://www.banrep.gov.co/estadisticas/trm")
EXTERNAL_API_KEY = os.getenv("EXTERNAL_API_KEY", "")
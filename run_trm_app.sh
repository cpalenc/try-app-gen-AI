#!/bin/bash

# Script simplificado para ejecutar la aplicación TRM Colombia
# Este script ejecuta directamente la aplicación web con Streamlit

# Colores para mensajes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con formato
print_message() {
    echo -e "${GREEN}[TRM App]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[TRM App]${NC} $1"
}

print_error() {
    echo -e "${RED}[TRM App]${NC} $1"
}

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Obtener la ruta del directorio actual
APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$APP_DIR/venv"
PYTHON_APP_DIR="$APP_DIR/python_app"

# Verificar si el directorio de la aplicación existe
if [ ! -d "$PYTHON_APP_DIR" ]; then
    print_error "El directorio de la aplicación no existe: $PYTHON_APP_DIR"
    exit 1
fi

# Eliminar entorno virtual existente si hay problemas
if [ -d "$VENV_DIR" ] && [ "$1" == "--clean" ]; then
    print_warning "Eliminando entorno virtual existente..."
    rm -rf "$VENV_DIR"
fi

# Crear entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    print_message "Creando entorno virtual en $VENV_DIR..."
    # Intentar con diferentes versiones de Python
    if command -v python3.10 &> /dev/null; then
        python3.10 -m venv "$VENV_DIR"
    elif command -v python3.9 &> /dev/null; then
        python3.9 -m venv "$VENV_DIR"
    elif command -v python3.8 &> /dev/null; then
        python3.8 -m venv "$VENV_DIR"
    else
        python3 -m venv "$VENV_DIR"
    fi
    
    if [ $? -ne 0 ]; then
        print_error "Error al crear el entorno virtual."
        exit 1
    fi
    print_message "Entorno virtual creado correctamente."
else
    print_message "Usando entorno virtual existente en $VENV_DIR"
fi

# Activar entorno virtual
print_message "Activando entorno virtual..."
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    print_error "Error al activar el entorno virtual."
    exit 1
fi

# Actualizar pip y setuptools
print_message "Actualizando pip y setuptools..."
pip install --upgrade pip setuptools wheel > /dev/null

# Instalar dependencias básicas primero
print_message "Instalando dependencias básicas..."
pip install numpy pandas matplotlib > /dev/null

# Instalar el resto de dependencias
print_message "Instalando dependencias restantes..."
pip install -r "$PYTHON_APP_DIR/requirements.txt" > /dev/null
if [ $? -ne 0 ]; then
    print_warning "Hubo problemas al instalar algunas dependencias. Intentando instalar individualmente..."
    pip install pandas==2.0.3 > /dev/null
    pip install numpy==1.24.3 > /dev/null
    pip install matplotlib==3.7.2 > /dev/null
    pip install seaborn==0.12.2 > /dev/null
    pip install flask==2.3.3 > /dev/null
    pip install flask-cors==4.0.0 > /dev/null
    pip install requests==2.31.0 > /dev/null
    pip install python-dotenv==1.0.0 > /dev/null
    pip install streamlit==1.27.0 > /dev/null
fi

# Crear directorio de logs si no existe
mkdir -p "$PYTHON_APP_DIR/logs"

# Ejecutar la aplicación web directamente
print_message "Ejecutando aplicación web con Streamlit..."
cd "$PYTHON_APP_DIR"
PYTHONPATH="$PYTHON_APP_DIR" python main.py web
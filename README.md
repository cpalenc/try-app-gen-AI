# TRM Colombia - Aplicación de Consulta

Esta aplicación permite consultar y analizar el histórico de la Tasa Representativa del Mercado (TRM) en Colombia.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
trm_app/
├── data/                     # Datos de la aplicación
│   └── trm_data.csv          # Datos históricos de la TRM
├── python_app/               # Aplicación Python
│   ├── simple_trm.py         # Versión minimalista (recomendada)
│   └── trm_app.py            # Versión con más funcionalidades
├── run_minimal.sh            # Script para ejecutar la versión minimalista
└── run_simple.sh             # Script para ejecutar la versión con más funcionalidades
```

## Características

- Consulta de datos históricos de la TRM
- Visualización de gráficos interactivos
- Cálculo de estadísticas y análisis
- Detección de variaciones extremas (en la versión completa)
- Cálculo de promedios móviles (en la versión completa)

## Requisitos

- Python 3.8 o superior

## Instalación y Ejecución

### Opción 1: Versión Minimalista (Más Compatible)

```bash
# Dar permisos de ejecución al script (solo la primera vez)
chmod +x run_minimal.sh

# Ejecutar la aplicación
./run_minimal.sh
```

Esta versión es extremadamente simple y debería funcionar en cualquier entorno.

### Opción 2: Versión con Más Funcionalidades

```bash
# Dar permisos de ejecución al script (solo la primera vez)
chmod +x run_simple.sh

# Ejecutar la aplicación
./run_simple.sh
```

Si tienes problemas con las dependencias, puedes usar:

```bash
./run_simple.sh --clean
```

Esto eliminará el entorno virtual existente y creará uno nuevo.

## Solución de Problemas

Si encuentras errores al ejecutar la aplicación, prueba estos pasos:

1. Usa la versión minimalista con `./run_minimal.sh`
2. Limpia el entorno virtual con `./run_simple.sh --clean`
3. Verifica que el archivo de datos exista en `data/trm_data.csv`

## Datos

Los datos de la TRM se encuentran en el archivo `data/trm_data.csv`. Este archivo contiene el histórico de la TRM en Colombia desde 1991.

## Licencia

Este proyecto está bajo la Licencia MIT .
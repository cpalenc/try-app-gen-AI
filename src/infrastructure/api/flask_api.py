"""
API REST con Flask para la TRM.
"""
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
import base64
import matplotlib.pyplot as plt

from ...application.services.trm_application_service import TRMApplicationService


def create_app(trm_service=None):
    """
    Crea y configura la aplicación Flask.
    
    Args:
        trm_service: Servicio de aplicación para la TRM
        
    Returns:
        Flask: Aplicación Flask configurada
    """
    app = Flask(__name__)
    CORS(app)  # Habilitar CORS para todas las rutas
    
    # Inicializar el servicio de aplicación
    trm_app_service = trm_service or TRMApplicationService()
    
    @app.route('/api/trm', methods=['GET'])
    def get_trm_data():
        """Endpoint para obtener datos de la TRM en un rango de fechas"""
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        data = trm_app_service.get_trm_data(start_date, end_date)
        
        if not data:
            return jsonify({'error': 'No se pudieron cargar los datos'}), 500
        
        return jsonify(data)
    
    @app.route('/api/trm/stats', methods=['GET'])
    def get_trm_stats():
        """Endpoint para obtener estadísticas de la TRM"""
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        stats = trm_app_service.get_statistics(start_date, end_date)
        
        if not stats:
            return jsonify({'error': 'No se pudieron calcular las estadísticas'}), 500
        
        return jsonify(stats)
    
    @app.route('/api/trm/plot', methods=['GET'])
    def get_trm_plot():
        """Endpoint para obtener un gráfico de la TRM"""
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Generar gráfico
        fig = trm_app_service.generate_plot(start_date, end_date)
        
        if fig is None:
            return jsonify({'error': 'No se pudo generar el gráfico'}), 500
        
        # Convertir gráfico a imagen
        img_bytes = io.BytesIO()
        fig.savefig(img_bytes, format='png')
        img_bytes.seek(0)
        plt.close(fig)
        
        # Opción 1: Devolver la imagen directamente
        return send_file(img_bytes, mimetype='image/png')
        
        # Opción 2: Devolver la imagen como base64 (descomenta si prefieres esta opción)
        # img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
        # return jsonify({'image': img_base64})
    
    @app.route('/api/trm/moving-average', methods=['GET'])
    def get_moving_average():
        """Endpoint para obtener el promedio móvil de la TRM"""
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        window = int(request.args.get('window', 30))
        
        data = trm_app_service.get_moving_average(window, start_date, end_date)
        
        if not data:
            return jsonify({'error': 'No se pudo calcular el promedio móvil'}), 500
        
        return jsonify(data)
    
    @app.route('/api/trm/variations', methods=['GET'])
    def get_extreme_variations():
        """Endpoint para obtener variaciones extremas de la TRM"""
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        threshold = float(request.args.get('threshold', 1.0))
        
        data = trm_app_service.get_extreme_variations(threshold, start_date, end_date)
        
        if not data:
            return jsonify({'error': 'No se pudieron calcular las variaciones'}), 500
        
        return jsonify(data)
    
    @app.route('/api/trm/date-range', methods=['GET'])
    def get_date_range():
        """Endpoint para obtener el rango de fechas disponibles"""
        min_date, max_date = trm_app_service.get_date_range()
        
        return jsonify({
            'min_date': min_date.isoformat(),
            'max_date': max_date.isoformat()
        })
    
    return app


def run_api(host='0.0.0.0', port=None, debug=True):
    """
    Ejecuta la API REST.
    
    Args:
        host (str): Host para la API
        port (int): Puerto para la API
        debug (bool): Modo debug
    """
    # Configurar el puerto (por defecto 5000)
    if port is None:
        port = int(os.environ.get('PORT', 5000))
    
    # Crear y ejecutar la aplicación
    app = create_app()
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_api()
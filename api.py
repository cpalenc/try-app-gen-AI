from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS
from trm_data_loader import TRMDataLoader
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Inicializar el cargador de datos
trm_loader = TRMDataLoader()

@app.route('/api/trm', methods=['GET'])
def get_trm_data():
    """Endpoint para obtener datos de la TRM en un rango de fechas"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    data = trm_loader.get_data_range(start_date, end_date)
    
    if data is None:
        return jsonify({'error': 'No se pudieron cargar los datos'}), 500
    
    # Convertir a formato JSON
    result = []
    for _, row in data.iterrows():
        result.append({
            'fecha': row['fecha'].strftime('%Y-%m-%d'),
            'trm': float(row['trm'])
        })
    
    return jsonify(result)

@app.route('/api/trm/stats', methods=['GET'])
def get_trm_stats():
    """Endpoint para obtener estadísticas de la TRM"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    stats = trm_loader.get_statistics(start_date, end_date)
    
    if stats is None:
        return jsonify({'error': 'No se pudieron calcular las estadísticas'}), 500
    
    return jsonify(stats)

@app.route('/api/trm/plot', methods=['GET'])
def get_trm_plot():
    """Endpoint para obtener un gráfico de la TRM"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Generar gráfico
    fig = trm_loader.plot_trm(start_date, end_date)
    
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
    
    data = trm_loader.calculate_moving_average(window, start_date, end_date)
    
    if data is None:
        return jsonify({'error': 'No se pudo calcular el promedio móvil'}), 500
    
    # Convertir a formato JSON
    result = []
    for _, row in data.iterrows():
        result.append({
            'fecha': row['fecha'].strftime('%Y-%m-%d'),
            'trm': float(row['trm']),
            f'ma_{window}': float(row[f'ma_{window}']) if not pd.isna(row[f'ma_{window}']) else None
        })
    
    return jsonify(result)

@app.route('/api/trm/variations', methods=['GET'])
def get_extreme_variations():
    """Endpoint para obtener variaciones extremas de la TRM"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    threshold = float(request.args.get('threshold', 1.0))
    
    data = trm_loader.find_extreme_variations(threshold, start_date, end_date)
    
    if data is None:
        return jsonify({'error': 'No se pudieron calcular las variaciones'}), 500
    
    # Convertir a formato JSON
    result = []
    for _, row in data.iterrows():
        result.append({
            'fecha': row['fecha'].strftime('%Y-%m-%d'),
            'trm': float(row['trm']),
            'variacion_pct': float(row['var_pct'])
        })
    
    return jsonify(result)

if __name__ == '__main__':
    # Configurar el puerto (por defecto 5000)
    port = int(os.environ.get('PORT', 8000))
    
    # Iniciar la aplicación
    app.run(host='0.0.0.0', port=port, debug=True)
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from services.mongo_service import MongoService
from services.asignador import AsignadorColecciones

# Crear una instancia de Flask
app = Flask(__name__)
# Habilitar CORS para permitir solicitudes desde otros orígenes
CORS(app)

# Instanciar servicios necesarios
mongo_service = MongoService()
asignador = AsignadorColecciones()

@app.route('/')
def formulario():
    """
    Ruta principal que renderiza el formulario HTML.
    """
    return render_template('formulario.html')

@app.route('/api/respuestas', methods=['POST'])
def recibir_respuestas():
    try:
        data = request.json
        print("✅ Datos recibidos:", data)

        asignacion = asignador.obtener_asignacion()

        mongo_service.insertar_por_categoria(data, asignacion)
        mongo_service.insertar_resumen_completo(data)

        print("✅ Respuestas guardadas en MongoDB")
        return jsonify({"mensaje": "Respuestas guardadas correctamente en MongoDB"}), 200

    except Exception as e:
        print(f"❌ ERROR en /api/respuestas: {e}")
        return jsonify({"mensaje": "Error interno del servidor"}), 500

if __name__ == '__main__':
    # Ejecutar la aplicación en el puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

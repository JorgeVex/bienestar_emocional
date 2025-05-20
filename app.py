from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Para permitir peticiones desde el frontend si está separado

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/api/respuestas', methods=['POST'])
def recibir_respuestas():
    data = request.json
    print("Datos recibidos:", data)
    return jsonify({"mensaje": "Respuestas recibidas correctamente"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/test/nominas')
def test_nominas():
    return jsonify({"mensaje": "Servicio de nóminas funcionando", "estado": "activo"})

@app.route('/api/test/registrar_empresa', methods=['POST'])
def test_registrar_empresa():
    return jsonify({"mensaje": "Empresa registrada", "empresa_id": 1})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

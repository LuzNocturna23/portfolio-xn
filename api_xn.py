from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "sistema": "XN API Python",
        "version": "1.0.0", 
        "estado": "ACTIVO"
    })

@app.route("/enjambre")
def enjambre():
    if os.path.exists("~/sistemas-enjambre/reporte_enjambre_completo.json"):
        with open("~/sistemas-enjambre/reporte_enjambre_completo.json") as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({"error": "Reporte no encontrado"})

@app.route("/sistemas")
def sistemas():
    return jsonify({
        "sistemas_activos": [
            "arquitectura-xn",
            "sistemas-enjambre", 
            "algoritmos-python",
            "paquetes-xn",
            "mi-proyecto-rust"
        ],
        "total": 9,
        "estado": "OPERATIVO"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

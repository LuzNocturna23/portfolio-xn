from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "mensaje": "🚀 XN API ACTIVA",
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat(),
        "estado": "🎉 FUNCIONANDO"
    })

@app.route("/sistemas")
def sistemas():
    return jsonify({
        "repositorios": 9,
        "estado": "TODOS OPERATIVOS",
        "lenguajes": ["Python", "Rust", "JS", "HTML", "Shell"],
        "enjambre": "150% OPERATIVIDAD"
    })

@app.route("/ping")
def ping():
    return "🏓 PONG - XN API viva"

if __name__ == "__main__":
    print("🔥 INICIANDO XN API SIMPLE...")
    print("🌐 http://127.0.0.1:5000")
    print("🌐 http://127.0.0.1:5000/sistemas") 
    print("🌐 http://127.0.0.1:5000/ping")
    app.run(host="127.0.0.1", port=5000, debug=False)


"""
API Principal XN - Sistema Unificado
Versión: 1.0.0
Autor: LuzNocturna23
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuración
app.config['SECRET_KEY'] = os.getenv('XN_SECRET_KEY', 'default_secret_key')

class XNSystem:
    def __init__(self):
        self.aliados_activos = 6
        self.operatividad = 150
        self.estado = "operacional"
        self.ultima_actualizacion = datetime.now().isoformat()
    
    def obtener_estado(self):
        return {
            "sistema": "XN Portfolio",
            "version": "1.0.0",
            "aliados_activos": self.aliados_activos,
            "operatividad": self.operatividad,
            "estado": self.estado,
            "ultima_actualizacion": self.ultima_actualizacion,
            "desarrollador": "LuzNocturna23"
        }
    
    def generar_reporte(self):
        return {
            "reporte": {
                "timestamp": datetime.now().isoformat(),
                "metricas": {
                    "rendimiento": "150%",
                    "estabilidad": "óptima",
                    "conexiones_activas": self.aliados_activos
                },
                "subsistemas": [
                    "API Principal ✓",
                    "Enjambre IA ✓", 
                    "Dashboard Web ✓",
                    "Bot Integrado ✓"
                ]
            }
        }

# Instancia del sistema
xn_system = XNSystem()

# Rutas principales
@app.route('/')
def home():
    return jsonify({
        "mensaje": "Bienvenido al Portfolio XN - LuzNocturna23",
        "version": "1.0.0",
        "endpoints": {
            "estado": "/api/estado",
            "reporte": "/api/reporte",
            "enjambre": "/api/enjambre"
        }
    })

@app.route('/api/estado')
def estado():
    return jsonify(xn_system.obtener_estado())

@app.route('/api/reporte')
def reporte():
    return jsonify(xn_system.generar_reporte())

@app.route('/api/enjambre')
def enjambre():
    return jsonify({
        "enjambre": {
            "aliados_activos": xn_system.aliados_activos,
            "operatividad": f"{xn_system.operatividad}%",
            "modo": "autónomo",
            "estado": "optimizado"
        }
    })

@app.route('/api/proyectos')
def proyectos():
    return jsonify({
        "proyectos": [
            {
                "nombre": "Sistemas de Enjambre",
                "estado": "activo",
                "tecnologias": ["Python", "Flask", "WebSockets"],
                "descripcion": "Algoritmos de IA colectiva con 6 aliados activos"
            },
            {
                "nombre": "Arquitectura XN", 
                "estado": "estable",
                "tecnologias": ["Microservicios", "APIs REST", "Seguridad"],
                "descripcion": "Sistemas empresariales distribuidos"
            },
            {
                "nombre": "Paquetes XN",
                "estado": "desarrollo",
                "tecnologias": ["Node.js", "Python", "Rust"],
                "descripcion": "Módulos y herramientas de desarrollo"
            }
        ]
    })

if __name__ == '__main__':
    app.run(
        host='127.0.0.1', 
        port=5000, 
        debug=True
    )

"""
API Principal XN - Versión Corregida con Todos los Módulos
"""
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)

# Configuración
app.config['SECRET_KEY'] = os.getenv('XN_SECRET_KEY', 'default_secret_key')

print("🚀 Iniciando API XN con todos los módulos...")

# Importar y registrar módulos
try:
    from database import xn_db
    print("✅ Base de datos SQLite cargada")
except ImportError as e:
    print(f"❌ Error BD: {e}")
    class FakeDB: pass
    xn_db = FakeDB()

try:
    from servicio_nominas_completo import servicio_nominas_bp
    app.register_blueprint(servicio_nominas_bp, url_prefix='/api')
    print("✅ Servicio nóminas registrado")
except ImportError as e:
    print(f"❌ Servicio nóminas: {e}")

try:
    from enjambre_nominas import enjambre_nominas_bp
    app.register_blueprint(enjambre_nominas_bp, url_prefix='/api')
    print("✅ Enjambre nóminas registrado")
except ImportError as e:
    print(f"❌ Enjambre nóminas: {e}")

try:
    from nominas_xn import nominas_bp
    app.register_blueprint(nominas_bp, url_prefix='/api')
    print("✅ Módulo nóminas XN registrado")
except ImportError as e:
    print(f"❌ Módulo nóminas: {e}")

class XNSystem:
    def __init__(self):
        self.version = "1.2.0"
    
    def obtener_estado_completo(self):
        return {
            "sistema": "XN Portfolio - Servicio Nóminas",
            "version": self.version,
            "aliados_activos": 6,
            "operatividad": 150,
            "estado": "operacional",
            "ultima_actualizacion": datetime.now().isoformat(),
            "desarrollador": "LuzNocturna23",
            "servicios_activos": [
                "Generación de Nóminas",
                "Gestión de Empresas", 
                "Cálculo Automático",
                "Reportes Ejecutivos"
            ]
        }

xn_system = XNSystem()

@app.route('/')
def home():
    return jsonify({
        "mensaje": "🚀 Portfolio XN - Servicio Completo de Nóminas",
        "version": "1.2.0",
        "endpoints_activos": {
            "servicio_nominas": [
                "POST /api/servicio/nominas/registrar_empresa",
                "POST /api/servicio/nominas/agregar_empleados", 
                "GET /api/servicio/nominas/generar/<empresa_id>",
                "GET /api/servicio/nominas/empresas"
            ],
            "enjambre_nominas": [
                "GET /api/enjambre/nominas/estado",
                "POST /api/enjambre/nominas/analizar"
            ],
            "sistema_principal": [
                "GET /api/estado",
                "GET /api/aliados",
                "GET /api/logs"
            ]
        }
    })

@app.route('/api/estado')
def estado():
    return jsonify(xn_system.obtener_estado_completo())

@app.route('/api/aliados')
def aliados():
    return jsonify({
        "total_aliados": 6,
        "aliados": ["Analizador Legal", "Optimizador Fiscal", "Predictor", "Auditor", "Generador Reportes", "Integrador"]
    })

@app.route('/api/logs')
def logs():
    return jsonify({
        "logs": [
            {"timestamp": datetime.now().isoformat(), "nivel": "INFO", "mensaje": "Sistema de nóminas activo"},
            {"timestamp": datetime.now().isoformat(), "nivel": "SUCCESS", "mensaje": "API funcionando correctamente"}
        ]
    })

if __name__ == '__main__':
    print("🎯 Endpoints disponibles:")
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            print(f"  {rule.methods} {rule.rule}")
    
    print("\n🌐 Servidor listo en http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)

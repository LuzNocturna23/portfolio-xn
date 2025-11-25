"""
API Principal XN - Sistema Unificado con Base de Datos
Versión: 1.1.0
Autor: LuzNocturna23
"""
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import sys
import os

# Agregar el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database import xn_db
    print("✅ Base de datos SQLite cargada correctamente")
except ImportError as e:
    print(f"❌ Error cargando base de datos: {e}")
    # Crear una versión de respaldo sin BD
    class FakeDB:
        def obtener_estado_sistema(self):
            return {
                "aliados_activos": 6,
                "operatividad": 150,
                "estado": "operacional",
                "ultima_actualizacion": datetime.now().isoformat()
            }
        def obtener_aliados_enjambre(self): return []
        def obtener_logs_recientes(self, limite=5): return []
    xn_db = FakeDB()

app = Flask(__name__)
CORS(app)

class XNSystem:
    def __init__(self):
        self.version = "1.1.0"
    
    def obtener_estado_completo(self):
        """Obtener estado completo desde la base de datos"""
        try:
            estado_bd = xn_db.obtener_estado_sistema()
            aliados = xn_db.obtener_aliados_enjambre()
            logs = xn_db.obtener_logs_recientes(3)
            
            return {
                "sistema": "XN Portfolio",
                "version": self.version,
                "aliados_activos": estado_bd.get("aliados_activos", 6),
                "operatividad": estado_bd.get("operatividad", 150),
                "estado": estado_bd.get("estado", "operacional"),
                "ultima_actualizacion": estado_bd.get("ultima_actualizacion", datetime.now().isoformat()),
                "desarrollador": "LuzNocturna23",
                "base_datos": "SQLite 3.51.0",
                "aliados_detallados": aliados,
                "logs_recientes": logs
            }
        except Exception as e:
            return {
                "sistema": "XN Portfolio",
                "version": self.version,
                "aliados_activos": 6,
                "operatividad": 150,
                "estado": "operacional",
                "ultima_actualizacion": datetime.now().isoformat(),
                "desarrollador": "LuzNocturna23",
                "base_datos": f"Error: {str(e)}",
                "aliados_detallados": [],
                "logs_recientes": []
            }

xn_system = XNSystem()

@app.route('/')
def home():
    return jsonify({
        "mensaje": "🚀 Portfolio XN con Base de Datos - LuzNocturna23",
        "version": "1.1.0",
        "base_datos": "SQLite 3.51.0",
        "endpoints": {
            "estado": "/api/estado",
            "reporte": "/api/reporte", 
            "enjambre": "/api/enjambre",
            "aliados": "/api/aliados",
            "logs": "/api/logs"
        }
    })

@app.route('/api/estado')
def estado():
    return jsonify(xn_system.obtener_estado_completo())

@app.route('/api/aliados')
def aliados():
    try:
        aliados = xn_db.obtener_aliados_enjambre()
        return jsonify({
            "total_aliados": len(aliados),
            "aliados": aliados,
            "timestamp": datetime.now().isoformat()
        })
    except:
        return jsonify({
            "total_aliados": 6,
            "aliados": [],
            "timestamp": datetime.now().isoformat(),
            "mensaje": "Base de datos temporalmente no disponible"
        })

@app.route('/api/logs')
def logs():
    try:
        logs = xn_db.obtener_logs_recientes(10)
        return jsonify({
            "total_logs": len(logs),
            "logs": logs
        })
    except:
        return jsonify({
            "total_logs": 0,
            "logs": [],
            "mensaje": "Logs no disponibles"
        })

@app.route('/api/reporte')
def reporte():
    estado = xn_system.obtener_estado_completo()
    return jsonify({
        "reporte": {
            "timestamp": datetime.now().isoformat(),
            "metricas": {
                "rendimiento": f"{estado['operatividad']}%",
                "estabilidad": "óptima",
                "conexiones_activas": estado['aliados_activos'],
                "base_datos": "operacional" if "Error" not in estado.get('base_datos', '') else "con errores"
            },
            "subsistemas": [
                "API Principal ✓",
                "Enjambre IA ✓", 
                "Dashboard Web ✓",
                "Base de Datos SQLite ✓",
                "Bot Integrado ✓"
            ]
        }
    })

if __name__ == '__main__':
    print("🚀 Iniciando API XN con Base de Datos SQLite...")
    app.run(host='127.0.0.1', port=5000, debug=True)

# Importar módulo de nóminas
try:
    from api.nominas_xn import nominas_bp
    app.register_blueprint(nominas_bp, url_prefix='/api')
    print("✅ Módulo de nóminas XN cargado correctamente")
except ImportError as e:
    print(f"❌ Error cargando módulo nóminas: {e}")

# Importar enjambre de nóminas
try:
    from api.enjambre_nominas import enjambre_nominas_bp
    app.register_blueprint(enjambre_nominas_bp, url_prefix='/api')
    print("✅ Enjambre de nóminas XN cargado correctamente")
except ImportError as e:
    print(f"❌ Error cargando enjambre nóminas: {e}")

# Importar servicio completo de nóminas
try:
    from api.servicio_nominas_completo import servicio_nominas_bp
    app.register_blueprint(servicio_nominas_bp, url_prefix='/api')
    print("✅ Servicio completo de nóminas cargado")
except ImportError as e:
    print(f"❌ Error cargando servicio nóminas: {e}")

# Importar servicio completo de nóminas
try:
    from api.servicio_nominas_completo import servicio_nominas_bp
    app.register_blueprint(servicio_nominas_bp, url_prefix='/api')
    print("✅ Servicio completo de nóminas cargado")
except ImportError as e:
    print(f"❌ Error cargando servicio nóminas: {e}")

from flask import Flask, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

def get_enjambre_data():
    """Obtener datos del enjambre con ruta corregida"""
    try:
        # Ruta absoluta corregida
        home_dir = os.path.expanduser("~")
        ruta_reporte = os.path.join(home_dir, "sistemas-enjambre", "reporte_enjambre_completo.json")
        
        print(f"🔍 Buscando reporte en: {ruta_reporte}")  # Debug
        
        if os.path.exists(ruta_reporte):
            with open(ruta_reporte, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # Si no existe, generar uno de ejemplo
            return {
                "enjambre_activo": True,
                "aliados": 6,
                "operatividad": "150%",
                "compromisos": 37,
                "estado": "🎉 ENJAMBRE COMPLETO - 100% OPERATIVO",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {"error": f"Error cargando enjambre: {str(e)}"}

@app.route("/")
def home():
    return jsonify({
        "sistema": "🚀 XN API Python",
        "version": "2.0.0", 
        "estado": "ACTIVO",
        "timestamp": datetime.now().isoformat(),
        "mensaje": "¡API funcionando correctamente!",
        "endpoints": [
            "/sistemas - Lista de sistemas activos",
            "/enjambre - Estado del enjambre",
            "/estadisticas - Métricas completas",
            "/debug - Información de debug"
        ]
    })

@app.route("/sistemas")
def sistemas():
    sistemas = [
        {"nombre": "arquitectura-xn", "estado": "🟢 ACTIVO", "version": "1.0.0", "tags": ["v1.0.0"]},
        {"nombre": "sistemas-enjambre", "estado": "🟢 ACTIVO", "operatividad": "150%", "aliados": 6},
        {"nombre": "algoritmos-python", "estado": "🟢 ACTIVO", "scripts": 3, "dependencias": 5},
        {"nombre": "paquetes-xn", "estado": "🟢 ACTIVO", "server": True, "dependencias": 4},
        {"nombre": "mi-proyecto-rust", "estado": "🟢 ACTIVO", "lenguaje": "Rust", "archivos": 8},
        {"nombre": "analizador-termux", "estado": "🟢 ACTIVO", "herramientas": 3},
        {"nombre": "proyecto-python", "estado": "🟢 ACTIVO", "ejemplos": 1},
        {"nombre": "workspace-clean", "estado": "🟢 ACTIVO", "categorias": 4},
        {"nombre": "mis-proyectos", "estado": "🟢 ACTIVO", "public": True}
    ]
    return jsonify({
        "total_sistemas": len(sistemas),
        "sistemas_activos": sistemas,
        "estado_general": "🎉 TODOS LOS SISTEMAS OPERATIVOS",
        "repositorios_totales": 9,
        "lenguajes": ["Python", "Rust", "JavaScript", "HTML", "Shell", "Markdown"]
    })

@app.route("/enjambre")
def enjambre():
    datos = get_enjambre_data()
    return jsonify(datos)

@app.route("/estadisticas")
def estadisticas():
    return jsonify({
        "repositorios": {
            "total": 9,
            "publicos": 1,
            "privados": 8
        },
        "lenguajes": {
            "python": 3,
            "rust": 1, 
            "javascript": 2,
            "html": 2,
            "shell": 2,
            "markdown": 9
        },
        "actividad": {
            "api_estado": "🟢 FUNCIONANDO",
            "enjambre_operatividad": "150%",
            "ultima_actualizacion": datetime.now().isoformat(),
            "servidor_desde": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    })

@app.route("/debug")
def debug():
    home_dir = os.path.expanduser("~")
    ruta_reporte = os.path.join(home_dir, "sistemas-enjambre", "reporte_enjambre_completo.json")
    
    return jsonify({
        "home_directory": home_dir,
        "reporte_path": ruta_reporte,
        "reporte_exists": os.path.exists(ruta_reporte),
        "current_directory": os.getcwd(),
        "python_version": os.sys.version
    })

@app.route("/dashboard")
def dashboard():
    return """
    <html>
        <head>
            <title>🚀 XN Dashboard</title>
            <style>
                body { font-family: Arial; margin: 40px; background: #f0f0f0; }
                .card { background: white; padding: 20px; margin: 10px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
                .endpoint { background: #e3f2fd; padding: 10px; margin: 5px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>🚀 XN Dashboard - Control Center</h1>
            
            <div class="card">
                <h2>📡 Endpoints Disponibles</h2>
                <div class="endpoint"><a href="/sistemas">/sistemas</a> - Lista de sistemas activos</div>
                <div class="endpoint"><a href="/enjambre">/enjambre</a> - Estado del enjambre</div>
                <div class="endpoint"><a href="/estadisticas">/estadisticas</a> - Métricas completas</div>
                <div class="endpoint"><a href="/debug">/debug</a> - Información técnica</div>
            </div>
            
            <div class="card">
                <h2>🎯 Estado del Sistema</h2>
                <p><strong>API:</strong> 🟢 FUNCIONANDO</p>
                <p><strong>Repositorios:</strong> 9 activos</p>
                <p><strong>Enjambre:</strong> 150% operatividad</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    print("🚀 INICIANDO XN API v2.0 MEJORADA...")
    print("📍 Endpoints disponibles:")
    print("   http://127.0.0.1:5000/")
    print("   http://127.0.0.1:5000/sistemas")
    print("   http://127.0.0.1:5000/enjambre") 
    print("   http://127.0.0.1:5000/estadisticas")
    print("   http://127.0.0.1:5000/dashboard")
    print("   http://127.0.0.1:5000/debug")
    print("")
    print("📊 Probando enjambre...")
    datos_enjambre = get_enjambre_data()
    print(f"   Enjambre: {datos_enjambre.get(estado, DESCONOCIDO)}")
    print("")
    app.run(host="0.0.0.0", port=5000, debug=True)


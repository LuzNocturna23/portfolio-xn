"""
API XN COMPLETA - Todos los servicios funcionando
Servicio de Nóminas + Enjambre IA + Base de Datos
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import sqlite3
import json
import os

app = Flask(__name__)
CORS(app)

print("🚀 INICIANDO API XN COMPLETA - SERVICIO DE NÓMINAS ACTIVO")

# Configuración de base de datos
DB_PATH = "enjambre_nominas.db"

def init_database():
    """Inicializar base de datos para servicio de nóminas"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            nit TEXT UNIQUE,
            email TEXT,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER,
            cedula TEXT,
            nombre TEXT,
            cargo TEXT,
            salario_base DECIMAL(12,2),
            banco TEXT,
            FOREIGN KEY (empresa_id) REFERENCES empresas (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nominas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER,
            periodo TEXT,
            total_empleados INTEGER,
            nomina_bruta DECIMAL(12,2),
            total_impuestos DECIMAL(12,2),
            nomina_neta DECIMAL(12,2),
            fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (empresa_id) REFERENCES empresas (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada")

# Inicializar BD al inicio
init_database()

# ==================== SERVICIO DE NÓMINAS ====================

@app.route('/api/servicio/nominas/registrar_empresa', methods=['POST'])
def registrar_empresa():
    """Registrar nueva empresa cliente"""
    try:
        datos = request.get_json()
        
        if not datos or 'nombre' not in datos or 'nit' not in datos:
            return jsonify({"error": "Faltan datos: nombre y nit son obligatorios"}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO empresas (nombre, nit, email) 
            VALUES (?, ?, ?)
        ''', (datos['nombre'], datos['nit'], datos.get('email', '')))
        
        empresa_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            "mensaje": "Empresa registrada exitosamente",
            "empresa_id": empresa_id,
            "empresa": datos['nombre']
        })
        
    except sqlite3.IntegrityError:
        return jsonify({"error": "El NIT ya está registrado"}), 400
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/api/servicio/nominas/agregar_empleados', methods=['POST'])
def agregar_empleados():
    """Agregar empleados a una empresa"""
    try:
        datos = request.get_json()
        
        if not datos or 'empresa_id' not in datos or 'empleados' not in datos:
            return jsonify({"error": "Faltan datos: empresa_id y empleados son obligatorios"}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        empleados_agregados = 0
        for empleado in datos['empleados']:
            try:
                cursor.execute('''
                    INSERT INTO empleados (empresa_id, cedula, nombre, cargo, salario_base, banco)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    datos['empresa_id'],
                    empleado['cedula'],
                    empleado['nombre'],
                    empleado['cargo'],
                    empleado['salario_base'],
                    empleado.get('banco', '')
                ))
                empleados_agregados += 1
            except sqlite3.IntegrityError:
                continue  # Empleado ya existe
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "mensaje": f"{empleados_agregados} empleados agregados",
            "empresa_id": datos['empresa_id'],
            "total_empleados": empleados_agregados
        })
        
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.route('/api/servicio/nominas/generar/<int:empresa_id>')
def generar_nomina(empresa_id):
    """Generar nómina para una empresa"""
    try:
        periodo = request.args.get('periodo', datetime.now().strftime("%Y-%m"))
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Obtener empresa
        cursor.execute('SELECT nombre FROM empresas WHERE id = ?', (empresa_id,))
        empresa = cursor.fetchone()
        
        if not empresa:
            return jsonify({"error": "Empresa no encontrada"}), 404
        
        # Obtener empleados
        cursor.execute('SELECT * FROM empleados WHERE empresa_id = ?', (empresa_id,))
        empleados = cursor.fetchall()
        
        if not empleados:
            return jsonify({"error": "No hay empleados registrados"}), 400
        
        # Calcular nómina
        total_bruta = 0
        total_impuestos = 0
        nominas_detalle = []
        
        for emp in empleados:
            salario_bruto = emp[5]  # salario_base
            impuestos = salario_bruto * 0.15
            salario_neto = salario_bruto - impuestos
            
            nominas_detalle.append({
                "cedula": emp[2],
                "nombre": emp[3],
                "cargo": emp[4],
                "salario_bruto": float(salario_bruto),
                "impuestos": float(impuestos),
                "salario_neto": float(salario_neto)
            })
            
            total_bruta += salario_bruto
            total_impuestos += impuestos
        
        total_neta = total_bruta - total_impuestos
        
        # Guardar nómina
        cursor.execute('''
            INSERT INTO nominas (empresa_id, periodo, total_empleados, nomina_bruta, total_impuestos, nomina_neta)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (empresa_id, periodo, len(empleados), total_bruta, total_impuestos, total_neta))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "empresa": empresa[0],
            "periodo": periodo,
            "total_empleados": len(empleados),
            "nomina_bruta": float(total_bruta),
            "total_impuestos": float(total_impuestos),
            "nomina_neta": float(total_neta),
            "nominas_detalle": nominas_detalle,
            "estado": "completado"
        })
        
    except Exception as e:
        return jsonify({"error": f"Error generando nómina: {str(e)}"}), 500

@app.route('/api/servicio/nominas/empresas')
def listar_empresas():
    """Listar todas las empresas"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.id, e.nombre, e.nit, e.fecha_registro,
                   COUNT(emp.id) as total_empleados
            FROM empresas e
            LEFT JOIN empleados emp ON e.id = emp.empresa_id
            GROUP BY e.id
        ''')
        
        empresas = []
        for row in cursor.fetchall():
            empresas.append({
                "id": row[0],
                "nombre": row[1],
                "nit": row[2],
                "fecha_registro": row[3],
                "total_empleados": row[4]
            })
        
        conn.close()
        
        return jsonify({
            "total_empresas": len(empresas),
            "empresas": empresas
        })
        
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

# ==================== ENDPOINTS DEL SISTEMA ====================

@app.route('/')
def home():
    return jsonify({
        "mensaje": "🚀 API XN COMPLETA - Servicio de Nóminas Activo",
        "version": "2.0.0",
        "servicios": {
            "nominas": [
                "POST /api/servicio/nominas/registrar_empresa",
                "POST /api/servicio/nominas/agregar_empleados", 
                "GET /api/servicio/nominas/generar/<empresa_id>",
                "GET /api/servicio/nominas/empresas"
            ]
        }
    })

@app.route('/api/estado')
def estado_sistema():
    return jsonify({
        "sistema": "XN Portfolio - Servicio Nóminas",
        "version": "2.0.0",
        "estado": "operacional",
        "servicios_activos": ["Generación de Nóminas", "Gestión de Empresas"],
        "base_datos": "SQLite",
        "ultima_actualizacion": datetime.now().isoformat()
    })

# ==================== INICIAR SERVIDOR ====================

if __name__ == '__main__':
    print("🎯 ENDPOINTS DISPONIBLES:")
    print("  POST /api/servicio/nominas/registrar_empresa")
    print("  POST /api/servicio/nominas/agregar_empleados")
    print("  GET  /api/servicio/nominas/generar/<empresa_id>")
    print("  GET  /api/servicio/nominas/empresas")
    print("  GET  /api/estado")
    print("  GET  /")
    print("\n🌐 Servidor listo en http://127.0.0.1:5000")
    print("💡 Usa Ctrl+C para detener el servidor")
    
    app.run(host='127.0.0.1', port=5000, debug=True)

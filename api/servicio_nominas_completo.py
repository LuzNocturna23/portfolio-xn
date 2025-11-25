"""
SERVICIO COMPLETO DE NÓMINAS - Enjambre XN
Generación automática de nóminas para empresas
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import sqlite3
import json

servicio_nominas_bp = Blueprint('servicio_nominas', __name__)

class ServicioNominasCompleto:
    def __init__(self):
        self.db_path = "enjambre_nominas.db"
        self.init_database()
    
    def init_database(self):
        """Inicializar base de datos para servicio de nóminas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de empresas clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empresas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                nit TEXT UNIQUE,
                direccion TEXT,
                telefono TEXT,
                email TEXT,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                estado TEXT DEFAULT 'activa'
            )
        ''')
        
        # Tabla de empleados por empresa
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleados_empresas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empresa_id INTEGER,
                cedula TEXT,
                nombre TEXT,
                cargo TEXT,
                salario_base DECIMAL(12,2),
                tipo_contrato TEXT,
                banco TEXT,
                numero_cuenta TEXT,
                FOREIGN KEY (empresa_id) REFERENCES empresas (id)
            )
        ''')
        
        # Tabla de nóminas generadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nominas_generadas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empresa_id INTEGER,
                periodo TEXT,
                total_empleados INTEGER,
                nomina_bruta DECIMAL(12,2),
                total_impuestos DECIMAL(12,2),
                nomina_neta DECIMAL(12,2),
                archivo_json TEXT,
                fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (empresa_id) REFERENCES empresas (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def registrar_empresa(self, datos_empresa):
        """Registrar nueva empresa cliente"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO empresas (nombre, nit, direccion, telefono, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datos_empresa['nombre'],
                datos_empresa['nit'],
                datos_empresa.get('direccion', ''),
                datos_empresa.get('telefono', ''),
                datos_empresa.get('email', '')
            ))
            
            empresa_id = cursor.lastrowid
            conn.commit()
            
            print(f"✅ Empresa registrada: {datos_empresa['nombre']} (ID: {empresa_id})")
            return empresa_id
            
        except sqlite3.IntegrityError:
            print(f"❌ Empresa con NIT {datos_empresa['nit']} ya existe")
            return None
        finally:
            conn.close()
    
    def agregar_empleados(self, empresa_id, lista_empleados):
        """Agregar empleados a una empresa"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        empleados_agregados = 0
        for empleado in lista_empleados:
            try:
                cursor.execute('''
                    INSERT INTO empleados_empresas 
                    (empresa_id, cedula, nombre, cargo, salario_base, tipo_contrato, banco, numero_cuenta)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    empresa_id,
                    empleado['cedula'],
                    empleado['nombre'],
                    empleado['cargo'],
                    empleado['salario_base'],
                    empleado.get('tipo_contrato', 'termino_fijo'),
                    empleado.get('banco', ''),
                    empleado.get('numero_cuenta', '')
                ))
                empleados_agregados += 1
            except sqlite3.IntegrityError:
                print(f"⚠️  Empleado {empleado['cedula']} ya existe")
        
        conn.commit()
        conn.close()
        
        print(f"✅ {empleados_agregados} empleados agregados a empresa ID: {empresa_id}")
        return empleados_agregados
    
    def generar_nomina_empresa(self, empresa_id, periodo=None):
        """Generar nómina completa para una empresa"""
        if not periodo:
            periodo = datetime.now().strftime("%Y-%m")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Obtener datos de la empresa
        cursor.execute('SELECT * FROM empresas WHERE id = ?', (empresa_id,))
        empresa = cursor.fetchone()
        
        if not empresa:
            return {"error": "Empresa no encontrada"}
        
        # Obtener empleados activos
        cursor.execute('''
            SELECT * FROM empleados_empresas 
            WHERE empresa_id = ?
        ''', (empresa_id,))
        
        empleados = cursor.fetchall()
        
        if not empleados:
            return {"error": "No hay empleados registrados"}
        
        # Procesar nómina para cada empleado
        nominas_detalladas = []
        total_nomina_bruta = 0
        total_impuestos = 0
        
        for empleado in empleados:
            salario_bruto = empleado[5]  # salario_base
            impuestos = salario_bruto * 0.15  # 15% ISR
            salario_neto = salario_bruto - impuestos
            
            nomina_empleado = {
                "cedula": empleado[2],
                "nombre": empleado[3],
                "cargo": empleado[4],
                "salario_bruto": float(salario_bruto),
                "impuestos": float(impuestos),
                "salario_neto": float(salario_neto),
                "banco": empleado[7],
                "cuenta": empleado[8],
                "periodo": periodo
            }
            
            nominas_detalladas.append(nomina_empleado)
            total_nomina_bruta += salario_bruto
            total_impuestos += impuestos
        
        total_nomina_neta = total_nomina_bruta - total_impuestos
        
        # Guardar nómina en base de datos
        archivo_json = f"nominas/{empresa_id}_{periodo}.json"
        
        cursor.execute('''
            INSERT INTO nominas_generadas 
            (empresa_id, periodo, total_empleados, nomina_bruta, total_impuestos, nomina_neta, archivo_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            empresa_id,
            periodo,
            len(empleados),
            float(total_nomina_bruta),
            float(total_impuestos),
            float(total_nomina_neta),
            archivo_json
        ))
        
        conn.commit()
        conn.close()
        
        # Guardar archivo JSON con detalles
        self.guardar_archivo_nomina(empresa_id, periodo, nominas_detalladas, {
            "empresa": empresa[1],
            "nit": empresa[2],
            "periodo": periodo,
            "resumen": {
                "total_empleados": len(empleados),
                "nomina_bruta": float(total_nomina_bruta),
                "total_impuestos": float(total_impuestos),
                "nomina_neta": float(total_nomina_neta)
            }
        })
        
        return {
            "empresa": empresa[1],
            "periodo": periodo,
            "total_empleados": len(empleados),
            "nomina_bruta": float(total_nomina_bruta),
            "total_impuestos": float(total_impuestos),
            "nomina_neta": float(total_nomina_neta),
            "nominas_detalladas": nominas_detalladas,
            "archivo_generado": archivo_json,
            "estado": "completado"
        }
    
    def guardar_archivo_nomina(self, empresa_id, periodo, nominas_detalladas, metadata):
        """Guardar archivo JSON con la nómina generada"""
        import os
        os.makedirs("nominas", exist_ok=True)
        
        archivo_path = f"nominas/{empresa_id}_{periodo}.json"
        
        datos_completos = {
            "metadata": metadata,
            "nominas": nominas_detalladas,
            "fecha_generacion": datetime.now().isoformat(),
            "sistema": "Enjambre XN - Servicio de Nóminas"
        }
        
        with open(archivo_path, 'w', encoding='utf-8') as f:
            json.dump(datos_completos, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Archivo de nómina guardado: {archivo_path}")

servicio_nominas = ServicioNominasCompleto()

@servicio_nominas_bp.route('/servicio/nominas/registrar_empresa', methods=['POST'])
def registrar_empresa():
    """Registrar nueva empresa para servicio de nóminas"""
    datos_empresa = request.get_json()
    
    if not datos_empresa or 'nombre' not in datos_empresa or 'nit' not in datos_empresa:
        return jsonify({"error": "Datos incompletos"}), 400
    
    empresa_id = servicio_nominas.registrar_empresa(datos_empresa)
    
    if empresa_id:
        return jsonify({
            "mensaje": "Empresa registrada exitosamente",
            "empresa_id": empresa_id,
            "estado": "activa"
        })
    else:
        return jsonify({"error": "Error registrando empresa"}), 400

@servicio_nominas_bp.route('/servicio/nominas/agregar_empleados', methods=['POST'])
def agregar_empleados():
    """Agregar empleados a una empresa"""
    datos = request.get_json()
    
    if not datos or 'empresa_id' not in datos or 'empleados' not in datos:
        return jsonify({"error": "Datos incompletos"}), 400
    
    empleados_agregados = servicio_nominas.agregar_empleados(
        datos['empresa_id'], 
        datos['empleados']
    )
    
    return jsonify({
        "empleados_agregados": empleados_agregados,
        "empresa_id": datos['empresa_id']
    })

@servicio_nominas_bp.route('/servicio/nominas/generar/<int:empresa_id>')
def generar_nomina_empresa(empresa_id):
    """Generar nómina para una empresa"""
    periodo = request.args.get('periodo')
    
    resultado = servicio_nominas.generar_nomina_empresa(empresa_id, periodo)
    
    return jsonify({
        "servicio": "generacion_nominas",
        "resultado": resultado
    })

@servicio_nominas_bp.route('/servicio/nominas/empresas')
def listar_empresas():
    """Listar todas las empresas registradas"""
    conn = sqlite3.connect(servicio_nominas.db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT e.id, e.nombre, e.nit, e.estado, 
               COUNT(emp.id) as total_empleados,
               MAX(n.fecha_generacion) as ultima_nomina
        FROM empresas e
        LEFT JOIN empleados_empresas emp ON e.id = emp.empresa_id
        LEFT JOIN nominas_generadas n ON e.id = n.empresa_id
        GROUP BY e.id
    ''')
    
    empresas = []
    for row in cursor.fetchall():
        empresas.append({
            "id": row[0],
            "nombre": row[1],
            "nit": row[2],
            "estado": row[3],
            "total_empleados": row[4],
            "ultima_nomina": row[5]
        })
    
    conn.close()
    
    return jsonify({
        "total_empresas": len(empresas),
        "empresas": empresas
    })

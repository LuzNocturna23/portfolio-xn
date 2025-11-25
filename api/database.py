import sqlite3
import json
from datetime import datetime

class XNDatabase:
    def __init__(self, db_path="xn_system.db"):
        self.db_path = db_path
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def obtener_estado_sistema(self):
        """Obtener el estado actual del sistema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT aliados_activos, operatividad, estado, timestamp 
            FROM system_metrics 
            ORDER BY id DESC LIMIT 1
        ''')
        
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            return {
                "aliados_activos": resultado[0],
                "operatividad": resultado[1],
                "estado": resultado[2],
                "ultima_actualizacion": resultado[3]
            }
        return None
    
    def obtener_aliados_enjambre(self):
        """Obtener lista de aliados del enjambre"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nombre, tipo, estado, carga_trabajo, ultima_comunicacion
            FROM enjambre_aliados
            ORDER BY id
        ''')
        
        aliados = []
        for row in cursor.fetchall():
            aliados.append({
                "id": row[0],
                "nombre": row[1],
                "tipo": row[2],
                "estado": row[3],
                "carga_trabajo": row[4],
                "ultima_comunicacion": row[5]
            })
        
        conn.close()
        return aliados
    
    def guardar_metrica(self, aliados_activos, operatividad, estado, carga_sistema=75.5):
        """Guardar nueva métrica del sistema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO system_metrics 
            (aliados_activos, operatividad, estado, carga_sistema)
            VALUES (?, ?, ?, ?)
        ''', (aliados_activos, operatividad, estado, carga_sistema))
        
        conn.commit()
        conn.close()
        return True
    
    def obtener_logs_recientes(self, limite=5):
        """Obtener logs recientes del sistema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp, nivel, modulo, mensaje 
            FROM system_logs 
            ORDER BY id DESC 
            LIMIT ?
        ''', (limite,))
        
        logs = []
        for row in cursor.fetchall():
            logs.append({
                "timestamp": row[0],
                "nivel": row[1],
                "modulo": row[2],
                "mensaje": row[3]
            })
        
        conn.close()
        return logs

# Instancia global de la base de datos
xn_db = XNDatabase()

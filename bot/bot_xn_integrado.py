#!/bin/env python3
import os
import json
from datetime import datetime

class XNBotIntegrado:
    def __init__(self):
        self.nombre = "Bot XN Integrado"
        self.version = "1.0.0"
        self.sistemas = {
            "enjambre": "~/sistemas-enjambre",
            "arquitectura": "~/arquitectura-xn", 
            "algoritmos": "~/algoritmos-python",
            "rust": "~/mi_proyecto_rust",
            "herramientas": "~/analizador-termux"
        }
    
    def activar_sistema(self):
        print("🚀 ACTIVANDO BOT XN INTEGRADO")
        print(f"🤖 {self.nombre} v{self.version}")
        print("📋 SISTEMAS DISPONIBLES:")
        
        for nombre, ruta in self.sistemas.items():
            if os.path.exists(os.path.expanduser(ruta)):
                print(f"   ✅ {nombre.upper()} - Conectado")
            else:
                print(f"   ❌ {nombre.upper()} - No encontrado")
    
    def generar_reporte(self):
        print("\n📊 GENERANDO REPORTE DE SISTEMAS...")
        reporte = {
            "timestamp": datetime.now().isoformat(),
            "bot": self.nombre,
            "sistemas_activos": [],
            "estado": "OPERATIVO"
        }
        
        for nombre, ruta in self.sistemas.items():
            if os.path.exists(os.path.expanduser(ruta)):
                reporte["sistemas_activos"].append(nombre)
        
        print(f"🎯 Sistemas activos: {len(reporte[sistemas_activos])}/5")
        print(f"📈 Estado: {reporte[estado]}")
        
        # Guardar reporte
        with open("reporte_xn_bot.json", "w") as f:
            json.dump(reporte, f, indent=2)
        print("💾 Reporte guardado en: reporte_xn_bot.json")
    
    def ejecutar_enjambre(self):
        print("\n🐝 EJECUTANDO SISTEMA DE ENJAMBRE...")
        os.system("cd ~/sistemas-enjambre && python algoritmos/revelador_enjambre_final.py")

# Crear y activar el bot
if __name__ == "__main__":
    bot = XNBotIntegrado()
    bot.activar_sistema()
    bot.generar_reporte()
    bot.ejecutar_enjambre()
    print("\n🎉 ¡BOT XN INTEGRADO ACTIVADO CORRECTAMENTE!")

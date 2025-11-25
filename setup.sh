#!/bin/bash
# Script de instalación Portfolio XN

echo "🚀 Instalando Portfolio XN..."
echo "📁 Creando estructura de proyectos..."

# Verificar dependencias
if command -v python &> /dev/null; then
    echo "✅ Python encontrado"
else
    echo "❌ Python no instalado"
    exit 1
fi

if command -v git &> /dev/null; then
    echo "✅ Git encontrado"
else
    echo "❌ Git no instalado" 
    exit 1
fi

# Instalar dependencias Python
echo "📦 Instalando dependencias..."
pip install flask requests

echo "🎉 Instalación completada!"
echo "🌐 Para ejecutar: python api_simple.py"
echo "📊 Dashboard: abrir dashboard.html"

#!/bin/bash
echo "🚀 Instalando GitHub Projects CLI..."
echo ""

# Instalar dependencias Python si es necesario
pip install requests

# Crear enlace simbólico para usar globalmente
if [ ! -f "/data/data/com.termux/files/usr/bin/github-projects" ]; then
    ln -s "$(pwd)/github_projects.py" /data/data/com.termux/files/usr/bin/github-projects
    echo "✅ Comando 'github-projects' instalado globalmente"
else
    echo "⚠️  El comando ya existe"
fi

echo ""
echo "🎯 USO:"
echo "  github-projects config --token TU_TOKEN_GITHUB"
echo "  github-projects create-project 'Mi Proyecto'"
echo "  github-projects add-card 'Mi Proyecto' 'Nueva tarea'"
echo "  github-projects list"
echo ""
echo "📝 Primero obtén un token de GitHub:"
echo "https://github.com/settings/tokens"

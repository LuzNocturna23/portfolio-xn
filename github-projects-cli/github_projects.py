#!/usr/bin/env python3
"""
🚀 GitHub Projects CLI - Gestiona Projects de GitHub desde Termux
Autor: LuzNocturna23
Repositorio: https://github.com/LuzNocturna23/portfolio-xn
"""

import os
import json
import requests
import argparse
from datetime import datetime

class GitHubProjectsCLI:
    def __init__(self):
        self.config_file = "github_config.json"
        self.load_config()
    
    def load_config(self):
        """Cargar configuración de GitHub"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "username": "LuzNocturna23",
                "repository": "portfolio-xn",
                "token": "YOUR_GITHUB_TOKEN_HERE"
            }
            self.save_config()
            print("⚠️  Configuración inicial creada. Edita github_config.json con tu token")
    
    def save_config(self):
        """Guardar configuración"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def set_token(self, token):
        """Establecer token de GitHub"""
        self.config['token'] = token
        self.save_config()
        print("✅ Token guardado correctamente")
    
    def create_project(self, name, description=""):
        """Crear un nuevo proyecto (simulación - GitHub no tiene API pública para Projects)"""
        project_data = {
            "name": name,
            "description": description,
            "columns": ["📋 Backlog", "🔄 En Progreso", "✅ Completado"],
            "created_at": datetime.now().isoformat(),
            "status": "planned"
        }
        
        # Guardar localmente
        projects_file = "github_projects.json"
        if os.path.exists(projects_file):
            with open(projects_file, 'r') as f:
                projects = json.load(f)
        else:
            projects = []
        
        projects.append(project_data)
        
        with open(projects_file, 'w') as f:
            json.dump(projects, f, indent=2)
        
        print(f"✅ Proyecto '{name}' creado localmente")
        print("📋 Para crear en GitHub, ejecuta:")
        print(f"termux-open-url 'https://github.com/users/{self.config['username']}/projects/new'")
        
        return project_data
    
    def add_card(self, project_name, title, description="", column="📋 Backlog"):
        """Agregar tarjeta a proyecto"""
        card_data = {
            "project": project_name,
            "title": title,
            "description": description,
            "column": column,
            "created_at": datetime.now().isoformat(),
            "labels": []
        }
        
        cards_file = "project_cards.json"
        if os.path.exists(cards_file):
            with open(cards_file, 'r') as f:
                cards = json.load(f)
        else:
            cards = []
        
        cards.append(card_data)
        
        with open(cards_file, 'w') as f:
            json.dump(cards, f, indent=2)
        
        print(f"✅ Tarjeta '{title}' agregada a '{project_name}' en columna '{column}'")
        
        return card_data
    
    def list_projects(self):
        """Listar proyectos locales"""
        projects_file = "github_projects.json"
        if os.path.exists(projects_file):
            with open(projects_file, 'r') as f:
                projects = json.load(f)
            
            print("\n📊 PROYECTOS LOCALES:")
            for i, project in enumerate(projects, 1):
                print(f"{i}. {project['name']} - {project['status']}")
        else:
            print("📭 No hay proyectos locales")
    
    def show_project(self, project_name):
        """Mostrar detalles de un proyecto"""
        projects_file = "github_projects.json"
        cards_file = "project_cards.json"
        
        if os.path.exists(projects_file):
            with open(projects_file, 'r') as f:
                projects = json.load(f)
            
            project = next((p for p in projects if p['name'] == project_name), None)
            if project:
                print(f"\n🏗️ PROYECTO: {project['name']}")
                print(f"📝 {project.get('description', 'Sin descripción')}")
                print(f"🕐 Creado: {project['created_at']}")
                print("\n📋 COLUMNAS:")
                
                # Mostrar tarjetas por columna
                if os.path.exists(cards_file):
                    with open(cards_file, 'r') as f:
                        cards = json.load(f)
                    
                    project_cards = [c for c in cards if c['project'] == project_name]
                    
                    columns = project.get('columns', ['📋 Backlog', '🔄 En Progreso', '✅ Completado'])
                    for column in columns:
                        column_cards = [c for c in project_cards if c['column'] == column]
                        print(f"\n{column} ({len(column_cards)} tarjetas):")
                        for card in column_cards:
                            print(f"  • {card['title']}")
            else:
                print(f"❌ Proyecto '{project_name}' no encontrado")
        else:
            print("📭 No hay proyectos locales")
    
    def generate_github_template(self, project_name):
        """Generar template para copiar/pegar en GitHub"""
        projects_file = "github_projects.json"
        cards_file = "project_cards.json"
        
        if os.path.exists(projects_file) and os.path.exists(cards_file):
            with open(projects_file, 'r') as f:
                projects = json.load(f)
            with open(cards_file, 'r') as f:
                cards = json.load(f)
            
            project = next((p for p in projects if p['name'] == project_name), None)
            if project:
                project_cards = [c for c in cards if c['project'] == project_name]
                
                template = f"""
🎯 PROYECTO GITHUB: {project_name}

{project.get('description', '')}

📋 COLUMNAS A CREAR EN GITHUB:
"""
                # Columnas
                for column in project.get('columns', []):
                    template += f"- '{column}'\n"
                
                template += "\n🎫 TARJETAS PARA AGREGAR:\n"
                
                # Tarjetas por columna
                for column in project.get('columns', []):
                    column_cards = [c for c in project_cards if c['column'] == column]
                    if column_cards:
                        template += f"\n📍 EN '{column}':\n"
                        for card in column_cards:
                            template += f"   - '{card['title']}'"
                            if card.get('description'):
                                template += f" - {card['description']}"
                            template += "\n"
                
                template += f"\n🔗 URL PARA CREAR: https://github.com/users/{self.config['username']}/projects/new"
                
                # Guardar template
                template_file = f"github_template_{project_name.replace(' ', '_')}.txt"
                with open(template_file, 'w') as f:
                    f.write(template)
                
                print(f"✅ Template generado: {template_file}")
                print("📋 Contenido:")
                print(template)
                
                return template
        else:
            print("❌ No se pudo generar el template")

def main():
    parser = argparse.ArgumentParser(description='🚀 GitHub Projects CLI - Gestiona Projects desde Termux')
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando: config
    config_parser = subparsers.add_parser('config', help='Configurar GitHub token')
    config_parser.add_argument('--token', help='GitHub Personal Access Token')
    
    # Comando: create-project
    create_parser = subparsers.add_parser('create-project', help='Crear nuevo proyecto')
    create_parser.add_argument('name', help='Nombre del proyecto')
    create_parser.add_argument('--description', help='Descripción del proyecto', default='')
    
    # Comando: add-card
    card_parser = subparsers.add_parser('add-card', help='Agregar tarjeta a proyecto')
    card_parser.add_argument('project', help='Nombre del proyecto')
    card_parser.add_argument('title', help='Título de la tarjeta')
    card_parser.add_argument('--description', help='Descripción de la tarjeta', default='')
    card_parser.add_argument('--column', help='Columna destino', 
                           choices=['📋 Backlog', '🔄 En Progreso', '✅ Completado'],
                           default='📋 Backlog')
    
    # Comando: list
    subparsers.add_parser('list', help='Listar proyectos')
    
    # Comando: show
    show_parser = subparsers.add_parser('show', help='Mostrar proyecto')
    show_parser.add_argument('project', help='Nombre del proyecto')
    
    # Comando: template
    template_parser = subparsers.add_parser('template', help='Generar template para GitHub')
    template_parser.add_argument('project', help='Nombre del proyecto')
    
    args = parser.parse_args()
    
    cli = GitHubProjectsCLI()
    
    if args.command == 'config' and args.token:
        cli.set_token(args.token)
    elif args.command == 'create-project':
        cli.create_project(args.name, args.description)
    elif args.command == 'add-card':
        cli.add_card(args.project, args.title, args.description, args.column)
    elif args.command == 'list':
        cli.list_projects()
    elif args.command == 'show':
        cli.show_project(args.project)
    elif args.command == 'template':
        cli.generate_github_template(args.project)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

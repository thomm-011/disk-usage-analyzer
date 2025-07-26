#!/usr/bin/env python3
"""
Disk Usage Analyzer - Web Interface
Interface web com Flask e Plotly para visualização interativa
"""

import os
import sys
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
import plotly.graph_objs as go
import plotly.utils
import humanize
from datetime import datetime

# Adicionar o diretório src ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from analyzer.core import DiskUsageAnalyzer, DirectoryStats

app = Flask(__name__)
app.config['SECRET_KEY'] = 'disk-analyzer-secret-key'

# Cache para análises
analysis_cache = {}


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API para análise de diretório"""
    try:
        data = request.get_json()
        path = data.get('path', '/home')
        min_size = parse_size_web(data.get('min_size', '0B'))
        max_depth = int(data.get('max_depth', 5))
        include_hidden = data.get('include_hidden', False)
        
        # Verificar se path existe
        if not os.path.exists(path):
            return jsonify({'error': f'Diretório não encontrado: {path}'}), 400
        
        # Criar chave de cache
        cache_key = f"{path}_{min_size}_{max_depth}_{include_hidden}"
        
        # Verificar cache (válido por 5 minutos)
        if cache_key in analysis_cache:
            cached_data, timestamp = analysis_cache[cache_key]
            if (datetime.now() - timestamp).seconds < 300:
                return jsonify(cached_data)
        
        # Executar análise
        analyzer = DiskUsageAnalyzer(
            min_size=min_size,
            max_depth=max_depth,
            include_hidden=include_hidden,
            exclude_patterns=['*.tmp', '.git', '__pycache__', '*.pyc']
        )
        
        stats = analyzer.analyze_directory(path)
        summary = analyzer.get_summary(stats)
        
        # Preparar dados para visualização
        result = {
            'summary': summary,
            'tree_data': prepare_tree_data(stats),
            'pie_chart': create_pie_chart_data(stats),
            'treemap_data': create_treemap_data(stats),
            'large_files': get_large_files_data(stats, min_size * 10),  # 10x maior que min_size
            'file_types': summary['file_types'],
            'errors': analyzer.errors[:10]  # Primeiros 10 erros
        }
        
        # Salvar no cache
        analysis_cache[cache_key] = (result, datetime.now())
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/directories')
def api_directories():
    """API para listar diretórios disponíveis"""
    try:
        base_paths = ['/home', '/var', '/usr', '/opt', '/tmp']
        available_dirs = []
        
        for base_path in base_paths:
            if os.path.exists(base_path) and os.access(base_path, os.R_OK):
                try:
                    # Listar subdiretórios
                    for item in os.listdir(base_path):
                        full_path = os.path.join(base_path, item)
                        if os.path.isdir(full_path) and os.access(full_path, os.R_OK):
                            available_dirs.append({
                                'path': full_path,
                                'name': f"{base_path}/{item}",
                                'readable': True
                            })
                except PermissionError:
                    continue
        
        # Adicionar diretórios comuns
        common_dirs = [
            {'path': '/home', 'name': '/home (Diretórios de usuários)', 'readable': True},
            {'path': '/var/log', 'name': '/var/log (Logs do sistema)', 'readable': True},
            {'path': '/usr', 'name': '/usr (Programas do sistema)', 'readable': True},
        ]
        
        return jsonify({
            'directories': available_dirs[:20],  # Limitar a 20
            'common': common_dirs
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def prepare_tree_data(stats: DirectoryStats, max_depth: int = 3) -> list:
    """Prepara dados da árvore para visualização"""
    def build_tree_node(dir_stats: DirectoryStats, depth: int = 0) -> dict:
        node = {
            'name': Path(dir_stats.path).name or dir_stats.path,
            'path': dir_stats.path,
            'size': dir_stats.total_size,
            'size_human': humanize.naturalsize(dir_stats.total_size),
            'file_count': dir_stats.file_count,
            'dir_count': dir_stats.dir_count,
            'children': []
        }
        
        if depth < max_depth and dir_stats.children:
            # Ordenar filhos por tamanho e pegar os maiores
            sorted_children = sorted(dir_stats.children, 
                                   key=lambda x: x.total_size, 
                                   reverse=True)[:10]
            
            for child in sorted_children:
                node['children'].append(build_tree_node(child, depth + 1))
        
        return node
    
    return [build_tree_node(stats)]


def create_pie_chart_data(stats: DirectoryStats) -> dict:
    """Cria dados para gráfico de pizza"""
    if not stats.children:
        return {}
    
    # Pegar os 10 maiores diretórios
    sorted_children = sorted(stats.children, 
                           key=lambda x: x.total_size, 
                           reverse=True)[:10]
    
    labels = []
    values = []
    colors = []
    
    color_palette = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
        '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
    ]
    
    for i, child in enumerate(sorted_children):
        name = Path(child.path).name
        labels.append(f"{name}\n({humanize.naturalsize(child.total_size)})")
        values.append(child.total_size)
        colors.append(color_palette[i % len(color_palette)])
    
    return {
        'labels': labels,
        'values': values,
        'colors': colors
    }


def create_treemap_data(stats: DirectoryStats) -> dict:
    """Cria dados para treemap"""
    labels = []
    values = []
    parents = []
    
    def add_to_treemap(dir_stats: DirectoryStats, parent_name: str = ""):
        current_name = Path(dir_stats.path).name or "root"
        full_name = f"{parent_name}/{current_name}" if parent_name else current_name
        
        labels.append(full_name)
        values.append(dir_stats.total_size)
        parents.append(parent_name)
        
        # Adicionar filhos (limitado aos maiores)
        if dir_stats.children:
            sorted_children = sorted(dir_stats.children, 
                                   key=lambda x: x.total_size, 
                                   reverse=True)[:8]
            
            for child in sorted_children:
                add_to_treemap(child, full_name)
    
    add_to_treemap(stats)
    
    return {
        'labels': labels,
        'values': values,
        'parents': parents
    }


def get_large_files_data(stats: DirectoryStats, threshold: int) -> list:
    """Obtém dados dos arquivos grandes"""
    large_files = []
    
    def collect_large_files(dir_stats: DirectoryStats):
        if dir_stats.largest_file and dir_stats.largest_file.size >= threshold:
            large_files.append({
                'path': dir_stats.largest_file.path,
                'name': dir_stats.largest_file.name,
                'size': dir_stats.largest_file.size,
                'size_human': humanize.naturalsize(dir_stats.largest_file.size),
                'modified': dir_stats.largest_file.modified.isoformat() if hasattr(dir_stats.largest_file, 'modified') else None
            })
        
        for child in dir_stats.children:
            collect_large_files(child)
    
    collect_large_files(stats)
    
    # Ordenar por tamanho e retornar os 20 maiores
    return sorted(large_files, key=lambda x: x['size'], reverse=True)[:20]


def parse_size_web(size_str: str) -> int:
    """Converte string de tamanho para bytes (versão web)"""
    if not size_str or size_str == '0':
        return 0
    
    size_str = size_str.upper().strip()
    
    multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4
    }
    
    import re
    match = re.match(r'^(\d+(?:\.\d+)?)\s*([KMGT]?B?)$', size_str)
    
    if not match:
        return 0
    
    number = float(match.group(1))
    unit = match.group(2) or 'B'
    
    return int(number * multipliers.get(unit, 1))


@app.route('/static/<path:filename>')
def static_files(filename):
    """Servir arquivos estáticos"""
    return send_from_directory('static', filename)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500


def main():
    """Função principal para executar o servidor web"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Disk Usage Analyzer - Web Interface')
    parser.add_argument('--host', default='127.0.0.1', help='Host para bind')
    parser.add_argument('--port', type=int, default=8080, help='Porta para bind')
    parser.add_argument('--debug', action='store_true', help='Modo debug')
    
    args = parser.parse_args()
    
    print(f"🌐 Iniciando servidor web em http://{args.host}:{args.port}")
    print("📊 Interface de análise de disco disponível!")
    
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Disk Usage Analyzer - CLI Interface
Interface de linha de comando com Rich para visualização
"""

import click
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.tree import Tree
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
import humanize

# Adicionar o diretório src ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from analyzer.core import DiskUsageAnalyzer, DirectoryStats


console = Console()


def create_tree_view(stats: DirectoryStats, max_items: int = 20) -> Tree:
    """Cria visualização em árvore dos diretórios"""
    
    def format_size(size: int) -> str:
        return f"[cyan]{humanize.naturalsize(size)}[/cyan]"
    
    def format_name(name: str, is_dir: bool, size: int) -> str:
        icon = "📁" if is_dir else "📄"
        size_str = format_size(size)
        return f"{icon} [bold]{name}[/bold] {size_str}"
    
    # Criar árvore raiz
    root_name = Path(stats.path).name or stats.path
    tree = Tree(format_name(root_name, True, stats.total_size))
    
    def add_children(parent_tree: Tree, directory_stats: DirectoryStats, depth: int = 0):
        if depth > 3:  # Limitar profundidade visual
            return
        
        # Ordenar filhos por tamanho (maiores primeiro)
        sorted_children = sorted(directory_stats.children, 
                               key=lambda x: x.total_size, 
                               reverse=True)
        
        # Mostrar apenas os maiores
        for child in sorted_children[:max_items]:
            child_name = Path(child.path).name
            child_node = parent_tree.add(format_name(child_name, True, child.total_size))
            
            if child.children:
                add_children(child_node, child, depth + 1)
    
    add_children(tree, stats)
    return tree


def create_summary_table(summary: dict) -> Table:
    """Cria tabela com resumo da análise"""
    table = Table(title="📊 Resumo da Análise", show_header=True, header_style="bold magenta")
    table.add_column("Métrica", style="cyan", no_wrap=True)
    table.add_column("Valor", style="green")
    
    table.add_row("📁 Diretório", summary['path'])
    table.add_row("💾 Tamanho Total", summary['total_size_human'])
    table.add_row("📄 Arquivos", f"{summary['file_count']:,}")
    table.add_row("📁 Diretórios", f"{summary['dir_count']:,}")
    
    if summary['largest_file']:
        table.add_row("🔍 Maior Arquivo", 
                     f"{Path(summary['largest_file']['path']).name} ({summary['largest_file']['size_human']})")
    
    table.add_row("⚡ Arquivos Escaneados", f"{summary['files_scanned']:,}")
    
    if summary['errors_count'] > 0:
        table.add_row("⚠️ Erros", f"{summary['errors_count']}", style="red")
    
    return table


def create_file_types_table(file_types: dict) -> Table:
    """Cria tabela com tipos de arquivo"""
    if not file_types:
        return None
    
    table = Table(title="📋 Tipos de Arquivo", show_header=True, header_style="bold blue")
    table.add_column("Extensão", style="cyan")
    table.add_column("Quantidade", style="green", justify="right")
    table.add_column("Percentual", style="yellow", justify="right")
    
    total_files = sum(file_types.values())
    
    # Ordenar por quantidade
    sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)
    
    for file_type, count in sorted_types[:15]:  # Top 15
        percentage = (count / total_files) * 100
        ext_display = file_type if file_type != 'no_extension' else '(sem extensão)'
        table.add_row(ext_display, f"{count:,}", f"{percentage:.1f}%")
    
    return table


@click.command()
@click.argument('path', default='.', type=click.Path(exists=True))
@click.option('--min-size', default='0B', help='Tamanho mínimo (ex: 1MB, 100KB)')
@click.option('--max-depth', default=10, help='Profundidade máxima de análise')
@click.option('--exclude', multiple=True, help='Padrões para excluir (ex: *.tmp)')
@click.option('--include-hidden', is_flag=True, help='Incluir arquivos ocultos')
@click.option('--tree-items', default=20, help='Máximo de itens na árvore')
@click.option('--export', type=click.Choice(['json', 'csv']), help='Exportar resultados')
@click.option('--output', help='Arquivo de saída para exportação')
@click.option('--large-files', help='Mostrar arquivos maiores que (ex: 100MB)')
@click.option('--quiet', is_flag=True, help='Modo silencioso')
def analyze(path, min_size, max_depth, exclude, include_hidden, tree_items, 
           export, output, large_files, quiet):
    """
    🔍 Analisa o uso de disco em um diretório
    
    Exemplos:
    
    disk-analyzer                          # Diretório atual
    
    disk-analyzer /home/user               # Diretório específico
    
    disk-analyzer --min-size 1MB          # Arquivos >= 1MB
    
    disk-analyzer --exclude "*.log" "*.tmp"  # Excluir padrões
    """
    
    if not quiet:
        console.print(Panel.fit("🔍 [bold blue]Disk Usage Analyzer[/bold blue]", 
                               border_style="blue"))
    
    # Converter tamanho mínimo
    min_size_bytes = parse_size(min_size)
    
    # Configurar analisador
    analyzer = DiskUsageAnalyzer(
        min_size=min_size_bytes,
        max_depth=max_depth,
        exclude_patterns=list(exclude),
        include_hidden=include_hidden,
        calculate_hashes=False  # Por enquanto desabilitado
    )
    
    # Executar análise com progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        
        task = progress.add_task("Analisando diretórios...", total=None)
        
        try:
            stats = analyzer.analyze_directory(path)
            progress.update(task, description="✅ Análise concluída!")
            
        except Exception as e:
            console.print(f"[red]❌ Erro na análise: {e}[/red]")
            sys.exit(1)
    
    # Gerar resumo
    summary = analyzer.get_summary(stats)
    
    if not quiet:
        # Mostrar resultados
        console.print()
        console.print(create_summary_table(summary))
        console.print()
        
        # Árvore de diretórios
        tree = create_tree_view(stats, tree_items)
        console.print(Panel(tree, title="🌳 Estrutura de Diretórios", border_style="green"))
        console.print()
        
        # Tipos de arquivo
        file_types_table = create_file_types_table(summary['file_types'])
        if file_types_table:
            console.print(file_types_table)
            console.print()
    
    # Arquivos grandes
    if large_files:
        threshold = parse_size(large_files)
        large_file_list = analyzer.find_large_files(stats, threshold)
        
        if large_file_list:
            console.print(f"📋 [bold]Arquivos maiores que {large_files}:[/bold]")
            for i, file_info in enumerate(large_file_list[:20], 1):
                size_str = humanize.naturalsize(file_info.size)
                console.print(f"{i:2d}. [cyan]{size_str}[/cyan] {file_info.path}")
            console.print()
    
    # Exportar se solicitado
    if export:
        export_results(stats, summary, export, output)
    
    # Mostrar erros se houver
    if analyzer.errors and not quiet:
        console.print(f"[yellow]⚠️ {len(analyzer.errors)} erro(s) encontrado(s)[/yellow]")
        if len(analyzer.errors) <= 5:
            for error in analyzer.errors:
                console.print(f"  [red]•[/red] {error}")
        else:
            for error in analyzer.errors[:3]:
                console.print(f"  [red]•[/red] {error}")
            console.print(f"  [yellow]... e mais {len(analyzer.errors) - 3} erros[/yellow]")


def parse_size(size_str: str) -> int:
    """Converte string de tamanho para bytes"""
    if not size_str or size_str == '0':
        return 0
    
    size_str = size_str.upper().strip()
    
    # Multiplicadores
    multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4
    }
    
    # Extrair número e unidade
    import re
    match = re.match(r'^(\d+(?:\.\d+)?)\s*([KMGT]?B?)$', size_str)
    
    if not match:
        raise click.BadParameter(f"Formato de tamanho inválido: {size_str}")
    
    number = float(match.group(1))
    unit = match.group(2) or 'B'
    
    if unit not in multipliers:
        raise click.BadParameter(f"Unidade inválida: {unit}")
    
    return int(number * multipliers[unit])


def export_results(stats: DirectoryStats, summary: dict, format_type: str, output_file: str):
    """Exporta resultados para arquivo"""
    if not output_file:
        output_file = f"disk_analysis.{format_type}"
    
    try:
        if format_type == 'json':
            import json
            
            # Converter stats para dict serializável
            export_data = {
                'summary': summary,
                'timestamp': str(datetime.now()),
                'directory_tree': serialize_stats(stats)
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        elif format_type == 'csv':
            import csv
            
            # Criar CSV com informações dos diretórios
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Path', 'Size_Bytes', 'Size_Human', 'Files', 'Directories'])
                
                def write_directory(dir_stats: DirectoryStats):
                    writer.writerow([
                        dir_stats.path,
                        dir_stats.total_size,
                        humanize.naturalsize(dir_stats.total_size),
                        dir_stats.file_count,
                        dir_stats.dir_count
                    ])
                    
                    for child in dir_stats.children:
                        write_directory(child)
                
                write_directory(stats)
        
        console.print(f"[green]✅ Resultados exportados para: {output_file}[/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Erro na exportação: {e}[/red]")


def serialize_stats(stats: DirectoryStats) -> dict:
    """Converte DirectoryStats para dict serializável"""
    return {
        'path': stats.path,
        'total_size': stats.total_size,
        'file_count': stats.file_count,
        'dir_count': stats.dir_count,
        'largest_file': {
            'path': stats.largest_file.path,
            'size': stats.largest_file.size,
            'name': stats.largest_file.name
        } if stats.largest_file else None,
        'file_types': stats.file_types,
        'children': [serialize_stats(child) for child in stats.children]
    }


if __name__ == '__main__':
    from datetime import datetime
    analyze()

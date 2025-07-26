#!/usr/bin/env python3
"""
Exemplo de uso do Disk Usage Analyzer
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from analyzer.core import DiskUsageAnalyzer
import humanize


def main():
    """Exemplo básico de uso"""
    print("🔍 Disk Usage Analyzer - Exemplo de Uso")
    print("=" * 50)
    
    # Configurar analisador
    analyzer = DiskUsageAnalyzer(
        min_size=1024,  # 1KB mínimo
        max_depth=3,    # 3 níveis de profundidade
        exclude_patterns=[
            '*.tmp', '*.log', '.git', '__pycache__', 
            '*.pyc', '.cache', '.npm'
        ],
        include_hidden=False
    )
    
    # Analisar diretório atual
    try:
        print("📁 Analisando diretório atual...")
        stats = analyzer.analyze_directory('.')
        
        # Mostrar resumo
        summary = analyzer.get_summary(stats)
        
        print(f"\n📊 RESUMO DA ANÁLISE")
        print(f"Diretório: {summary['path']}")
        print(f"Tamanho total: {summary['total_size_human']}")
        print(f"Arquivos: {summary['file_count']:,}")
        print(f"Diretórios: {summary['dir_count']:,}")
        
        if summary['largest_file']:
            print(f"Maior arquivo: {summary['largest_file']['path']}")
            print(f"Tamanho: {summary['largest_file']['size_human']}")
        
        print(f"Arquivos escaneados: {summary['files_scanned']:,}")
        
        # Mostrar tipos de arquivo
        if summary['file_types']:
            print(f"\n📋 TIPOS DE ARQUIVO (Top 10):")
            sorted_types = sorted(summary['file_types'].items(), 
                                key=lambda x: x[1], reverse=True)[:10]
            
            for file_type, count in sorted_types:
                ext = file_type if file_type != 'no_extension' else '(sem extensão)'
                print(f"  {ext}: {count:,} arquivos")
        
        # Mostrar estrutura de diretórios
        print(f"\n🌳 ESTRUTURA DE DIRETÓRIOS:")
        print_directory_tree(stats, max_depth=2)
        
        # Mostrar erros se houver
        if analyzer.errors:
            print(f"\n⚠️ ERROS ENCONTRADOS ({len(analyzer.errors)}):")
            for error in analyzer.errors[:5]:
                print(f"  • {error}")
            if len(analyzer.errors) > 5:
                print(f"  ... e mais {len(analyzer.errors) - 5} erros")
        
        # Encontrar arquivos grandes
        large_files = analyzer.find_large_files(stats, 1024 * 1024)  # > 1MB
        if large_files:
            print(f"\n📄 ARQUIVOS GRANDES (> 1MB):")
            for i, file_info in enumerate(large_files[:10], 1):
                size_str = humanize.naturalsize(file_info.size)
                print(f"  {i:2d}. {size_str:>8} - {file_info.name}")
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        return 1
    
    return 0


def print_directory_tree(stats, level=0, max_depth=3):
    """Imprime árvore de diretórios"""
    if level > max_depth:
        return
    
    indent = "  " * level
    name = Path(stats.path).name or stats.path
    size_str = humanize.naturalsize(stats.total_size)
    
    print(f"{indent}📁 {name} ({size_str})")
    
    # Mostrar filhos ordenados por tamanho
    if stats.children:
        sorted_children = sorted(stats.children, 
                               key=lambda x: x.total_size, 
                               reverse=True)[:5]  # Top 5
        
        for child in sorted_children:
            print_directory_tree(child, level + 1, max_depth)


if __name__ == "__main__":
    sys.exit(main())

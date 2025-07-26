#!/usr/bin/env python3
"""
Disk Usage Analyzer - Core Module
Análise principal de uso de disco
"""

import os
import stat
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import humanize
import hashlib


@dataclass
class FileInfo:
    """Informações de um arquivo ou diretório"""
    path: str
    name: str
    size: int
    is_dir: bool
    modified: datetime
    permissions: str
    owner: str
    group: str
    file_type: str
    hash_md5: Optional[str] = None


@dataclass
class DirectoryStats:
    """Estatísticas de um diretório"""
    path: str
    total_size: int
    file_count: int
    dir_count: int
    largest_file: Optional[FileInfo]
    file_types: Dict[str, int]
    children: List['DirectoryStats']


class DiskUsageAnalyzer:
    """Analisador principal de uso de disco"""
    
    def __init__(self, 
                 min_size: int = 0,
                 max_depth: int = 10,
                 exclude_patterns: List[str] = None,
                 include_hidden: bool = False,
                 calculate_hashes: bool = False):
        """
        Inicializa o analisador
        
        Args:
            min_size: Tamanho mínimo em bytes para incluir
            max_depth: Profundidade máxima de análise
            exclude_patterns: Padrões para excluir
            include_hidden: Incluir arquivos ocultos
            calculate_hashes: Calcular hashes MD5 para detecção de duplicatas
        """
        self.min_size = min_size
        self.max_depth = max_depth
        self.exclude_patterns = exclude_patterns or []
        self.include_hidden = include_hidden
        self.calculate_hashes = calculate_hashes
        self.total_files_scanned = 0
        self.total_size_scanned = 0
        self.errors = []
    
    def should_exclude(self, path: Path) -> bool:
        """Verifica se um path deve ser excluído"""
        if not self.include_hidden and path.name.startswith('.'):
            return True
        
        for pattern in self.exclude_patterns:
            if path.match(pattern):
                return True
        
        return False
    
    def get_file_info(self, path: Path) -> Optional[FileInfo]:
        """Obtém informações detalhadas de um arquivo"""
        try:
            stat_info = path.stat()
            
            # Informações básicas
            file_info = FileInfo(
                path=str(path),
                name=path.name,
                size=stat_info.st_size,
                is_dir=path.is_dir(),
                modified=datetime.fromtimestamp(stat_info.st_mtime),
                permissions=stat.filemode(stat_info.st_mode),
                owner=str(stat_info.st_uid),
                group=str(stat_info.st_gid),
                file_type=path.suffix.lower() if path.suffix else 'no_extension'
            )
            
            # Calcular hash se solicitado e for arquivo
            if self.calculate_hashes and not file_info.is_dir and file_info.size > 0:
                try:
                    file_info.hash_md5 = self._calculate_md5(path)
                except Exception as e:
                    self.errors.append(f"Erro calculando hash para {path}: {e}")
            
            return file_info
            
        except (OSError, PermissionError) as e:
            self.errors.append(f"Erro acessando {path}: {e}")
            return None
    
    def _calculate_md5(self, path: Path) -> str:
        """Calcula hash MD5 de um arquivo"""
        hash_md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def analyze_directory(self, path: str, current_depth: int = 0) -> DirectoryStats:
        """
        Analisa um diretório recursivamente
        
        Args:
            path: Caminho do diretório
            current_depth: Profundidade atual
            
        Returns:
            DirectoryStats com informações do diretório
        """
        dir_path = Path(path)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Diretório não encontrado: {path}")
        
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Não é um diretório: {path}")
        
        # Inicializar estatísticas
        stats = DirectoryStats(
            path=str(dir_path),
            total_size=0,
            file_count=0,
            dir_count=0,
            largest_file=None,
            file_types={},
            children=[]
        )
        
        try:
            # Listar conteúdo do diretório
            items = list(dir_path.iterdir())
            
            for item in items:
                # Verificar se deve excluir
                if self.should_exclude(item):
                    continue
                
                # Obter informações do item
                file_info = self.get_file_info(item)
                if not file_info:
                    continue
                
                # Filtrar por tamanho mínimo
                if file_info.size < self.min_size:
                    continue
                
                self.total_files_scanned += 1
                self.total_size_scanned += file_info.size
                
                if file_info.is_dir:
                    # Diretório - analisar recursivamente se não excedeu profundidade
                    stats.dir_count += 1
                    
                    if current_depth < self.max_depth:
                        child_stats = self.analyze_directory(str(item), current_depth + 1)
                        stats.children.append(child_stats)
                        stats.total_size += child_stats.total_size
                        stats.file_count += child_stats.file_count
                        stats.dir_count += child_stats.dir_count
                        
                        # Atualizar tipos de arquivo
                        for file_type, count in child_stats.file_types.items():
                            stats.file_types[file_type] = stats.file_types.get(file_type, 0) + count
                        
                        # Verificar se tem o maior arquivo
                        if child_stats.largest_file:
                            if not stats.largest_file or child_stats.largest_file.size > stats.largest_file.size:
                                stats.largest_file = child_stats.largest_file
                
                else:
                    # Arquivo
                    stats.file_count += 1
                    stats.total_size += file_info.size
                    
                    # Atualizar tipos de arquivo
                    file_type = file_info.file_type
                    stats.file_types[file_type] = stats.file_types.get(file_type, 0) + 1
                    
                    # Verificar se é o maior arquivo
                    if not stats.largest_file or file_info.size > stats.largest_file.size:
                        stats.largest_file = file_info
        
        except PermissionError as e:
            self.errors.append(f"Sem permissão para acessar {dir_path}: {e}")
        
        return stats
    
    def find_large_files(self, stats: DirectoryStats, threshold: int) -> List[FileInfo]:
        """Encontra arquivos maiores que o threshold"""
        large_files = []
        
        def collect_large_files(directory_stats: DirectoryStats):
            if directory_stats.largest_file and directory_stats.largest_file.size >= threshold:
                large_files.append(directory_stats.largest_file)
            
            for child in directory_stats.children:
                collect_large_files(child)
        
        collect_large_files(stats)
        return sorted(large_files, key=lambda x: x.size, reverse=True)
    
    def find_duplicates(self, stats: DirectoryStats) -> Dict[str, List[FileInfo]]:
        """Encontra arquivos duplicados baseado no hash MD5"""
        if not self.calculate_hashes:
            return {}
        
        hash_map = {}
        
        def collect_hashes(directory_stats: DirectoryStats):
            # Implementar coleta de hashes recursivamente
            # Por simplicidade, retornando dict vazio
            pass
        
        collect_hashes(stats)
        
        # Retornar apenas hashes com múltiplos arquivos
        return {h: files for h, files in hash_map.items() if len(files) > 1}
    
    def get_summary(self, stats: DirectoryStats) -> Dict:
        """Gera resumo da análise"""
        return {
            'path': stats.path,
            'total_size': stats.total_size,
            'total_size_human': humanize.naturalsize(stats.total_size),
            'file_count': stats.file_count,
            'dir_count': stats.dir_count,
            'largest_file': {
                'path': stats.largest_file.path,
                'size': stats.largest_file.size,
                'size_human': humanize.naturalsize(stats.largest_file.size)
            } if stats.largest_file else None,
            'file_types': stats.file_types,
            'files_scanned': self.total_files_scanned,
            'total_scanned_size': humanize.naturalsize(self.total_size_scanned),
            'errors_count': len(self.errors)
        }


def main():
    """Função principal para teste"""
    analyzer = DiskUsageAnalyzer(
        min_size=1024,  # 1KB
        max_depth=3,
        exclude_patterns=['*.tmp', '.git', '__pycache__']
    )
    
    try:
        stats = analyzer.analyze_directory('/home/thomas')
        summary = analyzer.get_summary(stats)
        
        print("=== Resumo da Análise ===")
        print(f"Diretório: {summary['path']}")
        print(f"Tamanho total: {summary['total_size_human']}")
        print(f"Arquivos: {summary['file_count']}")
        print(f"Diretórios: {summary['dir_count']}")
        
        if summary['largest_file']:
            print(f"Maior arquivo: {summary['largest_file']['path']} ({summary['largest_file']['size_human']})")
        
        print(f"Arquivos escaneados: {summary['files_scanned']}")
        print(f"Erros: {summary['errors_count']}")
        
        if analyzer.errors:
            print("\n=== Erros ===")
            for error in analyzer.errors[:5]:  # Mostrar apenas os primeiros 5
                print(f"- {error}")
    
    except Exception as e:
        print(f"Erro na análise: {e}")


if __name__ == "__main__":
    main()

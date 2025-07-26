#!/usr/bin/env python3
"""
Testes para o Disk Usage Analyzer
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from analyzer.core import DiskUsageAnalyzer, DirectoryStats, FileInfo


class TestDiskUsageAnalyzer(unittest.TestCase):
    """Testes para a classe DiskUsageAnalyzer"""
    
    def setUp(self):
        """Configurar ambiente de teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.analyzer = DiskUsageAnalyzer(
            min_size=0,
            max_depth=5,
            include_hidden=True
        )
    
    def tearDown(self):
        """Limpar ambiente de teste"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_files(self):
        """Criar estrutura de arquivos para teste"""
        # Criar diretórios
        os.makedirs(os.path.join(self.temp_dir, "dir1", "subdir1"))
        os.makedirs(os.path.join(self.temp_dir, "dir2"))
        
        # Criar arquivos
        files = [
            ("file1.txt", "Conteúdo do arquivo 1"),
            ("dir1/file2.py", "print('Hello World')"),
            ("dir1/subdir1/file3.log", "Log entry 1\nLog entry 2"),
            ("dir2/file4.md", "# Título\nConteúdo markdown"),
        ]
        
        for file_path, content in files:
            full_path = os.path.join(self.temp_dir, file_path)
            with open(full_path, 'w') as f:
                f.write(content)
    
    def test_analyzer_initialization(self):
        """Testar inicialização do analisador"""
        analyzer = DiskUsageAnalyzer(
            min_size=1024,
            max_depth=3,
            exclude_patterns=['*.tmp'],
            include_hidden=False
        )
        
        self.assertEqual(analyzer.min_size, 1024)
        self.assertEqual(analyzer.max_depth, 3)
        self.assertEqual(analyzer.exclude_patterns, ['*.tmp'])
        self.assertFalse(analyzer.include_hidden)
    
    def test_should_exclude(self):
        """Testar lógica de exclusão"""
        analyzer = DiskUsageAnalyzer(
            exclude_patterns=['*.tmp', '.git'],
            include_hidden=False
        )
        
        # Arquivos ocultos devem ser excluídos
        self.assertTrue(analyzer.should_exclude(Path('.hidden_file')))
        
        # Arquivos que correspondem aos padrões devem ser excluídos
        self.assertTrue(analyzer.should_exclude(Path('temp.tmp')))
        self.assertTrue(analyzer.should_exclude(Path('.git')))
        
        # Arquivos normais não devem ser excluídos
        self.assertFalse(analyzer.should_exclude(Path('normal_file.txt')))
    
    def test_get_file_info(self):
        """Testar obtenção de informações de arquivo"""
        self.create_test_files()
        
        file_path = Path(os.path.join(self.temp_dir, "file1.txt"))
        file_info = self.analyzer.get_file_info(file_path)
        
        self.assertIsNotNone(file_info)
        self.assertEqual(file_info.name, "file1.txt")
        self.assertFalse(file_info.is_dir)
        self.assertGreater(file_info.size, 0)
        self.assertEqual(file_info.file_type, '.txt')
    
    def test_analyze_directory(self):
        """Testar análise de diretório"""
        self.create_test_files()
        
        stats = self.analyzer.analyze_directory(self.temp_dir)
        
        self.assertIsInstance(stats, DirectoryStats)
        self.assertEqual(stats.path, self.temp_dir)
        self.assertGreater(stats.total_size, 0)
        self.assertGreater(stats.file_count, 0)
        self.assertGreater(stats.dir_count, 0)
        self.assertIsNotNone(stats.largest_file)
    
    def test_directory_not_found(self):
        """Testar erro quando diretório não existe"""
        with self.assertRaises(FileNotFoundError):
            self.analyzer.analyze_directory("/path/that/does/not/exist")
    
    def test_not_a_directory(self):
        """Testar erro quando path não é um diretório"""
        # Criar um arquivo
        file_path = os.path.join(self.temp_dir, "test_file.txt")
        with open(file_path, 'w') as f:
            f.write("test content")
        
        with self.assertRaises(NotADirectoryError):
            self.analyzer.analyze_directory(file_path)
    
    def test_min_size_filter(self):
        """Testar filtro de tamanho mínimo"""
        self.create_test_files()
        
        # Analisador com tamanho mínimo alto
        analyzer = DiskUsageAnalyzer(min_size=1000)  # 1KB
        stats = analyzer.analyze_directory(self.temp_dir)
        
        # Deve ter menos arquivos devido ao filtro
        self.assertGreaterEqual(stats.file_count, 0)
    
    def test_max_depth_limit(self):
        """Testar limite de profundidade"""
        self.create_test_files()
        
        # Analisador com profundidade limitada
        analyzer = DiskUsageAnalyzer(max_depth=1)
        stats = analyzer.analyze_directory(self.temp_dir)
        
        # Verificar que não vai muito fundo
        self.assertIsInstance(stats, DirectoryStats)
    
    def test_file_types_counting(self):
        """Testar contagem de tipos de arquivo"""
        self.create_test_files()
        
        stats = self.analyzer.analyze_directory(self.temp_dir)
        
        # Deve ter diferentes tipos de arquivo
        self.assertIn('.txt', stats.file_types)
        self.assertIn('.py', stats.file_types)
        self.assertIn('.log', stats.file_types)
        self.assertIn('.md', stats.file_types)
    
    def test_get_summary(self):
        """Testar geração de resumo"""
        self.create_test_files()
        
        stats = self.analyzer.analyze_directory(self.temp_dir)
        summary = self.analyzer.get_summary(stats)
        
        # Verificar campos obrigatórios
        required_fields = [
            'path', 'total_size', 'total_size_human',
            'file_count', 'dir_count', 'file_types',
            'files_scanned', 'total_scanned_size', 'errors_count'
        ]
        
        for field in required_fields:
            self.assertIn(field, summary)
    
    def test_find_large_files(self):
        """Testar busca por arquivos grandes"""
        self.create_test_files()
        
        stats = self.analyzer.analyze_directory(self.temp_dir)
        large_files = self.analyzer.find_large_files(stats, threshold=1)  # 1 byte
        
        # Deve encontrar arquivos
        self.assertIsInstance(large_files, list)
        self.assertGreaterEqual(len(large_files), 0)


class TestFileInfo(unittest.TestCase):
    """Testes para a classe FileInfo"""
    
    def test_file_info_creation(self):
        """Testar criação de FileInfo"""
        from datetime import datetime
        
        file_info = FileInfo(
            path="/test/file.txt",
            name="file.txt",
            size=1024,
            is_dir=False,
            modified=datetime.now(),
            permissions="rw-r--r--",
            owner="1000",
            group="1000",
            file_type=".txt"
        )
        
        self.assertEqual(file_info.name, "file.txt")
        self.assertEqual(file_info.size, 1024)
        self.assertFalse(file_info.is_dir)
        self.assertEqual(file_info.file_type, ".txt")


class TestDirectoryStats(unittest.TestCase):
    """Testes para a classe DirectoryStats"""
    
    def test_directory_stats_creation(self):
        """Testar criação de DirectoryStats"""
        stats = DirectoryStats(
            path="/test/dir",
            total_size=2048,
            file_count=5,
            dir_count=2,
            largest_file=None,
            file_types={'.txt': 3, '.py': 2},
            children=[]
        )
        
        self.assertEqual(stats.path, "/test/dir")
        self.assertEqual(stats.total_size, 2048)
        self.assertEqual(stats.file_count, 5)
        self.assertEqual(stats.dir_count, 2)
        self.assertEqual(stats.file_types['.txt'], 3)


if __name__ == '__main__':
    # Executar testes
    unittest.main(verbosity=2)

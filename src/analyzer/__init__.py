"""
Disk Usage Analyzer - Core Module
Módulo principal para análise de uso de disco
"""

from .core import DiskUsageAnalyzer, DirectoryStats, FileInfo

__version__ = "1.0.0"
__author__ = "Thomas"

__all__ = [
    "DiskUsageAnalyzer",
    "DirectoryStats", 
    "FileInfo"
]

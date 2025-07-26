#!/usr/bin/env python3
"""
Setup script para Disk Usage Analyzer
"""

from setuptools import setup, find_packages
from pathlib import Path

# Ler README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="disk-usage-analyzer",
    version="1.0.0",
    author="Thomas",
    author_email="thomas@example.com",
    description="Analisador de uso de disco para Linux com interface CLI e Web",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thomm-011/disk-usage-analyzer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Filesystems",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "flask>=2.3.0",
        "plotly>=5.15.0",
        "pandas>=2.0.0",
        "pyyaml>=6.0",
        "psutil>=5.9.0",
        "humanize>=4.7.0",
        "tqdm>=4.65.0",
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "web": [
            "gunicorn>=20.1.0",
            "waitress>=2.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "disk-analyzer=cli.main:analyze",
            "disk-analyzer-web=web.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "web": ["templates/*.html", "static/*.css", "static/*.js"],
    },
    keywords="disk usage analyzer linux filesystem monitoring",
    project_urls={
        "Bug Reports": "https://github.com/thomm-011/disk-usage-analyzer/issues",
        "Source": "https://github.com/thomm-011/disk-usage-analyzer",
        "Documentation": "https://github.com/thomm-011/disk-usage-analyzer/wiki",
    },
)

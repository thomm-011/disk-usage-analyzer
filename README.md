# 🔍 Disk Usage Analyzer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20WSL2-lightgrey.svg)]()

Um analisador de uso de disco moderno e interativo com interface web e CLI, desenvolvido em Python.

## ✨ Características

- 🌐 **Interface Web Moderna** - Dashboard interativo com gráficos
- 💻 **Interface CLI Rica** - Terminal com cores e formatação
- 📊 **Múltiplas Visualizações** - Pizza, Treemap, Árvore de diretórios
- 🚀 **Performance Otimizada** - Análise rápida e eficiente
- 🔧 **WSL2 Compatible** - Funciona perfeitamente no Windows WSL2
- 📱 **Responsivo** - Interface adaptável para diferentes telas
- 🎯 **Filtros Avançados** - Por tamanho, profundidade, arquivos ocultos

## 🖼️ Screenshots

### Interface Web
![Web Interface](docs/screenshots/web-interface.png)

### Interface CLI
![CLI Interface](docs/screenshots/cli-interface.png)

## 🚀 Instalação Rápida

### Método 1: Script Automático
```bash
git clone https://github.com/seu-usuario/disk-usage-analyzer.git
cd disk-usage-analyzer
./install.sh
```

### Método 2: Manual
```bash
git clone https://github.com/seu-usuario/disk-usage-analyzer.git
cd disk-usage-analyzer
pip install -r requirements.txt
```

## 🎯 Uso

### Interface Web
```bash
# Iniciar servidor web
./start.sh
# Acesse: http://localhost:8080 (ou IP do WSL2)
```

### Interface CLI
```bash
# Análise básica
python3 src/cli/main.py /home --min-size 1MB

# Análise detalhada
python3 src/cli/main.py /var/log --min-size 1KB --max-depth 5 --include-hidden
```

### Exemplo Programático
```python
from src.core.analyzer import DiskAnalyzer

analyzer = DiskAnalyzer()
stats = analyzer.analyze_directory("/home", min_size="1MB", max_depth=3)
print(f"Total size: {stats.total_size}")
```

## 📊 Funcionalidades

### Interface Web
- 📈 **Gráfico de Pizza** - Distribuição por diretórios
- 🗺️ **Treemap** - Visualização hierárquica interativa
- 🌳 **Árvore de Diretórios** - Navegação estruturada
- 📄 **Lista de Arquivos Grandes** - Ordenada por tamanho
- 📋 **Análise por Tipo** - Estatísticas por extensão

### Interface CLI
- 🎨 **Output Colorido** - Formatação rica no terminal
- 📊 **Tabelas Organizadas** - Dados estruturados
- 🔍 **Busca Interativa** - Filtros em tempo real
- 📈 **Gráficos ASCII** - Visualizações no terminal

## 🔧 Configuração

### WSL2 (Windows)
```bash
# Use o script específico para WSL2
./start_wsl2.sh
# Acesse: http://IP_DO_WSL2:8080
```

### Linux Nativo
```bash
# Inicialização padrão
python3 src/web/app.py --host 0.0.0.0 --port 8080
```

## 🛠️ Scripts Utilitários

| Script | Descrição |
|--------|-----------|
| `start.sh` | Inicialização rápida |
| `start_wsl2.sh` | Específico para WSL2 |
| `auto_fix.sh` | Correção automática de problemas |
| `diagnose.sh` | Diagnóstico de conectividade |
| `debug_web.py` | Servidor debug simples |

## 📋 Requisitos

- **Python:** 3.8+
- **Dependências:** Flask, Rich, Humanize, Plotly
- **Sistema:** Linux, WSL2, macOS
- **Navegador:** Chrome, Firefox, Safari, Edge

## 🔍 Troubleshooting

### Problemas Comuns
- **Não consegue acessar localhost:** Veja [WSL2_ACCESS.md](WSL2_ACCESS.md)
- **Servidor não inicia:** Execute `./diagnose.sh`
- **Performance lenta:** Reduza profundidade ou aumente tamanho mínimo

### Documentação Completa
- 📖 [Guia de Uso](USAGE.md)
- 🔧 [Troubleshooting](TROUBLESHOOTING.md)
- 🚀 [Quick Start](QUICK_START.md)
- 🐧 [WSL2 Setup](WSL2_ACCESS.md)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [Rich](https://github.com/Textualize/rich) - Interface CLI rica
- [Flask](https://flask.palletsprojects.com/) - Framework web
- [Plotly](https://plotly.com/) - Gráficos interativos
- [Tailwind CSS](https://tailwindcss.com/) - Estilização moderna

## 👨‍💻 Autor

**Thomas** - [GitHub](https://github.com/thomm-011)

---

⭐ **Se este projeto foi útil, considere dar uma estrela!** ⭐

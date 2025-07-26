#!/bin/bash

# Disk Usage Analyzer - Script de Instalação Rápida
# Este script instala o Disk Usage Analyzer e suas dependências

set -e

echo "🔍 Disk Usage Analyzer - Instalação"
echo "===================================="

# Verificar se Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

# Verificar versão do Python
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION encontrado. Requer Python $REQUIRED_VERSION ou superior."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION encontrado"

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instalando..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

echo "✅ pip3 disponível"

# Instalar dependências do sistema (se necessário)
echo "📦 Instalando dependências do sistema..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y python3-dev python3-venv
elif command -v yum &> /dev/null; then
    sudo yum install -y python3-devel python3-venv
elif command -v dnf &> /dev/null; then
    sudo dnf install -y python3-devel python3-venv
fi

# Criar ambiente virtual (opcional)
read -p "🤔 Deseja criar um ambiente virtual? (recomendado) [y/N]: " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "🔧 Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Ambiente virtual ativado"
    echo "💡 Para ativar novamente: source venv/bin/activate"
fi

# Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Instalar o pacote
echo "🔧 Instalando Disk Usage Analyzer..."
pip3 install -e .

# Verificar instalação
echo "🧪 Testando instalação..."
if python3 -c "from analyzer.core import DiskUsageAnalyzer; print('✅ Módulo core OK')"; then
    echo "✅ Instalação bem-sucedida!"
else
    echo "❌ Erro na instalação"
    exit 1
fi

# Mostrar comandos disponíveis
echo ""
echo "🎉 Instalação concluída!"
echo "========================"
echo ""
echo "📋 Comandos disponíveis:"
echo "  python3 src/cli/main.py --help     # Interface CLI"
echo "  python3 src/web/app.py             # Interface Web"
echo "  python3 example.py                 # Exemplo de uso"
echo "  make help                          # Ver todos os comandos"
echo ""
echo "🚀 Exemplos de uso:"
echo "  python3 src/cli/main.py /home --min-size 1MB"
echo "  python3 src/cli/main.py . --export json --output report.json"
echo "  python3 src/web/app.py --port 8080"
echo ""
echo "📖 Documentação: README.md"
echo "🐛 Problemas: https://github.com/thomm-011/disk-usage-analyzer/issues"

# Executar exemplo se solicitado
read -p "🤔 Deseja executar um exemplo agora? [y/N]: " run_example
if [[ $run_example =~ ^[Yy]$ ]]; then
    echo "🔍 Executando exemplo..."
    python3 example.py
fi

echo ""
echo "✨ Pronto para usar! Divirta-se analisando seus discos! 🎯"

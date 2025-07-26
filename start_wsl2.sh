#!/bin/bash

# Script específico para iniciar o servidor no WSL2

echo "🐧 Disk Usage Analyzer - WSL2 Mode"
echo "=================================="

# Detectar IP do WSL2
WSL_IP=$(hostname -I | awk '{print $1}')
PORT=${1:-8080}

echo "🔍 Detectando configuração WSL2..."
echo "  IP do WSL2: $WSL_IP"
echo "  Porta: $PORT"
echo ""

# Verificar se estamos no WSL2
if grep -qi microsoft /proc/version; then
    echo "✅ WSL2 detectado"
else
    echo "⚠️ Não parece ser WSL2, mas continuando..."
fi

# Verificar dependências
echo "📦 Verificando dependências..."
python3 -c "import flask, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependências não encontradas. Instalando..."
    pip3 install flask plotly pandas
fi

echo ""
echo "🌐 URLs de Acesso:"
echo "  📍 No WSL2:     http://localhost:$PORT"
echo "  📍 No Windows:  http://$WSL_IP:$PORT"
echo "  📍 Direto:      http://127.0.0.1:$PORT"
echo ""

echo "💡 Instruções:"
echo "  1. Deixe este terminal aberto"
echo "  2. No Windows, abra o navegador"
echo "  3. Acesse: http://$WSL_IP:$PORT"
echo "  4. Use Ctrl+C para parar o servidor"
echo ""

echo "🔧 Para port forwarding no Windows (PowerShell como Admin):"
echo "  netsh interface portproxy add v4tov4 listenport=$PORT listenaddress=0.0.0.0 connectport=$PORT connectaddress=$WSL_IP"
echo ""

# Função para cleanup
cleanup() {
    echo ""
    echo "🛑 Parando servidor..."
    exit 0
}

trap cleanup SIGINT SIGTERM

# Verificar se a porta está disponível
if command -v ss >/dev/null 2>&1; then
    if ss -tuln | grep ":$PORT " >/dev/null; then
        echo "⚠️ Porta $PORT já está em uso!"
        echo "   Tentando matar processo existente..."
        pkill -f "python.*$PORT" 2>/dev/null || true
        sleep 2
    fi
fi

echo "🚀 Iniciando servidor..."
echo "   Aguarde alguns segundos para inicialização..."
echo ""

# Iniciar servidor
cd "$(dirname "$0")"

# Tentar servidor principal primeiro
if [ -f "src/web/app.py" ]; then
    echo "📊 Iniciando interface completa..."
    python3 src/web/app.py --host 0.0.0.0 --port $PORT
else
    echo "🐛 Iniciando servidor debug..."
    python3 debug_web.py --host 0.0.0.0 --port $PORT
fi

#!/bin/bash

# Script para iniciar o servidor web do Disk Usage Analyzer

echo "🔍 Disk Usage Analyzer - Servidor Web"
echo "====================================="

# Verificar dependências
echo "📦 Verificando dependências..."
python3 -c "import flask, plotly, pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependências não encontradas. Instalando..."
    pip3 install flask plotly pandas
fi

# Verificar se a porta está disponível
PORT=${1:-8080}
HOST=${2:-127.0.0.1}

echo "🔍 Verificando porta $PORT..."
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️ Porta $PORT já está em uso. Tentando porta alternativa..."
    PORT=$((PORT + 1))
fi

echo "🌐 Iniciando servidor em http://$HOST:$PORT"
echo "📊 Acesse no navegador: http://localhost:$PORT"
echo ""
echo "💡 Dicas:"
echo "  - Use Ctrl+C para parar o servidor"
echo "  - Para acesso externo: ./start_web.sh 8080 0.0.0.0"
echo "  - Para debug: python3 src/web/app.py --debug"
echo ""

# Verificar conectividade local
echo "🧪 Testando conectividade..."
curl -s http://localhost:$PORT >/dev/null 2>&1 &
CURL_PID=$!

# Iniciar servidor
cd "$(dirname "$0")"
python3 src/web/app.py --host $HOST --port $PORT

# Cleanup
kill $CURL_PID 2>/dev/null || true

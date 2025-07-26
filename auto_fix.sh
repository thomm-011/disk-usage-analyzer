#!/bin/bash

# Auto-diagnóstico e correção para problemas intermitentes

echo "🤖 Auto-Fix: Disk Usage Analyzer"
echo "================================"

WSL_IP=$(hostname -I | awk '{print $1}')
PORT=8080

# Função para testar conectividade
test_connectivity() {
    local url=$1
    local name=$2
    
    if curl -s --connect-timeout 3 "$url" >/dev/null 2>&1; then
        echo "✅ $name: OK"
        return 0
    else
        echo "❌ $name: FALHA"
        return 1
    fi
}

# Função para iniciar servidor
start_server() {
    local port=$1
    echo "🚀 Iniciando servidor na porta $port..."
    
    cd /home/thomas/disk-usage-analyzer
    
    # Matar processos antigos
    pkill -f "python.*$port" 2>/dev/null || true
    sleep 1
    
    # Iniciar servidor debug em background
    python3 debug_web.py --host 0.0.0.0 --port $port > /tmp/server_$port.log 2>&1 &
    local pid=$!
    
    # Aguardar inicialização
    sleep 3
    
    # Verificar se está rodando
    if kill -0 $pid 2>/dev/null; then
        echo "✅ Servidor iniciado (PID: $pid)"
        return 0
    else
        echo "❌ Falha ao iniciar servidor"
        return 1
    fi
}

echo "🔍 Diagnóstico automático..."
echo "IP WSL2: $WSL_IP"
echo ""

# 1. Verificar se já há servidor rodando
echo "1️⃣ Verificando servidores existentes..."
if ss -tuln | grep ":$PORT " >/dev/null 2>&1; then
    echo "⚠️ Porta $PORT em uso. Testando conectividade..."
    
    if test_connectivity "http://localhost:$PORT/health" "localhost:$PORT"; then
        echo "✅ Servidor já funcionando!"
        echo "🌐 Acesse: http://$WSL_IP:$PORT"
        exit 0
    else
        echo "🧹 Servidor não responde. Reiniciando..."
        pkill -f "python.*$PORT" 2>/dev/null || true
        sleep 2
    fi
else
    echo "✅ Porta $PORT livre"
fi

# 2. Verificar dependências
echo ""
echo "2️⃣ Verificando dependências..."
if python3 -c "import flask, plotly" 2>/dev/null; then
    echo "✅ Dependências OK"
else
    echo "📦 Instalando dependências..."
    pip3 install --user flask plotly pandas 2>/dev/null
fi

# 3. Tentar iniciar servidor
echo ""
echo "3️⃣ Iniciando servidor..."
if start_server $PORT; then
    echo "✅ Servidor iniciado com sucesso!"
else
    echo "⚠️ Tentando porta alternativa..."
    PORT=8081
    if start_server $PORT; then
        echo "✅ Servidor iniciado na porta alternativa!"
    else
        echo "❌ Falha ao iniciar servidor"
        exit 1
    fi
fi

# 4. Testar conectividade
echo ""
echo "4️⃣ Testando conectividade..."
sleep 2

test_connectivity "http://localhost:$PORT" "localhost"
test_connectivity "http://$WSL_IP:$PORT" "WSL IP"

# 5. Mostrar informações finais
echo ""
echo "🎉 Servidor funcionando!"
echo "📍 URLs de acesso:"
echo "   🐧 No WSL2:    http://localhost:$PORT"
echo "   🪟 No Windows: http://$WSL_IP:$PORT"
echo ""
echo "💡 Comandos úteis:"
echo "   Testar: curl http://$WSL_IP:$PORT/health"
echo "   Parar:  pkill -f 'python.*$PORT'"
echo ""
echo "📄 Log do servidor: /tmp/server_$PORT.log"

# 6. Manter servidor rodando
echo "🔄 Monitorando servidor... (Ctrl+C para parar)"
while true; do
    if ! ss -tuln | grep ":$PORT " >/dev/null 2>&1; then
        echo "⚠️ Servidor parou. Reiniciando..."
        start_server $PORT
    fi
    sleep 10
done

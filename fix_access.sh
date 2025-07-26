#!/bin/bash

# Script para resolver problemas intermitentes de acesso

echo "🔧 Disk Usage Analyzer - Fix Access Issues"
echo "=========================================="

PORT=${1:-8080}
WSL_IP=$(hostname -I | awk '{print $1}')

echo "🔍 Diagnóstico atual:"
echo "  IP WSL2: $WSL_IP"
echo "  Porta: $PORT"
echo "  Data/Hora: $(date)"
echo ""

# 1. Limpar processos antigos
echo "🧹 Limpando processos antigos..."
pkill -f "python.*$PORT" 2>/dev/null || true
pkill -f "flask" 2>/dev/null || true
sleep 2

# 2. Verificar se a porta está livre
echo "🔍 Verificando porta $PORT..."
if ss -tuln | grep ":$PORT " >/dev/null 2>&1; then
    echo "⚠️ Porta $PORT ainda em uso. Tentando liberar..."
    sudo fuser -k $PORT/tcp 2>/dev/null || true
    sleep 2
fi

# 3. Verificar conectividade de rede
echo "🌐 Testando conectividade..."
if ping -c 1 -W 1 $WSL_IP >/dev/null 2>&1; then
    echo "✅ IP $WSL_IP acessível"
else
    echo "❌ Problema de conectividade com $WSL_IP"
fi

# 4. Verificar dependências
echo "📦 Verificando dependências..."
python3 -c "import flask, plotly, pandas; print('✅ Dependências OK')" 2>/dev/null || {
    echo "❌ Dependências em falta. Reinstalando..."
    pip3 install --user flask plotly pandas humanize rich
}

# 5. Testar diferentes portas se necessário
echo "🔍 Testando portas disponíveis..."
for test_port in $PORT 8081 8082 5000 3000; do
    if ! ss -tuln | grep ":$test_port " >/dev/null 2>&1; then
        echo "✅ Porta $test_port disponível"
        PORT=$test_port
        break
    fi
done

# 6. Criar arquivo de status
STATUS_FILE="/tmp/disk_analyzer_status.txt"
cat > $STATUS_FILE << EOF
Disk Usage Analyzer Status
==========================
Timestamp: $(date)
WSL IP: $WSL_IP
Port: $PORT
URLs:
  - WSL2: http://localhost:$PORT
  - Windows: http://$WSL_IP:$PORT
  - Direct: http://127.0.0.1:$PORT

Commands to access from Windows:
  curl http://$WSL_IP:$PORT
  
Port forwarding command (Windows PowerShell as Admin):
  netsh interface portproxy delete v4tov4 listenport=$PORT listenaddress=0.0.0.0
  netsh interface portproxy add v4tov4 listenport=$PORT listenaddress=0.0.0.0 connectport=$PORT connectaddress=$WSL_IP
EOF

echo "📄 Status salvo em: $STATUS_FILE"

# 7. Função de monitoramento
monitor_server() {
    local pid=$1
    local count=0
    while kill -0 $pid 2>/dev/null; do
        if [ $count -eq 0 ]; then
            echo "🚀 Servidor iniciado! Testando conectividade..."
            sleep 3
            
            # Testar conectividade
            if curl -s --connect-timeout 5 http://localhost:$PORT/health >/dev/null 2>&1; then
                echo "✅ Servidor respondendo em localhost:$PORT"
            else
                echo "⚠️ Servidor não responde em localhost:$PORT"
            fi
            
            if curl -s --connect-timeout 5 http://$WSL_IP:$PORT/health >/dev/null 2>&1; then
                echo "✅ Servidor respondendo em $WSL_IP:$PORT"
            else
                echo "⚠️ Servidor não responde em $WSL_IP:$PORT"
            fi
        fi
        
        count=$((count + 1))
        if [ $count -eq 10 ]; then
            echo "📊 Servidor rodando há $(($count * 5)) segundos"
            count=0
        fi
        sleep 5
    done
    echo "❌ Servidor parou de responder"
}

# 8. Iniciar servidor com monitoramento
echo ""
echo "🚀 Iniciando servidor na porta $PORT..."
echo "📍 URLs de acesso:"
echo "   WSL2:    http://localhost:$PORT"
echo "   Windows: http://$WSL_IP:$PORT"
echo "   Health:  http://$WSL_IP:$PORT/health"
echo ""
echo "💡 Deixe este terminal aberto e acesse no navegador do Windows"
echo "🛑 Use Ctrl+C para parar"
echo ""

cd "$(dirname "$0")"

# Tentar servidor debug primeiro (mais estável)
if [ -f "debug_web.py" ]; then
    echo "🐛 Iniciando servidor debug (mais estável)..."
    python3 debug_web.py --host 0.0.0.0 --port $PORT &
    SERVER_PID=$!
    
    # Aguardar inicialização
    sleep 3
    
    # Verificar se iniciou
    if kill -0 $SERVER_PID 2>/dev/null; then
        echo "✅ Servidor debug iniciado (PID: $SERVER_PID)"
        monitor_server $SERVER_PID
    else
        echo "❌ Falha ao iniciar servidor debug"
    fi
else
    echo "❌ Arquivo debug_web.py não encontrado"
fi

# Cleanup
echo "🧹 Limpando..."
kill $SERVER_PID 2>/dev/null || true

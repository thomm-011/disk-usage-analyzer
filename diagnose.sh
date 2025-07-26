#!/bin/bash

# Script de diagnóstico para problemas de conectividade

echo "🔍 Disk Usage Analyzer - Diagnóstico de Conectividade"
echo "===================================================="

PORT=${1:-8080}

echo "📊 Informações do Sistema:"
echo "  OS: $(uname -a)"
echo "  Python: $(python3 --version 2>/dev/null || echo 'Não encontrado')"
echo "  Diretório: $(pwd)"
echo ""

echo "🌐 Verificações de Rede:"

# Verificar se a porta está disponível
echo "  🔍 Verificando porta $PORT..."
if command -v netstat >/dev/null 2>&1; then
    if netstat -tuln | grep ":$PORT " >/dev/null; then
        echo "    ⚠️ Porta $PORT já está em uso:"
        netstat -tuln | grep ":$PORT "
    else
        echo "    ✅ Porta $PORT disponível"
    fi
else
    echo "    ⚠️ netstat não disponível"
fi

# Verificar conectividade localhost
echo "  🔍 Testando conectividade localhost..."
if command -v curl >/dev/null 2>&1; then
    if curl -s --connect-timeout 5 http://localhost:$PORT/health >/dev/null 2>&1; then
        echo "    ✅ localhost:$PORT acessível"
    else
        echo "    ❌ localhost:$PORT não acessível"
    fi
else
    echo "    ⚠️ curl não disponível"
fi

# Verificar firewall
echo "  🔍 Verificando firewall..."
if command -v ufw >/dev/null 2>&1; then
    if ufw status | grep -q "Status: active"; then
        echo "    ⚠️ UFW ativo - pode estar bloqueando conexões"
        ufw status | grep $PORT || echo "    Porta $PORT não configurada no UFW"
    else
        echo "    ✅ UFW inativo"
    fi
elif command -v iptables >/dev/null 2>&1; then
    if iptables -L | grep -q "DROP\|REJECT"; then
        echo "    ⚠️ iptables com regras restritivas detectadas"
    else
        echo "    ✅ iptables sem restrições aparentes"
    fi
else
    echo "    ℹ️ Firewall não detectado"
fi

# Verificar interfaces de rede
echo "  🔍 Interfaces de rede:"
if command -v ip >/dev/null 2>&1; then
    ip addr show | grep -E "inet " | grep -v "127.0.0.1" | head -3
elif command -v ifconfig >/dev/null 2>&1; then
    ifconfig | grep -E "inet " | grep -v "127.0.0.1" | head -3
else
    echo "    ⚠️ Comandos de rede não disponíveis"
fi

echo ""
echo "🐛 Iniciando servidor de debug..."
echo "   Acesse: http://localhost:$PORT"
echo "   Use Ctrl+C para parar"
echo ""

# Iniciar servidor de debug
cd "$(dirname "$0")"
python3 debug_web.py --host 0.0.0.0 --port $PORT

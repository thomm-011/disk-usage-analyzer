#!/bin/bash

# Comando simples para iniciar o Disk Usage Analyzer

clear
echo "🔍 Disk Usage Analyzer"
echo "====================="

cd /home/thomas/disk-usage-analyzer

# Detectar IP
WSL_IP=$(hostname -I | awk '{print $1}')

# Limpar processos antigos
pkill -f "python.*808" 2>/dev/null || true

# Iniciar servidor
echo "🚀 Iniciando servidor..."
python3 debug_web.py --host 0.0.0.0 --port 8080 > /dev/null 2>&1 &

# Aguardar inicialização
sleep 3

# Verificar se funcionou
if curl -s http://localhost:8080/health >/dev/null 2>&1; then
    echo "✅ Servidor funcionando!"
    echo ""
    echo "🌐 Acesse no navegador do Windows:"
    echo "   http://$WSL_IP:8080"
    echo ""
    echo "🔄 Servidor rodando em background"
    echo "🛑 Para parar: pkill -f python"
else
    echo "❌ Erro ao iniciar. Tente: ./auto_fix.sh"
fi

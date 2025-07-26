#!/bin/bash

echo "🚀 Push para GitHub - Disk Usage Analyzer"
echo "========================================"

# Verificar se estamos no diretório correto
if [ ! -f "README.md" ]; then
    echo "❌ Execute este script no diretório do projeto"
    exit 1
fi

echo "📋 Instruções:"
echo "1. Crie o repositório no GitHub primeiro:"
echo "   https://github.com/new"
echo "   Nome: disk-usage-analyzer"
echo "   Público, sem README"
echo ""

read -p "✅ Repositório criado no GitHub? (y/n): " created
if [ "$created" != "y" ]; then
    echo "❌ Crie o repositório primeiro e execute novamente"
    exit 1
fi

read -p "👤 Digite seu username do GitHub: " username
if [ -z "$username" ]; then
    echo "❌ Username é obrigatório"
    exit 1
fi

echo ""
echo "🔗 Configurando remote..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/$username/disk-usage-analyzer.git

echo "🌿 Configurando branch main..."
git branch -M main

echo "📤 Fazendo push..."
echo "⚠️ Você precisará inserir suas credenciais do GitHub"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Sucesso! Repositório publicado:"
    echo "🌐 https://github.com/$username/disk-usage-analyzer"
    echo ""
    echo "📋 Próximos passos:"
    echo "1. Acesse o repositório no GitHub"
    echo "2. Adicione screenshots se quiser"
    echo "3. Configure GitHub Pages se desejar"
    echo "4. Adicione topics/tags para melhor descoberta"
else
    echo ""
    echo "❌ Erro no push. Possíveis soluções:"
    echo "1. Verifique suas credenciais"
    echo "2. Configure token de acesso pessoal"
    echo "3. Verifique se o repositório foi criado"
fi

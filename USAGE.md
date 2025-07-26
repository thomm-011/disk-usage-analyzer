# 📖 Guia de Uso - Disk Usage Analyzer

## 🚀 Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/thomm-011/disk-usage-analyzer.git
cd disk-usage-analyzer

# Execute o script de instalação
./install.sh

# OU instale manualmente
pip3 install -r requirements.txt
pip3 install -e .
```

## 💻 Interface CLI

### Comandos Básicos

```bash
# Analisar diretório atual
python3 src/cli/main.py

# Analisar diretório específico
python3 src/cli/main.py /home/user

# Analisar com tamanho mínimo
python3 src/cli/main.py /var --min-size 10MB

# Analisar com profundidade limitada
python3 src/cli/main.py /usr --max-depth 3
```

### Filtros e Exclusões

```bash
# Excluir padrões específicos
python3 src/cli/main.py /home --exclude "*.log" "*.tmp" ".cache"

# Incluir arquivos ocultos
python3 src/cli/main.py /home --include-hidden

# Mostrar apenas arquivos grandes
python3 src/cli/main.py /var --large-files 100MB
```

### Exportação de Dados

```bash
# Exportar para JSON
python3 src/cli/main.py /home --export json --output report.json

# Exportar para CSV
python3 src/cli/main.py /home --export csv --output report.csv

# Modo silencioso (apenas exportar)
python3 src/cli/main.py /home --quiet --export json
```

### Exemplos Práticos

```bash
# Análise completa do diretório home
python3 src/cli/main.py /home --min-size 1MB --tree-items 25

# Encontrar arquivos grandes no sistema
python3 src/cli/main.py /var --large-files 50MB --quiet

# Análise rápida com exportação
python3 src/cli/main.py . --max-depth 2 --export json --output quick_report.json
```

## 🌐 Interface Web

### Iniciar Servidor

```bash
# Servidor local (padrão: localhost:8080)
python3 src/web/app.py

# Servidor personalizado
python3 src/web/app.py --host 0.0.0.0 --port 5000

# Modo debug
python3 src/web/app.py --debug
```

### Usando a Interface Web

1. **Acesse** `http://localhost:8080` no navegador
2. **Configure** o diretório e parâmetros de análise
3. **Clique** em "Analisar" para executar
4. **Explore** os gráficos e visualizações interativas

### Funcionalidades Web

- 📊 **Gráfico de Pizza** - Distribuição por diretórios
- 🗺️ **Treemap** - Visualização hierárquica
- 🌳 **Árvore de Diretórios** - Estrutura navegável
- 📄 **Lista de Arquivos Grandes** - Ordenada por tamanho
- 📋 **Tabela de Tipos** - Estatísticas por extensão

## 🛠️ Makefile

```bash
# Ver todos os comandos disponíveis
make help

# Instalar dependências
make install

# Executar exemplo
make example

# Executar interface web
make run-web

# Análises rápidas
make analyze-home    # Analisar /home
make analyze-var     # Analisar /var
make analyze-current # Analisar diretório atual
```

## ⚙️ Configuração

### Arquivo config.yaml

```yaml
general:
  default_path: "/home"
  min_size_threshold: "1KB"
  max_depth: 10

exclude_patterns:
  - "*.tmp"
  - "*.log"
  - ".git"
  - "__pycache__"

cli:
  tree_items: 20
  show_colors: true

web:
  host: "127.0.0.1"
  port: 8080
```

## 📊 Exemplos de Saída

### CLI - Resumo
```
📊 Resumo da Análise
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📁 Diretório           ┃ /home/user           ┃
┃ 💾 Tamanho Total       ┃ 15.2 GB              ┃
┃ 📄 Arquivos            ┃ 12,543               ┃
┃ 📁 Diretórios          ┃ 1,234                ┃
┃ 🔍 Maior Arquivo       ┃ video.mp4 (2.1 GB)   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━┛
```

### CLI - Árvore de Diretórios
```
🌳 Estrutura de Diretórios
📁 /home/user (15.2 GB)
├── 📁 Documents (8.5 GB)
│   ├── 📁 Projects (6.4 GB)
│   └── 📄 large_file.pdf (2.1 GB)
├── 📁 Downloads (4.2 GB)
└── 📁 Pictures (2.5 GB)
```

### JSON Export
```json
{
  "summary": {
    "path": "/home/user",
    "total_size": 16307200000,
    "total_size_human": "15.2 GB",
    "file_count": 12543,
    "dir_count": 1234
  },
  "directory_tree": {
    "name": "user",
    "size": 16307200000,
    "children": [...]
  }
}
```

## 🔧 Casos de Uso Comuns

### 1. Limpeza de Disco
```bash
# Encontrar arquivos grandes para remoção
python3 src/cli/main.py /home --large-files 100MB

# Identificar diretórios que consomem mais espaço
python3 src/cli/main.py /var --min-size 50MB --max-depth 2
```

### 2. Monitoramento de Sistema
```bash
# Análise completa do sistema
python3 src/cli/main.py / --exclude "/proc" "/sys" "/dev" --export json

# Monitorar logs
python3 src/cli/main.py /var/log --min-size 10MB
```

### 3. Desenvolvimento
```bash
# Analisar projeto
python3 src/cli/main.py ./my-project --exclude "node_modules" ".git"

# Encontrar arquivos temporários
python3 src/cli/main.py . --include-hidden | grep -E "\.(tmp|cache|log)$"
```

### 4. Relatórios
```bash
# Relatório completo em JSON
python3 src/cli/main.py /home --export json --output home_analysis.json

# Relatório CSV para planilhas
python3 src/cli/main.py /data --export csv --output data_usage.csv
```

## 🐛 Solução de Problemas

### Erro de Permissão
```bash
# Executar com sudo se necessário
sudo python3 src/cli/main.py /root

# Ou analisar apenas diretórios acessíveis
python3 src/cli/main.py /home --exclude "/root"
```

### Performance
```bash
# Limitar profundidade para diretórios grandes
python3 src/cli/main.py /usr --max-depth 3

# Usar tamanho mínimo para filtrar arquivos pequenos
python3 src/cli/main.py /var --min-size 1MB
```

### Memória
```bash
# Para diretórios muito grandes, use filtros
python3 src/cli/main.py /big-directory --min-size 10MB --max-depth 2
```

## 📈 Dicas de Performance

1. **Use filtros** - `--min-size` e `--max-depth` reduzem o tempo de análise
2. **Exclua diretórios** - Use `--exclude` para pular diretórios desnecessários
3. **Modo silencioso** - Use `--quiet` quando só precisar dos dados exportados
4. **Cache web** - A interface web mantém cache por 5 minutos

## 🤝 Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature
3. Execute os testes: `python3 tests/test_analyzer.py`
4. Faça commit das mudanças
5. Abra um Pull Request

## 📞 Suporte

- 📖 **Documentação**: README.md
- 🐛 **Issues**: GitHub Issues
- 💬 **Discussões**: GitHub Discussions
- 📧 **Email**: thomas@example.com

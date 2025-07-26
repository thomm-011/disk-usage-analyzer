# 🚀 Quick Start - Disk Usage Analyzer

## 🎯 Acesso Rápido ao Localhost

### ✅ **Você está no WSL2? Use isto:**

```bash
cd /home/thomas/disk-usage-analyzer
./start_wsl2.sh
```

**Então no Windows, acesse:** `http://172.21.9.158:8080`

### ✅ **Linux Nativo? Use isto:**

```bash
cd /home/thomas/disk-usage-analyzer
python3 src/web/app.py --host 0.0.0.0 --port 8080
```

**Acesse:** `http://localhost:8080`

### ✅ **Problemas? Use o Debug:**

```bash
cd /home/thomas/disk-usage-analyzer
python3 debug_web.py --host 0.0.0.0 --port 8080
```

**Acesse:** `http://localhost:8080` ou `http://172.21.9.158:8080`

## 🔧 Comandos Essenciais

### Instalação Rápida:
```bash
cd /home/thomas/disk-usage-analyzer
./install.sh
```

### Interface CLI:
```bash
python3 src/cli/main.py /home --min-size 1MB
```

### Exemplo de Uso:
```bash
python3 example.py
```

### Diagnóstico:
```bash
./diagnose.sh
```

## 🌐 URLs de Acesso

Dependendo do seu ambiente:

- **WSL2**: `http://172.21.9.158:8080`
- **Linux**: `http://localhost:8080`
- **Debug**: `http://127.0.0.1:8080`

## 🆘 Solução de Emergência

Se nada funcionar:

```bash
cd /home/thomas/disk-usage-analyzer
pkill -f python  # Mata processos Python
python3 debug_web.py --port 5000  # Usa porta diferente
```

Acesse: `http://localhost:5000` ou `http://172.21.9.158:5000`

## 📞 Precisa de Ajuda?

1. Leia: `TROUBLESHOOTING.md`
2. WSL2: `WSL2_ACCESS.md`
3. Uso completo: `USAGE.md`

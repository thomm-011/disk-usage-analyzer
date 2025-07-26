# 🐧 Acessando o Disk Usage Analyzer no WSL2

## 🔍 Problema Identificado
Você está usando **WSL2** (Windows Subsystem for Linux 2), que tem algumas particularidades de rede.

## 🌐 Soluções para Acesso

### ✅ **Solução 1: Acesso Direto via IP do WSL2**

O servidor está rodando em: `http://172.21.9.158:8080`

**No Windows:**
1. Abra o navegador (Chrome, Firefox, Edge)
2. Acesse: `http://172.21.9.158:8080`

### ✅ **Solução 2: Usar localhost com Port Forwarding**

**No PowerShell do Windows (como Administrador):**
```powershell
# Descobrir IP do WSL2
wsl hostname -I

# Fazer port forwarding
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=172.21.9.158
```

Depois acesse: `http://localhost:8080`

### ✅ **Solução 3: Script Automático para WSL2**

Criei um script que detecta automaticamente o IP:

```bash
# No WSL2, execute:
./start_wsl2.sh
```

### ✅ **Solução 4: Usar Windows Terminal**

Se você tem Windows Terminal:
1. Abra uma aba WSL2
2. Execute: `python3 debug_web.py --host 0.0.0.0 --port 8080`
3. No Windows, acesse: `http://172.21.9.158:8080`

## 🔧 Comandos Úteis para WSL2

### Descobrir IP do WSL2:
```bash
# No WSL2
hostname -I
ip addr show eth0 | grep inet

# No Windows PowerShell
wsl hostname -I
```

### Testar Conectividade:
```bash
# No WSL2
curl http://localhost:8080
curl http://172.21.9.158:8080

# No Windows
curl http://172.21.9.158:8080
```

### Verificar Portas:
```bash
# No WSL2
ss -tuln | grep 8080

# No Windows
netstat -an | findstr 8080
```

## 🚀 Inicialização Rápida

Execute este comando no WSL2:
```bash
cd /home/thomas/disk-usage-analyzer
python3 debug_web.py --host 0.0.0.0 --port 8080
```

**Então acesse no Windows:**
- `http://172.21.9.158:8080` (IP direto)
- `http://localhost:8080` (se configurou port forwarding)

## 🐛 Troubleshooting WSL2

### Problema: IP muda a cada reinicialização
**Solução:** Use script que detecta IP automaticamente

### Problema: Firewall do Windows bloqueia
**Solução:** 
```powershell
# No PowerShell como Admin
New-NetFirewallRule -DisplayName "WSL2 Port 8080" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
```

### Problema: Não consegue acessar do Windows
**Solução:** Verifique se o servidor está em `0.0.0.0:8080`, não `127.0.0.1:8080`

## 📱 Acesso via Celular/Tablet

Se quiser acessar de outros dispositivos na mesma rede:

1. **Descobrir IP do Windows:**
```cmd
ipconfig | findstr IPv4
```

2. **Configurar port forwarding:**
```powershell
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=172.21.9.158
```

3. **Acessar:** `http://IP_DO_WINDOWS:8080`

## ✨ Dica Final

Para facilitar, sempre use:
```bash
python3 debug_web.py --host 0.0.0.0 --port 8080
```

E acesse via: `http://172.21.9.158:8080`

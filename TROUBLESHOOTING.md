# 🔧 Troubleshooting - Disk Usage Analyzer

## 🌐 Problemas de Acesso ao Localhost

### ❌ Problema: "Não consigo acessar localhost:8080"

#### 🔍 **Diagnóstico Rápido**
```bash
# Execute o diagnóstico automático
./diagnose.sh 8080

# OU teste o servidor de debug
python3 debug_web.py --host 0.0.0.0 --port 8080
```

#### 🛠️ **Soluções Passo a Passo**

### 1. **Verificar se o Servidor Está Rodando**
```bash
# Iniciar servidor
python3 src/web/app.py --host 0.0.0.0 --port 8080

# Verificar se está escutando
netstat -tuln | grep 8080
# OU
ss -tuln | grep 8080
```

**Saída esperada:**
```
tcp    0    0 0.0.0.0:8080    0.0.0.0:*    LISTEN
```

### 2. **Testar Conectividade Local**
```bash
# Teste básico
curl http://localhost:8080

# Teste com timeout
curl --connect-timeout 5 http://localhost:8080

# Teste health check
curl http://localhost:8080/health
```

### 3. **Verificar Firewall**

#### Ubuntu/Debian (UFW):
```bash
# Verificar status
sudo ufw status

# Se ativo, liberar porta
sudo ufw allow 8080

# OU desabilitar temporariamente
sudo ufw disable
```

#### CentOS/RHEL (firewalld):
```bash
# Verificar status
sudo firewall-cmd --state

# Liberar porta
sudo firewall-cmd --add-port=8080/tcp --permanent
sudo firewall-cmd --reload
```

#### iptables:
```bash
# Verificar regras
sudo iptables -L

# Liberar porta (temporário)
sudo iptables -I INPUT -p tcp --dport 8080 -j ACCEPT
```

### 4. **Problemas de Porta**

#### Porta em uso:
```bash
# Encontrar processo usando a porta
sudo lsof -i :8080
# OU
sudo netstat -tulpn | grep 8080

# Matar processo se necessário
sudo kill -9 <PID>

# Usar porta alternativa
python3 src/web/app.py --port 8081
```

#### Testar portas disponíveis:
```bash
# Testar várias portas
for port in 8080 8081 8082 5000 3000; do
    if ! lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; then
        echo "Porta $port disponível"
        break
    fi
done
```

### 5. **Problemas de Permissão**

#### Portas privilegiadas (< 1024):
```bash
# Use sudo para portas < 1024
sudo python3 src/web/app.py --port 80

# OU use porta não privilegiada
python3 src/web/app.py --port 8080
```

### 6. **Problemas de DNS/Hosts**

#### Verificar resolução localhost:
```bash
# Testar resolução
nslookup localhost
ping -c 1 localhost

# Verificar arquivo hosts
cat /etc/hosts | grep localhost
```

**Deve conter:**
```
127.0.0.1   localhost
::1         localhost
```

### 7. **Problemas de Dependências**

#### Instalar dependências em falta:
```bash
# Instalar dependências web
pip3 install flask plotly pandas

# Verificar instalação
python3 -c "import flask, plotly, pandas; print('OK')"

# Reinstalar se necessário
pip3 uninstall flask plotly pandas
pip3 install flask plotly pandas
```

### 8. **Problemas de Ambiente Virtual**

#### Se usando venv:
```bash
# Ativar ambiente
source venv/bin/activate

# Instalar dependências no venv
pip install -r requirements.txt

# Executar aplicação
python src/web/app.py
```

## 🐛 Modo Debug Avançado

### Servidor de Debug Simples:
```bash
# Iniciar servidor debug
python3 debug_web.py --debug --host 0.0.0.0 --port 8080

# Acessar: http://localhost:8080
```

### Logs Detalhados:
```bash
# Executar com logs verbosos
FLASK_ENV=development python3 src/web/app.py --debug

# OU com Python logging
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
exec(open('src/web/app.py').read())
"
```

### Teste Manual da API:
```bash
# Testar API diretamente
curl -X POST http://localhost:8080/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"path": "/home", "min_size": "1KB", "max_depth": 3}'
```

## 🌐 Problemas de Acesso Externo

### Acesso de Outras Máquinas:
```bash
# Iniciar com bind em todas as interfaces
python3 src/web/app.py --host 0.0.0.0 --port 8080

# Descobrir IP da máquina
ip addr show | grep "inet " | grep -v 127.0.0.1

# Acessar de outra máquina: http://IP_DA_MAQUINA:8080
```

### Problemas de Rede:
```bash
# Verificar conectividade
ping IP_DA_MAQUINA

# Testar porta específica
telnet IP_DA_MAQUINA 8080
# OU
nc -zv IP_DA_MAQUINA 8080
```

## 📱 Problemas no Navegador

### Cache do Navegador:
- Pressione `Ctrl+F5` (hard refresh)
- Abra em aba anônima/privada
- Limpe cache do navegador

### JavaScript Desabilitado:
- Verifique se JavaScript está habilitado
- Teste em navegador diferente

### Bloqueadores:
- Desabilite ad-blockers temporariamente
- Verifique extensões do navegador

## 🔧 Comandos de Diagnóstico Úteis

```bash
# Status completo do sistema
./diagnose.sh

# Verificar processos Python
ps aux | grep python

# Verificar conexões de rede
ss -tuln | grep 8080

# Verificar logs do sistema
journalctl -f | grep python

# Testar com diferentes navegadores
# Chrome/Chromium
google-chrome http://localhost:8080

# Firefox
firefox http://localhost:8080

# Lynx (terminal)
lynx http://localhost:8080
```

## 🆘 Soluções Rápidas

### Solução 1: Reiniciar Tudo
```bash
# Matar todos os processos Python
pkill -f python

# Reiniciar aplicação
python3 src/web/app.py --host 0.0.0.0 --port 8080
```

### Solução 2: Usar Porta Diferente
```bash
# Testar porta 5000 (padrão Flask)
python3 src/web/app.py --port 5000

# Acessar: http://localhost:5000
```

### Solução 3: Modo Mínimo
```bash
# Usar servidor debug simples
python3 debug_web.py

# Acessar: http://localhost:8080
```

## 📞 Ainda com Problemas?

1. **Execute o diagnóstico**: `./diagnose.sh`
2. **Teste o servidor debug**: `python3 debug_web.py`
3. **Verifique os logs** da aplicação
4. **Teste em navegador diferente**
5. **Reinicie a máquina** se necessário

### Informações para Suporte:
- Sistema operacional: `uname -a`
- Versão Python: `python3 --version`
- Saída do diagnóstico: `./diagnose.sh > diagnostico.txt`
- Logs da aplicação
- Mensagens de erro específicas

#!/usr/bin/env python3
"""
Versão simplificada da aplicação web para debug
"""

from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Template HTML simples
SIMPLE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Disk Usage Analyzer - Debug</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .status { padding: 20px; background: #e8f5e8; border-radius: 5px; margin: 20px 0; }
        .error { background: #ffe8e8; }
        .info { background: #e8f0ff; }
        pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
        button { padding: 10px 20px; background: #007cba; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #005a87; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Disk Usage Analyzer - Debug Mode</h1>
        
        <div class="status">
            <h3>✅ Servidor Web Funcionando!</h3>
            <p>Se você está vendo esta página, o servidor Flask está rodando corretamente.</p>
        </div>
        
        <div class="info">
            <h3>📊 Informações do Sistema</h3>
            <ul>
                <li><strong>Diretório atual:</strong> {{ current_dir }}</li>
                <li><strong>Python:</strong> {{ python_version }}</li>
                <li><strong>Flask:</strong> {{ flask_version }}</li>
                <li><strong>Host:</strong> {{ host }}</li>
                <li><strong>Porta:</strong> {{ port }}</li>
            </ul>
        </div>
        
        <div class="info">
            <h3>🔧 Próximos Passos</h3>
            <ol>
                <li>Verifique se consegue acessar esta página</li>
                <li>Teste a API básica clicando no botão abaixo</li>
                <li>Se a API <strong>funcionar</strong>, o servidor está OK</li>
                <li>Se a API <strong>não funcionar</strong>, o problema está no servidor/backend</li>
            </ol>
            <button onclick="testAPI()">🧪 Testar API</button>
        </div>
        
        <div id="apiResult" style="display: none;">
            <h3>📡 Resultado da API</h3>
            <pre id="apiOutput"></pre>
        </div>
        
        <div class="info">
            <h3>🌐 URLs de Acesso</h3>
            <ul>
                <li><a href="http://localhost:{{ port }}">http://localhost:{{ port }}</a></li>
                <li><a href="http://127.0.0.1:{{ port }}">http://127.0.0.1:{{ port }}</a></li>
                <li><a href="http://{{ host }}:{{ port }}">http://{{ host }}:{{ port }}</a></li>
            </ul>
        </div>
    </div>
    
    <script>
        async function testAPI() {
            try {
                const response = await fetch('/api/test');
                const data = await response.json();
                document.getElementById('apiOutput').textContent = JSON.stringify(data, null, 2);
                document.getElementById('apiResult').style.display = 'block';
            } catch (error) {
                document.getElementById('apiOutput').textContent = 'Erro: ' + error.message;
                document.getElementById('apiResult').style.display = 'block';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Página principal de debug"""
    import sys
    import flask
    
    return render_template_string(SIMPLE_TEMPLATE,
        current_dir=os.getcwd(),
        python_version=sys.version,
        flask_version=flask.__version__,
        host=app.config.get('HOST', '127.0.0.1'),
        port=app.config.get('PORT', 8080)
    )

@app.route('/api/test')
def api_test():
    """API de teste"""
    return {
        'status': 'success',
        'message': 'API funcionando corretamente!',
        'timestamp': str(__import__('datetime').datetime.now()),
        'server_info': {
            'python_version': __import__('sys').version,
            'working_directory': os.getcwd(),
            'environment': dict(os.environ)
        }
    }

@app.route('/health')
def health():
    """Health check"""
    return {'status': 'healthy', 'service': 'disk-usage-analyzer'}

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Debug Web Server')
    parser.add_argument('--host', default='127.0.0.1', help='Host')
    parser.add_argument('--port', type=int, default=8080, help='Port')
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    
    args = parser.parse_args()
    
    app.config['HOST'] = args.host
    app.config['PORT'] = args.port
    
    print(f"🐛 Debug Web Server")
    print(f"🌐 Acesse: http://{args.host}:{args.port}")
    print(f"🔍 Health check: http://{args.host}:{args.port}/health")
    print(f"📡 API test: http://{args.host}:{args.port}/api/test")
    print("=" * 50)
    
    app.run(host=args.host, port=args.port, debug=args.debug)

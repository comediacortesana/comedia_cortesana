#!/usr/bin/env python3
"""
Servidor HTTP local para desarrollo rápido
Permite probar cambios en index.html sin hacer push a GitHub
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Puerto por defecto
PORT = 8000

# Directorio del proyecto
PROJECT_ROOT = Path(__file__).parent.parent

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personalizado con mejor logging"""
    
    def log_message(self, format, *args):
        """Log mejorado con colores"""
        message = format % args
        # Colorear según el método HTTP
        if 'GET' in message:
            print(f"✅ {message}")
        elif '404' in message:
            print(f"❌ {message}")
        else:
            print(f"ℹ️  {message}")
    
    def end_headers(self):
        """Agregar headers CORS y cache control"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    """Inicia el servidor local"""
    # Cambiar al directorio del proyecto
    os.chdir(PROJECT_ROOT)
    
    # Verificar que index.html existe
    if not (PROJECT_ROOT / 'index.html').exists():
        print(f"❌ Error: No se encontró index.html en {PROJECT_ROOT}")
        sys.exit(1)
    
    # Crear servidor
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print("="*60)
        print("🚀 SERVIDOR LOCAL DE DESARROLLO")
        print("="*60)
        print(f"📂 Directorio: {PROJECT_ROOT}")
        print(f"🌐 URL: http://localhost:{PORT}/")
        print(f"📄 index.html: http://localhost:{PORT}/index.html")
        print("="*60)
        print("💡 Presiona Ctrl+C para detener el servidor")
        print("="*60)
        print()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Servidor detenido")
            sys.exit(0)

if __name__ == '__main__':
    main()


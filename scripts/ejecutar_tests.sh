#!/bin/bash
# Script helper para ejecutar tests de persistencia

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🧪 Script de Testing Automatizado"
echo "=================================="
echo ""

# Verificar si Python está instalado
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python no está instalado${NC}"
    exit 1
fi

# Verificar si Selenium está instalado
if ! python -c "import selenium" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Selenium no está instalado. Instalando...${NC}"
    pip install selenium webdriver-manager
fi

# Detectar URL de la aplicación
URL=""
EMAIL=""

# URL por defecto: GitHub Pages
DEFAULT_URL="https://comediacortesana.github.io/comedia_cortesana/"

# Opción 1: Verificar si hay un servidor local corriendo
if curl -s http://localhost:8000 > /dev/null 2>&1; then
    URL="http://localhost:8000"
    echo -e "${GREEN}✅ Servidor local detectado en http://localhost:8000${NC}"
elif curl -s http://localhost:3000 > /dev/null 2>&1; then
    URL="http://localhost:3000"
    echo -e "${GREEN}✅ Servidor local detectado en http://localhost:3000${NC}"
elif curl -s http://127.0.0.1:8000 > /dev/null 2>&1; then
    URL="http://127.0.0.1:8000"
    echo -e "${GREEN}✅ Servidor local detectado en http://127.0.0.1:8000${NC}"
elif curl -s "$DEFAULT_URL" > /dev/null 2>&1; then
    URL="$DEFAULT_URL"
    echo -e "${GREEN}✅ GitHub Pages detectado: $DEFAULT_URL${NC}"
else
    echo -e "${YELLOW}⚠️  No se detectó servidor local ni GitHub Pages${NC}"
    echo ""
    echo "Opciones:"
    echo "1. Usar GitHub Pages: $DEFAULT_URL"
    echo "2. Iniciar servidor Python local: python -m http.server 8000"
    echo "3. Especificar URL manualmente"
    echo ""
    read -p "¿Qué URL quieres usar? (Enter para GitHub Pages): " URL_INPUT
    if [ -z "$URL_INPUT" ]; then
        URL="$DEFAULT_URL"
    else
        URL="$URL_INPUT"
    fi
fi

# Solicitar email
if [ -z "$EMAIL" ]; then
    read -p "Ingresa el email del usuario admin: " EMAIL
fi

if [ -z "$EMAIL" ]; then
    echo -e "${RED}❌ Email requerido${NC}"
    exit 1
fi

echo ""
echo "📋 Configuración:"
echo "   URL: $URL"
echo "   Email: $EMAIL"
echo ""

# Preguntar si quiere iniciar servidor si no está corriendo
if ! curl -s "$URL" > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  No se puede conectar a $URL${NC}"
    read -p "¿Quieres iniciar un servidor Python simple en el puerto 8000? (s/n): " START_SERVER
    
    if [ "$START_SERVER" = "s" ] || [ "$START_SERVER" = "S" ]; then
        echo "Iniciando servidor en http://localhost:8000..."
        echo "Presiona Ctrl+C para detener el servidor después de los tests"
        echo ""
        
        # Iniciar servidor en background
        cd "$(dirname "$0")/.."
        python -m http.server 8000 > /dev/null 2>&1 &
        SERVER_PID=$!
        
        # Esperar a que el servidor esté listo
        sleep 2
        
        URL="http://localhost:8000"
        echo -e "${GREEN}✅ Servidor iniciado (PID: $SERVER_PID)${NC}"
        echo ""
    else
        echo -e "${RED}❌ No se puede ejecutar tests sin servidor${NC}"
        exit 1
    fi
fi

# Ejecutar tests
echo "🚀 Ejecutando tests..."
echo ""

python scripts/test_edicion_persistencia.py --url "$URL" --email "$EMAIL"

# Limpiar: matar servidor si lo iniciamos
if [ ! -z "$SERVER_PID" ]; then
    echo ""
    echo "Deteniendo servidor..."
    kill $SERVER_PID 2>/dev/null
fi


#!/bin/bash
# Script para iniciar servidor de desarrollo local
# Uso: ./scripts/iniciar_desarrollo.sh

cd "$(dirname "$0")/.."

echo "🚀 Iniciando servidor de desarrollo local..."
echo ""

# Verificar si Python está disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

# Iniciar servidor
python3 scripts/servidor_local.py


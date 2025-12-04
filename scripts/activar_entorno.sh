#!/bin/bash
# Script para activar el entorno conda delia
# Uso: source scripts/activar_entorno.sh

# Obtener el directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_ROOT"

# Verificar si conda está disponible
if ! command -v conda &> /dev/null; then
    echo "❌ Conda no está instalado o no está en el PATH"
    echo "💡 Instala conda desde: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Inicializar conda si no está inicializado
if [ -z "$CONDA_DEFAULT_ENV" ]; then
    eval "$(conda shell.bash hook)"
fi

# Activar entorno delia
echo "🔧 Activando entorno conda 'delia'..."
conda activate delia

if [ $? -eq 0 ]; then
    echo "✅ Entorno 'delia' activado"
    echo "🐍 Python: $(python --version)"
    echo "📦 Pip: $(pip --version)"
    echo ""
    echo "💡 Para desactivar: conda deactivate"
else
    echo "❌ Error activando entorno 'delia'"
    echo "💡 Crear entorno con: conda env create -f environment.yml"
    exit 1
fi


#!/bin/bash
# ============================================================================
# Script de prueba local para keep_supabase_active.py
# Uso: bash scripts/test_keep_active.sh
# ============================================================================

echo "======================================================================"
echo "🧪 PRUEBA LOCAL: Keep Supabase Active"
echo "======================================================================"
echo ""

# Cargar credenciales desde .env si existe
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
    echo "✅ Credenciales cargadas desde .env"
elif [ -f scripts/.env ]; then
    export $(grep -v '^#' scripts/.env | xargs)
    echo "✅ Credenciales cargadas desde scripts/.env"
else
    echo "⚠️  Archivo .env no encontrado"
    echo ""
    echo "Por favor, configura las variables de entorno:"
    echo "  export SUPABASE_URL='https://kyxxpoewwjixbpcezays.supabase.co'"
    echo "  export SUPABASE_KEY='tu-anon-public-key'"
    echo ""
    exit 1
fi

echo ""
echo "🐍 Ejecutando script Python..."
echo ""

# Ejecutar el script
python3 scripts/keep_supabase_active.py

exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
    echo "✅ Prueba exitosa - El script funciona correctamente"
    echo "📝 Siguiente paso: Subir a GitHub y configurar Actions"
else
    echo "❌ Prueba fallida - Revisa los errores arriba"
    echo "💡 Verifica que las credenciales son correctas"
fi

echo "======================================================================"

exit $exit_code


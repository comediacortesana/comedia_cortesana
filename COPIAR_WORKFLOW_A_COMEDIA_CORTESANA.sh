#!/bin/bash
# Script para copiar el workflow al repositorio comedia_cortesana

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📋 Copiando workflow al repositorio comedia_cortesana...${NC}"

# Ruta del repositorio destino
REPO_DESTINO="/Users/ivansimo/Documents/2025/ITEM/comedia_cortesana"

# Verificar si existe el repositorio destino
if [ ! -d "$REPO_DESTINO" ]; then
    echo -e "${YELLOW}⚠️  El repositorio no existe. Clonando...${NC}"
    cd /Users/ivansimo/Documents/2025/ITEM
    git clone https://github.com/comediacortesana/comedia_cortesana.git
fi

# Crear carpetas necesarias
mkdir -p "$REPO_DESTINO/.github/workflows"
mkdir -p "$REPO_DESTINO/scripts"

# Copiar archivos
echo -e "${GREEN}📁 Copiando archivos...${NC}"
cp .github/workflows/backup-supabase.yml "$REPO_DESTINO/.github/workflows/"
cp scripts/backup_supabase_completo.py "$REPO_DESTINO/scripts/"

echo -e "${GREEN}✅ Archivos copiados exitosamente${NC}"
echo ""
echo -e "${YELLOW}📝 Próximos pasos:${NC}"
echo "1. Abre GitHub Desktop"
echo "2. Selecciona el repositorio 'comedia_cortesana'"
echo "3. Verás los archivos nuevos en 'Changes'"
echo "4. Haz commit con el mensaje: '🔄 Agregar automatización de backup de Supabase'"
echo "5. Haz push a origin"
echo ""
echo -e "${GREEN}¡Listo!${NC}"

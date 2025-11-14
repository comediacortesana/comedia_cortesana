# 🚀 Guía Rápida: Cómo Ejecutar los Scripts

## ⚠️ Importante: Desde dónde ejecutar

**SIEMPRE ejecuta los scripts desde el directorio raíz del proyecto**, NO desde dentro de `scripts/`:

```bash
# ✅ CORRECTO (desde raíz del proyecto)
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/comedia_cortesana
python scripts/sync_to_supabase.py --file datos_obras.json

# ❌ INCORRECTO (desde dentro de scripts/)
cd scripts
python scripts/sync_to_supabase.py  # Esto busca scripts/scripts/...
```

## 📋 Comandos Rápidos

### 1. Sincronizar JSON → Supabase

```bash
# Desde el directorio raíz del proyecto
python scripts/sync_to_supabase.py --file datos_obras.json --dry-run
python scripts/sync_to_supabase.py --file datos_obras.json
```

### 2. Hacer Backup de Supabase → JSON

```bash
# Desde el directorio raíz del proyecto
python scripts/backup_from_supabase.py --output datos_obras_backup.json
```

### 3. Sincronizar con Google Sheets

```bash
# Desde el directorio raíz del proyecto
python scripts/sync_to_sheets.py --file datos_obras.json --spreadsheet-id TU_ID
```

## 🔧 Configuración Inicial

1. **Instalar dependencias** (solo una vez):
```bash
pip install -r scripts/requirements.txt
```

2. **Configurar variables de entorno**:
```bash
# Copiar archivo de ejemplo
cp scripts/.env.example scripts/.env

# Editar scripts/.env con tus credenciales
# - SUPABASE_URL
# - SUPABASE_KEY
# - GOOGLE_SHEETS_CREDENTIALS_FILE (opcional)
# - GOOGLE_SHEETS_SPREADSHEET_ID (opcional)
```

## 🐛 Troubleshooting

### Error: "No module named 'supabase'"
**Solución:** Instala las dependencias:
```bash
pip install -r scripts/requirements.txt
```

### Error: "SUPABASE_URL y SUPABASE_KEY deben estar definidos"
**Solución:** Crea el archivo `scripts/.env` con tus credenciales (ver arriba)

### Error: "can't open file 'scripts/scripts/...'"
**Solución:** Estás ejecutando desde dentro de `scripts/`. Vuelve al directorio raíz:
```bash
cd ..  # Volver al directorio raíz
python scripts/sync_to_supabase.py ...
```

### Error: "FileNotFoundError: datos_obras.json"
**Solución:** Asegúrate de que el archivo existe en el directorio raíz, o especifica la ruta completa:
```bash
python scripts/sync_to_supabase.py --file /ruta/completa/datos_obras.json
```

## 📚 Más Información

- Ver [scripts/README.md](./scripts/README.md) para documentación completa
- Ver [ARQUITECTURA_SUPABASE_PRINCIPAL.md](./ARQUITECTURA_SUPABASE_PRINCIPAL.md) para entender la arquitectura


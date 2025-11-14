# 🔧 Corregir Fuente: FUENTESXI → Fuentes IX

Este script corrige el valor incorrecto "FUENTESXI" a "Fuentes IX" tanto en el JSON local como en Supabase.

## 📋 Uso

### 1. Activar entorno conda

```bash
conda activate delia
```

### 2. Ver qué se cambiaría (dry-run)

```bash
# Solo JSON
python scripts/corregir_fuente_fuentesxi.py --dry-run --solo-json

# Solo Supabase
python scripts/corregir_fuente_fuentesxi.py --dry-run --solo-supabase

# Ambos
python scripts/corregir_fuente_fuentesxi.py --dry-run
```

### 3. Aplicar cambios

```bash
# Solo JSON
python scripts/corregir_fuente_fuentesxi.py --solo-json

# Solo Supabase (requiere confirmación)
python scripts/corregir_fuente_fuentesxi.py --solo-supabase

# Ambos (JSON primero, luego Supabase con confirmación)
python scripts/corregir_fuente_fuentesxi.py
```

## ⚠️ Importante

- **JSON**: Los cambios se aplican inmediatamente
- **Supabase**: Requiere confirmación manual antes de actualizar
- **Backup**: Se recomienda hacer backup del JSON antes de aplicar cambios

## 📊 Estadísticas

Según el último análisis:
- **376 obras** tienen "FUENTESXI" que deben corregirse
- El cambio afecta el campo `fuente` o `Fuente Principal`

## 🔄 Proceso Recomendado

1. **Hacer backup del JSON**:
   ```bash
   cp datos_obras.json datos_obras_backup_$(date +%Y%m%d).json
   ```

2. **Verificar cambios**:
   ```bash
   python scripts/corregir_fuente_fuentesxi.py --dry-run
   ```

3. **Aplicar en JSON**:
   ```bash
   python scripts/corregir_fuente_fuentesxi.py --solo-json
   ```

4. **Aplicar en Supabase**:
   ```bash
   python scripts/corregir_fuente_fuentesxi.py --solo-supabase
   ```

5. **Verificar**:
   - Revisar el JSON actualizado
   - Verificar en Supabase que los cambios se aplicaron
   - Probar la aplicación web


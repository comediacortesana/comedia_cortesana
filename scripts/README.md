# 📜 Scripts de Sincronización - DELIA

Scripts de Python para trabajar con datos locales y sincronizarlos con Supabase y Google Sheets.

## 🚀 Instalación

1. **Instalar dependencias:**

```bash
pip install -r scripts/requirements.txt
```

2. **Configurar variables de entorno:**

Copia `scripts/.env.example` a `scripts/.env` y completa con tus credenciales:

```bash
cp scripts/.env.example scripts/.env
```

Edita `scripts/.env` con tus credenciales:
- `SUPABASE_URL`: URL de tu proyecto Supabase
- `SUPABASE_KEY`: Service role key de Supabase
- `GOOGLE_SHEETS_CREDENTIALS_FILE`: Ruta al archivo de credenciales JSON de Google
- `GOOGLE_SHEETS_SPREADSHEET_ID`: ID de tu hoja de cálculo

## 📋 Scripts Disponibles

### 1. `sync_to_supabase.py`

Sincroniza datos locales con Supabase.

**Uso:**
```bash
# Sincronizar desde datos_obras.json
python scripts/sync_to_supabase.py

# Especificar archivo
python scripts/sync_to_supabase.py --file mi_archivo.json

# Dry run (simular sin guardar)
python scripts/sync_to_supabase.py --dry-run

# Especificar tamaño de lote
python scripts/sync_to_supabase.py --batch-size 50
```

**Opciones:**
- `--file`: Archivo JSON con los datos (default: `datos_obras.json`)
- `--dry-run`: Simular sincronización sin guardar cambios
- `--batch-size`: Tamaño del lote para sincronización (default: 100)

### 2. `sync_to_sheets.py`

Sincroniza datos locales con Google Sheets.

**Uso:**
```bash
# Sincronizar desde datos_obras.json
python scripts/sync_to_sheets.py

# Especificar archivo y spreadsheet
python scripts/sync_to_sheets.py --file mi_archivo.json --spreadsheet-id ABC123

# Dry run
python scripts/sync_to_sheets.py --dry-run
```

**Opciones:**
- `--file`: Archivo JSON con los datos (default: `datos_obras.json`)
- `--spreadsheet-id`: ID de la hoja de cálculo (o usar variable de entorno)
- `--sheet-name`: Nombre de la hoja (default: `Obras`)
- `--dry-run`: Simular sincronización sin guardar cambios

### 3. `backup_from_supabase.py`

Hace backup de todas las obras de Supabase a un archivo JSON.

**Uso:**
```bash
# Hacer backup
python scripts/backup_from_supabase.py

# Especificar archivo de salida
python scripts/backup_from_supabase.py --output backup_2025-01-15.json

# Dry run
python scripts/backup_from_supabase.py --dry-run
```

**Opciones:**
- `--output`: Archivo JSON de salida (default: `datos_obras.json`)
- `--dry-run`: Simular backup sin guardar archivo

### 4. `validate.py`

Valida datos antes de sincronizar (usado internamente por otros scripts).

**Uso directo:**
```python
from scripts.validate import DataValidator

validator = DataValidator()
is_valid, errors, warnings = validator.validate_obra(obra_dict)
```

## 📁 Estructura de Archivos

```
scripts/
├── README.md                 # Esta documentación
├── requirements.txt           # Dependencias Python
├── .env.example              # Ejemplo de configuración
├── schema.py                 # Definición de campos y validaciones
├── supabase_client.py        # Cliente de Supabase
├── validate.py               # Validación de datos
├── sync_to_supabase.py      # Sincronización con Supabase
├── sync_to_sheets.py        # Sincronización con Google Sheets
├── backup_from_supabase.py  # Backup de Supabase a JSON
└── migrate_data.py          # Migraciones de datos
```

## 🔧 Módulos Principales

### `schema.py`

Define todos los campos del sistema y sus tipos. Útil para:
- Validar datos
- Documentar estructura
- Generar formularios
- Migraciones

### `supabase_client.py`

Cliente para interactuar con Supabase:
- Obtener obras
- Crear/actualizar obras
- Gestionar cambios pendientes
- Aprobar/rechazar cambios

### `validate.py`

Validador de datos:
- Valida estructura de campos
- Valida tipos de datos
- Valida reglas de negocio
- Transforma datos a formato consistente

## 💡 Ejemplos de Uso

### Ejemplo 1: Sincronizar datos extraídos automáticamente

```bash
# 1. Extraer datos con tu script de IA/extracción
python mi_script_extraccion.py > datos_nuevos.json

# 2. Validar antes de sincronizar
python scripts/sync_to_supabase.py --file datos_nuevos.json --dry-run

# 3. Si todo está bien, sincronizar realmente
python scripts/sync_to_supabase.py --file datos_nuevos.json
```

### Ejemplo 2: Sincronizar con Google Sheets para revisión

```bash
# Sincronizar a Sheets para que editores puedan revisar
python scripts/sync_to_sheets.py --file datos_validados.json
```

### Ejemplo 4: Usar en scripts personalizados

```python
from scripts.supabase_client import SupabaseSync
from scripts.validate import DataValidator

# Validar y sincronizar una obra
validator = DataValidator()
sync = SupabaseSync()

obra = {
    'id': 1234,
    'titulo': 'Nueva Obra',
    # ... más campos
}

# Validar
is_valid, errors, warnings = validator.validate_obra(obra)
if is_valid:
    obra_transformada = validator.transform_obra(obra)
    resultado = sync.upsert_obra(obra_transformada)
    print(f"Obra {resultado['id']} sincronizada")
else:
    print(f"Errores: {errors}")
```

## 🔐 Seguridad

- **Nunca commits el archivo `.env`** con credenciales reales
- Usa variables de entorno en producción
- El archivo `.env.example` está en `.gitignore`
- Las credenciales de Google deben estar en un archivo seguro

## 🐛 Troubleshooting

### Error: "SUPABASE_URL y SUPABASE_KEY deben estar definidos"

**Solución:** Asegúrate de tener un archivo `.env` en la carpeta `scripts/` con las credenciales correctas.

### Error: "google-api-python-client no está instalado"

**Solución:** 
```bash
pip install -r scripts/requirements.txt
```

### Error: "Archivo no encontrado"

**Solución:** Verifica que el archivo JSON existe y la ruta es correcta. Usa rutas absolutas si es necesario.

### Error de permisos en Google Sheets

**Solución:** 
1. Verifica que el archivo de credenciales JSON es válido
2. Asegúrate de que el servicio tiene permisos de escritura en la hoja
3. Verifica que el `spreadsheet_id` es correcto

## 📚 Referencias

- [Documentación de Supabase Python Client](https://supabase.com/docs/reference/python/introduction)
- [Google Sheets API Python Quickstart](https://developers.google.com/sheets/api/quickstart/python)
- [CAMPO_MIGRACIONES.md](../CAMPO_MIGRACIONES.md) - Guía de migraciones de campos

## 🤝 Contribuir

Al agregar nuevos scripts o modificar existentes:

1. Documenta los cambios en este README
2. Actualiza `schema.py` si agregas nuevos campos
3. Agrega validaciones en `validate.py` si es necesario
4. Prueba con `--dry-run` antes de sincronizar datos reales

---

**Última actualización:** 2025-01-XX


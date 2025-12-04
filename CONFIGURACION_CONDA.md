# 🐍 Configuración del Entorno Conda DELIA

Este proyecto usa **Conda** para gestionar las dependencias de Python de forma aislada y reproducible.

## 🚀 Inicio Rápido

### 1. Crear el entorno conda

```bash
# Opción A: Desde el archivo environment.yml (recomendado)
conda env create -f environment.yml

# Opción B: Crear manualmente
conda create -n delia python=3.11 -y
conda activate delia
pip install -r scripts/requirements.txt
```

### 2. Activar el entorno

```bash
# Método 1: Script de activación (recomendado)
source scripts/activar_entorno.sh

# Método 2: Comando conda directo
conda activate delia
```

### 3. Verificar instalación

```bash
python --version  # Debería mostrar Python 3.11.x
pip list | grep supabase  # Debería mostrar supabase instalado
```

## 📋 Comandos Útiles

### Activar/Desactivar

```bash
# Activar entorno
conda activate delia

# Desactivar entorno
conda deactivate

# Listar entornos disponibles
conda env list
```

### Gestionar Dependencias

```bash
# Instalar nueva dependencia
conda activate delia
pip install nombre-paquete

# Actualizar requirements.txt después de instalar
pip freeze > scripts/requirements.txt

# Recrear environment.yml
conda env export > environment.yml
```

### Recrear el Entorno

Si necesitas recrear el entorno desde cero:

```bash
# Eliminar entorno existente
conda env remove -n delia

# Recrear desde environment.yml
conda env create -f environment.yml

# O desde requirements.txt
conda create -n delia python=3.11 -y
conda activate delia
pip install -r scripts/requirements.txt
```

## 🔧 Scripts Disponibles

Todos los scripts de Python del proyecto deben ejecutarse con el entorno `delia` activado:

```bash
# Activar entorno primero
conda activate delia

# Ejecutar scripts
python scripts/corregir_fuente_fuentesxi.py --dry-run
python scripts/sync_to_supabase.py --file datos_obras.json
python scripts/diagnosticar_carga_datos.py --url https://comediacortesana.github.io/comedia_cortesana/
```

## 📦 Dependencias Principales

- **supabase**: Cliente para interactuar con Supabase
- **selenium**: Para pruebas automatizadas y scraping
- **webdriver-manager**: Gestión automática de ChromeDriver
- **google-api-python-client**: API de Google Sheets
- **python-dotenv**: Manejo de variables de entorno
- **pydantic**: Validación de datos
- **jsonschema**: Validación de esquemas JSON

Ver `scripts/requirements.txt` para la lista completa.

## 🐛 Solución de Problemas

### Error: "Conda no está instalado"

Instala Conda desde:
- **Miniconda**: https://docs.conda.io/en/latest/miniconda.html
- **Anaconda**: https://www.anaconda.com/products/distribution

### Error: "Environment not found"

```bash
# Crear el entorno desde environment.yml
conda env create -f environment.yml
```

### Error: "ModuleNotFoundError"

```bash
# Asegúrate de que el entorno está activado
conda activate delia

# Reinstalar dependencias
pip install -r scripts/requirements.txt
```

### Error: "Command not found: conda"

```bash
# Inicializar conda en tu shell
eval "$(conda shell.bash hook)"  # Para bash
eval "$(conda shell.zsh hook)"   # Para zsh
```

## 💡 Mejores Prácticas

1. **Siempre activa el entorno** antes de ejecutar scripts
2. **No instales paquetes globalmente** - usa el entorno conda
3. **Actualiza environment.yml** cuando agregues nuevas dependencias
4. **Usa versiones específicas** en producción para reproducibilidad

## 🔄 Migración desde venv

Si estabas usando un entorno virtual (`venv`), puedes migrar:

```bash
# Desactivar venv si está activo
deactivate

# Crear entorno conda
conda env create -f environment.yml

# Activar conda
conda activate delia

# Eliminar venv antiguo (opcional)
rm -rf venv_diagnostico
```


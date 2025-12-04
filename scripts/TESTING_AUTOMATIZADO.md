# 🧪 Testing Automatizado - Guía de Uso

## 📋 Descripción

Script de testing automatizado que verifica que los cambios de admin persisten después de recargar la página. Usa Selenium para simular un navegador real y ejecutar las pruebas.

## 🚀 Instalación

### 1. Instalar dependencias de Python

```bash
pip install selenium webdriver-manager
```

### 2. Instalar ChromeDriver

**macOS:**
```bash
brew install chromedriver
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install chromium-chromedriver
```

**Windows:**
Descargar desde: https://chromedriver.chromium.org/

### 3. Verificar instalación

```bash
chromedriver --version
```

## 📝 Uso Básico

### Ejecutar tests con magic link (recomendado)

```bash
python scripts/test_edicion_persistencia.py \
  --url http://localhost:8000 \
  --email tu-email@example.com
```

El script abrirá Chrome, enviará el magic link, y esperará a que confirmes el login manualmente.

### Ejecutar tests con contraseña

```bash
python scripts/test_edicion_persistencia.py \
  --url http://localhost:8000 \
  --email tu-email@example.com \
  --password tu-contraseña
```

### Ejecutar en modo headless (sin ventana del navegador)

```bash
python scripts/test_edicion_persistencia.py \
  --url http://localhost:8000 \
  --email tu-email@example.com \
  --headless
```

### Especificar archivo de salida para el reporte

```bash
python scripts/test_edicion_persistencia.py \
  --url http://localhost:8000 \
  --email tu-email@example.com \
  --output mi_reporte.json
```

## 🧪 Tests que se Ejecutan

1. **Cargar página inicial** - Verifica que la página carga correctamente
2. **Login** - Hace login como admin
3. **Verificar rol admin** - Confirma que el usuario tiene rol de admin
4. **Activar modo edición** - Activa el modo de edición
5. **Editar campo** - Edita el campo "titulo" de la primera obra
6. **Recargar página** - Recarga la página
7. **Verificar persistencia** - Verifica que el cambio persiste después de recargar

## 📊 Reporte de Resultados

El script genera un archivo JSON con los resultados de todos los tests:

```json
{
  "fecha": "2025-01-XX...",
  "url": "http://localhost:8000",
  "email": "admin@example.com",
  "total_tests": 7,
  "tests_exitosos": 6,
  "tests_fallidos": 1,
  "resultados": [
    {
      "test": "Cargar página",
      "success": true,
      "message": "Página cargada correctamente",
      "timestamp": "...",
      "details": {}
    },
    ...
  ]
}
```

## 🔍 Debugging

### Ver qué está pasando en el navegador

No uses `--headless` para ver el navegador en acción:

```bash
python scripts/test_edicion_persistencia.py \
  --url http://localhost:8000 \
  --email tu-email@example.com
```

### Ver logs detallados

El script imprime información detallada de cada paso. Si un test falla, revisa:
- El mensaje de error en la consola
- El archivo de reporte JSON para más detalles
- La captura de pantalla (si está habilitada)

## 🐛 Troubleshooting

### Error: "ChromeDriver not found"

**Solución:** Instala ChromeDriver:
```bash
brew install chromedriver  # macOS
```

### Error: "Chrome version mismatch"

**Solución:** Actualiza ChromeDriver:
```bash
brew upgrade chromedriver  # macOS
```

### Error: "Element not found"

**Solución:** 
- Verifica que la URL es correcta
- Asegúrate de que la aplicación está corriendo
- Revisa que los IDs de elementos en `index.html` coinciden con los del script

### El test falla en "Verificar persistencia"

**Posibles causas:**
1. El cambio no se está guardando en Supabase
2. La función `cargarDatos()` no está cargando desde Supabase
3. Hay un error en la lógica de actualización

**Debug:**
1. Revisa la consola del navegador durante el test
2. Verifica en Supabase directamente que el cambio se guardó
3. Revisa los logs del script para ver qué valor se buscó

## 🔄 Integración con CI/CD

Puedes integrar este script en tu pipeline de CI/CD:

```yaml
# Ejemplo para GitHub Actions
- name: Run persistence tests
  run: |
    pip install selenium webdriver-manager
    python scripts/test_edicion_persistencia.py \
      --url ${{ secrets.APP_URL }} \
      --email ${{ secrets.ADMIN_EMAIL }} \
      --headless
```

## 📝 Personalización

Para modificar qué campo se edita o qué obra se usa, edita la función `test_editar_campo()` en el script.

## 🎯 Próximos Pasos

- [ ] Agregar capturas de pantalla automáticas cuando falla un test
- [ ] Agregar más tests (editar múltiples campos, campos anidados, etc.)
- [ ] Agregar tests para editores (verificar que necesitan aprobación)
- [ ] Agregar tests de rendimiento


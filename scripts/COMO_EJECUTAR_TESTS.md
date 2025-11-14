# 🧪 Cómo Ejecutar los Tests de Persistencia

## 🚀 Método Rápido (Recomendado)

### Opción 1: Usar el script helper (más fácil)

```bash
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/comedia_cortesana
./scripts/ejecutar_tests.sh
```

El script:
- ✅ Detecta automáticamente si hay un servidor local o usa GitHub Pages
- ✅ Te pregunta el email del admin
- ✅ Inicia un servidor local si es necesario
- ✅ Ejecuta los tests
- ✅ Genera un reporte

### Opción 2: Ejecutar directamente con Python

#### Si la app está en GitHub Pages (producción):

```bash
python scripts/test_edicion_persistencia.py \
  --url https://comediacortesana.github.io/comedia_cortesana/ \
  --email tu-email-admin@example.com
```

#### Si quieres probar localmente:

1. **Iniciar servidor local:**
```bash
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/comedia_cortesana
python -m http.server 8000
```

2. **En otra terminal, ejecutar tests:**
```bash
python scripts/test_edicion_persistencia.py \
  --url http://localhost:8000 \
  --email tu-email-admin@example.com
```

## 📋 Requisitos Previos

1. **Instalar dependencias:**
```bash
pip install selenium webdriver-manager
```

2. **Tener Chrome instalado** (ChromeDriver se descarga automáticamente)

3. **Tener un usuario admin en Supabase** con el email que usarás

## 🔍 Qué Hace el Test

1. Abre Chrome y carga la aplicación
2. Hace login como admin (magic link o contraseña)
3. Activa el modo edición
4. Edita el campo "titulo" de la primera obra
5. Recarga la página
6. Verifica que el cambio persiste
7. Genera un reporte JSON con los resultados

## 📊 Ver Resultados

Después de ejecutar, revisa:

1. **Consola:** Verás los resultados en tiempo real
2. **Reporte JSON:** `test_report.json` con detalles completos

```json
{
  "fecha": "2025-01-XX...",
  "url": "...",
  "email": "...",
  "total_tests": 7,
  "tests_exitosos": 6,
  "tests_fallidos": 1,
  "resultados": [...]
}
```

## 🐛 Troubleshooting

### Error: "ERR_CONNECTION_REFUSED"

**Causa:** No hay servidor corriendo en esa URL

**Solución:**
- Si quieres probar localmente: `python -m http.server 8000`
- Si quieres usar producción: Usa la URL de GitHub Pages

### Error: "ChromeDriver not found"

**Solución:** El webdriver-manager lo descarga automáticamente. Si falla:
```bash
brew install chromedriver  # macOS
```

### El test falla en "Verificar persistencia"

**Posibles causas:**
1. El cambio no se guardó en Supabase
2. La función `cargarDatos()` no está cargando desde Supabase
3. Hay un error en la lógica de actualización

**Debug:**
1. Revisa la consola del navegador durante el test
2. Verifica en Supabase directamente que el cambio se guardó
3. Revisa `test_report.json` para ver qué valor se buscó

## 💡 Tips

- **Modo headless:** Agrega `--headless` para ejecutar sin ventana del navegador
- **Ver el navegador:** No uses `--headless` para ver qué está pasando
- **Reporte personalizado:** Usa `--output mi_reporte.json` para cambiar el nombre del reporte

## 📝 Ejemplo Completo

```bash
# 1. Ir al directorio del proyecto
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/comedia_cortesana

# 2. Ejecutar tests contra GitHub Pages
python scripts/test_edicion_persistencia.py \
  --url https://comediacortesana.github.io/comedia_cortesana/ \
  --email admin@example.com \
  --output test_persistencia_$(date +%Y%m%d_%H%M%S).json

# 3. Revisar resultados
cat test_report.json | python -m json.tool
```

## 🎯 Próximos Pasos

Si los tests fallan:
1. Comparte el archivo `test_report.json` generado
2. Revisaré los errores específicos
3. Corregiré el código según los resultados


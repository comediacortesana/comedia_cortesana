# 🎭 Sistema Completo de Filtrado con Feedback - Teatro Español

## 🎯 Respuesta a tus preguntas:

### ✅ SÍ, GitHub Pages puede leer JSON del repositorio
- El HTML carga datos desde `datos_obras.json` automáticamente
- Sin necesidad de backend o servidor
- Completamente gratis en GitHub Pages

### ✅ Sistema inteligente de feedback
- Los investigadores filtran datos
- Exportan su búsqueda + comentario
- Tú replicas exactamente lo que buscaron
- Implementas mejoras basadas en feedback real

---

## 📦 Archivos Creados

```
filtro_basico/
├── index.html                          # Versión básica sin comentarios
├── index_con_comentarios.html          # ⭐ Versión con sistema de feedback
├── datos_obras.json                    # 15 obras de ejemplo
├── README.md                           # Documentación de campos
├── README_COMPLETO.md                  # Este archivo
├── SISTEMA_FEEDBACK.md                 # Explicación detallada del sistema
├── INSTRUCCIONES_PUBLICACION.md        # Cómo publicar (Gist, CodePen, etc.)
├── GITHUB_PAGES_TUTORIAL.md            # Tutorial GitHub Pages (GRATIS)
└── CONFIGURAR_DOMINIO_PERSONALIZADO.md # Para dominio custom (opcional)

scripts/
└── export_to_json_for_github.py        # Script para exportar desde Django
```

---

## 🚀 Uso Rápido

### 1. Publicar en GitHub Pages (2 minutos)

```bash
# En tu repositorio GitHub
cd filtro_basico
git add .
git commit -m "Add sistema de filtrado con feedback"
git push

# Activar GitHub Pages
# Settings → Pages → Source: main branch → Save

# URL: https://thygolem.github.io/comedia_cortesana/index_con_comentarios.html
```

### 2. Actualizar datos desde Django

```bash
# Exportar datos reales desde tu BD Django
python scripts/export_to_json_for_github.py

# Subir actualización
git add filtro_basico/datos_obras.json
git commit -m "Actualizar datos con obras reales"
git push

# ¡En 1-2 minutos está en vivo!
```

---

## 🎓 Cómo Funciona el Sistema de Feedback

### Para Investigadores:

```
1. Abren: https://thygolem.github.io/comedia_cortesana/index_con_comentarios.html
2. Aplican filtros (ej: Autor="Lope", Tipo="comedia", Fecha=1610-1625)
3. Ven resultados filtrados
4. Escriben comentario: "Me gustaría ver también información sobre actores"
5. Click en "Descargar Búsqueda + Comentario"
6. Se descarga archivo JSON o TXT con:
   ✅ Sus filtros exactos
   ✅ Los resultados que obtuvieron
   ✅ Su comentario
   ✅ Fecha y estadísticas
```

### Para Ti (Desarrollador):

```
1. Recibes archivo del investigador (por email, Drive, etc.)
2. Abres el JSON/TXT
3. Ves exactamente:
   - Qué filtros aplicó
   - Qué resultados obtuvo
   - Qué mejora solicita
4. Replicas la búsqueda en Django:
   
   Obra.objects.filter(
       autor__nombre__icontains='Lope',
       tipo_obra='comedia',
       fecha_creacion_estimada__gte='1610',
       fecha_creacion_estimada__lte='1625'
   )
   
5. Implementas la mejora:
   - Añadir campo al JSON
   - Añadir filtro al HTML
   - Entrenar IA para extraer ese dato de PDFs
   
6. Push → GitHub Pages actualiza automáticamente
```

---

## 📊 Ejemplo Real de Feedback

### Archivo que recibes del investigador:

**feedback_teatro_1730300000.json**
```json
{
  "metadata": {
    "fecha_exportacion": "2025-10-30T15:30:00.000Z",
    "total_obras_base_datos": 15
  },
  "filtros_aplicados": {
    "autor": "Lope de Vega",
    "tipo_obra": "comedia"
  },
  "estadisticas_busqueda": {
    "total_resultados": 4,
    "porcentaje_del_total": "26.67%"
  },
  "resultados_obtenidos": [
    {
      "id": 2,
      "titulo": "El perro del hortelano",
      "autor": "Lope de Vega",
      "tipo_obra": "comedia",
      "fuente": "CATCOM"
    }
  ],
  "comentario_investigador": "Todas las comedias de Lope tienen mecenas nobles. Sería útil filtrar por tipo de mecenas (real, ducal, eclesiástico)"
}
```

### Tu respuesta:

1. **Entiendes la necesidad**: Quieren categorizar mecenas
2. **Actualizas el JSON**:
   ```json
   {
     "mecenas": "Duque de Osuna",
     "tipo_mecenas": "ducal"  // ← NUEVO CAMPO
   }
   ```
3. **Añades filtro al HTML**:
   ```html
   <select id="tipo_mecenas">
     <option value="">Todos</option>
     <option value="real">Real</option>
     <option value="ducal">Ducal</option>
     <option value="eclesiastico">Eclesiástico</option>
   </select>
   ```
4. **Push y notificas al investigador**

---

## 🎨 Dos Versiones del HTML

### Versión 1: `index.html` (Básica)
- Filtros funcionando
- Carga desde JSON
- Sin sistema de comentarios
- **Uso**: Demo simple o prototipo

### Versión 2: `index_con_comentarios.html` (Completa) ⭐
- Todo lo de la versión 1
- Sistema de feedback con comentarios
- Exportación de búsquedas (JSON y TXT)
- Muestra filtros activos visualmente
- **Uso**: Producción con investigadores reales

---

## 💰 Costos

| Componente | Costo |
|------------|-------|
| GitHub Pages | 🆓 $0/mes (Gratis para siempre) |
| Dominio .es (opcional) | 💰 ~€10/año |
| Hosting backend | 🆓 $0 (no necesario, todo estático) |
| SSL Certificate | 🆓 $0 (incluido en GitHub Pages) |
| **TOTAL** | **🆓 $0** |

---

## 🔄 Workflow de Actualización

```bash
# 1. Exportar datos desde Django
python scripts/export_to_json_for_github.py

# Output:
# ✅ Exportación completada!
# 📁 Archivo guardado en: filtro_basico/datos_obras.json
# 📦 Tamaño: 15.47 KB

# 2. Revisar cambios
git diff filtro_basico/datos_obras.json

# 3. Commit y push
git add filtro_basico/datos_obras.json
git commit -m "Actualizar datos con 50 nuevas obras"
git push

# 4. Esperar 1-2 minutos
# GitHub Pages actualiza automáticamente

# 5. Verificar
# https://thygolem.github.io/comedia_cortesana/index_con_comentarios.html
```

---

## 🎯 Casos de Uso

### 1. Demo para reunión
**Situación**: Presentas el proyecto a investigadores  
**Usa**: `index_con_comentarios.html`  
**URL**: Compartes el link de GitHub Pages  
**Resultado**: Pueden probarlo en vivo desde cualquier dispositivo

### 2. Recoger feedback
**Situación**: Investigadores usan el sistema  
**Usa**: Sistema de exportación integrado  
**Reciben**: Archivo JSON/TXT con su búsqueda  
**Resultado**: Tú sabes qué mejoras implementar

### 3. Validar datos
**Situación**: Verificar calidad de extracción de PDFs  
**Usa**: Filtros + exportación  
**Investigador**: "La fecha de esta obra está mal"  
**Resultado**: Corriges en la BD y re-exportas

### 4. Descubrir patrones
**Situación**: Investigador encuentra algo interesante  
**Usa**: Comentarios en exportación  
**Ejemplo**: "Todas las obras de este autor tienen mecenas real"  
**Resultado**: Entrenas IA para buscar más patrones así

---

## 🔧 Personalización

### Cambiar colores
```css
/* En el <style> del HTML */
.btn-primary {
    background-color: #tu-color;
}
```

### Añadir campo al filtro
```html
<!-- En .filters-grid -->
<div class="filter-group">
    <label for="tu-campo">Tu Campo</label>
    <input type="text" id="tu-campo">
</div>
```

```javascript
// En aplicarFiltros()
const tuCampo = document.getElementById('tu-campo').value;
if (tuCampo && !obra.tu_campo.includes(tuCampo)) return false;
```

### Añadir columna a resultados
```javascript
// En mostrarResultados()
html += '<th>Tu Columna</th>';  // En thead

html += `<td>${obra.tu_campo}</td>`;  // En tbody
```

---

## 📊 Analytics (Opcional)

### Ver qué buscan los investigadores

Puedes añadir Google Analytics gratis:

```html
<!-- Antes de </head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=TU-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'TU-ID');
</script>
```

Verás:
- Cuántas visitas
- Qué páginas más visitadas
- Desde qué países
- Dispositivos (móvil/desktop)

---

## 🚨 Limitaciones y Soluciones

### Limitación 1: Archivo JSON muy grande

**Problema**: Si tienes 10,000 obras, el JSON pesa mucho  
**Solución**:
```python
# Exportar solo primeras 500
export_to_json_for_github.py --max-obras 500

# O implementar paginación
# O usar API Django para datos grandes
```

### Limitación 2: Sin autenticación

**Problema**: Todos ven los mismos datos  
**Solución**:
```
Opción A: GitHub Pages es público → OK para datos académicos
Opción B: Si necesitas login → usar Django con API
```

### Limitación 3: Comentarios no se guardan automáticamente

**Problema**: Investigadores deben enviar archivo manualmente  
**Solución Futura**:
```javascript
// Enviar a API de Django
fetch('https://tu-api.com/feedback', {
    method: 'POST',
    body: JSON.stringify(exportData)
})
```

---

## 🎓 Próximos Pasos Sugeridos

### Fase 1: MVP (Ya está listo!) ✅
- [x] HTML con filtros
- [x] Carga desde JSON
- [x] Sistema de feedback
- [x] Exportación de búsquedas

### Fase 2: Datos Reales (Ahora)
```bash
python scripts/export_to_json_for_github.py
git push
```

### Fase 3: Publicar y Compartir
```bash
# Activar GitHub Pages
# Compartir URL con investigadores
# Esperar feedback
```

### Fase 4: Iterar
```
Recibir feedback → Implementar mejoras → Actualizar → Repetir
```

### Fase 5: Escalar (Opcional, futuro)
- API Django para datos dinámicos
- Login para guardar búsquedas favoritas
- Dashboard de analytics
- Integración con IA para análisis

---

## 📞 Soporte

### Documentación incluida:
- `README.md` - Campos disponibles
- `SISTEMA_FEEDBACK.md` - Cómo funciona el feedback
- `GITHUB_PAGES_TUTORIAL.md` - Publicar gratis
- `INSTRUCCIONES_PUBLICACION.md` - Alternativas (Gist, CodePen, etc.)

### Scripts útiles:
- `export_to_json_for_github.py` - Exportar desde Django

---

## ✅ Checklist de Lanzamiento

- [ ] Datos exportados desde Django (`python scripts/export_to_json_for_github.py`)
- [ ] Archivos subidos a GitHub (`git push`)
- [ ] GitHub Pages activado (Settings → Pages)
- [ ] URL funciona (`https://thygolem.github.io/comedia_cortesana/`)
- [ ] Probado en móvil y desktop
- [ ] Compartido con al menos un investigador
- [ ] Recibido primer feedback
- [ ] Implementada primera mejora

---

## 🎉 ¡Todo Listo!

Tienes un sistema completo:
- ✅ Frontend bonito y funcional
- ✅ Datos desde JSON (actualizable fácilmente)
- ✅ Sistema de feedback inteligente
- ✅ 100% gratis en GitHub Pages
- ✅ Fácil de mantener y actualizar

**Tu URL:** `https://thygolem.github.io/comedia_cortesana/index_con_comentarios.html`

**Siguiente acción:**
```bash
python scripts/export_to_json_for_github.py
git add filtro_basico/datos_obras.json
git commit -m "Add datos reales del teatro español"
git push
```

¡Los investigadores tendrán una herramienta potente y tú tendrás feedback valioso! 🎭


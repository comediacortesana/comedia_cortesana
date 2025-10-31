# 💬 Sistema de Feedback para Investigadores

## 🎯 Concepto

Sistema inteligente que permite a los investigadores:
1. **Filtrar** datos del teatro español
2. **Comentar** sobre lo que encuentran o necesitan
3. **Exportar** su búsqueda exacta + comentario
4. **Tú replicas** exactamente lo que buscaron
5. **Mejoras** el sistema basándote en feedback real

---

## ✅ Respuesta a tu pregunta: SÍ, GitHub Pages puede leer JSON del repositorio

### Cómo funciona:

```
Repositorio GitHub:
├── index_con_comentarios.html  (interfaz web)
├── datos_obras.json            (datos que se cargan)
└── README.md

Cuando el usuario abre la página:
1. HTML se carga desde GitHub Pages
2. JavaScript hace fetch('datos_obras.json')
3. Carga los datos automáticamente
4. ¡Funciona sin backend!
```

### Ventajas:
- ✅ **Sin servidor necesario** - todo estático
- ✅ **Gratis en GitHub Pages**
- ✅ **Actualizas el JSON** → se actualiza el sitio
- ✅ **Rápido** - no hay base de datos

---

## 📦 Archivos Creados

### 1. `datos_obras.json`
- **15 obras de ejemplo** con datos reales
- Campos completos: título, autor, tipo, fuente, lugar, fecha, etc.
- **Estructura extensible**: puedes añadir más campos fácilmente

### 2. `index_con_comentarios.html`
- **Versión mejorada** con sistema de feedback
- **Carga datos desde JSON** automáticamente
- **Sistema de exportación** de búsquedas + comentarios

---

## 🚀 Funcionalidades del Sistema de Feedback

### Para los Investigadores:

1. **Aplican filtros** (autor, tipo, fecha, lugar, etc.)
2. **Ven resultados** filtrados
3. **Escriben comentario**:
   - "Me gustaría ver también información sobre actores"
   - "Encontré un patrón: obras de Lope en Toledo son de 1610-1620"
   - "Sería útil tener estadísticas automáticas por época"
   - "Falta el campo 'música' en los filtros"
4. **Descargan archivo** con:
   - Sus filtros exactos
   - Los resultados que obtuvieron
   - Su comentario

### Para Ti (Desarrollador):

1. **Recibes el archivo** del investigador
2. **Abres el JSON o TXT** y ves:
   - Exactamente qué buscaron
   - Qué resultados obtuvieron
   - Qué mejora solicitan
3. **Replicas la búsqueda** fácilmente
4. **Implementas mejoras** basadas en uso real

---

## 📄 Ejemplo de Archivo Exportado (JSON)

```json
{
  "metadata": {
    "fecha_exportacion": "2025-10-30T15:30:00.000Z",
    "fecha_legible": "30/10/2025, 16:30:00",
    "version_sistema": "1.0",
    "total_obras_base_datos": 15
  },
  "filtros_aplicados": {
    "autor": "Lope de Vega",
    "tipo_obra": "comedia",
    "fecha_desde": "1610",
    "fecha_hasta": "1625"
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
      "fuente": "CATCOM",
      "fecha_creacion": "1618",
      "lugar": "Toledo",
      "region": "Castilla-La Mancha"
    }
  ],
  "comentario_investigador": "He notado que todas las comedias de Lope en este periodo tienen un patrón similar de mecenazgo. Sería útil añadir un campo para 'relación con la nobleza' y poder filtrar por tipo de mecenas (real, ducal, eclesiástico)."
}
```

---

## 📝 Ejemplo de Archivo Exportado (Texto)

```
================================================================================
FEEDBACK DE INVESTIGADOR - TEATRO ESPAÑOL DEL SIGLO DE ORO
================================================================================

Fecha: 30/10/2025, 16:30:00
Total de obras en sistema: 15
Resultados encontrados: 4

--------------------------------------------------------------------------------
FILTROS APLICADOS
--------------------------------------------------------------------------------
  • autor: Lope de Vega
  • tipo_obra: comedia
  • fecha_desde: 1610
  • fecha_hasta: 1625

--------------------------------------------------------------------------------
RESULTADOS OBTENIDOS (4 obras)
--------------------------------------------------------------------------------

1. El perro del hortelano
   Autor: Lope de Vega
   Tipo: comedia | Fuente: CATCOM
   Lugar: Toledo, Castilla-La Mancha
   Fecha: 1618

2. Fuenteovejuna
   Autor: Lope de Vega
   Tipo: comedia | Fuente: CATCOM
   Lugar: Madrid, Madrid
   Fecha: 1612

[...]

================================================================================
COMENTARIO DEL INVESTIGADOR
================================================================================

He notado que todas las comedias de Lope en este periodo tienen un patrón 
similar de mecenazgo. Sería útil añadir un campo para 'relación con la nobleza' 
y poder filtrar por tipo de mecenas (real, ducal, eclesiástico).

================================================================================
```

---

## 🔄 Workflow Completo

### Fase 1: Investigador usa el sistema

```
Investigador → Aplica filtros → Ve resultados → Escribe comentario → Descarga archivo
```

### Fase 2: Tú recibes feedback

```
Email/Drive con archivo → Abres JSON/TXT → Lees comentario → Entiendes necesidad
```

### Fase 3: Replicas búsqueda

```python
# En Django shell o script
filtros = {
    'autor__nombre__icontains': 'Lope de Vega',
    'tipo_obra': 'comedia',
    'fecha_creacion_estimada__gte': '1610',
    'fecha_creacion_estimada__lte': '1625'
}
obras = Obra.objects.filter(**filtros)
# Ves exactamente lo mismo que el investigador
```

### Fase 4: Implementas mejora

#### Opción A: Añadir al JSON
```json
{
  "id": 2,
  "titulo": "El perro del hortelano",
  "autor": "Lope de Vega",
  "tipo_mecenas": "ducal",  // ← NUEVO CAMPO
  "mecenas": "Duque de Osuna",
  "relacion_nobleza": "directa"  // ← NUEVO CAMPO
}
```

#### Opción B: Entrenar IA para extraer
```python
# Con el feedback sabes qué datos buscar en los PDFs
prompt = """
Extrae del texto:
- Tipo de mecenas (real, ducal, eclesiástico, municipal)
- Relación con la nobleza (directa, indirecta, ninguna)
Basándome en el feedback del investigador que notó este patrón.
"""
```

#### Opción C: Añadir filtro al HTML
```html
<div class="filter-group">
    <label for="tipo_mecenas">Tipo de Mecenas</label>
    <select id="tipo_mecenas">
        <option value="">Todos</option>
        <option value="real">Real</option>
        <option value="ducal">Ducal</option>
        <option value="eclesiastico">Eclesiástico</option>
    </select>
</div>
```

### Fase 5: Actualizas y notificas

```
Git push → GitHub Pages actualiza → Investigador ve mejora → Ciclo de feedback continúa
```

---

## 🎓 Casos de Uso Reales

### Caso 1: Solicitud de nuevo campo

**Comentario:**
> "Necesito saber qué obras tienen música conservada para mi investigación sobre zarzuelas del s.XVII"

**Tu acción:**
1. Añades campo `musica_conservada: true/false` al JSON
2. Añades filtro checkbox "Solo obras con música"
3. Actualizas GitHub Pages

### Caso 2: Patrón descubierto

**Comentario:**
> "Todas las tragedias de Calderón tienen mecenazgo real. ¿Podríamos ver estadísticas por género y mecenazgo?"

**Tu acción:**
1. Creas script que genera estadísticas desde el JSON
2. Añades sección de "Estadísticas" al HTML
3. O entrenas IA para buscar más patrones similares en PDFs

### Caso 3: Mejora de datos

**Comentario:**
> "La fecha de 'El perro del hortelano' debería ser 1613, no 1618 según mis fuentes"

**Tu acción:**
1. Verificas la corrección
2. Actualizas el JSON
3. Git push → cambio en vivo inmediatamente

### Caso 4: Feature request específico

**Comentario:**
> "Sería útil exportar los resultados como CSV para importar a Excel y hacer análisis cuantitativo"

**Tu acción:**
```javascript
// Añades botón en el HTML
function exportarCSV() {
    let csv = 'Título,Autor,Tipo,Fuente,Fecha,Lugar\n';
    datosFiltrados.forEach(obra => {
        csv += `"${obra.titulo}","${obra.autor}","${obra.tipo_obra}",`;
        csv += `"${obra.fuente}","${obra.fecha_creacion}","${obra.lugar}"\n`;
    });
    // Descargar CSV...
}
```

---

## 💡 Ideas Avanzadas

### 1. Sistema de "Issues" simulado

Los investigadores pueden categorizar su feedback:

```javascript
<select id="tipo-feedback">
    <option value="bug">🐛 Error en los datos</option>
    <option value="feature">✨ Nueva funcionalidad</option>
    <option value="mejora">🔧 Mejora sugerida</option>
    <option value="patron">📊 Patrón descubierto</option>
</select>
```

### 2. Versionado de búsquedas

```json
{
  "id_busqueda": "busqueda_123",
  "version": "v1.0",
  "reproducible": true,
  "puede_replicarse_en_django": true
}
```

### 3. Integración con IA

```python
# Script que procesa feedback automáticamente
feedbacks = cargar_todos_los_json('feedback/*.json')
for feedback in feedbacks:
    if 'añadir campo' in feedback['comentario'].lower():
        sugerir_modificacion_modelo(feedback)
    elif 'patrón' in feedback['comentario'].lower():
        analizar_patron_con_ia(feedback)
```

### 4. Dashboard de feedback

Creas otra página HTML que lee todos los JSON exportados:

```
feedback_dashboard.html
├── Lee todos los feedback/*.json
├── Muestra estadísticas de solicitudes
├── Agrupa por tipo (bugs, features, etc.)
└── Prioriza mejoras más solicitadas
```

---

## 🔧 Actualizar Datos (tu workflow)

### Desde Django:

```python
# Script: export_to_json.py
from apps.obras.models import Obra
import json

obras = Obra.objects.select_related('autor').all()[:50]

data = {
    "metadata": {
        "version": "1.0",
        "fecha_actualizacion": datetime.now().isoformat(),
        "total_obras": obras.count()
    },
    "obras": []
}

for obra in obras:
    data["obras"].append({
        "id": obra.id,
        "titulo": obra.titulo_limpio,
        "autor": obra.autor.nombre if obra.autor else "",
        "tipo_obra": obra.tipo_obra,
        "fuente": obra.fuente_principal,
        # ... más campos
    })

with open('filtro_basico/datos_obras.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### Actualizar GitHub Pages:

```bash
cd filtro_basico
git add datos_obras.json
git commit -m "Actualizar datos con 50 nuevas obras"
git push

# ¡En 1-2 minutos está en vivo en GitHub Pages!
```

---

## 📊 Métricas que puedes obtener

Con este sistema puedes rastrear:

1. **Filtros más usados** → qué campos son importantes
2. **Combinaciones de filtros** → cómo buscan los investigadores
3. **Campos faltantes** → qué datos necesitan extraer
4. **Patrones descubiertos** → insights para IA
5. **Errores en datos** → correcciones necesarias

---

## 🎯 Siguiente Nivel: Sistema Híbrido

### Versión Básica (actual):
- HTML estático en GitHub Pages
- JSON con datos
- Exportación de comentarios

### Versión Avanzada (futuro):
```
GitHub Pages (frontend) → API Django (backend) → Base de datos
                ↓
        Formulario de feedback → Email automático a ti
                                 ↓
                         Guarda en BD para analytics
```

Pero **empiezas simple** (lo que te creé) y creces según necesidad.

---

## ✅ Resumen

| Pregunta | Respuesta |
|----------|-----------|
| ¿GitHub Pages lee JSON del repo? | ✅ Sí, perfectamente |
| ¿Es gratis? | ✅ Totalmente |
| ¿Puede exportar búsquedas? | ✅ Sí, como JSON o TXT |
| ¿Puedes replicar búsquedas? | ✅ Sí, tienes todos los filtros |
| ¿Ayuda a mejorar el sistema? | ✅ Feedback directo de usuarios reales |

---

## 🚀 Para Publicar

```bash
# 1. Sube archivos al repositorio
git add datos_obras.json index_con_comentarios.html
git commit -m "Add sistema de feedback para investigadores"
git push

# 2. GitHub Pages sirve todo automáticamente
# URL: https://thygolem.github.io/comedia_cortesana/index_con_comentarios.html

# 3. Puedes renombrar index_con_comentarios.html → index.html
# Para que sea la página principal
```

---

## 💬 Feedback que esperarías recibir

```
"Excelente herramienta! Encontré todas las tragedias de Calderón 
patrocinadas por Felipe IV. Me gustaría que el sistema mostrara 
automáticamente el promedio de años entre obras del mismo autor y mecenas."

→ Sabes exactamente qué implementar next!
```

¡Este sistema convierte a tus investigadores en **beta testers activos** y 
generadores de **requisitos basados en uso real**! 🎭



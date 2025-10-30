# Filtro Básico - Teatro Español del Siglo de Oro

Este directorio contiene un `index.html` básico y funcional para filtrar los datos del proyecto DELIA_DJANGO.

## 📋 Campos Disponibles para Filtrado

### **OBRA** (`apps/obras/models.py`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `titulo` | CharField | Título original de la obra |
| `titulo_limpio` | CharField | Título normalizado (único) |
| `titulo_alternativo` | CharField | Títulos alternativos o variaciones |
| `tipo_obra` | Choice | comedia, auto, zarzuela, entremés, tragedia, loa, sainete, baile, otro |
| `genero` | CharField | Género específico |
| `subgenero` | CharField | Subgénero o clasificación más específica |
| `fuente_principal` | Choice | FUENTESXI, CATCOM, AMBAS |
| `origen_datos` | Choice | web, pdf, manual |
| `tema` | CharField | Tema principal de la obra |
| `fecha_creacion_estimada` | CharField | Fecha estimada de creación |
| `idioma` | CharField | Idioma de la obra (default: español) |
| `versos` | Integer | Número de versos |
| `actos` | Integer | Número de actos |
| `musica_conservada` | Boolean | Si se conserva música de la obra |
| `compositor` | CharField | Compositor de la música |
| `mecenas` | CharField | Mecenas o patrocinador |
| `autor` | ForeignKey | Relación con modelo Autor |

### **AUTOR** (`apps/autores/models.py`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `nombre` | CharField | Nombre del autor |
| `nombre_completo` | CharField | Nombre completo del autor |
| `fecha_nacimiento` | CharField | Fecha de nacimiento (formato original) |
| `fecha_muerte` | CharField | Fecha de muerte (formato original) |
| `biografia` | TextField | Biografía del autor |
| `obras_principales` | TextField | Lista de obras principales |
| `epoca` | CharField | Época histórica (ej: Siglo de Oro) |

### **LUGAR** (`apps/lugares/models.py`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `nombre` | CharField | Nombre del lugar |
| `coordenadas_lat` | Float | Latitud |
| `coordenadas_lng` | Float | Longitud |
| `region` | CharField | Región o provincia |
| `pais` | CharField | País (default: España) |
| `tipo_lugar` | Choice | palacio, corral, iglesia, plaza, teatro, casa, universidad, convento, otro |
| `poblacion_estimada` | Integer | Población estimada en el siglo XVII |
| `es_capital` | Boolean | Si es capital de región o país |

### **REPRESENTACIÓN** (`apps/representaciones/models.py`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `fecha` | CharField | Fecha original del texto |
| `fecha_formateada` | DateField | Fecha formateada para consultas |
| `compañia` | CharField | Compañía teatral |
| `director_compañia` | CharField | Director de la compañía |
| `tipo_lugar` | Choice | Mismo que Lugar.tipo_lugar |
| `tipo_funcion` | CharField | Tipo de función (fiesta, celebración, etc.) |
| `publico` | CharField | Tipo de público (corte, pueblo, etc.) |
| `entrada` | CharField | Información sobre entrada o precio |
| `duracion` | CharField | Duración de la representación |
| `mecenas` | CharField | Mecenas o patrocinador |
| `es_anterior_1650` | Boolean | Si la representación es anterior a 1650 |
| `es_anterior_1665` | Boolean | Si la representación es anterior a 1665 |
| `personajes_historicos` | TextField | Menciones de personajes históricos |
| `organizadores_fiesta` | TextField | Organizadores de la fiesta |
| `obra` | ForeignKey | Relación con modelo Obra |
| `lugar` | ForeignKey | Relación con modelo Lugar |

## 🔌 Integración con Django API

### Opción 1: Usar el API REST existente

Si tu proyecto Django tiene Django REST Framework configurado, puedes conectar el HTML a la API:

```javascript
// Reemplazar datosEjemplo con llamada a la API
fetch('/api/obras/?format=json')
    .then(response => response.json())
    .then(data => {
        datosOriginales = data.results || data;
        datosFiltrados = [...datosOriginales];
        mostrarResultados();
    });
```

### Opción 2: Crear una vista Django que sirva este HTML

En `apps/obras/views.py`:

```python
from django.shortcuts import render
from django.http import JsonResponse
from .models import Obra

def filtro_basico(request):
    return render(request, 'filtro_basico/index.html')

def api_obras_filtradas(request):
    obras = Obra.objects.select_related('autor').prefetch_related('representaciones__lugar')
    
    # Aplicar filtros según request.GET
    if request.GET.get('titulo'):
        obras = obras.filter(titulo_limpio__icontains=request.GET.get('titulo'))
    
    if request.GET.get('tipo_obra'):
        obras = obras.filter(tipo_obra=request.GET.get('tipo_obra'))
    
    if request.GET.get('fuente'):
        obras = obras.filter(fuente_principal=request.GET.get('fuente'))
    
    # ... más filtros
    
    data = [{
        'id': obra.id,
        'titulo': obra.titulo_limpio,
        'autor': obra.autor.nombre if obra.autor else '',
        'tipo_obra': obra.tipo_obra,
        'fuente': obra.fuente_principal,
        # ... más campos
    } for obra in obras[:100]]  # Limitar a 100 resultados
    
    return JsonResponse(data, safe=False)
```

En `apps/obras/urls.py`:

```python
urlpatterns = [
    path('filtro-basico/', filtro_basico, name='filtro_basico'),
    path('api/obras-filtradas/', api_obras_filtradas, name='api_obras_filtradas'),
]
```

### Opción 3: Cargar datos desde un archivo JSON estático

```bash
# Exportar datos desde Django
python manage.py dumpdata obras.Obra --indent 2 > filtro_basico/obras.json
```

Luego en el HTML:

```javascript
fetch('obras.json')
    .then(response => response.json())
    .then(data => {
        datosOriginales = data;
        datosFiltrados = [...datosOriginales];
        mostrarResultados();
    });
```

## 🎨 Personalización

El archivo HTML es completamente autónomo y puede ser personalizado:

1. **Estilos CSS**: Modificar la sección `<style>` para cambiar colores, fuentes, etc.
2. **Filtros**: Añadir o quitar campos en `.filters-grid`
3. **Tabla de resultados**: Modificar columnas en `mostrarResultados()`
4. **Datos de ejemplo**: Reemplazar `datosEjemplo` con datos reales

## 🚀 Uso

1. **Desarrollo local**: Abrir directamente `index.html` en un navegador
2. **Producción**: Copiar a `static/` o `templates/` según necesites
3. **Con servidor Django**: 
   ```bash
   python manage.py runserver
   # Visitar http://localhost:8000/obras/filtro-basico/
   ```

## 📊 Ejemplo de Estructura de Datos

El JavaScript espera datos en este formato:

```json
[
    {
        "id": 1,
        "titulo": "La vida es sueño",
        "autor": "Calderón de la Barca",
        "tipo_obra": "comedia",
        "fuente": "FUENTESXI",
        "epoca": "Siglo de Oro",
        "lugar": "Madrid",
        "tipo_lugar": "corral",
        "region": "Madrid",
        "compania": "Compañía Real",
        "fecha": "1635",
        "mecenas": "Felipe IV"
    }
]
```

## 🔍 Filtros Implementados

- ✅ Título de la obra (búsqueda parcial)
- ✅ Tipo de obra (select)
- ✅ Fuente de datos (select)
- ✅ Autor (búsqueda parcial)
- ✅ Época (búsqueda parcial)
- ✅ Lugar (búsqueda parcial)
- ✅ Tipo de lugar (select)
- ✅ Región (búsqueda parcial)
- ✅ Compañía teatral (búsqueda parcial)
- ✅ Rango de fechas (desde - hasta)
- ✅ Mecenas (búsqueda parcial)

## 📝 Notas

- El HTML incluye 3 obras de ejemplo para demostración
- Los filtros funcionan de manera acumulativa (AND logic)
- La búsqueda de texto es case-insensitive
- Los filtros de fecha funcionan con años (formato numérico)


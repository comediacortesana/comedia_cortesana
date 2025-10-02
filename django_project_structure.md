# Estructura del Proyecto Django - Teatro Español del Siglo de Oro

## Resumen de Fuentes de Datos

### FUENTESXI (Extracción de PDF)
- **Fuente**: "Comedias en Madrid: 1603-1709" de J.E. Varey y N.D. Shergold
- **Datos**: 477 obras teatrales con 1154 representaciones
- **Estructura**: Base de datos SQLite con tablas `obras`, `representaciones`, `manuscritos`
- **Metadatos**: Lugares geográficos, fechas, compañías teatrales

### CATCOM (Web Scraping)
- **Fuente**: Base de datos CATCOM (catcom.uv.es)
- **Datos**: Obras teatrales con información bibliográfica detallada
- **Estructura**: Archivos JSON por letra del alfabeto
- **Metadatos**: Atribuciones, bibliografía, variaciones de títulos

## Estructura del Proyecto Django

```
teatro_espanol_django/
├── manage.py
├── requirements.txt
├── README.md
├── teatro_espanol/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── __init__.py
│   ├── obras/                    # App principal para obras teatrales
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── serializers.py
│   │   └── migrations/
│   ├── representaciones/         # App para representaciones
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── migrations/
│   ├── lugares/                  # App para lugares geográficos
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── migrations/
│   ├── autores/                  # App para autores/dramaturgos
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── migrations/
│   └── bibliografia/             # App para referencias bibliográficas
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── admin.py
│       └── migrations/
├── data/
│   ├── fuentesxi/               # Datos extraídos del PDF
│   │   ├── teatro_espanol_mejorado.db
│   │   ├── geographic_metadata.json
│   │   ├── lugares_procesados.json
│   │   └── places_hierarchy.json
│   ├── catcom/                  # Datos del web scraping
│   │   ├── all_works.json
│   │   ├── letter_*.json
│   │   └── work_*.json
│   └── raw/                     # Datos originales
│       ├── pdfs/
│       ├── extracted_text/
│       └── images/
├── scripts/
│   ├── import_fuentesxi.py      # Script para importar datos de FUENTESXI
│   ├── import_catcom.py         # Script para importar datos de CATCOM
│   ├── merge_data.py            # Script para fusionar ambas fuentes
│   └── data_validation.py       # Script para validar datos
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── base.html
│   ├── obras/
│   ├── representaciones/
│   ├── lugares/
│   └── autores/
└── media/
    └── uploads/
```

## Modelos Django Propuestos

### 1. Obras (apps/obras/models.py)
```python
class Obra(models.Model):
    titulo = models.CharField(max_length=500)
    titulo_limpio = models.CharField(max_length=500, unique=True)
    titulo_alternativo = models.CharField(max_length=500, blank=True)
    autor = models.ForeignKey('autores.Autor', on_delete=models.SET_NULL, null=True)
    tipo_obra = models.CharField(max_length=100)  # Comedia, Auto, Zarzuela, etc.
    genero = models.CharField(max_length=100, blank=True)
    edicion_principe = models.TextField(blank=True)
    notas_bibliograficas = models.TextField(blank=True)
    fuente_principal = models.CharField(max_length=50)  # 'FUENTESXI' o 'CATCOM'
    tema = models.CharField(max_length=200, blank=True)
    musica_conservada = models.BooleanField(default=False)
    compositor = models.CharField(max_length=200, blank=True)
    mecenas = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 2. Representaciones (apps/representaciones/models.py)
```python
class Representacion(models.Model):
    obra = models.ForeignKey('obras.Obra', on_delete=models.CASCADE)
    fecha = models.CharField(max_length=50)  # Fecha original del texto
    fecha_formateada = models.DateField(null=True, blank=True)
    compañia = models.CharField(max_length=200, blank=True)
    lugar = models.ForeignKey('lugares.Lugar', on_delete=models.SET_NULL, null=True)
    tipo_lugar = models.CharField(max_length=100, blank=True)
    fuente = models.CharField(max_length=200, blank=True)
    observaciones = models.TextField(blank=True)
    mecenas = models.CharField(max_length=200, blank=True)
    gestor_administrativo = models.CharField(max_length=200, blank=True)
```

### 3. Lugares (apps/lugares/models.py)
```python
class Lugar(models.Model):
    nombre = models.CharField(max_length=200)
    coordenadas_lat = models.FloatField(null=True, blank=True)
    coordenadas_lng = models.FloatField(null=True, blank=True)
    region = models.CharField(max_length=200, blank=True)
    pais = models.CharField(max_length=100, default='España')
    tipo_lugar = models.CharField(max_length=100)  # Palacio, Corral, etc.
    descripcion = models.TextField(blank=True)
    poblacion_estimada = models.IntegerField(null=True, blank=True)
    es_capital = models.BooleanField(default=False)
```

### 4. Autores (apps/autores/models.py)
```python
class Autor(models.Model):
    nombre = models.CharField(max_length=200)
    nombre_completo = models.CharField(max_length=300, blank=True)
    fecha_nacimiento = models.CharField(max_length=50, blank=True)
    fecha_muerte = models.CharField(max_length=50, blank=True)
    biografia = models.TextField(blank=True)
    obras_principales = models.TextField(blank=True)
    epoca = models.CharField(max_length=100, blank=True)  # Siglo de Oro, etc.
```

### 5. Bibliografia (apps/bibliografia/models.py)
```python
class ReferenciaBibliografica(models.Model):
    obra = models.ForeignKey('obras.Obra', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=500)
    autor = models.CharField(max_length=300, blank=True)
    editor = models.CharField(max_length=300, blank=True)
    lugar_publicacion = models.CharField(max_length=200, blank=True)
    año_publicacion = models.CharField(max_length=50, blank=True)
    paginas = models.CharField(max_length=100, blank=True)
    tipo_referencia = models.CharField(max_length=100)  # Libro, Artículo, etc.
    url = models.URLField(blank=True)
    notas = models.TextField(blank=True)
```

## APIs REST Propuestas

### Endpoints principales:
- `/api/obras/` - Lista y búsqueda de obras
- `/api/obras/{id}/` - Detalle de obra específica
- `/api/representaciones/` - Lista de representaciones
- `/api/lugares/` - Lista de lugares
- `/api/autores/` - Lista de autores
- `/api/bibliografia/` - Referencias bibliográficas
- `/api/stats/` - Estadísticas del sistema
- `/api/search/` - Búsqueda avanzada

## Funcionalidades Principales

1. **Búsqueda Avanzada**: Por título, autor, fecha, lugar, tipo de obra
2. **Visualización Geográfica**: Mapa interactivo de lugares de representación
3. **Análisis Temporal**: Gráficos de representaciones por década
4. **Comparación de Fuentes**: Análisis de diferencias entre FUENTESXI y CATCOM
5. **Exportación de Datos**: CSV, JSON, PDF
6. **API REST**: Para integración con otras aplicaciones
7. **Panel de Administración**: Gestión completa de datos
8. **Validación de Datos**: Verificación de consistencia entre fuentes

## Scripts de Importación

1. **import_fuentesxi.py**: Importa datos de la base SQLite
2. **import_catcom.py**: Importa datos de archivos JSON
3. **merge_data.py**: Fusiona y deduplica datos de ambas fuentes
4. **data_validation.py**: Valida consistencia de datos importados

## Tecnologías Utilizadas

- **Backend**: Django 4.2+, Django REST Framework
- **Base de Datos**: PostgreSQL (producción), SQLite (desarrollo)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **APIs**: Django REST Framework
- **Visualización**: Chart.js, Leaflet.js
- **Herramientas**: Celery (tareas asíncronas), Redis (cache)

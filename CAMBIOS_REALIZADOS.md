# Cambios Realizados en la Aplicación DELIA

## Fecha: 2 de Octubre, 2025

---

## 1. Corrección del Orden Cronológico de las Representaciones

### Problema
Las representaciones de cada comedia no estaban ordenadas cronológicamente. Por ejemplo, en "A un tiempo rey y vasallo", la representación de 1688 aparecía después de las de 1691.

### Solución
- **Archivo modificado**: `apps/obras/views.py`
- Se añadió ordenamiento explícito por `fecha_formateada` en la vista de detalle de obra:
  ```python
  representaciones = obra.representaciones.all().order_by('fecha_formateada')
  ```
- Las representaciones ahora se muestran en orden cronológico ascendente (de más antigua a más reciente).

---

## 2. Campos Adicionales: Mecenas, Música y Fuente Utilizada

### Estado Actual
Los campos solicitados **ya existían** en los modelos de la aplicación:

#### En el modelo `Obra`:
- `mecenas`: CharField para almacenar el mecenas o patrocinador
- `compositor`: CharField para el compositor de la música
- `musica_conservada`: BooleanField para indicar si se conserva música de la obra

#### En el modelo `Representacion`:
- `mecenas`: CharField para mecenas de representaciones específicas
- `gestor_administrativo`: CharField para gestores administrativos
- `fuente`: CharField para la fuente de información

### Mejoras Realizadas
- **Filtros API mejorados**: Se agregaron `mecenas`, `compositor` y `musica_conservada` a los filtros de la API REST en `ObraViewSet`.
- **Búsqueda mejorada**: Se añadieron estos campos a los campos de búsqueda (`search_fields`).
- **Formularios de edición**: Los campos ya estaban disponibles en las plantillas de edición.

---

## 3. Filtros Adicionales en la Interfaz

### Nuevos Filtros Implementados

#### Para Obras (`ObraViewSet`):
```python
filterset_fields = [
    'autor', 'tipo_obra', 'genero', 'fuente_principal', 
    'musica_conservada', 'mecenas', 'compositor'
]
search_fields = [
    'titulo', 'titulo_limpio', 'titulo_alternativo', 'autor__nombre', 
    'mecenas', 'compositor', 'tema', 'notas_bibliograficas'
]
```

#### Para Representaciones (`RepresentacionViewSet`):
```python
filterset_fields = [
    'obra', 'lugar', 'tipo_lugar', 'compañia', 'director_compañia', 
    'tipo_funcion', 'mecenas', 'gestor_administrativo'
]
search_fields = [
    'fecha', 'compañia', 'director_compañia', 'observaciones', 
    'fuente', 'mecenas', 'gestor_administrativo'
]
```

---

## 4. Sistema de Temas Literarios

### Nuevos Modelos Creados

#### `TemaLiterario`
Modelo para clasificar obras por temas literarios (mitológico, histórico, religioso, etc.).

**Tipos de tema disponibles**:
- Mitológico
- Histórico
- Religioso
- Cómico
- Trágico
- Pastoral
- Caballeresco
- Costumbrista
- Moral
- Político
- Amoroso
- Otro

#### `ObraTema`
Modelo intermedio many-to-many que relaciona obras con temas, permitiendo:
- Múltiples temas por obra
- Indicar si un tema es el principal
- Añadir notas sobre la relación obra-tema

### APIs Creadas
- `GET /obras/temas-literarios/` - Listar temas literarios
- `GET /obras/obra-temas/` - Listar relaciones obra-tema
- Filtros por tipo de tema, es_principal, etc.

### Panel de Administración
Se agregaron interfaces de administración para gestionar temas y asignaciones:
- `TemaLiterarioAdmin`: Gestionar temas literarios
- `ObraTemaAdmin`: Asignar temas a obras

---

## 5. Búsqueda Semántica Avanzada

### Nueva Funcionalidad: `busqueda_avanzada_view`

**URL**: `/obras/busqueda-avanzada/`

**Características**:
- Búsqueda semántica en notas bibliográficas, edición príncipe, observaciones y notas
- Filtros combinados:
  - Por tema literario
  - Por mecenas
  - Por compositor
  - Por presencia de música conservada
- Estadísticas de resultados
- Paginación de resultados

**Parámetros de búsqueda**:
- `q`: Término de búsqueda
- `tipo`: 'semantica' (busca en notas) o 'normal' (busca en títulos y autores)
- `tema`: Filtrar por tema literario
- `mecenas`: Filtrar por mecenas
- `compositor`: Filtrar por compositor
- `musica_conservada`: 'true' o 'false'

---

## 6. Análisis de Redes de Colaboración

### Nueva Vista: `redes_colaboracion_view`

**URL**: `/obras/redes-colaboracion/`

**Funcionalidades**:

#### Red de Autores
- Identifica colaboraciones entre autores que trabajaron con las mismas compañías
- Muestra los 20 autores más prolíficos
- Lista hasta 5 colaboradores por autor
- Estadísticas de obras y representaciones por autor

#### Red de Compañías
- Compañías que trabajaron con los mismos autores
- Relaciones entre compañías a través de autores comunes
- Estadísticas de representaciones y autores únicos por compañía
- Top 15 compañías más activas

#### Estadísticas Generales
- Total de autores en la base de datos
- Autores con obras registradas
- Total de compañías únicas
- Total de representaciones

---

## 7. Mapas Geográficos con Seguimiento Temporal

### Nueva Vista: `mapas_geograficos_view`

**URL**: `/obras/mapas-geograficos/`

**Características**:

#### Seguimiento Temporal
- Visualización de representaciones por lugar y año
- Movimiento de obras entre lugares a lo largo del tiempo
- Comparación de obras en diferentes espacios geográficos

#### Filtros Disponibles
- Por obra específica
- Por autor
- Por década
- Por lugar

#### Datos Proporcionados por Lugar
- Total de representaciones
- Obras únicas representadas
- Autores únicos
- Fecha de primera representación
- Fecha de última representación
- Desglose por año con obras y fechas

#### Estadísticas
- Total de lugares con representaciones
- Total de representaciones filtradas
- Total de obras únicas
- Total de autores únicos

---

## 8. Migraciones de Base de Datos

### Nueva Migración: `0003_obratema_temaliterario_obratema_tema_and_more.py`

**Cambios en la base de datos**:
- Tabla `obras_temaliterario`: Almacena temas literarios
- Tabla `obras_obratema`: Relación many-to-many entre obras y temas
- Constraint de unicidad: Una obra no puede tener el mismo tema duplicado

**Estado**: ✅ Migración aplicada exitosamente

---

## 9. URLs Actualizadas

### Nuevas Rutas API REST
- `/obras/temas-literarios/` - CRUD de temas literarios
- `/obras/obra-temas/` - CRUD de relaciones obra-tema

### Nuevas Vistas Web
- `/obras/busqueda-avanzada/` - Búsqueda semántica avanzada
- `/obras/redes-colaboracion/` - Análisis de redes
- `/obras/mapas-geograficos/` - Mapas temporales

---

## 10. Interfaces de Administración

### Modelos Administrados
1. **Obra** - Ya existente, mejorado con nuevos filtros
2. **Manuscrito** - Ya existente
3. **PaginaPDF** - Ya existente
4. **TemaLiterario** - NUEVO
5. **ObraTema** - NUEVO

### Funcionalidades de Administración
- Filtros por tipo de tema, principal, etc.
- Búsqueda en todos los campos relevantes
- Campos de solo lectura para metadatos
- Fieldsets colapsables para mejor organización

---

## Resumen de Archivos Modificados

### Modelos
- ✅ `apps/obras/models.py` - Añadidos `TemaLiterario` y `ObraTema`

### Vistas
- ✅ `apps/obras/views.py` - Añadidas 3 nuevas vistas, mejorados filtros
- ✅ `apps/representaciones/views.py` - Mejorados filtros

### Serializers
- ✅ `apps/obras/serializers.py` - Añadidos serializers para temas

### URLs
- ✅ `apps/obras/urls.py` - Añadidas nuevas rutas

### Admin
- ✅ `apps/obras/admin.py` - Registrados nuevos modelos

---

## Próximos Pasos Sugeridos

### 1. Plantillas HTML Pendientes
Crear las siguientes plantillas para las nuevas vistas:
- `apps/obras/templates/obras/busqueda_avanzada.html`
- `apps/obras/templates/obras/redes_colaboracion.html`
- `apps/obras/templates/obras/mapas_geograficos.html`

### 2. Integración con ASODAT
Considerar APIs para conectar con bases de datos del teatro clásico español.

### 3. Análisis Temporal Avanzado
Implementar visualizaciones interactivas de datos temporales con bibliotecas como:
- Chart.js o D3.js para gráficos
- Leaflet o Mapbox para mapas interactivos

### 4. Sistema de Usuarios
Crear roles para los tres investigadores que clasificarán obras mitológicas:
- Permisos de edición específicos
- Sistema de revisión colaborativa
- Historial de cambios

### 5. Exportación de Datos
Añadir funcionalidad para exportar datos filtrados en diferentes formatos:
- CSV
- JSON
- Excel

---

## Notas Técnicas

### Base de Datos
- **Motor**: SQLite (db.sqlite3)
- **ORM**: Django 4.x
- **Estado**: Migraciones aplicadas correctamente

### API REST
- **Framework**: Django REST Framework
- **Formato**: JSON
- **Filtros**: django-filter
- **Paginación**: Implementada

### Frontend
- Plantillas Django
- CSS personalizado
- JavaScript vanilla (sin frameworks adicionales por ahora)

---

## Contacto y Soporte

Para preguntas sobre estos cambios, contactar a:
- Iván (Desarrollador)
- Equipo de investigación (Demo RESUMEN_DEMO_INVESTIGADORES.md)

---

**Documento generado automáticamente el 2 de Octubre, 2025**


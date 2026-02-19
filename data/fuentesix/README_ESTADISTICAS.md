# 📊 Sistema de Estadísticas - Base de Datos DELIA

## Archivos Creados

### 1. `estadisticas.html`
Página HTML completa con análisis estadístico de la base de datos.

**Ubicación**: Raíz del proyecto (`/estadisticas.html`)

**Características**:
- Diseño responsive compatible con GitHub Pages
- Carga dinámica de datos desde JSON
- Visualizaciones de completitud con barras de progreso
- Botones para copiar conclusiones individuales o todas
- Estilo consistente con `index.html`

### 2. `data/fuentesix/estadisticas_datos.json`
Archivo JSON con todas las estadísticas y análisis.

**Contenido**:
- Estadísticas generales (total obras, por fuente, representaciones)
- Completitud de campos por fuente (CATCOM, FUENTES IX, AMBAS)
- Análisis específico de FUENTES IX
- Conclusiones y recomendaciones para investigación

### 3. `data/fuentesix/generar_estadisticas.py`
Script Python para generar/actualizar las estadísticas.

**Uso**:
```bash
cd data/fuentesix
python3 generar_estadisticas.py
```

## Integración en index.html

Se añadió un enlace en la sección de "quick-links":
```html
<a href="estadisticas.html">📊 Estadísticas y Análisis</a>
```

## Contenido del Informe de Estadísticas

### Sección 1: Estadísticas Generales
- Total de obras (2,580)
- Distribución por fuente (CATCOM, FUENTES IX, AMBAS)
- Total de representaciones
- Lugares y compañías únicas

### Sección 2: Completitud de Datos por Fuente
- Tablas de completitud de campos
- Barras de progreso visuales
- Porcentajes de completitud
- Análisis de representaciones por fuente

### Sección 3: Análisis Específico de FUENTES IX
- Obras sin autor identificado
- Obras sin representaciones
- Títulos alternativos
- Distribución temporal (1622-1709)
- Lugares más frecuentes
- Compañías más frecuentes

### Sección 4: Conclusiones y Recomendaciones

#### Conclusiones Generadas:
1. **Completitud de Datos por Fuente**
   - Comparación entre CATCOM y FUENTES IX
   - Estadísticas de representaciones

2. **Campos con Baja Completitud en FUENTES IX**
   - Lista de campos con <50% completitud
   - Identificación de áreas de mejora

3. **Análisis Específico de FUENTES IX**
   - Porcentaje de obras sin autor (77.3%)
   - Porcentaje de obras sin representaciones (73.0%)
   - Referencias cruzadas y títulos alternativos

4. **Distribución Temporal**
   - Rango temporal completo
   - Picos de actividad teatral

#### Recomendaciones para Investigación:

1. **Búsqueda de Autores Faltantes**
   - Catálogo de Barrera y Leirado
   - Catálogos de Fajardo, Medel, García de la Huerta
   - Bibliotecas con catálogos de manuscritos

2. **Búsqueda de Ediciones Príncipes**
   - Series Diferentes y Escogidas (48 tomos)
   - Partes de dramaturgos
   - Comedias sueltas

3. **Búsqueda de Manuscritos**
   - Biblioteca Nacional de Madrid (B.N.M.)
   - Biblioteca Municipal de Madrid (B.M.M.)
   - Biblioteca del Instituto del Teatro de Barcelona (B.I.T.B.)
   - British Library (B.L.)
   - Archivo de la Cofradía de la Novena

4. **Volúmenes Relacionados de la Serie Fuentes**
   - Fuentes I, IV, V, VI, X, XI, XIII
   - Información adicional no consolidada

5. **Investigadores y Estudios Mencionados**
   - Emilio Cotarelo y Mori
   - Edward M. Wilson
   - María Grazia Profeti
   - Ruth Lee Kennedy
   - Louise Kathrin Stein
   - Arnold G. Reichenberger

## Funcionalidades de Copia

Cada conclusión y recomendación tiene un botón "📋 Copiar" que:
- Copia el texto formateado al portapapeles
- Incluye título y contenido
- Listo para pegar en búsquedas o documentos

Botón "📋 Copiar Todas las Conclusiones" copia todo el informe completo.

## Actualización de Estadísticas

Para actualizar las estadísticas después de cambios en los datos:

```bash
cd data/fuentesix
python3 generar_estadisticas.py
```

Esto regenerará `estadisticas_datos.json` con los datos más recientes.

## Uso en GitHub Pages

El sistema está diseñado para funcionar en GitHub Pages:
- Rutas relativas (`data/fuentesix/estadisticas_datos.json`)
- Sin dependencias externas
- Compatible con CORS
- Carga asíncrona de datos

## Datos que Identifican Gaps Sistemáticos

### Campos con <50% Completitud en FUENTES IX:
- **Mecenas**: 0% - Campo crítico faltante
- **Subgénero**: 0% - Clasificación detallada faltante
- **Manuscritos Conocidos**: 0% - Información bibliográfica faltante
- **Tema**: 5.5% - Temática de obras poco documentada
- **Fecha de Creación**: 14.7% - Cronología incompleta
- **Representaciones**: 15.3% - Muchas obras sin representaciones documentadas
- **Edición Príncipe**: 16.9% - Información editorial faltante
- **Títulos Alternativos**: 17.4% - Variantes de títulos incompletas
- **Género**: 22.0% - Clasificación genérica incompleta
- **Notas Bibliográficas**: 25.1% - Referencias bibliográficas incompletas

### Obras sin Datos Críticos:
- **77.3%** sin autor identificado
- **73.0%** sin representaciones documentadas

Estos porcentajes indican áreas prioritarias para investigación futura.

---

*Sistema creado el 2026-02-19*
*Última actualización: 2026-02-19*

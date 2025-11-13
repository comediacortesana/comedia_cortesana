# 🎭 Sistema Completo - Teatro Español del Siglo de Oro

Aplicación web completa para filtrar y explorar obras del teatro español del Siglo de Oro, desplegada en **GitHub Pages** con integración de **Google Sheets** y **Supabase**.

## 🌐 Aplicación en Vivo

**URL:** https://comediacortesana.github.io/comedia_cortesana/

## 🏗️ Arquitectura del Sistema

El sistema está compuesto por:

1. **Frontend HTML estático** (`index.html`) que lee datos desde `datos_obras.json`
2. **Despliegue en GitHub Pages** (gratuito, automático)
3. **Automatización Google Sheets → GitHub** mediante Apps Script
4. **Autenticación y usuarios** con Supabase
5. **Exportación a CSV** para edición colaborativa

### 📊 Flujo de Datos

```
Google Sheets (edición colaborativa)
    ↓ [Apps Script - cada hora]
GitHub Repository (datos_obras.json)
    ↓ [GitHub Pages - automático]
Aplicación Web (index.html)
    ↓ [Supabase]
Autenticación y gestión de usuarios
```

## 📁 Archivos Principales

- **`index.html`** - Aplicación principal con filtros, autenticación y exportación
- **`datos_obras.json`** - Datos de obras en formato JSON (actualizado automáticamente desde Google Sheets)
- **`obras_completas.csv`** - Exportación CSV de los datos (para referencia)

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

## 📥 Carga de Datos

### Implementación Actual

El `index.html` carga datos automáticamente desde `datos_obras.json` al iniciar:

```javascript
// Función cargarDatos() en index.html
async function cargarDatos() {
    const response = await fetch('datos_obras.json');
    const data = await response.json();
    
    // Soporta dos formatos:
    // 1. {metadata: {}, obras: []} - Formato recomendado
    // 2. [] - Array directo (formato antiguo)
    
    if (data.metadata && data.obras) {
        metadata = data.metadata;
        datosOriginales = data.obras;
    } else if (Array.isArray(data)) {
        datosOriginales = data;
    }
    
    datosFiltrados = [...datosOriginales];
    mostrarResultados();
}
```

### Formato del JSON

El archivo `datos_obras.json` debe tener este formato:

```json
{
  "metadata": {
    "total_obras": 150,
    "fecha_exportacion": "2025-01-15",
    "version": "1.0"
  },
  "obras": [
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
}
```

### Exportación a CSV

La aplicación permite exportar los resultados filtrados a CSV:

- **Función:** `exportarCSV()` en `index.html`
- **Uso:** Botón "📊 Exportar a CSV" en la interfaz
- **Formato:** CSV estándar con todos los campos de las obras filtradas
- **Propósito:** Edición colaborativa en Google Sheets o Excel

## 🎨 Personalización

El archivo HTML es completamente autónomo y puede ser personalizado:

1. **Estilos CSS**: Modificar la sección `<style>` para cambiar colores, fuentes, etc.
2. **Filtros**: Añadir o quitar campos en `.filters-grid`
3. **Tabla de resultados**: Modificar columnas en `mostrarResultados()`
4. **Datos de ejemplo**: Reemplazar `datosEjemplo` con datos reales

## 🚀 Despliegue en GitHub Pages

### Estado Actual

✅ **Aplicación desplegada en:** https://comediacortesana.github.io/comedia_cortesana/

### Cómo Funciona

1. **Repositorio GitHub:** Los archivos están en el repositorio `comedia_cortesana`
2. **GitHub Pages:** Configurado para servir desde la rama `main`
3. **Actualización automática:** Cada push a `main` actualiza la aplicación en 1-2 minutos
4. **Sin servidor:** Todo es estático, 100% gratuito

### Desarrollo Local

```bash
# Clonar repositorio
git clone https://github.com/comediacortesana/comedia_cortesana.git
cd comedia_cortesana

# Abrir index.html en navegador
# O usar un servidor local:
python -m http.server 8000
# Visitar http://localhost:8000/index.html
```

### Actualizar Datos

```bash
# 1. Actualizar datos_obras.json (manual o desde Google Sheets)
# 2. Commit y push
git add datos_obras.json
git commit -m "Actualizar datos de obras"
git push origin main

# 3. GitHub Pages se actualiza automáticamente en 1-2 minutos
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

## 🔐 Autenticación con Supabase

### Integración Actual

El `index.html` incluye autenticación completa con Supabase:

- ✅ **Registro de usuarios** con email y contraseña
- ✅ **Inicio de sesión** con email/contraseña o enlace mágico
- ✅ **Recuperación de contraseña**
- ✅ **Gestión de sesión** persistente
- ✅ **Panel de administración** para gestionar usuarios y roles

### Configuración

```javascript
// En index.html (línea ~591)
const SUPABASE_URL = 'https://kyxxpoewwjixbpcezays.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
```

### Documentación Supabase

| Archivo | Descripción |
|---------|-------------|
| **[GUIA_SUPABASE_PASO_A_PASO.md](./GUIA_SUPABASE_PASO_A_PASO.md)** | 📖 Guía completa de configuración |
| **[CHECKLIST_SUPABASE.md](./CHECKLIST_SUPABASE.md)** | ✅ Checklist de configuración |
| **[supabase_schema.sql](./supabase_schema.sql)** | 🗄️ Esquema de base de datos |
| **[supabase_frontend_code.js](./supabase_frontend_code.js)** | 💻 Código de ejemplo frontend |
| **[supabase_apps_script_code.gs](./supabase_apps_script_code.gs)** | 📊 Código de ejemplo Apps Script |

### Funcionalidades de Usuario

- **Usuarios registrados:** Pueden acceder a funcionalidades adicionales
- **Administradores:** Panel de gestión de usuarios y roles
- **Sesión persistente:** La sesión se mantiene entre recargas
- **Seguridad:** Autenticación gestionada por Supabase (gratis hasta 50,000 usuarios/mes)

---

## 📝 Notas

- Los datos se cargan desde `datos_obras.json` al iniciar la aplicación
- Los filtros funcionan de manera acumulativa (AND logic)
- La búsqueda de texto es case-insensitive
- Los filtros de fecha funcionan con años (formato numérico)
- El CSV se usa solo para exportar, no para cargar datos

---

## 🔄 Automatización: Google Sheets → GitHub

### 🚀 Nueva Funcionalidad: Sincronización Automática

Sincroniza automáticamente Google Sheets con GitHub sin servidores, **100% gratuito**.

**Características:**
- ✅ Detección inteligente de cambios
- ✅ Exportación automática a CSV/JSON
- ✅ Push automático a GitHub
- ✅ Triggers configurables
- ✅ Backups en Google Drive
- ✅ Notificaciones (Slack/Discord/Email)

### 📚 Documentación Completa

| Archivo | Descripción |
|---------|-------------|
| **[SHEETS_GITHUB_SYNC_README.md](./SHEETS_GITHUB_SYNC_README.md)** | 🎯 README principal - **EMPIEZA AQUÍ** |
| **[GUIA_PASO_A_PASO_APPS_SCRIPT.md](./GUIA_PASO_A_PASO_APPS_SCRIPT.md)** | 📖 **Guía DETALLADA paso a paso** ⭐ NUEVA |
| **[AUTOMATIZACION_SHEETS_GITHUB.md](./AUTOMATIZACION_SHEETS_GITHUB.md)** | 📚 Guía completa paso a paso |
| **[CONFIGURACION_EJEMPLOS.md](./CONFIGURACION_EJEMPLOS.md)** | 📝 6 ejemplos de configuración reales |
| **[FAQ_TROUBLESHOOTING.md](./FAQ_TROUBLESHOOTING.md)** | ❓ Solución a problemas + FAQ |
| **[sheets-github-sync.gs](./sheets-github-sync.gs)** | 💻 Script principal para Apps Script |
| **[sheets-github-sync-advanced.gs](./sheets-github-sync-advanced.gs)** | 🚀 Script avanzado con extras |

### ⚡ Setup Rápido (5 minutos)

1. **Copiar script:** `sheets-github-sync.gs` → Apps Script
2. **Configurar:** owner, repo, token, paths
3. **Token GitHub:** https://github.com/settings/tokens (scope: `repo`)
4. **Guardar token:** Ejecutar `setGitHubToken()`
5. **Probar:** Ejecutar `syncToGitHub()`
6. **Automatizar:** Trigger cada hora

**Ver guía completa:** [AUTOMATIZACION_SHEETS_GITHUB.md](./AUTOMATIZACION_SHEETS_GITHUB.md)

### 🎯 Casos de Uso

- **Edición colaborativa:** Investigadores editan → Sync automático cada hora
- **Backup diario:** Guarda en Drive + GitHub cada medianoche
- **Tiempo real:** Push inmediato tras edición (con debounce)
- **Múltiples hojas:** Obras, Autores, Lugares → archivos separados

**Ver ejemplos completos:** [CONFIGURACION_EJEMPLOS.md](./CONFIGURACION_EJEMPLOS.md)

### 💡 Workflow Automatizado

```
Google Sheets (edición) 
    → Apps Script (cada hora)
    → Detección de cambios
    → Push a GitHub (si hay cambios)
    → GitHub Pages actualizado
    → ¡Usuarios ven cambios!
```

**Gratis, sin servidores, automático. 🎉**

---

## 📚 Documentación Adicional

### Guías Completas Disponibles

| Documento | Descripción |
|-----------|-------------|
| **[README_COMPLETO.md](./README_COMPLETO.md)** | 📖 Documentación completa del sistema |
| **[GITHUB_PAGES_TUTORIAL.md](./GITHUB_PAGES_TUTORIAL.md)** | 🚀 Tutorial de GitHub Pages |
| **[SISTEMA_FEEDBACK.md](./SISTEMA_FEEDBACK.md)** | 💬 Sistema de feedback para investigadores |
| **[INSTRUCCIONES_PUBLICACION.md](./INSTRUCCIONES_PUBLICACION.md)** | 📝 Instrucciones de publicación |
| **[CONFIGURAR_DOMINIO_PERSONALIZADO.md](./CONFIGURAR_DOMINIO_PERSONALIZADO.md)** | 🌐 Configurar dominio personalizado |

### Resumen del Sistema Completo

✅ **Frontend:** HTML estático con JavaScript vanilla  
✅ **Datos:** JSON (`datos_obras.json`) cargado automáticamente  
✅ **Despliegue:** GitHub Pages (gratuito)  
✅ **Automatización:** Google Sheets → GitHub (Apps Script)  
✅ **Usuarios:** Supabase (autenticación y gestión)  
✅ **Exportación:** CSV para edición colaborativa  

**URL de producción:** https://comediacortesana.github.io/comedia_cortesana/

---

## 🔄 Workflow Completo

```
1. Investigadores editan en Google Sheets
   ↓
2. Apps Script detecta cambios (cada hora)
   ↓
3. Apps Script actualiza datos_obras.json en GitHub
   ↓
4. GitHub Pages actualiza automáticamente (1-2 min)
   ↓
5. Usuarios ven datos actualizados en la web
   ↓
6. Usuarios pueden exportar a CSV para más ediciones
```

**Todo automático, gratuito y sin servidores. 🎉**


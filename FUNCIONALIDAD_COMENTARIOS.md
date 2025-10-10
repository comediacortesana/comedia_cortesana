# Funcionalidad de Comentarios de Usuario

## Descripción
Sistema de comentarios que permite a los usuarios registrados compartir sus descubrimientos, análisis y observaciones sobre obras teatrales del Siglo de Oro. Los comentarios públicos se muestran en la página principal para fomentar la colaboración académica.

## Características Implementadas

### 1. Creación de Comentarios
Los usuarios autenticados pueden crear comentarios asociados a una o más obras:
- **Título**: Resumen breve del comentario
- **Contenido**: Texto detallado del comentario/análisis
- **Obras Asociadas**: Una o más obras relacionadas con el comentario
- **Visibilidad**: Público o privado
- **Catálogo**: Asociado a FUENTESXI o CATCOM

### 2. Visualización en Panel Principal
La página principal (`http://127.0.0.1:8000/`) muestra:
- **Últimos 5 comentarios públicos** más recientes
- **Información del autor**: Nombre del usuario que hizo el comentario
- **Fecha y hora**: Cuándo se publicó el comentario
- **Resumen**: Primeros 200 caracteres del comentario
- **Obras asociadas**: Nombres completos de las obras con enlaces clickeables
- **Catálogo de origen**: FUENTESXI o CATCOM

### 3. Diseño y Presentación
Los comentarios se muestran con un diseño atractivo que incluye:
- 💬 Icono identificativo de comentarios
- 👤 Información del usuario
- 📚 **Enlaces a obras**: Nombres completos con enlaces clickeables que llevan a `/obras/{id}/`
- 🗂️ Identificación del catálogo (FUENTESXI/CATCOM)
- Efectos hover para mejor interactividad
- Diseño responsive para móviles
- Enlaces con estilo de badges que cambian al hacer hover

## Uso

### Para Crear un Comentario

#### Opción 1: Desde el Editor de Catálogos
1. **Iniciar Sesión**: Accede con tu usuario
2. **Ir al Editor**: `http://127.0.0.1:8000/obras/editor/`
3. **Seleccionar Catálogo**: Elige FUENTESXI o CATCOM
4. **Seleccionar Obras**: Marca las obras sobre las que quieres comentar
5. **Crear Comentario**: Usa el botón correspondiente para abrir el formulario
6. **Completar Datos**:
   - Título del comentario
   - Contenido/análisis
   - Marcar como público (si quieres que aparezca en el panel principal)
7. **Guardar**: El comentario se guardará y aparecerá en la página principal si es público

#### Opción 2: Desde el Perfil de una Obra (NUEVO)
1. **Iniciar Sesión**: Accede con tu usuario
2. **Ir a una Obra**: Por ejemplo `http://127.0.0.1:8000/obras/3058/`
3. **Ver Sección de Comentarios**: Desplázate hasta la sección "💬 Comentarios"
4. **Completar el Formulario**:
   - Título del comentario
   - Contenido de tu análisis u observación
   - Marcar como público si quieres compartirlo con la comunidad
5. **Publicar**: El comentario se asociará automáticamente a esa obra
6. **Ver Resultados**: Los comentarios públicos aparecen inmediatamente en el inicio

### Para Ver Comentarios

#### En la Página Principal
Los comentarios públicos aparecen automáticamente en:
- **Página Principal**: `http://127.0.0.1:8000/`
- Sección "💬 Comentarios Recientes de la Comunidad"
- Ordenados por fecha (más recientes primero)
- Con enlaces directos a las obras comentadas

#### En el Perfil de Cada Obra
- Cada obra muestra sus comentarios propios
- Puedes ver comentarios públicos de otros usuarios
- Puedes ver todos tus comentarios (públicos y privados) sobre esa obra
- Puedes eliminar tus propios comentarios

### Navegación Mejorada
Cada comentario ahora incluye:
- **Enlaces directos a obras**: Haz clic en el nombre de cualquier obra para ir a su página de detalle
- **URLs específicas**: Los enlaces siguen el formato `/obras/{id}/` (ej: `/obras/3058/`)
- **Navegación contextual**: Desde un comentario puedes ir directamente a ver los detalles de la obra comentada
- **Botones de navegación**: En el editor hay un botón "Ir a Inicio" para volver rápidamente a la página principal

## Modelo de Datos

### ComentarioUsuario
```python
- usuario: ForeignKey(Usuario) - Autor del comentario
- catalogo: CharField - 'fuentesxi' o 'catcom'
- obras_seleccionadas: ManyToManyField(Obra) - Obras relacionadas
- titulo: CharField - Título del comentario
- comentario: TextField - Contenido completo
- fecha_creacion: DateTimeField - Fecha de creación
- fecha_modificacion: DateTimeField - Última modificación
- es_publico: BooleanField - Visibilidad pública
```

## API Endpoints

### Guardar Comentario (Desde Editor)
- **URL**: `/obras/editor/<catalogo_id>/comentario/`
- **Método**: POST
- **Autenticación**: Requerida
- **Parámetros**:
  ```json
  {
    "titulo": "string",
    "comentario": "string",
    "es_publico": boolean,
    "elementos_seleccionados": [
      {
        "section": "obras",
        "item_id": number
      }
    ]
  }
  ```

### Guardar Comentario (Desde Perfil de Obra) - NUEVO
- **URL**: `/obras/<obra_id>/comentario/`
- **Método**: POST
- **Autenticación**: Requerida
- **Parámetros**:
  ```json
  {
    "titulo": "string",
    "comentario": "string",
    "es_publico": boolean
  }
  ```

### Obtener Comentarios de una Obra - NUEVO
- **URL**: `/obras/<obra_id>/comentarios/`
- **Método**: GET
- **Autenticación**: Requerida
- **Respuesta**: Lista de comentarios de esa obra (públicos + privados del usuario)

### Eliminar Comentario - NUEVO
- **URL**: `/obras/comentario/<comentario_id>/eliminar/`
- **Método**: POST
- **Autenticación**: Requerida
- **Restricción**: Solo el autor puede eliminar sus propios comentarios

### Obtener Comentarios del Usuario
- **URL**: `/obras/editor/<catalogo_id>/comentarios/`
- **Método**: GET
- **Autenticación**: Requerida
- **Respuesta**: Lista de comentarios del usuario actual

## Comentarios de Prueba

Para crear comentarios de prueba, ejecuta:
```bash
python scripts/create_test_comments.py
```

Este script crea 4 comentarios de ejemplo usando usuarios de prueba.

## Seguridad y Privacidad

- ✅ Solo usuarios autenticados pueden crear comentarios
- ✅ Los usuarios solo pueden ver sus propios comentarios privados
- ✅ Los comentarios públicos son visibles para todos
- ✅ Protección CSRF en todas las peticiones
- ✅ Validación de datos en el servidor
- ✅ Verificación de existencia de obras asociadas

## Futuras Mejoras

- [ ] Sistema de respuestas a comentarios (hilos de conversación)
- [ ] Votación/valoración de comentarios útiles
- [ ] Búsqueda y filtrado de comentarios
- [ ] Notificaciones cuando alguien comenta obras relacionadas
- [ ] Exportar comentarios a formato académico (PDF, BibTeX)
- [ ] Menciones a otros usuarios (@usuario)
- [ ] Etiquetas/tags para categorizar comentarios
- [ ] Página dedicada para ver todos los comentarios públicos
- [ ] Moderación de comentarios para administradores
- [ ] Estadísticas de participación de usuarios

## Casos de Uso Académico

### Investigador Analizando Patrones
Un investigador puede:
1. Identificar obras con características similares
2. Crear un comentario documentando sus hallazgos
3. Asociar todas las obras relevantes
4. Hacer público el comentario para colaboración
5. Otros investigadores pueden ver y construir sobre este análisis

### Estudiante Haciendo Notas
Un estudiante puede:
1. Tomar notas sobre obras específicas
2. Mantener comentarios privados para estudio personal
3. Compartir públicamente cuando tenga conclusiones completas

### Colaboración entre Académicos
Los académicos pueden:
1. Ver comentarios recientes en la página principal
2. Identificar investigaciones relacionadas
3. Contactar a autores de comentarios relevantes
4. Construir conocimiento colectivo sobre el Siglo de Oro

## Notas Técnicas

### Optimización de Consultas
- Uso de `select_related()` para evitar N+1 queries
- Uso de `prefetch_related()` para obras relacionadas
- Límite de 5 comentarios en página principal para rendimiento

### Truncado de Texto
- Comentarios largos se truncan a 200 caracteres
- Se agrega "..." para indicar contenido adicional
- Futuro: enlace para ver comentario completo

### Responsive Design
- Diseño adaptativo para móviles
- Cards apilables en pantallas pequeñas
- Tamaños de fuente ajustables

## Créditos y Licencia
Parte del sistema de Base de Datos de Teatro Español del Siglo de Oro
Desarrollado para investigación académica y colaboración científica


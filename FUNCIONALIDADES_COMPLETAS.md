# 📋 Listado Completo de Funcionalidades del Sistema

## 🎯 VISIÓN GENERAL
Sistema web para gestión y consulta de obras del Teatro Español del Siglo de Oro con autenticación, roles de usuario, edición colaborativa y sistema de comentarios.

---

## 🔐 AUTENTICACIÓN Y GESTIÓN DE USUARIOS

### Registro e Inicio de Sesión
- ✅ Registro de nuevos usuarios con email y contraseña
- ✅ Inicio de sesión con email/contraseña
- ✅ Inicio de sesión con enlace mágico (sin contraseña)
- ✅ Recuperación de contraseña por email
- ✅ Reenvío de email de confirmación
- ✅ Sesión persistente entre recargas de página
- ✅ Cierre de sesión seguro

### Roles y Permisos
- ✅ Sistema de 3 roles: Colaborador, Editor, Admin
- ✅ Asignación automática de rol "colaborador" al registrarse
- ✅ Cambio de roles por administradores
- ✅ Verificación de permisos en tiempo real
- ✅ Badge visual del rol en la interfaz

---

## 📊 CONSULTA Y FILTRADO DE DATOS

### Carga de Datos
- ✅ Carga automática desde la base de datos Django/PostgreSQL (fuente principal)
- ✅ Fallback automático a JSON local si la base de datos falla
- ✅ Carga paginada para grandes volúmenes (1000 obras por página)
- ✅ Timeout y reintentos automáticos en caso de error
- ✅ Indicador visual del estado de carga
- ✅ Metadata de fuente y última actualización

### Filtros de Búsqueda
- ✅ Filtro por título de obra (búsqueda parcial, case-insensitive)
- ✅ Filtro por tipo de obra (comedia, auto, zarzuela, entremés, etc.)
- ✅ Filtro por fuente de datos (FUENTES IX, CATCOM, AMBAS)
- ✅ Filtro por autor (búsqueda parcial)
- ✅ Filtro por época (ej: Siglo de Oro)
- ✅ Filtro por lugar/ciudad (búsqueda parcial)
- ✅ Filtro por tipo de lugar (palacio, corral, iglesia, etc.)
- ✅ Filtro por región/provincia
- ✅ Filtro por compañía teatral
- ✅ Filtro por rango de fechas (desde/hasta)
- ✅ Filtro por mecenas
- ✅ Aplicación de múltiples filtros simultáneos (lógica AND)
- ✅ Botón para limpiar todos los filtros
- ✅ Contador de resultados en tiempo real

### Visualización de Resultados
- ✅ Tabla responsive con todas las obras filtradas
- ✅ Columnas: ID, Título, Autor, Tipo, Fuente, Lugar, Fecha, Compañía
- ✅ Indicador visual de obras con cambios pendientes (fondo amarillo)
- ✅ Click en fila para ver detalles completos
- ✅ Scroll infinito para grandes listas
- ✅ Formato visual de badges para fuente de datos

---

## 📝 MODAL DE DETALLES DE OBRA

### Información Mostrada
- ✅ Información básica: ID, títulos, tipo, género, tema, idioma, fecha
- ✅ Información del autor: nombre, fechas, época, biografía
- ✅ Estructura: número de actos y versos
- ✅ Información musical: música conservada, compositor, bibliotecas
- ✅ Mecenazgo y patrocinio
- ✅ Bibliografía e historia textual: ediciones, manuscritos, notas
- ✅ Fuente y origen de datos: PDF, página, texto original
- ✅ Notas y observaciones
- ✅ Representaciones: lista completa con todos los campos
- ✅ Texto original extraído del PDF (si existe)

### Navegación
- ✅ Botón "💬 Comentarios" en header para ir directamente a comentarios
- ✅ Scroll suave entre secciones
- ✅ Cierre con botón X o tecla ESC
- ✅ Click fuera del modal para cerrar

---

## ✏️ SISTEMA DE EDICIÓN

### Modo Edición
- ✅ Activación/desactivación del modo edición (solo Editor y Admin)
- ✅ Botón visual "✏️ Modo Edición" en la interfaz
- ✅ Indicador visual cuando el modo está activo
- ✅ Botones de edición junto a cada campo editable en el modal

### Edición de Campos
- ✅ Edición individual de campos desde el modal de detalles
- ✅ Validación de datos antes de guardar
- ✅ Vista previa del cambio antes de confirmar
- ✅ Comentarios opcionales al editar
- ✅ Cambios guardados en memoria local mientras se editan

### Gestión de Cambios
- ✅ Cambios pendientes visibles con fondo amarillo
- ✅ Vista de todos los cambios pendientes antes de guardar
- ✅ Persistencia de cambios según rol:
  - **Editor**: Cambios requieren aprobación del admin
  - **Admin**: Cambios se aplican inmediatamente
- ✅ Cancelación de cambios pendientes

---

## 💬 SISTEMA DE COMENTARIOS

### Comentarios por Obra
- ✅ Sección de comentarios en cada modal de obra
- ✅ Ubicación destacada al principio del modal
- ✅ Formulario para añadir comentarios sobre obras específicas
- ✅ Lista de todos los comentarios de la obra
- ✅ Información del autor del comentario y fecha
- ✅ Comentarios públicos para todos los usuarios logueados

### Comentarios Generales
- ✅ Botón "💬 Comentarios" en la barra superior con contador
- ✅ Modal global con todos los comentarios del sistema
- ✅ Creación de comentarios generales (sin asociar a obra)
- ✅ Opción para guardar filtros de búsqueda con el comentario
- ✅ Botón "🔍 Reproducir búsqueda" para comentarios con filtros guardados
- ✅ Aplicación automática de filtros guardados al reproducir búsqueda

### Gestión de Comentarios (Admin)
- ✅ Contador de comentarios no vistos en el botón principal
- ✅ Badge "✅ OK, visto" para comentarios revisados
- ✅ Badge "⚠️ Pendiente" para comentarios sin revisar
- ✅ Botón "✓ OK, visto" para marcar comentarios como revisados
- ✅ Actualización automática del contador cada 2 minutos
- ✅ Indicador visual de comentarios vistos (opacidad reducida)

---

## ⚠️ SISTEMA DE LOGS DE ERRORES

### Registro Automático
- ✅ Registro automático cuando falla la carga desde la base de datos
- ✅ Registro cuando falla el fallback a JSON
- ✅ Registro de errores no manejados
- ✅ Información capturada: usuario, hora, tipo de error, mensaje, detalles técnicos
- ✅ URL y user agent del navegador

### Visualización (Solo Admin)
- ✅ Sección dedicada en el Panel Admin
- ✅ Tabla con todos los logs de errores
- ✅ Filtrado por estado (visto/no visto)
- ✅ Contador de errores pendientes de revisar
- ✅ Botón para ver detalles técnicos completos
- ✅ Botón para marcar logs como vistos

---

## ⚙️ PANEL DE ADMINISTRACIÓN

### Gestión de Usuarios
- ✅ Lista completa de todos los usuarios registrados
- ✅ Visualización de ID, nombre y rol actual
- ✅ Cambio de roles mediante dropdown (colaborador/editor/admin)
- ✅ Aplicación inmediata de cambios de rol
- ✅ Actualización automática de la lista tras cambios

### Gestión de Cambios Pendientes
- ✅ Lista de todos los cambios pendientes de aprobación
- ✅ Información del usuario que propuso el cambio
- ✅ Vista de campo, valor anterior y valor propuesto
- ✅ Aprobación o rechazo de cambios
- ✅ Aplicación inmediata de cambios aprobados

### Logs de Errores
- ✅ Visualización de todos los errores registrados
- ✅ Filtrado por estado (visto/no visto)
- ✅ Detalles técnicos de cada error
- ✅ Marcado de errores como vistos

---

## 📤 EXPORTACIÓN DE DATOS

### Exportación a CSV
- ✅ Exportación de resultados filtrados a CSV
- ✅ Inclusión de todos los campos de las obras
- ✅ Formato compatible con Excel y Google Sheets
- ✅ Escapado correcto de caracteres especiales
- ✅ Descarga automática del archivo CSV

---

## 🔄 SINCRONIZACIÓN Y BACKUP

### Sincronización con la Base de Datos
- ✅ Carga automática desde la base de datos al iniciar
- ✅ Scripts Python para sincronización manual
- ✅ Backup automático a JSON local si la base de datos falla

### Scripts Disponibles
- ✅ `sync_to_sheets.py` - Sincronizar con Google Sheets
- ✅ `diagnosticar_carga_datos.py` - Diagnosticar problemas de carga

---

## 🎨 INTERFAZ DE USUARIO

### Diseño y Usabilidad
- ✅ Interfaz responsive y moderna
- ✅ Colores distintivos por tipo de fuente de datos
- ✅ Badges visuales para estados y roles
- ✅ Iconos emoji para mejor identificación visual
- ✅ Modales con scroll independiente
- ✅ Mensajes de error claros y descriptivos
- ✅ Indicadores de carga y estado

### Navegación
- ✅ Header fijo con información del usuario
- ✅ Botones de acción siempre visibles
- ✅ Accesos rápidos a funciones principales
- ✅ Teclado ESC para cerrar modales
- ✅ Scroll suave entre secciones

---

## 🔒 SEGURIDAD Y PERMISOS

### Row Level Security (RLS)
- ✅ Políticas RLS en todas las tablas
- ✅ Lectura pública de obras
- ✅ Escritura controlada por roles
- ✅ Comentarios públicos para usuarios autenticados
- ✅ Logs solo visibles para administradores

### Validaciones
- ✅ Validación de email en registro
- ✅ Validación de permisos antes de acciones
- ✅ Verificación de sesión en operaciones críticas
- ✅ Manejo seguro de errores sin exponer información sensible

---

## 📱 CARACTERÍSTICAS TÉCNICAS

### Rendimiento
- ✅ Carga paginada de datos grandes
- ✅ Timeout y reintentos automáticos
- ✅ Cache de datos en memoria
- ✅ Actualización incremental del contador de comentarios
- ✅ Lazy loading de comentarios

### Compatibilidad
- ✅ Funciona en todos los navegadores modernos
- ✅ Sin dependencias externas pesadas
- ✅ JavaScript vanilla (sin frameworks)
- ✅ HTML estático compatible con GitHub Pages

### Manejo de Errores
- ✅ Mensajes de error descriptivos
- ✅ Fallback automático a respaldo
- ✅ Logging detallado en consola
- ✅ Notificaciones al usuario cuando es necesario
- ✅ Instrucciones claras para resolver problemas

---

## 🔄 AUTOMATIZACIÓN

### Google Sheets → GitHub
- ✅ Sincronización automática cada hora
- ✅ Detección inteligente de cambios
- ✅ Exportación automática a JSON
- ✅ Push automático a GitHub
- ✅ Backups en Google Drive

---

## 📊 ESTADÍSTICAS Y MONITOREO

### Información Visible
- ✅ Total de obras en la base de datos
- ✅ Fuente de datos actual (base de datos o JSON)
- ✅ Última actualización de datos
- ✅ Contador de resultados filtrados
- ✅ Contador de comentarios pendientes (admin)
- ✅ Contador de cambios pendientes (admin)

---

## 🛠️ HERRAMIENTAS DE DESARROLLO

### Funciones de Diagnóstico
- ✅ `diagnosticarUsuario()` - Diagnóstico completo del usuario
- ✅ Logs detallados en consola del navegador
- ✅ Verificación de estado de la base de datos
- ✅ Pruebas de conectividad

### Scripts de Mantenimiento
- ✅ Corrección de datos (fuente FUENTESXI)
- ✅ Validación de esquema de datos
- ✅ Migración de datos entre sistemas

---

## 📚 DOCUMENTACIÓN

### Guías Disponibles
- ✅ README completo del sistema
- ✅ Guía de configuración de Google Sheets
- ✅ Documentación de scripts Python
- ✅ FAQ y solución de problemas
- ✅ Guía de roles y permisos

---

## 🎯 RESUMEN POR ROL

### Colaborador
- Ver obras y filtrar
- Exportar a CSV
- Crear comentarios (generales y por obra)
- Ver todos los comentarios públicos

### Editor
- Todo lo de Colaborador +
- Editar campos de obras
- Ver cambios pendientes propios
- Los cambios requieren aprobación del admin

### Admin
- Todo lo de Editor +
- Cambios se aplican inmediatamente
- Gestionar usuarios y roles
- Aprobar/rechazar cambios de editores
- Ver y gestionar logs de errores
- Marcar comentarios como vistos
- Ver contador de comentarios pendientes

---

**Última actualización:** Noviembre 2025


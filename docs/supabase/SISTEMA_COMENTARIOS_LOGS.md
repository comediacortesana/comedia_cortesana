# 💬 Sistema de Comentarios y Logs de Errores

## 📋 Resumen de Funcionalidades Implementadas

Este documento describe el sistema de comentarios mejorado y el sistema de logs de errores que se ha añadido a la aplicación.

### ✅ Funcionalidades Implementadas

1. **Sistema de Comentarios Mejorado**
   - Todos los usuarios autenticados pueden hacer comentarios en los modales de obras
   - Los comentarios son públicos para cualquier usuario logueado
   - Los administradores pueden marcar comentarios como "OK, visto"
   - Los comentarios marcados como vistos se muestran con un badge verde
   - Botón destacado para añadir comentarios en cada modal

2. **Sistema de Logs de Errores**
   - Registro automático de errores cuando falla la carga de datos desde Supabase
   - Los logs incluyen: hora, usuario, tipo de error, mensaje y detalles técnicos
   - Solo los administradores pueden ver los logs de errores
   - Los administradores pueden marcar logs como vistos
   - Panel de administración con sección dedicada a logs de errores

## 🚀 Instrucciones de Instalación

### Paso 1: Ejecutar Script SQL en Supabase

1. Ve a tu proyecto en Supabase: https://supabase.com/dashboard
2. Abre **SQL Editor**
3. Copia y pega el contenido del archivo `supabase_sistema_comentarios_logs.sql`
4. Ejecuta el script (botón "Run" o F5)
5. Verifica que no haya errores

### Paso 2: Verificar que las Tablas se Crearon Correctamente

Ejecuta esta consulta en SQL Editor para verificar:

```sql
-- Verificar campos nuevos en comentarios
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'comentarios' 
AND column_name IN ('visto_por_admin', 'visto_at', 'visto_por');

-- Verificar que la tabla logs_errores existe
SELECT * FROM logs_errores LIMIT 1;
```

### Paso 3: Verificar Políticas RLS

Las políticas RLS deberían haberse creado automáticamente. Verifica con:

```sql
-- Ver políticas de comentarios
SELECT * FROM pg_policies WHERE tablename = 'comentarios';

-- Ver políticas de logs_errores
SELECT * FROM pg_policies WHERE tablename = 'logs_errores';
```

## 📖 Uso del Sistema

### Para Usuarios (Colaboradores, Editores, Admins)

#### Añadir Comentarios

1. Haz clic en cualquier fila de la tabla para abrir el modal de detalles
2. En la sección "💬 Comentarios y Validaciones", verás:
   - Un botón destacado "💬 Añadir Comentario"
   - Un área de texto para escribir tu comentario
   - Todos los comentarios existentes (públicos para usuarios logueados)

3. Escribe tu comentario y haz clic en "Enviar Comentario"
4. El comentario aparecerá inmediatamente en la lista

**Tipos de comentarios que puedes hacer:**
- Sugerencias de mejora en los datos
- Reportar errores o inconsistencias
- Añadir información adicional sobre la obra
- Preguntas sobre los datos

### Para Administradores

#### Marcar Comentarios como Vistos

1. Abre el modal de cualquier obra
2. En la sección de comentarios, verás un botón "✓ OK, visto" en cada comentario no revisado
3. Haz clic en el botón para marcarlo como visto
4. El comentario se actualizará y mostrará un badge verde "✅ OK, visto"

#### Ver Logs de Errores

1. Haz clic en el botón "⚙️ Panel Admin" (solo visible para admins)
2. Desplázate hasta la sección "⚠️ Logs de Errores"
3. Verás una tabla con todos los errores registrados:
   - **Fecha/Hora**: Cuándo ocurrió el error
   - **Usuario**: Qué usuario experimentó el error
   - **Tipo**: Tipo de error (generalmente "carga_datos")
   - **Mensaje**: Descripción del error
   - **Estado**: Si está pendiente o visto
   - **Acción**: Botones para marcar como visto o ver detalles

4. Los errores no vistos aparecen con fondo amarillo
5. Haz clic en "Ver detalles" para ver información técnica completa del error

#### Marcar Logs como Vistos

1. En la tabla de logs, haz clic en "✓ Marcar visto" en cualquier log pendiente
2. El log se marcará como visto y desaparecerá del resumen de pendientes

## 🔍 Estructura de la Base de Datos

### Tabla `comentarios` (actualizada)

```sql
- id (UUID, PK)
- obra_id (INTEGER, FK -> obras.id)
- usuario_id (UUID, FK -> auth.users.id)
- contenido (TEXT)
- tipo (TEXT, default: 'comentario')
- estado (TEXT, default: 'pendiente')
- visto_por_admin (BOOLEAN, default: FALSE) -- NUEVO
- visto_at (TIMESTAMPTZ) -- NUEVO
- visto_por (UUID, FK -> auth.users.id) -- NUEVO
- created_at (TIMESTAMPTZ)
- updated_at (TIMESTAMPTZ)
```

### Tabla `logs_errores` (nueva)

```sql
- id (UUID, PK)
- tipo_error (TEXT, default: 'carga_datos')
- mensaje (TEXT)
- detalles (JSONB)
- usuario_id (UUID, FK -> auth.users.id)
- usuario_email (TEXT)
- url (TEXT)
- user_agent (TEXT)
- created_at (TIMESTAMPTZ)
- visto_por_admin (BOOLEAN, default: FALSE)
- visto_at (TIMESTAMPTZ)
- visto_por (UUID, FK -> auth.users.id)
```

## 🔐 Políticas de Seguridad (RLS)

### Comentarios

- **Lectura**: Pública para usuarios autenticados
- **Creación**: Cualquier usuario autenticado
- **Actualización**: 
  - El propio usuario puede editar sus comentarios
  - Los admins pueden marcar comentarios como vistos

### Logs de Errores

- **Creación**: Cualquier usuario autenticado puede crear logs
- **Lectura**: Solo administradores
- **Actualización**: Solo administradores pueden marcar como vistos

## 🐛 Solución de Problemas

### Los comentarios no se muestran

1. Verifica que estás logueado
2. Verifica que el `obra_id` es válido (consola del navegador)
3. Verifica las políticas RLS en Supabase

### Los logs de errores no aparecen

1. Verifica que eres administrador
2. Verifica que la tabla `logs_errores` existe
3. Verifica las políticas RLS para `logs_errores`

### No puedo marcar comentarios como visto

1. Verifica que eres administrador (rol = 'admin' en `perfiles_usuarios`)
2. Verifica que los campos `visto_por_admin`, `visto_at`, `visto_por` existen en la tabla `comentarios`

### Los errores no se registran automáticamente

1. Verifica que estás logueado cuando ocurre el error
2. Verifica que la tabla `logs_errores` existe
3. Revisa la consola del navegador para ver si hay errores al crear el log

## 📝 Notas Importantes

1. **Los comentarios son públicos**: Cualquier usuario autenticado puede ver todos los comentarios. Esto es intencional para facilitar la colaboración.

2. **Los logs solo se crean si el usuario está autenticado**: Si un usuario no logueado experimenta un error, no se registrará en los logs.

3. **Los logs incluyen información sensible**: Los logs incluyen URLs y user agents. Solo los administradores pueden acceder a esta información.

4. **Rendimiento**: Los logs se crean de forma asíncrona y no bloquean la carga de datos. Si falla la creación del log, no afectará la experiencia del usuario.

## 🔄 Próximas Mejoras Posibles

- Notificaciones por email cuando hay comentarios o errores nuevos
- Filtros avanzados en la tabla de logs
- Exportación de logs a CSV
- Dashboard con estadísticas de comentarios y errores
- Sistema de respuestas a comentarios (threading)

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias, puedes:
1. Dejar un comentario en cualquier obra
2. Revisar los logs de errores en el panel de administración
3. Verificar la consola del navegador para errores técnicos


# 📝 Guía del Sistema de Edición con Supabase

## 🎯 Resumen

Sistema completo de edición de datos con aprobación de administradores usando Supabase como base de datos intermedia.

## 🔄 Flujo del Sistema

```
1. Editor hace cambios en la interfaz
   ↓
2. Cambios se guardan en Supabase (tabla cambios_pendientes)
   ↓
3. Admin revisa y aprueba cambios en Panel Admin
   ↓
4. Apps Script sincroniza cambios aprobados con GitHub
   ↓
5. GitHub Pages se actualiza automáticamente
```

## 📋 Paso 1: Configurar Supabase

### 1.1 Ejecutar el script SQL

1. Ve a tu proyecto en Supabase: https://supabase.com/dashboard
2. Abre el **SQL Editor**
3. Ejecuta el archivo `supabase_cambios_pendientes.sql` completo
4. Verifica que la tabla `cambios_pendientes` se creó correctamente

### 1.2 Verificar políticas RLS

Las políticas de seguridad (RLS) ya están incluidas en el script:
- ✅ Cualquier usuario autenticado puede crear cambios
- ✅ Solo el creador puede editar sus cambios pendientes
- ✅ Solo admins pueden aprobar/rechazar cambios
- ✅ Todos pueden ver cambios (lectura pública)

## 📋 Paso 2: Usar el Sistema

### Para Editores

1. **Iniciar sesión** con tu cuenta
2. **Activar "Modo Edición"** (botón verde)
3. **Editar campos** haciendo clic en "✏️ Editar" en cualquier campo
4. Los cambios se guardan automáticamente en Supabase
5. Ver tus cambios pendientes con "Ver Cambios"

### Para Administradores

1. **Abrir "Panel Admin"** (botón morado)
2. **Ir a la sección "Cambios Pendientes"**
3. **Revisar cada cambio:**
   - Ver qué campo cambió
   - Ver valor anterior vs nuevo
   - Ver quién hizo el cambio
4. **Aprobar o Rechazar** cada cambio
5. Los cambios aprobados se sincronizarán con GitHub automáticamente

## 📋 Paso 3: Sincronizar con GitHub (Apps Script)

### 3.1 Crear el script de sincronización

El script debe:
1. Leer cambios aprobados de Supabase
2. Aplicarlos al JSON local
3. Hacer commit a GitHub
4. Actualizar `datos_obras.json`

### 3.2 Ejemplo de código Apps Script

```javascript
function sincronizarCambiosAprobados() {
  // 1. Conectar a Supabase y obtener cambios aprobados
  const cambiosAprobados = obtenerCambiosAprobados();
  
  // 2. Cargar datos_obras.json actual
  const datosActuales = cargarJSONDesdeGitHub();
  
  // 3. Aplicar cambios aprobados
  cambiosAprobados.forEach(cambio => {
    const obra = datosActuales.obras.find(o => String(o.id) === String(cambio.obra_id));
    if (obra) {
      obra[cambio.campo] = cambio.valor_nuevo;
    }
  });
  
  // 4. Actualizar metadata
  datosActuales.metadata.ultima_sincronizacion = new Date().toISOString();
  datosActuales.metadata.cambios_aplicados = cambiosAprobados.length;
  
  // 5. Hacer commit a GitHub
  hacerCommitAGitHub(datosActuales);
  
  // 6. Marcar cambios como sincronizados (opcional)
  marcarCambiosSincronizados(cambiosAprobados.map(c => c.id));
}
```

## 🔍 Estructura de la Tabla `cambios_pendientes`

```sql
CREATE TABLE cambios_pendientes (
    id UUID PRIMARY KEY,
    obra_id TEXT NOT NULL,           -- ID de la obra
    campo TEXT NOT NULL,             -- Nombre del campo (ej: 'titulo')
    valor_anterior TEXT,              -- Valor antes del cambio
    valor_nuevo TEXT NOT NULL,        -- Nuevo valor propuesto
    usuario_id UUID NOT NULL,         -- Usuario que hizo el cambio
    estado TEXT DEFAULT 'pendiente',  -- 'pendiente', 'aprobado', 'rechazado'
    revisado_por UUID,               -- Admin que revisó (si aplica)
    revisado_at TIMESTAMPTZ,         -- Fecha de revisión
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 📊 Estados de los Cambios

- **pendiente**: Cambio propuesto, esperando aprobación
- **aprobado**: Cambio aprobado por admin, listo para sincronizar
- **rechazado**: Cambio rechazado por admin

## 🔐 Seguridad

- ✅ Solo usuarios autenticados pueden crear cambios
- ✅ Solo admins pueden aprobar/rechazar
- ✅ Row Level Security (RLS) activado
- ✅ Historial completo de quién hizo qué y cuándo

## 🚨 Troubleshooting

### Error: "No se pudo guardar en Supabase"
- Verifica que ejecutaste el script SQL completo
- Verifica que estás autenticado
- Revisa la consola del navegador para más detalles

### Los cambios no aparecen en el Panel Admin
- Verifica que eres admin (rol = 'admin')
- Verifica que los cambios tienen estado 'pendiente'
- Recarga el panel admin

### Los cambios aprobados no se sincronizan
- Verifica que el Apps Script está configurado correctamente
- Verifica que tiene permisos de escritura en GitHub
- Revisa los logs del Apps Script

## 📚 Archivos Relacionados

- `supabase_cambios_pendientes.sql` - Script SQL para crear la tabla
- `index.html` - Código frontend con funciones de edición
- `sheets-github-sync.gs` - Apps Script base (necesita adaptación)

## 🎉 Próximos Pasos

1. ✅ Configurar Supabase (ejecutar SQL)
2. ✅ Probar edición como Editor
3. ✅ Probar aprobación como Admin
4. ⏳ Configurar Apps Script para sincronización automática
5. ⏳ Configurar trigger para ejecutar sincronización periódicamente


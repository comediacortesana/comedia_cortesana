# Solución para Timeout en Consultas de Supabase

## Problema
Las consultas a Supabase se quedan colgadas (timeout) y no se resuelven, impidiendo que se cargue el rol del usuario.

## Causas Posibles

1. **Políticas RLS (Row Level Security) bloqueando las consultas**
2. **Problema de CORS o configuración de red**
3. **Problema con el cliente de Supabase**
4. **Problema de conexión a Supabase**

## Soluciones Implementadas

### 1. Timeout con Fallback a Fetch Directo
Se ha añadido un sistema de timeout (8 segundos) que, si la consulta falla, automáticamente intenta usar `fetch` directo a la API REST de Supabase.

### 2. Configuración Mejorada del Cliente
Se ha añadido configuración adicional al cliente de Supabase:
- Headers con `apikey`
- Esquema de base de datos explícito

### 3. Script SQL para Verificar/Arreglar RLS
Ejecuta el script `supabase_fix_rls_perfiles.sql` en Supabase para asegurar que las políticas RLS están correctas.

## Pasos para Solucionar

### Paso 1: Verificar Políticas RLS en Supabase

1. Ve a tu proyecto en Supabase
2. Abre el **SQL Editor**
3. Ejecuta este query para ver las políticas actuales:

```sql
SELECT policyname, cmd, qual, with_check
FROM pg_policies
WHERE tablename = 'perfiles_usuarios';
```

Deberías ver al menos una política de `SELECT` con `qual: true` (lectura pública).

### Paso 2: Ejecutar Script de Fix RLS

Ejecuta el contenido completo de `supabase_fix_rls_perfiles.sql` en el SQL Editor de Supabase.

Este script:
- Elimina todas las políticas existentes
- Crea políticas nuevas y correctas
- Habilita RLS
- Verifica que todo está bien

### Paso 3: Probar en el Navegador

1. Recarga la página completamente (Ctrl+Shift+R o Cmd+Shift+R)
2. Inicia sesión
3. Abre la consola del navegador (F12)
4. Ejecuta: `recargarRol()`

Deberías ver:
- Si funciona con el cliente de Supabase: `✅ Rol obtenido: admin`
- Si usa fetch directo: `🌐 Usando fetch directo...` seguido de `✅ Rol obtenido via fetch: admin`

### Paso 4: Verificar en Supabase

1. Ve a **Table Editor** → `perfiles_usuarios`
2. Busca tu usuario por email o ID
3. Verifica que el campo `rol` está en `admin` (o el rol que quieras)

## Solución Temporal: Deshabilitar RLS (SOLO PARA DEBUG)

⚠️ **ADVERTENCIA**: Solo para pruebas, NO para producción.

Si necesitas probar rápidamente si el problema es RLS:

```sql
ALTER TABLE perfiles_usuarios DISABLE ROW LEVEL SECURITY;
```

Si después de esto funciona, el problema es definitivamente RLS. Luego vuelve a habilitarlo:

```sql
ALTER TABLE perfiles_usuarios ENABLE ROW LEVEL SECURITY;
```

Y ejecuta el script `supabase_fix_rls_perfiles.sql` para arreglar las políticas.

## Verificar que Funciona

Ejecuta en la consola del navegador:

```javascript
// Verificar rol actual
console.log('Rol:', rolUsuario);
console.log('Es admin:', esAdmin);

// Recargar rol
await recargarRol();

// Diagnosticar
diagnosticarUsuario();
```

## Si Nada Funciona

1. **Verifica las credenciales de Supabase**:
   - URL correcta: `https://kyxxpoewwjixbpcezays.supabase.co`
   - Anon key correcta

2. **Verifica la conexión a internet**:
   - Prueba acceder a `https://kyxxpoewwjixbpcezays.supabase.co` en el navegador

3. **Verifica CORS**:
   - Abre la consola del navegador
   - Busca errores de CORS en la pestaña Network

4. **Contacta con Soporte de Supabase**:
   - Si el problema persiste, puede ser un problema del servicio

## Archivos Relacionados

- `index.html`: Código principal con las funciones mejoradas
- `supabase_fix_rls_perfiles.sql`: Script SQL para arreglar políticas RLS
- `CAMBIAR_ROL_USUARIO.md`: Guía para cambiar roles de usuario


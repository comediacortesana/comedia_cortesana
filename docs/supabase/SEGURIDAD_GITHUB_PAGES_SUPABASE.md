# 🔒 Seguridad: GitHub Pages + Supabase

## 📋 Resumen Ejecutivo

Este documento analiza la seguridad del proyecto cuando se despliega en **GitHub Pages** (que requiere repositorios públicos) y usa **Supabase** como backend.

**Estado actual:** ✅ **Básicamente seguro**, pero con algunas mejoras recomendadas.

---

## ✅ Lo que ESTÁ BIEN (y por qué es seguro)

### 1. Uso correcto de la `anon key` en el frontend

```672:673:comedia_cortesana/index.html
        const SUPABASE_URL = 'https://kyxxpoewwjixbpcezays.supabase.co';
        const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';
```

✅ **Correcto**: La `anon key` está diseñada para ser pública. Está bien tenerla en el código del frontend.

### 2. `service_role` key NO está en el código

✅ **Correcto**: La `service_role` key solo se usa en:
- **Apps Script** (guardada en `PropertiesService`, no en el código)
- **Scripts Python** (desde `.env`, que está en `.gitignore`)

### 3. RLS está habilitado en todas las tablas

```132:137:supabase_schema.sql
-- Habilitar RLS
ALTER TABLE obras ENABLE ROW LEVEL SECURITY;
ALTER TABLE comentarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE validaciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE historial_validaciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE perfiles_usuarios ENABLE ROW LEVEL SECURITY;
```

✅ **Correcto**: Row Level Security está activo.

---

## ⚠️ Problemas Potenciales Identificados

### Problema 1: Admins haciendo UPDATE directo en `obras` desde el frontend

**Ubicación del código:**

```1993:1996:comedia_cortesana/index.html
                    const { error: errorUpdate } = await supabase
                        .from('obras')
                        .update(updateData)
                        .eq('id', obraIdStr);
```

**Problema:**
- Los administradores están haciendo `UPDATE` directo en la tabla `obras` desde el frontend
- Las políticas RLS actuales solo permiten `SELECT` público en `obras`
- **No hay política RLS que permita UPDATE en `obras` con la `anon key`**

**¿Por qué funciona actualmente?**
- Posiblemente las políticas RLS no están aplicadas correctamente, O
- Hay alguna política que permite esto pero no está documentada

**Riesgo:**
- Si alguien obtiene la `anon key` (que es pública), podría intentar hacer UPDATEs
- Sin RLS adecuado, esto podría ser un problema

### Problema 2: Falta política RLS para UPDATE en `obras`

**Estado actual de políticas RLS para `obras`:**

```143:147:supabase_schema.sql
-- OBRAS: Lectura pública
DROP POLICY IF EXISTS "obras_lectura_publica" ON obras;
CREATE POLICY "obras_lectura_publica"
ON obras FOR SELECT
USING (true);
```

**Falta:**
- Política para `UPDATE` en `obras` que verifique que el usuario es admin
- Política para `INSERT` en `obras` (si se necesita)
- Política para `DELETE` en `obras` (si se necesita)

---

## 🔧 Soluciones Recomendadas

### Solución 1: Agregar políticas RLS para admins (RECOMENDADO)

**Ventajas:**
- Mantiene la arquitectura actual
- No requiere cambios en el código del frontend
- Más simple de implementar

**Implementación:**

Ejecuta este SQL en Supabase SQL Editor:

```sql
-- ============================================================================
-- POLÍTICAS RLS PARA OBRAS: Permitir UPDATE solo a admins
-- ============================================================================

-- Política para UPDATE: Solo admins pueden actualizar obras
DROP POLICY IF EXISTS "obras_update_admin" ON obras;
CREATE POLICY "obras_update_admin"
ON obras FOR UPDATE
USING (
    EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    )
)
WITH CHECK (
    EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    )
);

-- Política para INSERT: Solo admins pueden insertar obras
-- (Opcional: si necesitas que admins puedan crear obras desde el frontend)
DROP POLICY IF EXISTS "obras_insert_admin" ON obras;
CREATE POLICY "obras_insert_admin"
ON obras FOR INSERT
WITH CHECK (
    EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    )
);

-- Política para DELETE: Solo admins pueden eliminar obras
-- (Opcional: si necesitas que admins puedan eliminar obras)
DROP POLICY IF EXISTS "obras_delete_admin" ON obras;
CREATE POLICY "obras_delete_admin"
ON obras FOR DELETE
USING (
    EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    )
);
```

**Cómo funciona:**
1. El usuario debe estar autenticado (`auth.uid()` existe)
2. Debe tener un perfil en `perfiles_usuarios` con `rol = 'admin'`
3. Solo entonces puede hacer UPDATE/INSERT/DELETE

**Verificación:**
- Usuario no autenticado → ❌ No puede hacer UPDATE
- Usuario autenticado pero no admin → ❌ No puede hacer UPDATE
- Usuario autenticado y admin → ✅ Puede hacer UPDATE

---

### Solución 2: Mover operaciones privilegiadas a Supabase Edge Functions

**Cuándo usar esta solución:**
- Si necesitas operaciones más complejas que requieren validación adicional
- Si quieres tener más control sobre qué puede hacer un admin
- Si necesitas logging/auditoría más detallado

**Ventajas:**
- Lógica del lado servidor (más segura)
- Puedes usar `service_role` key dentro de la función
- Más control sobre las operaciones

**Desventajas:**
- Requiere escribir código TypeScript/JavaScript para Edge Functions
- Más complejo de mantener

**Ejemplo de Edge Function:**

1. **Crear función en Supabase:**

```typescript
// supabase/functions/update-obra/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  try {
    // Obtener token del usuario
    const authHeader = req.headers.get('Authorization')
    if (!authHeader) {
      return new Response(JSON.stringify({ error: 'No autorizado' }), { 
        status: 401 
      })
    }

    // Crear cliente con service_role para verificar permisos
    const supabaseAdmin = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    // Verificar que el usuario es admin
    const token = authHeader.replace('Bearer ', '')
    const { data: { user }, error: authError } = await supabaseAdmin.auth.getUser(token)
    
    if (authError || !user) {
      return new Response(JSON.stringify({ error: 'No autorizado' }), { 
        status: 401 
      })
    }

    // Verificar rol de admin
    const { data: perfil } = await supabaseAdmin
      .from('perfiles_usuarios')
      .select('rol')
      .eq('id', user.id)
      .single()

    if (perfil?.rol !== 'admin') {
      return new Response(JSON.stringify({ error: 'No tienes permisos de admin' }), { 
        status: 403 
      })
    }

    // Obtener datos del request
    const { obra_id, updateData } = await req.json()

    // Actualizar obra
    const { data, error } = await supabaseAdmin
      .from('obras')
      .update(updateData)
      .eq('id', obra_id)
      .select()
      .single()

    if (error) {
      return new Response(JSON.stringify({ error: error.message }), { 
        status: 400 
      })
    }

    return new Response(JSON.stringify({ success: true, data }), {
      headers: { 'Content-Type': 'application/json' },
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), { 
      status: 500 
    })
  }
})
```

2. **Llamar desde el frontend:**

```javascript
// En lugar de:
await supabase.from('obras').update(updateData).eq('id', obraIdStr)

// Usar:
const { data, error } = await supabase.functions.invoke('update-obra', {
  body: { obra_id: obraIdStr, updateData }
})
```

**Nota:** Esta solución es más compleja y solo necesaria si la Solución 1 no es suficiente.

---

## 🛡️ Checklist de Seguridad

### ✅ Verificaciones Actuales

- [x] Solo `anon key` en el código del frontend
- [x] `service_role` key NO está en el código
- [x] RLS habilitado en todas las tablas
- [x] Políticas RLS para lectura pública donde corresponde
- [x] Políticas RLS para usuarios autenticados donde corresponde

### ⚠️ Verificaciones Pendientes

- [ ] **CRÍTICO**: Agregar política RLS para UPDATE en `obras` (solo admins)
- [ ] Verificar que las políticas RLS están funcionando correctamente
- [ ] Probar que usuarios no-admin NO pueden hacer UPDATE en `obras`
- [ ] Considerar agregar políticas para INSERT/DELETE si se necesitan

---

## 📚 Conceptos Clave de Seguridad

### ¿Por qué la `anon key` es segura aunque sea pública?

1. **RLS protege los datos**: Aunque cualquiera tenga la `anon key`, las políticas RLS determinan qué puede hacer cada usuario
2. **Autenticación separada**: Los usuarios deben autenticarse con `supabase.auth.signIn()` para obtener un token JWT
3. **Token JWT**: Cada request incluye el token del usuario, que Supabase verifica
4. **Políticas RLS usan `auth.uid()`**: Las políticas verifican quién es el usuario autenticado

### ¿Por qué NO debes "encriptar" la `anon key` en el frontend?

**NO funciona:**
```javascript
// ❌ MAL: Esto NO es seguro
const encryptedKey = "aGVsbG8gd29ybGQ=" // base64 encoded
const SUPABASE_ANON_KEY = atob(encryptedKey) // Cualquiera puede decodificar
```

**Razones:**
1. El código JavaScript siempre es visible en el navegador
2. Cualquiera puede ver el código fuente y decodificar
3. No añade seguridad real
4. Solo añade complejidad innecesaria

**Lo correcto:**
- Usar la `anon key` directamente (está diseñada para ser pública)
- Confiar en RLS para proteger los datos
- Usar `service_role` key solo en el backend (Edge Functions, Apps Script, etc.)

---

## 🔍 Verificación de Políticas RLS

### Cómo verificar que las políticas están funcionando:

1. **En Supabase Dashboard:**
   - Ve a "Authentication" → "Policies"
   - Verifica que todas las tablas tienen políticas activas

2. **Probar manualmente:**
   ```sql
   -- En Supabase SQL Editor, ejecuta:
   SELECT 
       schemaname,
       tablename,
       policyname,
       cmd,  -- SELECT, INSERT, UPDATE, DELETE
       qual  -- Condición USING
   FROM pg_policies
   WHERE tablename = 'obras'
   ORDER BY cmd;
   ```

3. **Probar desde el frontend:**
   - Abre la consola del navegador
   - Intenta hacer UPDATE sin estar autenticado → Debe fallar
   - Intenta hacer UPDATE como usuario no-admin → Debe fallar
   - Intenta hacer UPDATE como admin → Debe funcionar

---

## 📝 Recomendaciones Finales

### Prioridad ALTA (Hacer ahora):

1. **Agregar política RLS para UPDATE en `obras`** (Solución 1)
   - Ejecuta el SQL proporcionado arriba
   - Verifica que funciona correctamente

2. **Verificar que no hay `service_role` key en el código**
   - Busca en todo el repositorio: `grep -r "service_role" .`
   - Asegúrate de que solo está en Apps Script (PropertiesService) y scripts Python (.env)

### Prioridad MEDIA (Considerar):

3. **Agregar políticas para INSERT/DELETE si se necesitan**
   - Solo si planeas permitir estas operaciones desde el frontend

4. **Considerar Edge Functions para operaciones complejas**
   - Solo si necesitas lógica más compleja o validaciones adicionales

### Prioridad BAJA (Opcional):

5. **Documentar todas las políticas RLS**
   - Crear un documento que explique cada política y por qué existe

6. **Agregar logging/auditoría**
   - Registrar quién hace qué cambios y cuándo

---

## 🎯 Conclusión

**Tu proyecto está básicamente seguro**, pero necesita una mejora importante:

✅ **Lo que está bien:**
- Uso correcto de `anon key` en el frontend
- `service_role` key no está expuesta
- RLS está habilitado

⚠️ **Lo que falta:**
- Política RLS para UPDATE en `obras` que verifique que el usuario es admin

**Acción inmediata:** Ejecuta el SQL de la Solución 1 para agregar la política RLS faltante.

---

## 📖 Referencias

- [Supabase RLS Documentation](https://supabase.com/docs/guides/auth/row-level-security)
- [Supabase Security Best Practices](https://supabase.com/docs/guides/auth/security)
- [Supabase Edge Functions](https://supabase.com/docs/guides/functions)









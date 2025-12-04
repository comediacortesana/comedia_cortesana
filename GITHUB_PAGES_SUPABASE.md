# GitHub Pages y Supabase: Posibles Problemas y Soluciones

## ¿GitHub Pages Bloquea Supabase?

**Respuesta corta:** NO, GitHub Pages NO bloquea las consultas a Supabase. GitHub Pages solo sirve archivos estáticos (HTML, CSS, JS) y no intercepta las llamadas HTTP que hace tu JavaScript al navegador.

## ¿Entonces Cuál Es el Problema?

Si estás experimentando timeouts en las consultas a Supabase, las causas más probables son:

### 1. **Políticas RLS (Row Level Security) en Supabase** ⚠️ MÁS PROBABLE
Las políticas RLS pueden estar bloqueando las consultas sin devolver un error claro, causando que se queden colgadas.

**Solución:** Ejecuta `supabase_fix_rls_perfiles.sql` en Supabase.

### 2. **Problema de CORS**
Aunque Supabase debería tener CORS configurado correctamente, podría haber un problema.

**Solución:** Verifica en la consola del navegador si hay errores de CORS:
```javascript
// En la consola del navegador
fetch('https://kyxxpoewwjixbpcezays.supabase.co/rest/v1/perfiles_usuarios', {
    headers: {
        'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
        'Content-Type': 'application/json'
    }
}).then(r => r.json()).then(console.log).catch(console.error);
```

### 3. **Content Security Policy (CSP)**
Si GitHub Pages añade headers CSP restrictivos, podría bloquear las conexiones.

**Solución:** Verifica los headers de respuesta:
```javascript
// En la consola del navegador
fetch(window.location.href).then(r => {
    console.log('CSP Headers:', r.headers.get('content-security-policy'));
});
```

### 4. **Problema de Red/Firewall**
Tu red o firewall podría estar bloqueando las conexiones a Supabase.

**Solución:** Prueba desde otra red o con VPN.

### 5. **Problema con el Cliente de Supabase**
El cliente JavaScript de Supabase podría tener un bug o incompatibilidad.

**Solución:** Ya implementada - usar `fetch` directo como alternativa.

## Diferencias: Localhost vs GitHub Pages

### Localhost (http://127.0.0.1:5500)
- ✅ No hay restricciones de CORS
- ✅ No hay CSP de GitHub
- ✅ Acceso directo a recursos locales
- ⚠️ Si falla aquí, el problema NO es GitHub Pages

### GitHub Pages (https://comediacortesana.github.io)
- ⚠️ Puede tener CSP headers
- ⚠️ Puede tener restricciones de red
- ✅ Pero NO bloquea llamadas HTTP del navegador

## Cómo Diagnosticar

### Paso 1: Verificar en Localhost
Si el problema ocurre en localhost (`http://127.0.0.1:5500`), **NO es GitHub Pages**.

### Paso 2: Verificar en GitHub Pages
1. Despliega tu código a GitHub Pages
2. Abre la consola del navegador (F12)
3. Ve a la pestaña **Network**
4. Intenta iniciar sesión
5. Busca las llamadas a `kyxxpoewwjixbpcezays.supabase.co`
6. Verifica:
   - ¿Se hacen las llamadas? (deberían aparecer en Network)
   - ¿Qué status code tienen? (200, 401, 403, etc.)
   - ¿Hay errores de CORS? (aparecerán en rojo)

### Paso 3: Comparar Localhost vs GitHub Pages
Si funciona en localhost pero NO en GitHub Pages:
- Problema de CSP o headers de GitHub Pages
- Problema de red específico de GitHub Pages

Si NO funciona en ninguno:
- Problema de RLS en Supabase (más probable)
- Problema de configuración de Supabase
- Problema de red general

## Soluciones Específicas

### Si el Problema Es RLS (Más Probable)

Ejecuta en Supabase SQL Editor:

```sql
-- Verificar políticas actuales
SELECT policyname, cmd, qual, with_check
FROM pg_policies
WHERE tablename = 'perfiles_usuarios';

-- Si no hay política de lectura pública, crearla
CREATE POLICY "perfiles_lectura_publica"
ON perfiles_usuarios FOR SELECT
USING (true);
```

### Si el Problema Es CORS

Verifica en Supabase:
1. Ve a **Settings** → **API**
2. Verifica que **CORS** está habilitado
3. Añade tu dominio de GitHub Pages a las URLs permitidas:
   - `https://comediacortesana.github.io`
   - `https://*.github.io` (para todos los subdominios)

### Si el Problema Es CSP

Añade un meta tag en `index.html`:

```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self' https://kyxxpoewwjixbpcezays.supabase.co https://cdn.jsdelivr.net; 
               script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; 
               connect-src 'self' https://kyxxpoewwjixbpcezays.supabase.co;">
```

⚠️ **Nota:** Esto solo funciona si GitHub Pages NO sobrescribe los headers CSP.

## Solución Implementada: Fetch Directo

Ya hemos implementado una solución que usa `fetch` directo cuando el cliente de Supabase falla. Esto debería funcionar incluso si hay problemas con el cliente.

La función `obtenerRolConFetchDirecto()` hace una llamada HTTP directa a la API REST de Supabase, evitando posibles problemas con el cliente JavaScript.

## Prueba Rápida

Ejecuta esto en la consola del navegador (tanto en localhost como en GitHub Pages):

```javascript
// Prueba 1: Cliente Supabase
console.log('Probando cliente Supabase...');
const { data, error } = await supabase
    .from('perfiles_usuarios')
    .select('*')
    .limit(1);
console.log('Cliente:', { data, error });

// Prueba 2: Fetch directo
console.log('Probando fetch directo...');
const response = await fetch('https://kyxxpoewwjixbpcezays.supabase.co/rest/v1/perfiles_usuarios?limit=1', {
    headers: {
        'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt5eHhwb2V3d2ppeGJwY2V6YXlzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MjAzMDksImV4cCI6MjA3Nzk5NjMwOX0.sIw7flVHQ00r3VwrhU7tvohVzKpb7LGtXVzG43FAP10',
        'Content-Type': 'application/json'
    }
});
const fetchData = await response.json();
console.log('Fetch:', { status: response.status, data: fetchData });
```

Compara los resultados:
- Si ambos fallan: Problema de RLS o configuración de Supabase
- Si solo el cliente falla: Problema con el cliente de Supabase
- Si solo fetch falla: Problema de CORS o red

## Conclusión

**GitHub Pages NO bloquea Supabase**, pero puede haber otros problemas:
1. ✅ RLS en Supabase (más probable) → Ejecuta `supabase_fix_rls_perfiles.sql`
2. ✅ CORS → Verifica configuración en Supabase
3. ✅ CSP → Añade meta tag si es necesario
4. ✅ Cliente de Supabase → Ya tenemos fallback con fetch directo

La solución implementada con `fetch` directo debería funcionar incluso si hay problemas con el cliente de Supabase.


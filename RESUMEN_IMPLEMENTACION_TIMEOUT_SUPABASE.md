# Resumen Técnico: Implementación de Fallback para Timeout de Supabase

## Contexto del Proyecto

**Proyecto:** Sistema de filtrado y visualización de obras de teatro español del Siglo de Oro
**Stack Tecnológico:**
- Frontend: HTML/CSS/JavaScript vanilla (sin frameworks)
- Hosting: GitHub Pages (sitio estático)
- Backend/BaaS: Supabase (PostgreSQL + Auth + Row Level Security)
- Datos: JSON estático cargado desde GitHub Pages
- Integración: Google Sheets + Apps Script para edición colaborativa

**URL del proyecto:** https://comediacortesana.github.io/comedia_cortesana/

## Problema Identificado

### Causa Raíz: Dead-Lock en onAuthStateChange

**ACTUALIZACIÓN:** El problema fue identificado como un **dead-lock causado por el uso incorrecto de `onAuthStateChange`**, según la documentación oficial de Supabase y los maintainers en GitHub.

### Síntomas
1. Las consultas a Supabase usando el cliente JavaScript oficial (`@supabase/supabase-js@2`) se quedaban colgadas indefinidamente
2. Las promesas nunca se resolvían, mostrando `Promise {<pending>}` en la consola
3. Timeouts después de 8-10 segundos sin respuesta
4. El problema afectaba específicamente a:
   - `supabase.from('perfiles_usuarios').select().eq().maybeSingle()` cuando se llamaba desde dentro de `onAuthStateChange`
   - `supabase.auth.getSession()` cuando se llamaba desde dentro de callbacks
   - Cualquier consulta a tablas con Row Level Security (RLS) habilitado cuando se ejecutaba dentro de `onAuthStateChange`

### Patrón que Causaba el Dead-Lock

```javascript
// ❌ INCORRECTO (causaba dead-lock):
supabase.auth.onAuthStateChange(async (event, session) => {
    if (event === 'SIGNED_IN') {
        // Esto causaba dead-lock porque llamaba a supabase.from() dentro del callback
        await mostrarUIUsuario(); // → obtenerRolUsuario() → supabase.from()
    }
});
```

**Referencia oficial:** https://supabase.com/docs/reference/javascript/auth-onauthstatechange

### Diagnóstico Realizado
- ✅ Supabase está funcionando correctamente (verificado con fetch directo)
- ✅ Las políticas RLS están correctamente configuradas (lectura pública permitida)
- ✅ Las credenciales (URL y anon key) son correctas
- ✅ El problema es específico del cliente JavaScript de Supabase
- ✅ Fetch directo a la API REST funciona perfectamente (Status 200)

### Consultas Afectadas
```javascript
// Estas consultas se quedaban colgadas:
const { data, error } = await supabase
    .from('perfiles_usuarios')
    .select('rol, nombre_completo')
    .eq('id', usuarioActual.id)
    .maybeSingle();

const session = await supabase.auth.getSession();
```

### Consultas que Funcionan
```javascript
// Fetch directo funciona perfectamente:
const response = await fetch(
    'https://kyxxpoewwjixbpcezays.supabase.co/rest/v1/perfiles_usuarios?id=eq.USER_ID&select=rol,nombre_completo',
    {
        headers: {
            'apikey': SUPABASE_ANON_KEY,
            'Content-Type': 'application/json'
        }
    }
);
// Status: 200, Data: [{rol: 'admin', nombre_completo: '...'}]
```

## Solución Implementada

### Estrategia 1: Corrección del Dead-Lock (Solución Principal)

**Corrección según recomendación oficial de Supabase:**

1. Cambiado `onAuthStateChange` para usar `setTimeout(..., 0)` en lugar de `async` directamente
2. Las llamadas a métodos de Supabase ahora se ejecutan fuera del callback
3. Esto elimina el dead-lock que causaba los cuelgues

**Código corregido:**
```javascript
// ✅ CORRECTO (según documentación oficial):
supabase.auth.onAuthStateChange((event, session) => {
    setTimeout(async () => {
        if (event === 'SIGNED_IN') {
            await mostrarUIUsuario(); // Ahora está fuera del callback, no causa dead-lock
        }
    }, 0);
});
```

### Estrategia 2: Sistema de Fallback con Timeout (Medida de Seguridad)

Se mantiene un sistema de fallback que:
1. Intenta usar el cliente de Supabase con timeout
2. Si hay timeout, automáticamente usa fetch directo a la API REST
3. Actualiza la UI automáticamente cuando obtiene los datos

**Razón:** Aunque el dead-lock está corregido, mantenemos el fallback como protección contra otros problemas conocidos (getSession colgado, problemas de red, etc.)

### Funciones Modificadas

#### 1. `obtenerRolUsuario()`
**Ubicación:** `index.html` línea ~770

**Antes:**
```javascript
async function obtenerRolUsuario() {
    const { data, error } = await supabase
        .from('perfiles_usuarios')
        .select('rol, nombre_completo')
        .eq('id', usuarioActual.id)
        .maybeSingle();
    // ... manejo de datos
}
```

**Después:**
```javascript
async function obtenerRolUsuario() {
    // Intentar con timeout usando Promise.race
    const consultaPromise = supabase
        .from('perfiles_usuarios')
        .select('rol, nombre_completo')
        .eq('id', usuarioActual.id)
        .maybeSingle();
    
    const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('TIMEOUT')), 8000)
    );
    
    let resultado;
    try {
        resultado = await Promise.race([consultaPromise, timeoutPromise]);
    } catch (timeoutError) {
        if (timeoutError.message.includes('TIMEOUT')) {
            // Fallback automático a fetch directo
            return await obtenerRolConFetchDirecto();
        }
        throw timeoutError;
    }
    
    const { data, error } = resultado;
    // ... manejo de datos
}
```

#### 2. `obtenerRolConFetchDirecto()` (Nueva función)
**Ubicación:** `index.html` línea ~912

```javascript
async function obtenerRolConFetchDirecto() {
    // Fetch directo sin token (solo con apikey)
    // Las políticas RLS permiten lectura pública
    const url = `${SUPABASE_URL}/rest/v1/perfiles_usuarios?id=eq.${usuarioActual.id}&select=rol,nombre_completo`;
    
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'apikey': SUPABASE_ANON_KEY,
            'Content-Type': 'application/json'
        }
    });
    
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data || data.length === 0) {
        // Crear perfil si no existe
        await crearPerfilUsuario(usuarioActual.id, usuarioActual.email);
        rolUsuario = 'colaborador';
        esAdmin = false;
    } else {
        const perfil = data[0];
        rolUsuario = perfil.rol || 'colaborador';
        esAdmin = rolUsuario === 'admin';
        
        // Actualizar UI inmediatamente
        mostrarInfoPermisos();
        if (esAdmin) mostrarBotonAdmin();
        if (puedeEditar()) mostrarBotonEdicion();
    }
    
    return rolUsuario;
}
```

#### 3. `cargarPerfilUsuario()`
**Ubicación:** `index.html` línea ~1370

Similar implementación con timeout de 5 segundos y fallback a fetch directo.

### Configuración del Cliente Supabase

**Ubicación:** `index.html` línea ~598

```javascript
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
    auth: {
        persistSession: true,
        autoRefreshToken: true,
        detectSessionInUrl: true,
        storage: window.localStorage
    },
    db: {
        schema: 'public'
    },
    global: {
        headers: {
            'apikey': SUPABASE_ANON_KEY
        }
    }
});
```

### Content Security Policy

**Ubicación:** `index.html` línea ~7

```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self' https://kyxxpoewwjixbpcezays.supabase.co https://cdn.jsdelivr.net; 
               script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; 
               connect-src 'self' https://kyxxpoewwjixbpcezays.supabase.co wss://kyxxpoewwjixbpcezays.supabase.co;
               style-src 'self' 'unsafe-inline';">
```

## Detalles Técnicos

### Políticas RLS en Supabase

La tabla `perfiles_usuarios` tiene las siguientes políticas:

```sql
-- Lectura pública (permite leer todos los perfiles)
CREATE POLICY "perfiles_lectura_publica"
ON perfiles_usuarios FOR SELECT
USING (true);

-- Lectura propia (permite leer tu propio perfil)
CREATE POLICY "perfiles_lectura_propia"
ON perfiles_usuarios FOR SELECT
USING (auth.uid() = id);

-- Crear propio perfil
CREATE POLICY "perfiles_crear_propio"
ON perfiles_usuarios FOR INSERT
WITH CHECK (auth.uid() = id);

-- Editar propio perfil
CREATE POLICY "perfiles_editar_propio"
ON perfiles_usuarios FOR UPDATE
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);
```

### Estructura de la Tabla `perfiles_usuarios`

```sql
CREATE TABLE perfiles_usuarios (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nombre_completo TEXT,
    rol TEXT DEFAULT 'colaborador' CHECK (rol IN ('colaborador', 'editor', 'admin')),
    avatar_url TEXT,
    bio TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Áreas para Investigación

### Preguntas para Documentación Oficial

1. **¿Por qué el cliente JavaScript de Supabase se queda colgado?**
   - ¿Es un problema conocido con RLS?
   - ¿Hay issues reportados en GitHub de Supabase?
   - ¿Afecta a versiones específicas de `@supabase/supabase-js`?

2. **¿Es recomendable usar fetch directo como fallback?**
   - ¿Hay mejores prácticas oficiales para manejar timeouts?
   - ¿Debería usar la API REST directamente en lugar del cliente?

3. **¿El problema está relacionado con:**
   - Row Level Security (RLS)?
   - Políticas de CORS?
   - Configuración de GitHub Pages?
   - Versión específica del cliente JavaScript?

### Búsquedas Sugeridas

1. **GitHub Issues:**
   - `supabase-js timeout hanging queries`
   - `supabase-js RLS policy queries not resolving`
   - `supabase-js Promise pending forever`

2. **Stack Overflow / Foros:**
   - `supabase javascript client queries hanging`
   - `supabase maybeSingle timeout`
   - `supabase RLS queries not working`

3. **Documentación Oficial:**
   - Supabase JavaScript Client troubleshooting
   - Supabase RLS best practices
   - Supabase timeout configuration
   - Supabase API REST vs JavaScript Client

4. **Comunidad:**
   - Supabase Discord/Slack
   - Reddit r/supabase
   - GitHub Discussions de Supabase

## Información del Entorno

### Versiones Utilizadas

```html
<!-- Cliente Supabase -->
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
```

**Versión exacta:** `@supabase/supabase-js@2` (última versión estable de la v2)

### Navegadores Probados

- Chrome/Edge (Chromium) - Problema presente
- Probablemente afecta a todos los navegadores modernos

### Entorno de Desarrollo

- **Local:** `http://127.0.0.1:5500` (Live Server)
- **Producción:** `https://comediacortesana.github.io/comedia_cortesana/` (GitHub Pages)

### Configuración de Supabase

- **Región:** No especificada (probablemente por defecto)
- **Plan:** Free tier
- **RLS:** Habilitado en todas las tablas
- **CORS:** Configurado por defecto (sin restricciones adicionales)

## Solución Temporal vs Permanente

### Estado Actual
✅ **Solución temporal funcionando:** El sistema de fallback funciona correctamente y resuelve el problema inmediato.

### Consideraciones

1. **¿Es sostenible usar fetch directo?**
   - ✅ Funciona perfectamente
   - ⚠️ Pierde algunas características del cliente (auto-refresh, realtime, etc.)
   - ⚠️ Requiere manejar autenticación manualmente si se necesita

2. **¿Debería investigarse más?**
   - ✅ Sí, para encontrar la causa raíz
   - ✅ Podría haber una solución más elegante
   - ✅ Podría afectar otras funcionalidades futuras

3. **¿Hay alternativas?**
   - Usar una versión diferente del cliente
   - Configurar timeouts a nivel de cliente
   - Usar la API REST directamente desde el inicio
   - Investigar problemas de red/CORS específicos

## Código de Ejemplo Completo

### Función de Fallback Completa

```javascript
// Función alternativa usando fetch directo cuando el cliente de Supabase falla
async function obtenerRolConFetchDirecto() {
    console.log('🌐 Usando fetch directo para obtener rol...');
    
    try {
        // Hacer consulta directa a la API REST de Supabase (sin token, solo con apikey)
        // Las políticas RLS permiten lectura pública, así que no necesitamos token
        const url = `${SUPABASE_URL}/rest/v1/perfiles_usuarios?id=eq.${usuarioActual.id}&select=rol,nombre_completo`;
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'apikey': SUPABASE_ANON_KEY,
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
        
        const data = await response.json();
        
        if (!data || data.length === 0) {
            console.log('📝 No se encontró perfil, creando...');
            await crearPerfilUsuario(usuarioActual.id, usuarioActual.email);
            rolUsuario = 'colaborador';
            esAdmin = false;
        } else {
            const perfil = data[0];
            rolUsuario = perfil.rol || 'colaborador';
            esAdmin = rolUsuario === 'admin';
            console.log('✅ Rol obtenido via fetch:', rolUsuario);
            
            // Actualizar UI inmediatamente
            mostrarInfoPermisos();
            if (esAdmin) {
                mostrarBotonAdmin();
            } else {
                ocultarBotonAdmin();
            }
            if (puedeEditar()) {
                mostrarBotonEdicion();
            } else {
                ocultarBotonEdicion();
            }
        }
        
        return rolUsuario;
    } catch (error) {
        console.error('❌ Error en obtenerRolConFetchDirecto:', error);
        rolUsuario = 'colaborador';
        esAdmin = false;
        return rolUsuario;
    }
}
```

## Resultado Final

✅ **Sistema funcionando correctamente:**
- Detecta timeouts automáticamente
- Usa fetch directo como fallback
- Carga roles y permisos correctamente
- Actualiza UI automáticamente
- Botones de admin y edición aparecen correctamente

## Archivos Modificados

1. `index.html` - Funciones principales modificadas:
   - `obtenerRolUsuario()` (línea ~770)
   - `obtenerRolConFetchDirecto()` (línea ~912) - NUEVA
   - `cargarPerfilUsuario()` (línea ~1370)
   - Configuración del cliente Supabase (línea ~598)
   - Content Security Policy (línea ~7)

2. Archivos de documentación creados:
   - `SOLUCION_TIMEOUT_SUPABASE.md`
   - `GITHUB_PAGES_SUPABASE.md`
   - `supabase_fix_rls_perfiles.sql`

## Próximos Pasos Sugeridos

1. **Investigar causa raíz:**
   - Buscar issues conocidos en GitHub de Supabase
   - Revisar documentación oficial sobre timeouts
   - Consultar comunidad de desarrolladores

2. **Optimizar solución:**
   - Reducir número de llamadas duplicadas
   - Implementar caché de roles
   - Considerar usar API REST directamente si es más confiable

3. **Monitorear:**
   - Verificar si el problema persiste en producción
   - Monitorear logs de errores
   - Evaluar si afecta otras funcionalidades

---

**Fecha de implementación:** Enero 2025
**Estado:** ✅ Funcionando con solución de fallback
**Prioridad de investigación:** Media (solución temporal funciona, pero debería investigarse causa raíz)


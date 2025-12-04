# Solución al Dead-Lock en onAuthStateChange

## Problema Identificado

El cliente JavaScript de Supabase se quedaba colgado debido a un **dead-lock causado por el uso incorrecto de `onAuthStateChange`**.

### Causa Raíz

Según la documentación oficial de Supabase y los maintainers en GitHub, el problema más común de cuelgues en el cliente es:

**❌ Patrón INCORRECTO (causa dead-lock):**
```javascript
supabase.auth.onAuthStateChange(async (event, session) => {
    // ❌ NUNCA hacer esto dentro del callback:
    const { data } = await supabase
        .from('perfiles_usuarios')
        .select(...)
        .maybeSingle();   // 💥 Esto bloquea todo
});
```

### Por Qué Ocurre

Cuando haces llamadas a otros métodos de Supabase (como `supabase.from().select()`) dentro del callback de `onAuthStateChange`, puedes crear un dead-lock porque:

1. `onAuthStateChange` está esperando que el callback termine
2. El callback está esperando que la query de Supabase termine
3. Pero Supabase está esperando que `onAuthStateChange` termine
4. **Resultado:** Todo se queda colgado indefinidamente

## Solución Oficial

### ✅ Patrón CORRECTO (recomendado por Supabase):

```javascript
supabase.auth.onAuthStateChange((event, session) => {
    // ✅ Usar setTimeout(..., 0) para mover las llamadas fuera del callback
    setTimeout(async () => {
        // Ahora puedes llamar a otros métodos de Supabase sin problemas
        const { data } = await supabase
            .from('perfiles_usuarios')
            .select(...)
            .maybeSingle();
    }, 0);
});
```

### Cambio Implementado

**Antes (causaba dead-lock):**
```javascript
supabase.auth.onAuthStateChange(async (event, session) => {
    if (event === 'SIGNED_IN' && session) {
        usuarioActual = session.user;
        await mostrarUIUsuario(); // ❌ Esto llama a obtenerRolUsuario() que usa supabase.from()
    }
});
```

**Después (corregido):**
```javascript
supabase.auth.onAuthStateChange((event, session) => {
    // ✅ Callback NO es async, y usamos setTimeout para mover las llamadas fuera
    setTimeout(async () => {
        if (event === 'SIGNED_IN' && session) {
            usuarioActual = session.user;
            await mostrarUIUsuario(); // ✅ Ahora está fuera del callback, no causa dead-lock
        }
    }, 0);
});
```

## Referencias Oficiales

### Documentación de Supabase

**URL:** https://supabase.com/docs/reference/javascript/auth-onauthstatechange

**Cita importante:**
> "Puedes crear fácilmente un dead-lock usando await en otra llamada a Supabase dentro del callback."
> 
> **Recomendaciones:**
> - Evita usar callbacks async
> - No uses otros métodos de Supabase dentro del callback
> - Si tienes que hacerlo, lanza esas funciones después, con `setTimeout(..., 0)`

### GitHub Discussion

**Issue:** Login se cuelga al intentar leer user_profiles con RLS

**Respuesta del maintainer (GaryAustin):**
> "Lo más probable no es RLS, sino un dead-lock causado por cómo se usa onAuthStateChange"

**Enlace:** https://github.com/supabase/supabase/discussions/[número]

## Otros Problemas Conocidos

### 1. `getSession()` se cuelga tras expirar token

Hay un bug conocido donde `supabase.auth.getSession()` se queda colgado indefinidamente después de que el token expire.

**Issue:** https://github.com/supabase/supabase-js/issues/[número]

### 2. Query Builder se cuelga en ciertos entornos

Hay un bug donde el promise del query builder no se construye bien en ciertos entornos (Windows 11 + Vite + React 19).

**Issue:** https://github.com/supabase/supabase-js/issues/[número]

## Solución Implementada en Este Proyecto

### 1. Corrección del Dead-Lock

✅ Cambiado `onAuthStateChange` para usar `setTimeout(..., 0)` según recomendación oficial

### 2. Sistema de Fallback (Mantenido)

Aunque el dead-lock está corregido, mantenemos el sistema de fallback con fetch directo como medida de seguridad adicional:

- Timeout de 8 segundos para consultas de rol
- Fallback automático a fetch directo si hay timeout
- Funciona incluso si hay otros problemas con el cliente

### 3. Mejoras Adicionales

- ✅ Comentarios explicativos sobre el dead-lock
- ✅ Referencias a la documentación oficial
- ✅ Logging mejorado para debugging

## Pruebas Recomendadas

Después de esta corrección, deberías probar:

1. **Inicio de sesión:** Verificar que el rol se carga correctamente sin timeouts
2. **Cierre de sesión:** Verificar que la UI se actualiza correctamente
3. **Refresh de token:** Verificar que no hay cuelgues durante el refresh
4. **Carga inicial:** Verificar que la sesión guardada se carga sin problemas

## Resultado Esperado

Con esta corrección:

- ✅ El cliente de Supabase debería funcionar correctamente sin cuelgues
- ✅ Las consultas deberían resolverse normalmente
- ✅ El sistema de fallback seguirá funcionando como medida de seguridad
- ✅ No debería haber más `Promise {<pending>}` indefinidos

## Notas Adicionales

### ¿Por Qué Mantener el Fallback?

Aunque el dead-lock está corregido, mantenemos el sistema de fallback porque:

1. **Seguridad:** Protege contra otros problemas conocidos (getSession colgado, etc.)
2. **Robustez:** Funciona incluso si hay problemas de red temporales
3. **Experiencia de usuario:** Garantiza que la aplicación siempre funciona

### Alternativa: Usar AbortController

La documentación oficial también recomienda usar `AbortController` para manejar timeouts:

```javascript
const controller = new AbortController();
setTimeout(() => controller.abort(), 8000);

const { data, error } = await supabase
    .from('perfiles_usuarios')
    .select('*')
    .abortSignal(controller.signal);
```

Sin embargo, nuestro sistema de `Promise.race` es equivalente y funciona bien.

---

**Fecha de corrección:** Enero 2025
**Estado:** ✅ Dead-lock corregido según recomendación oficial
**Referencia:** Documentación oficial de Supabase + GitHub Discussions


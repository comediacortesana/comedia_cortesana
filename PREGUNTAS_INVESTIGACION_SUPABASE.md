# Preguntas para Investigación: Timeout en Cliente Supabase JavaScript

## Problema Resumido

El cliente JavaScript oficial de Supabase (`@supabase/supabase-js@2`) se queda colgado indefinidamente en consultas a tablas con Row Level Security (RLS) habilitado. Las promesas nunca se resuelven, mostrando `Promise {<pending>}` indefinidamente.

**Fetch directo a la API REST funciona perfectamente**, lo que confirma que:
- ✅ Supabase está funcionando correctamente
- ✅ Las políticas RLS están bien configuradas
- ✅ El problema es específico del cliente JavaScript

## Preguntas Específicas para Buscar

### 1. Issues Conocidos en GitHub

**Búsquedas sugeridas:**
- `supabase-js timeout hanging queries`
- `supabase-js RLS policy queries not resolving`
- `supabase-js Promise pending forever`
- `supabase-js maybeSingle timeout`
- `supabase-js queries hanging with RLS enabled`

**Repositorios a revisar:**
- `supabase/supabase-js`
- `supabase/supabase`

### 2. Documentación Oficial

**Temas a buscar:**
- Supabase JavaScript Client troubleshooting guide
- Supabase timeout configuration options
- Supabase RLS queries best practices
- Supabase client hanging queries solution
- Supabase API REST vs JavaScript Client comparison

**URLs de documentación:**
- https://supabase.com/docs/reference/javascript
- https://supabase.com/docs/guides/api
- https://supabase.com/docs/guides/database/postgres/row-level-security

### 3. Stack Overflow / Foros

**Preguntas similares a buscar:**
- "Supabase JavaScript client queries hanging"
- "Supabase maybeSingle timeout not resolving"
- "Supabase RLS queries Promise pending"
- "Supabase client vs REST API performance"
- "Supabase queries timeout GitHub Pages"

### 4. Comunidad y Redes Sociales

**Lugares a consultar:**
- Supabase Discord/Slack
- Reddit r/supabase
- GitHub Discussions de Supabase
- Twitter/X con hashtag #supabase

**Preguntas para la comunidad:**
- "¿Alguien ha experimentado queries colgadas con el cliente JavaScript?"
- "¿Es mejor usar fetch directo cuando hay problemas con el cliente?"
- "¿Hay configuraciones específicas para evitar timeouts?"

### 5. Alternativas y Soluciones

**Investigar:**
- ¿Hay versiones específicas del cliente que funcionan mejor?
- ¿Hay configuraciones de timeout a nivel de cliente?
- ¿Es recomendable usar fetch directo como solución permanente?
- ¿Hay problemas conocidos con GitHub Pages y Supabase?

## Información Técnica para Búsquedas

### Versión del Cliente
```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
```
Versión: `@supabase/supabase-js@2` (última estable v2)

### Código que Falla
```javascript
// Esto se queda colgado:
const { data, error } = await supabase
    .from('perfiles_usuarios')
    .select('rol, nombre_completo')
    .eq('id', usuarioActual.id)
    .maybeSingle();
```

### Código que Funciona
```javascript
// Esto funciona perfectamente:
const response = await fetch(
    'https://PROJECT.supabase.co/rest/v1/perfiles_usuarios?id=eq.USER_ID&select=rol,nombre_completo',
    {
        headers: {
            'apikey': SUPABASE_ANON_KEY,
            'Content-Type': 'application/json'
        }
    }
);
const data = await response.json(); // Funciona inmediatamente
```

### Configuración Actual
```javascript
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
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

### Políticas RLS
```sql
-- Lectura pública permitida
CREATE POLICY "perfiles_lectura_publica"
ON perfiles_usuarios FOR SELECT
USING (true);
```

## Contexto Adicional

- **Entorno:** GitHub Pages (sitio estático)
- **Navegador:** Chrome/Edge (Chromium)
- **Plan Supabase:** Free tier
- **RLS:** Habilitado en todas las tablas
- **CORS:** Configurado por defecto

## Solución Temporal Implementada

Se implementó un sistema de fallback con `Promise.race` que:
1. Intenta usar el cliente con timeout de 8 segundos
2. Si hay timeout, automáticamente usa fetch directo
3. Actualiza la UI automáticamente

**¿Es esta la mejor solución?** Necesitamos investigar si hay alternativas más elegantes o si el problema tiene una causa raíz que pueda solucionarse.

## Resultado Esperado de la Investigación

1. **Confirmar si es un problema conocido:**
   - ¿Hay issues abiertos en GitHub?
   - ¿Hay soluciones oficiales o recomendadas?

2. **Encontrar solución permanente:**
   - ¿Hay configuraciones que puedan solucionarlo?
   - ¿Hay versiones específicas que funcionen mejor?
   - ¿Deberíamos migrar completamente a API REST?

3. **Mejores prácticas:**
   - ¿Es común usar fetch directo como fallback?
   - ¿Hay patrones recomendados para manejar timeouts?
   - ¿Qué recomienda la comunidad de Supabase?

---

**Instrucciones para GPT que investigue:**

1. Busca en GitHub Issues de `supabase/supabase-js` y `supabase/supabase`
2. Revisa la documentación oficial de Supabase sobre troubleshooting
3. Busca en Stack Overflow preguntas similares
4. Consulta comunidades de Supabase (Discord, Reddit)
5. Compara experiencias de otros desarrolladores
6. Verifica si hay soluciones oficiales o workarounds recomendados

**Información clave a reportar:**
- ¿Es un problema conocido?
- ¿Hay soluciones oficiales?
- ¿Qué recomienda la comunidad?
- ¿Hay alternativas mejores que fetch directo?


# ❓ FAQ y Troubleshooting: Google Sheets → GitHub

## 🐛 Problemas Comunes y Soluciones

### Error 1: `401 Unauthorized`

**Mensaje completo:**
```
GitHub API error: 401 - {"message":"Bad credentials"}
```

**Causa:** Token de GitHub inválido, expirado o mal configurado

**Soluciones:**

1. **Verificar que el token existe:**
```javascript
function checkToken() {
  const token = PropertiesService.getScriptProperties()
    .getProperty('GITHUB_TOKEN');
  
  if (!token) {
    Logger.log('❌ Token no encontrado');
  } else {
    Logger.log(`✅ Token: ${token.substring(0, 10)}...`);
  }
}
```

2. **Generar nuevo token:**
   - Ve a: https://github.com/settings/tokens
   - **Generate new token (classic)**
   - Scope: `repo` ✅
   - Copiar y ejecutar:
```javascript
function resetToken() {
  const newToken = 'ghp_NUEVO_TOKEN_AQUI';
  PropertiesService.getScriptProperties()
    .setProperty('GITHUB_TOKEN', newToken);
  Logger.log('✅ Token actualizado');
}
```

3. **Verificar que el token tiene permisos:**
   - En GitHub: Settings → Applications → Personal access tokens
   - Verifica que el token tenga acceso al repositorio

---

### Error 2: `404 Not Found`

**Mensaje completo:**
```
GitHub API error: 404 - {"message":"Not Found"}
```

**Causa:** Ruta incorrecta (owner, repo o path del archivo)

**Soluciones:**

1. **Verificar owner y repo:**
```javascript
function checkRepo() {
  Logger.log(`Owner: ${CONFIG.github.owner}`);
  Logger.log(`Repo: ${CONFIG.github.repo}`);
  Logger.log(`URL: https://github.com/${CONFIG.github.owner}/${CONFIG.github.repo}`);
  
  // Visita la URL manualmente para verificar
}
```

2. **Verificar path del archivo:**
```javascript
function checkPath() {
  const path = CONFIG.paths.csv;
  Logger.log(`Path configurado: ${path}`);
  
  // ⚠️ El path NO debe empezar con /
  // ✅ Correcto: filtro_basico/obras.csv
  // ❌ Incorrecto: /filtro_basico/obras.csv
}
```

3. **Verificar que tienes acceso al repositorio:**
   - Si es privado, asegúrate de tener permisos de escritura
   - Prueba clonando el repo manualmente

---

### Error 3: `403 Forbidden`

**Mensaje completo:**
```
GitHub API error: 403 - {"message":"Resource not accessible by integration"}
```

**Causa:** Token sin permisos suficientes

**Soluciones:**

1. **Regenerar token con scope correcto:**
   - Ve a: https://github.com/settings/tokens
   - Scope necesario: `repo` (acceso completo)
   - NO uses `public_repo` (solo repositorios públicos)

2. **Verificar permisos en el repositorio:**
   - Si es de una organización, verifica que el token tenga acceso
   - **Organization Settings** → **Third-party access**

---

### Error 4: `409 Conflict`

**Mensaje completo:**
```
GitHub API error: 409 - {"message":"Conflict"}
```

**Causa:** SHA del archivo no coincide (alguien más actualizó el archivo)

**Soluciones:**

El script maneja esto automáticamente obteniendo el SHA correcto. Si persiste:

```javascript
function forceUpdate() {
  // Deshabilita verificación de cambios temporalmente
  const originalCheck = CONFIG.options.checkForChanges;
  CONFIG.options.checkForChanges = false;
  
  syncToGitHub();
  
  // Restaura configuración
  CONFIG.options.checkForChanges = originalCheck;
}
```

---

### Error 5: `Rate limit exceeded`

**Mensaje completo:**
```
API rate limit exceeded for user
```

**Causa:** Demasiadas llamadas a la API de GitHub

**Límites de GitHub:**
- **Con autenticación:** 5,000 requests/hora
- **Sin autenticación:** 60 requests/hora

**Soluciones:**

1. **Verificar límite actual:**
```javascript
function checkRateLimit() {
  const token = getGitHubToken();
  const url = 'https://api.github.com/rate_limit';
  
  const response = UrlFetchApp.fetch(url, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const data = JSON.parse(response.getContentText());
  
  Logger.log(`Límite: ${data.resources.core.limit}`);
  Logger.log(`Usado: ${data.resources.core.used}`);
  Logger.log(`Restante: ${data.resources.core.remaining}`);
  Logger.log(`Reset: ${new Date(data.resources.core.reset * 1000)}`);
}
```

2. **Reducir frecuencia de triggers:**
   - En lugar de cada 5 minutos → cada hora
   - O usar trigger de edición con debounce

3. **Activar `checkForChanges`:**
```javascript
options: {
  checkForChanges: true  // Solo hace push si hay cambios reales
}
```

---

### Error 6: Caracteres raros en el CSV (encoding)

**Síntomas:**
- Acentos se ven como: `Ã©`, `Ã±`, `Ã¡`
- Caracteres especiales corruptos

**Causa:** Problema de encoding (UTF-8 vs Latin-1)

**Soluciones:**

1. **Verificar encoding en conversión:**
```javascript
function convertToCSVWithBOM(data) {
  const csv = data.map(row => {
    return row.map(cell => {
      let value = cell !== null && cell !== undefined ? cell.toString() : '';
      value = value.replace(/"/g, '""');
      
      if (value.includes(',') || value.includes('\n') || value.includes('"')) {
        value = `"${value}"`;
      }
      
      return value;
    }).join(',');
  }).join('\n');
  
  // Añadir BOM (Byte Order Mark) para UTF-8
  return '\ufeff' + csv;
}
```

2. **Verificar en GitHub:**
   - Abre el archivo en GitHub
   - Si se ve bien ahí, el problema es en tu editor local
   - Abre con editor que soporte UTF-8 (VSCode, Sublime)

---

### Error 7: Script se detiene sin error

**Síntomas:**
- Script parece ejecutarse pero no completa
- No aparece en logs de ejecución
- No hace push a GitHub

**Causas posibles:**
- Timeout de Apps Script (6 minutos máximo)
- Hoja muy grande
- Demasiadas hojas

**Soluciones:**

1. **Verificar tiempo de ejecución:**
```javascript
function measureExecutionTime() {
  const start = new Date();
  
  syncToGitHub();
  
  const end = new Date();
  const duration = (end - start) / 1000;
  
  Logger.log(`⏱️ Duración: ${duration} segundos`);
  
  if (duration > 300) {
    Logger.log('⚠️ Cerca del límite de 6 minutos');
  }
}
```

2. **Optimizar para hojas grandes:**
```javascript
sheets: {
  skipEmptyRows: true,  // Ignora filas vacías
  maxRows: 10000        // Limitar filas exportadas
}
```

3. **Procesar por lotes:**
```javascript
function syncInBatches() {
  const batchSize = 1000;
  // Exportar de 1000 en 1000
}
```

---

### Error 8: Permisos denegados en Apps Script

**Mensaje:**
```
Authorization required
This app requires permission to access your data
```

**Causa:** Primera ejecución, necesita autorización

**Soluciones:**

1. **Autorizar el script:**
   - Click **"Revisar permisos"**
   - Selecciona tu cuenta Google
   - Click **"Avanzado"**
   - Click **"Ir a [nombre del proyecto] (no seguro)"**
   - Click **"Permitir"**

2. **Si aparece "App no verificada":**
   - Es normal para scripts personales
   - Click **"Avanzado"** → **"Ir a [proyecto]"**
   - Es seguro porque es TU propio script

3. **Permisos solicitados:**
   - ✅ Ver y administrar hojas de cálculo (necesario)
   - ✅ Conectarse a servicio externo (GitHub API)
   - ✅ Enviar emails (si usas notificaciones)
   - ✅ Acceso a Google Drive (si usas backups)

---

### Error 9: Token expira constantemente

**Síntomas:**
- Funciona bien por un tiempo
- Luego empieza a fallar con 401
- Necesitas regenerar token seguido

**Causa:** Token configurado con expiración corta

**Soluciones:**

1. **Generar token sin expiración:**
   - En GitHub: https://github.com/settings/tokens
   - **Expiration**: Selecciona **"No expiration"**
   - ⚠️ Guárdalo en lugar seguro

2. **O configurar recordatorio:**
   - Si usas expiración de 90 días
   - Añade evento en calendario para renovar

3. **Crear script de verificación:**
```javascript
function checkTokenExpiration() {
  // GitHub no expone fecha de expiración en API
  // Pero puedes verificar que funciona:
  
  try {
    const token = getGitHubToken();
    const url = 'https://api.github.com/user';
    
    const response = UrlFetchApp.fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    Logger.log('✅ Token válido');
    return true;
    
  } catch (error) {
    Logger.log('❌ Token inválido o expirado');
    
    // Enviar email de alerta
    MailApp.sendEmail(
      CONFIG.options.emailTo,
      '⚠️ Token de GitHub expirado',
      'El token de GitHub necesita ser renovado.'
    );
    
    return false;
  }
}
```

4. **Trigger mensual de verificación:**
   - Función: `checkTokenExpiration`
   - Cada mes
   - Te avisa si el token expira pronto

---

### Error 10: CSV con comas rompe columnas

**Síntomas:**
- Columnas se desplazan
- Datos en columnas incorrectas
- Filas rotas

**Causa:** Comas dentro del contenido no escapadas

**Solución:** El script ya escapa automáticamente, pero verifica:

```javascript
function testCSVEscaping() {
  const testData = [
    ['ID', 'Título', 'Notas'],
    [1, 'Obra con, comas', 'Notas con "comillas"'],
    [2, 'Obra normal', 'Sin problemas']
  ];
  
  const csv = convertToCSV(testData);
  Logger.log(csv);
  
  // Debe verse:
  // ID,Título,Notas
  // 1,"Obra con, comas","Notas con ""comillas"""
  // 2,Obra normal,Sin problemas
}
```

Si el problema persiste, usa formato JSON en vez de CSV:

```javascript
sheets: {
  exportFormat: 'json'
}
```

---

## ❓ Preguntas Frecuentes

### ¿Es seguro guardar el token en Apps Script?

**Respuesta:** Sí, si usas `PropertiesService`:

- ✅ El token NO está visible en el código
- ✅ Solo tú tienes acceso (tu cuenta Google)
- ✅ No se sube a GitHub si compartes el código
- ⚠️ NUNCA pongas el token directamente en `CONFIG.github.token`

### ¿Cuánto cuesta esto?

**Respuesta:** ¡Completamente GRATIS! 🎉

- Google Apps Script: Gratis
- GitHub API: Gratis (5,000 requests/hora)
- Google Drive (backups): 15 GB gratis
- Sheets, Gmail: Ya incluidos

**Límites a considerar:**
- Apps Script: 6 minutos por ejecución
- GitHub: 5,000 requests/hora
- Google Drive: 15 GB (más que suficiente para CSVs)

### ¿Puedo usar esto con repositorios privados?

**Respuesta:** ¡Sí! Funciona igual con repos privados y públicos.

Solo asegúrate de:
- ✅ Token tiene scope `repo`
- ✅ Tienes permisos de escritura en el repo

### ¿Cuántas veces al día puedo sincronizar?

**Respuesta:** Tantas como quieras, respetando límites:

- **Límite GitHub API:** 5,000 requests/hora
- **Límite Apps Script:** 20-30 triggers por día (gratis)
- **Recomendado:** Cada hora = 24 syncs/día

Con `checkForChanges: true`, solo hace push real si hay cambios.

### ¿Qué pasa si dos personas editan al mismo tiempo?

**Respuesta:** 

1. **En Google Sheets:** No hay problema, Sheets maneja ediciones simultáneas
2. **En GitHub:** El script siempre sube la versión más reciente de Sheets
3. **Conflictos:** No hay conflictos porque Sheets es la "fuente de verdad"

**Flujo:**
```
Persona A edita celda X → Sheets la guarda
Persona B edita celda Y → Sheets la guarda
Script ejecuta → Sube AMBOS cambios juntos
```

### ¿Puedo sincronizar de GitHub → Sheets?

**Respuesta:** No está implementado por defecto, pero puedes hacerlo:

```javascript
function syncFromGitHub() {
  // 1. Obtener CSV de GitHub
  const content = getFileFromGitHub(CONFIG.paths.csv);
  
  // 2. Parsear CSV
  const rows = content.split('\n').map(line => 
    line.split(',')
  );
  
  // 3. Escribir en Sheet
  const sheet = SpreadsheetApp.getActiveSpreadsheet()
    .getSheetByName('Obras Completas');
  
  sheet.clear();
  sheet.getRange(1, 1, rows.length, rows[0].length)
    .setValues(rows);
  
  Logger.log('✅ Datos importados desde GitHub');
}
```

⚠️ **Cuidado:** Esto sobrescribirá la hoja. Mejor hacer backup primero.

### ¿Funciona con Google Sheets de mi organización?

**Respuesta:** Sí, pero puede requerir aprobación de admin:

- Si tu organización tiene restricciones, puede que necesites:
  - Aprobación de IT para usar Apps Script
  - Aprobación para conectarse a APIs externas

- Consulta con tu admin de Google Workspace

### ¿Puedo pausar la sincronización temporalmente?

**Respuesta:** Sí, varias formas:

**Opción 1: Deshabilitar triggers**
- **Activadores** (en Apps Script)
- Click en los 3 puntos del trigger
- **Eliminar**

**Opción 2: Añadir "kill switch" al código**
```javascript
const SYNC_ENABLED = true;  // Cambiar a false para pausar

function syncToGitHub() {
  if (!SYNC_ENABLED) {
    Logger.log('⏸️ Sincronización pausada');
    return;
  }
  
  // ... resto del código
}
```

**Opción 3: Usar Properties**
```javascript
function pauseSync() {
  PropertiesService.getScriptProperties()
    .setProperty('SYNC_PAUSED', 'true');
  Logger.log('⏸️ Sync pausado');
}

function resumeSync() {
  PropertiesService.getScriptProperties()
    .setProperty('SYNC_PAUSED', 'false');
  Logger.log('▶️ Sync reanudado');
}

// En syncToGitHub():
const paused = PropertiesService.getScriptProperties()
  .getProperty('SYNC_PAUSED') === 'true';

if (paused) {
  Logger.log('⏸️ Sincronización pausada');
  return;
}
```

### ¿Cómo veo el historial de cambios?

**Respuesta:** Tienes dos opciones:

**1. En GitHub:**
- Ve al archivo en GitHub
- Click en **"History"**
- Verás todos los commits con fechas y cambios

**2. En Google Sheets:**
- **Archivo** → **Historial de versiones**
- Verás cambios en el Sheet (antes del push)

**3. En Apps Script:**
```javascript
function showStats() {
  // Muestra estadísticas de sincronizaciones
}
```

### ¿Puedo usar esto para otros proyectos?

**Respuesta:** ¡Absolutamente! Es 100% reutilizable.

Solo necesitas cambiar:
```javascript
const CONFIG = {
  github: {
    owner: 'NUEVO_USUARIO',
    repo: 'NUEVO_REPO',
  },
  sheets: {
    sheetNames: ['NUEVA_HOJA']
  },
  paths: {
    csv: 'ruta/nueva/archivo.csv'
  }
};
```

Funciona con cualquier combinación de:
- ✅ Cualquier repositorio GitHub
- ✅ Cualquier Google Sheet
- ✅ CSV o JSON
- ✅ Público o privado

---

## 🔍 Debug Avanzado

### Modo Verbose

Activa logs super detallados:

```javascript
const DEBUG = true;

function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString();
  const prefix = DEBUG ? '🔍' : '';
  Logger.log(`[${timestamp}] ${prefix} [${level}] ${message}`);
}
```

### Inspeccionar Requests a GitHub

```javascript
function debugGitHubRequest() {
  const token = getGitHubToken();
  const url = `https://api.github.com/repos/${CONFIG.github.owner}/${CONFIG.github.repo}/contents/${CONFIG.paths.csv}`;
  
  Logger.log('🔍 URL: ' + url);
  Logger.log('🔍 Token (primeros 10 chars): ' + token.substring(0, 10));
  
  const options = {
    method: 'get',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/vnd.github.v3+json'
    },
    muteHttpExceptions: true
  };
  
  Logger.log('🔍 Request headers: ' + JSON.stringify(options.headers, null, 2));
  
  const response = UrlFetchApp.fetch(url, options);
  
  Logger.log('🔍 Response code: ' + response.getResponseCode());
  Logger.log('🔍 Response body: ' + response.getContentText());
}
```

### Ver Contenido Generado

```javascript
function debugGeneratedContent() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName(CONFIG.sheets.sheetNames[0]);
  const data = readSheetData(sheet);
  
  const csvContent = convertToCSV(data);
  
  Logger.log('🔍 CSV generado:');
  Logger.log('─'.repeat(60));
  Logger.log(csvContent.substring(0, 500)); // Primeros 500 caracteres
  Logger.log('─'.repeat(60));
  Logger.log(`🔍 Total bytes: ${csvContent.length}`);
}
```

---

## 📊 Monitoreo Proactivo

### Dashboard de Estado

```javascript
function createStatusDashboard() {
  const stats = getStats();
  const properties = PropertiesService.getScriptProperties();
  
  const dashboard = `
╔════════════════════════════════════════════════════╗
║       📊 ESTADO DE SINCRONIZACIÓN                  ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║  Total sincronizaciones: ${stats.totalSyncs.padEnd(27)}║
║  Exitosas: ${stats.successfulSyncs.padEnd(38)}║
║  Última sync: ${stats.lastSync.substring(0, 19).padEnd(31)}║
║                                                    ║
║  Token configurado: ${properties.getProperty('GITHUB_TOKEN') ? '✅' : '❌'}                        ║
║  Repo: ${CONFIG.github.owner}/${CONFIG.github.repo.padEnd(32)}║
║  Rama: ${CONFIG.github.branch.padEnd(42)}║
║                                                    ║
╚════════════════════════════════════════════════════╝
`;
  
  Logger.log(dashboard);
}
```

### Health Check Automático

```javascript
function healthCheck() {
  const checks = {
    token: false,
    github: false,
    sheet: false,
    trigger: false
  };
  
  // Check 1: Token
  try {
    getGitHubToken();
    checks.token = true;
  } catch (e) {
    Logger.log('❌ Token no configurado');
  }
  
  // Check 2: GitHub
  try {
    testGitHubConnection();
    checks.github = true;
  } catch (e) {
    Logger.log('❌ No se puede conectar a GitHub');
  }
  
  // Check 3: Sheet
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet()
      .getSheetByName(CONFIG.sheets.sheetNames[0]);
    if (sheet) checks.sheet = true;
  } catch (e) {
    Logger.log('❌ Hoja no encontrada');
  }
  
  // Check 4: Triggers
  const triggers = ScriptApp.getProjectTriggers();
  checks.trigger = triggers.length > 0;
  
  // Resumen
  const total = Object.values(checks).filter(v => v).length;
  const health = (total / Object.keys(checks).length) * 100;
  
  Logger.log(`\n🏥 Health Check: ${health.toFixed(0)}%`);
  Logger.log(`✅ Token: ${checks.token ? 'OK' : 'FAIL'}`);
  Logger.log(`✅ GitHub: ${checks.github ? 'OK' : 'FAIL'}`);
  Logger.log(`✅ Sheet: ${checks.sheet ? 'OK' : 'FAIL'}`);
  Logger.log(`✅ Triggers: ${checks.trigger ? 'OK' : 'FAIL'}`);
  
  return health === 100;
}
```

---

## 🎓 Recursos Adicionales

### Documentación Oficial

- **Google Apps Script:** https://developers.google.com/apps-script/guides/sheets
- **GitHub REST API:** https://docs.github.com/en/rest/repos/contents
- **GitHub Tokens:** https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

### Tutoriales

- **Apps Script Triggers:** https://developers.google.com/apps-script/guides/triggers
- **UrlFetchApp:** https://developers.google.com/apps-script/reference/url-fetch
- **Properties Service:** https://developers.google.com/apps-script/reference/properties

### Comunidad

- **Stack Overflow:** https://stackoverflow.com/questions/tagged/google-apps-script
- **GitHub Community:** https://github.community

---

## 💬 Soporte

Si tienes problemas que no están en esta guía:

1. **Ejecuta health check:**
```javascript
healthCheck();
```

2. **Revisa logs detallados:**
```javascript
createStatusDashboard();
debugGitHubRequest();
```

3. **Verifica configuración:**
```javascript
runAllTests();
```

4. **Consulta documentación:**
   - `AUTOMATIZACION_SHEETS_GITHUB.md` - Guía completa
   - `CONFIGURACION_EJEMPLOS.md` - Ejemplos de uso

---

**¡Buena suerte con tu sincronización automática! 🚀**




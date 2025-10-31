# 📋 Cheat Sheet: Google Sheets → GitHub Sync

## ⚡ Comandos Rápidos

### Primera Configuración

```javascript
// 1. Configurar token (una sola vez)
setGitHubToken();

// 2. Verificar configuración
runAllTests();

// 3. Primera sincronización
syncToGitHub();

// 4. Ver estadísticas
showStats();
```

### Uso Diario

```javascript
// Sincronizar manualmente
syncToGitHub();

// Verificar salud del sistema
healthCheck();

// Ver últimos logs
Logger.log(Logger.getLog());

// Limpiar estadísticas
clearStats();
```

---

## 🔧 Configuración Mínima

```javascript
const CONFIG = {
  github: {
    owner: 'TU_USUARIO',
    repo: 'TU_REPO',
    token: '',  // usar setGitHubToken()
    branch: 'main'
  },
  
  sheets: {
    exportFormat: 'csv',
    sheetNames: ['TU_HOJA']
  },
  
  paths: {
    csv: 'ruta/archivo.csv'
  },
  
  options: {
    checkForChanges: true  // ⭐ IMPORTANTE
  }
};
```

---

## 🎯 Triggers Comunes

| Frecuencia | Configuración | Uso |
|------------|---------------|-----|
| **Cada hora** | Según tiempo → Cada hora | Edición colaborativa |
| **Cada día** | Según tiempo → Diario 00:00 | Backup nocturno |
| **Cada 30 min** | Según tiempo → Cada 30 minutos | Alta frecuencia |
| **Al editar** | Al editar | Tiempo real (con debounce) |

---

## 🐛 Errores y Soluciones Rápidas

| Error | Solución Rápida |
|-------|-----------------|
| `401 Unauthorized` | `setGitHubToken()` con nuevo token |
| `404 Not Found` | Verificar `owner` y `repo` en CONFIG |
| `403 Forbidden` | Token necesita scope `repo` |
| `409 Conflict` | Automático, o ejecuta `forceUpdate()` |
| Rate limit | Reducir frecuencia de trigger |
| Encoding | Usa `convertToCSVWithBOM()` |
| Sin push | Verificar `checkForChanges` y logs |

---

## 📊 Funciones de Debug

```javascript
// Health check completo
healthCheck();

// Test individual
testConfig();
testGitHubConnection();
testReadSheet();

// Ver configuración
Logger.log(JSON.stringify(CONFIG, null, 2));

// Ver token (primeros 10 chars)
Logger.log(getGitHubToken().substring(0, 10));

// Ver límite de API
checkRateLimit();

// Dashboard de estado
createStatusDashboard();

// Ver contenido generado
debugGeneratedContent();
```

---

## 🔐 Seguridad

### ✅ HACER
```javascript
// Guardar token en Properties
PropertiesService.getScriptProperties()
  .setProperty('GITHUB_TOKEN', 'ghp_XXX');

// Dejar CONFIG.github.token vacío
token: ''
```

### ❌ NO HACER
```javascript
// NUNCA poner token directamente en código
token: 'ghp_XXXXXXXXXX'  // ❌ ❌ ❌
```

---

## 🎨 Mensajes de Commit Personalizados

```javascript
// Simple
return `Actualización desde ${sheetName}`;

// Con fecha
return `Actualización ${new Date().toISOString().split('T')[0]}`;

// Detallado
return `📊 ${sheetName} actualizado

Total filas: ${data.length}
Formato: ${format}
Usuario: ${Session.getActiveUser().getEmail()}

[Auto-sync]`;
```

---

## 📱 Notificaciones Rápidas

### Slack
```javascript
notifications: {
  slack: {
    enabled: true,
    webhookUrl: 'https://hooks.slack.com/services/XXX'
  }
}
```

### Discord
```javascript
notifications: {
  discord: {
    enabled: true,
    webhookUrl: 'https://discord.com/api/webhooks/XXX'
  }
}
```

### Email
```javascript
notifications: {
  email: {
    enabled: true,
    recipients: ['tu@email.com']
  }
}
```

---

## 🔍 Verificaciones Rápidas

```javascript
// ¿Token configurado?
!!PropertiesService.getScriptProperties()
  .getProperty('GITHUB_TOKEN')

// ¿Hoja existe?
!!SpreadsheetApp.getActiveSpreadsheet()
  .getSheetByName(CONFIG.sheets.sheetNames[0])

// ¿Triggers activos?
ScriptApp.getProjectTriggers().length > 0

// ¿Conexión a GitHub OK?
testGitHubConnection()
```

---

## 📦 Formatos de Exportación

### CSV
```javascript
sheets: {
  exportFormat: 'csv'
}
paths: {
  csv: 'filtro_basico/obras.csv'
}
```

**Salida:**
```csv
ID,Título,Autor
1,La vida es sueño,Calderón
```

### JSON
```javascript
sheets: {
  exportFormat: 'json'
}
paths: {
  json: 'filtro_basico/obras.json'
}
```

**Salida:**
```json
[
  {
    "ID": 1,
    "Título": "La vida es sueño",
    "Autor": "Calderón"
  }
]
```

---

## 🎯 Casos de Uso Rápidos

### 1. Simple - Una hoja cada hora
```javascript
// CONFIG básico + trigger cada hora
syncToGitHub();
```

### 2. Múltiples hojas
```javascript
multiSheet: {
  enabled: true,
  mappings: {
    'Hoja1': 'archivo1.csv',
    'Hoja2': 'archivo2.csv'
  }
}
```

### 3. Con validación
```javascript
validation: {
  enabled: true,
  requiredColumns: ['ID', 'Título']
}
```

### 4. Con backup
```javascript
backup: {
  enabled: true,
  folderName: 'Backups',
  keepLastN: 10
}
```

### 5. Solo si investigador marca "Listo"
```javascript
// Usar función syncOnlyReady()
// Ver CONFIGURACION_EJEMPLOS.md - Caso 6
```

---

## 🔄 Flujo Típico

```
1. Copiar sheets-github-sync.gs
2. Editar CONFIG (owner, repo, paths)
3. setGitHubToken()
4. runAllTests()
5. syncToGitHub() (manual)
6. Configurar trigger
7. ¡Automático! 🎉
```

---

## 📊 Estadísticas

```javascript
// Ver stats
getStats()

// Propiedades guardadas:
PropertiesService.getScriptProperties().getProperties()
// - GITHUB_TOKEN
// - totalSyncs
// - successfulSyncs
// - lastSync
// - lastResults
```

---

## 💡 Tips Rápidos

1. ✅ Siempre usa `checkForChanges: true`
2. ✅ Empieza con trigger cada hora
3. ✅ Activa backups en Drive
4. ✅ Revisa logs frecuentemente
5. ✅ Token sin expiración (o recordatorio)
6. ✅ Scope mínimo: solo `repo`
7. ✅ Nunca pongas token en código
8. ✅ Prueba manual antes de automatizar

---

## 🔗 Enlaces Rápidos

- **Token GitHub:** https://github.com/settings/tokens
- **Verificar repo:** `https://github.com/OWNER/REPO`
- **Apps Script:** Extensiones → Apps Script
- **Triggers:** ⏰ en menú lateral
- **Logs:** Ver → Registros de ejecución (Ctrl+Enter)

---

## 📁 Archivos del Proyecto

```
filtro_basico/
├── sheets-github-sync.gs              # Script básico ⭐
├── sheets-github-sync-advanced.gs     # Script avanzado
├── SHEETS_GITHUB_SYNC_README.md       # README principal
├── AUTOMATIZACION_SHEETS_GITHUB.md    # Guía completa
├── CONFIGURACION_EJEMPLOS.md          # 6 ejemplos
├── FAQ_TROUBLESHOOTING.md             # FAQ + debug
└── CHEATSHEET.md                      # Este archivo
```

---

## 🎓 Orden de Lectura

1. **[SHEETS_GITHUB_SYNC_README.md](./SHEETS_GITHUB_SYNC_README.md)** - Empieza aquí
2. **[AUTOMATIZACION_SHEETS_GITHUB.md](./AUTOMATIZACION_SHEETS_GITHUB.md)** - Guía paso a paso
3. **[CONFIGURACION_EJEMPLOS.md](./CONFIGURACION_EJEMPLOS.md)** - Busca tu caso de uso
4. **[CHEATSHEET.md](./CHEATSHEET.md)** - Referencia rápida (este archivo)
5. **[FAQ_TROUBLESHOOTING.md](./FAQ_TROUBLESHOOTING.md)** - Solo si hay problemas

---

## 🚀 Inicio Ultra-Rápido (2 minutos)

```javascript
// 1. Copiar sheets-github-sync.gs a Apps Script

// 2. Editar CONFIG (3 líneas)
owner: 'ivansimo',
repo: 'DELIA_DJANGO',
sheetNames: ['Obras Completas'],
csv: 'filtro_basico/obras_completas.csv'

// 3. Ejecutar (solo una vez)
function setup() {
  PropertiesService.getScriptProperties()
    .setProperty('GITHUB_TOKEN', 'ghp_XXXXX');
  runAllTests();
  syncToGitHub();
}

// 4. Configurar trigger
// ⏰ → + Agregar → syncToGitHub → Cada hora

// ✅ ¡Listo!
```

---

## 📞 Ayuda Rápida

### Problema: No funciona
```javascript
// Ejecutar en orden:
1. healthCheck()
2. runAllTests()
3. Logger.log(Logger.getLog())
4. Consultar FAQ_TROUBLESHOOTING.md
```

### Problema: Error 401
```javascript
// Token inválido
setGitHubToken();  // Ingresar nuevo token
testGitHubConnection();  // Verificar
```

### Problema: Error 404
```javascript
// Verificar configuración
Logger.log(`Owner: ${CONFIG.github.owner}`);
Logger.log(`Repo: ${CONFIG.github.repo}`);
Logger.log(`Path: ${CONFIG.paths.csv}`);

// Visitar manualmente:
// https://github.com/OWNER/REPO
```

---

## 🎉 Resultado Final

```
Investigadores editan Google Sheet
         ↓
Script detecta cambios (cada hora)
         ↓
Push automático a GitHub
         ↓
GitHub Pages actualizado
         ↓
Usuario final ve cambios
         ↓
¡TODO AUTOMÁTICO! 🚀
```

**Gratis · Sin servidores · 5 minutos de setup**

---

## 💾 Backup de Configuración

```javascript
// Guardar tu configuración
function backupConfig() {
  const backup = {
    config: CONFIG,
    advancedConfig: ADVANCED_CONFIG,
    timestamp: new Date().toISOString()
  };
  
  Logger.log(JSON.stringify(backup, null, 2));
  
  // Copiar y pegar en un archivo de texto
}
```

---

## 🔄 Restaurar Token

```javascript
// Si perdiste el token
function restoreToken() {
  // 1. Genera nuevo en GitHub
  const newToken = 'ghp_NUEVO_TOKEN';
  
  // 2. Guarda
  PropertiesService.getScriptProperties()
    .setProperty('GITHUB_TOKEN', newToken);
  
  // 3. Verifica
  testGitHubConnection();
}
```

---

**Versión:** 2.0  
**Última actualización:** 2025-10-31  

**⭐ Guarda este archivo para referencia rápida ⭐**


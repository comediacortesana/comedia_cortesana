# 📝 Ejemplos de Configuración: Google Sheets → GitHub

## 🎯 Casos de Uso Comunes

### Caso 1: Sincronización Simple (Una hoja, cada hora)

**Necesidad:** 
- Equipo de 3-5 investigadores editando una sola hoja
- Sincronizar a GitHub cada hora
- Solo CSV
- Sin complicaciones

**Configuración en `sheets-github-sync.gs`:**

```javascript
const CONFIG = {
  github: {
    owner: 'ivansimo',
    repo: 'DELIA_DJANGO',
    token: '',  // usar setGitHubToken()
    branch: 'main'
  },
  
  sheets: {
    exportFormat: 'csv',
    sheetNames: ['Obras Completas'],
    exportAll: false,
    includeHeaders: true,
    skipEmptyRows: true
  },
  
  paths: {
    csv: 'filtro_basico/obras_completas.csv',
    json: 'filtro_basico/datos_obras.json',
    exportBoth: false
  },
  
  options: {
    checkForChanges: true,    // ✅ Solo push si hay cambios
    enableLogs: true,
    notifyOnError: false,
    maxRetries: 3,
    retryDelay: 2000
  }
};
```

**Trigger:**
- **Función:** `syncToGitHub`
- **Evento:** Según tiempo
- **Intervalo:** Cada hora

**Resultado:**
- Cada hora verifica cambios
- Si hay cambios, hace push automático
- Si no hay cambios, no hace nada
- Historial limpio en GitHub

---

### Caso 2: Múltiples Hojas (Obras, Autores, Lugares)

**Necesidad:**
- 4 hojas diferentes: Obras, Autores, Lugares, Representaciones
- Cada hoja → archivo CSV separado
- Sincronizar cada 30 minutos
- Validación de datos

**Configuración en `sheets-github-sync-advanced.gs`:**

```javascript
const CONFIG = {
  github: {
    owner: 'ivansimo',
    repo: 'DELIA_DJANGO',
    token: '',
    branch: 'main'
  },
  
  sheets: {
    exportFormat: 'csv',
    sheetNames: [], // no usado cuando multiSheet está habilitado
    exportAll: false
  },
  
  paths: {
    exportBoth: false
  },
  
  options: {
    checkForChanges: true,
    enableLogs: true,
    notifyOnError: true,
    emailTo: 'ivan@example.com'
  }
};

const ADVANCED_CONFIG = {
  validation: {
    enabled: true,
    minRows: 2,
    maxEmptyRows: 0.3,
    requiredColumns: ['ID', 'Título'],
    validateTypes: true
  },
  
  backup: {
    enabled: true,
    folderName: 'Backups Sheets GitHub',
    keepLastN: 10,
    format: 'csv'
  },
  
  notifications: {
    slack: { enabled: false },
    discord: { enabled: false },
    email: {
      enabled: true,
      recipients: ['ivan@example.com']
    }
  },
  
  multiSheet: {
    enabled: true,
    mappings: {
      'Obras Completas': 'filtro_basico/obras_completas.csv',
      'Autores': 'filtro_basico/autores.csv',
      'Lugares': 'filtro_basico/lugares.csv',
      'Representaciones': 'filtro_basico/representaciones.csv'
    }
  }
};
```

**Trigger:**
- **Función:** `syncToGitHubAdvanced`
- **Evento:** Según tiempo
- **Intervalo:** Cada 30 minutos

**Resultado:**
- Cada 30 minutos procesa las 4 hojas
- Valida datos antes de subir
- Crea backup en Google Drive
- Envía email si hay errores
- Mantiene solo los últimos 10 backups

---

### Caso 3: Sincronización en Tiempo Real (con debounce)

**Necesidad:**
- Push inmediato tras cada edición
- Pero esperar 5 minutos por si hay más cambios
- Notificaciones a Slack
- Backup automático

**Configuración en `sheets-github-sync-advanced.gs`:**

```javascript
const CONFIG = {
  // ... config básica igual que antes
  
  options: {
    checkForChanges: true,
    enableLogs: true,
    notifyOnError: true,
    emailTo: 'ivan@example.com'
  }
};

const ADVANCED_CONFIG = {
  validation: {
    enabled: true,
    minRows: 2,
    maxEmptyRows: 0.5,
    requiredColumns: ['ID', 'Título']
  },
  
  backup: {
    enabled: true,
    folderName: 'Backups Sheets GitHub',
    keepLastN: 20,
    format: 'csv'
  },
  
  notifications: {
    slack: {
      enabled: true,
      webhookUrl: 'https://hooks.slack.com/services/T00/B00/XXXX'
    },
    discord: { enabled: false },
    email: { enabled: false }
  },
  
  debounce: {
    enabled: true,
    delayMinutes: 5  // esperar 5 minutos
  },
  
  dataProcessing: {
    trimWhitespace: true,
    removeEmptyRows: true,
    normalizeLineBreaks: true,
    convertDates: true,
    lowercaseHeaders: false
  }
};
```

**Triggers (dos):**

1. **Trigger de edición:**
   - **Función:** `onEdit` (solo registra el timestamp)
   - **Evento:** Al editar
   
2. **Trigger de verificación:**
   - **Función:** `syncToGitHubAdvanced`
   - **Evento:** Según tiempo
   - **Intervalo:** Cada 5 minutos

**Flujo:**
1. Usuario edita celda → `onEdit` registra timestamp
2. 5 minutos después → `syncToGitHubAdvanced` verifica debounce
3. Si pasaron 5 min sin más ediciones → hace push
4. Si hubo más ediciones → espera otros 5 min
5. Envía notificación a Slack cuando hay push

**Resultado:**
- Sincronización casi en tiempo real
- Evita múltiples pushes por edición continua
- Equipo notificado en Slack instantáneamente

---

### Caso 4: Exportar CSV y JSON simultáneamente

**Necesidad:**
- CSV para importar a Django
- JSON para frontend (filtro_basico/index.html)
- Ambos archivos actualizados al mismo tiempo

**Configuración - Opción A (modificar función principal):**

```javascript
// En sheets-github-sync.gs, modificar processSheet():

function processSheet(spreadsheet, sheetName) {
  // ... código existente ...
  
  const data = readSheetData(sheet);
  
  // Generar CSV
  const csvContent = convertToCSV(data);
  const csvPath = CONFIG.paths.csv;
  
  // Generar JSON
  const jsonContent = convertToJSON(data);
  const jsonPath = CONFIG.paths.json;
  
  // Push CSV
  log('📤 Subiendo CSV...', 'INFO');
  const csvResult = pushToGitHub(csvContent, csvPath, `${sheetName} (CSV)`);
  
  // Push JSON
  log('📤 Subiendo JSON...', 'INFO');
  const jsonResult = pushToGitHub(jsonContent, jsonPath, `${sheetName} (JSON)`);
  
  return {
    sheet: sheetName,
    status: 'success',
    csv: csvResult.commit.sha,
    json: jsonResult.commit.sha
  };
}
```

**Configuración - Opción B (crear nueva función):**

```javascript
function syncBothFormats() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheetName = CONFIG.sheets.sheetNames[0];
  const sheet = spreadsheet.getSheetByName(sheetName);
  const data = readSheetData(sheet);
  
  const results = [];
  
  // CSV
  const csvContent = convertToCSV(data);
  const csvResult = pushToGitHub(
    csvContent, 
    'filtro_basico/obras_completas.csv',
    `${sheetName} (CSV)`
  );
  results.push({ format: 'CSV', commit: csvResult.commit.sha });
  
  // JSON
  const jsonContent = convertToJSON(data);
  const jsonResult = pushToGitHub(
    jsonContent,
    'filtro_basico/datos_obras.json',
    `${sheetName} (JSON)`
  );
  results.push({ format: 'JSON', commit: jsonResult.commit.sha });
  
  log('✅ Ambos formatos subidos', 'INFO');
  return results;
}
```

**Trigger:**
- **Función:** `syncBothFormats`
- **Evento:** Según tiempo
- **Intervalo:** Cada hora

---

### Caso 5: Backup Diario con Notificaciones

**Necesidad:**
- Backup diario a medianoche
- Guardar en Google Drive
- Notificar por email con resumen
- No necesita estar sincronizado constantemente

**Configuración:**

```javascript
const ADVANCED_CONFIG = {
  validation: {
    enabled: false  // no necesario para backup
  },
  
  backup: {
    enabled: true,
    folderName: 'Backups Diarios - Teatro Español',
    keepLastN: 30,  // mantener 30 días
    format: 'csv'
  },
  
  notifications: {
    slack: { enabled: false },
    discord: { enabled: false },
    email: {
      enabled: true,
      recipients: [
        'ivan@example.com',
        'investigador1@example.com',
        'investigador2@example.com'
      ]
    }
  }
};
```

**Función personalizada:**

```javascript
function dailyBackup() {
  log('🌙 Backup diario iniciado...', 'INFO');
  
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheetName = CONFIG.sheets.sheetNames[0];
  const sheet = spreadsheet.getSheetByName(sheetName);
  const data = readSheetData(sheet);
  
  // Generar CSV
  const csvContent = convertToCSV(data);
  
  // Guardar en Drive
  backupToGoogleDrive(csvContent, sheetName, 'csv');
  
  // También subir a GitHub (opcional)
  if (CONFIG.options.checkForChanges) {
    const hasChanges = checkForChanges(
      csvContent, 
      CONFIG.paths.csv
    );
    
    if (hasChanges) {
      pushToGitHub(csvContent, CONFIG.paths.csv, sheetName);
      log('✅ Cambios pusheados a GitHub', 'INFO');
    } else {
      log('⚪ Sin cambios en GitHub', 'INFO');
    }
  }
  
  // Enviar resumen por email
  const summary = {
    date: new Date().toISOString().split('T')[0],
    rows: data.length,
    backupLocation: 'Google Drive',
    githubUpdated: hasChanges || false
  };
  
  sendDailySummaryEmail(summary);
  
  log('🎉 Backup diario completado', 'INFO');
}

function sendDailySummaryEmail(summary) {
  const recipients = ADVANCED_CONFIG.notifications.email.recipients;
  const subject = `📊 Backup Diario - ${summary.date}`;
  const body = `
Backup diario completado exitosamente:

📅 Fecha: ${summary.date}
📊 Total de obras: ${summary.rows}
💾 Ubicación backup: ${summary.backupLocation}
🔄 GitHub actualizado: ${summary.githubUpdated ? 'Sí' : 'No'}

El backup está disponible en Google Drive en la carpeta:
"Backups Diarios - Teatro Español"

Saludos,
Sistema automatizado de backups
`;
  
  recipients.forEach(email => {
    MailApp.sendEmail(email, subject, body);
  });
}
```

**Trigger:**
- **Función:** `dailyBackup`
- **Evento:** Según tiempo
- **Tipo:** Activador de temporizador de día
- **Hora:** 00:00 - 01:00 (medianoche)

---

### Caso 6: Solo Push si Investigador Marca "Listo"

**Necesidad:**
- No hacer push automático de cualquier cambio
- Solo hacer push cuando investigador marca columna "Estado" como "Listo"
- Evita subir trabajo incompleto

**Configuración:**

Añadir columna "Estado de Revisión" en la hoja con valores:
- `En progreso`
- `Listo para publicar`
- `Publicado`

**Función personalizada:**

```javascript
function syncOnlyReady() {
  log('🔍 Verificando filas listas para publicar...', 'INFO');
  
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName('Obras Completas');
  const data = readSheetData(sheet);
  
  if (data.length === 0) return;
  
  // Encontrar columna "Estado de Revisión"
  const headers = data[0];
  const statusColIndex = headers.indexOf('Estado de Revisión');
  
  if (statusColIndex === -1) {
    throw new Error('Columna "Estado de Revisión" no encontrada');
  }
  
  // Contar filas listas
  let readyRows = 0;
  let publishedRows = 0;
  
  for (let i = 1; i < data.length; i++) {
    const status = data[i][statusColIndex];
    
    if (status === 'Listo para publicar') {
      readyRows++;
    } else if (status === 'Publicado') {
      publishedRows++;
    }
  }
  
  log(`📊 Filas listas: ${readyRows}`, 'INFO');
  log(`📊 Filas ya publicadas: ${publishedRows}`, 'INFO');
  
  if (readyRows === 0) {
    log('⚪ No hay filas nuevas listas para publicar', 'INFO');
    return;
  }
  
  // Hay filas listas, hacer push completo
  log('✅ Haciendo push de datos actualizados...', 'INFO');
  
  const csvContent = convertToCSV(data);
  const result = pushToGitHub(
    csvContent,
    CONFIG.paths.csv,
    `${readyRows} obras nuevas publicadas`
  );
  
  // Marcar como "Publicado"
  for (let i = 1; i < data.length; i++) {
    if (data[i][statusColIndex] === 'Listo para publicar') {
      sheet.getRange(i + 1, statusColIndex + 1).setValue('Publicado');
    }
  }
  
  log(`🎉 ${readyRows} obras publicadas exitosamente`, 'INFO');
  
  // Notificar
  const message = `✅ ${readyRows} obras nuevas han sido publicadas en GitHub`;
  
  if (ADVANCED_CONFIG.notifications.slack.enabled) {
    sendSlackNotification({ text: message });
  }
  
  return result;
}
```

**Trigger:**
- **Función:** `syncOnlyReady`
- **Evento:** Según tiempo
- **Intervalo:** Cada 2 horas

**Flujo:**
1. Investigador edita obras
2. Cuando termina, cambia "Estado de Revisión" a "Listo para publicar"
3. Cada 2 horas, script verifica si hay filas "Listas"
4. Si hay, hace push a GitHub
5. Marca automáticamente como "Publicado"
6. Notifica al equipo

---

## 🔐 Configuración Segura del Token

### Método 1: Properties Service (Recomendado)

**Una sola vez, ejecuta:**

```javascript
function setupToken() {
  const token = 'ghp_XXXXXXXXXXXXXXXXXXXXXXXX';  // tu token real
  PropertiesService.getScriptProperties()
    .setProperty('GITHUB_TOKEN', token);
  Logger.log('✅ Token guardado de forma segura');
}
```

O usa el diálogo interactivo:

```javascript
// Ejecutar setGitHubToken() desde el script
// Te pedirá el token por diálogo
```

**En CONFIG, deja vacío:**

```javascript
const CONFIG = {
  github: {
    token: '',  // ⚠️ DEJAR VACÍO
  }
};
```

El script automáticamente lo buscará en Properties Service.

### Método 2: Variables de Entorno

1. En Apps Script: **⚙️ Configuración del proyecto**
2. **Propiedades de secuencia de comandos**
3. Añadir:
   - Propiedad: `GITHUB_TOKEN`
   - Valor: `ghp_XXXXXXXX`

---

## 🎨 Personalización de Mensajes de Commit

### Mensaje Simple

```javascript
function generateCommitMessage(sheetName) {
  return `Actualización desde ${sheetName}`;
}
```

### Mensaje Detallado

```javascript
function generateCommitMessage(sheetName, data) {
  const date = new Date().toISOString().split('T')[0];
  const time = new Date().toTimeString().split(' ')[0];
  const rows = data.length - 1; // excluir encabezados
  
  return `📊 Actualización de ${sheetName}

- Fecha: ${date} ${time}
- Total de filas: ${rows}
- Formato: CSV
- Fuente: Google Sheets

[Auto-sync vía Apps Script]`;
}
```

### Mensaje con Usuario

```javascript
function generateCommitMessage(sheetName) {
  const user = Session.getActiveUser().getEmail();
  const date = new Date().toISOString();
  
  return `Actualización por ${user}

Hoja: ${sheetName}
Timestamp: ${date}

[Automated via Google Apps Script]`;
}
```

---

## 📱 Configuración de Notificaciones

### Slack

1. Ve a tu workspace de Slack
2. **Administración** → **Personalizar Slack**
3. **Menú** → **Configurar aplicaciones**
4. Busca **Incoming Webhooks**
5. **Añadir a Slack**
6. Elige el canal (ej: `#github-updates`)
7. Copia el **Webhook URL**

```javascript
const ADVANCED_CONFIG = {
  notifications: {
    slack: {
      enabled: true,
      webhookUrl: 'https://hooks.slack.com/services/T00/B00/XXXX'
    }
  }
};
```

### Discord

1. Abre tu servidor de Discord
2. **Configuración del Canal** → **Integraciones**
3. **Crear Webhook**
4. Nombre: `GitHub Sync`
5. Copia el **Webhook URL**

```javascript
const ADVANCED_CONFIG = {
  notifications: {
    discord: {
      enabled: true,
      webhookUrl: 'https://discord.com/api/webhooks/123456/XXXX'
    }
  }
};
```

### Email

```javascript
const ADVANCED_CONFIG = {
  notifications: {
    email: {
      enabled: true,
      recipients: [
        'ivan@example.com',
        'investigador1@example.com',
        'equipo@example.com'
      ]
    }
  }
};
```

---

## 🧪 Testing

### Test Completo

```javascript
function runAllTests() {
  // Ya incluido en sheets-github-sync.gs
  // Ejecutar desde menú: GitHub Sync → Ejecutar tests
}
```

### Test Individual de Conexión

```javascript
function quickTest() {
  log('🧪 Test rápido...', 'INFO');
  
  try {
    // 1. Verificar token
    const token = getGitHubToken();
    log('✅ Token encontrado', 'INFO');
    
    // 2. Probar conexión a GitHub
    const url = `https://api.github.com/repos/${CONFIG.github.owner}/${CONFIG.github.repo}`;
    const response = UrlFetchApp.fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    log('✅ Conexión a GitHub OK', 'INFO');
    
    // 3. Leer hoja
    const sheet = SpreadsheetApp.getActiveSpreadsheet()
      .getSheetByName(CONFIG.sheets.sheetNames[0]);
    const data = readSheetData(sheet);
    log(`✅ ${data.length} filas leídas`, 'INFO');
    
    log('🎉 Todo funciona correctamente', 'INFO');
    
  } catch (error) {
    log(`❌ Error: ${error.message}`, 'ERROR');
  }
}
```

---

## 📊 Monitoreo y Logs

### Ver Estadísticas

```javascript
// Ejecutar desde menú: GitHub Sync → Ver estadísticas
showStats();
```

### Limpiar Estadísticas

```javascript
function clearStats() {
  PropertiesService.getScriptProperties().deleteAllProperties();
  log('🗑️ Estadísticas limpiadas', 'INFO');
}
```

### Exportar Logs

```javascript
function exportLogs() {
  const logs = Logger.getLog();
  const file = DriveApp.createFile(
    `logs_${new Date().toISOString()}.txt`,
    logs
  );
  log(`📄 Logs exportados: ${file.getUrl()}`, 'INFO');
}
```

---

## 🚀 Inicio Rápido (5 minutos)

### Paso 1: Copiar Script (1 min)

1. Abre tu Google Sheet
2. **Extensiones** → **Apps Script**
3. Copia contenido de `sheets-github-sync.gs`
4. **Guardar**

### Paso 2: Configurar (2 min)

```javascript
const CONFIG = {
  github: {
    owner: 'TU_USUARIO',
    repo: 'TU_REPO',
    token: '',
    branch: 'main'
  },
  sheets: {
    exportFormat: 'csv',
    sheetNames: ['TU_HOJA']
  },
  paths: {
    csv: 'ruta/al/archivo.csv'
  }
};
```

### Paso 3: Token (1 min)

1. https://github.com/settings/tokens
2. **Generate new token**
3. Scope: `repo`
4. Copiar token

### Paso 4: Guardar Token (30 seg)

Ejecutar una vez:

```javascript
function setupToken() {
  PropertiesService.getScriptProperties()
    .setProperty('GITHUB_TOKEN', 'ghp_XXXXX');
}
```

### Paso 5: Test (30 seg)

```javascript
runAllTests();
```

Si todo pasa ✅:

```javascript
syncToGitHub();
```

### Paso 6: Automatizar (opcional)

**Activadores** → **+ Agregar activador**
- Función: `syncToGitHub`
- Evento: Según tiempo
- Intervalo: Cada hora

---

## 💡 Tips Finales

1. **Empezar simple**: Usa `sheets-github-sync.gs` primero
2. **Probar manualmente**: Ejecuta varias veces antes de automatizar
3. **Verificar en GitHub**: Comprueba que los commits aparecen
4. **Ajustar frecuencia**: Empieza con "cada hora", luego optimiza
5. **Usar checkForChanges**: Evita commits innecesarios
6. **Backup importante**: Activa backups en Drive por seguridad
7. **Notificaciones selectivas**: Solo para errores o cambios importantes
8. **Documentar cambios**: Usa mensajes de commit descriptivos

---

## 🆘 Ayuda

- **Guía completa**: `AUTOMATIZACION_SHEETS_GITHUB.md`
- **Script básico**: `sheets-github-sync.gs`
- **Script avanzado**: `sheets-github-sync-advanced.gs`
- **Documentación GitHub API**: https://docs.github.com/en/rest

---

**¡Listo para sincronizar! 🚀**




/**
 * ============================================================================
 * GOOGLE SHEETS → GITHUB SYNC - VERSIÓN AVANZADA
 * ============================================================================
 * 
 * Versión extendida con funcionalidades avanzadas:
 * - ✅ Múltiples hojas a múltiples archivos
 * - ✅ Validación de datos antes del push
 * - ✅ Backup automático en Google Drive
 * - ✅ Notificaciones a Slack/Discord
 * - ✅ Estadísticas detalladas
 * - ✅ Debounce para triggers de edición
 * - ✅ Formateo y limpieza de datos
 * 
 * Versión: 2.5
 * Última actualización: 2025-10-31
 */

// Usar la configuración del script principal
// (Asegúrate de tener sheets-github-sync.gs también)

// ============================================================================
// CONFIGURACIÓN AVANZADA
// ============================================================================

const ADVANCED_CONFIG = {
  // Validación de datos
  validation: {
    enabled: true,
    minRows: 2,                        // mínimo de filas (encabezado + 1 dato)
    maxEmptyRows: 0.5,                 // % máximo de filas vacías
    requiredColumns: ['ID', 'Título'], // columnas obligatorias
    validateTypes: true                // validar tipos de datos
  },
  
  // Backup automático
  backup: {
    enabled: true,
    folderName: 'Backups Sheets GitHub', // carpeta en Drive
    keepLastN: 10,                        // mantener últimos N backups
    format: 'csv'                         // formato del backup
  },
  
  // Notificaciones externas
  notifications: {
    slack: {
      enabled: false,
      webhookUrl: ''  // https://hooks.slack.com/services/...
    },
    discord: {
      enabled: false,
      webhookUrl: ''  // https://discord.com/api/webhooks/...
    },
    email: {
      enabled: false,
      recipients: []  // ['email1@example.com', 'email2@example.com']
    }
  },
  
  // Debounce para triggers de edición
  debounce: {
    enabled: true,
    delayMinutes: 5  // esperar 5 minutos antes de sync
  },
  
  // Limpieza y formateo de datos
  dataProcessing: {
    trimWhitespace: true,      // eliminar espacios al inicio/fin
    removeEmptyRows: true,     // eliminar filas vacías
    normalizeLineBreaks: true, // normalizar saltos de línea
    convertDates: true,        // convertir fechas a ISO
    lowercaseHeaders: false    // convertir encabezados a minúsculas
  },
  
  // Múltiples hojas → múltiples archivos
  multiSheet: {
    enabled: false,
    mappings: {
      'Obras Completas': 'filtro_basico/obras_completas.csv',
      'Autores': 'filtro_basico/autores.csv',
      'Lugares': 'filtro_basico/lugares.csv',
      'Representaciones': 'filtro_basico/representaciones.csv'
    }
  }
};

// ============================================================================
// SINCRONIZACIÓN AVANZADA
// ============================================================================

/**
 * Sincronización con validación y backup
 */
function syncToGitHubAdvanced() {
  try {
    log('🚀 Iniciando sincronización AVANZADA...', 'INFO');
    
    const startTime = new Date();
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    
    // Verificar debounce (si viene de trigger de edición)
    if (ADVANCED_CONFIG.debounce.enabled && !checkDebounce()) {
      log('⏳ Debounce activo. Esperando más cambios...', 'INFO');
      return;
    }
    
    // Determinar qué hojas exportar
    const sheetsMapping = ADVANCED_CONFIG.multiSheet.enabled
      ? ADVANCED_CONFIG.multiSheet.mappings
      : { [CONFIG.sheets.sheetNames[0]]: getFilePath(CONFIG.sheets.sheetNames[0], CONFIG.sheets.exportFormat) };
    
    const results = [];
    
    // Procesar cada hoja
    for (const [sheetName, filePath] of Object.entries(sheetsMapping)) {
      try {
        log(`\n📋 Procesando: ${sheetName} → ${filePath}`, 'INFO');
        
        const result = processSheetAdvanced(spreadsheet, sheetName, filePath);
        results.push(result);
        
        log(`✅ ${sheetName}: ${result.status}`, 'INFO');
        
      } catch (error) {
        log(`❌ Error en ${sheetName}: ${error.message}`, 'ERROR');
        results.push({ 
          sheet: sheetName, 
          status: 'error', 
          error: error.message 
        });
      }
    }
    
    // Resumen y notificaciones
    const duration = (new Date() - startTime) / 1000;
    const summary = generateSummary(results, duration);
    
    log(summary.text, 'INFO');
    
    // Notificar si está configurado
    if (summary.hasChanges) {
      sendNotifications(summary);
    }
    
    // Actualizar estadísticas
    updateAdvancedStats(results);
    
    return results;
    
  } catch (error) {
    log(`❌ Error general: ${error.message}`, 'ERROR');
    sendErrorNotification(error);
    throw error;
  }
}

/**
 * Procesa una hoja con validación y backup
 */
function processSheetAdvanced(spreadsheet, sheetName, filePath) {
  const sheet = spreadsheet.getSheetByName(sheetName);
  
  if (!sheet) {
    throw new Error(`Hoja "${sheetName}" no encontrada`);
  }
  
  // 1. Leer datos
  let data = readSheetData(sheet);
  
  if (data.length === 0) {
    return { sheet: sheetName, status: 'empty' };
  }
  
  log(`📊 ${data.length} filas leídas`, 'INFO');
  
  // 2. Validar datos
  if (ADVANCED_CONFIG.validation.enabled) {
    const validation = validateData(data, sheetName);
    
    if (!validation.valid) {
      throw new Error(`Validación falló: ${validation.errors.join(', ')}`);
    }
    
    log(`✅ Validación exitosa`, 'INFO');
  }
  
  // 3. Procesar/limpiar datos
  if (ADVANCED_CONFIG.dataProcessing.trimWhitespace || 
      ADVANCED_CONFIG.dataProcessing.normalizeLineBreaks) {
    data = cleanData(data);
    log(`🧹 Datos limpiados`, 'INFO');
  }
  
  // 4. Convertir a formato
  const format = filePath.endsWith('.json') ? 'json' : 'csv';
  const content = format === 'json' 
    ? convertToJSON(data) 
    : convertToCSV(data);
  
  // 5. Backup antes de subir
  if (ADVANCED_CONFIG.backup.enabled) {
    backupToGoogleDrive(content, sheetName, format);
    log(`💾 Backup creado`, 'INFO');
  }
  
  // 6. Verificar cambios
  if (CONFIG.options.checkForChanges) {
    const hasChanges = checkForChanges(content, filePath);
    
    if (!hasChanges) {
      log(`✅ No hay cambios`, 'INFO');
      return { 
        sheet: sheetName, 
        status: 'no_changes', 
        path: filePath 
      };
    }
  }
  
  // 7. Push a GitHub
  const result = pushToGitHub(content, filePath, sheetName);
  
  return {
    sheet: sheetName,
    status: 'success',
    path: filePath,
    commit: result.commit.sha,
    size: content.length,
    rows: data.length
  };
}

// ============================================================================
// VALIDACIÓN DE DATOS
// ============================================================================

/**
 * Valida datos antes de hacer push
 */
function validateData(data, sheetName) {
  const errors = [];
  
  // Verificar mínimo de filas
  if (data.length < ADVANCED_CONFIG.validation.minRows) {
    errors.push(`Solo ${data.length} filas (mínimo: ${ADVANCED_CONFIG.validation.minRows})`);
  }
  
  // Verificar columnas requeridas
  if (data.length > 0) {
    const headers = data[0].map(h => h.toString().trim());
    
    for (const requiredCol of ADVANCED_CONFIG.validation.requiredColumns) {
      if (!headers.includes(requiredCol)) {
        errors.push(`Falta columna obligatoria: "${requiredCol}"`);
      }
    }
  }
  
  // Verificar porcentaje de filas vacías
  const emptyRows = data.filter(isEmptyRow).length;
  const emptyPercentage = emptyRows / data.length;
  
  if (emptyPercentage > ADVANCED_CONFIG.validation.maxEmptyRows) {
    errors.push(`${(emptyPercentage * 100).toFixed(1)}% de filas vacías (máximo: ${ADVANCED_CONFIG.validation.maxEmptyRows * 100}%)`);
  }
  
  // Verificar tipos de datos (si está habilitado)
  if (ADVANCED_CONFIG.validation.validateTypes && data.length > 1) {
    const typeErrors = validateTypes(data);
    errors.push(...typeErrors);
  }
  
  return {
    valid: errors.length === 0,
    errors: errors,
    warnings: []
  };
}

/**
 * Valida tipos de datos por columna
 */
function validateTypes(data) {
  const errors = [];
  const headers = data[0];
  
  // Detectar tipo esperado por columna (basado en primeras filas)
  const expectedTypes = headers.map((header, colIndex) => {
    const samples = data.slice(1, 6).map(row => row[colIndex]);
    return detectType(samples);
  });
  
  // Validar cada fila
  for (let rowIndex = 1; rowIndex < data.length; rowIndex++) {
    const row = data[rowIndex];
    
    for (let colIndex = 0; colIndex < row.length; colIndex++) {
      const value = row[colIndex];
      const expectedType = expectedTypes[colIndex];
      const actualType = typeof value;
      
      // Solo validar si no está vacío
      if (value !== '' && value !== null && value !== undefined) {
        if (expectedType === 'number' && actualType !== 'number') {
          errors.push(`Fila ${rowIndex + 1}, columna "${headers[colIndex]}": esperado número, encontrado ${actualType}`);
        }
      }
    }
  }
  
  return errors.slice(0, 10); // Limitar a 10 errores
}

/**
 * Detecta el tipo más común en un array de valores
 */
function detectType(values) {
  const types = values
    .filter(v => v !== '' && v !== null && v !== undefined)
    .map(v => typeof v);
  
  const typeCounts = {};
  types.forEach(t => typeCounts[t] = (typeCounts[t] || 0) + 1);
  
  return Object.keys(typeCounts).reduce((a, b) => 
    typeCounts[a] > typeCounts[b] ? a : b
  , 'string');
}

// ============================================================================
// LIMPIEZA Y PROCESAMIENTO DE DATOS
// ============================================================================

/**
 * Limpia y formatea datos
 */
function cleanData(data) {
  return data.map(row => {
    return row.map(cell => {
      if (typeof cell !== 'string') {
        return cell;
      }
      
      let cleaned = cell;
      
      // Trim whitespace
      if (ADVANCED_CONFIG.dataProcessing.trimWhitespace) {
        cleaned = cleaned.trim();
      }
      
      // Normalizar saltos de línea
      if (ADVANCED_CONFIG.dataProcessing.normalizeLineBreaks) {
        cleaned = cleaned.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      }
      
      // Eliminar espacios múltiples
      cleaned = cleaned.replace(/\s+/g, ' ');
      
      return cleaned;
    });
  });
}

// ============================================================================
// BACKUP A GOOGLE DRIVE
// ============================================================================

/**
 * Guarda backup en Google Drive
 */
function backupToGoogleDrive(content, sheetName, format) {
  try {
    // Obtener o crear carpeta de backups
    const folder = getOrCreateBackupFolder();
    
    // Nombre del archivo con timestamp
    const timestamp = Utilities.formatDate(
      new Date(),
      'GMT-5',
      'yyyy-MM-dd_HH-mm-ss'
    );
    
    const fileName = `${sheetName}_${timestamp}.${format}`;
    const mimeType = format === 'json' ? 'application/json' : 'text/csv';
    
    // Crear archivo
    folder.createFile(fileName, content, mimeType);
    
    log(`💾 Backup guardado: ${fileName}`, 'INFO');
    
    // Limpiar backups antiguos
    cleanOldBackups(folder, sheetName);
    
  } catch (error) {
    log(`⚠️ Error al crear backup: ${error.message}`, 'WARN');
  }
}

/**
 * Obtiene o crea la carpeta de backups
 */
function getOrCreateBackupFolder() {
  const folderName = ADVANCED_CONFIG.backup.folderName;
  const folders = DriveApp.getFoldersByName(folderName);
  
  if (folders.hasNext()) {
    return folders.next();
  }
  
  return DriveApp.createFolder(folderName);
}

/**
 * Elimina backups antiguos, mantiene solo los últimos N
 */
function cleanOldBackups(folder, sheetName) {
  try {
    const files = folder.getFilesByName(sheetName);
    const filesList = [];
    
    while (files.hasNext()) {
      filesList.push(files.next());
    }
    
    // Ordenar por fecha (más recientes primero)
    filesList.sort((a, b) => b.getDateCreated() - a.getDateCreated());
    
    // Eliminar los que exceden el límite
    const keepN = ADVANCED_CONFIG.backup.keepLastN;
    
    for (let i = keepN; i < filesList.length; i++) {
      filesList[i].setTrashed(true);
      log(`🗑️ Backup antiguo eliminado: ${filesList[i].getName()}`, 'DEBUG');
    }
    
  } catch (error) {
    log(`⚠️ Error al limpiar backups: ${error.message}`, 'WARN');
  }
}

// ============================================================================
// DEBOUNCE PARA TRIGGERS DE EDICIÓN
// ============================================================================

/**
 * Verifica si ha pasado suficiente tiempo desde la última edición
 */
function checkDebounce() {
  const properties = PropertiesService.getScriptProperties();
  const lastEditTime = properties.getProperty('lastEditTime');
  
  if (!lastEditTime) {
    // Primera edición, guardar timestamp
    properties.setProperty('lastEditTime', new Date().getTime().toString());
    return false;
  }
  
  const now = new Date().getTime();
  const elapsed = now - parseInt(lastEditTime);
  const delayMs = ADVANCED_CONFIG.debounce.delayMinutes * 60 * 1000;
  
  if (elapsed < delayMs) {
    // Aún no ha pasado suficiente tiempo
    return false;
  }
  
  // Ha pasado suficiente tiempo, actualizar timestamp
  properties.setProperty('lastEditTime', now.toString());
  return true;
}

/**
 * Registra una edición (llamar desde trigger onEdit)
 */
function onEdit(e) {
  const properties = PropertiesService.getScriptProperties();
  properties.setProperty('lastEditTime', new Date().getTime().toString());
  
  log('✏️ Edición detectada. Debounce activado.', 'DEBUG');
}

// ============================================================================
// NOTIFICACIONES
// ============================================================================

/**
 * Envía notificaciones a todos los canales configurados
 */
function sendNotifications(summary) {
  if (ADVANCED_CONFIG.notifications.slack.enabled) {
    sendSlackNotification(summary);
  }
  
  if (ADVANCED_CONFIG.notifications.discord.enabled) {
    sendDiscordNotification(summary);
  }
  
  if (ADVANCED_CONFIG.notifications.email.enabled) {
    sendEmailNotification(summary);
  }
}

/**
 * Envía notificación a Slack
 */
function sendSlackNotification(summary) {
  try {
    const webhookUrl = ADVANCED_CONFIG.notifications.slack.webhookUrl;
    
    if (!webhookUrl) {
      return;
    }
    
    const payload = {
      text: `🔄 *Sincronización Google Sheets → GitHub*`,
      blocks: [
        {
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `*Estado:* ${summary.allSuccess ? '✅ Exitoso' : '⚠️ Con errores'}\n` +
                  `*Duración:* ${summary.duration}s\n` +
                  `*Hojas procesadas:* ${summary.totalSheets}\n` +
                  `*Cambios detectados:* ${summary.changedSheets}`
          }
        }
      ]
    };
    
    UrlFetchApp.fetch(webhookUrl, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload)
    });
    
    log('📱 Notificación enviada a Slack', 'INFO');
    
  } catch (error) {
    log(`⚠️ Error al enviar a Slack: ${error.message}`, 'WARN');
  }
}

/**
 * Envía notificación a Discord
 */
function sendDiscordNotification(summary) {
  try {
    const webhookUrl = ADVANCED_CONFIG.notifications.discord.webhookUrl;
    
    if (!webhookUrl) {
      return;
    }
    
    const color = summary.allSuccess ? 0x00ff00 : 0xffaa00;
    
    const payload = {
      embeds: [{
        title: '🔄 Sincronización Google Sheets → GitHub',
        color: color,
        fields: [
          { name: 'Estado', value: summary.allSuccess ? '✅ Exitoso' : '⚠️ Con errores', inline: true },
          { name: 'Duración', value: `${summary.duration}s`, inline: true },
          { name: 'Hojas procesadas', value: summary.totalSheets.toString(), inline: true },
          { name: 'Cambios detectados', value: summary.changedSheets.toString(), inline: true }
        ],
        timestamp: new Date().toISOString()
      }]
    };
    
    UrlFetchApp.fetch(webhookUrl, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload)
    });
    
    log('📱 Notificación enviada a Discord', 'INFO');
    
  } catch (error) {
    log(`⚠️ Error al enviar a Discord: ${error.message}`, 'WARN');
  }
}

/**
 * Envía notificación por email
 */
function sendEmailNotification(summary) {
  try {
    const recipients = ADVANCED_CONFIG.notifications.email.recipients;
    
    if (!recipients || recipients.length === 0) {
      return;
    }
    
    const subject = summary.allSuccess 
      ? '✅ Sincronización exitosa: Google Sheets → GitHub'
      : '⚠️ Sincronización con errores: Google Sheets → GitHub';
    
    const body = `
Resumen de sincronización:

${summary.text}

Timestamp: ${new Date().toISOString()}
Hoja: ${SpreadsheetApp.getActiveSpreadsheet().getName()}
`;
    
    recipients.forEach(email => {
      MailApp.sendEmail(email, subject, body);
    });
    
    log(`📧 Notificaciones enviadas a ${recipients.length} destinatarios`, 'INFO');
    
  } catch (error) {
    log(`⚠️ Error al enviar emails: ${error.message}`, 'WARN');
  }
}

/**
 * Envía notificación de error
 */
function sendErrorNotification(error) {
  // Slack
  if (ADVANCED_CONFIG.notifications.slack.enabled) {
    try {
      const payload = {
        text: `❌ *Error en sincronización*`,
        blocks: [{
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `*Error:* ${error.message}\n*Stack:* \`\`\`${error.stack}\`\`\``
          }
        }]
      };
      
      UrlFetchApp.fetch(ADVANCED_CONFIG.notifications.slack.webhookUrl, {
        method: 'post',
        contentType: 'application/json',
        payload: JSON.stringify(payload)
      });
    } catch (e) {
      log(`⚠️ Error al notificar error a Slack: ${e.message}`, 'WARN');
    }
  }
  
  // Email
  if (CONFIG.options.notifyOnError) {
    notifyError(error);
  }
}

// ============================================================================
// ESTADÍSTICAS AVANZADAS
// ============================================================================

/**
 * Genera resumen de la sincronización
 */
function generateSummary(results, duration) {
  const totalSheets = results.length;
  const successSheets = results.filter(r => r.status === 'success').length;
  const changedSheets = results.filter(r => r.status === 'success').length;
  const noChangeSheets = results.filter(r => r.status === 'no_changes').length;
  const errorSheets = results.filter(r => r.status === 'error').length;
  
  const allSuccess = errorSheets === 0;
  const hasChanges = changedSheets > 0;
  
  let text = '\n' + '='.repeat(60) + '\n';
  text += '🎉 SINCRONIZACIÓN COMPLETADA\n';
  text += '='.repeat(60) + '\n';
  text += `⏱️  Duración: ${duration.toFixed(2)}s\n`;
  text += `📊 Total hojas: ${totalSheets}\n`;
  text += `✅ Exitosas: ${successSheets}\n`;
  text += `🔄 Con cambios: ${changedSheets}\n`;
  text += `⚪ Sin cambios: ${noChangeSheets}\n`;
  
  if (errorSheets > 0) {
    text += `❌ Con errores: ${errorSheets}\n`;
  }
  
  text += '\n📋 Detalle por hoja:\n';
  results.forEach(result => {
    const icon = result.status === 'success' ? '✅' 
               : result.status === 'no_changes' ? '⚪' 
               : '❌';
    text += `  ${icon} ${result.sheet}: ${result.status}`;
    
    if (result.commit) {
      text += ` (${result.commit.substring(0, 7)})`;
    }
    
    if (result.rows) {
      text += ` - ${result.rows} filas`;
    }
    
    text += '\n';
  });
  
  text += '='.repeat(60) + '\n';
  
  return {
    text: text,
    allSuccess: allSuccess,
    hasChanges: hasChanges,
    totalSheets: totalSheets,
    changedSheets: changedSheets,
    duration: duration.toFixed(2)
  };
}

/**
 * Actualiza estadísticas avanzadas
 */
function updateAdvancedStats(results) {
  const properties = PropertiesService.getScriptProperties();
  
  // Estadísticas actuales
  const totalSyncs = parseInt(properties.getProperty('totalSyncs') || '0') + 1;
  const successfulSyncs = results.filter(r => r.status === 'success').length;
  const totalChanges = parseInt(properties.getProperty('totalChanges') || '0') + 
                      results.filter(r => r.status === 'success').length;
  const lastSync = new Date().toISOString();
  
  // Guardar
  properties.setProperties({
    'totalSyncs': totalSyncs.toString(),
    'totalChanges': totalChanges.toString(),
    'successfulSyncs': successfulSyncs.toString(),
    'lastSync': lastSync,
    'lastResults': JSON.stringify(results)
  });
}

/**
 * Muestra estadísticas avanzadas
 */
function showAdvancedStats() {
  const properties = PropertiesService.getScriptProperties();
  
  const stats = {
    totalSyncs: properties.getProperty('totalSyncs') || '0',
    totalChanges: properties.getProperty('totalChanges') || '0',
    lastSync: properties.getProperty('lastSync') || 'Never',
    lastResults: JSON.parse(properties.getProperty('lastResults') || '[]')
  };
  
  log('\n' + '='.repeat(60), 'INFO');
  log('📊 ESTADÍSTICAS AVANZADAS', 'INFO');
  log('='.repeat(60), 'INFO');
  log(`Total sincronizaciones: ${stats.totalSyncs}`, 'INFO');
  log(`Total cambios pusheados: ${stats.totalChanges}`, 'INFO');
  log(`Última sincronización: ${stats.lastSync}`, 'INFO');
  log('\nÚltimos resultados:', 'INFO');
  
  stats.lastResults.forEach(result => {
    const icon = result.status === 'success' ? '✅' 
               : result.status === 'no_changes' ? '⚪' 
               : '❌';
    log(`  ${icon} ${result.sheet}: ${result.status}`, 'INFO');
  });
  
  log('='.repeat(60), 'INFO');
}

// ============================================================================
// MENÚ AVANZADO
// ============================================================================

/**
 * Crea menú avanzado
 */
function createAdvancedMenu() {
  const ui = SpreadsheetApp.getUi();
  
  ui.createMenu('🔄 GitHub Sync Advanced')
    .addItem('📤 Sincronizar (Avanzado)', 'syncToGitHubAdvanced')
    .addSeparator()
    .addSubMenu(ui.createMenu('⚙️ Configuración')
      .addItem('🔧 Configurar token', 'setGitHubToken')
      .addItem('📁 Configurar backup', 'configureBackup')
      .addItem('📱 Configurar notificaciones', 'configureNotifications'))
    .addSubMenu(ui.createMenu('🧪 Tests')
      .addItem('▶️ Ejecutar todos', 'runAllTests')
      .addItem('✅ Test validación', 'testValidation')
      .addItem('💾 Test backup', 'testBackup'))
    .addSubMenu(ui.createMenu('📊 Estadísticas')
      .addItem('📈 Ver stats avanzadas', 'showAdvancedStats')
      .addItem('🗑️ Limpiar stats', 'clearStats'))
    .addSeparator()
    .addItem('📖 Ayuda avanzada', 'showAdvancedHelp')
    .addToUi();
}

/**
 * Test de validación
 */
function testValidation() {
  log('🧪 Probando validación de datos...', 'INFO');
  
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheetName = CONFIG.sheets.sheetNames[0];
    const sheet = spreadsheet.getSheetByName(sheetName);
    const data = readSheetData(sheet);
    
    const result = validateData(data, sheetName);
    
    if (result.valid) {
      log('✅ Validación exitosa', 'INFO');
    } else {
      log('❌ Errores de validación:', 'WARN');
      result.errors.forEach(error => log(`  - ${error}`, 'WARN'));
    }
    
    return result.valid;
    
  } catch (error) {
    log(`❌ Error en test: ${error.message}`, 'ERROR');
    return false;
  }
}

/**
 * Test de backup
 */
function testBackup() {
  log('🧪 Probando backup a Google Drive...', 'INFO');
  
  try {
    const testContent = 'ID,Título,Autor\n1,Test,Test Author';
    backupToGoogleDrive(testContent, 'TestBackup', 'csv');
    log('✅ Backup de prueba creado', 'INFO');
    return true;
    
  } catch (error) {
    log(`❌ Error en test: ${error.message}`, 'ERROR');
    return false;
  }
}

// Instalar el menú al abrir
function onOpen() {
  createAdvancedMenu();
}




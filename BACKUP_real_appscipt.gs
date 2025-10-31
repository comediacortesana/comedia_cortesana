/**
 * ============================================================================
 * GOOGLE SHEETS → GITHUB SYNC
 * ============================================================================
 * 
 * Sincroniza automáticamente Google Sheets con GitHub usando la API REST
 * 
 * Características:
 * - ✅ Detección inteligente de cambios (solo push si hay cambios)
 * - ✅ Soporte para múltiples hojas
 * - ✅ Exportación en CSV o JSON
 * - ✅ Manejo robusto de errores
 * - ✅ Logs detallados
 * - ✅ 100% gratuito (sin servidores externos)
 * 
 * Autor: AI Assistant
 * Versión: 2.0
 * Última actualización: 2025-10-31
 */

// ============================================================================
// CONFIGURACIÓN
// ============================================================================

const CONFIG = {
  // Configuración de GitHub
  github: {
    owner: 'comediacortesana',              // ej: 'ivansimo'
    repo: 'comedia_cortesana',        // nombre del repositorio
    token: '',                         // MEJOR: usar getGitHubToken()
    branch: 'main'                     // rama donde hacer push
  },
  
  // Configuración de las hojas
  sheets: {
    exportFormat: 'csv',               // 'csv' o 'json'
    sheetNames: ['obras_completas'],   // hojas a exportar
    exportAll: false,                  // true = exportar todas las hojas
    includeHeaders: true,              // incluir fila de encabezados
    skipEmptyRows: true                // ignorar filas vacías
  },
  
  // Rutas de los archivos en GitHub
  paths: {
    csv: 'obras_completas.csv',       // en la raíz del repositorio
    json: 'datos_obras.json',         // en la raíz del repositorio
    exportBoth: false                  // true = exportar CSV y JSON
  },
  
  // Opciones avanzadas
  options: {
    checkForChanges: true,             // solo push si hay cambios
    enableLogs: true,                  // logs detallados
    notifyOnError: false,              // email si hay error
    emailTo: '',                       // email para notificaciones
    maxRetries: 3,                     // reintentos si falla
    retryDelay: 2000                   // ms entre reintentos
  }
};

// ============================================================================
// FUNCIÓN PRINCIPAL
// ============================================================================

/**
 * Función principal para sincronizar Google Sheets con GitHub
 * Puedes ejecutarla manualmente o configurar un trigger automático
 */
function syncToGitHub() {
  try {
    log('🚀 Iniciando sincronización con GitHub...', 'INFO');
    
    const startTime = new Date();
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    
    // Determinar qué hojas exportar
    const sheetsToExport = CONFIG.sheets.exportAll 
      ? spreadsheet.getSheets().map(s => s.getName())
      : CONFIG.sheets.sheetNames;
    
    log(`📊 Hojas a exportar: ${sheetsToExport.join(', ')}`, 'INFO');
    
    // Procesar cada hoja
    const results = [];
    
    for (const sheetName of sheetsToExport) {
      try {
        const result = processSheet(spreadsheet, sheetName);
        results.push(result);
        log(`✅ ${sheetName}: ${result.status}`, 'INFO');
      } catch (error) {
        log(`❌ Error en ${sheetName}: ${error.message}`, 'ERROR');
        results.push({ sheet: sheetName, status: 'error', error: error.message });
      }
    }
    
    // Resumen
    const duration = (new Date() - startTime) / 1000;
    const successful = results.filter(r => r.status === 'success' || r.status === 'no_changes').length;
    
    log(`\n🎉 Sincronización completada en ${duration.toFixed(2)}s`, 'INFO');
    log(`✅ Exitosas: ${successful}/${results.length}`, 'INFO');
    
    // Guardar estadísticas
    updateStats(results);
    
    return results;
    
  } catch (error) {
    log(`❌ Error general: ${error.message}`, 'ERROR');
    
    if (CONFIG.options.notifyOnError) {
      notifyError(error);
    }
    
    throw error;
  }
}

// ============================================================================
// PROCESAMIENTO DE HOJAS
// ============================================================================

/**
 * Procesa una hoja individual y la sube a GitHub
 */
function processSheet(spreadsheet, sheetName) {
  const sheet = spreadsheet.getSheetByName(sheetName);
  
  if (!sheet) {
    throw new Error(`Hoja "${sheetName}" no encontrada`);
  }
  
  log(`\n📋 Procesando hoja: ${sheetName}`, 'INFO');
  
  // Leer datos de la hoja
  const data = readSheetData(sheet);
  
  if (data.length === 0) {
    log(`⚠️ La hoja "${sheetName}" está vacía`, 'WARN');
    return { sheet: sheetName, status: 'empty' };
  }
  
  log(`✅ ${data.length} filas leídas`, 'INFO');
  
  // Convertir a formato deseado
  const format = CONFIG.sheets.exportFormat;
  const content = format === 'json' 
    ? convertToJSON(data) 
    : convertToCSV(data);
  
  // Determinar ruta del archivo
  const filePath = getFilePath(sheetName, format);
  
  log(`📁 Ruta destino: ${filePath}`, 'INFO');
  
  // Verificar si hay cambios
  if (CONFIG.options.checkForChanges) {
    const hasChanges = checkForChanges(content, filePath);
    
    if (!hasChanges) {
      log('✅ No hay cambios. Skip push.', 'INFO');
      return { sheet: sheetName, status: 'no_changes', path: filePath };
    }
    
    log('🔄 Cambios detectados. Haciendo push...', 'INFO');
  }
  
  // Subir a GitHub
  const result = pushToGitHub(content, filePath, sheetName);
  
  return {
    sheet: sheetName,
    status: 'success',
    path: filePath,
    commit: result.commit.sha,
    size: content.length
  };
}

/**
 * Lee todos los datos de una hoja
 */
function readSheetData(sheet) {
  const lastRow = sheet.getLastRow();
  const lastCol = sheet.getLastColumn();
  
  if (lastRow === 0 || lastCol === 0) {
    return [];
  }
  
  const range = sheet.getRange(1, 1, lastRow, lastCol);
  const values = range.getValues();
  
  // Filtrar filas vacías si está configurado
  if (CONFIG.sheets.skipEmptyRows) {
    return values.filter(row => !isEmptyRow(row));
  }
  
  return values;
}

/**
 * Verifica si una fila está completamente vacía
 */
function isEmptyRow(row) {
  return row.every(cell => cell === '' || cell === null || cell === undefined);
}

// ============================================================================
// CONVERSIÓN DE FORMATOS
// ============================================================================

/**
 * Convierte datos a formato CSV
 */
function convertToCSV(data) {
  return data.map(row => {
    return row.map(cell => {
      // Convertir a string
      let value = cell !== null && cell !== undefined ? cell.toString() : '';
      
      // Escapar comillas dobles
      value = value.replace(/"/g, '""');
      
      // Envolver en comillas si contiene coma, salto de línea o comillas
      if (value.includes(',') || value.includes('\n') || value.includes('"')) {
        value = `"${value}"`;
      }
      
      return value;
    }).join(',');
  }).join('\n');
}

/**
 * Convierte datos a formato JSON
 */
function convertToJSON(data) {
  if (data.length === 0) {
    return JSON.stringify([]);
  }
  
  // Primera fila = encabezados
  const headers = data[0].map(h => h.toString().trim());
  
  // Resto de filas = datos
  const rows = data.slice(1);
  
  // Convertir a array de objetos
  const jsonData = rows.map(row => {
    const obj = {};
    
    headers.forEach((header, index) => {
      let value = row[index];
      
      // Convertir tipos de datos
      if (value === '') {
        value = null;
      } else if (typeof value === 'number') {
        // Mantener números
      } else if (value instanceof Date) {
        value = value.toISOString().split('T')[0];
      } else if (typeof value === 'string') {
        // Intentar convertir strings numéricos
        const num = parseFloat(value);
        if (!isNaN(num) && num.toString() === value) {
          value = num;
        }
      }
      
      obj[header] = value;
    });
    
    return obj;
  });
  
  // Exportar con indentación para legibilidad (o sin ella para tamaño)
  return JSON.stringify(jsonData, null, 2);
}

// ============================================================================
// DETECCIÓN DE CAMBIOS
// ============================================================================

/**
 * Verifica si el contenido ha cambiado comparado con GitHub
 * Retorna true si hay cambios, false si es idéntico
 */
function checkForChanges(newContent, filePath) {
  try {
    // Obtener contenido actual de GitHub
    const currentContent = getFileFromGitHub(filePath);
    
    if (currentContent === null) {
      // Archivo no existe en GitHub = hay cambios
      return true;
    }
    
    // Calcular hash del contenido nuevo
    const newHash = calculateHash(newContent);
    const currentHash = calculateHash(currentContent);
    
    log(`🔍 Hash actual: ${currentHash}`, 'DEBUG');
    log(`🔍 Hash nuevo:  ${newHash}`, 'DEBUG');
    
    return newHash !== currentHash;
    
  } catch (error) {
    // Si hay error al obtener archivo, asumir que hay cambios
    log(`⚠️ No se pudo verificar cambios: ${error.message}`, 'WARN');
    return true;
  }
}

/**
 * Calcula SHA-256 hash de un string
 */
function calculateHash(content) {
  const hash = Utilities.computeDigest(
    Utilities.DigestAlgorithm.SHA_256,
    content,
    Utilities.Charset.UTF_8
  );
  
  return hash.map(byte => {
    const v = (byte < 0) ? 256 + byte : byte;
    return ('0' + v.toString(16)).slice(-2);
  }).join('');
}

// ============================================================================
// INTERACCIÓN CON GITHUB API
// ============================================================================

/**
 * Obtiene un archivo desde GitHub
 * Retorna el contenido o null si no existe
 */
function getFileFromGitHub(filePath) {
  const token = getGitHubToken();
  const url = `https://api.github.com/repos/${CONFIG.github.owner}/${CONFIG.github.repo}/contents/${filePath}?ref=${CONFIG.github.branch}`;
  
  const options = {
    method: 'get',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/vnd.github.v3+json'
    },
    muteHttpExceptions: true
  };
  
  const response = UrlFetchApp.fetch(url, options);
  const statusCode = response.getResponseCode();
  
  if (statusCode === 404) {
    // Archivo no existe
    return null;
  }
  
  if (statusCode !== 200) {
    throw new Error(`GitHub API error: ${statusCode} - ${response.getContentText()}`);
  }
  
  const data = JSON.parse(response.getContentText());
  
  // Decodificar contenido de base64
  return Utilities.newBlob(
    Utilities.base64Decode(data.content)
  ).getDataAsString();
}

/**
 * Sube contenido a GitHub usando la API
 */
function pushToGitHub(content, filePath, sheetName) {
  const token = getGitHubToken();
  const url = `https://api.github.com/repos/${CONFIG.github.owner}/${CONFIG.github.repo}/contents/${filePath}`;
  
  // Codificar contenido en base64
  const contentBase64 = Utilities.base64Encode(content);
  
  // Obtener SHA del archivo actual (si existe)
  let sha = null;
  try {
    const fileInfo = getFileInfo(filePath);
    sha = fileInfo ? fileInfo.sha : null;
  } catch (error) {
    // Archivo no existe, sha = null
  }
  
  // Mensaje de commit
  const commitMessage = generateCommitMessage(sheetName);
  
  // Payload para la API
  const payload = {
    message: commitMessage,
    content: contentBase64,
    branch: CONFIG.github.branch
  };
  
  if (sha) {
    payload.sha = sha;
  }
  
  // Opciones de la petición
  const options = {
    method: 'put',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json'
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };
  
  // Hacer petición con reintentos
  let lastError;
  
  for (let attempt = 1; attempt <= CONFIG.options.maxRetries; attempt++) {
    try {
      const response = UrlFetchApp.fetch(url, options);
      const statusCode = response.getResponseCode();
      
      if (statusCode === 200 || statusCode === 201) {
        const result = JSON.parse(response.getContentText());
        log(`✅ Push exitoso. Commit: ${result.commit.sha}`, 'INFO');
        return result;
      }
      
      throw new Error(`GitHub API error: ${statusCode} - ${response.getContentText()}`);
      
    } catch (error) {
      lastError = error;
      log(`⚠️ Intento ${attempt}/${CONFIG.options.maxRetries} falló: ${error.message}`, 'WARN');
      
      if (attempt < CONFIG.options.maxRetries) {
        Utilities.sleep(CONFIG.options.retryDelay);
      }
    }
  }
  
  throw lastError;
}

/**
 * Obtiene información de un archivo en GitHub
 */
function getFileInfo(filePath) {
  const token = getGitHubToken();
  const url = `https://api.github.com/repos/${CONFIG.github.owner}/${CONFIG.github.repo}/contents/${filePath}?ref=${CONFIG.github.branch}`;
  
  const options = {
    method: 'get',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/vnd.github.v3+json'
    },
    muteHttpExceptions: true
  };
  
  const response = UrlFetchApp.fetch(url, options);
  const statusCode = response.getResponseCode();
  
  if (statusCode === 404) {
    return null;
  }
  
  if (statusCode !== 200) {
    throw new Error(`GitHub API error: ${statusCode}`);
  }
  
  return JSON.parse(response.getContentText());
}

// ============================================================================
// UTILIDADES
// ============================================================================

/**
 * Obtiene el token de GitHub de forma segura
 * Prioridad: 1. Properties Service, 2. CONFIG
 */
function getGitHubToken() {
  // Intentar obtener de Properties Service (recomendado)
  const properties = PropertiesService.getScriptProperties();
  const token = properties.getProperty('GITHUB_TOKEN');
  
  if (token) {
    return token;
  }
  
  // Fallback a CONFIG
  if (CONFIG.github.token) {
    return CONFIG.github.token;
  }
  
  throw new Error('Token de GitHub no configurado. Usa setGitHubToken() o CONFIG.github.token');
}

/**
 * Guarda el token de GitHub de forma segura
 * Ejecuta esta función UNA VEZ para guardar el token
 */
function setGitHubToken() {
  const ui = SpreadsheetApp.getUi();
  const result = ui.prompt(
    'Configurar Token de GitHub',
    'Ingresa tu token personal de GitHub (ghp_...):\n\n' +
    '⚠️ Este token se guardará de forma segura.',
    ui.ButtonSet.OK_CANCEL
  );
  
  if (result.getSelectedButton() === ui.Button.OK) {
    const token = result.getResponseText().trim();
    
    if (!token.startsWith('ghp_') && !token.startsWith('github_pat_')) {
      ui.alert('⚠️ Token inválido. Debe empezar con "ghp_" o "github_pat_"');
      return;
    }
    
    PropertiesService.getScriptProperties().setProperty('GITHUB_TOKEN', token);
    ui.alert('✅ Token guardado exitosamente de forma segura.\n\nYa puedes ejecutar syncToGitHub().');
  }
}

/**
 * Determina la ruta del archivo según hoja y formato
 */
function getFilePath(sheetName, format) {
  // Si hay una ruta específica configurada, usarla
  if (format === 'csv' && CONFIG.paths.csv) {
    return CONFIG.paths.csv;
  }
  
  if (format === 'json' && CONFIG.paths.json) {
    return CONFIG.paths.json;
  }
  
  // Generar ruta automática
  const sanitizedName = sheetName
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_|_$/g, '');
  
  return `filtro_basico/${sanitizedName}.${format}`;
}

/**
 * Genera mensaje de commit informativo
 */
function generateCommitMessage(sheetName) {
  const date = Utilities.formatDate(
    new Date(),
    'GMT-5',
    'yyyy-MM-dd HH:mm:ss'
  );
  
  return `Actualización automática desde Google Sheets

Hoja: ${sheetName}
Fecha: ${date}
Formato: ${CONFIG.sheets.exportFormat}

[Automated sync via Apps Script]`;
}

/**
 * Sistema de logging
 */
function log(message, level = 'INFO') {
  if (!CONFIG.options.enableLogs && level !== 'ERROR') {
    return;
  }
  
  const timestamp = Utilities.formatDate(
    new Date(),
    'GMT-5',
    'yyyy-MM-dd HH:mm:ss'
  );
  
  const prefix = {
    'ERROR': '❌',
    'WARN': '⚠️',
    'INFO': 'ℹ️',
    'DEBUG': '🔍'
  }[level] || 'ℹ️';
  
  Logger.log(`[${timestamp}] ${prefix} ${message}`);
}

/**
 * Notifica errores por email
 */
function notifyError(error) {
  if (!CONFIG.options.emailTo) {
    return;
  }
  
  const subject = '❌ Error en sincronización Google Sheets → GitHub';
  const body = `
Se produjo un error al sincronizar Google Sheets con GitHub:

Error: ${error.message}
Stack: ${error.stack}

Timestamp: ${new Date().toISOString()}
Hoja: ${SpreadsheetApp.getActiveSpreadsheet().getName()}

Por favor revisa los logs en Apps Script para más detalles.
`;
  
  MailApp.sendEmail(CONFIG.options.emailTo, subject, body);
}

/**
 * Actualiza estadísticas de sincronización
 */
function updateStats(results) {
  const properties = PropertiesService.getScriptProperties();
  
  const totalSyncs = parseInt(properties.getProperty('totalSyncs') || '0') + 1;
  const successfulSyncs = results.filter(r => r.status === 'success').length;
  const lastSync = new Date().toISOString();
  
  properties.setProperties({
    'totalSyncs': totalSyncs.toString(),
    'successfulSyncs': successfulSyncs.toString(),
    'lastSync': lastSync,
    'lastResults': JSON.stringify(results)
  });
}

/**
 * Obtiene estadísticas de sincronización
 */
function getStats() {
  const properties = PropertiesService.getScriptProperties();
  
  return {
    totalSyncs: properties.getProperty('totalSyncs') || '0',
    successfulSyncs: properties.getProperty('successfulSyncs') || '0',
    lastSync: properties.getProperty('lastSync') || 'Never',
    lastResults: JSON.parse(properties.getProperty('lastResults') || '[]')
  };
}

/**
 * Muestra estadísticas en el log
 */
function showStats() {
  const stats = getStats();
  
  log('\n📊 ESTADÍSTICAS DE SINCRONIZACIÓN', 'INFO');
  log(`Total sincronizaciones: ${stats.totalSyncs}`, 'INFO');
  log(`Sincronizaciones exitosas: ${stats.successfulSyncs}`, 'INFO');
  log(`Última sincronización: ${stats.lastSync}`, 'INFO');
  log(`\nÚltimos resultados:`, 'INFO');
  
  stats.lastResults.forEach(result => {
    log(`  - ${result.sheet}: ${result.status}`, 'INFO');
  });
}

// ============================================================================
// FUNCIONES AUXILIARES PARA TESTING
// ============================================================================

/**
 * Test: Verifica la configuración
 */
function testConfig() {
  log('🧪 Verificando configuración...', 'INFO');
  
  try {
    const token = getGitHubToken();
    log('✅ Token encontrado', 'INFO');
    
    if (!CONFIG.github.owner || !CONFIG.github.repo) {
      throw new Error('owner o repo no configurados');
    }
    log('✅ Owner y repo configurados', 'INFO');
    
    if (!CONFIG.sheets.sheetNames || CONFIG.sheets.sheetNames.length === 0) {
      throw new Error('No hay hojas configuradas para exportar');
    }
    log('✅ Hojas configuradas', 'INFO');
    
    log('🎉 Configuración válida', 'INFO');
    return true;
    
  } catch (error) {
    log(`❌ Error en configuración: ${error.message}`, 'ERROR');
    return false;
  }
}

/**
 * Test: Conexión con GitHub
 */
function testGitHubConnection() {
  log('🧪 Probando conexión con GitHub...', 'INFO');
  
  try {
    const token = getGitHubToken();
    const url = `https://api.github.com/repos/${CONFIG.github.owner}/${CONFIG.github.repo}`;
    
    const response = UrlFetchApp.fetch(url, {
      method: 'get',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    });
    
    const repo = JSON.parse(response.getContentText());
    log(`✅ Conectado a: ${repo.full_name}`, 'INFO');
    log(`   Rama por defecto: ${repo.default_branch}`, 'INFO');
    log(`   Privado: ${repo.private ? 'Sí' : 'No'}`, 'INFO');
    
    return true;
    
  } catch (error) {
    log(`❌ Error de conexión: ${error.message}`, 'ERROR');
    return false;
  }
}

/**
 * Test: Lectura de hoja
 */
function testReadSheet() {
  log('🧪 Probando lectura de hoja...', 'INFO');
  
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheetName = CONFIG.sheets.sheetNames[0];
    const sheet = spreadsheet.getSheetByName(sheetName);
    
    if (!sheet) {
      throw new Error(`Hoja "${sheetName}" no encontrada`);
    }
    
    const data = readSheetData(sheet);
    log(`✅ ${data.length} filas leídas de "${sheetName}"`, 'INFO');
    log(`   Columnas: ${data[0] ? data[0].length : 0}`, 'INFO');
    
    return true;
    
  } catch (error) {
    log(`❌ Error al leer hoja: ${error.message}`, 'ERROR');
    return false;
  }
}

/**
 * Ejecuta todos los tests
 */
function runAllTests() {
  log('\n🧪 EJECUTANDO TESTS', 'INFO');
  log('='.repeat(50), 'INFO');
  
  const tests = [
    { name: 'Configuración', fn: testConfig },
    { name: 'Conexión GitHub', fn: testGitHubConnection },
    { name: 'Lectura de hoja', fn: testReadSheet }
  ];
  
  const results = tests.map(test => {
    log(`\n▶️ Test: ${test.name}`, 'INFO');
    const result = test.fn();
    return { name: test.name, passed: result };
  });
  
  log('\n' + '='.repeat(50), 'INFO');
  log('📊 RESUMEN DE TESTS', 'INFO');
  
  results.forEach(result => {
    const icon = result.passed ? '✅' : '❌';
    log(`${icon} ${result.name}: ${result.passed ? 'PASS' : 'FAIL'}`, 'INFO');
  });
  
  const allPassed = results.every(r => r.passed);
  
  if (allPassed) {
    log('\n🎉 Todos los tests pasaron. Ya puedes ejecutar syncToGitHub()', 'INFO');
  } else {
    log('\n⚠️ Algunos tests fallaron. Revisa la configuración.', 'WARN');
  }
  
  return allPassed;
}

// ============================================================================
// MENÚ PERSONALIZADO
// ============================================================================

/**
 * Crea un menú personalizado en Google Sheets
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  
  ui.createMenu('🔄 GitHub Sync')
    .addItem('📤 Sincronizar ahora', 'syncToGitHub')
    .addSeparator()
    .addItem('🔧 Configurar token', 'setGitHubToken')
    .addItem('🧪 Ejecutar tests', 'runAllTests')
    .addItem('📊 Ver estadísticas', 'showStats')
    .addSeparator()
    .addItem('📖 Ayuda', 'showHelp')
    .addToUi();
}

/**
 * Muestra ayuda
 */
function showHelp() {
  const ui = SpreadsheetApp.getUi();
  
  ui.alert(
    'Ayuda: GitHub Sync',
    '🔄 Sincronizar ahora: Exporta y sube a GitHub inmediatamente\n\n' +
    '🔧 Configurar token: Guarda tu token de GitHub de forma segura\n\n' +
    '🧪 Ejecutar tests: Verifica que todo esté configurado correctamente\n\n' +
    '📊 Ver estadísticas: Muestra histórico de sincronizaciones\n\n' +
    'Para más información, consulta AUTOMATIZACION_SHEETS_GITHUB.md',
    ui.ButtonSet.OK
  );
}


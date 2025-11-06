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
 * - ✅ Codificación UTF-8 correcta (preserva acentos, ñ, caracteres especiales)
 * 
 * Autor: AI Assistant
 * Versión: 2.1
 * Última actualización: 2025-01-XX
 * 
 * Cambios v2.1:
 * - Corregido problema de codificación UTF-8 en caracteres especiales
 * - Usa Blob.getBytes() para preservar correctamente acentos y caracteres especiales
 */

// ============================================================================
// CONFIGURACIÓN
// ============================================================================

const CONFIG = {
  // Configuración de GitHub
  github: {
    owner: 'comediacortesana',        // usuario/organización de GitHub
    repo: 'comedia_cortesana',         // nombre del repositorio
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
    exportBoth: true                   // ⭐ true = exportar CSV y JSON (necesario para el HTML)
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
  
  // Si exportBoth está activado, exportar ambos formatos
  if (CONFIG.paths.exportBoth) {
    log('📤 Exportando ambos formatos: CSV y JSON', 'INFO');
    
    const results = [];
    let hasAnyChanges = false;
    
    // 1. Exportar CSV
    const csvContent = convertToCSV(data);
    const csvPath = CONFIG.paths.csv || getFilePath(sheetName, 'csv');
    
    let csvHasChanges = true;
    if (CONFIG.options.checkForChanges) {
      csvHasChanges = checkForChanges(csvContent, csvPath);
      if (!csvHasChanges) {
        log('✅ CSV: No hay cambios. Skip push.', 'INFO');
      } else {
        log('🔄 CSV: Cambios detectados. Haciendo push...', 'INFO');
        hasAnyChanges = true;
      }
    } else {
      hasAnyChanges = true;
    }
    
    // Preparar archivos para push conjunto
    const filesToPush = [];
    
    if (csvHasChanges) {
      filesToPush.push({
        path: csvPath,
        content: csvContent,
        format: 'CSV'
      });
    }
    
    // 2. Exportar JSON (con metadata para HTML)
    const jsonContent = convertToJSON(data, true);
    const jsonPath = CONFIG.paths.json || getFilePath(sheetName, 'json');
    
    let jsonHasChanges = true;
    if (CONFIG.options.checkForChanges) {
      jsonHasChanges = checkForChanges(jsonContent, jsonPath);
      if (!jsonHasChanges) {
        log('✅ JSON: No hay cambios. Skip push.', 'INFO');
      } else {
        log('🔄 JSON: Cambios detectados.', 'INFO');
        hasAnyChanges = true;
      }
    } else {
      hasAnyChanges = true;
    }
    
    if (jsonHasChanges) {
      filesToPush.push({
        path: jsonPath,
        content: jsonContent,
        format: 'JSON'
      });
    }
    
    // Si hay archivos para subir, hacer push conjunto en un solo commit
    if (filesToPush.length > 0) {
      log(`📤 Subiendo ${filesToPush.length} archivo(s) en un solo commit...`, 'INFO');
      const pushResult = pushMultipleFilesToGitHub(filesToPush, sheetName);
      
      filesToPush.forEach(file => {
        results.push({
          format: file.format,
          path: file.path,
          commit: pushResult.commit.sha
        });
      });
    } else {
      // Ningún archivo tiene cambios
      if (!csvHasChanges) {
        results.push({ format: 'CSV', path: csvPath, status: 'no_changes' });
      }
      if (!jsonHasChanges) {
        results.push({ format: 'JSON', path: jsonPath, status: 'no_changes' });
      }
    }
    
    // Si no hay cambios en ninguno, retornar no_changes
    if (!hasAnyChanges) {
      return { 
        sheet: sheetName, 
        status: 'no_changes', 
        formats: results 
      };
    }
    
    return {
      sheet: sheetName,
      status: 'success',
      formats: results
    };
  }
  
  // Si exportBoth está desactivado, exportar solo el formato configurado
  const format = CONFIG.sheets.exportFormat;
  const content = format === 'json' 
    ? convertToJSON(data, true)  // Siempre incluir metadata para HTML
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
 * Usa getDisplayValues() para obtener los valores como strings con UTF-8 correcto
 */
function readSheetData(sheet) {
  const lastRow = sheet.getLastRow();
  const lastCol = sheet.getLastColumn();
  
  if (lastRow === 0 || lastCol === 0) {
    return [];
  }
  
  const range = sheet.getRange(1, 1, lastRow, lastCol);
  
  // Usar getDisplayValues() en lugar de getValues() para preservar UTF-8
  // getDisplayValues() devuelve strings formateados que mantienen mejor la codificación
  const values = range.getDisplayValues();
  
  // Convertir los strings display a sus tipos originales si es necesario
  // Pero mantener los strings tal cual para preservar UTF-8
  const processedValues = values.map((row, rowIndex) => {
    if (rowIndex === 0) {
      // Primera fila (encabezados): mantener como strings
      return row;
    }
    
    // Filas de datos: intentar convertir números y fechas, pero mantener strings tal cual
    return row.map((cell, colIndex) => {
      if (cell === '' || cell === null) {
        return '';
      }
      
      // Intentar convertir a número si parece numérico
      const num = parseFloat(cell);
      if (!isNaN(num) && cell.trim() === num.toString()) {
        return num;
      }
      
      // Para todo lo demás, mantener como string (preserva UTF-8)
      return String(cell);
    });
  });
  
  // Filtrar filas vacías si está configurado
  if (CONFIG.sheets.skipEmptyRows) {
    return processedValues.filter(row => !isEmptyRow(row));
  }
  
  return processedValues;
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
 * Si es para datos_obras.json, incluye metadata para el HTML
 */
function convertToJSON(data, includeMetadata) {
  // Valor por defecto si no se especifica
  if (includeMetadata === undefined) {
    includeMetadata = true;
  }
  
  if (data.length === 0) {
    return includeMetadata 
      ? JSON.stringify({ metadata: {}, obras: [] }, null, 2)
      : JSON.stringify([]);
  }
  
  // Primera fila = encabezados
  // Asegurar que los encabezados se conviertan correctamente a UTF-8
  const headers = data[0].map(h => {
    if (h === null || h === undefined) {
      return '';
    }
    // Convertir a string asegurando UTF-8
    let header = String(h);
    // Normalizar caracteres especiales si es necesario
    header = header.trim();
    return header;
  });
  
  // Resto de filas = datos
  const rows = data.slice(1);
  
  // Convertir a array de objetos
  const obras = rows.map(row => {
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
        // Mantener string tal cual - getDisplayValues() ya devuelve UTF-8 correcto
        // No hacer conversiones que puedan corromper caracteres especiales
        
        // Intentar convertir strings numéricos (solo si es puramente numérico)
        const num = parseFloat(value);
        if (!isNaN(num) && value.trim() === num.toString() && value.trim() !== '') {
          value = num;
        }
        // Si no es numérico, mantener como string (preserva UTF-8, acentos, ñ, etc.)
      } else if (value !== null && value !== undefined) {
        // Cualquier otro tipo, convertir a string
        value = String(value);
      }
      
      obj[header] = value;
    });
    
    return obj;
  });
  
  // Si includeMetadata es true, crear estructura para HTML
  if (includeMetadata) {
    const now = new Date();
    const fecha = Utilities.formatDate(now, 'GMT-5', 'yyyy-MM-dd');
    const fechaCompleta = now.toISOString();
    
    // Extraer fuentes únicas si hay columna 'fuente'
    const fuentes = [];
    obras.forEach(obra => {
      if (obra.fuente && !fuentes.includes(obra.fuente)) {
        fuentes.push(obra.fuente);
      }
    });
    
    const resultado = {
      metadata: {
        version: '1.0',
        fecha_actualizacion: fecha,
        fecha_completa: fechaCompleta,
        total_obras: obras.length,
        fuentes: fuentes.length > 0 ? fuentes : ['AMBAS', 'CATCOM', 'FUENTESXI'],
        descripcion: 'Obras del teatro español del Siglo de Oro - Base de datos DELIA'
      },
      obras: obras
    };
    
    // JSON.stringify maneja UTF-8 correctamente por defecto
    // Asegurar que el resultado sea UTF-8 válido
    const jsonString = JSON.stringify(resultado, null, 2);
    return jsonString;
  }
  
  // Si no incluye metadata, retornar array simple
  // JSON.stringify maneja UTF-8 automáticamente
  const jsonString = JSON.stringify(obras, null, 2);
  return jsonString;
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
  
  // Decodificar contenido de base64 preservando UTF-8
  const decodedBytes = Utilities.base64Decode(data.content);
  const blob = Utilities.newBlob(decodedBytes);
  return blob.getDataAsString();
}

/**
 * Sube múltiples archivos en un solo commit usando la API de Git de GitHub
 */
function pushMultipleFilesToGitHub(files, sheetName) {
  const token = getGitHubToken();
  const baseUrl = `https://api.github.com/repos/${CONFIG.github.owner}/${CONFIG.github.repo}`;
  
  try {
    // 1. Obtener referencia de la rama
    const refUrl = `${baseUrl}/git/refs/heads/${CONFIG.github.branch}`;
    const refResponse = UrlFetchApp.fetch(refUrl, {
      method: 'get',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    });
    
    if (refResponse.getResponseCode() !== 200) {
      throw new Error(`No se pudo obtener la referencia de la rama: ${refResponse.getResponseCode()}`);
    }
    
    const refData = JSON.parse(refResponse.getContentText());
    const baseCommitSha = refData.object.sha;
    
    // 2. Obtener commit base y su árbol
    const commitUrl = `${baseUrl}/git/commits/${baseCommitSha}`;
    const commitResponse = UrlFetchApp.fetch(commitUrl, {
      method: 'get',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    });
    
    const baseCommit = JSON.parse(commitResponse.getContentText());
    const baseTreeSha = baseCommit.tree.sha;
    
    // 3. Obtener árbol base
    const treeUrl = `${baseUrl}/git/trees/${baseTreeSha}?recursive=1`;
    const treeResponse = UrlFetchApp.fetch(treeUrl, {
      method: 'get',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    });
    
    const baseTree = JSON.parse(treeResponse.getContentText());
    
    // 4. Crear blobs para cada archivo y construir el árbol
    const tree = [];
    const existingPaths = {};
    
    // Primero, agregar todos los archivos existentes (excepto los que vamos a actualizar)
    baseTree.tree.forEach(item => {
      if (item.type === 'blob') {
        const fileToUpdate = files.find(f => f.path === item.path);
        if (!fileToUpdate) {
          // Mantener archivo existente
          tree.push({
            path: item.path,
            mode: item.mode,
            type: item.type,
            sha: item.sha
          });
          existingPaths[item.path] = true;
        }
      }
    });
    
    // 5. Crear blobs para los archivos nuevos/actualizados
    files.forEach(file => {
      // ⭐ SOLUCIÓN UTF-8: Convertir string a bytes UTF-8 explícitamente
      // Crear un Blob desde el string (automáticamente usa UTF-8) y obtener sus bytes
      const blob = Utilities.newBlob(file.content);
      const bytes = blob.getBytes();
      const contentBase64 = Utilities.base64Encode(bytes);
      
      // Crear blob
      const blobUrl = `${baseUrl}/git/blobs`;
      const blobResponse = UrlFetchApp.fetch(blobUrl, {
        method: 'post',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/vnd.github.v3+json',
          'Content-Type': 'application/json'
        },
        payload: JSON.stringify({
          content: contentBase64,
          encoding: 'base64'
        })
      });
      
      if (blobResponse.getResponseCode() !== 201) {
        throw new Error(`Error creando blob para ${file.path}: ${blobResponse.getContentText()}`);
      }
      
      const blobData = JSON.parse(blobResponse.getContentText());
      
      // Agregar al árbol
      tree.push({
        path: file.path,
        mode: '100644',
        type: 'blob',
        sha: blobData.sha
      });
    });
    
    // 6. Crear nuevo árbol
    const newTreeUrl = `${baseUrl}/git/trees`;
    const newTreeResponse = UrlFetchApp.fetch(newTreeUrl, {
      method: 'post',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
      },
      payload: JSON.stringify({
        base_tree: baseTreeSha,
        tree: tree
      })
    });
    
    if (newTreeResponse.getResponseCode() !== 201) {
      throw new Error(`Error creando árbol: ${newTreeResponse.getContentText()}`);
    }
    
    const newTreeData = JSON.parse(newTreeResponse.getContentText());
    
    // 7. Crear commit
    const date = Utilities.formatDate(
      new Date(),
      'GMT-5',
      'yyyy-MM-dd HH:mm:ss'
    );
    
    const fileNames = files.map(f => f.format).join(' y ');
    const commitMessage = `Actualización automática desde Google Sheets

Hoja: ${sheetName}
Fecha: ${date}
Archivos: ${fileNames}

[Automated sync via Apps Script]`;
    
    const createCommitUrl = `${baseUrl}/git/commits`;
    const createCommitResponse = UrlFetchApp.fetch(createCommitUrl, {
      method: 'post',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
      },
      payload: JSON.stringify({
        message: commitMessage,
        tree: newTreeData.sha,
        parents: [baseCommitSha]
      })
    });
    
    if (createCommitResponse.getResponseCode() !== 201) {
      throw new Error(`Error creando commit: ${createCommitResponse.getContentText()}`);
    }
    
    const commitData = JSON.parse(createCommitResponse.getContentText());
    
    // 8. Actualizar referencia de la rama
    const updateRefUrl = `${baseUrl}/git/refs/heads/${CONFIG.github.branch}`;
    const updateRefResponse = UrlFetchApp.fetch(updateRefUrl, {
      method: 'patch',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
      },
      payload: JSON.stringify({
        sha: commitData.sha
      })
    });
    
    if (updateRefResponse.getResponseCode() !== 200) {
      throw new Error(`Error actualizando referencia: ${updateRefResponse.getContentText()}`);
    }
    
    log(`✅ Push exitoso (${files.length} archivo(s)) en un solo commit: ${commitData.sha}`, 'INFO');
    
    return {
      commit: {
        sha: commitData.sha
      }
    };
    
  } catch (error) {
    log(`❌ Error en push múltiple: ${error.message}`, 'ERROR');
    throw error;
  }
}

/**
 * Sube contenido a GitHub usando la API
 */
function pushToGitHub(content, filePath, sheetName) {
  const token = getGitHubToken();
  const url = `https://api.github.com/repos/${CONFIG.github.owner}/${CONFIG.github.repo}/contents/${filePath}`;
  
  // ⭐ SOLUCIÓN UTF-8: Convertir string a bytes UTF-8 explícitamente
  // Crear un Blob desde el string (automáticamente usa UTF-8) y obtener sus bytes
  const blob = Utilities.newBlob(content);
  const bytes = blob.getBytes();
  const contentBase64 = Utilities.base64Encode(bytes);
  
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
 * 
 * MÉTODO 1: Con diálogo (puede quedarse colgado si se ejecuta desde el editor)
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
 * MÉTODO 2: Función alternativa que acepta el token directamente
 * ⭐ USAR ESTA SI setGitHubToken() se queda colgado
 * 
 * INSTRUCCIONES:
 * 1. Reemplaza 'TU_TOKEN_AQUI' con tu token real
 * 2. Ejecuta la función
 * 3. Verifica en los logs que diga "✅ Token guardado"
 * 4. ¡Listo! Ya puedes borrar el token del código
 */
function setupToken() {
  const token = 'TU_TOKEN_AQUI';  // ⚠️ PEGA TU TOKEN AQUÍ (ej: ghp_xxxxxxxxxxxx)
  
  if (!token || token === 'TU_TOKEN_AQUI') {
    Logger.log('❌ Error: Debes reemplazar TU_TOKEN_AQUI con tu token real');
    return;
  }
  
  if (!token.startsWith('ghp_') && !token.startsWith('github_pat_')) {
    Logger.log('❌ Error: Token inválido. Debe empezar con "ghp_" o "github_pat_"');
    return;
  }
  
  PropertiesService.getScriptProperties().setProperty('GITHUB_TOKEN', token);
  Logger.log('✅ Token guardado exitosamente de forma segura');
  Logger.log('✅ Ya puedes ejecutar syncToGitHub()');
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
    
    // Verificar codificación UTF-8 en una muestra
    if (data.length > 1) {
      const sampleRow = data[1];
      const sampleText = JSON.stringify(sampleRow).substring(0, 200);
      log(`   Muestra de datos: ${sampleText}...`, 'DEBUG');
    }
    
    return true;
    
  } catch (error) {
    log(`❌ Error al leer hoja: ${error.message}`, 'ERROR');
    return false;
  }
}

/**
 * Test: Verificar codificación UTF-8
 * Prueba que los caracteres especiales se preserven correctamente
 */
function testUTF8Encoding() {
  log('🧪 Probando codificación UTF-8...', 'INFO');
  
  try {
    // Texto de prueba con caracteres especiales
    const testText = 'María el corazón';
    log(`   Texto original: ${testText}`, 'INFO');
    
    // Simular el proceso de codificación
    const blob = Utilities.newBlob(testText);
    const bytes = blob.getBytes();
    const base64 = Utilities.base64Encode(bytes);
    
    // Decodificar de vuelta
    const decodedBytes = Utilities.base64Decode(base64);
    const decodedBlob = Utilities.newBlob(decodedBytes);
    const decodedText = decodedBlob.getDataAsString();
    
    log(`   Texto decodificado: ${decodedText}`, 'INFO');
    
    if (testText === decodedText) {
      log('✅ Codificación UTF-8 funciona correctamente', 'INFO');
      return true;
    } else {
      log('❌ Error: Los caracteres no se preservaron', 'ERROR');
      return false;
    }
    
  } catch (error) {
    log(`❌ Error en test UTF-8: ${error.message}`, 'ERROR');
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
    { name: 'Lectura de hoja', fn: testReadSheet },
    { name: 'Codificación UTF-8', fn: testUTF8Encoding }
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


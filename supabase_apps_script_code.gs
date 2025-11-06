// ============================================================================
// CÓDIGO PARA AÑADIR A sheets-github-sync.gs
// ============================================================================
// 
// INSTRUCCIONES:
// 1. Copia este código al final de sheets-github-sync.gs
// 2. Configura setSupabaseServiceKey() con tu service_role key
// 3. Opcionalmente modifica syncToGitHub() para llamar también a syncToSupabase()
//
// Ver guía completa: GUIA_SUPABASE_PASO_A_PASO.md
// ============================================================================

// ============================================================================
// SINCRONIZACIÓN CON SUPABASE
// ============================================================================

/**
 * Sincroniza Google Sheets con Supabase
 * Ejecutar después de syncToGitHub() o en paralelo
 */
function syncToSupabase() {
  try {
    log('🚀 Iniciando sincronización con Supabase...', 'INFO');
    
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName('obras_completas');
    
    if (!sheet) {
      throw new Error('Hoja "obras_completas" no encontrada');
    }
    
    // Leer datos de la hoja
    const data = readSheetData(sheet);
    
    if (data.length === 0) {
      log('⚠️ La hoja está vacía', 'WARN');
      return;
    }
    
    // Convertir a objetos
    const headers = data[0];
    const obras = data.slice(1).map(row => {
      const obj = {};
      headers.forEach((header, index) => {
        obj[header] = row[index] || null;
      });
      return obj;
    });
    
    log(`📊 ${obras.length} obras procesadas`, 'INFO');
    
    // Configuración de Supabase
    // ⚠️ REEMPLAZA CON TU URL DE SUPABASE
    const SUPABASE_URL = 'https://TU-PROYECTO.supabase.co';
    const serviceKey = getSupabaseServiceKey();
    
    // Sincronizar cada obra
    let successCount = 0;
    let errorCount = 0;
    
    for (const obra of obras) {
      try {
        syncObraToSupabase(obra, SUPABASE_URL, serviceKey);
        successCount++;
        
        // Pequeña pausa para no sobrecargar la API
        if (successCount % 10 === 0) {
          Utilities.sleep(100);
        }
      } catch (error) {
        log(`❌ Error sincronizando obra ${obra.ID}: ${error.message}`, 'ERROR');
        errorCount++;
      }
    }
    
    log(`✅ Sincronización completada: ${successCount} exitosas, ${errorCount} errores`, 'INFO');
    
  } catch (error) {
    log(`❌ Error general: ${error.message}`, 'ERROR');
    throw error;
  }
}

/**
 * Sincroniza una obra individual con Supabase
 */
function syncObraToSupabase(obra, supabaseUrl, serviceKey) {
  const obraId = obra.ID || obra.id;
  if (!obraId) {
    throw new Error('Obra sin ID');
  }
  
  const url = `${supabaseUrl}/rest/v1/obras?id=eq.${obraId}`;
  
  // Verificar si existe
  const checkResponse = UrlFetchApp.fetch(url, {
    method: 'GET',
    headers: {
      'apikey': serviceKey,
      'Authorization': `Bearer ${serviceKey}`,
      'Content-Type': 'application/json'
    },
    muteHttpExceptions: true
  });
  
  const statusCode = checkResponse.getResponseCode();
  if (statusCode !== 200) {
    throw new Error(`Error verificando obra: ${statusCode} - ${checkResponse.getContentText()}`);
  }
  
  const existing = JSON.parse(checkResponse.getContentText());
  
  // Mapear campos del Sheet a la tabla de Supabase
  // Ajusta estos campos según los nombres de tus columnas en Google Sheets
  const obraData = {
    id: obraId,
    titulo: obra['Título'] || obra['T?tulo'] || null,
    titulo_original: obra['Título Original'] || obra['T?tulo Original'] || null,
    tipo_obra: obra['Tipo de Obra'] || null,
    autor_nombre: obra['Autor'] || null,
    fuente: obra['Fuente Principal'] || obra['Fuente'] || null,
    fecha_creacion: obra['Fecha de Creación'] || null,
    synced_from_sheet_at: new Date().toISOString()
  };
  
  if (existing && existing.length > 0) {
    // Actualizar existente
    const updateUrl = `${supabaseUrl}/rest/v1/obras?id=eq.${obraId}`;
    const updateResponse = UrlFetchApp.fetch(updateUrl, {
      method: 'PATCH',
      headers: {
        'apikey': serviceKey,
        'Authorization': `Bearer ${serviceKey}`,
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
      },
      payload: JSON.stringify(obraData),
      muteHttpExceptions: true
    });
    
    const updateStatusCode = updateResponse.getResponseCode();
    if (updateStatusCode !== 204 && updateStatusCode !== 200) {
      throw new Error(`Error actualizando: ${updateStatusCode} - ${updateResponse.getContentText()}`);
    }
  } else {
    // Insertar nuevo
    const insertUrl = `${supabaseUrl}/rest/v1/obras`;
    const insertResponse = UrlFetchApp.fetch(insertUrl, {
      method: 'POST',
      headers: {
        'apikey': serviceKey,
        'Authorization': `Bearer ${serviceKey}`,
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
      },
      payload: JSON.stringify(obraData),
      muteHttpExceptions: true
    });
    
    const insertStatusCode = insertResponse.getResponseCode();
    if (insertStatusCode !== 201 && insertStatusCode !== 200) {
      throw new Error(`Error insertando: ${insertStatusCode} - ${insertResponse.getContentText()}`);
    }
  }
}

/**
 * Obtiene la service key de Supabase de forma segura
 */
function getSupabaseServiceKey() {
  const properties = PropertiesService.getScriptProperties();
  const key = properties.getProperty('SUPABASE_SERVICE_KEY');
  
  if (!key) {
    throw new Error('SUPABASE_SERVICE_KEY no configurado. Usa setSupabaseServiceKey()');
  }
  
  return key;
}

/**
 * Guarda la service key de Supabase
 * ⚠️ EJECUTA ESTA FUNCIÓN UNA VEZ para guardar tu service_role key
 */
function setSupabaseServiceKey() {
  const ui = SpreadsheetApp.getUi();
  const result = ui.prompt(
    'Configurar Supabase Service Key',
    'Ingresa tu Service Role Key de Supabase:\n\n' +
    '⚠️ Esta key tiene permisos completos. Manténla segura.\n\n' +
    'Encuéntrala en: Supabase → Settings → API → service_role key',
    ui.ButtonSet.OK_CANCEL
  );
  
  if (result.getSelectedButton() === ui.Button.OK) {
    const key = result.getResponseText().trim();
    PropertiesService.getScriptProperties().setProperty('SUPABASE_SERVICE_KEY', key);
    ui.alert('✅ Service Key guardada exitosamente');
  }
}

/**
 * Función combinada: Sincroniza a GitHub Y Supabase
 * Úsala si quieres sincronizar ambos en una sola ejecución
 */
function syncToGitHubAndSupabase() {
  log('🔄 Sincronizando a GitHub y Supabase...', 'INFO');
  
  // Primero GitHub (como antes)
  const githubResults = syncToGitHub();
  
  // Luego Supabase
  try {
    syncToSupabase();
  } catch (error) {
    log(`⚠️ Error en Supabase (GitHub OK): ${error.message}`, 'WARN');
  }
  
  return githubResults;
}

// ============================================================================
// OPCIONAL: Modificar syncToGitHub() para incluir Supabase automáticamente
// ============================================================================
// 
// Si quieres que cada vez que se ejecute syncToGitHub() también se sincronice
// con Supabase, añade esto al final de syncToGitHub(), antes de return results:
//
//   // Sincronizar con Supabase si está habilitado
//   try {
//     syncToSupabase();
//   } catch (error) {
//     log(`⚠️ Error en Supabase: ${error.message}`, 'WARN');
//   }
//
// ============================================================================


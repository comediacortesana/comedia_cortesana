# 🔄 Automatización: Google Sheets → GitHub

## 🎯 Objetivo

Sincronizar automáticamente tus hojas de Google Sheets con GitHub sin servidores externos ni costos. Todo 100% gratuito usando:

- ✅ **Google Apps Script** (gratis)
- ✅ **GitHub API REST** (gratis)
- ✅ **Triggers automáticos** (gratis)

---

## 🚀 Características del Script

### ✨ Funcionalidades Implementadas

1. **Detección inteligente de cambios** → Solo hace push si hay cambios reales
2. **Soporte para múltiples hojas** → Exporta todas las pestañas o solo algunas
3. **Formato CSV o JSON** → Elige el formato según necesites
4. **Manejo de errores robusto** → Logs detallados y notificaciones
5. **Rate limiting** → Respeta los límites de GitHub API
6. **Validación de datos** → Verifica antes de hacer push
7. **Historial de cambios** → Mensajes de commit informativos
8. **Ejecución por triggers** → Automático por tiempo o manualmente

---

## 📋 Prerrequisitos

### 1. Repositorio GitHub
- Repositorio existente (ej: `DELIA_DJANGO`)
- Permisos de escritura

### 2. Token Personal de GitHub
1. Ve a: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Nombre: `Google Sheets Sync`
4. Scopes necesarios:
   - ✅ `repo` (acceso completo al repositorio)
   - ✅ `workflow` (opcional, solo si actualizas workflows)
5. Expiration: 1 año o "No expiration" (más seguro: 90 días)
6. Click **"Generate token"**
7. ⚠️ **COPIA EL TOKEN AHORA** (no lo podrás ver después)

### 3. Google Sheet con datos
- Tu hoja con datos de obras
- Permisos de editor en el Sheet

---

## 🔧 Instalación y Configuración

### Paso 1: Abrir Editor de Apps Script

1. Abre tu Google Sheet
2. **Extensiones** → **Apps Script**
3. Se abre el editor en nueva pestaña

### Paso 2: Copiar el Script Principal

Borra el código existente y pega el contenido de `sheets-github-sync.gs` (ver más abajo)

### Paso 3: Configurar Variables

Edita las líneas de configuración en el script:

```javascript
const CONFIG = {
  github: {
    owner: 'TU_USUARIO',           // ej: 'ivansimo'
    repo: 'DELIA_DJANGO',           // nombre del repositorio
    token: 'ghp_XXXXXXXXXXXXXXX',  // tu token personal
    branch: 'main'                  // rama donde hacer push
  },
  
  sheets: {
    exportFormat: 'csv',            // 'csv' o 'json'
    sheetNames: ['Obras Completas'], // hojas a exportar
    exportAll: false                // true = exportar todas las hojas
  },
  
  paths: {
    csv: 'filtro_basico/obras_completas.csv',
    json: 'filtro_basico/datos_obras.json'
  },
  
  options: {
    checkForChanges: true,          // solo push si hay cambios
    enableLogs: true,               // guardar logs de ejecución
    notifyOnError: true            // enviar email si hay error
  }
};
```

### Paso 4: Guardar el Script

- Click **💾 Guardar proyecto**
- Nombre sugerido: `Sync Sheets to GitHub`

### Paso 5: Primera Ejecución Manual

1. Selecciona función: `syncToGitHub` en el menú desplegable
2. Click **▶️ Ejecutar**
3. **Primera vez**: Aparecerá diálogo de permisos
   - Click **"Revisar permisos"**
   - Selecciona tu cuenta de Google
   - Click **"Permitir"** (es seguro, es tu propio script)
4. Verifica en **Logs** (Ctrl+Enter) que todo funcionó

### Paso 6: Verificar en GitHub

1. Ve a tu repositorio en GitHub
2. Navega a la ruta configurada (ej: `filtro_basico/obras_completas.csv`)
3. Debería aparecer el archivo actualizado
4. Verifica el mensaje de commit: "Actualización automática desde Google Sheets"

---

## ⚙️ Configurar Triggers Automáticos

### Opción 1: Trigger por Tiempo (Recomendado)

**Ideal para**: Sincronizar cada hora/día automáticamente

1. En el editor de Apps Script: **⏰ (Activadores/Triggers)** (menú lateral izquierdo)
2. Click **+ Agregar activador**
3. Configuración:
   - **Función**: `syncToGitHub`
   - **Evento**: `Según tiempo`
   - **Tipo**: `Activador de temporizador`
   - **Intervalo**: `Cada hora` (o el que prefieras)
4. Click **Guardar**

**Opciones de intervalo:**
- Cada 1 minuto (si necesitas máxima actualización)
- Cada hora (recomendado para edición colaborativa)
- Cada día a medianoche (para backups diarios)

### Opción 2: Trigger al Editar (Avanzado)

**Ideal para**: Push inmediato tras cada edición

1. **+ Agregar activador**
2. Configuración:
   - **Función**: `syncToGitHub`
   - **Evento**: `Al editar`
   - **Tipo**: `De una hoja de cálculo`
3. Click **Guardar**

⚠️ **Nota**: Este trigger se ejecuta en CADA edición. Para evitar múltiples pushes:
- Activa `checkForChanges: true` en CONFIG
- O usa un debounce (ver script avanzado)

### Opción 3: Botón Manual en el Sheet

**Ideal para**: Control manual del investigador

1. En tu Google Sheet: **Insertar** → **Dibujo**
2. Crea un botón bonito con texto: "🔄 Sincronizar con GitHub"
3. Guarda y asigna función: `syncToGitHub`
4. Click en el botón ejecuta el sync

---

## 📊 Formatos de Exportación

### Formato CSV (Recomendado para datos tabulares)

**Ventajas:**
- ✅ Formato estándar
- ✅ Fácil de importar a Django
- ✅ Compatible con Excel/LibreOffice
- ✅ Tamaño pequeño

**Ejemplo de salida:**
```csv
ID,Título,Autor,Tipo de Obra,Género
3058,A Dios por razon de estado,Anónimo,comedia,Religiosa
3059,A gran daño gran remedio,Lope de Vega,comedia,Histórica
```

### Formato JSON (Recomendado para APIs)

**Ventajas:**
- ✅ Estructura jerárquica
- ✅ Tipado de datos
- ✅ Ideal para frontend (filtro_basico/index.html)
- ✅ Fácil de parsear en JavaScript

**Ejemplo de salida:**
```json
[
  {
    "ID": 3058,
    "Título": "A Dios por razon de estado",
    "Autor": "Anónimo",
    "Tipo de Obra": "comedia",
    "Género": "Religiosa"
  }
]
```

### Exportar Múltiples Formatos

Modifica CONFIG para exportar ambos:

```javascript
paths: {
  exportBoth: true,
  csv: 'filtro_basico/obras_completas.csv',
  json: 'filtro_basico/datos_obras.json'
}
```

---

## 🔍 Detección de Cambios

### ¿Por qué es importante?

Evita commits innecesarios en GitHub cuando no hay cambios reales. Esto:
- Mantiene el historial limpio
- Respeta rate limits de GitHub
- Ahorra recursos

### ¿Cómo funciona?

El script:
1. Lee el archivo actual en GitHub
2. Genera el contenido nuevo desde Sheets
3. Compara checksums (SHA-256)
4. Solo hace push si son diferentes

### Código clave:

```javascript
// Calcular hash del contenido
const newHash = Utilities.computeDigest(
  Utilities.DigestAlgorithm.SHA_256,
  content,
  Utilities.Charset.UTF_8
);

// Comparar con hash anterior
if (newHash === previousHash) {
  Logger.log('✅ No hay cambios. Skip push.');
  return;
}
```

### Configuración:

```javascript
options: {
  checkForChanges: true,  // true = solo push si hay cambios
}
```

---

## 🛡️ Manejo de Errores

### Errores Comunes y Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `401 Unauthorized` | Token inválido | Generar nuevo token en GitHub |
| `404 Not Found` | Ruta incorrecta | Verificar owner/repo/path |
| `403 Forbidden` | Token sin permisos | Asegurar scope `repo` |
| `409 Conflict` | SHA incorrecto | El script lo maneja automáticamente |
| `Rate limit exceeded` | Muchas llamadas | Reducir frecuencia del trigger |

### Notificaciones por Email

El script puede enviarte un email si hay un error:

```javascript
options: {
  notifyOnError: true,
  emailTo: 'tu-email@example.com'
}
```

### Logs Detallados

Ver logs de ejecución:
1. En Apps Script: **Ver** → **Registros de ejecución**
2. O: **Ctrl+Enter** para ver logs en vivo

Ejemplo de logs:
```
[2025-10-31 10:30:15] 🚀 Iniciando sincronización...
[2025-10-31 10:30:16] 📊 Leyendo hoja: Obras Completas
[2025-10-31 10:30:17] ✅ 2,100 filas exportadas
[2025-10-31 10:30:18] 🔍 Verificando cambios...
[2025-10-31 10:30:19] ✅ Cambios detectados. Haciendo push...
[2025-10-31 10:30:21] 🎉 Push exitoso a GitHub!
[2025-10-31 10:30:21] 📝 Commit: abc123def456
```

---

## 🔐 Seguridad y Mejores Prácticas

### 1. Proteger el Token

⚠️ **NUNCA subas el script con el token a GitHub**

**Opción A: Usar Propiedades de Script** (Recomendado)

```javascript
// En vez de poner el token en CONFIG:
token: PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN')

// Guardar token de forma segura (ejecutar una sola vez):
function setGitHubToken() {
  PropertiesService.getScriptProperties()
    .setProperty('GITHUB_TOKEN', 'ghp_XXXXXXX');
  Logger.log('✅ Token guardado de forma segura');
}
```

**Opción B: Variables de Entorno de Apps Script**

1. En Apps Script: **⚙️ Configuración del proyecto**
2. **Propiedades de secuencia de comandos**
3. Añadir propiedad:
   - Nombre: `GITHUB_TOKEN`
   - Valor: `ghp_XXXXXXX`

### 2. Permisos Mínimos

Solo dar los permisos necesarios:
- ✅ Solo scope `repo` (no `admin`, no `delete`)
- ✅ Solo a este repositorio (si GitHub te lo permite)

### 3. Renovar Tokens Regularmente

- Configura tokens con expiración (90 días)
- Renueva antes de que expire
- Usa calendar reminders

### 4. Auditar Accesos

- Revisa: https://github.com/settings/applications
- Verifica que solo tu script tiene el token
- Revoca tokens antiguos

---

## 📈 Funcionalidades Avanzadas

### 1. Exportar Múltiples Hojas

Modifica `sheetNames` en CONFIG:

```javascript
sheets: {
  sheetNames: [
    'Obras Completas',
    'Autores',
    'Lugares',
    'Representaciones'
  ],
  exportAll: false
}
```

O exporta TODAS las hojas:

```javascript
sheets: {
  exportAll: true  // exporta todas las pestañas
}
```

### 2. Múltiples Archivos en GitHub

Exporta cada hoja a su propio archivo:

```javascript
function syncMultipleSheetsToGitHub() {
  const sheets = {
    'Obras Completas': 'filtro_basico/obras_completas.csv',
    'Autores': 'filtro_basico/autores.csv',
    'Lugares': 'filtro_basico/lugares.csv'
  };
  
  for (const [sheetName, path] of Object.entries(sheets)) {
    syncSheetToGitHub(sheetName, path);
  }
}
```

### 3. Validación de Datos Antes del Push

Valida que los datos sean correctos antes de hacer push:

```javascript
function validateData(data) {
  // Verificar que hay datos
  if (data.length < 2) {
    throw new Error('No hay suficientes datos para exportar');
  }
  
  // Verificar que la columna ID existe
  if (!data[0].includes('ID')) {
    throw new Error('Falta columna ID');
  }
  
  // Verificar que no hay filas vacías críticas
  const emptyRows = data.filter(row => 
    row.every(cell => cell === '')
  );
  
  if (emptyRows.length > data.length * 0.5) {
    throw new Error('Demasiadas filas vacías');
  }
  
  return true;
}
```

### 4. Notificaciones a Slack/Discord

Envía notificaciones a tu canal cuando hay un push:

```javascript
function notifySlack(message) {
  const webhookUrl = 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL';
  
  UrlFetchApp.fetch(webhookUrl, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({
      text: `🔄 ${message}`
    })
  });
}

// Usar en syncToGitHub():
notifySlack('Obras actualizadas en GitHub desde Google Sheets');
```

### 5. Backup Antes del Push

Guarda una copia de seguridad en Google Drive:

```javascript
function backupToGoogleDrive(content, filename) {
  const folder = DriveApp.getFoldersByName('Backups Sheets').next();
  const timestamp = Utilities.formatDate(
    new Date(), 
    'GMT-5', 
    'yyyy-MM-dd_HH-mm-ss'
  );
  
  folder.createFile(
    `${filename}_${timestamp}.csv`,
    content,
    'text/csv'
  );
}
```

### 6. Estadísticas de Sincronización

Mantén un registro de sincronizaciones:

```javascript
function logSyncStats() {
  const stats = PropertiesService.getScriptProperties();
  
  const totalSyncs = parseInt(stats.getProperty('totalSyncs') || '0') + 1;
  const lastSync = new Date().toISOString();
  
  stats.setProperties({
    'totalSyncs': totalSyncs.toString(),
    'lastSync': lastSync,
    'lastCommit': commitSha
  });
}

function getSyncStats() {
  const stats = PropertiesService.getScriptProperties();
  
  Logger.log(`Total sincronizaciones: ${stats.getProperty('totalSyncs')}`);
  Logger.log(`Última sincronización: ${stats.getProperty('lastSync')}`);
  Logger.log(`Último commit: ${stats.getProperty('lastCommit')}`);
}
```

---

## 🧪 Testing y Debugging

### Test Manual

1. Modifica una celda en tu Google Sheet
2. Ejecuta `syncToGitHub` manualmente
3. Verifica en GitHub que el cambio apareció
4. Verifica el mensaje de commit

### Test de Detección de Cambios

1. Ejecuta `syncToGitHub` (hace push)
2. Ejecuta `syncToGitHub` otra vez SIN modificar nada
3. En logs debe decir: "No hay cambios. Skip push."

### Test de Múltiples Hojas

1. Configura `exportAll: true`
2. Ejecuta `syncToGitHub`
3. Verifica que se exportaron todas las pestañas

### Debug Mode

Activa modo debug para ver más información:

```javascript
const DEBUG = true;

function log(message, level = 'INFO') {
  if (DEBUG || level === 'ERROR') {
    Logger.log(`[${level}] ${message}`);
  }
}
```

---

## 📊 Casos de Uso

### Caso 1: Investigadores Editando Colaborativamente

**Setup:**
- Trigger: Cada hora
- Formato: CSV
- Check changes: true
- Notificaciones: email si hay error

**Flujo:**
1. Investigadores editan Google Sheet durante el día
2. Cada hora, el script sincroniza a GitHub automáticamente
3. El sitio web (GitHub Pages) se actualiza con los nuevos datos
4. Los usuarios ven los cambios en la web

### Caso 2: Backup Diario Automático

**Setup:**
- Trigger: Cada día a medianoche
- Formato: JSON
- Backup a Google Drive: true

**Flujo:**
1. A medianoche, el script exporta todo
2. Guarda backup en Google Drive
3. Hace push a GitHub
4. Envía email con resumen

### Caso 3: Sincronización en Tiempo Real

**Setup:**
- Trigger: Al editar
- Formato: CSV y JSON
- Check changes: true
- Debounce: 5 minutos

**Flujo:**
1. Usuario edita una celda
2. Script espera 5 minutos (debounce)
3. Si no hay más ediciones, hace push
4. GitHub Pages se actualiza casi en tiempo real

---

## 🔄 Workflow Completo

```
┌─────────────────────┐
│  Google Sheets      │
│  (Investigadores)   │
└──────────┬──────────┘
           │ Edición
           ↓
┌─────────────────────┐
│  Apps Script        │
│  (Trigger cada hora)│
└──────────┬──────────┘
           │ Sync
           ↓
┌─────────────────────┐
│  GitHub API         │
│  (Push a repo)      │
└──────────┬──────────┘
           │ Commit
           ↓
┌─────────────────────┐
│  GitHub Actions     │
│  (Deploy Pages)     │
└──────────┬──────────┘
           │ Build
           ↓
┌─────────────────────┐
│  GitHub Pages       │
│  (Usuario final)    │
└─────────────────────┘
```

---

## 🎯 Checklist de Configuración

### Antes de Empezar:
- [ ] Tienes un repositorio GitHub
- [ ] Tienes permisos de escritura en el repo
- [ ] Tienes un Google Sheet con datos
- [ ] Tienes permisos de editor en el Sheet

### Configuración:
- [ ] Token de GitHub generado (scope: repo)
- [ ] Script copiado en Apps Script
- [ ] CONFIG actualizado con tus datos
- [ ] Primera ejecución manual exitosa
- [ ] Permisos de Apps Script aceptados
- [ ] Archivo visible en GitHub

### Automatización:
- [ ] Trigger configurado (tiempo o edición)
- [ ] Test de trigger realizado
- [ ] Logs verificados
- [ ] Detección de cambios funcionando

### Seguridad:
- [ ] Token guardado en Propiedades (no en código)
- [ ] Token NO subido a GitHub
- [ ] Permisos mínimos configurados
- [ ] Fecha de expiración de token registrada

---

## 💡 Tips y Trucos

### 1. Mensaje de Commit Personalizado

Incluye información útil en el commit:

```javascript
const commitMessage = `
Actualización automática desde Google Sheets

- Fecha: ${new Date().toISOString()}
- Hojas exportadas: ${sheetNames.join(', ')}
- Total de filas: ${rowCount}
- Cambios detectados: ${hasChanges ? 'Sí' : 'No'}
`.trim();
```

### 2. Filtrar Filas Antes de Exportar

Exporta solo filas completas o validadas:

```javascript
function filterValidRows(data) {
  return data.filter(row => {
    // Ignorar filas vacías
    if (row.every(cell => cell === '')) return false;
    
    // Ignorar filas sin ID
    if (!row[0]) return false;
    
    // Ignorar filas marcadas como "borrador"
    if (row.includes('BORRADOR')) return false;
    
    return true;
  });
}
```

### 3. Formatear Datos Antes de Exportar

Limpia y normaliza datos:

```javascript
function cleanData(data) {
  return data.map(row => 
    row.map(cell => {
      // Trim espacios
      if (typeof cell === 'string') {
        return cell.trim();
      }
      
      // Convertir fechas a formato ISO
      if (cell instanceof Date) {
        return cell.toISOString().split('T')[0];
      }
      
      return cell;
    })
  );
}
```

### 4. Comprimir JSON

Para archivos JSON grandes, elimina espacios:

```javascript
const jsonContent = JSON.stringify(data);  // Sin espacios
// vs
const jsonContent = JSON.stringify(data, null, 2);  // Con indentación
```

---

## 🆘 Soporte y Recursos

### Documentación Oficial:
- **Google Apps Script**: https://developers.google.com/apps-script
- **GitHub API**: https://docs.github.com/en/rest
- **GitHub Tokens**: https://docs.github.com/en/authentication

### Comunidad:
- **Stack Overflow**: Busca "Google Apps Script GitHub API"
- **GitHub Discussions**: Pregunta en tu repo

### Archivos del Proyecto:
- `sheets-github-sync.gs` - Script principal
- `sheets-github-sync-advanced.gs` - Versión con todas las funcionalidades
- `AUTOMATIZACION_SHEETS_GITHUB.md` - Esta guía

---

## 🎉 Resultado Final

Después de configurar todo:

1. ✅ Investigadores editan en Google Sheets
2. ✅ Cambios se sincronizan automáticamente a GitHub
3. ✅ GitHub Pages muestra datos actualizados
4. ✅ Todo sin intervención manual
5. ✅ Historial completo de cambios en Git
6. ✅ Backups automáticos
7. ✅ 100% gratuito

---

## 📞 ¿Necesitas Ayuda?

Si tienes problemas:
1. Revisa los **Logs** en Apps Script
2. Verifica la sección **Errores Comunes** arriba
3. Ejecuta el script en modo **DEBUG**
4. Revisa los permisos del token en GitHub

---

## 🔮 Próximos Pasos

### Ideas para Mejorar:

1. **Sincronización bidireccional**
   - GitHub → Google Sheets
   - Merge conflicts automáticos

2. **Webhooks de GitHub**
   - Recibir notificaciones en Sheets cuando alguien pushea

3. **Dashboard de Estadísticas**
   - Hoja con gráficos de actividad

4. **Revisión de cambios**
   - Comparar versiones antes de aceptar cambios

5. **Integración con Django**
   - Trigger automático de `import_from_csv.py` tras el push

---

**¡Listo para empezar! 🚀**

Copia el script de `sheets-github-sync.gs` y empieza a sincronizar tus datos.


# 📖 Guía Paso a Paso: Configurar Apps Script en Google Sheets

## 🎯 Objetivo

Configurar el script `sheets-github-sync.gs` en tu Google Sheet para sincronizar automáticamente con GitHub.

**Tiempo estimado:** 15-20 minutos  
**Dificultad:** Principiante (paso a paso)

---

## 📋 Requisitos Previos

Antes de empezar, asegúrate de tener:

- ✅ Una cuenta de Google (Gmail)
- ✅ Un Google Sheet con tus datos
- ✅ Una cuenta de GitHub
- ✅ Permisos de editor en el Google Sheet

---

## 🚀 PARTE 1: Abrir el Editor de Apps Script

### Paso 1.1: Abrir tu Google Sheet

1. **Ve a:** https://sheets.google.com
2. **Abre** tu hoja de cálculo existente
   - O crea una nueva: Click en **"+ En blanco"**
3. **Nombra tu hoja** (esquina superior izquierda)
   - Ejemplo: `DELIA - Teatro Español`

```
┌─────────────────────────────────────────────────┐
│ 🔗 DELIA - Teatro Español        👤 Mi Cuenta  │
├─────────────────────────────────────────────────┤
│ Archivo  Editar  Ver  Insertar  Formato  ...   │
├─────────────────────────────────────────────────┤
│    A         B          C          D            │
├─────────────────────────────────────────────────┤
│ 1  ID      Título     Autor      Tipo           │
│ 2  3058    A Dios...  Anónimo    comedia        │
│ 3  3059    A gran...  Lope       comedia        │
└─────────────────────────────────────────────────┘
```

### Paso 1.2: Acceder al Menú de Extensiones

1. En la barra de menú superior, busca: **Extensiones**
2. Haz click en **Extensiones**

```
┌─────────────────────────────────────────────────┐
│ Archivo  Editar  Ver  Insertar  Formato  Datos │
│ Herramientas  EXTENSIONES  Ayuda               │ ← AQUÍ
└─────────────────────────────────────────────────┘
```

### Paso 1.3: Abrir Apps Script

1. Click en **Extensiones**
2. En el menú desplegable, click en **Apps Script**

```
Extensiones
  ├─ Complementos
  │   └─ Obtener complementos
  │
  └─ Apps Script  ← CLICK AQUÍ
```

### Paso 1.4: Nueva Pestaña del Editor

Se abrirá **una nueva pestaña** en tu navegador con el editor de Apps Script.

```
┌─────────────────────────────────────────────────────────┐
│ 🔗 script.google.com/...                                │
├─────────────────────────────────────────────────────────┤
│  ≡  Apps Script          [Sin título] ▼    👤          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Archivos                    Editor                     │
│  📄 Código.gs          1  function myFunction() {       │
│                        2                                │
│                        3  }                             │
│                        4                                │
└─────────────────────────────────────────────────────────┘
```

**¡Ya estás en el editor de Apps Script! 🎉**

---

## 📝 PARTE 2: Copiar el Script

### Paso 2.1: Identificar el Código Existente

Verás un código predeterminado:

```javascript
function myFunction() {

}
```

**Este código hay que REEMPLAZARLO.**

### Paso 2.2: Seleccionar Todo el Código

1. Haz click en el editor (área blanca con código)
2. Usa atajo de teclado:
   - **Windows/Linux:** `Ctrl + A`
   - **Mac:** `Cmd + A`
3. Todo el código se seleccionará (fondo azul/gris)

```javascript
╔═══════════════════════════════════════╗
║ function myFunction() {               ║  ← Todo seleccionado
║                                       ║
║ }                                     ║
╚═══════════════════════════════════════╝
```

### Paso 2.3: Borrar el Código Existente

1. Con todo seleccionado, presiona: **Delete** o **Backspace**
2. El editor quedará vacío

```javascript
┌──────────────────────────────────────┐
│                                      │  ← Vacío
│                                      │
│                                      │
└──────────────────────────────────────┘
```

### Paso 2.4: Abrir el Archivo del Script

1. **En tu computadora**, navega a:
   ```
   DELIA_DJANGO/filtro_basico/sheets-github-sync.gs
   ```

2. **Abre el archivo** con un editor de texto:
   - **Windows:** Notepad, Notepad++, VSCode
   - **Mac:** TextEdit, VSCode
   - **Linux:** gedit, nano, VSCode

3. **Selecciona TODO** el contenido del archivo:
   - `Ctrl + A` (Windows/Linux)
   - `Cmd + A` (Mac)

4. **Copia** el contenido:
   - `Ctrl + C` (Windows/Linux)
   - `Cmd + C` (Mac)

### Paso 2.5: Pegar en Apps Script

1. **Vuelve** a la pestaña del editor de Apps Script
2. **Click** en el área del editor (asegúrate que esté vacío)
3. **Pega** el código:
   - `Ctrl + V` (Windows/Linux)
   - `Cmd + V` (Mac)

```javascript
┌──────────────────────────────────────────────────┐
│ /**                                              │
│  * ==========================                    │
│  * GOOGLE SHEETS → GITHUB SYNC                  │
│  * ==========================                    │
│  */                                             │
│                                                  │
│ const CONFIG = {                                │
│   github: {                                     │
│     owner: 'TU_USUARIO',                        │
│     ...                                         │
└──────────────────────────────────────────────────┘
```

**El script completo debe verse ahora en el editor.**

### Paso 2.6: Guardar el Proyecto

1. Click en el icono de **disco/guardar** (💾) en la parte superior
   - O usa: `Ctrl + S` / `Cmd + S`

2. **Nombrar el proyecto:**
   - Aparecerá un diálogo: "Sin título"
   - Cambia a: `Sync Sheets to GitHub`
   - Click **Aceptar**

```
┌─────────────────────────────────────┐
│  Cambiar el nombre del proyecto    │
├─────────────────────────────────────┤
│  Sync Sheets to GitHub              │  ← Escribe aquí
├─────────────────────────────────────┤
│        [Cancelar]    [Aceptar]      │
└─────────────────────────────────────┘
```

**¡Script guardado! ✅**

---

## ⚙️ PARTE 3: Configurar el Script

### Paso 3.1: Ubicar la Sección CONFIG

En el editor, busca (cerca del inicio del archivo):

```javascript
const CONFIG = {
  github: {
    owner: 'TU_USUARIO',           // ← Línea 20-25 aprox
    repo: 'DELIA_DJANGO',
    token: '',
    branch: 'main'
  },
  ...
```

### Paso 3.2: Editar `owner` (Tu Usuario de GitHub)

1. **Encuentra tu usuario de GitHub:**
   - Ve a: https://github.com
   - Mira la esquina superior derecha
   - Tu usuario es: `@tuusuario`

2. **En el script, modifica la línea:**
   ```javascript
   owner: 'TU_USUARIO',    // ANTES
   owner: 'ivansimo',      // DESPUÉS (usa TU usuario)
   ```

**Ejemplo:**
```javascript
const CONFIG = {
  github: {
    owner: 'ivansimo',        // ✅ Tu usuario real
    repo: 'DELIA_DJANGO',
    token: '',
    branch: 'main'
  },
```

### Paso 3.3: Editar `repo` (Nombre del Repositorio)

1. **Encuentra el nombre de tu repositorio:**
   - En GitHub, ve a tu repositorio
   - La URL es: `https://github.com/ivansimo/DELIA_DJANGO`
   - El nombre del repo es: `DELIA_DJANGO`

2. **En el script:**
   ```javascript
   repo: 'TU_REPO',           // ANTES
   repo: 'DELIA_DJANGO',      // DESPUÉS (usa TU repo)
   ```

### Paso 3.4: Configurar `sheetNames` (Nombre de tu Hoja)

1. **Mira el nombre de tu pestaña en el Sheet:**
   - En la parte inferior de Google Sheets
   - Ves pestañas: `Hoja 1`, `Obras Completas`, etc.

```
┌─────────────────────────────────────┐
│                                     │
│  (tu contenido)                     │
│                                     │
├─────────────────────────────────────┤
│  📄 Obras Completas  +  ...         │  ← ESTE es el nombre
└─────────────────────────────────────┘
```

2. **En el script, busca:**
   ```javascript
   sheets: {
     exportFormat: 'csv',
     sheetNames: ['TU_HOJA'],    // ← Cambiar aquí
   ```

3. **Modifica con el nombre exacto:**
   ```javascript
   sheetNames: ['Obras Completas'],  // ✅ Nombre exacto de tu pestaña
   ```

⚠️ **IMPORTANTE:** El nombre debe ser **EXACTO** (mayúsculas, espacios, tildes)

### Paso 3.5: Configurar `paths` (Ruta del Archivo en GitHub)

1. **Decide dónde guardar el archivo en GitHub:**
   ```javascript
   paths: {
     csv: 'filtro_basico/obras_completas.csv',  // ← Cambiar si es necesario
   ```

2. **Ejemplos de rutas:**
   ```javascript
   // En la raíz del repositorio:
   csv: 'datos.csv'
   
   // En una carpeta:
   csv: 'filtro_basico/obras_completas.csv'
   
   // En subcarpeta:
   csv: 'data/exports/obras.csv'
   ```

### Paso 3.6: Verificar TOKEN (Dejar Vacío por Ahora)

```javascript
token: '',  // ✅ Dejar vacío (lo configuraremos después)
```

### Paso 3.7: Guardar Cambios

1. Click en **💾 Guardar** (o `Ctrl + S` / `Cmd + S`)
2. Espera a que diga: "Última edición: hace unos segundos"

**¡Configuración básica completa! ✅**

---

## 🔐 PARTE 4: Crear Token de GitHub

### Paso 4.1: Ir a GitHub Settings

1. **Abre** https://github.com
2. **Click** en tu foto de perfil (esquina superior derecha)
3. **Click** en **Settings**

```
┌─────────────────────────┐
│  Signed in as ivansimo  │
│                         │
│  ➤ Your profile         │
│  ➤ Your repositories    │
│  ➤ Your organizations   │
│  ─────────────────────  │
│  ➤ Settings      ← AQUÍ │
└─────────────────────────┘
```

### Paso 4.2: Navegar a Developer Settings

1. En la barra lateral izquierda, **scroll hasta el final**
2. Click en **Developer settings** (último elemento)

```
Settings
├─ Profile
├─ Account
├─ Appearance
├─ ...
└─ Developer settings  ← AQUÍ (al final)
```

### Paso 4.3: Ir a Personal Access Tokens

1. En Developer settings, click en **Personal access tokens**
2. Click en **Tokens (classic)**

```
Developer settings
├─ GitHub Apps
├─ OAuth Apps
├─ Personal access tokens
│   ├─ Fine-grained tokens
│   └─ Tokens (classic)  ← AQUÍ
└─ ...
```

### Paso 4.4: Generar Nuevo Token

1. Click en el botón **Generate new token**
2. En el dropdown, selecciona **Generate new token (classic)**

```
┌─────────────────────────────────────┐
│  Personal access tokens (classic)   │
├─────────────────────────────────────┤
│  [Generate new token ▼]             │ ← CLICK
│    ├─ Generate new token (classic)  │ ← Seleccionar
│    └─ Generate new token (beta)     │
└─────────────────────────────────────┘
```

### Paso 4.5: Configurar el Token

**Página: New personal access token**

1. **Note** (nombre del token):
   ```
   Google Sheets Sync - DELIA
   ```

2. **Expiration** (expiración):
   - Recomendado: `90 days`
   - O: `No expiration` (pero menos seguro)

3. **Select scopes** (permisos):
   - ✅ Marca SOLO: **`repo`** (Full control of private repositories)
   
   ```
   Select scopes
   ☐ repo:status
   ☐ repo_deployment
   ☐ public_repo
   ☑ repo                     ← MARCAR ESTE (marca todos los de arriba)
   ☐ repo:invite
   ☐ security_events
   
   (No marcar nada más)
   ```

4. **Scroll hasta el final** de la página

5. Click en el botón verde: **Generate token**

```
┌─────────────────────────────────┐
│  [Generate token]               │ ← CLICK
└─────────────────────────────────┘
```

### Paso 4.6: COPIAR EL TOKEN

**⚠️ MUY IMPORTANTE ⚠️**

Aparecerá una página con tu token:

```
┌───────────────────────────────────────────────────────┐
│  Personal access tokens (classic)                     │
├───────────────────────────────────────────────────────┤
│  Make sure to copy your personal access token now.   │
│  You won't be able to see it again!                   │
│                                                       │
│  ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   [📋]      │ ← COPIAR
│                                                       │
│  ⚠️ Store this in a secure location!                  │
└───────────────────────────────────────────────────────┘
```

1. **Click en el icono de copiar** (📋)
   - O selecciona el token y `Ctrl + C` / `Cmd + C`

2. **PEGA EL TOKEN EN UN LUGAR SEGURO TEMPORALMENTE**
   - Notepad, TextEdit, o un archivo temporal
   - ⚠️ **NO cierres esta pestaña todavía**

3. El token se ve así:
   ```
   ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

**⚠️ NO LO VERÁS DE NUEVO. Si lo pierdes, debes generar uno nuevo.**

---

## 🔑 PARTE 5: Guardar el Token en Apps Script

### Paso 5.1: Volver a Apps Script

1. **Vuelve** a la pestaña de Apps Script
2. Deberías ver tu código guardado

### Paso 5.2: Guardar Token de Forma Segura

**MÉTODO RECOMENDADO: Usar función `setGitHubToken()`**

1. En el editor de Apps Script, busca el selector de funciones:

```
┌─────────────────────────────────────────┐
│  [myFunction ▼]  ▶ Ejecutar  Debug      │  ← Aquí
└─────────────────────────────────────────┘
```

2. **Click en el dropdown** (donde dice `myFunction`)

3. **Busca y selecciona:** `setGitHubToken`

```
Seleccionar función
├─ myFunction
├─ syncToGitHub
├─ setGitHubToken        ← SELECCIONAR ESTE
├─ testConfig
└─ ...
```

4. **Click en ▶ Ejecutar**

```
┌─────────────────────────────────────────┐
│  [setGitHubToken ▼]  ▶ Ejecutar         │  ← CLICK aquí
└─────────────────────────────────────────┘
```

### Paso 5.3: Autorizar el Script (Primera Vez)

**Aparecerá un diálogo de autorización:**

```
┌────────────────────────────────────────────┐
│  Autorización necesaria                    │
├────────────────────────────────────────────┤
│  Sync Sheets to GitHub necesita tu         │
│  autorización para acceder a tu cuenta     │
│  de Google.                                │
│                                            │
│  [Cancelar]  [Revisar permisos]           │ ← CLICK
└────────────────────────────────────────────┘
```

1. Click en **Revisar permisos**

2. **Selecciona tu cuenta de Google**

```
┌────────────────────────────────────────────┐
│  Elige una cuenta                          │
├────────────────────────────────────────────┤
│  📧 tu-email@gmail.com                     │ ← CLICK
└────────────────────────────────────────────┘
```

3. **Aparecerá advertencia de seguridad:**

```
┌────────────────────────────────────────────┐
│  🛡️ Google no ha verificado esta aplicación│
│                                            │
│  Esta aplicación no ha sido verificada    │
│  por Google todavía.                       │
│                                            │
│  [Volver]  [Avanzado]                     │ ← CLICK "Avanzado"
└────────────────────────────────────────────┘
```

4. Click en **Avanzado**

5. Click en **Ir a Sync Sheets to GitHub (no seguro)**

```
Este paso es seguro porque es TU PROPIO SCRIPT.
```

6. **Autorizar permisos:**

```
┌────────────────────────────────────────────┐
│  Sync Sheets to GitHub quiere:            │
├────────────────────────────────────────────┤
│  ✅ Ver y administrar hojas de cálculo     │
│  ✅ Conectar a servicios externos          │
│  ✅ Permitir ejecución cuando no estás     │
│                                            │
│  [Cancelar]  [Permitir]                   │ ← CLICK "Permitir"
└────────────────────────────────────────────┘
```

7. Click en **Permitir**

### Paso 5.4: Ingresar el Token

**Aparecerá un cuadro de diálogo:**

```
┌────────────────────────────────────────────┐
│  Configurar Token de GitHub                │
├────────────────────────────────────────────┤
│  Ingresa tu token personal de GitHub       │
│  (ghp_...):                                │
│                                            │
│  ghp_XXXXXXXXXXXXXXXXXXXXXXXXXX            │ ← PEGAR AQUÍ
│                                            │
│  ⚠️ Este token se guardará de forma        │
│     segura.                                │
│                                            │
│  [Cancelar]  [Aceptar]                    │
└────────────────────────────────────────────┘
```

1. **Pega** el token que copiaste de GitHub
   - `Ctrl + V` / `Cmd + V`

2. Click en **Aceptar**

### Paso 5.5: Verificar que se Guardó

**Aparecerá mensaje de confirmación:**

```
┌────────────────────────────────────────────┐
│  ✅ Token guardado exitosamente de forma   │
│     segura.                                │
│                                            │
│  Ya puedes ejecutar syncToGitHub().        │
│                                            │
│  [Aceptar]                                 │
└────────────────────────────────────────────┘
```

Click en **Aceptar**

**¡Token configurado! 🎉**

---

## ✅ PARTE 6: Verificar Configuración

### Paso 6.1: Ejecutar Tests

1. En el selector de funciones, selecciona: **`runAllTests`**

```
[runAllTests ▼]  ▶ Ejecutar
```

2. Click en **▶ Ejecutar**

### Paso 6.2: Ver Resultados de Tests

1. Click en **Ver** → **Registros** (o `Ctrl + Enter`)

```
┌────────────────────────────────────────────┐
│  🧪 EJECUTANDO TESTS                       │
│  ==================================        │
│                                            │
│  ▶️ Test: Configuración                    │
│  ✅ Token encontrado                       │
│  ✅ Owner y repo configurados              │
│  ✅ Hojas configuradas                     │
│  ✅ Configuración válida                   │
│                                            │
│  ▶️ Test: Conexión GitHub                  │
│  ✅ Conectado a: ivansimo/DELIA_DJANGO     │
│     Rama por defecto: main                 │
│     Privado: No                            │
│                                            │
│  ▶️ Test: Lectura de hoja                  │
│  ✅ 2100 filas leídas de "Obras Completas" │
│     Columnas: 32                           │
│                                            │
│  📊 RESUMEN DE TESTS                       │
│  ✅ Configuración: PASS                    │
│  ✅ Conexión GitHub: PASS                  │
│  ✅ Lectura de hoja: PASS                  │
│                                            │
│  🎉 Todos los tests pasaron.               │
└────────────────────────────────────────────┘
```

**Si todos pasan (✅): ¡Perfecto! Continúa.**

**Si alguno falla (❌):** Ve a la sección de Troubleshooting al final.

---

## 🚀 PARTE 7: Primera Sincronización

### Paso 7.1: Ejecutar Sincronización Manual

1. Selector de funciones: **`syncToGitHub`**

```
[syncToGitHub ▼]  ▶ Ejecutar
```

2. Click en **▶ Ejecutar**

3. **Espera** (puede tomar 10-30 segundos)

### Paso 7.2: Ver Logs de Ejecución

1. **Ver** → **Registros** (o `Ctrl + Enter`)

```
┌────────────────────────────────────────────┐
│  🚀 Iniciando sincronización...            │
│  📊 Hojas a exportar: Obras Completas      │
│                                            │
│  📋 Procesando hoja: Obras Completas       │
│  ✅ 2100 filas leídas                      │
│  📁 Ruta destino: filtro_basico/obras.csv  │
│  🔄 Cambios detectados. Haciendo push...   │
│  ✅ Push exitoso. Commit: abc123def456     │
│                                            │
│  🎉 Sincronización completada en 12.5s     │
│  ✅ Exitosas: 1/1                          │
└────────────────────────────────────────────┘
```

**Si ves `✅ Push exitoso`: ¡Funcionó! 🎉**

### Paso 7.3: Verificar en GitHub

1. **Ve a tu repositorio en GitHub:**
   ```
   https://github.com/TU_USUARIO/TU_REPO
   ```

2. **Navega** a la ruta que configuraste:
   ```
   filtro_basico/obras_completas.csv
   ```

3. **Deberías ver** el archivo con los datos de tu hoja

4. **Click en el archivo** para ver su contenido

5. **Click en "History"** para ver el commit automático

```
┌────────────────────────────────────────────┐
│  filtro_basico / obras_completas.csv       │
├────────────────────────────────────────────┤
│  📄 2,100 lines (42 KB)                    │
│                                            │
│  [Raw]  [Blame]  [History]  [...]          │
│                                            │
│  ID,Título,Autor,Tipo de Obra              │
│  3058,A Dios por razon de estado,Anónimo   │
│  ...                                       │
└────────────────────────────────────────────┘
```

**¡Tu primera sincronización exitosa! 🎉**

---

## ⏰ PARTE 8: Automatizar con Triggers

### Paso 8.1: Abrir Panel de Triggers

1. En Apps Script, en la barra lateral izquierda
2. Click en el icono del **reloj** ⏰ (Activadores)

```
Apps Script
├─ 📄 Archivos
├─ ⏰ Activadores      ← CLICK AQUÍ
├─ 📊 Ejecuciones
└─ ⚙️ Configuración
```

### Paso 8.2: Crear Nuevo Trigger

1. Click en **+ Agregar activador** (esquina inferior derecha)

```
┌────────────────────────────────────────────┐
│  Activadores del proyecto                  │
├────────────────────────────────────────────┤
│  No hay activadores configurados.          │
│                                            │
│                    [+ Agregar activador]   │ ← CLICK
└────────────────────────────────────────────┘
```

### Paso 8.3: Configurar el Trigger

**Aparecerá un formulario:**

```
┌────────────────────────────────────────────┐
│  Agregar activador                         │
├────────────────────────────────────────────┤
│  Elige la función que se ejecutará:        │
│  [syncToGitHub         ▼]                  │ ← Seleccionar
│                                            │
│  Elige el origen del evento:               │
│  [Según tiempo         ▼]                  │ ← Seleccionar
│                                            │
│  Tipo de activador de tiempo:              │
│  [Activador de temporizador por tiempo ▼]  │
│                                            │
│  Seleccionar intervalo de tiempo (horas):  │
│  [Cada hora            ▼]                  │ ← Seleccionar
│                                            │
│  Notificaciones de errores:                │
│  [Notificarme de inmediato ▼]              │
│                                            │
│  [Cancelar]  [Guardar]                     │
└────────────────────────────────────────────┘
```

**Configuración recomendada:**

1. **Función:** `syncToGitHub`
2. **Origen del evento:** `Según tiempo`
3. **Tipo:** `Activador de temporizador por tiempo`
4. **Intervalo:** `Cada hora`
5. **Notificaciones:** `Notificarme de inmediato`

### Paso 8.4: Guardar el Trigger

1. Click en **Guardar**

2. **Puede aparecer otro diálogo de autorización** (si es la primera vez)
   - Repite el proceso de autorización (Paso 5.3)

3. Verás el trigger en la lista:

```
┌────────────────────────────────────────────────────────┐
│  Activadores del proyecto                              │
├────────────────────────────────────────────────────────┤
│  Función         Evento           Frecuencia           │
│  syncToGitHub    Según tiempo     Cada hora      [...] │
│                                                        │
└────────────────────────────────────────────────────────┘
```

**¡Trigger configurado! Ahora se ejecutará automáticamente cada hora. ⏰**

---

## 🎨 PARTE 9: Crear Menú en Google Sheets

### Paso 9.1: Ejecutar función onOpen

Esta función crea un menú personalizado en tu Google Sheet.

1. En Apps Script, selector de funciones: **`onOpen`**
2. Click en **▶ Ejecutar**

### Paso 9.2: Volver a Google Sheets

1. **Vuelve** a la pestaña de tu Google Sheet
2. **Refresca** la página (`F5` o `Ctrl + R` / `Cmd + R`)

### Paso 9.3: Verificar el Menú

En la barra de menú, deberías ver un nuevo menú:

```
┌─────────────────────────────────────────────┐
│ Archivo  Editar  Ver  ...  🔄 GitHub Sync  │ ← NUEVO MENÚ
└─────────────────────────────────────────────┘
```

Click en **🔄 GitHub Sync** para ver opciones:

```
🔄 GitHub Sync
  ├─ 📤 Sincronizar ahora
  ├─ ──────────────────
  ├─ 🔧 Configurar token
  ├─ 🧪 Ejecutar tests
  ├─ 📊 Ver estadísticas
  ├─ ──────────────────
  └─ 📖 Ayuda
```

**¡Ahora puedes sincronizar directamente desde el Sheet! 🎉**

---

## 📊 PARTE 10: Uso Diario

### Sincronizar Manualmente

**Opción 1: Desde el Menú del Sheet**
1. Click en **🔄 GitHub Sync**
2. Click en **📤 Sincronizar ahora**
3. Espera unos segundos
4. ¡Listo!

**Opción 2: Desde Apps Script**
1. Ve a Apps Script
2. Ejecuta `syncToGitHub`

### Ver Estadísticas

1. **🔄 GitHub Sync** → **📊 Ver estadísticas**
2. **Ver** → **Registros** para ver detalles

### Ejecutar Tests

1. **🔄 GitHub Sync** → **🧪 Ejecutar tests**
2. Verifica que todo funcione correctamente

---

## 🐛 Troubleshooting

### Error: "Token no encontrado"

**Solución:**
1. Ejecuta `setGitHubToken()` de nuevo
2. Ingresa el token correctamente

### Error: "Hoja no encontrada"

**Solución:**
1. Verifica el nombre exacto de la pestaña en Google Sheets
2. En `CONFIG.sheets.sheetNames`, usa el nombre **exacto**
3. Respeta mayúsculas, tildes y espacios

### Error: "404 Not Found" (GitHub)

**Solución:**
1. Verifica `owner` y `repo` en CONFIG
2. Asegúrate de tener permisos en el repositorio
3. Verifica que la ruta del archivo sea correcta

### No aparece el menú "GitHub Sync"

**Solución:**
1. Ejecuta manualmente `onOpen()` en Apps Script
2. Refresca la página del Google Sheet
3. Espera 1-2 minutos y vuelve a refrescar

### "Authorization required" constantemente

**Solución:**
1. Completa el proceso de autorización completo
2. Click en "Permitir" todas las veces necesarias
3. No uses modo incógnito

---

## 📋 Checklist Final

Verifica que completaste todos los pasos:

- [ ] ✅ Abrí Google Sheets
- [ ] ✅ Accedí a Extensiones → Apps Script
- [ ] ✅ Copié el código de `sheets-github-sync.gs`
- [ ] ✅ Guardé el proyecto con nombre
- [ ] ✅ Configuré `owner`, `repo`, `sheetNames`, `paths`
- [ ] ✅ Creé token en GitHub
- [ ] ✅ Copié el token
- [ ] ✅ Ejecuté `setGitHubToken()` y pegué el token
- [ ] ✅ Ejecuté `runAllTests()` - todos pasan
- [ ] ✅ Ejecuté `syncToGitHub()` - primera sincronización exitosa
- [ ] ✅ Verifiqué el archivo en GitHub
- [ ] ✅ Configuré trigger automático (cada hora)
- [ ] ✅ Ejecuté `onOpen()` para crear menú
- [ ] ✅ Veo el menú "GitHub Sync" en Sheets

**Si todos tienen ✅: ¡Configuración completa! 🎉**

---

## 🎉 ¡Felicitaciones!

Tu sistema de sincronización automática está configurado y funcionando.

### Qué Hace Ahora Automáticamente:

1. ✅ Cada hora, verifica si hay cambios en tu Google Sheet
2. ✅ Si hay cambios, exporta a CSV/JSON
3. ✅ Hace push automático a GitHub
4. ✅ GitHub Pages se actualiza con los nuevos datos
5. ✅ Los usuarios ven los cambios en la web

### Próximos Pasos:

- Edita tu Google Sheet normalmente
- Los cambios se sincronizarán automáticamente
- Verifica GitHub ocasionalmente
- Usa el menú "GitHub Sync" para sincronizar manualmente

---

## 📞 Soporte

Si tienes problemas adicionales:

1. **Consulta:** `FAQ_TROUBLESHOOTING.md`
2. **Ejecuta:** `healthCheck()` en Apps Script
3. **Revisa:** Logs con `Ctrl + Enter`
4. **Tests:** `runAllTests()` para diagnóstico

---

**¡Disfruta tu sincronización automática! 🚀**




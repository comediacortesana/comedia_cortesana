# 🔄 Google Sheets → GitHub Sync

## 📚 Documentación Completa

### 🚀 Inicio Rápido (5 minutos)

**¿Qué hace esto?**
Sincroniza automáticamente tus Google Sheets con GitHub sin servidores, 100% gratis.

**Archivos principales:**

1. **[sheets-github-sync.gs](./sheets-github-sync.gs)** 
   - Script principal (copiar a Apps Script)
   - Funcionalidad básica y completa
   - ⭐ **EMPIEZA AQUÍ**

2. **[AUTOMATIZACION_SHEETS_GITHUB.md](./AUTOMATIZACION_SHEETS_GITHUB.md)**
   - Guía completa paso a paso
   - Instalación y configuración
   - Explicación de todas las características

3. **[CONFIGURACION_EJEMPLOS.md](./CONFIGURACION_EJEMPLOS.md)**
   - Ejemplos de configuración para casos reales
   - 6 casos de uso diferentes
   - Configuraciones listas para copiar/pegar

4. **[FAQ_TROUBLESHOOTING.md](./FAQ_TROUBLESHOOTING.md)**
   - Solución a 10+ errores comunes
   - Preguntas frecuentes
   - Debug y monitoreo

5. **[sheets-github-sync-advanced.gs](./sheets-github-sync-advanced.gs)**
   - Versión avanzada con funcionalidades extra
   - Validación, backups, notificaciones
   - Para usuarios avanzados

6. **[GUIA_PASO_A_PASO_APPS_SCRIPT.md](./GUIA_PASO_A_PASO_APPS_SCRIPT.md)** 🆕 ⭐
   - **Guía DETALLADA paso a paso**
   - Instrucciones EXPLÍCITAS con capturas visuales
   - Cómo acceder a Apps Script en Google Workspace
   - **Ideal para principiantes**

---

## ⚡ Setup Rápido (5 pasos)

**🆕 ¿Primera vez con Apps Script?**  
👉 Sigue la **[GUIA_PASO_A_PASO_APPS_SCRIPT.md](./GUIA_PASO_A_PASO_APPS_SCRIPT.md)** con instrucciones detalladas

**Si ya conoces Apps Script:**

### 1. Copiar Script

1. Abre tu Google Sheet
2. **Extensiones** → **Apps Script**
3. Copia contenido de `sheets-github-sync.gs`
4. Pega y guarda

### 2. Configurar

```javascript
const CONFIG = {
  github: {
    owner: 'TU_USUARIO',        // ej: ivansimo
    repo: 'TU_REPO',            // ej: DELIA_DJANGO
    token: '',                  // dejar vacío, usar paso 4
    branch: 'main'
  },
  sheets: {
    exportFormat: 'csv',
    sheetNames: ['TU_HOJA']     // ej: Obras Completas
  },
  paths: {
    csv: 'ruta/archivo.csv'     // ej: filtro_basico/obras_completas.csv
  },
  options: {
    checkForChanges: true       // ⭐ Recomendado: solo push si hay cambios
  }
};
```

### 3. Token GitHub

1. Ve a: https://github.com/settings/tokens
2. **Generate new token (classic)**
3. Nombre: `Google Sheets Sync`
4. Scope: ✅ `repo`
5. **Generate token**
6. ⚠️ Copia el token (solo lo verás una vez)

### 4. Guardar Token (seguro)

En Apps Script, ejecuta esta función UNA VEZ:

```javascript
function setupToken() {
  const token = 'ghp_XXXXXXXXXXXXXXXX';  // TU token aquí
  PropertiesService.getScriptProperties()
    .setProperty('GITHUB_TOKEN', token);
  Logger.log('✅ Token guardado');
}
```

O usa el menú:
- **GitHub Sync** → **Configurar token**
- Ingresa el token en el diálogo

### 5. Probar

```javascript
// Ejecutar en Apps Script:
runAllTests();

// Si todo está ✅:
syncToGitHub();
```

Verifica en GitHub que el archivo apareció! 🎉

---

## 🤖 Automatizar

### Opción 1: Cada Hora (Recomendado)

En Apps Script:
1. **⏰ Activadores** (menú lateral)
2. **+ Agregar activador**
3. Configuración:
   - Función: `syncToGitHub`
   - Evento: `Según tiempo`
   - Intervalo: `Cada hora`
4. **Guardar**

### Opción 2: Al Editar (Avanzado)

1. **+ Agregar activador**
2. Configuración:
   - Función: `syncToGitHub`
   - Evento: `Al editar`

⚠️ Activa `checkForChanges: true` para evitar pushes innecesarios.

---

## ✨ Características

### Básicas (sheets-github-sync.gs)

- ✅ Exporta CSV o JSON
- ✅ Detección de cambios (solo push si hay cambios)
- ✅ Múltiples hojas
- ✅ Manejo de errores robusto
- ✅ Logs detallados
- ✅ Estadísticas de sync
- ✅ Menú personalizado en Sheets

### Avanzadas (sheets-github-sync-advanced.gs)

- ✅ Validación de datos antes del push
- ✅ Backup automático en Google Drive
- ✅ Notificaciones a Slack/Discord/Email
- ✅ Debounce para triggers de edición
- ✅ Limpieza y formateo de datos
- ✅ Health checks automáticos

---

## 📊 Flujo de Trabajo

```
┌──────────────────┐
│  Google Sheets   │  ← Investigadores editan
└────────┬─────────┘
         │
         │ (Cada hora)
         ↓
┌──────────────────┐
│  Apps Script     │  ← Detecta cambios
└────────┬─────────┘
         │
         │ (Si hay cambios)
         ↓
┌──────────────────┐
│  GitHub API      │  ← Push automático
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│  GitHub Repo     │  ← Archivo actualizado
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│  GitHub Pages    │  ← Web actualizada
└──────────────────┘
```

---

## 🎯 Casos de Uso

### 1. Edición Colaborativa
- 3-5 investigadores editan Google Sheet
- Sync cada hora a GitHub
- GitHub Pages muestra datos actualizados
- **Setup:** Trigger cada hora + `checkForChanges: true`

### 2. Backup Diario
- Backup automático cada medianoche
- Guarda en Google Drive + GitHub
- Notifica por email
- **Setup:** Trigger diario + backup habilitado

### 3. Tiempo Real
- Push inmediato tras edición
- Debounce de 5 minutos
- Notifica a Slack
- **Setup:** Trigger al editar + debounce + Slack

### 4. Múltiples Hojas
- Obras, Autores, Lugares, Representaciones
- Cada hoja → archivo separado
- Validación de datos
- **Setup:** `multiSheet.enabled: true`

Ver ejemplos completos en: **[CONFIGURACION_EJEMPLOS.md](./CONFIGURACION_EJEMPLOS.md)**

---

## 🐛 Problemas Comunes

### Error 401: Token inválido
→ Regenera token en GitHub  
→ Ejecuta `setGitHubToken()` con el nuevo token

### Error 404: Repo no encontrado
→ Verifica `owner` y `repo` en CONFIG  
→ Asegúrate de tener acceso al repositorio

### Error 403: Sin permisos
→ Token necesita scope `repo`  
→ Regenera token con permisos correctos

### No hace push
→ Verifica logs: **Ver** → **Registros**  
→ Ejecuta `runAllTests()` para diagnóstico

**Más soluciones:** [FAQ_TROUBLESHOOTING.md](./FAQ_TROUBLESHOOTING.md)

---

## 💡 Tips

1. **Empezar simple:** Usa script básico primero
2. **Probar manualmente:** Ejecuta varias veces antes de automatizar
3. **Usar checkForChanges:** Evita commits vacíos
4. **Activar backups:** Google Drive es gratis, úsalo
5. **Logs son tus amigos:** Revísalos siempre

---

## 📖 Documentación

| Archivo | Descripción |
|---------|-------------|
| **[AUTOMATIZACION_SHEETS_GITHUB.md](./AUTOMATIZACION_SHEETS_GITHUB.md)** | 📚 Guía completa (instalación, configuración, uso) |
| **[CONFIGURACION_EJEMPLOS.md](./CONFIGURACION_EJEMPLOS.md)** | 📝 Ejemplos de configuración para 6 casos reales |
| **[FAQ_TROUBLESHOOTING.md](./FAQ_TROUBLESHOOTING.md)** | ❓ Solución a 10+ errores + preguntas frecuentes |
| **[sheets-github-sync.gs](./sheets-github-sync.gs)** | 💻 Script principal (básico, completo) |
| **[sheets-github-sync-advanced.gs](./sheets-github-sync-advanced.gs)** | 🚀 Script avanzado (validación, backup, notificaciones) |

---

## 🎓 Recursos

- **Google Apps Script:** https://developers.google.com/apps-script
- **GitHub API:** https://docs.github.com/en/rest
- **GitHub Tokens:** https://docs.github.com/en/authentication

---

## 📊 Estado del Proyecto

- ✅ Script básico funcionando
- ✅ Script avanzado con todas las características
- ✅ Documentación completa
- ✅ Ejemplos de configuración
- ✅ Troubleshooting y FAQ
- ✅ 100% gratuito
- ✅ Sin servidores externos
- ✅ Producción-ready

---

## 🤝 Contribuir

¿Mejoras o nuevas funcionalidades?

1. Edita los scripts `.gs`
2. Actualiza la documentación
3. Comparte tus casos de uso

---

## ⚠️ Seguridad

- ⚠️ **NUNCA** pongas el token directamente en el código
- ✅ Usa `PropertiesService` para guardar el token
- ✅ Token tiene solo permisos necesarios (`repo`)
- ✅ Revisa accesos en: https://github.com/settings/applications

---

## 🎉 ¡Listo para Empezar!

1. Lee: **[AUTOMATIZACION_SHEETS_GITHUB.md](./AUTOMATIZACION_SHEETS_GITHUB.md)**
2. Copia: **[sheets-github-sync.gs](./sheets-github-sync.gs)**
3. Configura según tu caso en: **[CONFIGURACION_EJEMPLOS.md](./CONFIGURACION_EJEMPLOS.md)**
4. Si hay problemas: **[FAQ_TROUBLESHOOTING.md](./FAQ_TROUBLESHOOTING.md)**

**¡A sincronizar! 🚀**

---

## 📞 Soporte

- Revisa primero: **FAQ_TROUBLESHOOTING.md**
- Ejecuta: `healthCheck()` para diagnóstico
- Consulta logs: **Ver** → **Registros de ejecución**

---

**Versión:** 2.0  
**Última actualización:** 2025-10-31  
**Licencia:** MIT (úsalo libremente)  
**Autor:** AI Assistant  

---

💡 **Tip:** Empieza con configuración simple (caso 1 en CONFIGURACION_EJEMPLOS.md), luego escala según necesites.


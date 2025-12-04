# 🚀 Tutorial: Publicar en GitHub Pages (100% GRATIS)

## ¿Es de pago?
**NO. GitHub Pages es completamente GRATUITO para siempre.**

- ✅ Sin tarjeta de crédito
- ✅ Sin límite de tiempo
- ✅ HTTPS incluido
- ✅ Repositorios públicos ilimitados

---

## 📝 Método 1: Desde GitHub Web (Sin comandos)

### Paso 1: Crear repositorio
1. Ve a https://github.com/new
2. Nombre del repositorio: `teatro-espanol-filtro`
3. Descripción: `Filtro interactivo de obras del Teatro Español del Siglo de Oro`
4. ✅ Public (para GitHub Pages gratis)
5. ✅ Add a README file
6. Click **"Create repository"**

### Paso 2: Subir el archivo
1. En tu repositorio, click **"Add file"** → **"Upload files"**
2. Arrastra `index.html` desde tu Mac
3. Commit message: `Add filtro básico`
4. Click **"Commit changes"**

### Paso 3: Activar GitHub Pages
1. En tu repositorio, ve a **Settings** (⚙️)
2. En el menú lateral, click **"Pages"**
3. En "Source", selecciona:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **"Save"**
5. Espera 1-2 minutos

### Paso 4: Ver tu sitio
Tu sitio estará en:
```
https://TU-USUARIO.github.io/teatro-espanol-filtro/
```

**¡Listo!** 🎉

---

## 💻 Método 2: Desde Terminal (Con Git)

### Requisitos previos:
- Git instalado
- Cuenta de GitHub
- Configurado SSH o HTTPS para GitHub

### Comandos:

```bash
# 1. Navegar a la carpeta del filtro
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/filtro_basico

# 2. Inicializar git
git init

# 3. Añadir archivos
git add index.html README.md

# 4. Primer commit
git commit -m "Initial commit: Filtro de Teatro Español"

# 5. Renombrar rama a main
git branch -M main

# 6. Conectar con GitHub (crea el repo primero en github.com)
git remote add origin https://github.com/TU-USUARIO/teatro-espanol-filtro.git

# 7. Subir código
git push -u origin main

# 8. Activar GitHub Pages (hacer desde la web de GitHub en Settings → Pages)
```

### Luego en GitHub.com:
1. Ve a tu repositorio
2. Settings → Pages
3. Source: `main` branch
4. Save

---

## 🎯 Método 3: GitHub Desktop (Visual)

### Si prefieres interfaz gráfica:

1. **Descargar GitHub Desktop**
   - https://desktop.github.com/

2. **Crear repositorio:**
   - File → New Repository
   - Name: `teatro-espanol-filtro`
   - Local path: `/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/filtro_basico`

3. **Copiar archivos:**
   - Copia `index.html` a la carpeta del repo
   - GitHub Desktop detectará el cambio automáticamente

4. **Commit:**
   - Añade mensaje: "Initial commit"
   - Click "Commit to main"

5. **Publicar:**
   - Click "Publish repository"
   - ✅ Deja Public marcado
   - Click "Publish repository"

6. **Activar Pages:**
   - Click "View on GitHub"
   - Settings → Pages → Enable

---

## ⚡ Método ULTRA-RÁPIDO: GitHub CLI

Si tienes `gh` instalado:

```bash
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/filtro_basico

# Crear repo y subir en UN comando
gh repo create teatro-espanol-filtro --public --source=. --push

# Activar Pages
gh api repos/:owner/teatro-espanol-filtro/pages \
  -X POST \
  -f source[branch]=main \
  -f source[path]=/
```

---

## 🔧 Personalizar URL (Opcional, también GRATIS)

### Opción A: Dominio de GitHub
Por defecto: `usuario.github.io/teatro-espanol-filtro`

### Opción B: Dominio personalizado (necesitas comprar dominio)
Ejemplo: `teatroespanol.com`
- Compras dominio (~$10/año en Namecheap, Google Domains, etc.)
- En Settings → Pages → Custom domain
- GitHub Pages sigue siendo GRATIS, solo pagas el dominio

---

## 📊 Comparación de Costos

| Servicio | Costo | Límites |
|----------|-------|---------|
| **GitHub Pages** | 🆓 $0/mes | 100GB ancho de banda |
| Netlify (gratis) | 🆓 $0/mes | 100GB ancho de banda |
| Vercel (gratis) | 🆓 $0/mes | 100GB ancho de banda |
| AWS S3 + CloudFront | 💰 ~$1-5/mes | Depende del tráfico |
| Heroku (static) | 💰 $7/mes | Sin límites |

**Conclusión: GitHub Pages es la mejor opción gratuita.**

---

## 🔒 Privacidad y Seguridad

### Repositorio Público (GRATIS):
- ✅ GitHub Pages gratis
- ⚠️ Código visible para todos
- ✅ Perfecto para tu filtro (no tiene datos sensibles)

### Repositorio Privado (GRATIS con cuenta Pro):
- GitHub Pro: $4/mes (incluye Pages para repos privados)
- O gratis si eres estudiante/profesor (GitHub Education)

### Tu caso:
- ✅ Tu HTML no tiene datos sensibles
- ✅ No tiene claves API
- ✅ Solo tiene datos de ejemplo
- **→ Repositorio público es perfecto**

---

## 🚀 Después de Publicar

### Actualizar el sitio:
```bash
# Editas index.html
# Luego:
git add index.html
git commit -m "Actualización de filtros"
git push

# GitHub Pages se actualiza automáticamente en 1-2 minutos
```

### Ver estadísticas de visitas (GRATIS):
1. Integra Google Analytics (opcional)
2. O usa GitHub Traffic en Settings → Insights → Traffic

---

## 💡 Tips Profesionales

### 1. README.md atractivo
Añade esto a tu README para que se vea profesional:

```markdown
# 🎭 Teatro Español del Siglo de Oro - Filtro Interactivo

Herramienta web para filtrar y explorar obras del teatro español del Siglo de Oro.

## 🌐 Demo en Vivo
https://TU-USUARIO.github.io/teatro-espanol-filtro/

## 🔍 Características
- 12 filtros diferentes
- Búsqueda en tiempo real
- Diseño responsive
- Sin dependencias externas

## 📖 Uso
Abre el link de demo y utiliza los filtros para explorar las obras.
```

### 2. Añade un favicon
Crea `favicon.ico` y súbelo junto con `index.html`

### 3. Conecta con datos reales
Cuando tengas tu API Django lista, actualiza la URL en el fetch del JavaScript

---

## 🆘 Solución de Problemas

### "404 Not Found"
- Espera 2-3 minutos después de activar Pages
- Verifica que el archivo se llame exactamente `index.html`
- Verifica que la rama sea `main` en Settings → Pages

### "Repo no aparece"
- Asegúrate que el repositorio es **público**
- Repos privados necesitan GitHub Pro

### "Changes no se ven"
- GitHub Pages cachea los archivos
- Ctrl+Shift+R (Windows) o Cmd+Shift+R (Mac) para refrescar sin caché
- O espera 1-2 minutos

---

## ✅ Checklist Final

- [ ] Repositorio creado en GitHub
- [ ] Archivo `index.html` subido
- [ ] GitHub Pages activado en Settings
- [ ] Sitio visible en `usuario.github.io/proyecto`
- [ ] URL compartida con colegas
- [ ] (Opcional) README.md actualizado
- [ ] (Opcional) Google Analytics añadido

---

## 🎉 ¡Felicidades!

Tu filtro está publicado GRATIS y para siempre en GitHub Pages.

**Ventajas finales:**
- ✅ URL permanente
- ✅ HTTPS automático
- ✅ Actualizaciones fáciles con git push
- ✅ Control de versiones completo
- ✅ $0 de costo
- ✅ 99.9% uptime garantizado por GitHub

**Tu sitio:** `https://TU-USUARIO.github.io/teatro-espanol-filtro/`



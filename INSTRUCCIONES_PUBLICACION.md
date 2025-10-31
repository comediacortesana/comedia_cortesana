# 🌐 Cómo Publicar el Filtro Básico - Opciones Gratuitas

## 1️⃣ GitHub Gist (Más Simple) ⭐

### Pasos:
1. Ve a https://gist.github.com/
2. Inicia sesión con tu cuenta de GitHub
3. Copia todo el contenido de `index.html`
4. Pega en el editor de Gist
5. Nombra el archivo: `teatro_espanol_filtro.html`
6. Click en "Create public gist"
7. **Para ver funcionando**: Usa este servicio:
   - URL del Gist: `https://gist.github.com/tu-usuario/HASH-DEL-GIST`
   - Para ver en vivo: `https://htmlpreview.github.io/?https://gist.githubusercontent.com/tu-usuario/HASH-DEL-GIST/raw/teatro_espanol_filtro.html`

### Ejemplo:
```
Gist: https://gist.github.com/ivansimo/abc123def456
Vista: https://htmlpreview.github.io/?https://gist.githubusercontent.com/ivansimo/abc123def456/raw/teatro_espanol_filtro.html
```

---

## 2️⃣ CodePen (Ideal para Demos) 🎨

### Ventajas:
- ✅ Visualización instantánea
- ✅ Gratis para siempre
- ✅ Muy popular para compartir
- ✅ Editor en vivo con preview

### Pasos:
1. Ve a https://codepen.io/
2. Click en "Create" → "Pen"
3. En la pestaña **HTML**: Pega el contenido del `<body>` (sin `<!DOCTYPE>`, `<html>`, `<head>`)
4. En la pestaña **CSS**: Pega el contenido del `<style>`
5. En la pestaña **JS**: Pega el contenido del `<script>`
6. Click en "Save"
7. Comparte la URL: `https://codepen.io/tu-usuario/pen/codigo-pen`

### Vista embebida:
También puedes embeber en cualquier sitio:
```html
<iframe height="600" style="width: 100%;" scrolling="no" 
  src="https://codepen.io/tu-usuario/pen/codigo-pen" 
  frameborder="no" allowtransparency="true" allowfullscreen="true">
</iframe>
```

---

## 3️⃣ JSFiddle (Similar a CodePen)

### Pasos:
1. Ve a https://jsfiddle.net/
2. Separa HTML, CSS y JavaScript en sus respectivos paneles
3. Click en "Save"
4. URL: `https://jsfiddle.net/tu-usuario/codigo-fiddle/`

---

## 4️⃣ GitHub Pages (Hosting Completo) 🚀

### Ventajas:
- ✅ URL personalizada: `tu-usuario.github.io/proyecto`
- ✅ Gratis para siempre
- ✅ Control total del código
- ✅ Puedes añadir múltiples páginas

### Pasos:
1. Crea un repositorio en GitHub: `teatro-espanol-filtro`
2. Sube el archivo `index.html`
3. Ve a Settings → Pages
4. En "Source" selecciona `main` branch
5. Click en "Save"
6. Tu sitio estará en: `https://tu-usuario.github.io/teatro-espanol-filtro/`

### Comandos:
```bash
# Opción A: Crear nuevo repositorio
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/filtro_basico
git init
git add index.html
git commit -m "Initial commit: Filtro de obras del Siglo de Oro"
git branch -M main
git remote add origin https://github.com/tu-usuario/teatro-espanol-filtro.git
git push -u origin main

# Luego activar Pages en GitHub Settings
```

---

## 5️⃣ Netlify Drop (Drag & Drop) 🎯

### Ventajas:
- ✅ Sin cuenta necesaria (opcionalmente puedes crear una)
- ✅ Simplemente arrastra el archivo
- ✅ URL única automática
- ✅ HTTPS automático

### Pasos:
1. Ve a https://app.netlify.com/drop
2. Arrastra la carpeta `filtro_basico` (o solo el `index.html`)
3. ¡Listo! Te da una URL tipo: `https://random-name.netlify.app`
4. (Opcional) Crea cuenta para personalizar el nombre

---

## 6️⃣ Vercel (Similar a Netlify)

### Pasos:
1. Ve a https://vercel.com
2. Crea cuenta gratuita
3. Click en "Add New" → "Project"
4. Importa desde GitHub o arrastra archivos
5. Deploy automático

---

## 🎯 Mi Recomendación según tu uso:

### Para compartir RÁPIDO:
→ **GitHub Gist** + **HTMLPreview.github.io**

### Para demostración VISUAL:
→ **CodePen** (el más popular para demos)

### Para proyecto SERIO con actualizaciones:
→ **GitHub Pages** (control total)

### Para máxima SIMPLICIDAD:
→ **Netlify Drop** (literalmente arrastrar y soltar)

---

## 📝 Ejemplo Real - GitHub Gist

### Paso a paso detallado:

1. **Crear el Gist:**
```
https://gist.github.com/ → "New gist"
Filename: teatro_espanol_filtro.html
Description: Filtro interactivo de obras del Teatro Español del Siglo de Oro
[Pegar contenido completo de index.html]
→ Create public gist
```

2. **Obtener URL para visualizar:**
```
Si tu Gist es: https://gist.github.com/ivansimo/abc123
Entonces usa: https://htmlpreview.github.io/?https://gist.githubusercontent.com/ivansimo/abc123/raw/teatro_espanol_filtro.html
```

3. **Alternativa con RawGit:**
```
https://raw.githack.com/gist/ivansimo/abc123/teatro_espanol_filtro.html
```

---

## 💡 Consejos:

1. **Sin datos sensibles**: Este HTML no tiene contraseñas ni APIs, ¡perfecto para publicar!
2. **Datos de ejemplo**: Los 3 ejemplos incluidos son perfectos para demo
3. **Actualizable**: Gist y GitHub Pages te dejan actualizar cuando quieras
4. **Compartible**: Todas estas opciones te dan una URL corta para compartir

---

## 🔗 Links Útiles:

- GitHub Gist: https://gist.github.com/
- HTMLPreview: https://htmlpreview.github.io/
- CodePen: https://codepen.io/
- JSFiddle: https://jsfiddle.net/
- Netlify Drop: https://app.netlify.com/drop
- GitHub Pages Docs: https://pages.github.com/
- Vercel: https://vercel.com

---

## ⚡ Versión Ultra-Rápida (1 minuto):

```bash
# 1. Copia el contenido de index.html
# 2. Ve a https://gist.github.com/
# 3. Pega y crea gist público
# 4. Copia la URL del Gist
# 5. Ve a https://htmlpreview.github.io/
# 6. Pega la URL del raw del Gist
# 7. ¡Listo! Comparte la URL resultante
```

Todas estas opciones son **100% gratuitas** y **duran para siempre** (mientras las plataformas existan, que son muy estables).



# 🔄 Diferencia entre GitHub Pages y GitHub Actions

## 📊 Resumen Visual

```
┌─────────────────────────────────────────────────────────────┐
│                    TU REPOSITORIO GITHUB                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📁 Código fuente (HTML, CSS, JS, Python, etc.)              │
│                                                               │
│  ┌──────────────────────┐    ┌──────────────────────┐       │
│  │   GITHUB PAGES      │    │   GITHUB ACTIONS      │       │
│  ├──────────────────────┤    ├──────────────────────┤       │
│  │ ✅ Sirve archivos   │    │ ✅ Ejecuta scripts   │       │
│  │    estáticos        │    │    (Python, Node,    │       │
│  │                     │    │     Bash, etc.)       │       │
│  │ ✅ HTML/CSS/JS      │    │                      │       │
│  │                     │    │ ✅ Automatización    │       │
│  │ ✅ Hosting web      │    │    (CI/CD)           │       │
│  │                     │    │                      │       │
│  │ ❌ NO ejecuta       │    │ ✅ Schedule (cron)   │       │
│  │    código servidor  │    │                      │       │
│  │                     │    │ ✅ Eventos (push,    │       │
│  │ URL:                │    │    pull request)     │       │
│  │ usuario.github.io   │    │                      │       │
│  └──────────────────────┘    └──────────────────────┘       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 GitHub Pages

### ¿Qué es?
Servicio de **hosting estático** gratuito de GitHub.

### ¿Qué hace?
- Sirve archivos HTML, CSS, JavaScript
- Crea un sitio web accesible públicamente
- URL: `tu-usuario.github.io/nombre-repo`

### ¿Qué NO puede hacer?
- ❌ Ejecutar Python
- ❌ Ejecutar PHP
- ❌ Ejecutar Node.js en el servidor
- ❌ Ejecutar cualquier código del lado del servidor
- ❌ Conectarse a bases de datos directamente

### Ejemplo:
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Mi Sitio</title>
</head>
<body>
    <h1>Hola Mundo</h1>
    <script>
        // JavaScript del cliente (sí funciona)
        console.log('Esto funciona');
    </script>
</body>
</html>
```

**Resultado:** GitHub Pages sirve este archivo y cualquiera puede verlo en `usuario.github.io/repo`

---

## ⚙️ GitHub Actions

### ¿Qué es?
Sistema de **automatización y CI/CD** de GitHub.

### ¿Qué hace?
- Ejecuta scripts en servidores de GitHub
- Puede ejecutar Python, Node.js, Bash, etc.
- Se ejecuta según eventos (push, schedule, manual)
- Puede hacer tareas automatizadas

### ¿Cuándo se ejecuta?
1. **Schedule (cron):** A horas específicas
2. **Push:** Cuando haces `git push`
3. **Pull Request:** Cuando alguien crea un PR
4. **Manual:** Cuando lo ejecutas manualmente desde GitHub
5. **Eventos:** Cualquier evento de GitHub

### Ejemplo - Tu caso:

```yaml
# .github/workflows/keep-supabase-active.yml
name: Keep Supabase Active

on:
  schedule:
    - cron: '0 9 * * *'   # 9:00 UTC todos los días
    - cron: '0 21 * * *'  # 21:00 UTC todos los días
  workflow_dispatch:      # Ejecución manual

jobs:
  query-supabase:
    runs-on: ubuntu-latest
    
    steps:
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install requests
      
      - name: Query Supabase
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
        run: |
          python scripts/keep_supabase_active.py
```

**Resultado:** 
- Se ejecuta automáticamente 2 veces al día
- En un servidor Ubuntu de GitHub
- Ejecuta Python y hace una consulta a Supabase
- **NO tiene nada que ver con GitHub Pages**

---

## 🔄 Flujo Completo en Tu Proyecto

```
┌─────────────────────────────────────────────────────────────┐
│                    TU REPOSITORIO                          │
│              comediacortesana/comedia_cortesana             │
└─────────────────────────────────────────────────────────────┘
                            │
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
        ▼                                       ▼
┌───────────────┐                      ┌───────────────┐
│ GITHUB PAGES  │                      │ GITHUB ACTIONS│
├───────────────┤                      ├───────────────┤
│               │                      │               │
│ Sirve:        │                      │ Ejecuta:      │
│ - index.html  │                      │ - Python      │
│ - CSS/JS      │                      │ - Scripts     │
│               │                      │               │
│ URL pública:  │                      │ Automático:   │
│ usuario.      │                      │ - 9:00 UTC    │
│ github.io/    │                      │ - 21:00 UTC    │
│ repo          │                      │               │
│               │                      │ Consulta:      │
│ ✅ Usuarios   │                      │ Supabase API  │
│    ven el     │                      │               │
│    sitio web  │                      │ ✅ Mantiene   │
│               │                      │    Supabase    │
│               │                      │    activo      │
└───────────────┘                      └───────────────┘
```

---

## 💡 Analogía Simple

### GitHub Pages = Restaurante
- Sirve comida (archivos estáticos)
- Los clientes (usuarios) vienen y consumen
- No cocina en tiempo real (no ejecuta código)

### GitHub Actions = Cocina del Restaurante
- Prepara la comida (ejecuta scripts)
- Trabaja en horarios específicos (schedule)
- Puede preparar cosas automáticamente (automatización)
- No es visible para los clientes (no es público)

---

## ✅ Resumen

| Característica | GitHub Pages | GitHub Actions |
|----------------|--------------|----------------|
| **Propósito** | Hosting web estático | Automatización/CI/CD |
| **Ejecuta código** | ❌ No | ✅ Sí |
| **Python** | ❌ No | ✅ Sí |
| **JavaScript** | ✅ Solo cliente | ✅ Cliente y servidor |
| **Cuándo se ejecuta** | Siempre (servidor web) | Según eventos/schedule |
| **Gratis** | ✅ Sí | ✅ Sí (con límites) |
| **URL pública** | ✅ Sí | ❌ No (solo logs) |

---

## 🎯 En Tu Caso Específico

1. **GitHub Pages:** Sirve tu `index.html` con el filtro de obras
   - Los usuarios visitan: `comediacortesana.github.io/comedia_cortesana`
   - Ven el sitio web estático

2. **GitHub Actions:** Ejecuta el script Python para mantener Supabase activo
   - Se ejecuta automáticamente 2 veces al día
   - Hace consultas a Supabase
   - Los usuarios NO ven esto, solo funciona en segundo plano

**Son servicios complementarios pero independientes.**








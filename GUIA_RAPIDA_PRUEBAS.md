# 🚀 Guía Rápida de Pruebas - Nuevas Funcionalidades

## ✅ Implementaciones Completadas

### 1️⃣ Botón "Ir a Inicio" en el Editor
### 2️⃣ Sistema de Comentarios en Perfiles de Obra

---

## 🧪 Cómo Probar

### Paso 1: Iniciar el Servidor
```bash
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO
python manage.py runserver
```

### Paso 2: Probar Botón "Ir a Inicio" en Editor

1. **Ir al editor**: http://127.0.0.1:8000/obras/editor/
2. **Seleccionar catálogo**: Haz clic en FUENTESXI o CATCOM
3. **Verificar botón**: En el sidebar izquierdo, deberías ver:
   ```
   🏠 Ir a Inicio
   ← Volver a Catálogos
   ```
4. **Probar navegación**: Haz clic en "Ir a Inicio" → deberías volver a la página principal

---

### Paso 3: Probar Comentarios en Perfil de Obra

#### 3.1. Iniciar Sesión
```
URL: http://127.0.0.1:8000/usuarios/login/
Usuario: test1
Contraseña: 123
```

O cualquiera de estos usuarios:
- `investigador / abc`
- `demo / demo`
- `ivansimo / 12345678`

#### 3.2. Ir a una Obra Específica
```
http://127.0.0.1:8000/obras/3058/
```

O cualquier otra obra del catálogo.

#### 3.3. Desplazarse a la Sección de Comentarios
- Verás una sección llamada **"💬 Comentarios"**
- Debajo verás **"✍️ Agregar Comentario"**

#### 3.4. Crear un Comentario
```
Título: Análisis del simbolismo de la obra
Comentario: Esta obra presenta elementos característicos 
del teatro del Siglo de Oro, con referencias claras 
a la mitología clásica...

☑️ Marcar "Hacer público" si quieres que aparezca en el inicio
```

#### 3.5. Publicar
- Haz clic en **"💾 Publicar Comentario"**
- Deberías ver un mensaje verde: **"✅ Comentario publicado exitosamente"**
- El comentario aparecerá inmediatamente debajo del formulario

#### 3.6. Verificar en la Página de Inicio
1. Ir a: http://127.0.0.1:8000/
2. Desplazarse hasta **"💬 Comentarios Recientes de la Comunidad"**
3. Tu comentario debería aparecer allí (si lo marcaste como público)
4. El nombre de la obra será un **enlace clickeable** que te lleva de vuelta al perfil

---

### Paso 4: Probar Comentarios Privados

1. Crear otro comentario en la misma obra
2. **NO marcar** el checkbox "Hacer público"
3. Publicar
4. Verificar que aparece en el perfil de la obra
5. Ir al inicio → **NO debería aparecer** allí
6. Iniciar sesión con otro usuario → **NO debería ver** el comentario privado

---

### Paso 5: Probar Eliminación de Comentarios

1. En el perfil de una obra donde tengas comentarios
2. Verás un botón **"🗑️ Eliminar"** junto a tus comentarios
3. Hacer clic en eliminar
4. Confirmar en el diálogo
5. El comentario desaparece inmediatamente

**Nota**: Solo puedes eliminar TUS propios comentarios.

---

## 📊 Verificación de Funcionalidades

### ✅ Checklist de Pruebas

- [ ] El botón "Ir a Inicio" aparece en el editor de catálogos
- [ ] El botón "Ir a Inicio" funciona correctamente
- [ ] El formulario de comentarios aparece en perfiles de obra
- [ ] Se pueden crear comentarios públicos
- [ ] Los comentarios públicos aparecen en el inicio
- [ ] Los comentarios aparecen en el perfil de la obra
- [ ] Se pueden crear comentarios privados
- [ ] Los comentarios privados NO aparecen en el inicio
- [ ] Solo el autor puede ver sus comentarios privados
- [ ] Los comentarios de otros usuarios aparecen (si son públicos)
- [ ] Se pueden eliminar comentarios propios
- [ ] NO se pueden eliminar comentarios de otros
- [ ] Los mensajes de feedback funcionan correctamente
- [ ] Los enlaces a obras desde comentarios funcionan

---

## 🎨 Elementos Visuales a Verificar

### En el Editor
```
Sidebar:
├── 🏠 Ir a Inicio          [NUEVO]
└── ← Volver a Catálogos
```

### En Perfil de Obra
```
💬 Comentarios
├── ✍️ Agregar Comentario
│   ├── Título del comentario: [input]
│   ├── Comentario: [textarea]
│   ├── ☑️ Hacer público
│   ├── [💾 Publicar Comentario]
│   └── [🔄 Limpiar]
│
└── Lista de Comentarios
    ├── Comentario 1
    │   ├── Título
    │   ├── 👤 Usuario | 📅 Fecha
    │   ├── [Público] o [Privado]
    │   ├── Contenido
    │   └── [🗑️ Eliminar] (si es tuyo)
    │
    └── Comentario 2...
```

### En Página de Inicio
```
💬 Comentarios Recientes de la Comunidad
├── Comentario 1
│   ├── 👤 Usuario | 📅 Fecha
│   ├── Título
│   ├── Contenido (primeros 200 caracteres)
│   ├── 📚 Obras: [Obra 1] [Obra 2]  (enlaces clickeables)
│   └── 🗂️ FUENTESXI o CATCOM
│
└── Comentario 2...
```

---

## 🐛 Problemas Comunes y Soluciones

### Problema: "Usuario no autenticado"
**Solución**: Debes iniciar sesión primero en `/usuarios/login/`

### Problema: No veo el formulario de comentarios
**Solución**: 
1. Asegúrate de estar en el perfil de una obra (`/obras/<id>/`)
2. Verifica que estés autenticado
3. Desplázate hacia abajo en la página

### Problema: Mi comentario no aparece en el inicio
**Posibles causas**:
1. No marcaste "Hacer público" al crearlo
2. Necesitas refrescar la página de inicio
3. Hay más de 5 comentarios públicos más recientes

### Problema: No puedo eliminar un comentario
**Posibles causas**:
1. No eres el autor del comentario
2. El comentario fue eliminado por otro usuario (si era tuyo)
3. Perdiste la sesión - intenta recargar la página

---

## 📱 Responsive Testing

Prueba también en diferentes tamaños de pantalla:
- **Desktop**: 1920x1080
- **Tablet**: 768x1024
- **Mobile**: 375x667

El diseño debería adaptarse correctamente en todos los dispositivos.

---

## 🔍 URLs de Referencia Rápida

| Función | URL |
|---------|-----|
| Página de Inicio | http://127.0.0.1:8000/ |
| Editor Principal | http://127.0.0.1:8000/obras/editor/ |
| Editor FUENTESXI | http://127.0.0.1:8000/obras/editor/fuentesxi/ |
| Editor CATCOM | http://127.0.0.1:8000/obras/editor/catcom/ |
| Obra Ejemplo 1 | http://127.0.0.1:8000/obras/3058/ |
| Obra Ejemplo 2 | http://127.0.0.1:8000/obras/1/ |
| Catálogo General | http://127.0.0.1:8000/obras/catalogo/ |
| Login | http://127.0.0.1:8000/usuarios/login/ |
| Admin | http://127.0.0.1:8000/admin/ |

---

## ✨ Características Destacadas

### 🎯 Comentarios Inteligentes
- Asociación automática de obra
- Detección automática de catálogo (FUENTESXI/CATCOM)
- Timestamps automáticos

### 🔒 Seguridad
- Solo usuarios autenticados pueden comentar
- Solo el autor puede eliminar sus comentarios
- Validación de datos en servidor
- Protección CSRF

### ⚡ Experiencia de Usuario
- Actualización sin recargar página (AJAX)
- Feedback visual inmediato
- Mensajes de éxito/error claros
- Confirmación antes de acciones destructivas

### 🎨 Diseño
- Colores consistentes con el tema del sitio
- Iconos descriptivos
- Badges de estado
- Hover effects
- Responsive design

---

**¡Disfruta probando las nuevas funcionalidades!** 🎉

Si encuentras algún problema, revisa la consola del navegador (F12) o los logs del servidor.


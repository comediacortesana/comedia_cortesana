# 📚 Flujo del Sistema DELIA - Explicación Simple

## 🎯 ¿Qué es este sistema?

Un catálogo digital de obras de teatro del Siglo de Oro español donde diferentes usuarios pueden ver, editar y comentar información sobre las obras.

---

## 🗄️ ¿Dónde están los datos?

### **Supabase = Base de datos principal** 🏛️
- **Todas las obras** están guardadas aquí
- Es como un "almacén digital" en la nube
- Cuando alguien hace un cambio, se guarda aquí inmediatamente

### **JSON local = Respaldo** 💾
- Es una copia de seguridad en tu computadora
- Si Supabase falla, puedes usar este archivo
- Se puede actualizar manualmente cuando quieras

---

## 👥 ¿Quiénes pueden hacer qué?

### **Usuario Normal (lector)**
- ✅ Ver las obras
- ✅ Buscar y filtrar
- ✅ Ver detalles completos
- ❌ No puede editar

### **Editor**
- ✅ Todo lo de usuario normal +
- ✅ **Editar campos** de las obras
- ✅ **Comentar** sobre cambios
- ❌ Sus cambios necesitan aprobación

### **Admin**
- ✅ Todo lo de editor +
- ✅ **Aprobar o rechazar** cambios de editores
- ✅ Sus cambios se aplican **inmediatamente**
- ✅ Puede editar directamente sin aprobación

---

## 🔄 Flujo de Edición (Paso a Paso)

### **1. Editor quiere cambiar algo**
```
Editor → Hace clic en "Editar" → Escribe nuevo valor → Confirma
```

### **2. ¿Qué pasa con ese cambio?**
```
Cambio → Se guarda en Supabase (tabla "cambios_pendientes")
       → Aparece en la lista de "Cambios Pendientes" del Admin
       → El editor ve su cambio aplicado temporalmente
```

### **3. Admin revisa**
```
Admin → Ve lista de cambios pendientes
      → Lee el cambio y los comentarios
      → Decide: ✅ Aprobar o ❌ Rechazar
```

### **4. Si Admin aprueba**
```
Aprobación → Cambio se aplica a la tabla "obras" en Supabase
            → Todos los usuarios ven el cambio actualizado
            → El cambio queda guardado permanentemente
```

### **5. Si Admin rechaza**
```
Rechazo → El cambio se elimina de "cambios_pendientes"
         → La obra vuelve a su valor original
         → El editor puede intentar de nuevo
```

---

## 📊 Flujo de Datos (Técnico Simple)

```
┌─────────────────┐
│  Usuario abre   │
│   la página     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  ¿Hay datos en  │ ────▶│   Supabase   │ ← Base de datos principal
│   Supabase?     │      │   (Nube)     │
└────────┬────────┘      └──────────────┘
         │ Sí ✅
         ▼
┌─────────────────┐
│ Carga desde     │
│ Supabase        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Muestra obras   │
│ en pantalla     │
└─────────────────┘

Si Supabase falla:
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│ Carga desde     │ ────▶│  JSON local  │ ← Respaldo
│ JSON (respaldo) │      │  (Archivo)    │
└─────────────────┘      └──────────────┘
```

---

## 🔐 Seguridad y Permisos

### **¿Cómo sabe el sistema quién es quién?**
- Cada usuario tiene un **perfil** en Supabase
- El perfil tiene un **rol**: `lector`, `editor`, o `admin`
- El sistema verifica el rol antes de permitir acciones

### **¿Dónde se guardan los permisos?**
```
Supabase → Tabla "perfiles_usuarios"
         → Campos: usuario_id, rol
```

---

## 📝 Ejemplo Real Completo

### **Escenario: Editor quiere corregir el título de una obra**

1. **Editor hace login** → Sistema verifica: "Es editor ✅"

2. **Editor busca la obra** → Encuentra "A Dios por razon de estado"

3. **Editor hace clic en la fila** → Se abre modal con detalles

4. **Editor hace clic en "Editar" junto al título** → Aparece campo de texto

5. **Editor escribe**: "A Dios por razón de estado" (corrige "razon" → "razón")

6. **Editor confirma** → 
   - Cambio se guarda en `cambios_pendientes` (Supabase)
   - Aparece notificación: "Cambio pendiente de aprobación"
   - El editor ve su cambio aplicado (solo en su pantalla)

7. **Admin hace login** → Ve notificación: "3 cambios pendientes"

8. **Admin revisa cambios** → Ve el cambio del título con comentario del editor

9. **Admin aprueba** → 
   - Cambio se aplica a la tabla `obras` (Supabase)
   - Todos los usuarios ahora ven "A Dios por razón de estado"
   - El cambio queda guardado permanentemente

10. **Si alguien recarga la página** → Ve el título corregido ✅

---

## 🛠️ Herramientas Adicionales

### **Scripts de Python** (para administradores técnicos)
- `sync_to_supabase.py` → Sincroniza JSON → Supabase
- `backup_from_supabase.py` → Hace backup Supabase → JSON
- `sync_to_sheets.py` → Sincroniza con Google Sheets

---

## 🎯 Resumen Ultra-Rápido

```
1. Datos principales → Supabase (nube)
2. Respaldo → JSON local
3. Usuarios → Ver, Editar, o Administrar según su rol
4. Cambios de editores → Necesitan aprobación
5. Cambios de admin → Se aplican inmediatamente
6. Todo se guarda en Supabase → Persiste para siempre
```

---

## ❓ Preguntas Frecuentes

**P: ¿Qué pasa si Supabase se cae?**
R: El sistema automáticamente carga desde el JSON local (respaldo)

**P: ¿Los cambios se pierden si recargo la página?**
R: No, si están aprobados están guardados en Supabase permanentemente

**P: ¿Puedo editar sin ser admin?**
R: Sí, como editor puedes editar, pero tus cambios necesitan aprobación

**P: ¿Dónde se guardan los comentarios?**
R: En Supabase, en la tabla `comentarios`, vinculados a cada obra

**P: ¿Cómo hago backup?**
R: Ejecuta: `python scripts/backup_from_supabase.py`

---

## 📍 Archivos Importantes

- `index.html` → Interfaz web (lo que ven los usuarios)
- `datos_obras.json` → Respaldo local de obras
- `scripts/` → Herramientas de sincronización y backup
- Supabase Dashboard → Base de datos y configuración

---

**Última actualización:** Enero 2025


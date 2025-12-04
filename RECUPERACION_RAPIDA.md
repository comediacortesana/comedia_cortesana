# 🚑 Recuperación Rápida de Supabase

## ⚡ 3 Pasos para Recuperar Todo

### 1️⃣ Recrear Schema (5 min)

```bash
# En Supabase Dashboard > SQL Editor
# Ejecutar el contenido de:
RECUPERACION_SUPABASE_COMPLETA.sql
```

### 2️⃣ Restaurar Datos (5 min)

```bash
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/comedia_cortesana

python scripts/sync_to_supabase.py \
  --file datos_obras_backup_20251114_132718.json
```

### 3️⃣ Verificar (2 min)

```bash
python scripts/verificar_recuperacion.py
```

---

## 📊 ¿Qué se Recupera?

| Elemento | Estado | Cantidad |
|----------|--------|----------|
| 📚 Obras | ✅ Recuperable | ~1,755 obras |
| 🏛️ Schema (tablas, RLS) | ✅ Recuperable | Completo |
| 👤 Usuarios auth | ⚠️ Depende* | - |
| 💬 Comentarios | ❌ Perdidos | - |
| 📝 Validaciones | ❌ Perdidas | - |

\* Los usuarios de `auth.users` pueden o no haberse borrado, depende de cómo se borró Supabase

---

## 🔑 Crear Usuario Admin

Después de recuperar, crea un admin:

```sql
-- En Supabase SQL Editor
-- Reemplaza el UUID con el de tu usuario
UPDATE perfiles_usuarios 
SET rol = 'admin' 
WHERE id = 'tu-uuid-aqui';
```

---

## 📚 Documentación Completa

- **Guía detallada**: `GUIA_RECUPERACION_COMPLETA.md`
- **Script SQL**: `RECUPERACION_SUPABASE_COMPLETA.sql`
- **Script verificación**: `scripts/verificar_recuperacion.py`

---

## 🆘 Problemas Comunes

**Error: "permission denied"**
→ Usa el `service_role` key en lugar del `anon` key

**Error: "Invalid API key"**
→ Verifica tu `.env` tiene las credenciales correctas

**Obras no se sincronizan**
→ Verifica que ejecutaste el SQL primero (paso 1)

---

## ✅ Checklist Rápido

- [ ] SQL ejecutado en Supabase
- [ ] 6 tablas creadas (obras, comentarios, etc.)
- [ ] Datos sincronizados (~1755 obras)
- [ ] Verificación exitosa
- [ ] Usuario admin creado
- [ ] App web funciona

---

**¿Listo?** → Sigue la guía completa en `GUIA_RECUPERACION_COMPLETA.md`


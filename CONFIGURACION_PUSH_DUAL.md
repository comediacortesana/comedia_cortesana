# 🔄 Configuración de Push Dual Automático

## ✅ Configuración Completada

El repositorio está configurado para hacer push automáticamente a **ambos repositorios** cuando haces push desde GitHub Desktop:

1. `iccmu/DELIA_DJANGO` (tu repositorio personal)
2. `comediacortesana/comedia_cortesana` (repositorio público)

## 📋 Cómo Funciona

Cuando haces push desde GitHub Desktop a `origin`, Git automáticamente hace push a ambos repositorios porque `origin` tiene múltiples URLs de push configuradas.

## 🧪 Probar que Funciona

1. **Haz un cambio pequeño** en cualquier archivo
2. **Haz commit** desde GitHub Desktop
3. **Haz push** a `origin`
4. **Verifica** que el cambio aparece en ambos repositorios:
   - https://github.com/iccmu/DELIA_DJANGO
   - https://github.com/comediacortesana/comedia_cortesana

## ⚠️ Nota Importante

- **GitHub Desktop** debería respetar esta configuración automáticamente
- Si GitHub Desktop no hace push a ambos, puedes hacerlo manualmente desde terminal:
  ```bash
  git push origin main
  ```
  Esto hará push a ambos repositorios automáticamente.

## 🔍 Ver Configuración Actual

Para ver la configuración actual de los remotes:

```bash
git remote -v
```

Deberías ver que `origin` tiene dos URLs de push.

## 🛠️ Si Necesitas Cambiar la Configuración

Para eliminar el push dual y volver a solo `iccmu/DELIA_DJANGO`:

```bash
git remote set-url origin https://github.com/iccmu/DELIA_DJANGO.git
```

Para volver a configurar el push dual:

```bash
git remote set-url --add --push origin https://github.com/iccmu/DELIA_DJANGO.git
git remote set-url --add --push origin https://github.com/comediacortesana/comedia_cortesana.git
```

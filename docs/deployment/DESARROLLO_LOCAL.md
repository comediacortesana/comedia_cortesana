# 🚀 Desarrollo Local Rápido

Para evitar tener que hacer push a GitHub cada vez que quieres probar cambios, puedes usar un servidor local.

## Opción 1: Script de Python (Recomendado)

```bash
# Iniciar servidor local
python3 scripts/servidor_local.py

# O usar el script bash
./scripts/iniciar_desarrollo.sh
```

Luego abre en tu navegador: `http://localhost:8000/`

## Opción 2: Python Simple HTTP Server

```bash
cd /ruta/al/proyecto
python3 -m http.server 8000
```

Luego abre: `http://localhost:8000/`

## Opción 3: Servidor HTTP de Node.js (si tienes Node instalado)

```bash
npx http-server -p 8000
```

## Ventajas del Desarrollo Local

✅ **Cambios instantáneos**: No necesitas hacer push y esperar GitHub Actions
✅ **Sin límites**: Puedes probar tantas veces como quieras
✅ **Debugging más fácil**: Puedes usar herramientas de desarrollo del navegador
✅ **Sin afectar producción**: Los cambios solo se ven en tu máquina

## Nota Importante

⚠️ **Django**: Para desarrollo local con el backend Django completo, usa `python manage.py runserver` que levanta el servidor de desarrollo en `http://127.0.0.1:8000/`.

## Detener el Servidor

Presiona `Ctrl+C` en la terminal donde está corriendo el servidor.


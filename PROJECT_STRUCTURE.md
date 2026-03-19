# Estructura recomendada del proyecto

Reorganizacion aplicada con enfoque seguro:

- `teatro_espanol/`: configuracion principal Django (`settings.py`, `urls.py`, `wsgi.py`).
- `apps/`: aplicaciones Django del dominio (`obras`, `representaciones`, `lugares`, `autores`, `usuarios`, `bibliografia`).
- `templates/`: plantillas Django.
- `static/`: estaticos para Django.
- `scripts/`: utilidades de importacion/exportacion/migracion.
- `sql/supabase/`: scripts SQL historicos y operativos de Supabase.
- `docs/deployment/`: guias de despliegue y entorno local.
- `docs/supabase/`: documentacion funcional/operativa de Supabase.
- `frontend/github-pages/`: copia organizada de la version estatica (GitHub Pages).

## Notas de compatibilidad

- Se mantiene `index.html` y demas archivos estaticos en raiz para no romper URLs o flujos actuales.
- Se copia la web estatica a `frontend/github-pages/` para trabajar ordenadamente a futuro.
- No se han movido `apps/`, `templates/` ni `manage.py` para evitar romper imports y rutas Django.

## Siguiente paso recomendado

Cuando confirmes que no dependes de los archivos estaticos en raiz, se puede hacer una segunda pasada:

1. Dejar `frontend/github-pages/` como unica fuente.
2. Actualizar rutas de publicacion GitHub Pages.
3. Eliminar duplicados en raiz.

# Migracion completa: GitHub Pages -> Django + PostgreSQL + Azure App Service

Este documento deja el flujo completo para migrar la demo HTML a un entorno Django con PostgreSQL, manteniendo estructura SQL y datos.

## 1) Preparar entorno local con conda

```bash
conda create -n comedias python=3.11 -y
conda activate comedias
pip install -r requirements.txt
```

Configurar entorno:

```bash
cp .env.example .env
```

Editar `.env` con tus valores locales.

## 2) Levantar PostgreSQL local y conectar Django

Ejemplo rapido:

```sql
CREATE DATABASE comedias_db;
CREATE USER comedias_user WITH PASSWORD 'cambia_esto';
GRANT ALL PRIVILEGES ON DATABASE comedias_db TO comedias_user;
```

En `.env`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=comedias_db
DB_USER=comedias_user
DB_PASSWORD=cambia_esto
DB_HOST=127.0.0.1
DB_PORT=5432
DB_SSLMODE=prefer
```

Aplicar migraciones:

```bash
python manage.py migrate
python manage.py createsuperuser
```

## 3) Migrar estructura + datos desde Supabase

Requisitos:
- `pg_dump`, `pg_restore`, `psql` instalados.
- URL PostgreSQL de Supabase (origen).
- URL PostgreSQL de PostgreSQL local o Azure (destino).

Ejecutar:

```bash
SOURCE_DB_URL="postgresql://usuario:pass@host:5432/postgres?sslmode=require" \
TARGET_DB_URL="postgresql://usuario:pass@host:5432/comedias_db?sslmode=prefer" \
./scripts/migrate_supabase_to_postgres.sh
```

Notas:
- El script exporta y restaura en formato custom de PostgreSQL.
- Luego ejecuta `python manage.py migrate` para consolidar esquema bajo migraciones Django.
- Si quieres mover solo tablas concretas:

```bash
TABLES="autores lugares obras representaciones" \
SOURCE_DB_URL="postgresql://..." \
TARGET_DB_URL="postgresql://..." \
./scripts/migrate_supabase_to_postgres.sh
```

## 4) Verificar Django Admin

```bash
python manage.py runserver
```

Verificar en `http://127.0.0.1:8000/admin/`:
- Login correcto.
- CRUD en `Obra`, `Representacion`, `Lugar`, `Autor`.
- Relacion FK consistente (obras con autor, representaciones con obra/lugar).

## 5) Preparar Azure App Service (Python)

El proyecto ya incluye `Procfile`:

```text
web: gunicorn teatro_espanol.wsgi --bind=0.0.0.0:$PORT --workers=3 --timeout=120
```

Variables de entorno minimas en App Service:
- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS=<tu-app>.azurewebsites.net`
- `CSRF_TRUSTED_ORIGINS=https://<tu-app>.azurewebsites.net`
- `DB_ENGINE=django.db.backends.postgresql`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT=5432`
- `DB_SSLMODE=require`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- `SECURE_SSL_REDIRECT=True`

## 6) Despliegue manual con GitHub Desktop

1. Confirmar cambios locales y test rapido:
   - `python manage.py check`
   - `python manage.py migrate --plan`
2. Commit desde GitHub Desktop.
3. Push a GitHub.
4. En Azure App Service, desplegar desde tu repo/branch.
5. Tras desplegar, ejecutar migraciones en el entorno Azure.

Si usas consola de App Service:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## 7) Checklist de salida a produccion

- `manage.py check` sin errores criticos.
- Migraciones aplicadas.
- Admin operativo con superusuario.
- Consultas principales responden.
- Variables seguras activadas (`DEBUG=False`, cookies seguras, SSL redirect).

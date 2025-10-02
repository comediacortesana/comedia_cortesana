# Guía de Contribución - DELIA

## Cómo Contribuir

### 1. Configuración del Entorno de Desarrollo

```bash
# Clonar el repositorio
git clone <repository-url>
cd DELIA_DJANGO

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env.example .env
# Editar .env con tus configuraciones

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 2. Estructura del Proyecto

- `apps/` - Aplicaciones Django
- `teatro_espanol/` - Configuración del proyecto
- `scripts/` - Scripts de importación y utilidades
- `templates/` - Plantillas HTML
- `static/` - Archivos estáticos
- `media/` - Archivos multimedia
- `docs/` - Documentación

### 3. Convenciones de Código

- **Python**: Seguir PEP 8
- **Django**: Seguir las convenciones de Django
- **Commits**: Usar mensajes descriptivos en español
- **Branches**: Usar nombres descriptivos (ej: `feature/nueva-funcionalidad`)

### 4. Proceso de Contribución

1. **Fork** el repositorio
2. **Crear** una rama para tu funcionalidad
3. **Hacer** los cambios necesarios
4. **Probar** que todo funciona correctamente
5. **Commit** con mensaje descriptivo
6. **Push** a tu fork
7. **Crear** un Pull Request

### 5. Testing

```bash
# Ejecutar tests
python manage.py test

# Verificar que el servidor funciona
python manage.py runserver
```

### 6. Importación de Datos

Si necesitas datos de prueba:

```bash
# Importar datos de FUENTESXI
python scripts/import_fuentesxi.py

# Importar datos de CATCOM
python scripts/import_catcom.py

# Fusionar datos
python scripts/merge_data.py
```

### 7. Documentación

- Actualizar el README.md si es necesario
- Documentar nuevas funcionalidades
- Mantener la documentación de la API actualizada

## Contacto

Para preguntas sobre el desarrollo, contactar al equipo del **ITEM (Instituto del Teatro y Música)**.

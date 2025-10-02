# DELIA - Teatro Español del Siglo de Oro

## Descripción

**DELIA** es una plataforma web Django que integra y organiza datos sobre teatro español del Siglo de Oro provenientes de dos fuentes principales:

1. **FUENTESXI**: Datos extraídos del PDF "Comedias en Madrid: 1603-1709" de J.E. Varey y N.D. Shergold
2. **CATCOM**: Datos obtenidos mediante web scraping de la base de datos CATCOM (catcom.uv.es)

El proyecto forma parte del **ITEM (Instituto del Teatro y Música)** y proporciona una interfaz web para investigadores y académicos del teatro español del Siglo de Oro.

## Estructura del Proyecto

```
teatro_espanol_django/
├── manage.py
├── requirements.txt
├── README.md
├── teatro_espanol/          # Configuración del proyecto Django
├── apps/                    # Aplicaciones Django
│   ├── obras/              # Obras teatrales
│   ├── representaciones/   # Representaciones teatrales
│   ├── lugares/            # Lugares geográficos
│   ├── autores/            # Autores/dramaturgos
│   └── bibliografia/       # Referencias bibliográficas
├── data/                   # Datos organizados
│   ├── fuentesxi/         # Datos de FUENTESXI
│   ├── catcom/            # Datos de CATCOM
│   └── raw/               # Datos originales
├── scripts/               # Scripts de importación
├── static/                # Archivos estáticos
├── templates/             # Plantillas HTML
└── media/                 # Archivos multimedia
```

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <repository-url>
   cd DELIA_DJANGO
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   ```bash
   cp env.example .env
   # Editar .env con tus configuraciones
   ```

5. **Configurar base de datos**:
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Importar datos (opcional)**:
   ```bash
   python scripts/import_fuentesxi.py
   python scripts/import_catcom.py
   python scripts/merge_data.py
   ```

## Importación de Datos

### Importar datos de FUENTESXI
```bash
python scripts/import_fuentesxi.py
```

### Importar datos de CATCOM
```bash
python scripts/import_catcom.py
```

### Fusionar y deduplicar datos
```bash
python scripts/merge_data.py
```

## Uso

### Servidor de desarrollo
```bash
python manage.py runserver
```

### Panel de administración
Acceder a: http://localhost:8000/admin/

### API REST
- **Obras**: http://localhost:8000/api/obras/
- **Representaciones**: http://localhost:8000/api/representaciones/
- **Lugares**: http://localhost:8000/api/lugares/
- **Autores**: http://localhost:8000/api/autores/
- **Referencias bibliográficas**: http://localhost:8000/api/referencias/

## Modelos de Datos

### Obra
- Información principal de obras teatrales
- Campos: título, autor, tipo, género, fuente, etc.

### Representacion
- Datos de representaciones teatrales
- Campos: fecha, lugar, compañía, observaciones, etc.

### Lugar
- Lugares geográficos de representación
- Campos: nombre, coordenadas, tipo, descripción, etc.

### Autor
- Autores y dramaturgos
- Campos: nombre, biografía, época, obras principales, etc.

### ReferenciaBibliografica
- Referencias bibliográficas
- Campos: título, autor, editorial, año, tipo, etc.

## Características

- **API REST completa** con Django REST Framework
- **Panel de administración** personalizado
- **Filtros avanzados** y búsqueda
- **Importación automática** de datos
- **Fusión y deduplicación** de fuentes
- **Validación de datos** y consistencia
- **Documentación automática** de la API

## Tecnologías Utilizadas

- **Backend**: Django 4.2+, Django REST Framework
- **Base de datos**: SQLite (desarrollo), PostgreSQL (producción)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **APIs**: Django REST Framework
- **Herramientas**: Celery, Redis, Pandas, NumPy

## Contribución

1. Fork el proyecto
2. Crear una rama para la nueva funcionalidad
3. Commit los cambios
4. Push a la rama
5. Crear un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## Contacto

Para preguntas o sugerencias sobre el proyecto DELIA, contactar al **ITEM (Instituto del Teatro y Música)**.

## Agradecimientos

- **FUENTESXI**: J.E. Varey y N.D. Shergold por "Comedias en Madrid: 1603-1709"
- **CATCOM**: DICAT Grupo de investigación teatral por la base de datos web
- **ITEM**: Instituto del Teatro y Música por el apoyo al proyecto
- **Comunidad Django** por el framework y la documentación

## Licencia

Este proyecto está desarrollado para el **ITEM (Instituto del Teatro y Música)** y está destinado a uso académico e investigativo.

"""
Definición del schema de campos para DELIA
Este archivo centraliza la definición de todos los campos del sistema
"""

from typing import Dict, Any, Optional, Tuple
from enum import Enum


class FieldType(str, Enum):
    """Tipos de campos disponibles"""
    TEXT = "text"
    INTEGER = "integer"
    DATE = "date"
    BOOLEAN = "boolean"
    JSON = "json"
    FLOAT = "float"


class FieldDefinition:
    """Definición de un campo"""
    
    def __init__(
        self,
        name: str,
        field_type: FieldType,
        required: bool = False,
        description: str = "",
        editable: bool = True,
        default: Any = None,
        validation: Optional[callable] = None
    ):
        self.name = name
        self.type = field_type
        self.required = required
        self.description = description
        self.editable = editable
        self.default = default
        self.validation = validation


# Campos de Obra
OBRA_FIELDS: Dict[str, FieldDefinition] = {
    # Información Básica
    'id': FieldDefinition(
        'id', FieldType.INTEGER, required=True, editable=False,
        description='ID único de la obra'
    ),
    'titulo': FieldDefinition(
        'titulo', FieldType.TEXT, required=True,
        description='Título principal de la obra'
    ),
    'titulo_original': FieldDefinition(
        'titulo_original', FieldType.TEXT,
        description='Título original de la obra'
    ),
    'titulo_alternativo': FieldDefinition(
        'titulo_alternativo', FieldType.TEXT,
        description='Títulos alternativos de la obra'
    ),
    'tipo_obra': FieldDefinition(
        'tipo_obra', FieldType.TEXT,
        description='Tipo de obra (comedia, auto, etc.)'
    ),
    'genero': FieldDefinition(
        'genero', FieldType.TEXT,
        description='Género de la obra'
    ),
    'subgenero': FieldDefinition(
        'subgenero', FieldType.TEXT,
        description='Subgénero de la obra'
    ),
    'tema': FieldDefinition(
        'tema', FieldType.TEXT,
        description='Tema principal de la obra'
    ),
    'idioma': FieldDefinition(
        'idioma', FieldType.TEXT,
        description='Idioma de la obra'
    ),
    'fecha_creacion': FieldDefinition(
        'fecha_creacion', FieldType.DATE,
        description='Fecha de creación de la obra'
    ),
    
    # Estructura
    'actos': FieldDefinition(
        'actos', FieldType.INTEGER,
        description='Número de actos'
    ),
    'versos': FieldDefinition(
        'versos', FieldType.INTEGER,
        description='Número de versos'
    ),
    
    # Música
    'musica_conservada': FieldDefinition(
        'musica_conservada', FieldType.BOOLEAN,
        description='Si la música está conservada'
    ),
    'compositor': FieldDefinition(
        'compositor', FieldType.TEXT,
        description='Nombre del compositor'
    ),
    'bibliotecas_musica': FieldDefinition(
        'bibliotecas_musica', FieldType.TEXT,
        description='Bibliotecas que conservan la música'
    ),
    'bibliografia_musica': FieldDefinition(
        'bibliografia_musica', FieldType.TEXT,
        description='Bibliografía sobre la música'
    ),
    
    # Mecenazgo
    'mecenas': FieldDefinition(
        'mecenas', FieldType.TEXT,
        description='Mecenas de la obra'
    ),
    
    # Bibliografía
    'edicion_principe': FieldDefinition(
        'edicion_principe', FieldType.TEXT,
        description='Edición príncipe'
    ),
    'notas_bibliograficas': FieldDefinition(
        'notas_bibliograficas', FieldType.TEXT,
        description='Notas bibliográficas'
    ),
    'manuscritos_conocidos': FieldDefinition(
        'manuscritos_conocidos', FieldType.TEXT,
        description='Manuscritos conocidos'
    ),
    'ediciones_conocidas': FieldDefinition(
        'ediciones_conocidas', FieldType.TEXT,
        description='Ediciones conocidas'
    ),
    
    # Fuente y Origen
    'fuente': FieldDefinition(
        'fuente', FieldType.TEXT,
        description='Fuente principal de datos'
    ),
    'origen_datos': FieldDefinition(
        'origen_datos', FieldType.TEXT,
        description='Origen de los datos'
    ),
    'pagina_pdf': FieldDefinition(
        'pagina_pdf', FieldType.TEXT,
        description='Página del PDF fuente'
    ),
    'texto_original_pdf': FieldDefinition(
        'texto_original_pdf', FieldType.TEXT,
        description='Texto original extraído del PDF'
    ),
    
    # Notas
    'notas': FieldDefinition(
        'notas', FieldType.TEXT,
        description='Notas generales'
    ),
    'observaciones': FieldDefinition(
        'observaciones', FieldType.TEXT,
        description='Observaciones adicionales'
    ),
    
    # Autor (campos anidados - se manejan como JSON)
    'autor': FieldDefinition(
        'autor', FieldType.JSON,
        description='Información del autor (objeto anidado)'
    ),
}


# Campos de Autor (dentro del objeto autor)
AUTOR_FIELDS: Dict[str, FieldDefinition] = {
    'nombre': FieldDefinition(
        'nombre', FieldType.TEXT,
        description='Nombre del autor'
    ),
    'nombre_completo': FieldDefinition(
        'nombre_completo', FieldType.TEXT,
        description='Nombre completo del autor'
    ),
    'fecha_nacimiento': FieldDefinition(
        'fecha_nacimiento', FieldType.DATE,
        description='Fecha de nacimiento'
    ),
    'fecha_muerte': FieldDefinition(
        'fecha_muerte', FieldType.DATE,
        description='Fecha de muerte'
    ),
    'epoca': FieldDefinition(
        'epoca', FieldType.TEXT,
        description='Época del autor'
    ),
    'biografia': FieldDefinition(
        'biografia', FieldType.TEXT,
        description='Biografía del autor'
    ),
}


def get_field_definition(field_name: str) -> Optional[FieldDefinition]:
    """Obtiene la definición de un campo"""
    # Manejar campos anidados (ej: "autor.nombre_completo")
    if '.' in field_name:
        partes = field_name.split('.')
        if partes[0] == 'autor' and len(partes) == 2:
            return AUTOR_FIELDS.get(partes[1])
        return None
    
    return OBRA_FIELDS.get(field_name)


def get_all_fields() -> Dict[str, FieldDefinition]:
    """Obtiene todos los campos definidos"""
    return {**OBRA_FIELDS, **{f'autor.{k}': v for k, v in AUTOR_FIELDS.items()}}


def validate_field_value(field_name: str, value: Any) -> Tuple[bool, Optional[str]]:
    """
    Valida un valor según la definición del campo
    Retorna: (es_valido, mensaje_error)
    """
    field_def = get_field_definition(field_name)
    
    if not field_def:
        return False, f"Campo '{field_name}' no está definido"
    
    # Validar requerido
    if field_def.required and (value is None or value == ''):
        return False, f"Campo '{field_name}' es requerido"
    
    # Validar tipo
    if value is not None and value != '':
        type_valid = _validate_type(value, field_def.type)
        if not type_valid:
            return False, f"Campo '{field_name}' debe ser de tipo {field_def.type.value}"
    
    # Validación personalizada
    if field_def.validation:
        try:
            field_def.validation(value)
        except Exception as e:
            return False, str(e)
    
    return True, None


def _validate_type(value: Any, field_type: FieldType) -> bool:
    """Valida que el valor coincida con el tipo esperado"""
    if field_type == FieldType.TEXT:
        return isinstance(value, str)
    elif field_type == FieldType.INTEGER:
        return isinstance(value, int) or (isinstance(value, str) and value.isdigit())
    elif field_type == FieldType.BOOLEAN:
        return isinstance(value, bool) or value in ['true', 'false', 'True', 'False', '1', '0']
    elif field_type == FieldType.DATE:
        return isinstance(value, str)  # Las fechas vienen como strings
    elif field_type == FieldType.JSON:
        return isinstance(value, (dict, list)) or value is None
    elif field_type == FieldType.FLOAT:
        try:
            float(value)
            return True
        except:
            return False
    
    return True


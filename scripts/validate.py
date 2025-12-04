"""
Validación y transformación de datos antes de sincronizar
"""

from typing import Dict, Any, List, Tuple, Optional
from scripts.schema import get_field_definition, validate_field_value, get_all_fields
import json


class DataValidator:
    """Validador de datos para obras"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_obra(self, obra: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        Valida una obra completa
        Retorna: (es_valida, errores, advertencias)
        """
        self.errors = []
        self.warnings = []
        
        # Validar ID
        if 'id' not in obra or not obra['id']:
            self.errors.append("La obra debe tener un ID")
            return False, self.errors, self.warnings
        
        # Validar campos requeridos (solo los que están en OBRA_FIELDS, no los anidados)
        from scripts.schema import OBRA_FIELDS
        for field_name, field_def in OBRA_FIELDS.items():
            if field_def.required:
                value = obra.get(field_name)
                if value is None or value == '':
                    self.errors.append(f"Campo requerido '{field_name}' está vacío")
        
        # Validar todos los campos presentes (solo los que existen en la obra)
        flattened = self._flatten_dict(obra)
        for field_name, value in flattened.items():
            # Solo validar si el valor no es None o vacío (los campos opcionales pueden estar ausentes)
            if value is not None and value != '':
                is_valid, error_msg = validate_field_value(field_name, value)
                if not is_valid:
                    self.errors.append(f"{field_name}: {error_msg}")
        
        # Validaciones específicas
        self._validate_specific_rules(obra)
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _get_nested_value(self, data: Dict[str, Any], field_name: str) -> Any:
        """Obtiene un valor anidado usando notación con punto"""
        if '.' not in field_name:
            return data.get(field_name)
        
        partes = field_name.split('.')
        value = data
        for parte in partes:
            if isinstance(value, dict):
                value = value.get(parte)
            else:
                return None
        return value
    
    def _flatten_dict(self, data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
        """Aplana un diccionario anidado"""
        result = {}
        for key, value in data.items():
            new_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                result.update(self._flatten_dict(value, new_key))
            else:
                result[new_key] = value
        
        return result
    
    def _validate_specific_rules(self, obra: Dict[str, Any]):
        """Validaciones específicas de reglas de negocio"""
        # Validar que fecha_muerte sea posterior a fecha_nacimiento (si ambas existen)
        autor = obra.get('autor', {})
        if isinstance(autor, dict):
            fecha_nac = autor.get('fecha_nacimiento')
            fecha_muerte = autor.get('fecha_muerte')
            
            if fecha_nac and fecha_muerte:
                try:
                    # Asumir formato YYYY-MM-DD o YYYY
                    nac_year = int(fecha_nac[:4]) if len(fecha_nac) >= 4 else None
                    muerte_year = int(fecha_muerte[:4]) if len(fecha_muerte) >= 4 else None
                    
                    if nac_year and muerte_year and muerte_year < nac_year:
                        self.errors.append(
                            "La fecha de muerte no puede ser anterior a la fecha de nacimiento"
                        )
                except ValueError:
                    self.warnings.append(
                        "No se pudo validar el orden de fechas (formato no reconocido)"
                    )
        
        # Validar que actos y versos sean números positivos
        if 'actos' in obra and obra['actos']:
            try:
                actos = int(obra['actos'])
                if actos < 0:
                    self.errors.append("El número de actos debe ser positivo")
            except (ValueError, TypeError):
                self.errors.append("El número de actos debe ser un número entero")
        
        if 'versos' in obra and obra['versos']:
            try:
                versos = int(obra['versos'])
                if versos < 0:
                    self.errors.append("El número de versos debe ser positivo")
            except (ValueError, TypeError):
                self.errors.append("El número de versos debe ser un número entero")
    
    def transform_obra(self, obra: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforma una obra para asegurar formato consistente
        """
        transformed = obra.copy()
        
        # Asegurar que autor sea un objeto si existe
        if 'autor' in transformed:
            if isinstance(transformed['autor'], str):
                transformed['autor'] = {'nombre': transformed['autor']}
            elif transformed['autor'] is None:
                transformed['autor'] = {}
        
        # Convertir valores booleanos
        if 'musica_conservada' in transformed:
            transformed['musica_conservada'] = self._to_bool(transformed['musica_conservada'])
        
        # Limpiar strings (trim, normalizar espacios)
        for key, value in transformed.items():
            if isinstance(value, str):
                transformed[key] = ' '.join(value.split())
            elif isinstance(value, dict):
                transformed[key] = self._clean_dict(value)
        
        return transformed
    
    def _to_bool(self, value: Any) -> bool:
        """Convierte un valor a booleano"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ['true', '1', 'yes', 'sí', 'si']
        return bool(value)
    
    def _clean_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Limpia strings en un diccionario"""
        cleaned = {}
        for key, value in data.items():
            if isinstance(value, str):
                cleaned[key] = ' '.join(value.split())
            elif isinstance(value, dict):
                cleaned[key] = self._clean_dict(value)
            else:
                cleaned[key] = value
        return cleaned
    
    def validate_batch(self, obras: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Valida un lote de obras
        Retorna: {
            'valid': [...],
            'invalid': [...],
            'stats': {...}
        }
        """
        valid = []
        invalid = []
        
        for obra in obras:
            is_valid, errors, warnings = self.validate_obra(obra)
            
            obra_info = {
                'obra': obra,
                'errors': errors,
                'warnings': warnings
            }
            
            if is_valid:
                valid.append(obra_info)
            else:
                invalid.append(obra_info)
        
        return {
            'valid': valid,
            'invalid': invalid,
            'stats': {
                'total': len(obras),
                'valid_count': len(valid),
                'invalid_count': len(invalid),
                'valid_percentage': (len(valid) / len(obras) * 100) if obras else 0
            }
        }


if __name__ == '__main__':
    # Ejemplo de uso
    validator = DataValidator()
    
    obra_ejemplo = {
        'id': 1,
        'titulo': 'Ejemplo de Obra',
        'autor': {
            'nombre': 'Autor Ejemplo',
            'fecha_nacimiento': '1600',
            'fecha_muerte': '1650'
        },
        'actos': 3,
        'versos': 2500
    }
    
    is_valid, errors, warnings = validator.validate_obra(obra_ejemplo)
    print(f"Válida: {is_valid}")
    print(f"Errores: {errors}")
    print(f"Advertencias: {warnings}")


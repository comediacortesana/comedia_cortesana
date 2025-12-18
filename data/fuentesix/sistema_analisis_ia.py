#!/usr/bin/env python3
"""
Sistema de Análisis e Interpretaciones de IA - Fuentes IX

Guarda análisis, interpretaciones y contexto de la IA al procesar textos,
similar al sistema de comentarios pero específico para datos extraídos por IA.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

class AnalisisIA:
    """
    Clase para crear análisis e interpretaciones de IA sobre datos extraídos
    
    Similar a comentarios pero específico para:
    - Frases originales donde se encontraron datos
    - Interpretaciones de la IA
    - Discrepancias detectadas
    - Contexto adicional
    - Patrones detectados
    """
    
    def __init__(self):
        self.analisis = []
    
    def crear_analisis_registro(
        self,
        tipo_registro: str,  # 'obra', 'representacion', 'lugar', 'mecenas'
        registro_id: Optional[str] = None,
        datos_extraidos: Dict = None,
        frases_originales: List[str] = None,
        interpretaciones: List[str] = None,
        discrepancias: List[Dict] = None,
        patrones_detectados: List[str] = None,
        confianza: str = 'medio',
        contexto_adicional: Dict = None
    ) -> Dict:
        """
        Crea un análisis de IA para un registro
        
        Returns:
            Dict con estructura de análisis_ia
        """
        analisis = {
            'tipo': 'analisis_ia_fuentes_ix',
            'tipo_registro': tipo_registro,  # obra, representacion, lugar, etc.
            'registro_id': registro_id,
            'fecha_analisis': datetime.now().isoformat(),
            'fuente_ia': 'sistema_extraccion_inteligente',
            'version_ia': '1.0.0',
            
            # Datos extraídos (resumen)
            'datos_extraidos': datos_extraidos or {},
            
            # Frases originales donde se encontraron los datos
            'frases_originales': frases_originales or [],
            
            # Interpretaciones de la IA
            'interpretaciones': interpretaciones or [],
            
            # Discrepancias detectadas
            'discrepancias': discrepancias or [],
            
            # Patrones detectados que llevaron a esta extracción
            'patrones_detectados': patrones_detectados or [],
            
            # Nivel de confianza
            'confianza': confianza,  # alto, medio, bajo
            
            # Contexto adicional
            'contexto_adicional': contexto_adicional or {},
            
            # Metadata
            'archivo_fuente': None,
            'pagina_pdf': None,
            'linea_texto': None,
        }
        
        self.analisis.append(analisis)
        return analisis
    
    def crear_analisis_discrepancia(
        self,
        tipo_discrepancia: str,  # 'fecha', 'lugar', 'compañia', 'titulo'
        registro_id: Optional[str] = None,
        fuente_1: Dict = None,
        fuente_2: Dict = None,
        interpretacion: str = None,
        confianza_resolucion: str = 'medio'
    ) -> Dict:
        """
        Crea un análisis específico para una discrepancia entre fuentes
        """
        return {
            'tipo': 'discrepancia_fuentes',
            'tipo_discrepancia': tipo_discrepancia,
            'registro_id': registro_id,
            'fecha_analisis': datetime.now().isoformat(),
            'fuente_1': fuente_1 or {},
            'fuente_2': fuente_2 or {},
            'interpretacion': interpretacion,
            'confianza_resolucion': confianza_resolucion,
            'ejemplo': self._generar_ejemplo_discrepancia(tipo_discrepancia, fuente_1, fuente_2)
        }
    
    def _generar_ejemplo_discrepancia(self, tipo: str, fuente_1: Dict, fuente_2: Dict) -> str:
        """Genera un texto descriptivo de la discrepancia"""
        if tipo == 'fecha':
            return f"Fuentes I registra fecha {fuente_1.get('fecha')}, pero Fuentes V registra {fuente_2.get('fecha')}"
        elif tipo == 'lugar':
            return f"Fuentes I menciona {fuente_1.get('lugar')}, Fuentes V menciona {fuente_2.get('lugar')}"
        elif tipo == 'compañia':
            return f"Fuentes I menciona compañía {fuente_1.get('compañia')}, Fuentes V menciona {fuente_2.get('compañia')}"
        elif tipo == 'titulo':
            return f"Fuentes I menciona título '{fuente_1.get('titulo')}', Fuentes V menciona '{fuente_2.get('titulo')}'"
        return "Discrepancia detectada entre fuentes"
    
    def crear_analisis_patron(
        self,
        patron_detectado: str,
        ejemplos: List[str],
        confianza: str = 'medio',
        tipo_patron: str = 'representacion'
    ) -> Dict:
        """
        Crea un análisis de un patrón detectado automáticamente
        """
        return {
            'tipo': 'patron_deteccion',
            'tipo_patron': tipo_patron,
            'patron': patron_detectado,
            'ejemplos': ejemplos,
            'confianza': confianza,
            'fecha_deteccion': datetime.now().isoformat(),
            'total_ejemplos': len(ejemplos)
        }
    
    def crear_analisis_frase_contexto(
        self,
        frase_original: str,
        terminos_identificados: Dict[str, List[str]],
        contexto_anterior: str = None,
        contexto_posterior: str = None,
        numero_linea: int = None
    ) -> Dict:
        """
        Crea un análisis de una frase con su contexto completo
        """
        return {
            'tipo': 'frase_contexto',
            'frase_original': frase_original,
            'terminos_identificados': terminos_identificados,
            'contexto_anterior': contexto_anterior,
            'contexto_posterior': contexto_posterior,
            'numero_linea': numero_linea,
            'fecha_analisis': datetime.now().isoformat(),
            'longitud_frase': len(frase_original),
            'tokens': len(frase_original.split())
        }
    
    def generar_json_analisis(self) -> Dict:
        """Genera JSON completo con todos los análisis"""
        return {
            'metadata': {
                'fecha_generacion': datetime.now().isoformat(),
                'total_analisis': len(self.analisis),
                'version_sistema': '1.0.0'
            },
            'analisis': self.analisis
        }
    
    def guardar_analisis(self, ruta_archivo: str):
        """Guarda los análisis en un archivo JSON"""
        datos = self.generar_json_analisis()
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        print(f"✅ Análisis guardado en: {ruta_archivo}")


# Ejemplo de uso
if __name__ == '__main__':
    analisis_ia = AnalisisIA()
    
    # Ejemplo 1: Análisis de una representación con discrepancia
    analisis_rep = analisis_ia.crear_analisis_registro(
        tipo_registro='representacion',
        registro_id='temp_part_001_rep_1',
        datos_extraidos={
            'obra_titulo': 'El Pastor Fido',
            'fecha': '22 de mayo de 1687',
            'compañia': 'compañía de Agustín Manuel',
            'lugar': 'Saloncillo del Buen Retiro'
        },
        frases_originales=[
            "El 22 de mayo de 1687 la compañía de Agustín Manuel representó El Pastor Fido, en el Saloncillo del Buen Retiro, según Fuentes V",
            "y en el Saloncete, según Fuentes I"
        ],
        interpretaciones=[
            "Ambas fuentes mencionan la misma representación pero con nombres diferentes de sala",
            "Saloncillo y Saloncete son ambas salas del Buen Retiro, probablemente la misma representación"
        ],
        discrepancias=[
            {
                'tipo': 'lugar',
                'fuente_1': {'fuente': 'Fuentes I', 'lugar': 'Saloncete'},
                'fuente_2': {'fuente': 'Fuentes V', 'lugar': 'Saloncillo del Buen Retiro'},
                'resolucion': 'Ambas son salas del Buen Retiro, probablemente la misma representación'
            }
        ],
        patrones_detectados=[
            "[FECHA] la compañía de [COMPAÑÍA] representó [OBRA], en [LUGAR], según [FUENTE]"
        ],
        confianza='medio',
        contexto_adicional={
            'archivo_fuente': 'part_001',
            'pagina_pdf': 134
        }
    )
    
    # Ejemplo 2: Análisis de discrepancia específica
    analisis_disc = analisis_ia.crear_analisis_discrepancia(
        tipo_discrepancia='fecha',
        registro_id='temp_part_001_rep_2',
        fuente_1={'fuente': 'Fuentes V', 'fecha': '3 de octubre de 1685', 'compañia': 'Rosendo López'},
        fuente_2={'fuente': 'Fuentes I', 'fecha': '4 de octubre de 1685', 'compañia': 'Manuel de Mosquera'},
        interpretacion='Es poco probable que dos compañías distintas hubiesen interpretado la misma comedia dos días seguidos. Posiblemente misma representación con datos contradictorios.',
        confianza_resolucion='medio'
    )
    
    # Guardar
    analisis_ia.guardar_analisis('ejemplo_analisis_ia.json')
    print(f"\n✅ Ejemplos creados:")
    print(f"   - Análisis de representación: {len(analisis_rep)} campos")
    print(f"   - Análisis de discrepancia: {len(analisis_disc)} campos")







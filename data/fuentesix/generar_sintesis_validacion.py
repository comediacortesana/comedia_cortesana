#!/usr/bin/env python3
"""
Genera síntesis legibles en frases para validación de investigadores

Convierte análisis JSON en síntesis legibles que los investigadores pueden
revisar, validar o rechazar antes de integrar a la DB.
"""

import json
from typing import Dict, List, Optional
from datetime import datetime

class GeneradorSintesis:
    """Genera síntesis legibles de análisis de IA"""
    
    def generar_sintesis_representacion(self, registro: Dict) -> Dict:
        """
        Genera síntesis legible de una representación extraída
        
        Args:
            registro: Dict con 'datos' y 'metadata_registro'
        
        Returns:
            Dict con síntesis legible
        """
        datos = registro.get('datos', registro)
        metadata = registro.get('metadata_registro', {})
        
        # Construir síntesis en frases naturales
        frases = []
        
        # Información principal
        obra_titulo = datos.get('obra_titulo', 'Obra desconocida')
        fecha = datos.get('fecha', 'Fecha desconocida')
        compañia = datos.get('compañia', datos.get('director_compañia', 'Compañía desconocida'))
        lugar = datos.get('lugar_nombre', 'Lugar desconocido')
        
        frases.append(f"Se encontró una representación de la obra '{obra_titulo}' el {fecha}.")
        
        if compañia and compañia != 'Compañía desconocida':
            frases.append(f"La representación fue realizada por {compañia}.")
        
        if lugar and lugar != 'Lugar desconocido':
            tipo_lugar = datos.get('lugar_tipo', '')
            if tipo_lugar:
                frases.append(f"Tuvo lugar en {lugar} ({tipo_lugar}).")
            else:
                frases.append(f"Tuvo lugar en {lugar}.")
        
        # Información adicional
        tipo_funcion = datos.get('tipo_funcion', '')
        if tipo_funcion:
            frases.append(f"Tipo de función: {tipo_funcion}.")
        
        publico = datos.get('publico', '')
        if publico:
            frases.append(f"Público: {publico}.")
        
        # Observaciones y discrepancias
        observaciones = datos.get('observaciones', '')
        if observaciones:
            if 'DISCREPANCIA' in observaciones:
                frases.append(f"⚠️ DISCREPANCIA DETECTADA: {observaciones}")
            else:
                frases.append(f"Observaciones: {observaciones}")
        
        # Referencia al PDF
        referencia_pdf = metadata.get('referencia_pagina_pdf', {})
        pagina_pdf = referencia_pdf.get('pagina_pdf') or datos.get('pagina_pdf')
        if pagina_pdf:
            frases.append(f"📄 Esta información aparece en la página {pagina_pdf} del PDF original.")
        
        # Texto original
        texto_original = metadata.get('texto_original', datos.get('texto_original', ''))
        if texto_original:
            frases.append(f"Texto original extraído: \"{texto_original[:200]}{'...' if len(texto_original) > 200 else ''}\"")
        
        # Confianza
        confianza = metadata.get('confianza', datos.get('confianza', 'medio'))
        nivel_confianza = {
            'alto': '🔵 Alta confianza',
            'medio': '🟡 Confianza media',
            'bajo': '🔴 Baja confianza'
        }.get(confianza, f'Confianza: {confianza}')
        frases.append(f"Nivel de confianza: {nivel_confianza}")
        
        return {
            'tipo': 'representacion',
            'id_temporal': metadata.get('id_temporal', f"temp_{datetime.now().isoformat()}"),
            'sintesis': ' '.join(frases),
            'frases': frases,
            'datos_json': datos,
            'metadata': metadata,
            'confianza': confianza,
            'pagina_pdf': pagina_pdf,
            'texto_original': texto_original
        }
    
    def generar_sintesis_obra(self, registro: Dict) -> Dict:
        """Genera síntesis legible de una obra extraída"""
        datos = registro.get('datos', registro)
        metadata = registro.get('metadata_registro', {})
        
        frases = []
        
        titulo = datos.get('titulo', datos.get('obra_titulo', 'Título desconocido'))
        frases.append(f"Se encontró información sobre la obra '{titulo}'.")
        
        autor = datos.get('autor', '')
        if autor:
            frases.append(f"Autor: {autor}.")
        
        genero = datos.get('genero', '')
        if genero:
            frases.append(f"Género: {genero}.")
        
        tipo_obra = datos.get('tipo_obra', '')
        if tipo_obra:
            frases.append(f"Tipo: {tipo_obra}.")
        
        # Referencia al PDF
        referencia_pdf = metadata.get('referencia_pagina_pdf', {})
        pagina_pdf = referencia_pdf.get('pagina_pdf') or datos.get('pagina_pdf')
        if pagina_pdf:
            frases.append(f"📄 Información encontrada en la página {pagina_pdf} del PDF original.")
        
        return {
            'tipo': 'obra',
            'id_temporal': metadata.get('id_temporal', f"temp_{datetime.now().isoformat()}"),
            'sintesis': ' '.join(frases),
            'frases': frases,
            'datos_json': datos,
            'metadata': metadata
        }
    
    def generar_sintesis_lugar(self, registro: Dict) -> Dict:
        """Genera síntesis legible de un lugar extraído"""
        datos = registro.get('datos', registro)
        metadata = registro.get('metadata_registro', {})
        
        frases = []
        
        nombre = datos.get('nombre', 'Lugar desconocido')
        frases.append(f"Se encontró información sobre el lugar '{nombre}'.")
        
        tipo = datos.get('tipo_lugar', '')
        if tipo:
            frases.append(f"Tipo: {tipo}.")
        
        region = datos.get('region', '')
        ciudad = datos.get('ciudad', '')
        if region or ciudad:
            ubicacion = ', '.join(filter(None, [ciudad, region]))
            frases.append(f"Ubicación: {ubicacion}.")
        
        return {
            'tipo': 'lugar',
            'id_temporal': metadata.get('id_temporal', f"temp_{datetime.now().isoformat()}"),
            'sintesis': ' '.join(frases),
            'frases': frases,
            'datos_json': datos,
            'metadata': metadata
        }
    
    def procesar_archivo_extraccion(self, archivo_json: str) -> Dict:
        """
        Procesa un archivo de extracción y genera síntesis para validación
        
        Returns:
            Dict con síntesis organizadas por tipo
        """
        with open(archivo_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        metadata_archivo = datos.get('metadata', {})
        sintesis = {
            'metadata_archivo': metadata_archivo,
            'representaciones': [],
            'obras': [],
            'lugares': [],
            'fecha_generacion': datetime.now().isoformat()
        }
        
        # Procesar representaciones
        representaciones = datos.get('representaciones', [])
        for rep in representaciones:
            sintesis_rep = self.generar_sintesis_representacion(rep)
            sintesis['representaciones'].append(sintesis_rep)
        
        # Procesar obras
        obras = datos.get('obras', [])
        for obra in obras:
            sintesis_obra = self.generar_sintesis_obra(obra)
            sintesis['obras'].append(sintesis_obra)
        
        # Procesar lugares
        lugares = datos.get('lugares_nuevos', [])
        for lugar in lugares:
            sintesis_lugar = self.generar_sintesis_lugar(lugar)
            sintesis['lugares'].append(sintesis_lugar)
        
        return sintesis


def generar_archivo_validacion(archivo_extraccion: str, archivo_salida: str = None):
    """
    Genera archivo JSON con síntesis para validación
    
    Args:
        archivo_extraccion: Archivo JSON con datos extraídos
        archivo_salida: Archivo de salida (opcional)
    """
    generador = GeneradorSintesis()
    sintesis = generador.procesar_archivo_extraccion(archivo_extraccion)
    
    if not archivo_salida:
        archivo_salida = archivo_extraccion.replace('.json', '_sintesis_validacion.json')
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(sintesis, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Síntesis generada: {archivo_salida}")
    print(f"   - Representaciones: {len(sintesis['representaciones'])}")
    print(f"   - Obras: {len(sintesis['obras'])}")
    print(f"   - Lugares: {len(sintesis['lugares'])}")
    
    return archivo_salida


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python generar_sintesis_validacion.py <archivo_extraccion.json> [archivo_salida.json]")
        sys.exit(1)
    
    archivo_extraccion = sys.argv[1]
    archivo_salida = sys.argv[2] if len(sys.argv) > 2 else None
    
    generar_archivo_validacion(archivo_extraccion, archivo_salida)







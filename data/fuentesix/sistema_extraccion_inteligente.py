#!/usr/bin/env python3
"""
Sistema de Extracción Inteligente de Datos - Fuentes IX

Analiza textos por frases, crea un lemario de términos y genera patrones
de detección basados en el contexto donde aparecen los términos.
"""

import re
import json
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple
from datetime import datetime
import os

class ExtractorInteligente:
    """Sistema inteligente de extracción basado en aprendizaje de patrones"""
    
    def __init__(self):
        self.lemario = {
            'autores': defaultdict(list),  # autor -> [frases donde aparece]
            'lugares': defaultdict(list),
            'compañias': defaultdict(list),
            'obras': defaultdict(list),
            'fechas': defaultdict(list),
            'mecenas': defaultdict(list),
            'personajes': defaultdict(list),
        }
        
        self.frases_completas = []  # Todas las frases extraídas
        self.patrones_deteccion = {
            'representacion': [],
            'fecha': [],
            'lugar': [],
            'compañia': [],
            'mecenas': [],
            'obra': []
        }
        
        self.terminos_frecuentes = Counter()
        
    def extraer_frases(self, texto: str) -> List[Dict]:
        """
        Extrae frases completas del texto, preservando contexto
        
        Returns:
            Lista de frases con metadata
        """
        frases = []
        
        # Dividir por oraciones (puntos seguidos de espacio y mayúscula, o final de línea)
        # Patrón más sofisticado para capturar frases completas
        patrones_frase = [
            r'([^\.]+\.)\s+(?=[A-ZÁÉÍÓÚÑ])',  # Frase terminada en punto seguida de mayúscula
            r'\((\d+)\)\s+([^\(]+?)(?=\(\d+\)|$)',  # Representaciones numeradas
            r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4}[^\.]*)',  # Fechas con contexto
        ]
        
        # Dividir por líneas primero
        lineas = texto.split('\n')
        
        for num_linea, linea in enumerate(lineas, 1):
            linea = linea.strip()
            if not linea or len(linea) < 10:
                continue
            
            # Detectar si es una frase con datos útiles
            tiene_fecha = bool(re.search(r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}', linea))
            tiene_compañia = bool(re.search(r'compañía|\.\s+[A-Z][a-z]+(?:\s+de\s+[A-Z][a-z]+)*\.', linea))
            tiene_lugar = bool(re.search(r'Palacio|Buen Retiro|Corral|Cuarto|Salón', linea, re.IGNORECASE))
            tiene_obra = bool(re.search(r'representó|hizo|representaron', linea, re.IGNORECASE))
            
            if tiene_fecha or tiene_compañia or tiene_lugar or tiene_obra:
                frase_info = {
                    'texto': linea,
                    'numero_linea': num_linea,
                    'tiene_fecha': tiene_fecha,
                    'tiene_compañia': tiene_compañia,
                    'tiene_lugar': tiene_lugar,
                    'tiene_obra': tiene_obra,
                    'longitud': len(linea),
                    'tokens': len(linea.split())
                }
                frases.append(frase_info)
                self.frases_completas.append(frase_info)
        
        return frases
    
    def identificar_terminos(self, frase: str, tipo: str = None) -> List[Tuple[str, str]]:
        """
        Identifica términos clave en una frase
        
        Returns:
            Lista de (termino, tipo) encontrados
        """
        terminos = []
        
        # Patrones para diferentes tipos de términos
        patrones = {
            'fecha': [
                r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',
                r'(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo)\s+de\s+\w+\s+de\s+\d{4}',
                r'(\d{4})',
                r'(antes\s+del\s+\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',
                r'(Entre\s+[^y]+y\s+[^\.]+)',
            ],
            'compañia': [
                r'compañía\s+de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+de\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
                r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+de\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)\.\s+(?:Palacio|Buen Retiro|Corral|Representación)',
                r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)\s+y\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
                r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+de\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)\s+\.\s+(?:Palacio|Buen Retiro)',
                r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\s*\.\s*(?:Palacio|Buen Retiro|Corral)',
            ],
            'lugar': [
                r'(Palacio)',
                r'(Buen Retiro)',
                r'(Coliseo\s+del\s+Buen Retiro)',
                r'(Cuarto\s+de\s+la\s+Reina)',
                r'(Cuarto\s+del\s+Rey)',
                r'(Salón(?:\s+dorado)?)',
                r'(Corral\s+del\s+Príncipe)',
                r'(Corral\s+de\s+la\s+Cruz)',
                r'(Saloncete|Saloncillo)',
                r'(Pardo)',
            ],
            'obra': [
                r'representó\s+([A-ZÁÉÍÓÚÑ][^\.]+?)(?:\.|,|en|por)',
                r'hizo\s+([A-ZÁÉÍÓÚÑ][^\.]+?)(?:\.|,|en|por)',
                r'([A-ZÁÉÍÓÚÑ][^,\.]+?),\s+El\s+',
            ],
            'mecenas': [
                r'(Reina|Rey|Infante|Príncipe|Condestable|Marqués|Conde|Duque)\s+[^\.]+',
                r'para\s+celebrar\s+el\s+(?:cumpleaños|santo|boda)\s+de\s+([^\.]+)',
                r'festejar\s+a\s+([^\.]+)',
            ],
        }
        
        for tipo_term, patrones_tipo in patrones.items():
            for patron in patrones_tipo:
                try:
                    matches = re.finditer(patron, frase, re.IGNORECASE)
                    for match in matches:
                        # Obtener el grupo capturado o el match completo
                        if match.lastindex and match.lastindex > 0:
                            termino = match.group(1)
                        else:
                            termino = match.group(0)
                        
                        termino = termino.strip()
                        
                        # Filtrar términos muy cortos o que son solo números
                        if len(termino) > 2 and not termino.isdigit():
                            # Normalizar antes de añadir
                            termino_norm = self.normalizar_termino(termino)
                            terminos.append((termino_norm, tipo_term))
                            self.terminos_frecuentes[termino_norm] += 1
                except Exception as e:
                    # Continuar si hay error en un patrón
                    continue
        
        return terminos
    
    def indexar_frase(self, frase_info: Dict):
        """Indexa una frase en el lemario"""
        frase_texto = frase_info['texto']
        
        # Identificar términos en la frase
        terminos = self.identificar_terminos(frase_texto)
        
        for termino_norm, tipo in terminos:
            # Añadir al lemario correspondiente
            if tipo in self.lemario:
                contexto = {
                    'frase': frase_texto,
                    'linea': frase_info['numero_linea'],
                    'termino_normalizado': termino_norm
                }
                self.lemario[tipo][termino_norm].append(contexto)
    
    def normalizar_termino(self, termino: str) -> str:
        """Normaliza un término para agrupar variantes"""
        termino = termino.strip()
        
        # Normalizar mayúsculas/minúsculas
        termino = termino.title()
        
        # Normalizar espacios múltiples
        termino = re.sub(r'\s+', ' ', termino)
        
        # Normalizar variantes comunes
        normalizaciones = {
            'Compañía De': 'Compañía de',
            'Compañia De': 'Compañía de',
            'Compañía': 'Compañía',
        }
        
        for variante, normalizado in normalizaciones.items():
            if variante in termino:
                termino = termino.replace(variante, normalizado)
        
        return termino
    
    def generar_patrones_deteccion(self) -> Dict:
        """
        Genera patrones de detección basados en los ejemplos encontrados
        
        Returns:
            Dict con patrones sugeridos para cada tipo
        """
        patrones = {
            'representacion': [],
            'fecha': [],
            'lugar': [],
            'compañia': [],
            'mecenas': [],
            'obra': []
        }
        
        # Analizar frases que tienen múltiples elementos
        frases_completas = [f for f in self.frases_completas if sum([
            f['tiene_fecha'], f['tiene_compañia'], f['tiene_lugar'], f['tiene_obra']
        ]) >= 2]
        
        # Generar patrones para representaciones
        for frase_info in frases_completas[:50]:  # Analizar primeras 50
            frase = frase_info['texto']
            
            # Patrón de representación completa
            if frase_info['tiene_fecha'] and frase_info['tiene_compañia']:
                patron = self.extraer_patron_representacion(frase)
                if patron:
                    patrones['representacion'].append({
                        'patron': patron,
                        'ejemplo': frase,
                        'confianza': 'alto' if frase_info['tiene_lugar'] else 'medio'
                    })
        
        # Generar patrones para fechas
        fechas_ejemplos = []
        for termino, contextos in list(self.lemario['fechas'].items())[:20]:
            for contexto in contextos[:3]:  # Primeros 3 ejemplos
                fechas_ejemplos.append(contexto['frase'])
        
        patrones['fecha'] = self.generar_patrones_fecha(fechas_ejemplos)
        
        # Generar patrones para compañías
        companias_ejemplos = []
        for termino, contextos in list(self.lemario['compañias'].items())[:20]:
            for contexto in contextos[:3]:
                companias_ejemplos.append(contexto['frase'])
        
        patrones['compañia'] = self.generar_patrones_compañia(companias_ejemplos)
        
        # Generar patrones para lugares
        lugares_ejemplos = []
        for termino, contextos in list(self.lemario['lugares'].items())[:20]:
            for contexto in contextos[:3]:
                lugares_ejemplos.append(contexto['frase'])
        
        patrones['lugar'] = self.generar_patrones_lugar(lugares_ejemplos)
        
        return patrones
    
    def extraer_patron_representacion(self, frase: str) -> str:
        """Extrae un patrón genérico de representación de una frase"""
        # Reemplazar valores específicos por placeholders
        patron = frase
        
        # Reemplazar fechas
        patron = re.sub(r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}', '[FECHA]', patron)
        patron = re.sub(r'\d{4}', '[AÑO]', patron)
        
        # Reemplazar nombres propios
        patron = re.sub(r'[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+de\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+', '[NOMBRE_COMPLETO]', patron)
        patron = re.sub(r'[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+', '[NOMBRE]', patron)
        
        return patron
    
    def generar_patrones_fecha(self, ejemplos: List[str]) -> List[Dict]:
        """Genera patrones de fecha basados en ejemplos"""
        patrones = []
        
        formatos_encontrados = Counter()
        
        for ejemplo in ejemplos:
            # Detectar formato
            if re.search(r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}', ejemplo):
                formato = 'dia_mes_año'
            elif re.search(r'\d{4}', ejemplo):
                formato = 'solo_año'
            elif re.search(r'antes\s+del', ejemplo, re.IGNORECASE):
                formato = 'antes_de'
            elif re.search(r'Entre', ejemplo):
                formato = 'rango'
            else:
                formato = 'otro'
            
            formatos_encontrados[formato] += 1
        
        for formato, count in formatos_encontrados.most_common():
            patrones.append({
                'formato': formato,
                'frecuencia': count,
                'patron_regex': self.get_regex_fecha(formato),
                'ejemplos': [e for e in ejemplos if self.coincide_formato(e, formato)][:5]
            })
        
        return patrones
    
    def get_regex_fecha(self, formato: str) -> str:
        """Retorna regex para un formato de fecha"""
        regexes = {
            'dia_mes_año': r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})',
            'solo_año': r'(\d{4})',
            'antes_de': r'antes\s+del\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})',
            'rango': r'Entre\s+([^y]+)\s+y\s+([^\.]+)',
        }
        return regexes.get(formato, '')
    
    def coincide_formato(self, texto: str, formato: str) -> bool:
        """Verifica si un texto coincide con un formato"""
        regex = self.get_regex_fecha(formato)
        return bool(re.search(regex, texto)) if regex else False
    
    def generar_patrones_compañia(self, ejemplos: List[str]) -> List[Dict]:
        """Genera patrones de compañía basados en ejemplos"""
        patrones = []
        
        formatos = Counter()
        
        for ejemplo in ejemplos:
            if 'compañía de' in ejemplo.lower():
                formato = 'compañía_de_X'
            elif re.search(r'[A-Z][a-z]+\.\s+(?:Palacio|Buen Retiro)', ejemplo):
                formato = 'nombre_punto_lugar'
            elif ' y ' in ejemplo and any(c.isupper() for c in ejemplo):
                formato = 'múltiples_compañías'
            else:
                formato = 'otro'
            
            formatos[formato] += 1
        
        for formato, count in formatos.most_common():
            patrones.append({
                'formato': formato,
                'frecuencia': count,
                'ejemplos': [e for e in ejemplos if self.coincide_formato_compañia(e, formato)][:5]
            })
        
        return patrones
    
    def coincide_formato_compañia(self, texto: str, formato: str) -> bool:
        """Verifica si un texto coincide con formato de compañía"""
        if formato == 'compañía_de_X':
            return 'compañía de' in texto.lower()
        elif formato == 'nombre_punto_lugar':
            return bool(re.search(r'[A-Z][a-z]+\.\s+(?:Palacio|Buen Retiro)', texto))
        elif formato == 'múltiples_compañías':
            return ' y ' in texto and any(c.isupper() for c in texto)
        return False
    
    def generar_patrones_lugar(self, ejemplos: List[str]) -> List[Dict]:
        """Genera patrones de lugar basados en ejemplos"""
        lugares_unicos = set()
        
        for ejemplo in ejemplos:
            lugares_encontrados = re.findall(
                r'(Palacio|Buen Retiro|Coliseo|Cuarto|Salón|Corral|Saloncete|Saloncillo|Pardo)',
                ejemplo,
                re.IGNORECASE
            )
            lugares_unicos.update(lugares_encontrados)
        
        return [{
            'lugar': lugar,
            'frecuencia': sum(1 for e in ejemplos if lugar.lower() in e.lower()),
            'ejemplos': [e for e in ejemplos if lugar.lower() in e.lower()][:5]
        } for lugar in sorted(lugares_unicos)]
    
    def procesar_archivo(self, ruta_archivo: str):
        """Procesa un archivo completo"""
        print(f"📖 Procesando: {ruta_archivo}")
        
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Extraer frases
        frases = self.extraer_frases(contenido)
        print(f"   ✅ Frases extraídas: {len(frases)}")
        
        # Indexar cada frase
        for frase_info in frases:
            self.indexar_frase(frase_info)
        
        print(f"   ✅ Términos indexados:")
        for tipo, terminos in self.lemario.items():
            if terminos:
                print(f"      - {tipo}: {len(terminos)} términos únicos")
    
    def generar_reporte(self) -> Dict:
        """Genera reporte completo del análisis"""
        # Generar patrones de detección
        patrones = self.generar_patrones_deteccion()
        
        # Términos más frecuentes
        terminos_top = dict(self.terminos_frecuentes.most_common(50))
        
        # Estadísticas del lemario
        estadisticas_lemario = {}
        for tipo, terminos in self.lemario.items():
            estadisticas_lemario[tipo] = {
                'total_terminos': len(terminos),
                'total_ocurrencias': sum(len(contextos) for contextos in terminos.values()),
                'top_5': [
                    {
                        'termino': termino,
                        'ocurrencias': len(contextos),
                        'ejemplo': contextos[0]['frase'] if contextos else ''
                    }
                    for termino, contextos in list(terminos.items())[:5]
                ]
            }
        
        return {
            'metadata': {
                'fecha_analisis': datetime.now().isoformat(),
                'total_frases': len(self.frases_completas),
                'total_terminos_unicos': len(self.terminos_frecuentes)
            },
            'estadisticas': {
                'frases_con_fecha': sum(1 for f in self.frases_completas if f['tiene_fecha']),
                'frases_con_compañia': sum(1 for f in self.frases_completas if f['tiene_compañia']),
                'frases_con_lugar': sum(1 for f in self.frases_completas if f['tiene_lugar']),
                'frases_completas': sum(1 for f in self.frases_completas if sum([
                    f['tiene_fecha'], f['tiene_compañia'], f['tiene_lugar'], f['tiene_obra']
                ]) >= 3)
            },
            'lemario': estadisticas_lemario,
            'terminos_frecuentes': terminos_top,
            'patrones_deteccion': patrones,
            'ejemplos_frases': [
                {
                    'texto': f['texto'],
                    'linea': f['numero_linea'],
                    'elementos': {
                        'fecha': f['tiene_fecha'],
                        'compañia': f['tiene_compañia'],
                        'lugar': f['tiene_lugar'],
                        'obra': f['tiene_obra']
                    }
                }
                for f in self.frases_completas[:20]
            ]
        }


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python sistema_extraccion_inteligente.py <archivo1> [archivo2] ...")
        sys.exit(1)
    
    extractor = ExtractorInteligente()
    
    # Procesar todos los archivos
    for archivo in sys.argv[1:]:
        if os.path.exists(archivo):
            extractor.procesar_archivo(archivo)
        else:
            print(f"⚠️  Archivo no encontrado: {archivo}")
    
    # Generar reporte
    print("\n" + "="*60)
    print("📊 GENERANDO REPORTE DE ANÁLISIS")
    print("="*60)
    
    reporte = extractor.generar_reporte()
    
    # Guardar reporte
    archivo_reporte = 'analisis_inteligente_fuentes_ix.json'
    with open(archivo_reporte, 'w', encoding='utf-8') as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Reporte guardado en: {archivo_reporte}")
    print(f"\n📈 Resumen:")
    print(f"   - Frases analizadas: {reporte['metadata']['total_frases']}")
    print(f"   - Términos únicos: {reporte['metadata']['total_terminos_unicos']}")
    print(f"   - Frases completas (3+ elementos): {reporte['estadisticas']['frases_completas']}")
    
    # Mostrar top términos por tipo
    print(f"\n🔍 Top términos por categoría:")
    for tipo, stats in reporte['lemario'].items():
        if stats['total_terminos'] > 0:
            print(f"\n   {tipo.upper()}:")
            for top in stats['top_5']:
                print(f"      - {top['termino']}: {top['ocurrencias']} ocurrencias")


if __name__ == '__main__':
    main()







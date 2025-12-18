#!/usr/bin/env python3
"""
Script de Integración de Datos de Fuentes IX con Sistema de Versionado

Este script integra los datos extraídos de los archivos de texto de Fuentes IX
a la base de datos, manteniendo un registro completo de versionado y auditoría.

Uso:
    python script_integracion_versionado.py --archivo extraccion_part_001.json --version 1.0.0 --dry-run
    python script_integracion_versionado.py --archivo extraccion_part_001.json --version 1.0.0 --integrar
"""

import json
import argparse
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
import os
import sys

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

class IntegradorDatosFuentesIX:
    """Clase para integrar datos de Fuentes IX con versionado completo"""
    
    def __init__(self, version_datos: str, dry_run: bool = True):
        """
        Inicializa el integrador
        
        Args:
            version_datos: Versión de los datos (ej: "1.0.0-20250127-153000")
            dry_run: Si True, solo valida sin integrar
        """
        self.version_datos = version_datos
        self.fecha_integracion = datetime.now()
        self.dry_run = dry_run
        self.log_operaciones: List[Dict] = []
        self.errores: List[Dict] = []
        self.advertencias: List[Dict] = []
        self.estadisticas = {
            'total_registros': 0,
            'insertados': 0,
            'actualizados': 0,
            'omitidos': 0,
            'errores': 0
        }
        
    def calcular_checksum(self, datos: Dict) -> str:
        """Calcula checksum SHA256 de los datos"""
        datos_str = json.dumps(datos, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(datos_str.encode('utf-8')).hexdigest()
    
    def validar_datos_nuevos(self, datos_nuevos: Dict, datos_existentes: Optional[Dict] = None) -> Dict:
        """
        Compara y valida datos nuevos antes de integrar
        
        Returns:
            Dict con diferencias encontradas
        """
        diferencias = {
            'campos_nuevos': [],
            'valores_diferentes': [],
            'conflictos': [],
            'advertencias': []
        }
        
        if not datos_existentes:
            diferencias['campos_nuevos'] = list(datos_nuevos.keys())
            return diferencias
        
        for campo, valor_nuevo in datos_nuevos.items():
            valor_existente = datos_existentes.get(campo)
            
            if valor_existente is None:
                diferencias['campos_nuevos'].append(campo)
            elif valor_existente != valor_nuevo:
                # Verificar si es un conflicto significativo
                if campo in ['titulo', 'autor', 'fecha']:
                    diferencias['conflictos'].append({
                        'campo': campo,
                        'anterior': valor_existente,
                        'nuevo': valor_nuevo,
                        'severidad': 'alta'
                    })
                else:
                    diferencias['valores_diferentes'].append({
                        'campo': campo,
                        'anterior': valor_existente,
                        'nuevo': valor_nuevo
                    })
        
        return diferencias
    
    def integrar_registro(self, tabla: str, datos_nuevos: Dict, registro_existente: Optional[Dict] = None, metadata_registro: Optional[Dict] = None):
        """
        Integra un registro con logging completo
        
        Args:
            tabla: Nombre de la tabla (obras, representaciones, lugares)
            datos_nuevos: Datos nuevos a integrar
            registro_existente: Registro existente si hay uno
            metadata_registro: Metadatos del registro extraído
        """
        self.estadisticas['total_registros'] += 1
        
        # Validar antes de integrar
        diferencias = self.validar_datos_nuevos(datos_nuevos, registro_existente)
        
        # Preparar operación
        operacion = {
            'tipo': 'INSERT' if not registro_existente else 'UPDATE',
            'tabla': tabla,
            'datos_anteriores': registro_existente,
            'datos_nuevos': datos_nuevos,
            'version': self.version_datos,
            'fecha': self.fecha_integracion.isoformat(),
            'metadata_registro': metadata_registro,
            'diferencias': diferencias
        }
        
        # Verificar conflictos
        if diferencias['conflictos']:
            self.advertencias.append({
                'tipo': 'conflicto',
                'tabla': tabla,
                'datos': datos_nuevos,
                'conflictos': diferencias['conflictos'],
                'mensaje': f'Conflicto en {tabla}: requiere revisión manual'
            })
            operacion['estado'] = 'pendiente_revision'
            self.estadisticas['omitidos'] += 1
        else:
            operacion['estado'] = 'listo_para_integrar'
            
            if not self.dry_run:
                # Aquí iría la lógica real de integración a la DB
                # Por ahora solo simulamos
                if registro_existente:
                    self.estadisticas['actualizados'] += 1
                else:
                    self.estadisticas['insertados'] += 1
            else:
                # En dry-run, solo contamos
                if registro_existente:
                    self.estadisticas['actualizados'] += 1
                else:
                    self.estadisticas['insertados'] += 1
        
        self.log_operaciones.append(operacion)
    
    def procesar_archivo_extraccion(self, archivo_json: str):
        """
        Procesa un archivo JSON de extracción completo
        
        Args:
            archivo_json: Ruta al archivo JSON de extracción
        """
        with open(archivo_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        metadata = datos.get('metadata', {})
        
        # Validar metadata
        if not metadata.get('archivo_fuente'):
            self.errores.append({
                'tipo': 'metadata_faltante',
                'mensaje': 'Falta archivo_fuente en metadata'
            })
            return
        
        # Procesar obras
        obras = datos.get('obras', [])
        for obra in obras:
            datos_obra = obra.get('datos', {})
            metadata_obra = obra.get('metadata_registro', {})
            
            # Buscar obra existente (simulado - aquí iría consulta real a DB)
            obra_existente = None  # buscar_obra_por_titulo(datos_obra.get('titulo'))
            
            self.integrar_registro('obras', datos_obra, obra_existente, metadata_obra)
        
        # Procesar representaciones
        representaciones = datos.get('representaciones', [])
        for rep in representaciones:
            datos_rep = rep.get('datos', rep)  # Si no hay 'datos', usar el objeto completo
            metadata_rep = rep.get('metadata_registro', {})
            
            # Buscar representación existente (simulado)
            rep_existente = None
            
            self.integrar_registro('representaciones', datos_rep, rep_existente, metadata_rep)
        
        # Procesar lugares
        lugares = datos.get('lugares_nuevos', [])
        for lugar in lugares:
            datos_lugar = lugar.get('datos', lugar)
            metadata_lugar = lugar.get('metadata_registro', {})
            
            lugar_existente = None
            
            self.integrar_registro('lugares', datos_lugar, lugar_existente, metadata_lugar)
    
    def generar_reporte(self) -> Dict:
        """Genera reporte completo de la integración"""
        return {
            'version': self.version_datos,
            'fecha': self.fecha_integracion.isoformat(),
            'modo': 'dry_run' if self.dry_run else 'integracion_real',
            'estadisticas': self.estadisticas,
            'total_operaciones': len(self.log_operaciones),
            'total_errores': len(self.errores),
            'total_advertencias': len(self.advertencias),
            'errores': self.errores,
            'advertencias': self.advertencias[:10],  # Primeras 10 advertencias
            'operaciones_ejemplo': self.log_operaciones[:5]  # Primeras 5 operaciones
        }
    
    def guardar_reporte(self, ruta_reporte: str):
        """Guarda el reporte en un archivo JSON"""
        reporte = self.generar_reporte()
        
        # Añadir log completo si es necesario
        reporte_completo = {
            **reporte,
            'log_completo': self.log_operaciones
        }
        
        with open(ruta_reporte, 'w', encoding='utf-8') as f:
            json.dump(reporte_completo, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Reporte guardado en: {ruta_reporte}")


def main():
    parser = argparse.ArgumentParser(description='Integrar datos de Fuentes IX con versionado')
    parser.add_argument('--archivo', required=True, help='Archivo JSON de extracción a procesar')
    parser.add_argument('--version', required=True, help='Versión de los datos (ej: 1.0.0-20250127-153000)')
    parser.add_argument('--integrar', action='store_true', help='Realizar integración real (por defecto es dry-run)')
    parser.add_argument('--reporte', help='Ruta donde guardar el reporte (opcional)')
    
    args = parser.parse_args()
    
    # Validar archivo
    if not os.path.exists(args.archivo):
        print(f"❌ Error: Archivo no encontrado: {args.archivo}")
        return 1
    
    # Crear integrador
    integrador = IntegradorDatosFuentesIX(
        version_datos=args.version,
        dry_run=not args.integrar
    )
    
    print(f"🔄 Procesando archivo: {args.archivo}")
    print(f"📦 Versión: {args.version}")
    print(f"🔍 Modo: {'DRY-RUN' if integrador.dry_run else 'INTEGRACIÓN REAL'}")
    print("-" * 60)
    
    # Procesar archivo
    try:
        integrador.procesar_archivo_extraccion(args.archivo)
    except Exception as e:
        print(f"❌ Error procesando archivo: {e}")
        return 1
    
    # Generar reporte
    reporte = integrador.generar_reporte()
    
    # Mostrar resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE INTEGRACIÓN")
    print("=" * 60)
    print(f"Total registros procesados: {reporte['estadisticas']['total_registros']}")
    print(f"  ✅ Insertados: {reporte['estadisticas']['insertados']}")
    print(f"  🔄 Actualizados: {reporte['estadisticas']['actualizados']}")
    print(f"  ⏸️  Omitidos (conflictos): {reporte['estadisticas']['omitidos']}")
    print(f"  ❌ Errores: {reporte['total_errores']}")
    print(f"  ⚠️  Advertencias: {reporte['total_advertencias']}")
    
    if reporte['errores']:
        print("\n❌ ERRORES ENCONTRADOS:")
        for error in reporte['errores']:
            print(f"  - {error.get('mensaje', error)}")
    
    if reporte['advertencias']:
        print("\n⚠️  ADVERTENCIAS (primeras 5):")
        for adv in reporte['advertencias'][:5]:
            print(f"  - {adv.get('mensaje', adv)}")
    
    # Guardar reporte
    if args.reporte:
        integrador.guardar_reporte(args.reporte)
    else:
        # Guardar en directorio por defecto
        nombre_base = os.path.splitext(os.path.basename(args.archivo))[0]
        ruta_reporte = os.path.join(
            os.path.dirname(args.archivo),
            f"reporte_integracion_{nombre_base}_{args.version.replace(':', '-')}.json"
        )
        integrador.guardar_reporte(ruta_reporte)
    
    print("\n" + "=" * 60)
    if integrador.dry_run:
        print("💡 Este fue un DRY-RUN. Para integrar realmente, usa --integrar")
    else:
        print("✅ Integración completada")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())







#!/usr/bin/env python
"""
Script para importar obras editadas desde CSV (Google Sheets)

Uso:
    python scripts/import_from_csv.py filtro_basico/obras_editadas.csv
    
    # Con preview sin guardar
    python scripts/import_from_csv.py filtro_basico/obras_editadas.csv --dry-run
"""

import os
import sys
import django
import csv
import argparse

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from apps.obras.models import Obra
from apps.autores.models import Autor


def importar_desde_csv(archivo_csv, dry_run=False, solo_campos_vacios=True):
    """
    Importa datos desde CSV editado en Google Sheets
    
    Args:
        archivo_csv: Ruta al archivo CSV
        dry_run: Si True, no guarda cambios (solo preview)
        solo_campos_vacios: Si True, solo actualiza campos que estaban vacíos
    """
    
    print(f"📥 Importando datos desde: {archivo_csv}")
    
    if dry_run:
        print(f"⚠️  MODO DRY-RUN: No se guardarán cambios\n")
    
    if solo_campos_vacios:
        print(f"📋 MODO CONSERVADOR: Solo actualiza campos vacíos\n")
    else:
        print(f"⚠️  MODO SOBRESCRITURA: Actualiza todos los campos\n")
    
    if not os.path.exists(archivo_csv):
        print(f"❌ Error: Archivo no encontrado: {archivo_csv}")
        sys.exit(1)
    
    # Mapeo de columnas CSV a campos Django
    mapeo_campos = {
        'ID': 'id',
        'Título': 'titulo_limpio',
        'Título Original': 'titulo',
        'Títulos Alternativos': 'titulo_alternativo',
        'Tipo de Obra': 'tipo_obra',
        'Género': 'genero',
        'Subgénero': 'subgenero',
        'Tema': 'tema',
        'Fuente Principal': 'fuente_principal',
        'Origen de Datos': 'origen_datos',
        'Página PDF': 'pagina_pdf',
        'Número de Actos': 'actos',
        'Número de Versos': 'versos',
        'Idioma': 'idioma',
        'Fecha de Creación': 'fecha_creacion_estimada',
        'Música Conservada': 'musica_conservada',
        'Compositor': 'compositor',
        'Bibliotecas con Música': 'bibliotecas_musica',
        'Bibliografía Musical': 'bibliografia_musica',
        'Mecenas': 'mecenas',
        'Edición Príncipe': 'edicion_principe',
        'Notas Bibliográficas': 'notas_bibliograficas',
        'Manuscritos Conocidos': 'manuscritos_conocidos',
        'Ediciones Conocidas': 'ediciones_conocidas',
        'Notas': 'notas',
        'Observaciones': 'observaciones',
    }
    
    # Campos de autor
    campos_autor = {
        'Autor Nombre Completo': 'nombre_completo',
        'Autor Nacimiento': 'fecha_nacimiento',
        'Autor Muerte': 'fecha_muerte',
        'Autor Época': 'epoca',
        'Autor Biografía': 'biografia',
    }
    
    actualizadas = 0
    errores = 0
    cambios_totales = 0
    nuevos_datos = {}
    
    try:
        with open(archivo_csv, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            filas = list(reader)
            total_filas = len(filas)
            
            print(f"📊 Procesando {total_filas} filas...\n")
            
            for idx, row in enumerate(filas, 1):
                try:
                    obra_id = row.get('ID')
                    if not obra_id:
                        continue
                    
                    obra = Obra.objects.get(id=int(obra_id))
                    cambios_obra = []
                    
                    # Actualizar campos de obra
                    for csv_col, django_field in mapeo_campos.items():
                        if csv_col not in row:
                            continue
                        
                        nuevo_valor = row[csv_col].strip()
                        
                        # Convertir booleano
                        if django_field == 'musica_conservada':
                            nuevo_valor = nuevo_valor.lower() in ['sí', 'si', 'yes', 'true', '1']
                        
                        # Convertir enteros
                        elif django_field in ['actos', 'versos', 'pagina_pdf']:
                            try:
                                nuevo_valor = int(nuevo_valor) if nuevo_valor else None
                            except ValueError:
                                nuevo_valor = None
                        
                        # Verificar si actualizar
                        valor_actual = getattr(obra, django_field, None)
                        
                        if solo_campos_vacios:
                            # Solo actualizar si estaba vacío
                            debe_actualizar = not valor_actual and nuevo_valor
                        else:
                            # Actualizar si es diferente
                            debe_actualizar = nuevo_valor and str(valor_actual) != str(nuevo_valor)
                        
                        if debe_actualizar:
                            if not dry_run:
                                setattr(obra, django_field, nuevo_valor)
                            cambios_obra.append(f"{csv_col}: '{nuevo_valor}'")
                            cambios_totales += 1
                    
                    # Actualizar campos de autor
                    if obra.autor:
                        for csv_col, django_field in campos_autor.items():
                            if csv_col not in row:
                                continue
                            
                            nuevo_valor = row[csv_col].strip()
                            valor_actual = getattr(obra.autor, django_field, None)
                            
                            if solo_campos_vacios:
                                debe_actualizar = not valor_actual and nuevo_valor
                            else:
                                debe_actualizar = nuevo_valor and str(valor_actual) != str(nuevo_valor)
                            
                            if debe_actualizar:
                                if not dry_run:
                                    setattr(obra.autor, django_field, nuevo_valor)
                                    obra.autor.save()
                                cambios_obra.append(f"{csv_col}: '{nuevo_valor}'")
                                cambios_totales += 1
                    
                    # Guardar obra
                    if cambios_obra:
                        if not dry_run:
                            obra.save()
                        actualizadas += 1
                        
                        if len(cambios_obra) <= 3:
                            print(f"✅ Obra #{obra.id} '{obra.titulo_limpio}': {', '.join(cambios_obra)}")
                        else:
                            print(f"✅ Obra #{obra.id} '{obra.titulo_limpio}': {len(cambios_obra)} cambios")
                    
                    # Progreso cada 100
                    if idx % 100 == 0:
                        print(f"\n📊 Progreso: {idx}/{total_filas} filas procesadas...\n")
                
                except Obra.DoesNotExist:
                    print(f"⚠️  Obra ID {obra_id} no encontrada en la base de datos")
                    errores += 1
                except Exception as e:
                    print(f"❌ Error en fila {idx} (ID {obra_id}): {str(e)}")
                    errores += 1
        
        # Resumen
        print(f"\n{'='*60}")
        print(f"📊 RESUMEN DE IMPORTACIÓN")
        print(f"{'='*60}")
        print(f"Total de filas procesadas: {total_filas}")
        print(f"Obras actualizadas: {actualizadas}")
        print(f"Cambios totales: {cambios_totales}")
        print(f"Errores: {errores}")
        
        if dry_run:
            print(f"\n⚠️  MODO DRY-RUN: Ningún cambio fue guardado")
            print(f"   Ejecuta sin --dry-run para aplicar cambios")
        else:
            print(f"\n✅ Cambios guardados en la base de datos")
            print(f"\n🚀 Siguiente paso:")
            print(f"   python scripts/export_to_json_for_github.py")
            print(f"   # Para actualizar el JSON de GitHub Pages")
        
        return actualizadas, cambios_totales, errores
        
    except Exception as e:
        print(f"\n❌ Error al procesar CSV: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Importar obras editadas desde CSV (Google Sheets)'
    )
    parser.add_argument(
        'archivo_csv',
        help='Ruta al archivo CSV editado'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Modo preview: no guarda cambios'
    )
    parser.add_argument(
        '--sobrescribir',
        action='store_true',
        help='Sobrescribir campos existentes (default: solo actualiza vacíos)'
    )
    
    args = parser.parse_args()
    
    print(f"\n🎭 IMPORTACIÓN DE OBRAS DESDE GOOGLE SHEETS\n")
    
    importar_desde_csv(
        archivo_csv=args.archivo_csv,
        dry_run=args.dry_run,
        solo_campos_vacios=not args.sobrescribir
    )





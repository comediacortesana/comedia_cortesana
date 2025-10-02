#!/usr/bin/env python
"""
Script para importar datos de FUENTESXI desde la carpeta de backup
"""

import os
import sys
import django
import sqlite3
from datetime import datetime
from pathlib import Path

# Configurar Django
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from apps.obras.models import Obra, Manuscrito
from apps.representaciones.models import Representacion
from apps.autores.models import Autor
from apps.lugares.models import Lugar


def import_fuentesxi_from_backup():
    """Importa datos de la base SQLite de FUENTESXI desde backup"""
    
    # Ruta a la base de datos en backup
    backup_dir = Path(__file__).parent.parent / 'FUENTESXI_backup'
    db_path = backup_dir / 'teatro_espanol_mejorado.db'
    
    if not db_path.exists():
        print(f"Error: No se encontró la base de datos en {db_path}")
        return
    
    print(f"Importando datos de FUENTESXI desde {db_path}")
    
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Importar autores
        print("Importando autores...")
        cursor.execute("SELECT DISTINCT autor FROM obras WHERE autor IS NOT NULL AND autor != ''")
        autores_data = cursor.fetchall()
        
        autores_dict = {}
        for (autor_nombre,) in autores_data:
            if autor_nombre and autor_nombre.strip():
                autor, created = Autor.objects.get_or_create(
                    nombre=autor_nombre.strip(),
                    defaults={
                        'epoca': 'Siglo de Oro',
                        'notas': 'Importado desde FUENTESXI backup'
                    }
                )
                autores_dict[autor_nombre] = autor
                if created:
                    print(f"  Creado autor: {autor.nombre}")
        
        # Importar lugares
        print("Importando lugares...")
        cursor.execute("SELECT DISTINCT lugar FROM representaciones WHERE lugar IS NOT NULL AND lugar != ''")
        lugares_data = cursor.fetchall()
        
        lugares_dict = {}
        for (lugar_nombre,) in lugares_data:
            if lugar_nombre and lugar_nombre.strip():
                # Limpiar y normalizar el nombre del lugar
                lugar_nombre_limpio = lugar_nombre.strip()
                
                # Determinar tipo de lugar basado en el nombre
                tipo_lugar = 'otro'
                if 'palacio' in lugar_nombre_limpio.lower():
                    tipo_lugar = 'palacio'
                elif 'corral' in lugar_nombre_limpio.lower():
                    tipo_lugar = 'corral'
                elif 'buen retiro' in lugar_nombre_limpio.lower():
                    tipo_lugar = 'palacio'
                elif 'cuarto' in lugar_nombre_limpio.lower():
                    tipo_lugar = 'palacio'
                
                lugar, created = Lugar.objects.get_or_create(
                    nombre=lugar_nombre_limpio,
                    region='Madrid',  # La mayoría de lugares están en Madrid
                    defaults={
                        'pais': 'España',
                        'tipo_lugar': tipo_lugar,
                        'notas_historicas': 'Importado desde FUENTESXI backup'
                    }
                )
                lugares_dict[lugar_nombre] = lugar
                if created:
                    print(f"  Creado lugar: {lugar.nombre}")
        
        # Importar obras
        print("Importando obras...")
        cursor.execute("""
            SELECT id, titulo, titulo_limpio, titulo_alternativo, autor, tipo_obra, 
                   edicion_principe, notas_bibliograficas, mecenas, musica_conservada, 
                   compositor, fuente_principal, tema, genero
            FROM obras
        """)
        obras_data = cursor.fetchall()
        
        obras_dict = {}
        for obra_row in obras_data:
            (id_original, titulo, titulo_limpio, titulo_alternativo, autor_nombre, 
             tipo_obra, edicion_principe, notas_bibliograficas, mecenas, musica_conservada,
             compositor, fuente_principal, tema, genero) = obra_row
            
            # Obtener autor
            autor = autores_dict.get(autor_nombre) if autor_nombre else None
            
            # Crear obra
            obra, created = Obra.objects.get_or_create(
                titulo_limpio=titulo_limpio or titulo,
                defaults={
                    'titulo': titulo or '',
                    'titulo_alternativo': titulo_alternativo or '',
                    'autor': autor,
                    'tipo_obra': tipo_obra or 'comedia',
                    'genero': genero or '',
                    'edicion_principe': edicion_principe or '',
                    'notas_bibliograficas': notas_bibliograficas or '',
                    'fuente_principal': 'FUENTESXI',
                    'tema': tema or '',
                    'musica_conservada': bool(musica_conservada),
                    'compositor': compositor or '',
                    'mecenas': mecenas or ''
                }
            )
            obras_dict[id_original] = obra
            if created:
                print(f"  Creada obra: {obra.titulo_limpio}")
        
        # Importar representaciones
        print("Importando representaciones...")
        cursor.execute("""
            SELECT obra_id, fecha, lugar, fecha_formateada, compañia, 
                   observaciones, fuente
            FROM representaciones
        """)
        representaciones_data = cursor.fetchall()
        
        for rep_row in representaciones_data:
            (obra_id, fecha, lugar_nombre, fecha_formateada, compania,
             observaciones, fuente) = rep_row
            
            # Obtener obra y lugar
            obra = obras_dict.get(obra_id)
            lugar = lugares_dict.get(lugar_nombre) if lugar_nombre else None
            
            if obra and lugar:
                Representacion.objects.get_or_create(
                    obra=obra,
                    lugar=lugar,
                    fecha=fecha or '',
                    defaults={
                        'fecha_formateada': fecha_formateada or '',
                        'compañia': compania or '',
                        'observaciones': observaciones or '',
                        'fuente': fuente or 'FUENTESXI'
                    }
                )
        
        # Importar manuscritos
        print("Importando manuscritos...")
        cursor.execute("""
            SELECT obra_id, ubicacion, signatura, fecha_manuscrito, 
                   tipo_manuscrito, descripcion, notas
            FROM manuscritos
        """)
        manuscritos_data = cursor.fetchall()
        
        for ms_row in manuscritos_data:
            (obra_id, ubicacion, signatura, fecha_manuscrito,
             tipo_manuscrito, descripcion, notas) = ms_row
            
            obra = obras_dict.get(obra_id)
            if obra:
                Manuscrito.objects.get_or_create(
                    obra=obra,
                    ubicacion=ubicacion or '',
                    defaults={
                        'signatura': signatura or '',
                        'fecha_manuscrito': fecha_manuscrito or '',
                        'tipo_manuscrito': tipo_manuscrito or '',
                        'descripcion': descripcion or '',
                        'notas': notas or ''
                    }
                )
        
        conn.close()
        
        # Estadísticas finales
        print_stats()
        
    except Exception as e:
        print(f"Error durante la importación: {e}")
        conn.close()
        raise


def print_stats():
    """Imprime estadísticas de la importación"""
    print("\n" + "="*50)
    print("ESTADÍSTICAS DE IMPORTACIÓN - FUENTESXI")
    print("="*50)
    print(f"  Obras: {Obra.objects.filter(fuente_principal='FUENTESXI').count()}")
    print(f"  Autores: {Autor.objects.count()}")
    print(f"  Lugares: {Lugar.objects.count()}")
    print(f"  Representaciones: {Representacion.objects.filter(fuente='FUENTESXI').count()}")
    print(f"  Manuscritos: {Manuscrito.objects.count()}")


if __name__ == '__main__':
    import_fuentesxi_from_backup()

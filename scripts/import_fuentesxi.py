#!/usr/bin/env python
"""
Script para importar datos de FUENTESXI (base de datos SQLite) a Django
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


def import_fuentesxi_data():
    """Importa datos de la base SQLite de FUENTESXI"""
    
    # Ruta a la base de datos
    db_path = Path(__file__).parent.parent / 'data' / 'fuentesxi' / 'teatro_espanol_mejorado.db'
    
    if not db_path.exists():
        print(f"Error: No se encontró la base de datos en {db_path}")
        return
    
    print(f"Importando datos de {db_path}")
    
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
                        'notas': 'Importado desde FUENTESXI'
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
                lugar, created = Lugar.objects.get_or_create(
                    nombre=lugar_nombre.strip(),
                    defaults={
                        'pais': 'España',
                        'tipo_lugar': 'otro',
                        'notas_historicas': 'Importado desde FUENTESXI'
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
        for row in obras_data:
            obra_id, titulo, titulo_limpio, titulo_alternativo, autor, tipo_obra, \
            edicion_principe, notas_bibliograficas, mecenas, musica_conservada, \
            compositor, fuente_principal, tema, genero = row
            
            # Obtener autor
            autor_obj = None
            if autor and autor in autores_dict:
                autor_obj = autores_dict[autor]
            
            obra, created = Obra.objects.get_or_create(
                titulo_limpio=titulo_limpio,
                defaults={
                    'titulo': titulo or titulo_limpio,
                    'titulo_alternativo': titulo_alternativo or '',
                    'autor': autor_obj,
                    'tipo_obra': tipo_obra or 'comedia',
                    'edicion_principe': edicion_principe or '',
                    'notas_bibliograficas': notas_bibliograficas or '',
                    'mecenas': mecenas or '',
                    'musica_conservada': bool(musica_conservada),
                    'compositor': compositor or '',
                    'fuente_principal': 'FUENTESXI',
                    'tema': tema or '',
                    'genero': genero or '',
                    'idioma': 'Español'
                }
            )
            obras_dict[obra_id] = obra
            if created:
                print(f"  Creada obra: {obra.titulo_limpio}")
        
        # Importar representaciones
        print("Importando representaciones...")
        cursor.execute("""
            SELECT obra_id, fecha, fecha_formateada, compañia, lugar, tipo_lugar,
                   fuente, observaciones, mecenas, gestor_administrativo
            FROM representaciones
        """)
        representaciones_data = cursor.fetchall()
        
        for row in representaciones_data:
            obra_id, fecha, fecha_formateada, compañia, lugar, tipo_lugar, \
            fuente, observaciones, mecenas, gestor_administrativo = row
            
            if obra_id not in obras_dict:
                continue
            
            obra = obras_dict[obra_id]
            
            # Obtener lugar
            lugar_obj = None
            if lugar and lugar in lugares_dict:
                lugar_obj = lugares_dict[lugar]
            
            # Parsear fecha formateada
            fecha_obj = None
            if fecha_formateada:
                try:
                    fecha_obj = datetime.strptime(fecha_formateada, '%d/%m/%Y').date()
                except ValueError:
                    try:
                        fecha_obj = datetime.strptime(fecha_formateada, '%Y-%m-%d').date()
                    except ValueError:
                        pass
            
            Representacion.objects.get_or_create(
                obra=obra,
                fecha=fecha or '',
                fecha_formateada=fecha_obj,
                compañia=compañia or '',
                lugar=lugar_obj,
                tipo_lugar=tipo_lugar or '',
                fuente=fuente or '',
                observaciones=observaciones or '',
                mecenas=mecenas or '',
                gestor_administrativo=gestor_administrativo or ''
            )
        
        # Importar manuscritos
        print("Importando manuscritos...")
        cursor.execute("SELECT obra_id, ubicacion FROM manuscritos")
        manuscritos_data = cursor.fetchall()
        
        for obra_id, ubicacion in manuscritos_data:
            if obra_id not in obras_dict:
                continue
            
            obra = obras_dict[obra_id]
            
            Manuscrito.objects.get_or_create(
                obra=obra,
                ubicacion=ubicacion or ''
            )
        
        print("Importación completada exitosamente!")
        
        # Estadísticas
        print(f"\nEstadísticas de importación:")
        print(f"  Autores: {Autor.objects.count()}")
        print(f"  Lugares: {Lugar.objects.count()}")
        print(f"  Obras: {Obra.objects.count()}")
        print(f"  Representaciones: {Representacion.objects.count()}")
        print(f"  Manuscritos: {Manuscrito.objects.count()}")
        
    except Exception as e:
        print(f"Error durante la importación: {e}")
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    import_fuentesxi_data()

#!/usr/bin/env python
"""
Script para exportar obras a CSV para Google Sheets

Uso:
    python scripts/export_to_csv.py
    
El archivo se guardará en: filtro_basico/obras_completas.csv
"""

import os
import sys
import django
import csv
from datetime import datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from apps.obras.models import Obra


def exportar_a_csv(max_obras=None, incluir_textos_largos=False):
    """
    Exporta obras a formato CSV para Google Sheets
    
    Args:
        max_obras: Límite de obras (None = todas)
        incluir_textos_largos: Si incluir texto_original_pdf (puede ser muy largo)
    """
    
    print(f"📊 Exportando obras a CSV para Google Sheets...")
    if max_obras:
        print(f"📦 Límite: {max_obras} obras")
    else:
        print(f"📦 Exportando TODAS las obras")
    
    # Obtener obras
    obras_query = Obra.objects.select_related('autor').order_by('titulo_limpio')
    if max_obras:
        obras = obras_query[:max_obras]
    else:
        obras = obras_query
    
    total = obras.count()
    print(f"✅ {total} obras para exportar\n")
    
    # Definir columnas
    columnas = [
        # Información básica
        ('id', 'ID'),
        ('titulo_limpio', 'Título'),
        ('titulo', 'Título Original'),
        ('titulo_alternativo', 'Títulos Alternativos'),
        
        # Autor
        ('autor__nombre', 'Autor'),
        ('autor__nombre_completo', 'Autor Nombre Completo'),
        ('autor__fecha_nacimiento', 'Autor Nacimiento'),
        ('autor__fecha_muerte', 'Autor Muerte'),
        ('autor__epoca', 'Autor Época'),
        ('autor__biografia', 'Autor Biografía'),
        
        # Clasificación
        ('tipo_obra', 'Tipo de Obra'),
        ('genero', 'Género'),
        ('subgenero', 'Subgénero'),
        ('tema', 'Tema'),
        
        # Fuentes y origen
        ('fuente_principal', 'Fuente Principal'),
        ('origen_datos', 'Origen de Datos'),
        ('pagina_pdf', 'Página PDF'),
        
        # Estructura
        ('actos', 'Número de Actos'),
        ('versos', 'Número de Versos'),
        ('idioma', 'Idioma'),
        
        # Fechas
        ('fecha_creacion_estimada', 'Fecha de Creación'),
        
        # Música
        ('musica_conservada', 'Música Conservada'),
        ('compositor', 'Compositor'),
        ('bibliotecas_musica', 'Bibliotecas con Música'),
        ('bibliografia_musica', 'Bibliografía Musical'),
        
        # Mecenazgo
        ('mecenas', 'Mecenas'),
        
        # Bibliografía e historia textual
        ('edicion_principe', 'Edición Príncipe'),
        ('notas_bibliograficas', 'Notas Bibliográficas'),
        ('manuscritos_conocidos', 'Manuscritos Conocidos'),
        ('ediciones_conocidas', 'Ediciones Conocidas'),
        
        # Notas
        ('notas', 'Notas'),
        ('observaciones', 'Observaciones'),
    ]
    
    if incluir_textos_largos:
        columnas.append(('texto_original_pdf', 'Texto Original PDF'))
    
    # Ruta de salida
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'filtro_basico',
        'obras_completas.csv'
    )
    
    # Escribir CSV
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        # Usar utf-8-sig para que Excel/Sheets reconozca los acentos
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        
        # Encabezados
        encabezados = [col[1] for col in columnas]
        writer.writerow(encabezados)
        
        # Datos
        for i, obra in enumerate(obras, 1):
            fila = []
            
            for campo_db, _ in columnas:
                # Manejar campos de autor (con __)
                if '__' in campo_db:
                    partes = campo_db.split('__')
                    if partes[0] == 'autor' and obra.autor:
                        valor = getattr(obra.autor, partes[1], '')
                    else:
                        valor = ''
                # Campo booleano
                elif campo_db == 'musica_conservada':
                    valor = 'Sí' if obra.musica_conservada else 'No'
                # Campo normal
                else:
                    valor = getattr(obra, campo_db, '')
                
                # Convertir None a string vacío
                if valor is None:
                    valor = ''
                
                fila.append(valor)
            
            writer.writerow(fila)
            
            # Progreso
            if i % 100 == 0:
                print(f"  📝 Procesadas {i}/{total} obras...")
    
    print(f"\n✅ Exportación CSV completada!")
    print(f"📁 Archivo: {output_path}")
    print(f"📦 Tamaño: {os.path.getsize(output_path) / 1024:.2f} KB")
    print(f"📊 Obras exportadas: {total}")
    print(f"📋 Columnas: {len(columnas)}")
    
    print(f"\n🚀 Siguiente paso:")
    print(f"   1. Abre Google Sheets")
    print(f"   2. Archivo → Importar → Cargar")
    print(f"   3. Selecciona: obras_completas.csv")
    print(f"   4. Edita colaborativamente")
    print(f"   5. Archivo → Descargar → CSV")
    print(f"   6. Importa de vuelta a Django")
    
    return output_path


def crear_csv_con_representaciones():
    """Crea CSV expandido con una fila por representación"""
    
    print(f"\n📊 OPCIÓN 2: CSV con representaciones expandidas")
    print(f"(Una fila por cada representación de cada obra)\n")
    
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'filtro_basico',
        'obras_con_representaciones.csv'
    )
    
    # Encabezados combinados
    encabezados = [
        # Obra
        'ID Obra', 'Título', 'Autor', 'Tipo', 'Fuente',
        # Representación
        'ID Rep', 'Fecha Rep', 'Lugar', 'Región', 'Compañía', 
        'Director', 'Mecenas Rep', 'Tipo Función', 'Público'
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(encabezados)
        
        obras = Obra.objects.select_related('autor').prefetch_related('representaciones__lugar')
        total_filas = 0
        
        for obra in obras:
            reps = obra.representaciones.all()
            
            if reps.exists():
                for rep in reps:
                    writer.writerow([
                        obra.id,
                        obra.titulo_limpio,
                        obra.autor.nombre if obra.autor else 'Anónimo',
                        obra.tipo_obra,
                        obra.fuente_principal,
                        rep.id,
                        rep.fecha,
                        rep.lugar.nombre if rep.lugar else '',
                        rep.lugar.region if rep.lugar else '',
                        rep.compañia,
                        rep.director_compañia,
                        rep.mecenas,
                        rep.tipo_funcion,
                        rep.publico
                    ])
                    total_filas += 1
            else:
                # Obra sin representaciones
                writer.writerow([
                    obra.id,
                    obra.titulo_limpio,
                    obra.autor.nombre if obra.autor else 'Anónimo',
                    obra.tipo_obra,
                    obra.fuente_principal,
                    '', '', '', '', '', '', '', '', ''
                ])
                total_filas += 1
    
    print(f"✅ CSV con representaciones creado!")
    print(f"📁 Archivo: {output_path}")
    print(f"📊 Filas totales: {total_filas}")
    
    return output_path


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Exportar obras a CSV')
    parser.add_argument('--max', type=int, help='Máximo de obras (default: todas)')
    parser.add_argument('--con-textos', action='store_true', help='Incluir texto_original_pdf')
    parser.add_argument('--con-reps', action='store_true', help='Crear CSV expandido con representaciones')
    
    args = parser.parse_args()
    
    try:
        # CSV principal
        output = exportar_a_csv(
            max_obras=args.max,
            incluir_textos_largos=args.con_textos
        )
        
        # CSV con representaciones (opcional)
        if args.con_reps:
            output2 = crear_csv_con_representaciones()
        
        print(f"\n🎉 ¡Proceso completado!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)





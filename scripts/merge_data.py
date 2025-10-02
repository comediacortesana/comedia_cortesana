#!/usr/bin/env python
"""
Script para fusionar y deduplicar datos de FUENTESXI y CATCOM
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from apps.obras.models import Obra
from apps.autores.models import Autor
from apps.lugares.models import Lugar
from django.db.models import Q
from difflib import SequenceMatcher


def similarity(a, b):
    """Calcula la similitud entre dos strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def merge_obras():
    """Fusiona obras duplicadas entre FUENTESXI y CATCOM"""
    
    print("Fusionando obras duplicadas...")
    
    # Buscar obras potencialmente duplicadas
    obras = Obra.objects.all()
    merged_count = 0
    
    for obra in obras:
        if obra.fuente_principal != 'AMBAS':
            # Buscar obras similares
            titulo_limpio = obra.titulo_limpio.lower()
            
            # Buscar por título similar
            obras_similares = Obra.objects.filter(
                Q(titulo_limpio__icontains=titulo_limpio[:20]) |
                Q(titulo_limpio__icontains=titulo_limpio[-20:])
            ).exclude(id=obra.id)
            
            for obra_similar in obras_similares:
                sim = similarity(obra.titulo_limpio, obra_similar.titulo_limpio)
                
                if sim > 0.8:  # 80% de similitud
                    print(f"  Fusionando: '{obra.titulo_limpio}' con '{obra_similar.titulo_limpio}' (similitud: {sim:.2f})")
                    
                    # Fusionar datos
                    if obra.fuente_principal == 'FUENTESXI' and obra_similar.fuente_principal == 'CATCOM':
                        # Mantener obra de FUENTESXI como principal
                        obra_principal = obra
                        obra_secundaria = obra_similar
                    elif obra.fuente_principal == 'CATCOM' and obra_similar.fuente_principal == 'FUENTESXI':
                        # Mantener obra de FUENTESXI como principal
                        obra_principal = obra_similar
                        obra_secundaria = obra
                    else:
                        # Mantener la más completa
                        if obra.representaciones.count() >= obra_similar.representaciones.count():
                            obra_principal = obra
                            obra_secundaria = obra_similar
                        else:
                            obra_principal = obra_similar
                            obra_secundaria = obra
                    
                    # Actualizar obra principal
                    obra_principal.fuente_principal = 'AMBAS'
                    
                    # Fusionar campos vacíos
                    if not obra_principal.autor and obra_secundaria.autor:
                        obra_principal.autor = obra_secundaria.autor
                    
                    if not obra_principal.tema and obra_secundaria.tema:
                        obra_principal.tema = obra_secundaria.tema
                    
                    if not obra_principal.genero and obra_secundaria.genero:
                        obra_principal.genero = obra_secundaria.genero
                    
                    if not obra_principal.notas_bibliograficas and obra_secundaria.notas_bibliograficas:
                        obra_principal.notas_bibliograficas = obra_secundaria.notas_bibliograficas
                    
                    obra_principal.save()
                    
                    # Mover representaciones
                    for rep in obra_secundaria.representaciones.all():
                        rep.obra = obra_principal
                        rep.save()
                    
                    # Mover manuscritos
                    for manuscrito in obra_secundaria.manuscritos.all():
                        manuscrito.obra = obra_principal
                        manuscrito.save()
                    
                    # Mover referencias bibliográficas
                    for ref in obra_secundaria.referencias_bibliograficas.all():
                        ref.obra = obra_principal
                        ref.save()
                    
                    # Eliminar obra duplicada
                    obra_secundaria.delete()
                    merged_count += 1
                    break
    
    print(f"Fusionadas {merged_count} obras duplicadas")


def merge_autores():
    """Fusiona autores duplicados"""
    
    print("Fusionando autores duplicados...")
    
    autores = Autor.objects.all()
    merged_count = 0
    
    for autor in autores:
        # Buscar autores similares
        nombre_limpio = autor.nombre.lower()
        
        autores_similares = Autor.objects.filter(
            nombre__icontains=nombre_limpio[:10]
        ).exclude(id=autor.id)
        
        for autor_similar in autores_similares:
            sim = similarity(autor.nombre, autor_similar.nombre)
            
            if sim > 0.9:  # 90% de similitud para autores
                print(f"  Fusionando autor: '{autor.nombre}' con '{autor_similar.nombre}' (similitud: {sim:.2f})")
                
                # Mantener el autor con más obras
                if autor.obras.count() >= autor_similar.obras.count():
                    autor_principal = autor
                    autor_secundario = autor_similar
                else:
                    autor_principal = autor_similar
                    autor_secundario = autor
                
                # Fusionar campos
                if not autor_principal.biografia and autor_secundario.biografia:
                    autor_principal.biografia = autor_secundario.biografia
                
                if not autor_principal.epoca and autor_secundario.epoca:
                    autor_principal.epoca = autor_secundario.epoca
                
                autor_principal.save()
                
                # Mover obras
                for obra in autor_secundario.obras.all():
                    obra.autor = autor_principal
                    obra.save()
                
                # Eliminar autor duplicado
                autor_secundario.delete()
                merged_count += 1
                break
    
    print(f"Fusionados {merged_count} autores duplicados")


def merge_lugares():
    """Fusiona lugares duplicados"""
    
    print("Fusionando lugares duplicados...")
    
    lugares = Lugar.objects.all()
    merged_count = 0
    
    for lugar in lugares:
        # Buscar lugares similares
        nombre_limpio = lugar.nombre.lower()
        
        lugares_similares = Lugar.objects.filter(
            nombre__icontains=nombre_limpio[:10]
        ).exclude(id=lugar.id)
        
        for lugar_similar in lugares_similares:
            sim = similarity(lugar.nombre, lugar_similar.nombre)
            
            if sim > 0.9:  # 90% de similitud para lugares
                print(f"  Fusionando lugar: '{lugar.nombre}' con '{lugar_similar.nombre}' (similitud: {sim:.2f})")
                
                # Mantener el lugar con más representaciones
                if lugar.representaciones.count() >= lugar_similar.representaciones.count():
                    lugar_principal = lugar
                    lugar_secundario = lugar_similar
                else:
                    lugar_principal = lugar_similar
                    lugar_secundario = lugar
                
                # Fusionar campos
                if not lugar_principal.coordenadas_lat and lugar_secundario.coordenadas_lat:
                    lugar_principal.coordenadas_lat = lugar_secundario.coordenadas_lat
                
                if not lugar_principal.coordenadas_lng and lugar_secundario.coordenadas_lng:
                    lugar_principal.coordenadas_lng = lugar_secundario.coordenadas_lng
                
                if not lugar_principal.region and lugar_secundario.region:
                    lugar_principal.region = lugar_secundario.region
                
                if not lugar_principal.descripcion and lugar_secundario.descripcion:
                    lugar_principal.descripcion = lugar_secundario.descripcion
                
                lugar_principal.save()
                
                # Mover representaciones
                for rep in lugar_secundario.representaciones.all():
                    rep.lugar = lugar_principal
                    rep.save()
                
                # Eliminar lugar duplicado
                lugar_secundario.delete()
                merged_count += 1
                break
    
    print(f"Fusionados {merged_count} lugares duplicados")


def main():
    """Función principal para fusionar datos"""
    
    print("Iniciando proceso de fusión de datos...")
    
    # Fusionar en orden: autores, lugares, obras
    merge_autores()
    merge_lugares()
    merge_obras()
    
    print("\nProceso de fusión completado!")
    
    # Estadísticas finales
    print(f"\nEstadísticas finales:")
    print(f"  Autores: {Autor.objects.count()}")
    print(f"  Lugares: {Lugar.objects.count()}")
    print(f"  Obras: {Obra.objects.count()}")
    print(f"  Obras con ambas fuentes: {Obra.objects.filter(fuente_principal='AMBAS').count()}")


if __name__ == '__main__':
    main()

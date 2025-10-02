#!/usr/bin/env python
"""
Script para actualizar los campos de época (es_anterior_1650, es_anterior_1665) 
en las representaciones existentes.

Este script calcula automáticamente estos campos basándose en la fecha_formateada
de cada representación.
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from apps.representaciones.models import Representacion
from django.db import transaction


def update_epoca_fields():
    """Actualiza los campos de época para todas las representaciones"""
    
    print("🔄 Iniciando actualización de campos de época...")
    
    # Obtener todas las representaciones con fecha formateada
    representaciones = Representacion.objects.filter(
        fecha_formateada__isnull=False
    ).select_related('obra')
    
    total = representaciones.count()
    print(f"📊 Total de representaciones a procesar: {total}")
    
    if total == 0:
        print("⚠️  No hay representaciones con fecha formateada para procesar.")
        return
    
    # Contadores para estadísticas
    anterior_1650 = 0
    anterior_1665 = 0
    actualizadas = 0
    
    # Procesar en lotes para mejor rendimiento
    batch_size = 100
    
    with transaction.atomic():
        for i in range(0, total, batch_size):
            batch = representaciones[i:i + batch_size]
            
            for rep in batch:
                if rep.fecha_formateada:
                    year = rep.fecha_formateada.year
                    
                    # Calcular campos de época
                    es_anterior_1650 = year < 1650
                    es_anterior_1665 = year < 1665
                    
                    # Actualizar solo si han cambiado
                    if (rep.es_anterior_1650 != es_anterior_1650 or 
                        rep.es_anterior_1665 != es_anterior_1665):
                        
                        rep.es_anterior_1650 = es_anterior_1650
                        rep.es_anterior_1665 = es_anterior_1665
                        rep.save(update_fields=['es_anterior_1650', 'es_anterior_1665'])
                        actualizadas += 1
                    
                    # Estadísticas
                    if es_anterior_1650:
                        anterior_1650 += 1
                    if es_anterior_1665:
                        anterior_1665 += 1
            
            # Mostrar progreso
            processed = min(i + batch_size, total)
            print(f"📈 Progreso: {processed}/{total} ({processed/total*100:.1f}%)")
    
    # Mostrar resultados
    print("\n✅ Actualización completada!")
    print(f"📊 Estadísticas:")
    print(f"   - Representaciones actualizadas: {actualizadas}")
    print(f"   - Representaciones anteriores a 1650: {anterior_1650}")
    print(f"   - Representaciones anteriores a 1665: {anterior_1665}")
    print(f"   - Total procesadas: {total}")


def show_statistics():
    """Muestra estadísticas de los campos de época"""
    
    print("\n📊 Estadísticas actuales de campos de época:")
    
    total = Representacion.objects.count()
    con_fecha = Representacion.objects.filter(fecha_formateada__isnull=False).count()
    anterior_1650 = Representacion.objects.filter(es_anterior_1650=True).count()
    anterior_1665 = Representacion.objects.filter(es_anterior_1665=True).count()
    
    print(f"   - Total de representaciones: {total}")
    print(f"   - Con fecha formateada: {con_fecha}")
    print(f"   - Anteriores a 1650: {anterior_1650}")
    print(f"   - Anteriores a 1665: {anterior_1665}")
    
    if con_fecha > 0:
        print(f"   - Porcentaje anteriores a 1650: {anterior_1650/con_fecha*100:.1f}%")
        print(f"   - Porcentaje anteriores a 1665: {anterior_1665/con_fecha*100:.1f}%")


if __name__ == "__main__":
    print("🎭 Script de actualización de campos de época")
    print("=" * 50)
    
    # Mostrar estadísticas antes
    show_statistics()
    
    # Preguntar si continuar
    response = input("\n¿Deseas actualizar los campos de época? (s/N): ").strip().lower()
    
    if response in ['s', 'sí', 'si', 'y', 'yes']:
        update_epoca_fields()
        show_statistics()
    else:
        print("❌ Operación cancelada.")
    
    print("\n🏁 Script finalizado.")

#!/usr/bin/env python
"""
Script para crear comentarios de prueba en el sistema
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from apps.usuarios.models import Usuario
from apps.obras.models import Obra, ComentarioUsuario
from django.utils import timezone

def create_test_comments():
    """Crear comentarios de prueba"""
    
    print("🎭 Creando comentarios de prueba...")
    
    # Obtener usuarios
    try:
        usuario1 = Usuario.objects.get(username='test1')
    except Usuario.DoesNotExist:
        print("⚠️ Usuario 'test1' no encontrado. Creándolo...")
        usuario1 = Usuario.objects.create_user(
            username='test1',
            email='test1@example.com',
            password='123',
            first_name='Usuario',
            last_name='Test'
        )
    
    try:
        usuario2 = Usuario.objects.get(username='investigador')
    except Usuario.DoesNotExist:
        print("⚠️ Usuario 'investigador' no encontrado. Creándolo...")
        usuario2 = Usuario.objects.create_user(
            username='investigador',
            email='investigador@example.com',
            password='abc',
            first_name='María',
            last_name='Investigadora'
        )
    
    # Obtener algunas obras para asociar
    obras = Obra.objects.all()[:5]
    
    if not obras:
        print("❌ No hay obras en la base de datos. Por favor, importa datos primero.")
        return
    
    # Comentario 1
    comentario1, created = ComentarioUsuario.objects.get_or_create(
        usuario=usuario1,
        catalogo='fuentesxi',
        titulo='Descubrimiento sobre comedias del Siglo de Oro',
        defaults={
            'comentario': 'He encontrado una conexión interesante entre las obras de Calderón y Lope de Vega en el periodo 1630-1640. Ambos autores parecen haber compartido temas similares sobre el honor y la venganza, lo cual sugiere una influencia mutua o una respuesta a las demandas del público de la época.',
            'es_publico': True
        }
    )
    if created:
        comentario1.obras_seleccionadas.set(obras[:3])
        print(f"✅ Comentario 1 creado: {comentario1.titulo}")
    else:
        print(f"ℹ️ Comentario 1 ya existe: {comentario1.titulo}")
    
    # Comentario 2
    comentario2, created = ComentarioUsuario.objects.get_or_create(
        usuario=usuario2,
        catalogo='catcom',
        titulo='Análisis de representaciones en Madrid',
        defaults={
            'comentario': 'Las representaciones en el Corral del Príncipe durante 1650 muestran una preferencia notable por las comedias de capa y espada. He identificado 15 obras que comparten esta característica y que tuvieron más de 10 representaciones cada una.',
            'es_publico': True
        }
    )
    if created:
        comentario2.obras_seleccionadas.set(obras[1:4])
        print(f"✅ Comentario 2 creado: {comentario2.titulo}")
    else:
        print(f"ℹ️ Comentario 2 ya existe: {comentario2.titulo}")
    
    # Comentario 3
    comentario3, created = ComentarioUsuario.objects.get_or_create(
        usuario=usuario1,
        catalogo='fuentesxi',
        titulo='Música en el teatro barroco',
        defaults={
            'comentario': 'Investigando las obras con música conservada, he notado que las zarzuelas del periodo 1680-1700 incluyen frecuentemente referencias a danzas cortesanas. Esto podría indicar una influencia de la música de la corte en el teatro popular.',
            'es_publico': True
        }
    )
    if created:
        comentario3.obras_seleccionadas.set(obras[2:5])
        print(f"✅ Comentario 3 creado: {comentario3.titulo}")
    else:
        print(f"ℹ️ Comentario 3 ya existe: {comentario3.titulo}")
    
    # Comentario 4 - más reciente
    comentario4, created = ComentarioUsuario.objects.get_or_create(
        usuario=usuario2,
        catalogo='catcom',
        titulo='Patrones en autores del Siglo de Oro',
        defaults={
            'comentario': 'Estoy trabajando en un análisis comparativo de los patrones narrativos en obras de diferentes autores. He encontrado que ciertos temas mitológicos se repiten con frecuencia, especialmente las referencias a dioses greco-romanos.',
            'es_publico': True
        }
    )
    if created:
        comentario4.obras_seleccionadas.set(obras[:2])
        print(f"✅ Comentario 4 creado: {comentario4.titulo}")
    else:
        print(f"ℹ️ Comentario 4 ya existe: {comentario4.titulo}")
    
    print("\n✨ Comentarios de prueba creados exitosamente!")
    print(f"📊 Total de comentarios públicos: {ComentarioUsuario.objects.filter(es_publico=True).count()}")
    print("\n💡 Ahora puedes ver los comentarios en la página principal: http://127.0.0.1:8000/")

if __name__ == '__main__':
    create_test_comments()






#!/usr/bin/env python
"""
Script para actualizar comentarios existentes con obras específicas
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from apps.obras.models import Obra, ComentarioUsuario

def update_comments_with_works():
    """Actualizar comentarios con obras específicas"""
    
    print("🎭 Actualizando comentarios con obras específicas...")
    
    # Obtener algunas obras específicas para asociar
    obras = Obra.objects.all()[:10]
    
    if not obras:
        print("❌ No hay obras en la base de datos.")
        return
    
    # Obtener todos los comentarios
    comentarios = ComentarioUsuario.objects.all()
    
    if not comentarios.exists():
        print("❌ No hay comentarios para actualizar.")
        return
    
    print(f"📚 Encontradas {obras.count()} obras para asociar")
    print(f"💬 Encontrados {comentarios.count()} comentarios")
    
    # Actualizar cada comentario con obras diferentes
    for i, comentario in enumerate(comentarios):
        # Asociar 2-4 obras diferentes a cada comentario
        start_idx = i * 2
        end_idx = min(start_idx + (i % 3) + 2, obras.count())
        obras_para_comentario = obras[start_idx:end_idx]
        
        if obras_para_comentario:
            comentario.obras_seleccionadas.set(obras_para_comentario)
            print(f"✅ Comentario '{comentario.titulo}' actualizado con {len(obras_para_comentario)} obras:")
            for obra in obras_para_comentario:
                print(f"   - {obra.titulo_limpio or obra.titulo} (ID: {obra.id})")
    
    print(f"\n✨ Todos los comentarios actualizados!")
    print(f"📊 Total de comentarios públicos: {ComentarioUsuario.objects.filter(es_publico=True).count()}")
    print("\n💡 Ahora puedes ver los enlaces a obras en: http://127.0.0.1:8000/")

if __name__ == '__main__':
    update_comments_with_works()

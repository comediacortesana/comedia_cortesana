#!/usr/bin/env python
"""
Script para exportar datos de Django a JSON para GitHub Pages

Uso:
    python scripts/export_to_json_for_github.py
    
El archivo se guardará en: filtro_basico/datos_obras.json
"""

import os
import sys
import django
from datetime import datetime
import json

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from apps.obras.models import Obra
from apps.autores.models import Autor
from apps.lugares.models import Lugar
from apps.representaciones.models import Representacion


def exportar_obras_a_json(max_obras=None):
    """
    Exporta obras de Django a formato JSON para GitHub Pages
    
    Args:
        max_obras: Número máximo de obras a exportar (default: None = todas)
    """
    
    print(f"🎭 Exportando obras del teatro español...")
    if max_obras:
        print(f"📊 Límite: {max_obras} obras\n")
    else:
        print(f"📊 Exportando TODAS las obras\n")
    
    # Obtener obras con relaciones
    obras_query = Obra.objects.select_related('autor').prefetch_related(
        'representaciones__lugar'
    ).order_by('titulo_limpio')
    
    if max_obras:
        obras = obras_query[:max_obras]
    else:
        obras = obras_query
    
    total_obras = obras.count()
    print(f"✅ Encontradas {total_obras} obras")
    
    # Preparar datos
    data = {
        "metadata": {
            "version": "1.0",
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d"),
            "fecha_completa": datetime.now().isoformat(),
            "total_obras": total_obras,
            "fuentes": list(set(obra.fuente_principal for obra in obras if obra.fuente_principal)),
            "descripcion": "Obras del teatro español del Siglo de Oro - Base de datos DELIA"
        },
        "obras": []
    }
    
    # Procesar cada obra
    for i, obra in enumerate(obras, 1):
        # Obtener primera representación para datos de contexto
        primera_rep = obra.representaciones.first()
        
        # Datos de autor completos
        autor_data = {}
        if obra.autor:
            autor_data = {
                "nombre": obra.autor.nombre,
                "nombre_completo": obra.autor.nombre_completo or "",
                "fecha_nacimiento": obra.autor.fecha_nacimiento or "",
                "fecha_muerte": obra.autor.fecha_muerte or "",
                "biografia": obra.autor.biografia or "",
                "epoca": obra.autor.epoca or "Siglo de Oro"
            }
        else:
            autor_data = {
                "nombre": "Anónimo",
                "nombre_completo": "",
                "fecha_nacimiento": "",
                "fecha_muerte": "",
                "biografia": "",
                "epoca": "Siglo de Oro"
            }
        
        obra_data = {
            "id": obra.id,
            # Títulos
            "titulo": obra.titulo_limpio or obra.titulo,
            "titulo_original": obra.titulo,
            "titulo_alternativo": obra.titulo_alternativo or "",
            
            # Autor (datos completos)
            "autor": autor_data,
            
            # Clasificación
            "tipo_obra": obra.tipo_obra or "otro",
            "genero": obra.genero or "",
            "subgenero": obra.subgenero or "",
            
            # Fuentes y origen
            "fuente": obra.fuente_principal or "FUENTESXI",
            "origen_datos": obra.origen_datos or "web",
            "pagina_pdf": obra.pagina_pdf,
            "texto_original_pdf": obra.texto_original_pdf or "",
            
            # Fechas y tema
            "fecha_creacion": obra.fecha_creacion_estimada or "",
            "tema": obra.tema or "",
            
            # Estructura
            "actos": obra.actos,
            "versos": obra.versos,
            "idioma": obra.idioma,
            
            # Música
            "musica_conservada": obra.musica_conservada,
            "compositor": obra.compositor or "",
            "bibliotecas_musica": obra.bibliotecas_musica or "",
            "bibliografia_musica": obra.bibliografia_musica or "",
            
            # Mecenazgo
            "mecenas": obra.mecenas or "",
            
            # Bibliografía y ediciones
            "edicion_principe": obra.edicion_principe or "",
            "notas_bibliograficas": obra.notas_bibliograficas or "",
            "manuscritos_conocidos": obra.manuscritos_conocidos or "",
            "ediciones_conocidas": obra.ediciones_conocidas or "",
            
            # Notas y observaciones
            "notas": obra.notas or "",
            "observaciones": obra.observaciones or "",
            
            # Estadísticas
            "total_representaciones": obra.representaciones.count(),
        }
        
        # Añadir información de representaciones (todas, no solo la primera) - COMPLETO
        representaciones_list = []
        for rep in obra.representaciones.all():
            rep_data = {
                # Fechas
                "fecha": rep.fecha,
                "fecha_formateada": rep.fecha_formateada.isoformat() if rep.fecha_formateada else "",
                
                # Lugar
                "lugar": rep.lugar.nombre if rep.lugar else "",
                "region": rep.lugar.region if rep.lugar else "",
                "pais": rep.lugar.pais if rep.lugar else "",
                "tipo_lugar": rep.tipo_lugar or "",
                
                # Compañía
                "compania": rep.compañia or "",
                "director_compañia": rep.director_compañia or "",
                
                # Mecenazgo y gestión
                "mecenas": rep.mecenas or "",
                "gestor_administrativo": rep.gestor_administrativo or "",
                
                # Personajes y organizadores
                "personajes_historicos": rep.personajes_historicos or "",
                "organizadores_fiesta": rep.organizadores_fiesta or "",
                
                # Tipo de función
                "tipo_funcion": rep.tipo_funcion or "",
                "publico": rep.publico or "",
                "entrada": rep.entrada or "",
                "duracion": rep.duracion or "",
                
                # Notas y fuentes
                "observaciones": rep.observaciones or "",
                "notas": rep.notas or "",
                "fuente": rep.fuente or "",
                
                # PDF
                "pagina_pdf": rep.pagina_pdf,
                "texto_original_pdf": rep.texto_original_pdf or "",
                
                # Época
                "es_anterior_1650": rep.es_anterior_1650,
                "es_anterior_1665": rep.es_anterior_1665,
            }
            representaciones_list.append(rep_data)
        
        obra_data["representaciones"] = representaciones_list
        
        # Datos legacy para compatibilidad (primera representación)
        if primera_rep:
            obra_data.update({
                "lugar": primera_rep.lugar.nombre if primera_rep.lugar else "",
                "tipo_lugar": primera_rep.tipo_lugar or "",
                "region": primera_rep.lugar.region if primera_rep.lugar else "",
                "compania": primera_rep.compañia or "",
                "director_compañia": primera_rep.director_compañia or "",
            })
        else:
            obra_data.update({
                "lugar": "",
                "tipo_lugar": "",
                "region": "",
                "compania": "",
                "director_compañia": "",
            })
        
        data["obras"].append(obra_data)
        
        # Mostrar progreso
        if i % 10 == 0:
            print(f"  📝 Procesadas {i}/{total_obras} obras...")
    
    # Guardar archivo
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'filtro_basico',
        'datos_obras.json'
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Exportación completada!")
    print(f"📁 Archivo guardado en: {output_path}")
    print(f"📦 Tamaño: {os.path.getsize(output_path) / 1024:.2f} KB")
    print(f"\n🚀 Siguiente paso:")
    print(f"   cd filtro_basico")
    print(f"   git add datos_obras.json")
    print(f"   git commit -m 'Actualizar datos con {total_obras} obras'")
    print(f"   git push")
    
    return output_path


def estadisticas_basicas():
    """Muestra estadísticas básicas de la base de datos"""
    
    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS DE LA BASE DE DATOS")
    print("="*60 + "\n")
    
    total_obras = Obra.objects.count()
    total_autores = Autor.objects.count()
    total_lugares = Lugar.objects.count()
    total_reps = Representacion.objects.count()
    
    print(f"  Obras totales: {total_obras}")
    print(f"  Autores: {total_autores}")
    print(f"  Lugares: {total_lugares}")
    print(f"  Representaciones: {total_reps}")
    
    print("\n  Por fuente:")
    for fuente in ['FUENTESXI', 'CATCOM', 'AMBAS']:
        count = Obra.objects.filter(fuente_principal=fuente).count()
        print(f"    {fuente}: {count}")
    
    print("\n  Por tipo de obra:")
    tipos = Obra.objects.values_list('tipo_obra', flat=True).distinct()
    for tipo in tipos:
        if tipo:
            count = Obra.objects.filter(tipo_obra=tipo).count()
            print(f"    {tipo}: {count}")
    
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    try:
        # Mostrar estadísticas
        estadisticas_basicas()
        
        # Exportar datos (todas las obras)
        output_path = exportar_obras_a_json()
        
        print("\n🎉 ¡Proceso completado exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante la exportación: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


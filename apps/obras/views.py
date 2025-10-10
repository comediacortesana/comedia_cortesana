from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Obra, Manuscrito, PaginaPDF, TemaLiterario, ObraTema, ComentarioUsuario
from .serializers import ObraSerializer, ManuscritoSerializer, TemaLiterarioSerializer, ObraTemaSerializer
from django.db.models import Q

class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['autor', 'tipo_obra', 'genero', 'fuente_principal', 'musica_conservada', 'mecenas', 'compositor']
    search_fields = ['titulo', 'titulo_limpio', 'titulo_alternativo', 'autor__nombre', 'mecenas', 'compositor', 'tema', 'notas_bibliograficas', 'bibliotecas_musica', 'bibliografia_musica', 'manuscritos_conocidos', 'ediciones_conocidas']
    ordering_fields = ['titulo', 'created_at', 'updated_at']
    ordering = ['titulo']

class ManuscritoViewSet(viewsets.ModelViewSet):
    queryset = Manuscrito.objects.all()
    serializer_class = ManuscritoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['obra']
    search_fields = ['ubicacion', 'signatura', 'notas']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

class TemaLiterarioViewSet(viewsets.ModelViewSet):
    """ViewSet para temas literarios"""
    queryset = TemaLiterario.objects.all()
    serializer_class = TemaLiterarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_tema']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'tipo_tema', 'total_obras']
    ordering = ['tipo_tema', 'nombre']

class ObraTemaViewSet(viewsets.ModelViewSet):
    """ViewSet para relaciones obra-tema"""
    queryset = ObraTema.objects.all()
    serializer_class = ObraTemaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['obra', 'tema', 'es_principal']
    search_fields = ['notas']
    ordering_fields = ['es_principal', 'created_at']
    ordering = ['-es_principal', 'tema__nombre']

def editor_view(request):
    """Vista principal del editor unificado"""
    # Estadísticas por fuente
    stats = {
        'total': Obra.objects.count(),
        'fuentesxi': Obra.objects.filter(fuente_principal='FUENTESXI').count(),
        'catcom': Obra.objects.filter(fuente_principal='CATCOM').count(),
    }
    
    # Información de cada catálogo
    catalogos = [
        {
            'id': 'fuentesxi',
            'nombre': 'FUENTES XI',
            'titulo_completo': 'Comedias en Madrid: 1603-1709',
            'autores': 'J.E. Varey & N.D. Shergold',
            'descripcion': 'Catálogo histórico de representaciones teatrales en Madrid durante el Siglo de Oro',
            'tipo': 'PDF Extraído',
            'color': '#2c3e50',
            'icono': '📜',
            'obras_count': stats['fuentesxi'],
            'fecha_publicacion': '1987',
            'caracteristicas': [
                '477 obras teatrales',
                '1,154 representaciones',
                'Metadatos geográficos',
                'Fechas precisas',
                'Información de compañías'
            ]
        },
        {
            'id': 'catcom',
            'nombre': 'CATCOM',
            'titulo_completo': 'Base de Datos CATCOM',
            'autores': 'Universidad de Valencia',
            'descripcion': 'Base de datos digital de comedias del Siglo de Oro español',
            'tipo': 'Web Scraping',
            'color': '#8e44ad',
            'icono': '🌐',
            'obras_count': stats['catcom'],
            'fecha_publicacion': 'En línea',
            'caracteristicas': [
                '1,561 obras teatrales',
                'Atribuciones detalladas',
                'Variaciones de títulos',
                'Información bibliográfica',
                'Enlaces a fuentes'
            ]
        }
    ]
    
    context = {
        'catalogos': catalogos,
        'stats': stats,
    }
    
    return render(request, 'obras/editor.html', context)

def editor_catalogo_view(request, catalogo_id):
    """Vista del editor para un catálogo específico"""
    fuente_map = {
        'fuentesxi': 'FUENTESXI',
        'catcom': 'CATCOM'
    }
    
    if catalogo_id not in fuente_map:
        from django.http import Http404
        raise Http404("Catálogo no encontrado")
    
    fuente = fuente_map[catalogo_id]
    
    # Obtener datos para el editor
    obras = Obra.objects.filter(fuente_principal=fuente).order_by('titulo_limpio')
    
    # Importar modelos y funciones necesarias
    from apps.autores.models import Autor
    from apps.lugares.models import Lugar
    from apps.representaciones.models import Representacion
    from apps.bibliografia.models import ReferenciaBibliografica
    from django.db.models import Count as DjangoCount
    
    # Estadísticas del catálogo
    stats = {
        'total_obras': obras.count(),
        'total_representaciones': sum(obra.total_representaciones for obra in obras),
        'autores_unicos': obras.values('autor').distinct().count(),
        'tipos_obra': obras.values('tipo_obra').distinct().count(),
        'con_musica': obras.filter(musica_conservada=True).count(),
        'sin_musica': obras.filter(musica_conservada=False).count(),
    }
    
    # Obtener opciones para los selects
    
    autores = Autor.objects.all().order_by('nombre')
    lugares = Lugar.objects.all().order_by('nombre')
    representaciones = Representacion.objects.filter(obra__fuente_principal=fuente).order_by('-fecha_formateada')
    bibliografia = ReferenciaBibliografica.objects.filter(obra__fuente_principal=fuente).order_by('autor')
    
    # Obtener autores que tienen obras en este catálogo
    autores_con_obras = Autor.objects.filter(
        obras__fuente_principal=fuente
    ).annotate(
        num_obras=DjangoCount('obras')
    ).order_by('nombre').distinct()
    
    # Obtener tipos de obra únicos CON CONTADOR
    tipos_obra_con_count = Obra.objects.exclude(
        tipo_obra__isnull=True
    ).exclude(
        tipo_obra=''
    ).values('tipo_obra').annotate(
        total=DjangoCount('id')
    ).order_by('tipo_obra')
    
    # Obtener géneros únicos CON CONTADOR
    generos_con_count = Obra.objects.exclude(
        genero__isnull=True
    ).exclude(
        genero=''
    ).values('genero').annotate(
        total=DjangoCount('id')
    ).order_by('genero')
    
    # Obtener compositores únicos CON CONTADOR
    compositores_con_count = Obra.objects.exclude(
        compositor__isnull=True
    ).exclude(
        compositor=''
    ).values('compositor').annotate(
        total=DjangoCount('id')
    ).order_by('compositor')
    
    # Obtener mecenas únicos CON CONTADOR
    mecenas_con_count = Obra.objects.exclude(
        mecenas__isnull=True
    ).exclude(
        mecenas=''
    ).values('mecenas').annotate(
        total=DjangoCount('id')
    ).order_by('mecenas')
    
    # Obtener lugares únicos CON CONTADOR de obras que tienen representaciones
    lugares_con_count = Lugar.objects.annotate(
        total=DjangoCount('representaciones__obra', distinct=True)
    ).filter(total__gt=0).order_by('nombre')
    
    # Si no hay representaciones, mostrar todos los lugares disponibles
    if not lugares_con_count.exists():
        lugares_con_count = Lugar.objects.annotate(
            total=DjangoCount('id')
        ).order_by('nombre')
    
    # Obtener compañías únicas de representaciones CON CONTADOR
    companias_con_count = Representacion.objects.exclude(
        compañia__isnull=True
    ).exclude(
        compañia=''
    ).values('compañia').annotate(
        total=DjangoCount('id')
    ).order_by('compañia')
    
    context = {
        'catalogo_id': catalogo_id,
        'fuente': fuente,
        'obras': obras,  # Mostrar todas las obras
        'autores': autores,
        'autores_con_obras': autores_con_obras,
        'tipos_obra_con_count': tipos_obra_con_count,
        'generos_con_count': generos_con_count,
        'compositores_con_count': compositores_con_count,
        'mecenas_con_count': mecenas_con_count,
        'lugares_con_count': lugares_con_count,
        'companias_con_count': companias_con_count,
        'lugares': lugares,
        'representaciones': representaciones,
        'bibliografia': bibliografia,
        'stats': stats,
        'tipo_obra_choices': Obra.TIPO_OBRA_CHOICES,
    }
    
    return render(request, 'obras/editor_catalogo.html', context)

@require_http_methods(["GET", "POST"])
def obra_edit_ajax(request, catalogo_id, obra_id):
    """Vista AJAX para editar una obra específica"""
    obra = get_object_or_404(Obra, id=obra_id)
    
    if request.method == 'POST':
        try:
            # Actualizar la obra con los datos del formulario
            obra.titulo = request.POST.get('titulo', obra.titulo)
            obra.titulo_limpio = request.POST.get('titulo_limpio', obra.titulo_limpio)
            obra.titulo_alternativo = request.POST.get('titulo_alternativo', obra.titulo_alternativo)
            obra.tipo_obra = request.POST.get('tipo_obra', obra.tipo_obra)
            obra.genero = request.POST.get('genero', obra.genero)
            obra.tema = request.POST.get('tema', obra.tema)
            obra.fecha_creacion_estimada = request.POST.get('fecha_creacion_estimada', obra.fecha_creacion_estimada)
            obra.versos = request.POST.get('versos') or None
            obra.actos = request.POST.get('actos') or None
            obra.musica_conservada = request.POST.get('musica_conservada') == 'on'
            obra.compositor = request.POST.get('compositor', obra.compositor)
            obra.bibliotecas_musica = request.POST.get('bibliotecas_musica', obra.bibliotecas_musica)
            obra.bibliografia_musica = request.POST.get('bibliografia_musica', obra.bibliografia_musica)
            obra.mecenas = request.POST.get('mecenas', obra.mecenas)
            obra.edicion_principe = request.POST.get('edicion_principe', obra.edicion_principe)
            obra.notas_bibliograficas = request.POST.get('notas_bibliograficas', obra.notas_bibliograficas)
            obra.notas = request.POST.get('notas', obra.notas)
            obra.origen_datos = request.POST.get('origen_datos', obra.origen_datos)
            obra.pagina_pdf = request.POST.get('pagina_pdf') or None
            obra.texto_original_pdf = request.POST.get('texto_original_pdf', obra.texto_original_pdf)
            
            # Actualizar autor si se proporciona
            autor_id = request.POST.get('autor')
            if autor_id:
                from apps.autores.models import Autor
                try:
                    autor = Autor.objects.get(id=autor_id)
                    obra.autor = autor
                except Autor.DoesNotExist:
                    pass
            
            obra.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Obra "{obra.titulo_limpio}" actualizada correctamente.',
                'obra': {
                    'id': obra.id,
                    'titulo': obra.titulo,
                    'titulo_limpio': obra.titulo_limpio,
                    'autor': obra.autor.nombre if obra.autor else 'Desconocido',
                    'tipo_obra': obra.tipo_obra,
                    'genero': obra.genero,
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al actualizar la obra: {str(e)}'
            })
    
    # GET request - devolver datos de la obra
    return JsonResponse({
        'obra': {
            'id': obra.id,
            'titulo': obra.titulo,
            'titulo_limpio': obra.titulo_limpio,
            'titulo_alternativo': obra.titulo_alternativo,
            'tipo_obra': obra.tipo_obra,
            'genero': obra.genero,
            'tema': obra.tema,
            'fecha_creacion_estimada': obra.fecha_creacion_estimada,
            'versos': obra.versos,
            'actos': obra.actos,
            'musica_conservada': obra.musica_conservada,
            'compositor': obra.compositor,
            'bibliotecas_musica': obra.bibliotecas_musica,
            'bibliografia_musica': obra.bibliografia_musica,
            'mecenas': obra.mecenas,
            'edicion_principe': obra.edicion_principe,
            'notas_bibliograficas': obra.notas_bibliograficas,
            'notas': obra.notas,
            'origen_datos': obra.origen_datos,
            'pagina_pdf': obra.pagina_pdf,
            'texto_original_pdf': obra.texto_original_pdf,
            'autor_id': obra.autor.id if obra.autor else None,
            'autor_nombre': obra.autor.nombre if obra.autor else 'Desconocido',
        }
    })

def busqueda_obras_ajax(request):
    """Vista AJAX para búsqueda de obras"""
    catalogo_id = request.GET.get('catalogo', '')
    query = request.GET.get('q', '')
    
    fuente_map = {
        'fuentesxi': 'FUENTESXI',
        'catcom': 'CATCOM'
    }
    
    if catalogo_id not in fuente_map:
        return JsonResponse({'error': 'Catálogo no válido'})
    
    fuente = fuente_map[catalogo_id]
    obras = Obra.objects.filter(fuente_principal=fuente)
    
    if query:
        obras = obras.filter(
            Q(titulo__icontains=query) |
            Q(titulo_limpio__icontains=query) |
            Q(autor__nombre__icontains=query) |
            Q(titulo_alternativo__icontains=query)
        )
    
    obras_data = []
    for obra in obras:  # Sin límite - se manejarán todos los resultados
        obras_data.append({
            'id': obra.id,
            'titulo': obra.titulo,
            'titulo_limpio': obra.titulo_limpio,
            'autor': obra.autor.nombre if obra.autor else 'Desconocido',
            'tipo_obra': obra.tipo_obra,
            'genero': obra.genero,
        })
    
    return JsonResponse({
        'obras': obras_data,
        'total': obras.count()
    })

@require_http_methods(["GET"])
def count_obras_ajax(request, catalogo_id):
    """Vista AJAX para contar obras según filtros (sin devolver los datos)"""
    fuente_map = {
        'fuentesxi': 'FUENTESXI',
        'catcom': 'CATCOM'
    }
    
    if catalogo_id not in fuente_map:
        return JsonResponse({'error': 'Catálogo no válido'})
    
    fuente = fuente_map[catalogo_id]
    obras = Obra.objects.filter(fuente_principal=fuente)
    
    # Aplicar filtros
    query = request.GET.get('q', '').strip()
    autor_id = request.GET.get('autor', '').strip()
    tipo_obra = request.GET.get('tipo', '').strip()
    genero = request.GET.get('genero', '').strip()
    musica = request.GET.get('musica', '').strip()
    compositor = request.GET.get('compositor', '').strip()
    lugar_id = request.GET.get('lugar', '').strip()
    mecenas = request.GET.get('mecenas', '').strip()
    compania = request.GET.get('compania', '').strip()
    
    if query:
        obras = obras.filter(
            Q(titulo__icontains=query) |
            Q(titulo_limpio__icontains=query) |
            Q(autor__nombre__icontains=query) |
            Q(titulo_alternativo__icontains=query)
        )
    
    if autor_id:
        obras = obras.filter(autor_id=autor_id)
    
    if tipo_obra:
        obras = obras.filter(tipo_obra=tipo_obra)
    
    if genero:
        obras = obras.filter(genero__icontains=genero)
    
    if musica == 'true':
        obras = obras.filter(musica_conservada=True)
    elif musica == 'false':
        obras = obras.filter(musica_conservada=False)
    
    if compositor:
        obras = obras.filter(compositor__icontains=compositor)
    
    if lugar_id:
        # Filtrar por obras que tengan representaciones en ese lugar
        obras = obras.filter(representaciones__lugar_id=lugar_id).distinct()
    
    if mecenas:
        obras = obras.filter(mecenas__icontains=mecenas)
    
    if compania:
        # Filtrar por obras que tengan representaciones de esa compañía
        obras = obras.filter(representaciones__compañia__icontains=compania).distinct()
    
    return JsonResponse({
        'count': obras.count(),
        'filters_applied': {
            'query': query != '',
            'autor': autor_id != '',
            'tipo': tipo_obra != '',
            'genero': genero != '',
            'musica': musica != '',
            'compositor': compositor != '',
            'lugar': lugar_id != '',
            'mecenas': mecenas != '',
            'compania': compania != ''
        }
    })

@require_http_methods(["GET"])
def obra_pdf_pages_ajax(request, catalogo_id, obra_id):
    """Vista AJAX para obtener las páginas PDF asociadas a una obra"""
    try:
        # Obtener la obra
        obra = get_object_or_404(Obra, id=obra_id)
        
        # Buscar páginas PDF asociadas a esta obra
        paginas = []
        
        # Si la obra tiene una página PDF específica
        if obra.pagina_pdf:
            try:
                pagina = PaginaPDF.objects.get(numero_pagina=obra.pagina_pdf)
                paginas.append({
                    'numero_pagina': pagina.numero_pagina,
                    'texto_extraido': pagina.texto_extraido,
                    'archivo_imagen': pagina.archivo_imagen,
                    'ruta_imagen_completa': pagina.ruta_imagen_completa,
                    'part_file': pagina.part_file,
                })
            except PaginaPDF.DoesNotExist:
                pass
        
        # Buscar páginas adicionales que contengan el título de la obra
        if obra.titulo_limpio:
            paginas_adicionales = PaginaPDF.objects.filter(
                texto_extraido__icontains=obra.titulo_limpio
            ).exclude(numero_pagina=obra.pagina_pdf if obra.pagina_pdf else 0)
            
            for pagina in paginas_adicionales:
                paginas.append({
                    'numero_pagina': pagina.numero_pagina,
                    'texto_extraido': pagina.texto_extraido,
                    'archivo_imagen': pagina.archivo_imagen,
                    'ruta_imagen_completa': pagina.ruta_imagen_completa,
                    'part_file': pagina.part_file,
                })
        
        # Si no hay páginas específicas, buscar por título alternativo
        if not paginas and obra.titulo_alternativo:
            paginas_alternativas = PaginaPDF.objects.filter(
                texto_extraido__icontains=obra.titulo_alternativo
            )
            
            for pagina in paginas_alternativas:
                paginas.append({
                    'numero_pagina': pagina.numero_pagina,
                    'texto_extraido': pagina.texto_extraido,
                    'archivo_imagen': pagina.archivo_imagen,
                    'ruta_imagen_completa': pagina.ruta_imagen_completa,
                    'part_file': pagina.part_file,
                })
        
        # Eliminar duplicados y ordenar por número de página
        paginas_unicas = []
        numeros_vistos = set()
        
        for pagina in paginas:
            if pagina['numero_pagina'] not in numeros_vistos:
                paginas_unicas.append(pagina)
                numeros_vistos.add(pagina['numero_pagina'])
        
        paginas_unicas.sort(key=lambda x: x['numero_pagina'])
        
        return JsonResponse({
            'success': True,
            'pages': paginas_unicas,
            'total': len(paginas_unicas)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al cargar las páginas PDF: {str(e)}',
            'pages': []
        })

@require_http_methods(["GET"])
def section_pdf_pages_ajax(request, catalogo_id, section, item_id):
    """Vista AJAX para obtener las páginas PDF asociadas a cualquier elemento de cualquier sección"""
    try:
        paginas = []
        
        if section == 'obras':
            # Para obras, usar la lógica existente
            obra = get_object_or_404(Obra, id=item_id)
            
            # Si la obra tiene una página PDF específica
            if obra.pagina_pdf:
                try:
                    pagina = PaginaPDF.objects.get(numero_pagina=obra.pagina_pdf)
                    paginas.append({
                        'numero_pagina': pagina.numero_pagina,
                        'texto_extraido': pagina.texto_extraido,
                        'archivo_imagen': pagina.archivo_imagen,
                        'ruta_imagen_completa': pagina.ruta_imagen_completa,
                        'part_file': pagina.part_file,
                    })
                except PaginaPDF.DoesNotExist:
                    pass
            
            # Buscar páginas adicionales que contengan el título de la obra
            if obra.titulo_limpio:
                paginas_adicionales = PaginaPDF.objects.filter(
                    texto_extraido__icontains=obra.titulo_limpio
                ).exclude(numero_pagina=obra.pagina_pdf if obra.pagina_pdf else 0)
                
                for pagina in paginas_adicionales:
                    paginas.append({
                        'numero_pagina': pagina.numero_pagina,
                        'texto_extraido': pagina.texto_extraido,
                        'archivo_imagen': pagina.archivo_imagen,
                        'ruta_imagen_completa': pagina.ruta_imagen_completa,
                        'part_file': pagina.part_file,
                    })
            
            # Si no hay páginas específicas, buscar por título alternativo
            if not paginas and obra.titulo_alternativo:
                paginas_alternativas = PaginaPDF.objects.filter(
                    texto_extraido__icontains=obra.titulo_alternativo
                )
                
                for pagina in paginas_alternativas:
                    paginas.append({
                        'numero_pagina': pagina.numero_pagina,
                        'texto_extraido': pagina.texto_extraido,
                        'archivo_imagen': pagina.archivo_imagen,
                        'ruta_imagen_completa': pagina.ruta_imagen_completa,
                        'part_file': pagina.part_file,
                    })
        
        elif section == 'autores':
            # Para autores, buscar páginas que contengan el nombre del autor
            from apps.autores.models import Autor
            autor = get_object_or_404(Autor, id=item_id)
            
            if autor.nombre:
                paginas_autor = PaginaPDF.objects.filter(
                    texto_extraido__icontains=autor.nombre
                )
                
                for pagina in paginas_autor:
                    paginas.append({
                        'numero_pagina': pagina.numero_pagina,
                        'texto_extraido': pagina.texto_extraido,
                        'archivo_imagen': pagina.archivo_imagen,
                        'ruta_imagen_completa': pagina.ruta_imagen_completa,
                        'part_file': pagina.part_file,
                    })
            
            # También buscar por nombre completo si es diferente
            if autor.nombre_completo and autor.nombre_completo != autor.nombre:
                paginas_nombre_completo = PaginaPDF.objects.filter(
                    texto_extraido__icontains=autor.nombre_completo
                )
                
                for pagina in paginas_nombre_completo:
                    paginas.append({
                        'numero_pagina': pagina.numero_pagina,
                        'texto_extraido': pagina.texto_extraido,
                        'archivo_imagen': pagina.archivo_imagen,
                        'ruta_imagen_completa': pagina.ruta_imagen_completa,
                        'part_file': pagina.part_file,
                    })
        
        elif section == 'lugares':
            # Para lugares, buscar páginas que contengan el nombre del lugar
            from apps.lugares.models import Lugar
            lugar = get_object_or_404(Lugar, id=item_id)
            
            if lugar.nombre:
                paginas_lugar = PaginaPDF.objects.filter(
                    texto_extraido__icontains=lugar.nombre
                )
                
                for pagina in paginas_lugar:
                    paginas.append({
                        'numero_pagina': pagina.numero_pagina,
                        'texto_extraido': pagina.texto_extraido,
                        'archivo_imagen': pagina.archivo_imagen,
                        'ruta_imagen_completa': pagina.ruta_imagen_completa,
                        'part_file': pagina.part_file,
                    })
            
            # También buscar por región si es diferente
            if lugar.region and lugar.region != lugar.nombre:
                paginas_region = PaginaPDF.objects.filter(
                    texto_extraido__icontains=lugar.region
                )
                
                for pagina in paginas_region:
                    paginas.append({
                        'numero_pagina': pagina.numero_pagina,
                        'texto_extraido': pagina.texto_extraido,
                        'archivo_imagen': pagina.archivo_imagen,
                        'ruta_imagen_completa': pagina.ruta_imagen_completa,
                        'part_file': pagina.part_file,
                    })
        
        elif section == 'representaciones':
            # Para representaciones, buscar páginas relacionadas con la obra y lugar
            from apps.representaciones.models import Representacion
            representacion = get_object_or_404(Representacion, id=item_id)
            
            # Buscar por obra
            if representacion.obra and representacion.obra.titulo_limpio:
                paginas_obra = PaginaPDF.objects.filter(
                    texto_extraido__icontains=representacion.obra.titulo_limpio
                )
                
                for pagina in paginas_obra:
                    paginas.append({
                        'numero_pagina': pagina.numero_pagina,
                        'texto_extraido': pagina.texto_extraido,
                        'archivo_imagen': pagina.archivo_imagen,
                        'ruta_imagen_completa': pagina.ruta_imagen_completa,
                        'part_file': pagina.part_file,
                    })
            
            # Buscar por lugar
            if representacion.lugar and representacion.lugar.nombre:
                paginas_lugar = PaginaPDF.objects.filter(
                    texto_extraido__icontains=representacion.lugar.nombre
                )
                
                for pagina in paginas_lugar:
                    paginas.append({
                        'numero_pagina': pagina.numero_pagina,
                        'texto_extraido': pagina.texto_extraido,
                        'archivo_imagen': pagina.archivo_imagen,
                        'ruta_imagen_completa': pagina.ruta_imagen_completa,
                        'part_file': pagina.part_file,
                    })
            
            # Buscar por compañía
            if representacion.compañia:
                paginas_compañia = PaginaPDF.objects.filter(
                    texto_extraido__icontains=representacion.compañia
                )
                
                for pagina in paginas_compañia:
                    paginas.append({
                        'numero_pagina': pagina.numero_pagina,
                        'texto_extraido': pagina.texto_extraido,
                        'archivo_imagen': pagina.archivo_imagen,
                        'ruta_imagen_completa': pagina.ruta_imagen_completa,
                        'part_file': pagina.part_file,
                    })
        
        elif section == 'bibliografia':
            # Para bibliografía, buscar páginas que contengan el título o autor
            from apps.bibliografia.models import ReferenciaBibliografica
            referencia = get_object_or_404(ReferenciaBibliografica, id=item_id)
            
            # Buscar por título
            if referencia.titulo:
                paginas_titulo = PaginaPDF.objects.filter(
                    texto_extraido__icontains=referencia.titulo
                )
                
                for pagina in paginas_titulo:
                    paginas.append({
                        'numero_pagina': pagina.numero_pagina,
                        'texto_extraido': pagina.texto_extraido,
                        'archivo_imagen': pagina.archivo_imagen,
                        'ruta_imagen_completa': pagina.ruta_imagen_completa,
                        'part_file': pagina.part_file,
                    })
            
            # Buscar por autor
            if referencia.autor:
                paginas_autor = PaginaPDF.objects.filter(
                    texto_extraido__icontains=referencia.autor
                )
                
                for pagina in paginas_autor:
                    paginas.append({
                        'numero_pagina': pagina.numero_pagina,
                        'texto_extraido': pagina.texto_extraido,
                        'archivo_imagen': pagina.archivo_imagen,
                        'ruta_imagen_completa': pagina.ruta_imagen_completa,
                        'part_file': pagina.part_file,
                    })
        
        # Eliminar duplicados y ordenar por número de página
        paginas_unicas = []
        numeros_vistos = set()
        
        for pagina in paginas:
            if pagina['numero_pagina'] not in numeros_vistos:
                paginas_unicas.append(pagina)
                numeros_vistos.add(pagina['numero_pagina'])
        
        paginas_unicas.sort(key=lambda x: x['numero_pagina'])
        
        return JsonResponse({
            'success': True,
            'pages': paginas_unicas,
            'total': len(paginas_unicas)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al cargar las páginas PDF: {str(e)}',
            'pages': []
        })

def get_section_data_ajax(request, catalogo_id, section):
    """Vista AJAX para obtener datos de diferentes secciones"""
    fuente_map = {
        'fuentesxi': 'FUENTESXI',
        'catcom': 'CATCOM'
    }
    
    if catalogo_id not in fuente_map:
        return JsonResponse({'error': 'Catálogo no válido'})
    
    fuente = fuente_map[catalogo_id]
    query = request.GET.get('q', '')
    
    if section == 'obras':
        from .models import Obra
        items = Obra.objects.filter(fuente_principal=fuente)
        
        # Aplicar filtros de búsqueda de texto
        if query:
            items = items.filter(
                Q(titulo__icontains=query) |
                Q(titulo_limpio__icontains=query) |
                Q(autor__nombre__icontains=query) |
                Q(titulo_alternativo__icontains=query)
            )
        
        # Aplicar filtros dropdown
        autor_id = request.GET.get('autor', '')
        tipo_obra = request.GET.get('tipo', '')
        genero = request.GET.get('genero', '')
        musica = request.GET.get('musica', '')
        compositor = request.GET.get('compositor', '')
        lugar_id = request.GET.get('lugar', '')
        mecenas = request.GET.get('mecenas', '')
        compania = request.GET.get('compania', '')
        
        if autor_id:
            items = items.filter(autor_id=autor_id)
        
        if tipo_obra:
            items = items.filter(tipo_obra=tipo_obra)
        
        if genero:
            items = items.filter(genero__icontains=genero)
        
        if musica == 'true':
            items = items.filter(musica_conservada=True)
        elif musica == 'false':
            items = items.filter(musica_conservada=False)
        
        if compositor:
            items = items.filter(compositor__icontains=compositor)
        
        if lugar_id:
            # Filtrar por obras que tengan representaciones en ese lugar
            items = items.filter(representaciones__lugar_id=lugar_id).distinct()
        
        if mecenas:
            items = items.filter(mecenas__icontains=mecenas)
        
        if compania:
            # Filtrar por obras que tengan representaciones de esa compañía
            items = items.filter(representaciones__compañia__icontains=compania).distinct()
        
        data = []
        for item in items:  # Sin límite - mostrar todos los resultados filtrados
            data.append({
                'id': item.id,
                'titulo': item.titulo_limpio or item.titulo,
                'subtitulo': item.autor.nombre if item.autor else 'Autor desconocido',
                'tipo': item.tipo_obra or 'Sin clasificar',
                'extra': item.genero or '',
            })
    
    elif section == 'autores':
        from apps.autores.models import Autor
        items = Autor.objects.all()
        if query:
            items = items.filter(
                Q(nombre__icontains=query) |
                Q(nombre_completo__icontains=query) |
                Q(biografia__icontains=query)
            )
        
        data = []
        for item in items[:50]:
            data.append({
                'id': item.id,
                'titulo': item.nombre,
                'subtitulo': item.nombre_completo or '',
                'tipo': item.epoca or 'Sin época',
                'extra': f"{item.obras.count()} obras",
            })
    
    elif section == 'lugares':
        from apps.lugares.models import Lugar
        items = Lugar.objects.all()
        if query:
            items = items.filter(
                Q(nombre__icontains=query) |
                Q(region__icontains=query) |
                Q(pais__icontains=query) |
                Q(descripcion__icontains=query)
            )
        
        data = []
        for item in items[:50]:
            data.append({
                'id': item.id,
                'titulo': item.nombre,
                'subtitulo': f"{item.region}, {item.pais}" if item.region and item.pais else item.region or item.pais or '',
                'tipo': item.tipo_lugar or 'Sin tipo',
                'extra': 'Capital' if item.es_capital else '',
            })
    
    elif section == 'representaciones':
        from apps.representaciones.models import Representacion
        items = Representacion.objects.filter(obra__fuente_principal=fuente)
        if query:
            items = items.filter(
                Q(obra__titulo__icontains=query) |
                Q(obra__titulo_limpio__icontains=query) |
                Q(lugar__nombre__icontains=query) |
                Q(compañia__icontains=query) |
                Q(fecha__icontains=query)
            )
        
        data = []
        for item in items[:50]:
            data.append({
                'id': item.id,
                'titulo': item.obra.titulo_limpio or item.obra.titulo,
                'subtitulo': f"{item.lugar.nombre if item.lugar else 'Lugar desconocido'} - {item.fecha}",
                'tipo': item.compañia or 'Sin compañía',
                'extra': item.tipo_funcion or '',
            })
    
    elif section == 'bibliografia':
        from apps.bibliografia.models import ReferenciaBibliografica
        items = ReferenciaBibliografica.objects.filter(obra__fuente_principal=fuente)
        if query:
            items = items.filter(
                Q(titulo__icontains=query) |
                Q(autor__icontains=query) |
                Q(editor__icontains=query) |
                Q(editorial__icontains=query)
            )
        
        data = []
        for item in items[:50]:
            data.append({
                'id': item.id,
                'titulo': item.titulo,
                'subtitulo': f"{item.autor} - {item.año_publicacion or 'Sin año'}",
                'tipo': item.tipo_referencia or 'Sin tipo',
                'extra': item.editorial or '',
            })
    
    else:
        return JsonResponse({'error': 'Sección no válida'})
    
    return JsonResponse({
        'items': data,
        'total': items.count(),
        'section': section
    })

@require_http_methods(["GET", "POST"])
def edit_item_ajax(request, catalogo_id, section, item_id):
    """Vista AJAX para editar elementos de diferentes secciones"""
    if section == 'obras':
        return obra_edit_ajax(request, catalogo_id, item_id)
    
    elif section == 'autores':
        from apps.autores.models import Autor
        item = get_object_or_404(Autor, id=item_id)
        
        if request.method == 'POST':
            try:
                item.nombre = request.POST.get('nombre', item.nombre)
                item.nombre_completo = request.POST.get('nombre_completo', item.nombre_completo)
                item.epoca = request.POST.get('epoca', item.epoca)
                item.biografia = request.POST.get('biografia', item.biografia)
                item.fecha_nacimiento = request.POST.get('fecha_nacimiento', item.fecha_nacimiento)
                item.fecha_muerte = request.POST.get('fecha_muerte', item.fecha_muerte)
                item.obras_principales = request.POST.get('obras_principales', item.obras_principales)
                item.notas = request.POST.get('notas', item.notas)
                item.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Autor "{item.nombre}" actualizado correctamente.',
                    'item': {
                        'id': item.id,
                        'nombre': item.nombre,
                        'nombre_completo': item.nombre_completo,
                        'epoca': item.epoca,
                        'biografia': item.biografia,
                        'fecha_nacimiento': item.fecha_nacimiento,
                        'fecha_muerte': item.fecha_muerte,
                        'obras_principales': item.obras_principales,
                        'notas': item.notas,
                    }
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error al actualizar el autor: {str(e)}'
                })
        
        return JsonResponse({
            'item': {
                'id': item.id,
                'nombre': item.nombre,
                'nombre_completo': item.nombre_completo,
                'epoca': item.epoca,
                'biografia': item.biografia,
                'fecha_nacimiento': item.fecha_nacimiento,
                'fecha_muerte': item.fecha_muerte,
                'obras_principales': item.obras_principales,
                'notas': item.notas,
            }
        })
    
    elif section == 'lugares':
        from apps.lugares.models import Lugar
        item = get_object_or_404(Lugar, id=item_id)
        
        if request.method == 'POST':
            try:
                item.nombre = request.POST.get('nombre', item.nombre)
                item.region = request.POST.get('region', item.region)
                item.pais = request.POST.get('pais', item.pais)
                item.tipo_lugar = request.POST.get('tipo_lugar', item.tipo_lugar)
                item.es_capital = request.POST.get('es_capital') == 'on'
                item.descripcion = request.POST.get('descripcion', item.descripcion)
                item.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Lugar "{item.nombre}" actualizado correctamente.',
                    'item': {
                        'id': item.id,
                        'nombre': item.nombre,
                        'region': item.region,
                        'pais': item.pais,
                        'tipo_lugar': item.tipo_lugar,
                        'es_capital': item.es_capital,
                    }
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error al actualizar el lugar: {str(e)}'
                })
        
        return JsonResponse({
            'item': {
                'id': item.id,
                'nombre': item.nombre,
                'region': item.region,
                'pais': item.pais,
                'tipo_lugar': item.tipo_lugar,
                'es_capital': item.es_capital,
                'descripcion': item.descripcion,
            }
        })
    
    elif section == 'representaciones':
        from apps.representaciones.models import Representacion
        item = get_object_or_404(Representacion, id=item_id)
        
        if request.method == 'POST':
            try:
                item.fecha = request.POST.get('fecha', item.fecha)
                item.fecha_formateada = request.POST.get('fecha_formateada', item.fecha_formateada)
                item.compañia = request.POST.get('compañia', item.compañia)
                item.tipo_funcion = request.POST.get('tipo_funcion', item.tipo_funcion)
                item.observaciones = request.POST.get('observaciones', item.observaciones)
                item.pagina_pdf = request.POST.get('pagina_pdf') or None
                item.texto_original_pdf = request.POST.get('texto_original_pdf', item.texto_original_pdf)
                
                # Actualizar lugar si se proporciona
                lugar_id = request.POST.get('lugar')
                if lugar_id:
                    from apps.lugares.models import Lugar
                    try:
                        lugar = Lugar.objects.get(id=lugar_id)
                        item.lugar = lugar
                    except Lugar.DoesNotExist:
                        pass
                
                item.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Representación actualizada correctamente.',
                    'item': {
                        'id': item.id,
                        'fecha': item.fecha,
                        'fecha_formateada': item.fecha_formateada,
                        'compañia': item.compañia,
                        'tipo_funcion': item.tipo_funcion,
                        'observaciones': item.observaciones,
                        'lugar_id': item.lugar.id if item.lugar else None,
                        'lugar_nombre': item.lugar.nombre if item.lugar else 'Sin lugar',
                        'obra_id': item.obra.id if item.obra else None,
                        'obra_titulo': item.obra.titulo_limpio if item.obra else 'Sin obra',
                    }
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error al actualizar la representación: {str(e)}'
                })
        
        return JsonResponse({
            'item': {
                'id': item.id,
                'fecha': item.fecha,
                'fecha_formateada': item.fecha_formateada,
                'compañia': item.compañia,
                'tipo_funcion': item.tipo_funcion,
                'observaciones': item.observaciones,
                'lugar_id': item.lugar.id if item.lugar else None,
                'lugar_nombre': item.lugar.nombre if item.lugar else 'Sin lugar',
                'obra_id': item.obra.id if item.obra else None,
                'obra_titulo': item.obra.titulo_limpio if item.obra else 'Sin obra',
                'pagina_pdf': item.pagina_pdf,
                'texto_original_pdf': item.texto_original_pdf,
            }
        })
    
    elif section == 'bibliografia':
        from apps.bibliografia.models import ReferenciaBibliografica
        item = get_object_or_404(ReferenciaBibliografica, id=item_id)
        
        if request.method == 'POST':
            try:
                item.autor = request.POST.get('autor', item.autor)
                item.titulo = request.POST.get('titulo', item.titulo)
                item.editorial = request.POST.get('editorial', item.editorial)
                item.fecha_publicacion = request.POST.get('fecha_publicacion', item.fecha_publicacion)
                item.tipo_referencia = request.POST.get('tipo_referencia', item.tipo_referencia)
                item.url = request.POST.get('url', item.url)
                item.notas = request.POST.get('notas', item.notas)
                item.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Referencia bibliográfica actualizada correctamente.',
                    'item': {
                        'id': item.id,
                        'autor': item.autor,
                        'titulo': item.titulo,
                        'editorial': item.editorial,
                        'fecha_publicacion': item.fecha_publicacion,
                        'tipo_referencia': item.tipo_referencia,
                        'url': item.url,
                        'notas': item.notas,
                        'obra_id': item.obra.id if item.obra else None,
                        'obra_titulo': item.obra.titulo_limpio if item.obra else 'Sin obra',
                    }
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error al actualizar la referencia bibliográfica: {str(e)}'
                })
        
        return JsonResponse({
            'item': {
                'id': item.id,
                'autor': item.autor,
                'titulo': item.titulo,
                'editorial': item.editorial,
                'fecha_publicacion': item.fecha_publicacion,
                'tipo_referencia': item.tipo_referencia,
                'url': item.url,
                'notas': item.notas,
                'obra_id': item.obra.id if item.obra else None,
                'obra_titulo': item.obra.titulo_limpio if item.obra else 'Sin obra',
            }
        })
    
    else:
        return JsonResponse({'error': 'Sección no válida'})

# Mantener las vistas existentes para compatibilidad
@require_http_methods(["GET", "POST"])
def obra_detail_view(request, obra_id):
    """Vista detallada de una obra específica con capacidad de edición"""
    obra = get_object_or_404(Obra, id=obra_id)
    
    # Manejar POST para guardar cambios (solo para usuarios autenticados)
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            # Actualizar campos editables
            if 'titulo' in request.POST:
                obra.titulo = request.POST.get('titulo', obra.titulo)
            if 'titulo_limpio' in request.POST:
                obra.titulo_limpio = request.POST.get('titulo_limpio', obra.titulo_limpio)
            if 'titulo_alternativo' in request.POST:
                obra.titulo_alternativo = request.POST.get('titulo_alternativo', obra.titulo_alternativo)
            
            # Actualizar autor si se proporciona
            if 'autor' in request.POST:
                autor_id = request.POST.get('autor')
                if autor_id:
                    from apps.autores.models import Autor
                    try:
                        autor = Autor.objects.get(id=autor_id)
                        obra.autor = autor
                    except Autor.DoesNotExist:
                        pass
                else:
                    obra.autor = None
            
            if 'genero' in request.POST:
                obra.genero = request.POST.get('genero', obra.genero)
            if 'tipo_obra' in request.POST:
                obra.tipo_obra = request.POST.get('tipo_obra', obra.tipo_obra)
            if 'idioma' in request.POST:
                obra.idioma = request.POST.get('idioma', obra.idioma)
            if 'actos' in request.POST:
                actos = request.POST.get('actos')
                obra.actos = int(actos) if actos else None
            if 'versos' in request.POST:
                versos = request.POST.get('versos')
                obra.versos = int(versos) if versos else None
            if 'fecha_creacion_estimada' in request.POST:
                obra.fecha_creacion_estimada = request.POST.get('fecha_creacion_estimada', obra.fecha_creacion_estimada)
            if 'tema' in request.POST:
                obra.tema = request.POST.get('tema', obra.tema)
            if 'musica_conservada' in request.POST:
                obra.musica_conservada = request.POST.get('musica_conservada') == 'on'
            if 'compositor' in request.POST:
                obra.compositor = request.POST.get('compositor', obra.compositor)
            if 'mecenas' in request.POST:
                obra.mecenas = request.POST.get('mecenas', obra.mecenas)
            if 'bibliotecas_musica' in request.POST:
                obra.bibliotecas_musica = request.POST.get('bibliotecas_musica', obra.bibliotecas_musica)
            if 'edicion_principe' in request.POST:
                obra.edicion_principe = request.POST.get('edicion_principe', obra.edicion_principe)
            if 'notas_bibliograficas' in request.POST:
                obra.notas_bibliograficas = request.POST.get('notas_bibliograficas', obra.notas_bibliograficas)
            if 'notas' in request.POST:
                obra.notas = request.POST.get('notas', obra.notas)
            
            obra.save()
            messages.success(request, f'Obra "{obra.titulo_limpio}" actualizada correctamente.')
            return redirect('obra_detail', obra_id=obra.id)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar la obra: {str(e)}')
    
    # Obtener datos relacionados
    manuscritos = obra.manuscritos.all()
    representaciones = obra.representaciones.all().order_by('fecha_formateada')
    
    # Obtener todos los autores para el dropdown
    from apps.autores.models import Autor
    autores = Autor.objects.all().order_by('nombre')
    
    # Estadísticas de la obra
    stats = {
        'total_manuscritos': manuscritos.count(),
        'total_representaciones': representaciones.count(),
        'lugares_unicos': representaciones.values('lugar__nombre').distinct().count(),
        'fechas_unicas': representaciones.values('fecha').distinct().count(),
    }
    
    context = {
        'obra': obra,
        'manuscritos': manuscritos,
        'representaciones': representaciones,
        'stats': stats,
        'autores': autores,
    }
    
    return render(request, 'obras/obra_detail.html', context)

def catalogos_view(request):
    """Vista principal que muestra las portadas de los catálogos disponibles"""
    # Estadísticas por fuente
    stats = {
        'total': Obra.objects.count(),
        'fuentesxi': Obra.objects.filter(fuente_principal='FUENTESXI').count(),
        'catcom': Obra.objects.filter(fuente_principal='CATCOM').count(),
        'ambas': Obra.objects.filter(fuente_principal__in=['FUENTESXI', 'CATCOM']).count(),
    }
    
    # Información de cada catálogo
    catalogos = [
        {
            'id': 'fuentesxi',
            'nombre': 'FUENTES XI',
            'titulo_completo': 'Comedias en Madrid: 1603-1709',
            'autores': 'J.E. Varey & N.D. Shergold',
            'descripcion': 'Catálogo histórico de representaciones teatrales en Madrid durante el Siglo de Oro',
            'tipo': 'PDF Extraído',
            'color': '#2c3e50',
            'icono': '📜',
            'obras_count': stats['fuentesxi'],
            'fecha_publicacion': '1987',
            'caracteristicas': [
                '477 obras teatrales',
                '1,154 representaciones',
                'Metadatos geográficos',
                'Fechas precisas',
                'Información de compañías'
            ]
        },
        {
            'id': 'catcom',
            'nombre': 'CATCOM',
            'titulo_completo': 'Base de Datos CATCOM',
            'autores': 'Universidad de Valencia',
            'descripcion': 'Base de datos digital de comedias del Siglo de Oro español',
            'tipo': 'Web Scraping',
            'color': '#8e44ad',
            'icono': '🌐',
            'obras_count': stats['catcom'],
            'fecha_publicacion': 'En línea',
            'caracteristicas': [
                '1,561 obras teatrales',
                'Atribuciones detalladas',
                'Variaciones de títulos',
                'Información bibliográfica',
                'Enlaces a fuentes'
            ]
        }
    ]
    
    context = {
        'catalogos': catalogos,
        'stats': stats,
    }
    
    return render(request, 'obras/catalogos.html', context)

def catalogo_detalle_view(request, catalogo_id):
    """Vista detallada de un catálogo específico con sus obras"""
    fuente_map = {
        'fuentesxi': 'FUENTESXI',
        'catcom': 'CATCOM'
    }
    
    if catalogo_id not in fuente_map:
        from django.http import Http404
        raise Http404("Catálogo no encontrado")
    
    fuente = fuente_map[catalogo_id]
    search = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    
    obras = Obra.objects.filter(fuente_principal=fuente)
    
    # Buscar por texto
    if search:
        obras = obras.filter(
            Q(titulo__icontains=search) |
            Q(titulo_limpio__icontains=search) |
            Q(autor__nombre__icontains=search) |
            Q(titulo_alternativo__icontains=search)
        )
    
    # Paginación simple
    from django.core.paginator import Paginator
    paginator = Paginator(obras.order_by('titulo'), 20)
    obras_page = paginator.get_page(page)
    
    # Estadísticas del catálogo
    stats = {
        'total_obras': obras.count(),
        'total_representaciones': sum(obra.total_representaciones for obra in obras),
        'autores_unicos': obras.values('autor').distinct().count(),
        'tipos_obra': obras.values('tipo_obra').distinct().count(),
    }
    
    context = {
        'catalogo_id': catalogo_id,
        'obras': obras_page,
        'search_actual': search,
        'stats': stats,
        'paginator': paginator,
    }
    
    return render(request, 'obras/catalogo_detalle.html', context)

def catalogo_view(request):
    """🔍 BUSCADOR/CATÁLOGO PÚBLICO - Vista del catálogo con filtros avanzados"""
    # Obtener parámetros de filtros
    fuente = request.GET.get('fuente', '')
    search = request.GET.get('search', '')
    tipo = request.GET.get('tipo', '')
    musica = request.GET.get('musica', '')
    autor_id = request.GET.get('autor', '')
    compositor = request.GET.get('compositor', '')
    genero = request.GET.get('genero', '')
    lugar_id = request.GET.get('lugar', '')
    mecenas = request.GET.get('mecenas', '')
    compania = request.GET.get('compania', '')
    
    # Obtener obras con sus representaciones para mostrar información completa
    obras = Obra.objects.select_related('autor').prefetch_related('representaciones__lugar').all()
    
    # Aplicar filtros
    if fuente:
        obras = obras.filter(fuente_principal=fuente)
    
    if tipo:
        obras = obras.filter(tipo_obra=tipo)
    
    if musica == 'true':
        obras = obras.filter(musica_conservada=True)
    elif musica == 'false':
        obras = obras.filter(musica_conservada=False)
    
    if autor_id:
        obras = obras.filter(autor_id=autor_id)
    
    if compositor:
        obras = obras.filter(compositor__icontains=compositor)
    
    if genero:
        obras = obras.filter(genero__icontains=genero)
    
    if lugar_id:
        obras = obras.filter(representaciones__lugar_id=lugar_id).distinct()
    
    if mecenas:
        obras = obras.filter(mecenas__icontains=mecenas)
    
    if compania:
        obras = obras.filter(representaciones__compañia__icontains=compania).distinct()
    
    # Buscar por texto (incluyendo campos principales)
    if search:
        obras = obras.filter(
            Q(titulo__icontains=search) |
            Q(titulo_limpio__icontains=search) |
            Q(autor__nombre__icontains=search) |
            Q(tipo_obra__icontains=search) |
            Q(fecha_creacion_estimada__icontains=search) |
            Q(mecenas__icontains=search) |
            Q(representaciones__compañia__icontains=search) |
            Q(representaciones__lugar__nombre__icontains=search)
        ).distinct()
    
    # Estadísticas generales
    stats = {
        'total': Obra.objects.count(),
        'fuentesxi': Obra.objects.filter(fuente_principal='FUENTESXI').count(),
        'catcom': Obra.objects.filter(fuente_principal='CATCOM').count(),
        'ambas': Obra.objects.filter(fuente_principal__in=['FUENTESXI', 'CATCOM']).count(),
        'con_musica': Obra.objects.filter(musica_conservada=True).count(),
        'sin_musica': Obra.objects.filter(musica_conservada=False).count(),
    }
    
    # Obtener opciones para los dropdowns
    from apps.autores.models import Autor
    from apps.lugares.models import Lugar
    from apps.representaciones.models import Representacion
    from django.db.models import Count as DjangoCount
    
    # Obtener autores CON CONTADOR
    autores_con_obras = Autor.objects.annotate(
        num_obras=DjangoCount('obras')
    ).filter(num_obras__gt=0).order_by('nombre')
    
    # tipo_obra ahora se muestra como "Género" (comedia, auto, zarzuela...)
    generos_principales_con_count = Obra.objects.exclude(
        tipo_obra__isnull=True
    ).exclude(
        tipo_obra=''
    ).values('tipo_obra').annotate(
        total=DjangoCount('id')
    ).order_by('tipo_obra')
    
    # genero ahora se muestra como "Subgénero" 
    subgeneros_con_count = Obra.objects.exclude(
        genero__isnull=True
    ).exclude(
        genero=''
    ).values('genero').annotate(
        total=DjangoCount('id')
    ).order_by('genero')
    
    # Nuevo campo subgenero para clasificaciones más específicas
    subgeneros_especificos_con_count = Obra.objects.exclude(
        subgenero__isnull=True
    ).exclude(
        subgenero=''
    ).values('subgenero').annotate(
        total=DjangoCount('id')
    ).order_by('subgenero')
    
    # Obtener compositores únicos CON CONTADOR
    compositores_con_count = Obra.objects.exclude(
        compositor__isnull=True
    ).exclude(
        compositor=''
    ).values('compositor').annotate(
        total=DjangoCount('id')
    ).order_by('compositor')
    
    # Obtener mecenas únicos CON CONTADOR
    mecenas_con_count = Obra.objects.exclude(
        mecenas__isnull=True
    ).exclude(
        mecenas=''
    ).values('mecenas').annotate(
        total=DjangoCount('id')
    ).order_by('mecenas')
    
    # Obtener lugares CON CONTADOR de obras que tienen representaciones
    lugares_con_count = Lugar.objects.annotate(
        total=DjangoCount('representaciones__obra', distinct=True)
    ).order_by('nombre')
    
    # Obtener compañías únicas CON CONTADOR
    companias_con_count = Representacion.objects.exclude(
        compañia__isnull=True
    ).exclude(
        compañia=''
    ).values('compañia').annotate(
        total=DjangoCount('id')
    ).order_by('compañia')
    
    context = {
        'obras': obras.order_by('titulo'),  # Sin límite - usar filtros para controlar resultados
        'fuente_actual': fuente,
        'search_actual': search,
        'tipo_actual': tipo,
        'musica_actual': musica,
        'autor_actual': autor_id,
        'compositor_actual': compositor,
        'genero_actual': genero,
        'lugar_actual': lugar_id,
        'mecenas_actual': mecenas,
        'compania_actual': compania,
        'stats': stats,
        'autores_con_obras': autores_con_obras,
        'generos_principales_con_count': generos_principales_con_count,  # tipo_obra mostrado como "Género"
        'subgeneros_con_count': subgeneros_con_count,  # genero mostrado como "Subgénero"
        'subgeneros_especificos_con_count': subgeneros_especificos_con_count,  # Nuevo campo
        'compositores_con_count': compositores_con_count,
        'mecenas_con_count': mecenas_con_count,
        'lugares_con_count': lugares_con_count,
        'companias_con_count': companias_con_count,
    }
    
    return render(request, 'obras/catalogo.html', context)

@require_http_methods(["GET"])
def catalogo_count_ajax(request):
    """🔍 BUSCADOR - Endpoint AJAX para contar obras según filtros (contador dinámico)"""
    # Obtener parámetros de filtros
    fuente = request.GET.get('fuente', '').strip()
    search = request.GET.get('search', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    musica = request.GET.get('musica', '').strip()
    autor_id = request.GET.get('autor', '').strip()
    compositor = request.GET.get('compositor', '').strip()
    genero = request.GET.get('genero', '').strip()
    lugar_id = request.GET.get('lugar', '').strip()
    mecenas = request.GET.get('mecenas', '').strip()
    compania = request.GET.get('compania', '').strip()
    
    # Aplicar filtros
    obras = Obra.objects.all()
    
    if fuente:
        obras = obras.filter(fuente_principal=fuente)
    
    if tipo:
        obras = obras.filter(tipo_obra=tipo)
    
    if musica == 'true':
        obras = obras.filter(musica_conservada=True)
    elif musica == 'false':
        obras = obras.filter(musica_conservada=False)
    
    if autor_id:
        obras = obras.filter(autor_id=autor_id)
    
    if compositor:
        obras = obras.filter(compositor__icontains=compositor)
    
    if genero:
        obras = obras.filter(genero__icontains=genero)
    
    if lugar_id:
        obras = obras.filter(representaciones__lugar_id=lugar_id).distinct()
    
    if mecenas:
        obras = obras.filter(mecenas__icontains=mecenas)
    
    if compania:
        obras = obras.filter(representaciones__compañia__icontains=compania).distinct()
    
    if search:
        obras = obras.filter(
            Q(titulo__icontains=search) |
            Q(titulo_limpio__icontains=search) |
            Q(autor__nombre__icontains=search) |
            Q(tipo_obra__icontains=search) |
            Q(fecha_creacion_estimada__icontains=search) |
            Q(mecenas__icontains=search) |
            Q(representaciones__compañia__icontains=search) |
            Q(representaciones__lugar__nombre__icontains=search)
        ).distinct()
    
    return JsonResponse({
        'count': obras.count(),
        'filters_applied': {
            'fuente': fuente != '',
            'search': search != '',
            'tipo': tipo != '',
            'musica': musica != '',
            'autor': autor_id != '',
            'compositor': compositor != '',
            'genero': genero != '',
            'lugar': lugar_id != '',
            'mecenas': mecenas != '',
            'compania': compania != ''
        }
    })

@require_http_methods(["GET", "POST"])
def obra_edit_view(request, obra_id):
    """Vista para editar una obra específica"""
    obra = get_object_or_404(Obra, id=obra_id)
    
    if request.method == 'POST':
        # Actualizar la obra con los datos del formulario
        obra.titulo = request.POST.get('titulo', obra.titulo)
        obra.titulo_limpio = request.POST.get('titulo_limpio', obra.titulo_limpio)
        obra.titulo_alternativo = request.POST.get('titulo_alternativo', obra.titulo_alternativo)
        obra.tipo_obra = request.POST.get('tipo_obra', obra.tipo_obra)
        obra.genero = request.POST.get('genero', obra.genero)
        obra.tema = request.POST.get('tema', obra.tema)
        obra.fecha_creacion_estimada = request.POST.get('fecha_creacion_estimada', obra.fecha_creacion_estimada)
        obra.versos = request.POST.get('versos') or None
        obra.actos = request.POST.get('actos') or None
        obra.musica_conservada = request.POST.get('musica_conservada') == 'on'
        obra.compositor = request.POST.get('compositor', obra.compositor)
        obra.bibliotecas_musica = request.POST.get('bibliotecas_musica', obra.bibliotecas_musica)
        obra.bibliografia_musica = request.POST.get('bibliografia_musica', obra.bibliografia_musica)
        obra.mecenas = request.POST.get('mecenas', obra.mecenas)
        obra.edicion_principe = request.POST.get('edicion_principe', obra.edicion_principe)
        obra.notas_bibliograficas = request.POST.get('notas_bibliograficas', obra.notas_bibliograficas)
        obra.notas = request.POST.get('notas', obra.notas)
        obra.origen_datos = request.POST.get('origen_datos', obra.origen_datos)
        obra.pagina_pdf = request.POST.get('pagina_pdf') or None
        obra.texto_original_pdf = request.POST.get('texto_original_pdf', obra.texto_original_pdf)
        
        # Actualizar autor si se proporciona
        autor_id = request.POST.get('autor')
        if autor_id:
            from apps.autores.models import Autor
            try:
                autor = Autor.objects.get(id=autor_id)
                obra.autor = autor
            except Autor.DoesNotExist:
                pass
        
        obra.save()
        messages.success(request, f'Obra "{obra.titulo_limpio}" actualizada correctamente.')
        
        # Redirigir de vuelta al catálogo correspondiente
        fuente_map = {'FUENTESXI': 'fuentesxi', 'CATCOM': 'catcom'}
        return redirect('catalogo_detalle', catalogo_id=fuente_map.get(obra.fuente_principal, 'fuentesxi'))
    
    # Obtener opciones para los selects
    from apps.autores.models import Autor
    autores = Autor.objects.all().order_by('nombre')
    
    context = {
        'obra': obra,
        'autores': autores,
        'tipo_obra_choices': Obra.TIPO_OBRA_CHOICES,
    }
    
    return render(request, 'obras/obra_edit.html', context)

def pagina_pdf_view(request, numero_pagina):
    """Vista para mostrar una página específica del PDF"""
    pagina = get_object_or_404(PaginaPDF, numero_pagina=numero_pagina)
    
    context = {
        'pagina': pagina,
    }
    
    return render(request, 'obras/pagina_pdf.html', context)

def pagina_pdf_modal(request, numero_pagina):
    """Vista AJAX para mostrar una página del PDF en un modal"""
    pagina = get_object_or_404(PaginaPDF, numero_pagina=numero_pagina)
    
    context = {
        'pagina': pagina,
    }
    
    return render(request, 'obras/pagina_pdf_modal.html', context)

def busqueda_avanzada_view(request):
    """Vista para búsqueda semántica y avanzada"""
    query = request.GET.get('q', '')
    tipo_busqueda = request.GET.get('tipo', 'semantica')
    tema = request.GET.get('tema', '')
    mecenas = request.GET.get('mecenas', '')
    compositor = request.GET.get('compositor', '')
    musica_conservada = request.GET.get('musica_conservada', '')
    
    obras = Obra.objects.all()
    
    # Búsqueda semántica en notas bibliográficas
    if query and tipo_busqueda == 'semantica':
        obras = obras.filter(
            Q(notas_bibliograficas__icontains=query) |
            Q(notas__icontains=query) |
            Q(edicion_principe__icontains=query) |
            Q(observaciones__icontains=query)
        )
    elif query:
        # Búsqueda normal
        obras = obras.filter(
            Q(titulo__icontains=query) |
            Q(titulo_limpio__icontains=query) |
            Q(autor__nombre__icontains=query) |
            Q(tema__icontains=query)
        )
    
    # Filtros adicionales
    if tema:
        obras = obras.filter(temas_literarios__tema__nombre__icontains=tema)
    
    if mecenas:
        obras = obras.filter(mecenas__icontains=mecenas)
    
    if compositor:
        obras = obras.filter(compositor__icontains=compositor)
    
    if musica_conservada == 'true':
        obras = obras.filter(musica_conservada=True)
    elif musica_conservada == 'false':
        obras = obras.filter(musica_conservada=False)
    
    # Estadísticas de búsqueda
    stats = {
        'total_resultados': obras.count(),
        'con_musica': obras.filter(musica_conservada=True).count(),
        'con_mecenas': obras.exclude(mecenas='').count(),
        'con_compositor': obras.exclude(compositor='').count(),
    }
    
    # Obtener temas disponibles para filtros
    temas_disponibles = TemaLiterario.objects.all().order_by('tipo_tema', 'nombre')
    
    # Obtener mecenas únicos
    mecenas_disponibles = Obra.objects.exclude(mecenas='').values_list('mecenas', flat=True).distinct().order_by('mecenas')
    
    # Obtener compositores únicos
    compositores_disponibles = Obra.objects.exclude(compositor='').values_list('compositor', flat=True).distinct().order_by('compositor')
    
    # Paginación
    from django.core.paginator import Paginator
    paginator = Paginator(obras.order_by('titulo_limpio'), 20)
    page = request.GET.get('page', 1)
    obras_page = paginator.get_page(page)
    
    context = {
        'obras': obras_page,
        'query': query,
        'tipo_busqueda': tipo_busqueda,
        'tema': tema,
        'mecenas': mecenas,
        'compositor': compositor,
        'musica_conservada': musica_conservada,
        'stats': stats,
        'temas_disponibles': temas_disponibles,
        'mecenas_disponibles': mecenas_disponibles,
        'compositores_disponibles': compositores_disponibles,
        'paginator': paginator,
    }
    
    return render(request, 'obras/busqueda_avanzada.html', context)

def redes_colaboracion_view(request):
    """Vista para análisis de redes de colaboración entre autores y compañías"""
    from django.db.models import Count, Q
    
    # Red de colaboración entre autores (obras co-escritas o relacionadas)
    autores_colaboracion = []
    autores = Autor.objects.annotate(
        total_obras=Count('obras'),
        total_representaciones=Count('obras__representaciones')
    ).filter(total_obras__gt=0).order_by('-total_obras')[:20]
    
    for autor in autores:
        # Buscar otros autores que hayan trabajado en las mismas compañías
        compañias_autor = Representacion.objects.filter(
            obra__autor=autor
        ).values_list('compañia', flat=True).distinct()
        
        colaboradores = []
        for compañia in compañias_autor:
            if compañia:
                otros_autores = Autor.objects.filter(
                    obras__representaciones__compañia=compañia
                ).exclude(id=autor.id).distinct()
                for otro_autor in otros_autores:
                    if otro_autor not in [c['autor'] for c in colaboradores]:
                        colaboradores.append({
                            'autor': otro_autor,
                            'compañia': compañia,
                            'obras_comunes': 0  # Se puede calcular después
                        })
        
        autores_colaboracion.append({
            'autor': autor,
            'total_obras': autor.total_obras,
            'total_representaciones': autor.total_representaciones,
            'colaboradores': colaboradores[:5]  # Limitar a 5 colaboradores
        })
    
    # Red de compañías (compañías que han trabajado con los mismos autores)
    compañias_colaboracion = []
    compañias = Representacion.objects.exclude(
        compañia=''
    ).values('compañia').annotate(
        total_representaciones=Count('id'),
        autores_unicos=Count('obra__autor', distinct=True)
    ).order_by('-total_representaciones')[:15]
    
    for compañia_data in compañias:
        compañia_nombre = compañia_data['compañia']
        
        # Obtener autores que han trabajado con esta compañía
        autores_compañia = Autor.objects.filter(
            obras__representaciones__compañia=compañia_nombre
        ).distinct()
        
        # Buscar otras compañías que hayan trabajado con los mismos autores
        compañias_relacionadas = []
        for autor in autores_compañia:
            otras_compañias = Representacion.objects.filter(
                obra__autor=autor
            ).exclude(compañia=compañia_nombre).exclude(
                compañia=''
            ).values('compañia').annotate(
                count=Count('id')
            ).order_by('-count')[:3]
            
            for otra_compañia in otras_compañias:
                if otra_compañia['compañia'] not in [c['compañia'] for c in compañias_relacionadas]:
                    compañias_relacionadas.append({
                        'compañia': otra_compañia['compañia'],
                        'autor_comun': autor,
                        'representaciones': otra_compañia['count']
                    })
        
        compañias_colaboracion.append({
            'compañia': compañia_nombre,
            'total_representaciones': compañia_data['total_representaciones'],
            'autores_unicos': compañia_data['autores_unicos'],
            'autores': autores_compañia[:5],  # Limitar a 5 autores
            'compañias_relacionadas': compañias_relacionadas[:5]
        })
    
    # Estadísticas generales
    stats = {
        'total_autores': Autor.objects.count(),
        'autores_con_obras': Autor.objects.annotate(
            total_obras=Count('obras')
        ).filter(total_obras__gt=0).count(),
        'total_compañias': Representacion.objects.exclude(
            compañia=''
        ).values('compañia').distinct().count(),
        'total_representaciones': Representacion.objects.count(),
    }
    
    context = {
        'autores_colaboracion': autores_colaboracion,
        'compañias_colaboracion': compañias_colaboracion,
        'stats': stats,
    }
    
    return render(request, 'obras/redes_colaboracion.html', context)

def mapas_geograficos_view(request):
    """Vista para mapas geográficos con seguimiento temporal de obras"""
    from django.db.models import Count, Min, Max
    from datetime import datetime
    
    # Obtener parámetros de filtro
    obra_id = request.GET.get('obra', '')
    autor_id = request.GET.get('autor', '')
    decada = request.GET.get('decada', '')
    lugar_id = request.GET.get('lugar', '')
    
    # Base query para representaciones
    representaciones = Representacion.objects.select_related(
        'obra', 'lugar', 'obra__autor'
    ).filter(
        fecha_formateada__isnull=False,
        lugar__isnull=False
    ).order_by('fecha_formateada')
    
    # Filtros
    if obra_id:
        representaciones = representaciones.filter(obra_id=obra_id)
    
    if autor_id:
        representaciones = representaciones.filter(obra__autor_id=autor_id)
    
    if decada:
        # Convertir década (ej: "1650s") a rango de años
        año_inicio = int(decada.replace('s', ''))
        año_fin = año_inicio + 9
        representaciones = representaciones.filter(
            fecha_formateada__year__gte=año_inicio,
            fecha_formateada__year__lte=año_fin
        )
    
    if lugar_id:
        representaciones = representaciones.filter(lugar_id=lugar_id)
    
    # Agrupar representaciones por lugar y año
    lugares_temporales = {}
    for rep in representaciones:
        lugar_key = f"{rep.lugar.id}_{rep.lugar.nombre}"
        año = rep.fecha_formateada.year
        
        if lugar_key not in lugares_temporales:
            lugares_temporales[lugar_key] = {
                'lugar': rep.lugar,
                'representaciones_por_año': {},
                'total_representaciones': 0,
                'obras_unicas': set(),
                'autores_unicos': set(),
                'fecha_primera': rep.fecha_formateada,
                'fecha_ultima': rep.fecha_formateada
            }
        
        lugar_data = lugares_temporales[lugar_key]
        
        # Contar por año
        if año not in lugar_data['representaciones_por_año']:
            lugar_data['representaciones_por_año'][año] = {
                'count': 0,
                'obras': set(),
                'fechas': []
            }
        
        lugar_data['representaciones_por_año'][año]['count'] += 1
        lugar_data['representaciones_por_año'][año]['obras'].add(rep.obra.titulo_limpio)
        lugar_data['representaciones_por_año'][año]['fechas'].append(rep.fecha_formateada)
        
        # Actualizar estadísticas generales
        lugar_data['total_representaciones'] += 1
        lugar_data['obras_unicas'].add(rep.obra.titulo_limpio)
        lugar_data['autores_unicos'].add(rep.obra.autor.nombre if rep.obra.autor else 'Desconocido')
        
        # Actualizar fechas
        if rep.fecha_formateada < lugar_data['fecha_primera']:
            lugar_data['fecha_primera'] = rep.fecha_formateada
        if rep.fecha_formateada > lugar_data['fecha_ultima']:
            lugar_data['fecha_ultima'] = rep.fecha_formateada
    
    # Convertir sets a listas para JSON
    for lugar_data in lugares_temporales.values():
        lugar_data['obras_unicas'] = list(lugar_data['obras_unicas'])
        lugar_data['autores_unicos'] = list(lugar_data['autores_unicos'])
        
        # Convertir fechas a strings para JSON
        for año_data in lugar_data['representaciones_por_año'].values():
            año_data['obras'] = list(año_data['obras'])
            año_data['fechas'] = [fecha.isoformat() for fecha in año_data['fechas']]
    
    # Obtener datos para filtros
    obras_disponibles = Obra.objects.filter(
        representaciones__lugar__isnull=False
    ).distinct().order_by('titulo_limpio')[:50]
    
    autores_disponibles = Autor.objects.filter(
        obras__representaciones__lugar__isnull=False
    ).distinct().order_by('nombre')[:30]
    
    lugares_disponibles = Representacion.objects.exclude(
        lugar__isnull=True
    ).values('lugar__id', 'lugar__nombre').distinct().order_by('lugar__nombre')
    
    # Décadas disponibles
    decadas_disponibles = []
    años = Representacion.objects.filter(
        fecha_formateada__isnull=False
    ).values_list('fecha_formateada__year', flat=True).distinct().order_by('fecha_formateada__year')
    
    for año in años:
        decada = f"{año//10*10}s"
        if decada not in decadas_disponibles:
            decadas_disponibles.append(decada)
    
    # Estadísticas generales
    stats = {
        'total_lugares': len(lugares_temporales),
        'total_representaciones': sum(data['total_representaciones'] for data in lugares_temporales.values()),
        'total_obras': len(set(obra for data in lugares_temporales.values() for obra in data['obras_unicas'])),
        'total_autores': len(set(autor for data in lugares_temporales.values() for autor in data['autores_unicos'])),
    }
    
    context = {
        'lugares_temporales': lugares_temporales,
        'obras_disponibles': obras_disponibles,
        'autores_disponibles': autores_disponibles,
        'lugares_disponibles': lugares_disponibles,
        'decadas_disponibles': decadas_disponibles,
        'stats': stats,
        'filtros_actuales': {
            'obra': obra_id,
            'autor': autor_id,
            'decada': decada,
            'lugar': lugar_id,
        }
    }
    
    return render(request, 'obras/mapas_geograficos.html', context)


@require_http_methods(["POST"])
def save_comment_ajax(request, catalogo_id):
    """Vista AJAX para guardar comentarios de usuario sobre selecciones de obras"""
    try:
        import json
        from django.contrib.auth.decorators import login_required
        from django.utils.decorators import method_decorator
        
        # Verificar que el usuario esté autenticado
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Usuario no autenticado'
            }, status=401)
        
        # Obtener datos del request
        data = json.loads(request.body)
        
        titulo = data.get('titulo', '').strip()
        comentario = data.get('comentario', '').strip()
        es_publico = data.get('es_publico', False)
        etiqueta_ia = data.get('etiqueta_ia', False)
        elementos_seleccionados = data.get('elementos_seleccionados', [])
        
        # Validar datos
        if not titulo:
            return JsonResponse({
                'success': False,
                'error': 'El título es obligatorio'
            })
        
        if not comentario:
            return JsonResponse({
                'success': False,
                'error': 'El comentario es obligatorio'
            })
        
        if not elementos_seleccionados:
            return JsonResponse({
                'success': False,
                'error': 'Debe seleccionar al menos un elemento'
            })
        
        # Verificar que los elementos existen
        obras_ids = []
        for elemento in elementos_seleccionados:
            section = elemento.get('section')
            item_id = elemento.get('item_id')
            
            if section == 'obras':
                try:
                    obra = Obra.objects.get(id=item_id)
                    obras_ids.append(obra.id)
                except Obra.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': f'La obra con ID {item_id} no existe'
                    })
            # Para otras secciones, por ahora solo asociamos con obras
            # En el futuro se puede extender para manejar otros tipos de elementos
        
        if not obras_ids:
            return JsonResponse({
                'success': False,
                'error': 'No se encontraron obras válidas para asociar'
            })
        
        # Crear comentario
        comentario_obj = ComentarioUsuario.objects.create(
            usuario=request.user,
            catalogo=catalogo_id,
            titulo=titulo,
            comentario=comentario,
            es_publico=es_publico,
            etiqueta_ia=etiqueta_ia
        )
        
        # Asociar obras seleccionadas
        obras = Obra.objects.filter(id__in=obras_ids)
        comentario_obj.obras_seleccionadas.set(obras)
        
        return JsonResponse({
            'success': True,
            'message': 'Comentario guardado exitosamente',
            'comentario_id': comentario_obj.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al guardar el comentario: {str(e)}'
        })


@require_http_methods(["GET"])
def get_comments_ajax(request, catalogo_id):
    """Vista AJAX para obtener comentarios de usuario"""
    try:
        from django.contrib.auth.decorators import login_required
        
        # Verificar que el usuario esté autenticado
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Usuario no autenticado'
            }, status=401)
        
        # Obtener comentarios del usuario para este catálogo
        comentarios = ComentarioUsuario.objects.filter(
            usuario=request.user,
            catalogo=catalogo_id
        ).order_by('-fecha_creacion')
        
        # Serializar comentarios
        comentarios_data = []
        for comentario in comentarios:
            comentarios_data.append({
                'id': comentario.id,
                'titulo': comentario.titulo,
                'comentario': comentario.comentario,
                'fecha_creacion': comentario.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
                'es_publico': comentario.es_publico,
                'numero_obras': comentario.numero_obras,
                'obras_titulos': comentario.obras_titulos
            })
        
        return JsonResponse({
            'success': True,
            'comentarios': comentarios_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al cargar los comentarios: {str(e)}'
        })


@require_http_methods(["POST"])
def save_obra_comment(request, obra_id):
    """Vista para guardar un comentario sobre una obra específica"""
    try:
        import json
        
        # Verificar autenticación
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Usuario no autenticado'
            }, status=401)
        
        # Obtener la obra
        obra = get_object_or_404(Obra, id=obra_id)
        
        # Obtener datos del request
        data = json.loads(request.body)
        
        titulo = data.get('titulo', '').strip()
        comentario = data.get('comentario', '').strip()
        es_publico = data.get('es_publico', False)
        etiqueta_ia = data.get('etiqueta_ia', False)
        
        # Validar datos
        if not titulo:
            return JsonResponse({
                'success': False,
                'error': 'El título es obligatorio'
            })
        
        if not comentario:
            return JsonResponse({
                'success': False,
                'error': 'El comentario es obligatorio'
            })
        
        # Determinar el catálogo según la fuente de la obra
        catalogo = 'fuentesxi' if obra.fuente_principal == 'FUENTESXI' else 'catcom'
        
        # Crear comentario
        comentario_obj = ComentarioUsuario.objects.create(
            usuario=request.user,
            catalogo=catalogo,
            titulo=titulo,
            comentario=comentario,
            es_publico=es_publico,
            etiqueta_ia=etiqueta_ia
        )
        
        # Asociar la obra
        comentario_obj.obras_seleccionadas.add(obra)
        
        return JsonResponse({
            'success': True,
            'message': 'Comentario guardado exitosamente',
            'comentario_id': comentario_obj.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al guardar el comentario: {str(e)}'
        })


@require_http_methods(["GET"])
def get_obra_comments(request, obra_id):
    """Vista para obtener comentarios de una obra específica"""
    try:
        # Verificar autenticación
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Usuario no autenticado'
            }, status=401)
        
        # Obtener la obra
        obra = get_object_or_404(Obra, id=obra_id)
        
        # Obtener comentarios de esta obra
        # Si el usuario es el autor, mostrar todos sus comentarios (públicos y privados)
        # También mostrar comentarios públicos de otros usuarios
        comentarios = ComentarioUsuario.objects.filter(
            obras_seleccionadas=obra
        ).filter(
            Q(usuario=request.user) | Q(es_publico=True)
        ).select_related('usuario').order_by('-fecha_creacion')
        
        # Serializar comentarios
        comentarios_data = []
        for comentario in comentarios:
            comentarios_data.append({
                'id': comentario.id,
                'titulo': comentario.titulo,
                'comentario': comentario.comentario,
                'fecha_creacion': comentario.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
                'es_publico': comentario.es_publico,
                'usuario': comentario.usuario.get_full_name() or comentario.usuario.username,
                'es_mio': comentario.usuario == request.user
            })
        
        return JsonResponse({
            'success': True,
            'comentarios': comentarios_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al cargar los comentarios: {str(e)}'
        })


@require_http_methods(["POST"])
def delete_comment(request, comentario_id):
    """Vista para eliminar un comentario"""
    try:
        # Verificar autenticación
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Usuario no autenticado'
            }, status=401)
        
        # Obtener el comentario
        comentario = get_object_or_404(ComentarioUsuario, id=comentario_id)
        
        # Verificar que el usuario sea el autor del comentario
        if comentario.usuario != request.user:
            return JsonResponse({
                'success': False,
                'error': 'No tienes permiso para eliminar este comentario'
            }, status=403)
        
        # Eliminar el comentario
        comentario.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Comentario eliminado exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al eliminar el comentario: {str(e)}'
        })


@require_http_methods(["GET"])
def exportar_comentarios_ia(request):
    """🤖 Exporta comentarios etiquetados para IA como archivo TXT"""
    from django.http import HttpResponse
    from datetime import datetime
    
    # Verificar autenticación (opcional - puedes hacerlo público si quieres)
    if not request.user.is_authenticated:
        return HttpResponse('No autorizado', status=401)
    
    # Obtener parámetros opcionales
    catalogo = request.GET.get('catalogo', '')  # 'fuentesxi', 'catcom', o vacío para todos
    usuario_id = request.GET.get('usuario', '')  # Filtrar por usuario específico
    
    # Obtener comentarios con etiqueta IA
    comentarios = ComentarioUsuario.objects.filter(
        etiqueta_ia=True
    ).select_related('usuario').prefetch_related('obras_seleccionadas__autor').order_by('-fecha_creacion')
    
    # Filtros opcionales
    if catalogo:
        comentarios = comentarios.filter(catalogo=catalogo)
    
    if usuario_id:
        comentarios = comentarios.filter(usuario_id=usuario_id)
    
    # Generar contenido del archivo TXT
    contenido = f"EXPORTACIÓN DE COMENTARIOS PARA IA\n"
    contenido += f"Fecha de exportación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    contenido += f"Total de comentarios: {comentarios.count()}\n"
    contenido += "="*70 + "\n\n"
    
    for comentario in comentarios:
        contenido += comentario.exportar_para_ia()
    
    # Crear respuesta HTTP con el archivo
    response = HttpResponse(contenido, content_type='text/plain; charset=utf-8')
    
    # Nombre del archivo con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"comentarios_ia_{catalogo if catalogo else 'todos'}_{timestamp}.txt"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@require_http_methods(["GET"])
def exportar_todos_comentarios(request):
    """📥 Exporta TODOS los comentarios públicos como archivo TXT"""
    from django.http import HttpResponse
    from datetime import datetime
    
    # Obtener parámetros opcionales
    catalogo = request.GET.get('catalogo', '')  # 'fuentesxi', 'catcom', o vacío para todos
    usuario_id = request.GET.get('usuario', '')  # Filtrar por usuario específico
    
    # Obtener todos los comentarios públicos (o todos si es admin)
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        # Admins pueden exportar todos los comentarios (públicos y privados)
        comentarios = ComentarioUsuario.objects.all()
    else:
        # Usuarios normales solo ven comentarios públicos
        comentarios = ComentarioUsuario.objects.filter(es_publico=True)
    
    comentarios = comentarios.select_related('usuario').prefetch_related('obras_seleccionadas__autor').order_by('-fecha_creacion')
    
    # Filtros opcionales
    if catalogo:
        comentarios = comentarios.filter(catalogo=catalogo)
    
    if usuario_id:
        comentarios = comentarios.filter(usuario_id=usuario_id)
    
    # Generar contenido del archivo TXT
    contenido = f"EXPORTACIÓN DE COMENTARIOS PÚBLICOS\n"
    contenido += f"Fecha de exportación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    contenido += f"Total de comentarios: {comentarios.count()}\n"
    if catalogo:
        contenido += f"Catálogo filtrado: {catalogo.upper()}\n"
    contenido += "="*70 + "\n\n"
    
    for comentario in comentarios:
        contenido += comentario.exportar_para_ia()
    
    # Crear respuesta HTTP con el archivo
    response = HttpResponse(contenido, content_type='text/plain; charset=utf-8')
    
    # Nombre del archivo con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    tipo = 'todos' if not catalogo else catalogo
    filename = f"comentarios_{tipo}_{timestamp}.txt"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
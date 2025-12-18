"""
Vistas para validación de análisis de IA por investigadores
"""

import json
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.db import transaction
from django.utils.dateparse import parse_datetime

from .models import Obra
from apps.representaciones.models import Representacion
from apps.lugares.models import Lugar


@login_required
def validacion_analisis_list(request):
    """
    Lista todos los archivos de síntesis disponibles para validación
    """
    # Buscar archivos de síntesis en data/fuentesix
    sintesis_dir = os.path.join(settings.BASE_DIR, 'data', 'fuentesix')
    archivos_sintesis = []
    
    if os.path.exists(sintesis_dir):
        for archivo in os.listdir(sintesis_dir):
            if archivo.endswith('_sintesis_validacion.json'):
                ruta_completa = os.path.join(sintesis_dir, archivo)
                try:
                    with open(ruta_completa, 'r', encoding='utf-8') as f:
                        datos = json.load(f)
                    
                    metadata = datos.get('metadata_archivo', {})
                    archivos_sintesis.append({
                        'archivo': archivo,
                        'ruta': ruta_completa,
                        'fecha_extraccion': metadata.get('fecha_extraccion', 'Desconocida'),
                        'archivo_fuente': metadata.get('archivo_fuente', 'Desconocido'),
                        'total_representaciones': len(datos.get('representaciones', [])),
                        'total_obras': len(datos.get('obras', [])),
                        'total_lugares': len(datos.get('lugares', [])),
                        'fecha_generacion': datos.get('fecha_generacion', 'Desconocida')
                    })
                except Exception as e:
                    continue
    
    archivos_sintesis.sort(key=lambda x: x['fecha_generacion'], reverse=True)
    
    return render(request, 'obras/validacion_analisis_list.html', {
        'archivos_sintesis': archivos_sintesis
    })


@login_required
def validacion_analisis_detail(request, nombre_archivo):
    """
    Muestra síntesis detalladas de un archivo para validación
    """
    sintesis_dir = os.path.join(settings.BASE_DIR, 'data', 'fuentesix')
    ruta_archivo = os.path.join(sintesis_dir, nombre_archivo)
    
    if not os.path.exists(ruta_archivo):
        messages.error(request, f'Archivo {nombre_archivo} no encontrado')
        return redirect('validacion_analisis_list')
    
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    # Organizar por tipo y estado de validación
    representaciones = datos.get('representaciones', [])
    obras = datos.get('obras', [])
    lugares = datos.get('lugares', [])
    
    # Contar por nivel de confianza
    confianza_stats = {
        'alto': sum(1 for r in representaciones if r.get('confianza') == 'alto'),
        'medio': sum(1 for r in representaciones if r.get('confianza') == 'medio'),
        'bajo': sum(1 for r in representaciones if r.get('confianza') == 'bajo')
    }
    
    return render(request, 'obras/validacion_analisis_detail.html', {
        'archivo': nombre_archivo,
        'metadata_archivo': datos.get('metadata_archivo', {}),
        'representaciones': representaciones,
        'obras': obras,
        'lugares': lugares,
        'confianza_stats': confianza_stats,
        'total_items': len(representaciones) + len(obras) + len(lugares)
    })


@login_required
@require_http_methods(["POST"])
def validar_item(request):
    """
    Valida un item individual (representación, obra, lugar)
    """
    data = json.loads(request.body)
    
    tipo = data.get('tipo')  # 'representacion', 'obra', 'lugar'
    id_temporal = data.get('id_temporal')
    accion = data.get('accion')  # 'validar' o 'rechazar'
    archivo_sintesis = data.get('archivo_sintesis')
    comentario = data.get('comentario', '')
    
    if accion not in ['validar', 'rechazar']:
        return JsonResponse({'success': False, 'error': 'Acción no válida'})
    
    try:
        # Cargar archivo de síntesis
        sintesis_dir = os.path.join(settings.BASE_DIR, 'data', 'fuentesix')
        ruta_archivo = os.path.join(sintesis_dir, archivo_sintesis)
        
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            datos_sintesis = json.load(f)
        
        # Encontrar el item
        items = []
        if tipo == 'representacion':
            items = datos_sintesis.get('representaciones', [])
        elif tipo == 'obra':
            items = datos_sintesis.get('obras', [])
        elif tipo == 'lugar':
            items = datos_sintesis.get('lugares', [])
        
        item = next((i for i in items if i.get('id_temporal') == id_temporal), None)
        
        if not item:
            return JsonResponse({'success': False, 'error': 'Item no encontrado'})
        
        # Actualizar estado de validación
        if 'validacion' not in item:
            item['validacion'] = {}
        
            from datetime import datetime
            item['validacion'] = {
                'estado': 'validado' if accion == 'validar' else 'rechazado',
                'fecha': datetime.now().isoformat(),
                'usuario': request.user.username if hasattr(request.user, 'username') else 'usuario',
                'usuario_id': str(request.user.id) if hasattr(request.user, 'id') else None,
                'comentario': comentario
            }
        
        # Guardar archivo actualizado
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos_sintesis, f, indent=2, ensure_ascii=False)
        
        # Si se valida, integrar a la DB
        if accion == 'validar':
            resultado_integracion = integrar_item_a_db(item, tipo, request.user)
            return JsonResponse({
                'success': True,
                'mensaje': f'Item {accion}do correctamente',
                'integracion': resultado_integracion
            })
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Item {accion}do correctamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@transaction.atomic
def integrar_item_a_db(item: dict, tipo: str, usuario):
    """
    Integra un item validado a la base de datos
    
    Returns:
        Dict con resultado de la integración
    """
    datos_json = item.get('datos_json', {})
    metadata = item.get('metadata', {})
    
    resultado = {
        'exito': False,
        'tipo': tipo,
        'id_creado': None,
        'mensaje': ''
    }
    
    try:
        if tipo == 'representacion':
            # Crear o actualizar representación
            obra_titulo = datos_json.get('obra_titulo', '')
            
            # Buscar obra existente o crear nueva
            obra, creada = Obra.objects.get_or_create(
                titulo=obra_titulo,
                defaults={
                    'titulo_limpio': obra_titulo,
                    'fuente_principal': 'FUENTESXI',
                    'origen_datos': 'pdf',
                    'pagina_pdf': metadata.get('pagina_pdf'),
                    'texto_original_pdf': metadata.get('texto_original', '')
                }
            )
            
            # Crear representación
            fecha_str = datos_json.get('fecha_formateada') or datos_json.get('fecha', '')
            lugar_nombre = datos_json.get('lugar_nombre', '')
            
            # Buscar lugar
            lugar = None
            if lugar_nombre:
                lugar = Lugar.objects.filter(nombre__icontains=lugar_nombre).first()
                if not lugar:
                    lugar = Lugar.objects.create(
                        nombre=lugar_nombre,
                        tipo_lugar=datos_json.get('lugar_tipo', ''),
                        region=datos_json.get('lugar_region', ''),
                        ciudad=datos_json.get('lugar_ciudad', '')
                    )
            
            representacion = Representacion.objects.create(
                obra=obra,
                fecha=fecha_str,
                lugar=lugar,
                compañia=datos_json.get('compañia', ''),
                tipo_funcion=datos_json.get('tipo_funcion', ''),
                publico=datos_json.get('publico', ''),
                observaciones=datos_json.get('observaciones', ''),
                pagina_pdf=metadata.get('pagina_pdf'),
                texto_original_pdf=metadata.get('texto_original', '')
            )
            
            resultado['exito'] = True
            resultado['id_creado'] = representacion.id
            resultado['mensaje'] = f'Representación creada (ID: {representacion.id})'
        
        elif tipo == 'obra':
            # Crear obra
            titulo = datos_json.get('titulo', datos_json.get('obra_titulo', ''))
            obra = Obra.objects.create(
                titulo=titulo,
                titulo_limpio=titulo,
                fuente_principal='FUENTESXI',
                origen_datos='pdf',
                pagina_pdf=metadata.get('pagina_pdf'),
                texto_original_pdf=metadata.get('texto_original', '')
            )
            
            resultado['exito'] = True
            resultado['id_creado'] = obra.id
            resultado['mensaje'] = f'Obra creada (ID: {obra.id})'
        
        elif tipo == 'lugar':
            # Crear lugar
            nombre = datos_json.get('nombre', '')
            lugar = Lugar.objects.create(
                nombre=nombre,
                tipo_lugar=datos_json.get('tipo_lugar', ''),
                region=datos_json.get('region', ''),
                ciudad=datos_json.get('ciudad', ''),
                pais=datos_json.get('pais', 'España')
            )
            
            resultado['exito'] = True
            resultado['id_creado'] = lugar.id
            resultado['mensaje'] = f'Lugar creado (ID: {lugar.id})'
        
    except Exception as e:
        resultado['mensaje'] = f'Error al integrar: {str(e)}'
    
    return resultado


@login_required
@require_http_methods(["POST"])
def validar_lote(request):
    """
    Valida múltiples items a la vez
    """
    data = json.loads(request.body)
    
    items_validar = data.get('items', [])  # Lista de {tipo, id_temporal}
    archivo_sintesis = data.get('archivo_sintesis')
    accion = data.get('accion', 'validar')  # 'validar' o 'rechazar'
    
    resultados = []
    
    for item_data in items_validar:
        tipo = item_data.get('tipo')
        id_temporal = item_data.get('id_temporal')
        
        # Cargar archivo de síntesis
        sintesis_dir = os.path.join(settings.BASE_DIR, 'data', 'fuentesix')
        ruta_archivo = os.path.join(sintesis_dir, archivo_sintesis)
        
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            datos_sintesis = json.load(f)
        
        # Encontrar y validar item
        items = []
        if tipo == 'representacion':
            items = datos_sintesis.get('representaciones', [])
        elif tipo == 'obra':
            items = datos_sintesis.get('obras', [])
        elif tipo == 'lugar':
            items = datos_sintesis.get('lugares', [])
        
        item = next((i for i in items if i.get('id_temporal') == id_temporal), None)
        
        if item:
            if 'validacion' not in item:
                item['validacion'] = {}
            
            from datetime import datetime
            item['validacion'] = {
                'estado': 'validado' if accion == 'validar' else 'rechazado',
                'fecha': datetime.now().isoformat(),
                'usuario': request.user.username if hasattr(request.user, 'username') else 'usuario'
            }
            
            if accion == 'validar':
                resultado_integracion = integrar_item_a_db(item, tipo, request.user)
                resultados.append({
                    'id_temporal': id_temporal,
                    'exito': resultado_integracion.get('exito', False),
                    'mensaje': resultado_integracion.get('mensaje', '')
                })
            else:
                resultados.append({
                    'id_temporal': id_temporal,
                    'exito': True,
                    'mensaje': 'Rechazado correctamente'
                })
        
        # Guardar archivo actualizado
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos_sintesis, f, indent=2, ensure_ascii=False)
    
    return JsonResponse({
        'success': True,
        'resultados': resultados,
        'total': len(resultados)
    })







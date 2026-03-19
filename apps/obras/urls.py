from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import views_validacion

router = DefaultRouter()
router.register(r'obras', views.ObraViewSet)
router.register(r'manuscritos', views.ManuscritoViewSet)
router.register(r'temas-literarios', views.TemaLiterarioViewSet)
router.register(r'obra-temas', views.ObraTemaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Nuevas rutas del editor unificado
    path('editor/', views.editor_view, name='editor'),
    path('editor/<str:catalogo_id>/', views.editor_catalogo_view, name='editor_catalogo'),
    path('editor/<str:catalogo_id>/obra/<int:obra_id>/', views.obra_edit_ajax, name='obra_edit_ajax'),
    path('editor/<str:catalogo_id>/obra/<int:obra_id>/pdf-pages/', views.obra_pdf_pages_ajax, name='obra_pdf_pages_ajax'),
    path('editor/<str:catalogo_id>/<str:section>/<int:item_id>/pdf-pages/', views.section_pdf_pages_ajax, name='section_pdf_pages_ajax'),
    path('editor/busqueda/', views.busqueda_obras_ajax, name='busqueda_obras_ajax'),
    path('editor/<str:catalogo_id>/count/', views.count_obras_ajax, name='count_obras_ajax'),
    path('editor/<str:catalogo_id>/comentario/', views.save_comment_ajax, name='save_comment_ajax'),
    path('editor/<str:catalogo_id>/comentarios/', views.get_comments_ajax, name='get_comments_ajax'),
    path('editor/<str:catalogo_id>/<str:section>/', views.get_section_data_ajax, name='get_section_data_ajax'),
    path('editor/<str:catalogo_id>/<str:section>/<int:item_id>/', views.edit_item_ajax, name='edit_item_ajax'),
    # Rutas para comentarios en perfiles de obra
    path('<int:obra_id>/comentario/', views.save_obra_comment, name='save_obra_comment'),
    path('<int:obra_id>/comentarios/', views.get_obra_comments, name='get_obra_comments'),
    path('comentario/<int:comentario_id>/eliminar/', views.delete_comment, name='delete_comment'),

    # Comentarios estilo index.html (paridad con Supabase)
    path('comentarios-index/', views.index_crear_comentario, name='index_crear_comentario'),
    path('comentarios-index/global/', views.index_comentarios_global, name='index_comentarios_global'),
    path('comentarios-index/count-unseen/', views.index_comentarios_count_unseen, name='index_comentarios_count_unseen'),
    path('comentarios-index/obra/<int:obra_id>/', views.index_comentarios_obra, name='index_comentarios_obra'),
    path('comentarios-index/<int:comentario_id>/visto/', views.index_comentario_marcar_visto, name='index_comentario_marcar_visto'),
    path('comentarios-index/<int:comentario_id>/filtros/', views.index_comentario_filtros, name='index_comentario_filtros'),
    # Exportar comentarios
    path('comentarios/exportar-ia/', views.exportar_comentarios_ia, name='exportar_comentarios_ia'),
    path('comentarios/exportar-todos/', views.exportar_todos_comentarios, name='exportar_todos_comentarios'),
    # Propuestas de edición de obras (flujo validado)
    path('propuestas/', views.crear_propuesta_cambio_obra, name='crear_propuesta_cambio_obra'),
    path('propuestas/pendientes-usuario/', views.listar_propuestas_pendientes_usuario, name='listar_propuestas_pendientes_usuario'),
    path('propuestas/obra/<int:obra_id>/', views.listar_propuestas_obra, name='listar_propuestas_obra'),
    path('propuestas/<int:propuesta_id>/votar/', views.votar_propuesta_obra, name='votar_propuesta_obra'),
    path('propuestas/<int:propuesta_id>/resolver/', views.resolver_propuesta_obra, name='resolver_propuesta_obra'),
    # Rutas existentes (mantenidas para compatibilidad)
    path('catalogos/', views.catalogos_view, name='catalogos'),
    path('catalogos/<str:catalogo_id>/', views.catalogo_detalle_view, name='catalogo_detalle'),
    path('catalogo/', views.catalogo_view, name='catalogo'),  # 🔍 BUSCADOR PÚBLICO
    path('catalogo/count/', views.catalogo_count_ajax, name='catalogo_count_ajax'),  # Contador para buscador
    path('edit/<int:obra_id>/', views.obra_edit_view, name='obra_edit'),
    path('<int:obra_id>/', views.obra_detail_view, name='obra_detail'),
    path('pagina-pdf/<int:numero_pagina>/', views.pagina_pdf_view, name='pagina_pdf'),
    path('pagina-pdf-modal/<int:numero_pagina>/', views.pagina_pdf_modal, name='pagina_pdf_modal'),
    path('busqueda-avanzada/', views.busqueda_avanzada_view, name='busqueda_avanzada'),
    path('redes-colaboracion/', views.redes_colaboracion_view, name='redes_colaboracion'),
    path('mapas-geograficos/', views.mapas_geograficos_view, name='mapas_geograficos'),
    # Rutas de validación de análisis de IA
    path('validacion-analisis/', views_validacion.validacion_analisis_list, name='validacion_analisis_list'),
    path('validacion-analisis/<str:nombre_archivo>/', views_validacion.validacion_analisis_detail, name='validacion_analisis_detail'),
    path('validacion-analisis/api/archivos-sintesis/', views_validacion.archivos_sintesis_api, name='archivos_sintesis_api'),
    path('validacion-analisis/validar-item/', views_validacion.validar_item, name='validar_item'),
    path('validacion-analisis/validar-lote/', views_validacion.validar_lote, name='validar_lote'),
]

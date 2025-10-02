from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

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
    path('editor/busqueda/', views.busqueda_obras_ajax, name='busqueda_obras_ajax'),
    path('editor/<str:catalogo_id>/comentario/', views.save_comment_ajax, name='save_comment_ajax'),
    path('editor/<str:catalogo_id>/comentarios/', views.get_comments_ajax, name='get_comments_ajax'),
    path('editor/<str:catalogo_id>/<str:section>/', views.get_section_data_ajax, name='get_section_data_ajax'),
    path('editor/<str:catalogo_id>/<str:section>/<int:item_id>/', views.edit_item_ajax, name='edit_item_ajax'),
    # Rutas existentes (mantenidas para compatibilidad)
    path('catalogos/', views.catalogos_view, name='catalogos'),
    path('catalogos/<str:catalogo_id>/', views.catalogo_detalle_view, name='catalogo_detalle'),
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('edit/<int:obra_id>/', views.obra_edit_view, name='obra_edit'),
    path('<int:obra_id>/', views.obra_detail_view, name='obra_detail'),
    path('pagina-pdf/<int:numero_pagina>/', views.pagina_pdf_view, name='pagina_pdf'),
    path('pagina-pdf-modal/<int:numero_pagina>/', views.pagina_pdf_modal, name='pagina_pdf_modal'),
    path('busqueda-avanzada/', views.busqueda_avanzada_view, name='busqueda_avanzada'),
    path('redes-colaboracion/', views.redes_colaboracion_view, name='redes_colaboracion'),
    path('mapas-geograficos/', views.mapas_geograficos_view, name='mapas_geograficos'),
]

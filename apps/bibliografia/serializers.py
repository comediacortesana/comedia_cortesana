from rest_framework import serializers
from .models import ReferenciaBibliografica
from apps.obras.models import Obra


class ObraSerializer(serializers.ModelSerializer):
    """Serializer para obras en referencias bibliográficas"""
    
    class Meta:
        model = Obra
        fields = ['id', 'titulo_limpio', 'autor', 'tipo_obra']


class ReferenciaBibliograficaSerializer(serializers.ModelSerializer):
    """Serializer para referencias bibliográficas"""
    
    obra = ObraSerializer(read_only=True)
    cita_completa = serializers.ReadOnlyField()
    
    class Meta:
        model = ReferenciaBibliografica
        fields = [
            'id', 'obra', 'titulo', 'autor', 'editor', 'lugar_publicacion',
            'año_publicacion', 'paginas', 'tipo_referencia', 'url', 'isbn',
            'issn', 'doi', 'volumen', 'numero', 'revista', 'editorial',
            'coleccion', 'notas', 'created_at', 'updated_at', 'cita_completa'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ReferenciaBibliograficaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listas de referencias bibliográficas"""
    
    obra = ObraSerializer(read_only=True)
    cita_completa = serializers.ReadOnlyField()
    
    class Meta:
        model = ReferenciaBibliografica
        fields = [
            'id', 'obra', 'titulo', 'autor', 'año_publicacion', 'tipo_referencia',
            'cita_completa'
        ]

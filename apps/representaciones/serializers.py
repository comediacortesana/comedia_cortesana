from rest_framework import serializers
from .models import Representacion
from apps.obras.models import Obra
from apps.lugares.models import Lugar


class ObraSerializer(serializers.ModelSerializer):
    """Serializer para obras en representaciones"""
    
    class Meta:
        model = Obra
        fields = ['id', 'titulo_limpio', 'autor', 'tipo_obra']


class LugarSerializer(serializers.ModelSerializer):
    """Serializer para lugares en representaciones"""
    
    class Meta:
        model = Lugar
        fields = ['id', 'nombre', 'region', 'pais', 'tipo_lugar']


class RepresentacionSerializer(serializers.ModelSerializer):
    """Serializer para representaciones"""
    
    obra = ObraSerializer(read_only=True)
    lugar = LugarSerializer(read_only=True)
    siglo = serializers.ReadOnlyField()
    decada = serializers.ReadOnlyField()
    
    class Meta:
        model = Representacion
        fields = [
            'id', 'obra', 'fecha', 'fecha_formateada', 'compañia', 'lugar',
            'tipo_lugar', 'director_compañia', 'fuente', 'observaciones',
            'mecenas', 'gestor_administrativo', 'personajes_historicos',
            'organizadores_fiesta', 'es_anterior_1650', 'es_anterior_1665',
            'tipo_funcion', 'publico', 'entrada', 'duracion', 'notas', 
            'created_at', 'updated_at', 'siglo', 'decada'
        ]
        read_only_fields = ['created_at', 'updated_at']


class RepresentacionListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listas de representaciones"""
    
    obra = ObraSerializer(read_only=True)
    lugar = LugarSerializer(read_only=True)
    siglo = serializers.ReadOnlyField()
    decada = serializers.ReadOnlyField()
    
    class Meta:
        model = Representacion
        fields = [
            'id', 'obra', 'fecha_formateada', 'compañia', 'lugar',
            'tipo_lugar', 'siglo', 'decada'
        ]

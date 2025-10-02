from rest_framework import serializers
from .models import Lugar


class LugarSerializer(serializers.ModelSerializer):
    """Serializer para lugares"""
    
    total_representaciones = serializers.ReadOnlyField()
    coordenadas = serializers.ReadOnlyField()
    
    class Meta:
        model = Lugar
        fields = [
            'id', 'nombre', 'coordenadas_lat', 'coordenadas_lng', 'region', 'pais',
            'tipo_lugar', 'descripcion', 'poblacion_estimada', 'es_capital',
            'notas_historicas', 'created_at', 'updated_at', 'total_representaciones',
            'coordenadas'
        ]
        read_only_fields = ['created_at', 'updated_at']


class LugarListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listas de lugares"""
    
    total_representaciones = serializers.ReadOnlyField()
    
    class Meta:
        model = Lugar
        fields = ['id', 'nombre', 'region', 'pais', 'tipo_lugar', 'total_representaciones']

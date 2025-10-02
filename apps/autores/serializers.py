from rest_framework import serializers
from .models import Autor


class AutorSerializer(serializers.ModelSerializer):
    """Serializer para autores"""
    
    total_obras = serializers.ReadOnlyField()
    total_representaciones = serializers.ReadOnlyField()
    
    class Meta:
        model = Autor
        fields = [
            'id', 'nombre', 'nombre_completo', 'fecha_nacimiento', 'fecha_muerte',
            'biografia', 'obras_principales', 'epoca', 'notas', 'created_at', 'updated_at',
            'total_obras', 'total_representaciones'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AutorListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listas de autores"""
    
    total_obras = serializers.ReadOnlyField()
    
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'epoca', 'total_obras']

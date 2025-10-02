from rest_framework import serializers
from .models import Obra, Manuscrito, TemaLiterario, ObraTema
from apps.autores.models import Autor
from apps.lugares.models import Lugar


class AutorSerializer(serializers.ModelSerializer):
    """Serializer para autores"""
    
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'nombre_completo', 'epoca']


class LugarSerializer(serializers.ModelSerializer):
    """Serializer para lugares"""
    
    class Meta:
        model = Lugar
        fields = ['id', 'nombre', 'region', 'pais', 'tipo_lugar']


class ManuscritoSerializer(serializers.ModelSerializer):
    """Serializer para manuscritos"""
    
    class Meta:
        model = Manuscrito
        fields = ['id', 'ubicacion', 'signatura', 'fecha_manuscrito', 'tipo_manuscrito', 'descripcion']


class TemaLiterarioSerializer(serializers.ModelSerializer):
    """Serializer para temas literarios"""
    
    total_obras = serializers.ReadOnlyField()
    
    class Meta:
        model = TemaLiterario
        fields = ['id', 'nombre', 'tipo_tema', 'descripcion', 'total_obras']


class ObraTemaSerializer(serializers.ModelSerializer):
    """Serializer para relaciones obra-tema"""
    
    tema = TemaLiterarioSerializer(read_only=True)
    
    class Meta:
        model = ObraTema
        fields = ['id', 'tema', 'es_principal', 'notas']


class ObraSerializer(serializers.ModelSerializer):
    """Serializer para obras teatrales"""
    
    autor = AutorSerializer(read_only=True)
    manuscritos = ManuscritoSerializer(many=True, read_only=True)
    temas_literarios = ObraTemaSerializer(many=True, read_only=True, source='obratema_set')
    total_representaciones = serializers.ReadOnlyField()
    primera_representacion = serializers.ReadOnlyField()
    ultima_representacion = serializers.ReadOnlyField()
    lugares_representacion = serializers.ReadOnlyField()
    
    class Meta:
        model = Obra
        fields = [
            'id', 'titulo', 'titulo_limpio', 'titulo_alternativo', 'autor',
            'tipo_obra', 'genero', 'edicion_principe', 'notas_bibliograficas',
            'fuente_principal', 'tema', 'musica_conservada', 'compositor',
            'bibliotecas_musica', 'bibliografia_musica', 'mecenas', 
            'fecha_creacion_estimada', 'idioma', 'versos', 'actos',
            'notas', 'manuscritos_conocidos', 'ediciones_conocidas',
            'created_at', 'updated_at', 'manuscritos', 'temas_literarios',
            'total_representaciones', 'primera_representacion', 'ultima_representacion',
            'lugares_representacion'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ObraListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listas de obras"""
    
    autor = AutorSerializer(read_only=True)
    total_representaciones = serializers.ReadOnlyField()
    temas_literarios = ObraTemaSerializer(many=True, read_only=True, source='obratema_set')
    
    class Meta:
        model = Obra
        fields = [
            'id', 'titulo_limpio', 'autor', 'tipo_obra', 'genero',
            'fuente_principal', 'total_representaciones', 'temas_literarios'
        ]

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, PerfilUsuario


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Usuario
    """
    perfil = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'es_investigador', 'institucion', 'biografia', 'avatar',
            'fecha_registro', 'perfil'
        ]
        read_only_fields = ['id', 'fecha_registro']
    
    def get_perfil(self, obj):
        """Obtiene el perfil del usuario si existe"""
        try:
            perfil = obj.perfil
            return PerfilUsuarioSerializer(perfil).data
        except PerfilUsuario.DoesNotExist:
            return None


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo PerfilUsuario
    """
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    usuario_email = serializers.EmailField(source='usuario.email', read_only=True)
    
    class Meta:
        model = PerfilUsuario
        fields = [
            'id', 'usuario_nombre', 'usuario_email', 'especialidades',
            'intereses', 'publicaciones', 'redes_sociales',
            'perfil_publico', 'mostrar_email', 'mostrar_institucion',
            'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_actualizacion']


class RegistroSerializer(serializers.ModelSerializer):
    """
    Serializer para el registro de nuevos usuarios
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'es_investigador', 'institucion'
        ]
    
    def validate(self, attrs):
        """Valida que las contraseñas coincidan"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return attrs
    
    def create(self, validated_data):
        """Crea un nuevo usuario"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        usuario = Usuario.objects.create_user(
            password=password,
            **validated_data
        )
        
        # Crear perfil automáticamente
        PerfilUsuario.objects.create(usuario=usuario)
        
        return usuario


class LoginSerializer(serializers.Serializer):
    """
    Serializer para el login de usuarios
    """
    login_field = serializers.CharField()  # Puede ser email o username
    password = serializers.CharField()
    
    def validate(self, attrs):
        """Valida las credenciales del usuario"""
        login_field = attrs.get('login_field')
        password = attrs.get('password')
        
        if login_field and password:
            # Buscar usuario por email primero, luego por username
            try:
                try:
                    usuario = Usuario.objects.get(email=login_field)
                except Usuario.DoesNotExist:
                    try:
                        usuario = Usuario.objects.get(username=login_field)
                    except Usuario.DoesNotExist:
                        raise serializers.ValidationError('Credenciales inválidas.')
                
                user = authenticate(
                    request=self.context.get('request'),
                    username=usuario.username,
                    password=password
                )
                
                if not user:
                    raise serializers.ValidationError('Credenciales inválidas.')
                
                if not user.is_active:
                    raise serializers.ValidationError('La cuenta está desactivada.')
                
                attrs['user'] = user
                return attrs
                
            except Usuario.DoesNotExist:
                raise serializers.ValidationError('Credenciales inválidas.')
        else:
            raise serializers.ValidationError('Debe proporcionar usuario/email y contraseña.')


class CambioPasswordSerializer(serializers.Serializer):
    """
    Serializer para cambio de contraseña
    """
    password_actual = serializers.CharField()
    password_nueva = serializers.CharField(validators=[validate_password])
    password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        """Valida el cambio de contraseña"""
        if attrs['password_nueva'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las nuevas contraseñas no coinciden.")
        return attrs
    
    def validate_password_actual(self, value):
        """Valida la contraseña actual"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value

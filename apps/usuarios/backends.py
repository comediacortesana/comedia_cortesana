from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UsuarioBackend(ModelBackend):
    """
    Backend de autenticación personalizado para el modelo Usuario
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica un usuario usando username o email
        """
        identifier = username or kwargs.get("username") or kwargs.get("email")
        if identifier is None or password is None:
            return None
        
        try:
            # Buscar usuario por username o email (case-insensitive)
            user = User.objects.filter(
                Q(username__iexact=identifier) | Q(email__iexact=identifier)
            ).first()
            if user is None:
                User().set_password(password)
                return None
            
            # Verificar contraseña
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
                
        except Exception:
            # Ejecutar el hash de contraseña para evitar timing attacks
            User().set_password(password)
            
        return None
    
    def user_can_authenticate(self, user):
        """
        Rechazar usuarios con is_active=False. Los usuarios personalizados pueden
        tener is_active=False pero aún poder autenticarse.
        """
        return getattr(user, 'is_active', True)
    
    def get_user(self, user_id):
        """
        Obtener un usuario por ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None



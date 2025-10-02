from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser
    """
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    fecha_registro = models.DateTimeField(default=timezone.now, verbose_name="Fecha de registro")
    es_investigador = models.BooleanField(default=False, verbose_name="Es investigador")
    institucion = models.CharField(max_length=200, blank=True, verbose_name="Institución")
    biografia = models.TextField(blank=True, verbose_name="Biografía")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")
    
    # Campos de configuración
    notificaciones_email = models.BooleanField(default=True, verbose_name="Notificaciones por email")
    tema_oscuro = models.BooleanField(default=False, verbose_name="Tema oscuro")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_short_name(self):
        """Retorna el nombre corto del usuario"""
        return self.first_name or self.username


class PerfilUsuario(models.Model):
    """
    Modelo para información adicional del perfil de usuario
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
    especialidades = models.TextField(blank=True, verbose_name="Especialidades de investigación")
    intereses = models.TextField(blank=True, verbose_name="Intereses de investigación")
    publicaciones = models.TextField(blank=True, verbose_name="Publicaciones relevantes")
    redes_sociales = models.JSONField(default=dict, blank=True, verbose_name="Redes sociales")
    
    # Configuraciones de privacidad
    perfil_publico = models.BooleanField(default=True, verbose_name="Perfil público")
    mostrar_email = models.BooleanField(default=False, verbose_name="Mostrar email")
    mostrar_institucion = models.BooleanField(default=True, verbose_name="Mostrar institución")
    
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
    
    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name()}"


class SesionUsuario(models.Model):
    """
    Modelo para rastrear sesiones de usuario
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='sesiones')
    ip_address = models.GenericIPAddressField(verbose_name="Dirección IP")
    user_agent = models.TextField(verbose_name="User Agent")
    fecha_inicio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de inicio")
    fecha_ultima_actividad = models.DateTimeField(auto_now=True, verbose_name="Última actividad")
    activa = models.BooleanField(default=True, verbose_name="Sesión activa")
    
    class Meta:
        verbose_name = "Sesión de Usuario"
        verbose_name_plural = "Sesiones de Usuario"
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"Sesión de {self.usuario.username} - {self.fecha_inicio.strftime('%d/%m/%Y %H:%M')}"


from django.contrib.auth.models import User
from django.db import models

class PerfilUsuario(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('director', 'Director de plantel'),
        ('visor', 'Solo lectura'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

class PerfilUsuario(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('director', 'Director de Plantel'),
        ('personal', 'Personal Militar'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"

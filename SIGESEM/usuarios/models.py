from django.contrib.auth.models import User
from django.db import models

class PerfilUsuario(models.Model):
    ROLES = [
        ('administrador', 'Administrador'),
        ('encargado', 'Encargado de Plantel'),
        ('consulta', 'Usuario Consulta'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"

    @property
    def es_administrador(self):
        return self.rol == 'administrador'

    @property
    def es_encargado(self):
        return self.rol == 'encargado'

    @property
    def es_consulta(self):
        return self.rol == 'consulta'

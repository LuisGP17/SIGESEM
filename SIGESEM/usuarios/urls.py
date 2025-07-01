from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'usuarios'

urlpatterns = [
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('', views.lista_usuarios, name='lista_usuarios'),
    path('editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('redireccion/', views.redireccion_por_rol, name='redireccion_por_rol'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

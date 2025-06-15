from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    registrar_usuario,
    redireccion_por_rol,
    dashboard_admin,
    dashboard_plantel,
)

urlpatterns = [
    path('registrar/', registrar_usuario, name='registrar_usuario'),
    path('redireccion/', redireccion_por_rol, name='redireccion_por_rol'),
    path('admin/dashboard/', dashboard_admin, name='dashboard_admin'),
    path('plantel/dashboard/', dashboard_plantel, name='dashboard_plantel'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.redireccion_por_rol, name='redireccion_por_rol'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/plantel/', views.dashboard_plantel, name='dashboard_plantel'),
    path('dashboard/default/', views.dashboard_default, name='dashboard_default'),
]
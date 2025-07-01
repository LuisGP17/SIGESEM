from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Discentes
    path('discente/nuevo/', lambda r: views.crear_objeto(r,
         views.DiscenteForm), name='nuevo_discente'),
    path('discente/editar/<int:pk>/',
         views.editar_discente, name='editar_discente'),
    path('discentes/', views.lista_discentes, name='lista'),
    path('discentes/exportar/', views.exportar_discentes_excel,
         name='exportar_discentes_excel'),


    # Planteles
    path('planteles/', views.lista_planteles, name='lista_planteles'),
    path('planteles/nuevo/', views.nuevo_plantel, name='nuevo_plantel'),
    path('planteles/editar/<int:id>/',
         views.editar_plantel, name='editar_plantel'),
    path('planteles/eliminar/<int:id>/',
         views.eliminar_plantel, name='eliminar_plantel'),

    # Categorías
    path('categoria/nueva/', lambda r: views.crear_objeto(r,
         views.CategoriaDiscenteForm), name='nueva_categoria'),

    # Casos médico-legales
    path('caso/nuevo/', nuevo_caso_medico_legal, name='nuevo_caso'),
    path('casos/', views.lista_casos, name='lista_casos'),
    path('editar/<int:id>/', views.editar_caso, name='editar_caso'),
    path('casos/eliminar/<int:pk>/', views.eliminar_caso, name='eliminar_caso'),
    path('exportar/casos/excel/', views.exportar_casos_excel,
         name='exportar_casos_excel'),
    path('exportar/casos/pdf/', views.exportar_casos_pdf,
         name='exportar_casos_pdf'),

    # Bajas
    path('tipo-baja/nuevo/', nuevo_tipo_baja, name='nuevo_tipo_baja'),
    path('baja/nueva/', nueva_baja, name='nueva_baja'),
    path('bajas/', views.lista_bajas, name='lista_bajas'),
    path('bajas/editar/<int:id>/', views.editar_baja, name='editar_baja'),
    path('bajas/eliminar/<int:id>/', views.eliminar_baja, name='eliminar_baja'),
    path('bajas/exportar_excel/', exportar_bajas_excel,
         name='exportar_bajas_excel'),

    # Usuarios
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
]

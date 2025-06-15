from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from planteles import views as plantel_views
from django.shortcuts import redirect


def redireccion_dashboard(request):
    return redirect('dashboard')  # Usa el nombre de tu vista del dashboard


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('planteles.urls')),  # apunta a la app planteles
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('usuarios/', include('usuarios.urls')),
    path('', login_required(redireccion_dashboard), name='inicio'),
    path('dashboard/', include('usuarios.urls')),
]

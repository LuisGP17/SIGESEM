from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse
from .forms import RegistroUsuarioForm
from planteles.models import Discente, Baja, CasoMedicoLegal, Plantel

@user_passes_test(lambda u: u.is_superuser)
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.save()
            grupo = form.cleaned_data['group']
            usuario.groups.add(grupo)
            messages.success(
                request, f'El usuario "{usuario.username}" fue registrado correctamente.')
            form = RegistroUsuarioForm()  # Limpiar formulario después de guardar
        else:
            messages.error(
                request, "Por favor corrige los errores en el formulario.")
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def redireccion_por_rol(request):
    user = request.user
    if user.groups.filter(name='Administrador').exists():
        return redirect('dashboard_admin')
    elif user.groups.filter(name='Plantel').exists():
        return redirect('dashboard_plantel')
    else:
        # Vista para otros roles o usuarios sin grupo
        return redirect('dashboard_default')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Administrador').exists())
def dashboard_admin(request):
    # Puedes enviar datos para el dashboard si quieres
    return render(request, 'usuarios/dashboard_admin.html', {
        'mensaje': 'Bienvenido al panel de administrador',
        'usuario': request.user
    })


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Plantel').exists())
def dashboard_plantel(request):
    return render(request, 'usuarios/dashboard_plantel.html', {
        'mensaje': 'Bienvenido al panel del plantel',
        'usuario': request.user
    })


@login_required
def dashboard_default(request):
    return HttpResponse("Bienvenido a la vista por defecto para usuarios sin rol asignado")


@login_required
def dashboard_general(request):
    user = request.user
    context = {}

    if user.groups.filter(name='Administrador').exists():
        # Admin ve todos los datos generales
        context['total_discentes'] = Discente.objects.count()
        context['total_bajas'] = Baja.objects.count()
        context['total_casos'] = CasoMedicoLegal.objects.count()
        context['total_planteles'] = Plantel.objects.count()
    elif user.groups.filter(name='Plantel').exists():
        # Plantel ve solo los datos de su plantel
        # Aquí debes adaptar cómo obtener el plantel del usuario
        plantel_usuario = getattr(user, 'perfil', None)
        if plantel_usuario and hasattr(plantel_usuario, 'plantel'):
            plantel = plantel_usuario.plantel
            context['total_discentes'] = Discente.objects.filter(id_plantel=plantel).count()
            context['total_bajas'] = Baja.objects.filter(id_discente__id_plantel=plantel).count()
            context['total_casos'] = CasoMedicoLegal.objects.filter(id_discente__id_plantel=plantel).count()
            context['total_planteles'] = 1
        else:
            context['total_discentes'] = 0
            context['total_bajas'] = 0
            context['total_casos'] = 0
            context['total_planteles'] = 0
    else:
        # Otros roles o sin grupo
        context['total_discentes'] = 0
        context['total_bajas'] = 0
        context['total_casos'] = 0
        context['total_planteles'] = 0

    return render(request, 'planteles/dashboard.html', context)
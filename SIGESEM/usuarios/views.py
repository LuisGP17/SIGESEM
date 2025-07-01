from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegistroUsuarioForm
from django import forms

# Decorador para permitir solo superusuarios


def es_superusuario(user):
    return user.is_superuser

# Registrar usuario - ya tienes esta vista


@user_passes_test(es_superusuario)
@login_required
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
            return redirect('lista_usuarios')
        else:
            messages.error(
                request, "Por favor corrige los errores en el formulario.")
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})

# Listar usuarios


@user_passes_test(es_superusuario)
@login_required
def lista_usuarios(request):
    rol_filtrado = request.GET.get('rol')
    if rol_filtrado:
        usuarios = User.objects.filter(groups__name=rol_filtrado)
    else:
        usuarios = User.objects.all()
    roles = Group.objects.all()
    return render(request, 'usuarios/lista.html', {
        'usuarios': usuarios,
        'roles': roles,
        'rol_filtrado': rol_filtrado,
    })
# Formulario para editar usuario (sin contraseña)


class EditarUsuarioForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre', max_length=100)
    last_name = forms.CharField(label='Apellido', max_length=100)
    email = forms.EmailField(label='Correo electrónico')
    group = forms.ModelChoiceField(
        label='Rol', queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'group']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            grupos = self.instance.groups.all()
            self.fields['group'].initial = grupos[0] if grupos else None

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.groups.clear()
            user.groups.add(self.cleaned_data['group'])
        return user

# Editar usuario


@user_passes_test(es_superusuario)
@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Usuario "{usuario.username}" actualizado.')
            return redirect('lista_usuarios')
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = EditarUsuarioForm(instance=usuario)
    return render(request, 'usuarios/formulario.html', {'form': form, 'titulo': 'Editar Usuario'})

# Eliminar usuario con confirmación


@user_passes_test(es_superusuario)
@login_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, f'Usuario "{usuario.username}" eliminado.')
        return redirect('lista_usuarios')
    return render(request, 'usuarios/confirmar_eliminar.html', {'usuario': usuario})


@login_required
def redireccion_por_rol(request):
    # Simplemente redirige al dashboard general
    return redirect('planteles/dashboard.html')

